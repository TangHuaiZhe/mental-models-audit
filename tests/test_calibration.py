import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from publish_notion import MARKER, PublishError, desired, publish, request
from validate_calibration import validate

class CalibrationTests(unittest.TestCase):
    def test_frozen_model_set_and_hashes(self):
        validate()

    def test_dry_run_never_calls_notion(self):
        manifest = {'models': [self.entry('unverified')]}
        def fail(*args, **kwargs):
            raise AssertionError('network call in dry run')
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(publish(manifest, False, state_path=Path(tmp) / 'status.json', client=fail), 0)

    def test_unverified_mapping_blocks_apply(self):
        manifest = {'models': [self.entry('unverified')]}
        self.assertEqual(publish(manifest, True, token='fake', client=lambda *a, **k: None), 1)

    def test_publish_then_remote_marker_skips_retry(self):
        entry = self.entry('verified')
        page_id = entry['notion_page_id']
        remote = {'markdown': 'Old content'}
        calls = []
        def client(method, page_id_arg, token, body=None):
            calls.append(method)
            self.assertEqual(page_id_arg, page_id)
            if method == 'PATCH':
                remote['markdown'] = body['replace_content']['new_str']
            return {'object': 'page_markdown', 'id': page_id, 'truncated': False, 'unknown_block_ids': [], 'markdown': remote['markdown']}
        manifest = {'models': [entry]}
        self.assertEqual(publish(manifest, True, token='fake', client=client), 0)
        self.assertIn(MARKER, remote['markdown'])
        self.assertEqual(publish(manifest, True, token='fake', client=client), 0)
        self.assertEqual(calls, ['GET', 'PATCH', 'GET', 'GET'])

    def test_incomplete_remote_page_fails_closed(self):
        entry = self.entry('verified')
        def client(*args, **kwargs):
            return {'object': 'page_markdown', 'id': entry['notion_page_id'], 'truncated': True, 'markdown': ''}
        self.assertEqual(publish({'models': [entry]}, True, token='fake', client=client), 1)

    def test_rate_limit_is_retried(self):
        attempts = []
        class Response(io.BytesIO):
            status = 200
            def __enter__(self): return self
            def __exit__(self, *args): self.close()
        def opener(req, timeout):
            attempts.append(req)
            if len(attempts) == 1:
                raise HTTPError(req.full_url, 429, 'rate limited', {'Retry-After': '0'}, None)
            return Response(b'{"object":"page_markdown"}')
        self.assertEqual(request('GET', 'a' * 32, 'fake', opener=opener, sleeper=lambda seconds: None)['object'], 'page_markdown')
        self.assertEqual(len(attempts), 2)

    def test_published_course_links_are_absolute(self):
        import yaml
        entries = yaml.safe_load((Path(__file__).resolve().parents[1] / 'content-manifest.yaml').read_text())['models']
        rendered = desired(entries[14])
        self.assertIn('https://tanghuaizhe.github.io/mental-models-audit/', rendered)
        self.assertIn(MARKER, rendered)

    @staticmethod
    def entry(status):
        import yaml
        data = yaml.safe_load((Path(__file__).resolve().parents[1] / 'content-manifest.yaml').read_text())
        entry = dict(data['models'][0])
        entry['mapping_status'] = status
        return entry

if __name__ == '__main__':
    unittest.main()
