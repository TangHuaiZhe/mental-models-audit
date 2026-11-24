#!/usr/bin/env python3
"""Validate the frozen model set and publication manifest."""
from pathlib import Path
import hashlib
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return yaml.safe_load((ROOT / path).read_text(encoding='utf-8'))

def validate():
    registry = load('config/model-registry.yaml')['models']
    manifest = load('content-manifest.yaml')['models']
    expected = [f'{i:03d}' for i in range(1, 101)]
    assert [m['id'] for m in registry] == expected, 'registry must contain frozen IDs 001–100'
    assert [m['model_id'] for m in manifest] == expected, 'manifest must contain frozen IDs 001–100'
    mapped = [m['notion_page_id'] for m in manifest if m['notion_page_id']]
    assert len(mapped) == len(set(mapped)), 'duplicate Notion page ID'
    assert len({m['github_path'] for m in manifest}) == 100, 'active course paths must be unique'
    for model, entry in zip(registry, manifest):
        assert entry['mapping_status'] in ('missing', 'unverified', 'verified'), model['id']
        assert (entry['notion_page_id'] is None and entry['mapping_status'] == 'missing') or (entry['notion_page_id'] and re.fullmatch(r'[0-9a-f]{32}', entry['notion_page_id']) and entry['mapping_status'] != 'missing'), model['id']
        assert model['source'] == entry['github_path'], model['id']
        assert model['path'] == entry['skill_path'], model['id']
        for key in ('github_path', 'skill_path'):
            path = ROOT / entry[key]
            assert path.is_file() and path.resolve().is_relative_to(ROOT), str(path)
        digest = hashlib.sha256((ROOT / entry['github_path']).read_bytes()).hexdigest()
        assert entry['content_hash'] == 'sha256:' + digest, model['id']
    for path in ('config/router.yaml', 'config/model-routing-metadata.yaml', 'config/mechanism-clusters.yaml', 'schema/audit-output.yaml', 'schema/benchmark.yaml', 'tests/regression-cases.yaml', 'config/versions.yaml'):
        assert isinstance(load(path), dict), path
    relations = load('config/mechanism-clusters.yaml')['clusters']
    for cluster in relations.values():
        assert cluster['relation'] in ('duplicate', 'complementary', 'object-specific')
        assert cluster['primary_model'] in cluster['members']
        assert set(cluster['members']) <= set(expected)
    print(f'Calibration validation passed: 100 frozen models, course and skill paths, manifest hashes, {len(mapped)} mapped page IDs, YAML contracts.')

if __name__ == '__main__':
    try:
        validate()
    except (AssertionError, KeyError, ValueError) as exc:
        print(f'Calibration validation failed: {exc}', file=sys.stderr)
        raise SystemExit(1)
