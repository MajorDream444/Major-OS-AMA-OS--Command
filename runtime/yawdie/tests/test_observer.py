import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

RUNTIME = Path(__file__).parents[1]
sys.path.insert(0, str(RUNTIME))

import observer
import observer_service
import worker


class ObserverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.database = self.root / 'state.sqlite'
        self.logs = self.root / 'logs'
        self.logs.mkdir()
        (self.logs / 'stdout.log').write_text('healthy\n')
        (self.logs / 'stderr.log').write_text('')
        self.db = worker.connect(self.database)

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_snapshot_is_read_only_and_records_attempts(self):
        job_id = worker.enqueue(self.db, 'maim', 'body', 'ref', '2026-10-26')
        job = worker.claim(self.db, now=100)
        worker.finish(self.db, job, 'draft_ready', 'artifact', now=101)
        before = self.database.stat().st_mtime_ns
        now = datetime(2026, 10, 26, 15, 0, tzinfo=ZoneInfo('Asia/Makassar'))
        with patch.object(observer, 'launchd_snapshot', return_value={
                'loaded': True, 'state': 'running', 'pid': '123', 'runs': '1', 'last_exit': None}), \
             patch.object(observer, 'ollama_reachable', return_value=True):
            result = observer.snapshot(self.database, self.logs, now)
        self.assertEqual(result['queue']['counts'], {'draft_ready': 1})
        self.assertEqual(result['queue']['jobs'][0]['id'], job_id)
        self.assertEqual(result['queue']['jobs'][0]['attempt_history'][0]['status'], 'draft_ready')
        self.assertEqual(self.database.stat().st_mtime_ns, before)

    def test_append_is_valid_jsonl_and_private(self):
        target = self.root / 'operations/evidence.jsonl'
        observer.append_record(target, {'observed_at': '2026-10-26T15:00:00+08:00'})
        observer.append_record(target, {'observed_at': '2026-10-26T15:15:00+08:00'})
        self.assertEqual(len(observer.read_records(target)), 2)
        self.assertEqual(target.stat().st_mode & 0o777, 0o600)

    def test_summary_marks_gaps_and_does_not_claim_sleep(self):
        zone = ZoneInfo('Asia/Makassar')
        start = datetime(2026, 10, 26, 14, 0, tzinfo=zone)
        end = start + timedelta(hours=2)
        records = [{
            'observed_at': (start + timedelta(hours=1)).isoformat(),
            'yawdie': {'state': 'running'},
            'ollama_loopback_reachable': True,
            'queue': {'available': True, 'counts': {'draft_ready': 1}, 'jobs': []},
        }]
        target = self.root / 'summary.md'
        with patch.object(observer, 'sleep_events', return_value=[]):
            self.assertTrue(observer.write_summary(target, records, start, end, 900))
        text = target.read_text()
        self.assertIn('Status: COMPLETE_WITH_GAPS_OR_FAILURES', text)
        self.assertIn('Sleep/wake recovery remains untested', text)
        self.assertIn('Review each gap or failure', text)
        self.assertFalse(observer.write_summary(target, records, start, end, 900))

    def test_observer_service_uses_separate_label_and_evidence_names(self):
        self.assertNotEqual(observer_service.LABEL, 'com.major.hamal.yawdie')
        evidence, summary = observer_service.evidence_paths('2026-10-26')
        self.assertEqual(evidence.name, 'OVERNIGHT_OBSERVATION_2026-10-26.jsonl')
        self.assertEqual(summary.name, 'OVERNIGHT_OBSERVATION_2026-10-26_FINAL.md')


if __name__ == '__main__':
    unittest.main()
