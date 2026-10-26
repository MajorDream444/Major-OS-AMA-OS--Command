import importlib.util
import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

MODULE = Path(__file__).parents[1] / 'worker.py'
spec = importlib.util.spec_from_file_location('worker', MODULE)
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)


class WorkerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.db = w.connect(self.root / 'state.sqlite')

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def enqueue(self):
        return w.enqueue(self.db, 'maim', 'original thought', 'test-source', '2026-10-15')

    def test_source_and_dedup_survive_reopen(self):
        a = self.enqueue()
        self.assertEqual(a, self.enqueue())
        self.db.close()
        self.db = w.connect(self.root / 'state.sqlite')
        self.assertEqual(self.db.execute('select count(*) from jobs').fetchone()[0], 1)
        self.assertEqual(self.db.execute('select body from sources').fetchone()[0], 'original thought')

    def test_changed_content_and_explicit_rerun_create_new_jobs(self):
        first = self.enqueue()
        changed = w.enqueue(self.db, 'maim', 'changed thought', 'test-source', '2026-10-15')
        rerun = w.enqueue(self.db, 'maim', 'original thought', 'test-source', '2026-10-15', rerun=True)
        self.assertEqual(len({first, changed, rerun}), 3)

    def test_watcher_and_manual_overlap_share_atomic_identity(self):
        inbox = self.root / 'inbox'
        inbox.mkdir()
        source = inbox / 'brief.md'
        body = 'Yawdie-Actionable: true\noperating priorities'
        source.write_text(body)
        source.chmod(0o600)
        w.tick(self.db, self.root, inbox, datetime(2026,10,15,20))
        watcher_id = self.db.execute('select id from jobs').fetchone()[0]
        manual_id = w.enqueue(self.db, 'maim', body, 'founder-reference', '2026-10-15')
        self.assertEqual(watcher_id, manual_id)
        self.assertEqual(self.db.execute('select count(*) from jobs').fetchone()[0], 1)

    def test_concurrent_intake_creates_one_job(self):
        db_path = self.root / 'concurrent.sqlite'
        self.db.close()
        self.db = w.connect(db_path)

        def submit(reference):
            db = w.connect(db_path)
            try:
                return w.enqueue(db, 'maim', 'same body', reference, '2026-10-15', task='operating-brief')
            finally:
                db.close()

        with ThreadPoolExecutor(max_workers=8) as pool:
            ids = list(pool.map(submit, [f'ref-{i}' for i in range(16)]))
        self.assertEqual(len(set(ids)), 1)
        self.assertEqual(self.db.execute('select count(*) from jobs').fetchone()[0], 1)

    def test_claim_is_exclusive_across_connections(self):
        self.enqueue()
        a = w.claim(self.db, now=100)
        other = w.connect(self.root / 'state.sqlite')
        self.assertIsNone(w.claim(other, now=101))
        other.close()
        self.assertIsNotNone(a)

    def test_expired_claim_recovers_and_old_owner_cannot_finish(self):
        self.enqueue()
        old = w.claim(self.db, now=100)
        new = w.claim(self.db, now=100 + w.LEASE_SECONDS + 1)
        self.assertNotEqual(old['lease_token'], new['lease_token'])
        self.assertFalse(w.finish(self.db, old, 'draft_ready', 'old-output'))
        self.assertTrue(w.finish(self.db, new, 'draft_ready', 'new-output'))

    def test_invalid_workspace_rejected(self):
        with self.assertRaises(ValueError):
            w.enqueue(self.db, '../client', 'body', 'ref', '2026-10-15')

    def test_model_error_is_retry_then_blocked(self):
        self.enqueue()
        with patch.object(w, 'generate', side_effect=RuntimeError('unreachable')):
            for i in range(w.MAX_ATTEMPTS):
                w.run_once(self.db, self.root, 'local-model', now=10000*i)
        row = self.db.execute('select * from jobs').fetchone()
        self.assertEqual(row['status'], 'blocked')
        self.assertEqual(row['attempts'], w.MAX_ATTEMPTS)
        self.assertEqual(w.report(self.db)['published'], 0)

    def test_completed_draft_has_source_and_twelve_placements(self):
        self.enqueue()
        with patch.object(w, 'generate', return_value={'article':'Real draft','short_script':'Video script','thumbnail_prompt':'Visual prompt','note':'Short note','youtube_post':'Community post'}):
            self.assertTrue(w.run_once(self.db, self.root, 'local-model', now=100))
        row = self.db.execute('select * from jobs').fetchone()
        packet = json.loads(Path(row['artifact']).read_text())
        self.assertEqual(len(packet['placements']), 12)
        self.assertEqual(packet['source']['body'], 'original thought')
        self.assertTrue(all(p['status']=='planned' for p in packet['placements']))
        self.assertEqual(w.report(self.db)['published'], 0)

    def test_empty_or_wrong_model_output_rejected(self):
        with self.assertRaises(ValueError):
            w.validate_draft({'article':''})

    def test_cloud_model_endpoint_rejected(self):
        with self.assertRaises(ValueError):
            w.generate('text','model', endpoint='https://cloud.example')

    def test_local_ollama_opener_explicitly_disables_proxies(self):
        class Response:
            def __init__(self, value):
                self.value = json.dumps(value).encode()
            def __enter__(self):
                return self
            def __exit__(self, *_):
                return False
            def read(self, _limit):
                return self.value
        draft = {k: 'Grounded Major Artificial Intelligence Mindset draft.' for k in w.CONTENT_FIELDS}
        opener = unittest.mock.Mock()
        opener.open.side_effect = [Response({}), Response({'response': json.dumps(draft)})]
        with patch.object(w, 'build_opener', return_value=opener) as build:
            w.generate('source without URLs', 'local-model')
        self.assertEqual(type(build.call_args.args[0]).__name__, 'ProxyHandler')
        self.assertEqual(build.call_args.args[0].proxies, {})

    def test_daily_tick_deduplicates_and_does_not_recycle_source(self):
        inbox = self.root / 'inbox'
        inbox.mkdir()
        source = inbox / 'thought.md'
        source.write_text('Yawdie-Actionable: true\noriginal thought')
        source.chmod(0o600)
        for day in (15,15,16):
            w.tick(self.db, self.root, inbox, datetime(2026,10,day,20))
        self.assertEqual(self.db.execute('select count(*) from jobs').fetchone()[0], 1)
        self.assertEqual(len(list((self.root / 'briefs').glob('*.json'))), 4)

    def test_templates_and_unmarked_files_are_not_watched(self):
        inbox = self.root / 'inbox'
        inbox.mkdir()
        (inbox / 'DAILY_BRIEF_TEMPLATE.md').write_text('Yawdie-Actionable: true\ntemplate')
        (inbox / 'notes.md').write_text('ordinary notes')
        (inbox / 'DAILY_BRIEF_TEMPLATE.md').chmod(0o600)
        (inbox / 'notes.md').chmod(0o600)
        w.tick(self.db, self.root, inbox, datetime(2026,10,15,20))
        self.assertEqual(self.db.execute('select count(*) from jobs').fetchone()[0], 0)

    def test_no_source_is_not_fake_completed_content(self):
        w.tick(self.db, self.root, self.root / 'absent', datetime(2026,10,15,20))
        self.assertEqual(self.db.execute('select count(*) from jobs').fetchone()[0], 0)
        self.assertEqual(w.report(self.db)['published'], 0)

    def test_operator_status_maps_draft_ready_to_completed(self):
        self.enqueue()
        self.assertEqual(w.status(self.db)['queued'], 1)
        with patch.object(w, 'generate', return_value={'article':'Real draft','short_script':'Video script','thumbnail_prompt':'Visual prompt','note':'Short note','youtube_post':'Community post'}):
            w.run_once(self.db, self.root, 'local-model', now=100)
        self.assertEqual(w.status(self.db)['completed'], 1)
        self.assertEqual(w.status(self.db)['publication_adapter'], 'blocked: adapter unavailable')

    def test_canonical_founder_context_is_exact(self):
        self.assertIn("Yawdie is Major Dream Williams's chief of staff", w.FOUNDER_CONTEXT)
        self.assertIn('MAIM means Major Artificial Intelligence Mindset', w.FOUNDER_CONTEXT)
        self.assertNotIn('MAIM is Major AI Mindset', w.FOUNDER_CONTEXT)

    def test_grounding_rejects_invented_url_and_acronym(self):
        base = {k: 'A factual draft about Major Artificial Intelligence Mindset.' for k in w.CONTENT_FIELDS}
        self.assertEqual(w.validate_grounding(base, 'source without a URL'), base)
        bad_url = dict(base, article='Read https://invented.example/path today.')
        with self.assertRaises(ValueError):
            w.validate_grounding(bad_url, 'source without a URL')
        bad_name = dict(base, note='MAIM is Major AI Mindset for everyone.')
        with self.assertRaises(ValueError):
            w.validate_grounding(bad_name, 'source without a URL')
        legitimate = dict(base, note='A major AI shift requires careful review.')
        self.assertEqual(w.validate_grounding(legitimate, 'source without a URL'), legitimate)
        punctuated = dict(base, note='Review https://example.com/path.')
        self.assertEqual(w.validate_grounding(punctuated, 'Source: https://example.com/path.'), punctuated)
        with self.assertRaises(ValueError):
            w.validate_grounding(dict(base, note='Visit invented.example/offer'), 'source without a URL')

    def test_operating_brief_has_only_operating_fields_and_no_placements(self):
        w.enqueue(self.db, 'maim', 'priorities and blockers', 'founder', '2026-10-15', task='operating-brief')
        result = {k: 'Founder supplied operating evidence and next action.' for k in w.OPERATING_FIELDS}
        result['blockers'] = 'Publishing is blocked: adapter unavailable.'
        with patch.object(w, 'generate', return_value=result):
            w.run_once(self.db, self.root, 'local-model', now=100)
        row = self.db.execute('select * from jobs').fetchone()
        packet = json.loads(Path(row['artifact']).read_text())
        self.assertEqual(set(packet['draft']), set(w.OPERATING_FIELDS))
        self.assertEqual(packet['placements'], [])
        self.assertEqual(packet['unsupported_actions']['publishing'], 'blocked: adapter unavailable')

    def test_operating_coverage_requires_all_priorities_and_adapter_blocker(self):
        source = '## Priorities\n1. First\n2. Second\n\n## Blockers\nblocked: adapter unavailable'
        good = {
            'priorities': '1. First priority. 2. Second priority.',
            'next_actions': 'Review the smallest next actions.',
            'blockers': 'Publishing is blocked: adapter unavailable.',
            'evidence_needed': 'Review the job receipt and artifact.',
        }
        self.assertEqual(w.validate_operating_coverage(good, source), good)
        with self.assertRaises(ValueError):
            w.validate_operating_coverage(dict(good, priorities='1. First only.'), source)
        with self.assertRaises(ValueError):
            w.validate_operating_coverage(dict(good, blockers='No blockers.'), source)

    def test_operating_sections_preserve_founder_supplied_items(self):
        source = ('## Priorities\n1. First\n2. Second\n\n'
                  '## Requested next actions\n- Act\n\n'
                  '## Known blockers and boundaries\n- Publishing is blocked: adapter unavailable.\n\n'
                  '## Evidence needed\n- Job receipt\n')
        draft = {k: 'Model summary that may omit source items.' for k in w.OPERATING_FIELDS}
        grounded = w.ground_operating_sections(draft, source)
        self.assertEqual(grounded['priorities'], '1. First 2. Second')
        self.assertIn('blocked: adapter unavailable', grounded['blockers'])
        self.assertEqual(grounded['evidence_needed'], '- Job receipt')

    def test_operating_sections_support_founder_activation_headings(self):
        source = (
            '## Founder-approved priorities\n1. First.\n2. Second.\n3. Third.\n\n'
            '## Requested output\n- Identify next actions.\n\n'
            '## Completion criteria\n- Unsupported actions are marked blocked: adapter unavailable.\n'
        )
        draft = {name: 'Model draft value.' for name in w.OPERATING_FIELDS}
        grounded = w.ground_operating_sections(draft, source)
        self.assertIn('3. Third.', grounded['priorities'])
        self.assertIn('Identify next actions', grounded['next_actions'])
        self.assertIn('blocked: adapter unavailable', grounded['blockers'])
        self.assertIn('Unsupported actions', grounded['evidence_needed'])
        w.validate_operating_coverage(grounded, source)

    def test_graceful_service_stop_does_not_consume_attempt(self):
        self.enqueue()
        job = w.claim(self.db, now=100)
        self.assertEqual(job['attempts'], 1)
        self.assertTrue(w.release_for_service_stop(self.db, job, now=101))
        row = self.db.execute('select status,attempts from jobs').fetchone()
        self.assertEqual((row['status'], row['attempts']), ('queued', 0))
        attempt = self.db.execute('select status from execution_attempts').fetchone()[0]
        self.assertEqual(attempt, 'administrative_interrupt')

    def test_execution_lock_blocks_second_executor(self):
        with w.execution_lock(self.root):
            with self.assertRaises(BlockingIOError):
                with w.execution_lock(self.root):
                    pass

    def test_unchanged_inbox_file_is_not_read_repeatedly(self):
        inbox = self.root / 'inbox'
        inbox.mkdir()
        source = inbox / 'brief.md'
        source.write_text('Yawdie-Actionable: true\ncontent')
        source.chmod(0o600)
        self.assertEqual(len(list(w.changed_inbox_files(self.db, inbox))), 1)
        self.assertEqual(len(list(w.changed_inbox_files(self.db, inbox))), 0)

    def test_inbox_file_becomes_eligible_after_permissions_are_fixed(self):
        inbox = self.root / 'inbox'
        inbox.mkdir()
        source = inbox / 'brief.md'
        source.write_text('Yawdie-Actionable: true\ncontent')
        source.chmod(0o644)
        self.assertEqual(len(list(w.changed_inbox_files(self.db, inbox))), 0)
        source.chmod(0o600)
        self.assertEqual(len(list(w.changed_inbox_files(self.db, inbox))), 1)


if __name__ == '__main__':
    unittest.main()
