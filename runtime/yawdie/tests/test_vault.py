import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

RUNTIME = Path(__file__).parents[1]
sys.path.insert(0, str(RUNTIME))

import path_policy
import vault
import worker


class PathPolicyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / 'Approved').mkdir()
        self.policy = path_policy.PathPolicy(self.root, ('Approved',), max_file_bytes=32)

    def tearDown(self):
        self.tmp.cleanup()

    def test_rejects_traversal_hidden_binary_and_oversized_files(self):
        (self.root / 'Approved/ok.md').write_text('ok')
        (self.root / 'Approved/.hidden.md').write_text('hidden')
        (self.root / 'Approved/binary.md').write_bytes(b'a\x00b')
        (self.root / 'Approved/large.md').write_text('x' * 33)
        self.assertEqual(self.policy.read_text('Approved/ok.md')['text'], 'ok')
        for value in ('../outside.md', '/tmp/outside.md', 'Approved/.hidden.md'):
            with self.assertRaises(path_policy.PathPolicyError):
                self.policy.read_text(value)
        with self.assertRaises(path_policy.PathPolicyError):
            self.policy.read_text('Approved/binary.md')
        with self.assertRaises(path_policy.PathPolicyError):
            self.policy.read_text('Approved/large.md')

    def test_rejects_symlink_escape(self):
        outside = self.root / 'outside.md'
        outside.write_text('private')
        os.symlink(outside, self.root / 'Approved/link.md')
        with self.assertRaises(path_policy.PathPolicyError):
            self.policy.read_text('Approved/link.md')

    def test_unavailable_file_is_non_destructive(self):
        target = self.root / 'Approved/icloud.md'
        target.write_text('available later')
        with patch.object(Path, 'read_bytes', side_effect=OSError('not downloaded')):
            with self.assertRaises(path_policy.TemporarilyUnavailable):
                self.policy.read_text('Approved/icloud.md')
        self.assertTrue(target.exists())


class VaultTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.vault = self.root / 'Major OS'
        self.vault.mkdir()
        vault.initialize_layout(self.vault)
        self.state = self.root / 'state'
        self.db = worker.connect(self.state / 'state.sqlite')

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def brief(self, name='brief.md', body=None):
        body = body or (
            'Yawdie-Actionable: true\nYawdie-Task: operating-brief\n\n'
            '## Priorities\n1. Verify the local bridge.\n\n'
            '## Requested next actions\n- Draft a bounded report.\n\n'
            '## Known blockers and boundaries\n- Publishing is blocked: adapter unavailable.\n\n'
            '## Evidence needed\n- Job ID and hashes.\n'
        )
        target = self.vault / 'Yawdie/Briefs/Inbox' / name
        target.write_text(body)
        return target

    def test_layout_is_only_four_approved_folders(self):
        found = sorted(str(path.relative_to(self.vault)) for path in self.vault.rglob('*') if path.is_dir())
        self.assertEqual(found, ['Yawdie', 'Yawdie/Briefs', 'Yawdie/Briefs/Inbox',
                                 'Yawdie/Context', 'Yawdie/Reports', 'Yawdie/Templates'])

    def test_submit_context_dedupe_rerun_and_template_exclusion(self):
        (self.vault / 'Yawdie/Context/founder.md').write_text('MAIM means Major Artificial Intelligence Mindset.')
        self.brief()
        first = vault.submit(self.db, self.vault, 'Yawdie/Briefs/Inbox/brief.md', day='2026-10-26')
        duplicate = vault.submit(self.db, self.vault, 'Yawdie/Briefs/Inbox/brief.md', day='2026-10-26')
        rerun = vault.submit(self.db, self.vault, 'Yawdie/Briefs/Inbox/brief.md', day='2026-10-26', rerun=True)
        self.assertEqual(first['job_id'], duplicate['job_id'])
        self.assertNotEqual(first['job_id'], rerun['job_id'])
        self.assertEqual(first['context']['files'][0]['relative_path'], 'Yawdie/Context/founder.md')
        context = self.db.execute('SELECT * FROM job_contexts WHERE job_id=?', (first['job_id'],)).fetchone()
        self.assertEqual(context['context_sha256'], first['context']['sha256'])
        self.brief('DAILY_BRIEF_TEMPLATE.md')
        with self.assertRaises(ValueError):
            vault.submit(self.db, self.vault, 'Yawdie/Briefs/Inbox/DAILY_BRIEF_TEMPLATE.md')

    def test_context_is_bounded_and_does_not_crawl_other_vault_folders(self):
        (self.vault / 'Private').mkdir()
        (self.vault / 'Private/client.md').write_text('must not load')
        for index in range(5):
            (self.vault / f'Yawdie/Context/{index}.md').write_text('x' * 3500)
        result = vault.load_context(self.vault)
        self.assertLessEqual(result['bytes'], vault.MAX_CONTEXT_BYTES)
        self.assertTrue(result['truncated'])
        self.assertNotIn('client.md', result['text'])

    def test_bad_context_is_rejected_without_blocking_good_context(self):
        (self.vault / 'Yawdie/Context/good.md').write_text('approved')
        (self.vault / 'Yawdie/Context/too-large.md').write_text('x' * (vault.MAX_CONTEXT_FILE_BYTES + 1))
        result = vault.load_context(self.vault)
        self.assertIn('approved', result['text'])
        self.assertEqual(result['rejected'], ['Yawdie/Context/too-large.md'])

    def test_scan_is_idempotent_and_reports_unavailable_without_deleting(self):
        source = self.brief()
        first = vault.scan(self.db, self.vault, day='2026-10-26')
        second = vault.scan(self.db, self.vault, day='2026-10-26')
        self.assertEqual(first['submitted'][0]['job_id'], self.db.execute('SELECT id FROM jobs').fetchone()[0])
        self.assertEqual(second['submitted'], [])
        self.assertEqual(self.db.execute('SELECT count(*) FROM jobs').fetchone()[0], 1)
        self.assertTrue(source.exists())

    def test_context_reaches_generation_and_report_export_is_atomic_idempotent(self):
        context_note = self.vault / 'Yawdie/Context/founder.md'
        context_note.write_text('Approved operating context.')
        self.brief()
        receipt = vault.submit(self.db, self.vault, 'Yawdie/Briefs/Inbox/brief.md', day='2026-10-26')
        generated = {
            'priorities': '1. Verify the local bridge.',
            'next_actions': '- Draft a bounded report.',
            'blockers': '- Publishing is blocked: adapter unavailable.',
            'evidence_needed': '- Job ID and hashes.',
        }
        with patch.object(worker, 'generate', return_value=generated) as call:
            worker.run_once(self.db, self.state, 'local-model', now=100)
        self.assertIn('Approved operating context.', call.call_args.kwargs['context'])
        exported = vault.export_report(self.db, self.vault, receipt['job_id'])
        repeated = vault.export_report(self.db, self.vault, receipt['job_id'])
        report = self.vault / exported['report']
        self.assertTrue(report.exists())
        self.assertFalse(exported['unchanged'])
        self.assertTrue(repeated['unchanged'])
        self.assertIn(receipt['source']['sha256'], report.read_text())
        self.assertIn('Inference duration:', report.read_text())
        self.assertTrue(self.brief().exists())

    def test_cycle_exports_ready_jobs_without_reingesting_reports(self):
        self.brief()
        receipt = vault.submit(self.db, self.vault, 'Yawdie/Briefs/Inbox/brief.md', day='2026-10-26')
        generated = {
            'priorities': '1. Verify the local bridge.',
            'next_actions': '- Draft a bounded report.',
            'blockers': '- Publishing is blocked: adapter unavailable.',
            'evidence_needed': '- Job ID and hashes.',
        }
        with patch.object(worker, 'generate', return_value=generated):
            worker.run_once(self.db, self.state, 'local-model', now=100)
        result = vault.cycle(self.db, self.vault, day='2026-10-26')
        self.assertEqual(result['reports']['exported'][0]['job_id'], receipt['job_id'])
        self.assertEqual(self.db.execute('SELECT count(*) FROM jobs').fetchone()[0], 1)
        self.assertEqual(vault.export_ready(self.db, self.vault)['exported'], [])

    def test_unsupported_task_is_blocked_without_crashing_scan(self):
        self.brief(body='Yawdie-Actionable: true\nYawdie-Task: publish\n')
        result = vault.scan(self.db, self.vault, day='2026-10-26')
        self.assertEqual(result['submitted'], [])
        self.assertEqual(result['blocked'][0]['reason'], 'adapter unavailable')
        self.assertEqual(self.db.execute('SELECT count(*) FROM jobs').fetchone()[0], 0)

    def test_report_export_rejects_symlink_destination(self):
        self.brief()
        receipt = vault.submit(self.db, self.vault, 'Yawdie/Briefs/Inbox/brief.md', day='2026-10-26')
        generated = {
            'priorities': '1. Verify the local bridge.',
            'next_actions': '- Draft a bounded report.',
            'blockers': '- Publishing is blocked: adapter unavailable.',
            'evidence_needed': '- Job ID and hashes.',
        }
        with patch.object(worker, 'generate', return_value=generated):
            worker.run_once(self.db, self.state, 'local-model', now=100)
        outside = self.root / 'outside.md'
        outside.write_text('must remain untouched')
        os.symlink(outside, self.vault / 'Yawdie/Reports' / (receipt['job_id'] + '.md'))
        with self.assertRaises(path_policy.PathPolicyError):
            vault.export_report(self.db, self.vault, receipt['job_id'])
        self.assertEqual(outside.read_text(), 'must remain untouched')


if __name__ == '__main__':
    unittest.main()
