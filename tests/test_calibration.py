import io
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.error import HTTPError

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from publish_notion import MARKER, desired, publish, request
from validate_calibration import validate


class CalibrationTests(unittest.TestCase):
    def test_frozen_model_set_and_contracts(self):
        validate()

    def test_dry_run_never_calls_notion(self):
        manifest = {'models': [self.entry('unverified')]}

        def fail(*args, **kwargs):
            raise AssertionError('network call in dry run')

        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                publish(
                    manifest,
                    False,
                    state_path=Path(tmp) / 'status.json',
                    client=fail,
                ),
                0,
            )

    def test_unverified_mapping_blocks_apply(self):
        manifest = {'models': [self.entry('unverified')]}
        self.assertEqual(
            publish(
                manifest,
                True,
                token='fake',
                client=lambda *a, **k: None,
            ),
            1,
        )

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
            return {
                'object': 'page_markdown',
                'id': page_id,
                'truncated': False,
                'unknown_block_ids': [],
                'markdown': remote['markdown'],
            }

        manifest = {'models': [entry]}
        self.assertEqual(publish(manifest, True, token='fake', client=client), 0)
        self.assertIn(MARKER, remote['markdown'])
        self.assertEqual(publish(manifest, True, token='fake', client=client), 0)
        self.assertEqual(calls, ['GET', 'PATCH', 'GET', 'GET'])

    def test_incomplete_remote_page_fails_closed(self):
        entry = self.entry('verified')

        def client(*args, **kwargs):
            return {
                'object': 'page_markdown',
                'id': entry['notion_page_id'],
                'truncated': True,
                'markdown': '',
            }

        self.assertEqual(
            publish({'models': [entry]}, True, token='fake', client=client),
            1,
        )

    def test_rate_limit_is_retried(self):
        attempts = []

        class Response(io.BytesIO):
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *args):
                self.close()

        def opener(req, timeout):
            attempts.append(req)
            if len(attempts) == 1:
                raise HTTPError(
                    req.full_url,
                    429,
                    'rate limited',
                    {'Retry-After': '0'},
                    None,
                )
            return Response(b'{"object":"page_markdown"}')

        self.assertEqual(
            request(
                'GET',
                'a' * 32,
                'fake',
                opener=opener,
                sleeper=lambda seconds: None,
            )['object'],
            'page_markdown',
        )
        self.assertEqual(len(attempts), 2)

    def test_published_course_links_are_absolute(self):
        entries = yaml.safe_load(
            (ROOT / 'content-manifest.yaml').read_text()
        )['models']
        rendered = desired(entries[14])
        self.assertIn(
            'https://tanghuaizhe.github.io/mental-models-audit/',
            rendered,
        )
        self.assertIn(MARKER, rendered)
        self.assertFalse(rendered.lstrip().startswith('# '))
        self.assertTrue(rendered.startswith('## '))

    def test_router_has_no_blanket_cluster_penalty(self):
        router = yaml.safe_load(
            (ROOT / 'config/router.yaml').read_text()
        )
        self.assertNotIn('same_cluster_already_selected', router['scoring'])
        self.assertLess(router['scoring']['duplicate_relation_already_selected'], 0)
        self.assertGreater(
            router['scoring']['complementary_with_independent_question_or_evidence'],
            0,
        )

    def test_key_pairs_are_complementary(self):
        relations = yaml.safe_load(
            (ROOT / 'config/model-relationships.yaml').read_text()
        )['relationships']
        by_pair = {
            frozenset((edge['from'], edge['to'])): edge['type']
            for edge in relations
        }
        self.assertEqual(
            by_pair[frozenset(('024', '076'))],
            'complementary',
        )
        self.assertEqual(
            by_pair[frozenset(('031', '054'))],
            'complementary',
        )

    def test_audit_contract_splits_confidence(self):
        audit = yaml.safe_load(
            (ROOT / 'schema/audit-output.yaml').read_text()
        )
        dims = audit['atomic_audit']['confidence_dimensions']
        self.assertEqual(
            set(dims),
            {
                'evidence_confidence',
                'mechanism_confidence',
                'underwriting_confidence',
            },
        )

    def test_benchmark_tracks_incremental_utility(self):
        benchmark = yaml.safe_load(
            (ROOT / 'schema/benchmark.yaml').read_text()
        )
        row = benchmark['case']['relevance_matrix'][0]
        self.assertIn('incremental_information', row)
        self.assertIn('decision_impact', row)
        self.assertIn('shared_evidence_with_models', row)
        self.assertIn('same_conclusion_with_models', row)

    @staticmethod
    def entry(status):
        data = yaml.safe_load(
            (ROOT / 'content-manifest.yaml').read_text()
        )
        entry = dict(data['models'][0])
        entry['mapping_status'] = status
        return entry


if __name__ == '__main__':
    unittest.main()
