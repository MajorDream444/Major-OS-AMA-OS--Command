import hashlib
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE = Path(__file__).parents[1] / 'production.py'
spec = importlib.util.spec_from_file_location('production', MODULE)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


class ProductionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.sources = self.root / 'sources'
        self.outputs = self.root / 'outputs'
        self.sources.mkdir()
        self.source = self.sources / 'episode.mp4'
        self.source.write_bytes(b'fixture-video')
        self.source_hash = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.config_path = self.root / 'config.json'
        self.config_path.write_text(json.dumps({
            'schema_version': 'yawdie-production-config-1',
            'source_roots': [str(self.sources)],
            'output_root': str(self.outputs),
            'tools': {'ffmpeg': '/usr/bin/true', 'ffprobe': '/usr/bin/true', 'renderer': '/usr/bin/true'},
            'worker_identity': 'test-worker',
        }))
        self.config_path.chmod(0o600)
        self.manifest_path = self.root / 'manifest.json'
        self.manifest_path.write_text(json.dumps({
            'schema_version': 'yawdie-production-excerpt-1',
            'idempotency_key': 'expertise-excerpt-fixture-v1',
            'episode': '02',
            'title': 'What lives in your head is not expertise',
            'source': str(self.source),
            'source_sha256': self.source_hash,
            'start_seconds': 113,
            'end_seconds': 211,
            'style_version': 'maim-captions-1.1.0',
            'output_alias': 'expertise-clip-01',
            'review_required': True,
            'caption_replacements': {'notebook LM': 'NotebookLM'},
            'audio_peak_ceiling_db': -1.0,
        }))
        self.manifest_path.chmod(0o600)
        self.db = p.sqlite3.connect(self.root / 'state.sqlite')
        self.db.row_factory = p.sqlite3.Row
        p.initialize(self.db)
        p.acknowledge(self.db, 'a' * 40, 'test-worker', now=10)

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_duplicate_submission_returns_one_parent_and_stage_set(self):
        first = p.submit(self.db, self.config_path, self.manifest_path, now=20)
        second = p.submit(self.db, self.config_path, self.manifest_path, now=21)
        self.assertEqual(first['job_id'], second['job_id'])
        self.assertFalse(first['duplicate'])
        self.assertTrue(second['duplicate'])
        self.assertEqual(self.db.execute('select count(*) from production_jobs').fetchone()[0], 1)
        self.assertEqual(self.db.execute('select count(*) from production_stages').fetchone()[0], len(p.STAGES))

    def test_changed_content_requires_changed_manifest_and_key(self):
        first = p.submit(self.db, self.config_path, self.manifest_path, now=20)
        data = json.loads(self.manifest_path.read_text())
        data['idempotency_key'] = 'expertise-excerpt-fixture-v2'
        data['end_seconds'] = 210
        self.manifest_path.write_text(json.dumps(data))
        self.manifest_path.chmod(0o600)
        second = p.submit(self.db, self.config_path, self.manifest_path, now=21)
        self.assertNotEqual(first['job_id'], second['job_id'])

    def test_rejects_source_escape_symlink_and_unapproved_style(self):
        outside = self.root / 'outside.mp4'
        outside.write_bytes(b'outside')
        data = json.loads(self.manifest_path.read_text())
        data['source'] = str(outside)
        data['source_sha256'] = hashlib.sha256(outside.read_bytes()).hexdigest()
        self.manifest_path.write_text(json.dumps(data))
        self.manifest_path.chmod(0o600)
        with self.assertRaisesRegex(ValueError, 'outside approved roots'):
            p.submit(self.db, self.config_path, self.manifest_path)
        link = self.sources / 'link.mp4'
        link.symlink_to(outside)
        data['source'] = str(link)
        self.manifest_path.write_text(json.dumps(data))
        self.manifest_path.chmod(0o600)
        with self.assertRaises(ValueError):
            p.submit(self.db, self.config_path, self.manifest_path)

    def test_private_config_and_manifest_are_required(self):
        self.config_path.chmod(0o644)
        with self.assertRaisesRegex(ValueError, 'private'):
            p.submit(self.db, self.config_path, self.manifest_path)

    def test_active_word_ass_has_white_base_gold_overlay_and_thin_outline(self):
        srt = '1\n00:00:00,000 --> 00:00:02,000\nKnowledge becomes a system.\n'
        ass = p.srt_to_active_word_ass(srt)
        self.assertIn('Outline, Shadow', ass)
        self.assertIn(',2,0,2,', ass)
        self.assertIn(r'\c&H0000C8FF&', ass)
        self.assertIn(r'\alpha&HFF&', ass)
        self.assertGreaterEqual(ass.count('Dialogue:'), 5)
        cues = p.srt_to_cues(srt)
        self.assertEqual(cues, [{'start': 0.0, 'end': 2.0, 'text': 'Knowledge becomes a system.'}])

    def test_source_timestamps_are_rebased_to_excerpt_time(self):
        source = ('1\n00:01:55,020 --> 00:01:56,540\nFirst phrase\n\n'
                  '2\n00:02:00,000 --> 00:02:01,000\nSecond phrase\n')
        normalized = p.normalize_srt(source, 113)
        self.assertIn('00:00:02,020 --> 00:00:03,540', normalized)
        self.assertIn('00:00:07,000 --> 00:00:08,000', normalized)
        already_relative = p.normalize_srt('1\n00:00:02,000 --> 00:00:03,000\nText\n', 113)
        self.assertIn('00:00:02,000 --> 00:00:03,000', already_relative)

    def test_caption_replacements_are_exact_and_cues_are_clamped(self):
        source = ('1\n00:00:00,000 --> 00:00:02,000\nnotebook LM and sub stack\n\n'
                  '2\n00:00:04,000 --> 00:00:06,000\nEnding phrase\n')
        revised = p.revise_srt(source, {'notebook LM': 'NotebookLM', 'sub stack': 'Substack'}, 5.0)
        self.assertIn('NotebookLM and Substack', revised)
        self.assertIn('00:00:04,000 --> 00:00:05,000', revised)

    def test_preview_audio_is_limited_with_fixed_argv(self):
        command = p.audio_ceiling_command('/opt/ffmpeg', 'raw.mp4', 'safe.mp4', -1.0)
        self.assertEqual(command[:6], ['/opt/ffmpeg', '-nostdin', '-y', '-i', 'raw.mp4', '-map'])
        self.assertIn('alimiter=limit=0.891251:level=false', command)
        self.assertEqual(command[-1], 'safe.mp4')

    def test_renderer_uses_fixed_compiled_binary_argv(self):
        command = p.renderer_command('/private/runtime/render_excerpt', 'props.json', 'preview.mp4')
        self.assertEqual(command, ['/private/runtime/render_excerpt', 'props.json', 'preview.mp4'])

    def test_real_stage_artifacts_share_parent_job_directory(self):
        job = p.submit(self.db, self.config_path, self.manifest_path, now=20)
        stage = p._claim(self.db, 'test-worker', now=30)
        probe = {'streams': [{'codec_type': 'video'}, {'codec_type': 'audio'}, {'codec_type': 'subtitle'}],
                 'format': {'duration': '300', 'size': '12'}}
        with patch.object(p, '_probe', return_value=probe):
            artifact = p._execute_stage(self.db, p.load_config(self.config_path), stage, stage)
        self.assertEqual(artifact.parent.name, job['job_id'])
        snapshot = artifact.parent / 'source-original.mp4'
        self.assertTrue(snapshot.is_file())
        self.assertEqual(p.sha256_file(snapshot), json.loads(self.manifest_path.read_text())['source_sha256'])

    def test_transcript_trim_uses_output_seek_and_bounded_duration(self):
        p.submit(self.db, self.config_path, self.manifest_path, now=20)
        intake = p._claim(self.db, 'test-worker', now=30)
        intake_path = self.outputs / 'intake.json'
        intake_path.parent.mkdir(exist_ok=True)
        intake_path.write_text('{}')
        job_folder = p._job_dir(p.load_config(self.config_path), intake['job_id'])
        (job_folder / 'source-original.mp4').write_bytes(self.source.read_bytes())
        p._complete(self.db, intake, intake_path, now=31)
        stage = p._claim(self.db, 'test-worker', now=32)
        captured = []

        def command(argv, *_args, **_kwargs):
            captured.extend(str(item) for item in argv)
            Path(argv[-1]).write_text('1\n00:00:00,000 --> 00:00:01,000\nCaption\n')
            return b''

        with patch.object(p, '_run', side_effect=command):
            p._execute_stage(self.db, p.load_config(self.config_path), stage, stage)
        self.assertLess(captured.index('-i'), captured.index('-ss'))
        self.assertEqual(captured[captured.index('-t') + 1], '98.0')

    def test_stage_progress_is_persistent_and_final_status_waits_for_review(self):
        job = p.submit(self.db, self.config_path, self.manifest_path, now=20)

        def artifact(_db, config, _job, stage):
            name = 'expertise-clip-01.mp4' if stage['name'] == 'preview_render' else (stage['name'] + '.json')
            path = p._job_dir(config, stage['job_id']) / name
            path.write_text('{}')
            return path

        with patch.object(p, '_execute_stage', side_effect=artifact):
            for index in range(len(p.STAGES) - 1):
                self.assertTrue(p.run_once(self.db, self.config_path, now=30 + index))
        result = p.report(self.db, job['job_id'])['jobs'][0]
        self.assertEqual(result['status'], 'awaiting_review')
        self.assertTrue(all(stage['status'] == 'completed' for stage in result['stages']))
        self.assertEqual(len(result['attempts']), len(p.STAGES) - 1)

    def test_administrative_interrupt_requeues_without_consuming_attempt(self):
        class ServiceStop(Exception):
            pass

        job = p.submit(self.db, self.config_path, self.manifest_path, now=20)
        with patch.object(p, '_execute_stage', side_effect=ServiceStop()):
            with self.assertRaises(ServiceStop):
                p.run_once(self.db, self.config_path, now=30)
        stage = self.db.execute("select status,attempts,error_class from production_stages where job_id=? and name='intake'",
                                (job['job_id'],)).fetchone()
        self.assertEqual(tuple(stage), ('queued', 0, 'administrative_interrupt'))
        attempt = self.db.execute('select status from production_attempts').fetchone()[0]
        self.assertEqual(attempt, 'administrative_interrupt')

    def test_success_clears_stage_error_but_preserves_failed_attempt(self):
        p.submit(self.db, self.config_path, self.manifest_path, now=20)
        stage = p._claim(self.db, 'test-worker', now=30)
        p._fail(self.db, stage, RuntimeError('temporary'), now=31)
        stage = p._claim(self.db, 'test-worker', now=100)
        artifact = self.root / 'artifact.json'
        artifact.write_text('{}')
        self.assertTrue(p._complete(self.db, stage, artifact, now=101))
        current = self.db.execute('select status,error_class from production_stages where id=?',
                                  (stage['id'],)).fetchone()
        failed = self.db.execute("select count(*) from production_attempts where status='queued' "
                                 "and error_class='RuntimeError'").fetchone()[0]
        self.assertEqual(tuple(current), ('completed', None))
        self.assertEqual(failed, 1)

    def test_expired_lease_recovers_and_records_attempt(self):
        job = p.submit(self.db, self.config_path, self.manifest_path, now=20)
        old = p._claim(self.db, 'worker-a', now=30)
        self.assertIsNotNone(old)
        path = self.outputs / 'recovered.json'
        path.parent.mkdir(exist_ok=True)
        path.write_text('{}')
        with patch.object(p, '_execute_stage', return_value=path):
            self.assertTrue(p.run_once(self.db, self.config_path, now=30 + p.LEASE_SECONDS + 1))
        attempts = self.db.execute('select status from production_attempts order by started_at').fetchall()
        self.assertEqual([row[0] for row in attempts], ['lease_expired', 'completed'])
        self.assertEqual(self.db.execute("select status from production_stages where job_id=? and name='intake'",
                                         (job['job_id'],)).fetchone()[0], 'completed')


if __name__ == '__main__':
    unittest.main()
