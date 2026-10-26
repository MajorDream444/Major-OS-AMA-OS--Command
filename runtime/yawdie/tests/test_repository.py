import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RUNTIME = Path(__file__).parents[1]
sys.path.insert(0, str(RUNTIME))

import path_policy
import repository


class RepositoryAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'repo'
        self.root.mkdir()
        subprocess.run(['/usr/bin/git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['/usr/bin/git', '-C', str(self.root), 'config', 'user.name', 'Fixture'], check=True)
        subprocess.run(['/usr/bin/git', '-C', str(self.root), 'config', 'user.email', 'fixture@example.invalid'], check=True)
        (self.root / 'docs').mkdir()
        (self.root / 'docs/readme.md').write_text('approved evidence')
        (self.root / 'private.md').write_text('excluded')
        subprocess.run(['/usr/bin/git', '-C', str(self.root), 'add', 'docs/readme.md'], check=True)
        subprocess.run(['/usr/bin/git', '-C', str(self.root), 'commit', '-qm', 'fixture'], check=True)
        self.manifest = Path(self.tmp.name) / 'manifest.json'
        self.manifest.write_text(json.dumps({'repositories': {'fixture': {'root': str(self.root), 'include': ['docs']}}}))
        os.chmod(self.manifest, 0o600)

    def tearDown(self):
        self.tmp.cleanup()

    def test_snapshot_is_bounded_grounded_and_records_git_state(self):
        item = repository.snapshot_named(self.manifest, ['fixture'])['fixture']
        self.assertEqual(item['files'][0]['relative_path'], 'docs/readme.md')
        self.assertEqual(item['files'][0]['text'], 'approved evidence')
        self.assertNotIn('excluded', repository.markdown({'fixture': item}))
        self.assertEqual(len(item['commit']), 40)
        self.assertTrue(item['dirty'])
        self.assertEqual(len(item['snapshot_sha256']), 64)

    def test_manifest_permissions_and_unapproved_names_are_rejected(self):
        os.chmod(self.manifest, 0o644)
        with self.assertRaises(path_policy.PathPolicyError):
            repository.load_manifest(self.manifest)
        os.chmod(self.manifest, 0o600)
        with self.assertRaises(path_policy.PathPolicyError):
            repository.snapshot_named(self.manifest, ['missing'])

    def test_hidden_symlink_binary_and_oversize_are_not_read(self):
        (self.root / 'docs/.secret.md').write_text('hidden')
        (self.root / 'docs/binary.md').write_bytes(b'a\x00b')
        (self.root / 'docs/large.md').write_text('x' * (repository.MAX_FILE_BYTES + 1))
        os.symlink(self.root / 'private.md', self.root / 'docs/link.md')
        item = repository.snapshot({'root': str(self.root), 'include': ['docs']})
        paths = [entry['relative_path'] for entry in item['files']]
        self.assertEqual(paths, ['docs/readme.md'])
        self.assertIn('docs/binary.md', item['rejected'])
        self.assertIn('docs/large.md', item['rejected'])

    def test_context_export_is_atomic_and_never_overwrites(self):
        vault = Path(self.tmp.name) / 'vault'
        (vault / 'Yawdie/Context').mkdir(parents=True)
        relative = repository.export_context(vault, 'YAWDIE_REPOSITORY_SNAPSHOT_TEST.md', 'bounded')
        self.assertEqual(relative, 'Yawdie/Context/YAWDIE_REPOSITORY_SNAPSHOT_TEST.md')
        self.assertEqual((vault / relative).read_text(), 'bounded')
        with self.assertRaises(FileExistsError):
            repository.export_context(vault, 'YAWDIE_REPOSITORY_SNAPSHOT_TEST.md', 'other')
        with self.assertRaises(path_policy.PathPolicyError):
            repository.export_context(vault, 'founder-note.md', 'other')

    def test_context_markdown_is_bounded_and_keeps_provenance(self):
        item = repository.snapshot_named(self.manifest, ['fixture'])['fixture']
        content = repository.context_markdown({'fixture': item}, limit=1000)
        self.assertLessEqual(len(content.encode()), 1000)
        self.assertIn(item['commit'], content)
        self.assertIn('docs/readme.md', content)
        self.assertIn(item['files'][0]['sha256'], content)


if __name__ == '__main__':
    unittest.main()
