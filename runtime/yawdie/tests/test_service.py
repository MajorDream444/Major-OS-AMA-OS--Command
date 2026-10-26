import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

MODULE = Path(__file__).parents[1] / 'service.py'
spec = importlib.util.spec_from_file_location('service', MODULE)
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.paths = patch.multiple(s, STATE=root/'state', INBOX=root/'inbox', LOGS=root/'logs', RUNTIME=root/'runtime')
        self.paths.start()

    def tearDown(self):
        self.paths.stop()
        self.tmp.cleanup()

    def test_start_is_noop_when_already_running(self):
        with patch.object(s, 'loaded_state', return_value='running'), \
             patch.object(s, 'model_is_installed') as model, patch.object(s, 'run') as run:
            s.start()
        model.assert_not_called()
        run.assert_not_called()

    def test_loaded_service_is_kicked_without_kill(self):
        with patch.object(s, 'loaded_state', return_value='loaded'), \
             patch.object(s, 'model_is_installed', return_value=True), patch.object(s, 'run') as run:
            s.start()
        args = run.call_args.args
        self.assertEqual(args[:2], ('launchctl', 'kickstart'))
        self.assertNotIn('-k', args)

    def test_missing_model_blocks_start(self):
        with patch.object(s, 'loaded_state', return_value=None), \
             patch.object(s, 'model_is_installed', return_value=False):
            with self.assertRaises(SystemExit):
                s.start()


if __name__ == '__main__':
    unittest.main()
