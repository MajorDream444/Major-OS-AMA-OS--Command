import importlib.util
import json
import tempfile
import unittest
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
            w.generate('text','model','https://cloud.example')

    def test_daily_tick_deduplicates_and_does_not_recycle_source(self):
        inbox = self.root / 'inbox'
        inbox.mkdir()
        (inbox / 'thought.md').write_text('original thought')
        for day in (15,15,16):
            w.tick(self.db, self.root, inbox, datetime(2026,10,day,20))
        self.assertEqual(self.db.execute('select count(*) from jobs').fetchone()[0], 1)
        self.assertEqual(len(list((self.root / 'briefs').glob('*.json'))), 4)

    def test_no_source_is_not_fake_completed_content(self):
        w.tick(self.db, self.root, self.root / 'absent', datetime(2026,10,15,20))
        self.assertEqual(self.db.execute('select count(*) from jobs').fetchone()[0], 0)
        self.assertEqual(w.report(self.db)['published'], 0)


if __name__ == '__main__':
    unittest.main()
