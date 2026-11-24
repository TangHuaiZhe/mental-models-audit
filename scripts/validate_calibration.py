#!/usr/bin/env python3
"""Validate the frozen model set, publication manifest, and calibration contracts."""
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
        assert (
            entry['notion_page_id'] is None and entry['mapping_status'] == 'missing'
        ) or (
            entry['notion_page_id']
            and re.fullmatch(r'[0-9a-f]{32}', entry['notion_page_id'])
            and entry['mapping_status'] != 'missing'
        ), model['id']
        assert model['source'] == entry['github_path'], model['id']
        assert model['path'] == entry['skill_path'], model['id']
        for key in ('github_path', 'skill_path'):
            path = ROOT / entry[key]
            assert path.is_file() and path.resolve().is_relative_to(ROOT), str(path)
        digest = hashlib.sha256((ROOT / entry['github_path']).read_bytes()).hexdigest()
        assert entry['content_hash'] == 'sha256:' + digest, model['id']

    required_yaml = (
        'config/router.yaml',
        'config/model-routing-metadata.yaml',
        'config/mechanism-clusters.yaml',
        'config/model-relationships.yaml',
        'schema/audit-output.yaml',
        'schema/benchmark.yaml',
        'tests/regression-cases.yaml',
        'config/versions.yaml',
    )
    docs = {path: load(path) for path in required_yaml}
    for path, data in docs.items():
        assert isinstance(data, dict), path

    versions = docs['config/versions.yaml']
    assert versions['model_set'] == '1.0.0'
    assert versions['router'] == '5.0.0'
    assert versions['audit_output_contract'] == '5.0.0'
    assert versions['benchmark_contract'] == '2.0.0'
    assert versions['mechanism_clusters'] == '4.0.0'
    assert versions['model_relationships'] == '1.0.0'

    clusters_doc = docs['config/mechanism-clusters.yaml']
    assert clusters_doc['relationship_source'] == 'config/model-relationships.yaml'
    for cluster in clusters_doc['clusters'].values():
        assert cluster['relation'] in ('duplicate', 'complementary', 'object_specific', 'object-specific')
        assert cluster['primary_model'] in cluster['members']
        assert set(cluster['members']) <= set(expected)
        assert cluster['dedup_policy'] == 'pairwise_relationship_graph'

    relationship_doc = docs['config/model-relationships.yaml']
    assert relationship_doc['default_when_missing'] == 'none'
    allowed_relations = {
        'duplicate', 'complementary', 'object_specific', 'prerequisite',
        'supports', 'commonly_confused_with', 'conflicts_with'
    }
    seen_pairs = set()
    for edge in relationship_doc['relationships']:
        assert edge['from'] in expected and edge['to'] in expected
        assert edge['from'] != edge['to']
        assert edge['type'] in allowed_relations
        key = (edge['from'], edge['to'], edge['type'])
        reverse = (edge['to'], edge['from'], edge['type'])
        assert key not in seen_pairs and reverse not in seen_pairs, f'duplicate relationship {key}'
        seen_pairs.add(key)

    router = docs['config/router.yaml']
    assert router['version'] == 5
    assert 'same_cluster_already_selected' not in router['scoring'], 'blanket cluster penalty must not return'
    assert router['scoring']['duplicate_relation_already_selected'] < 0
    assert router['relationship_policy']['source'] == 'config/model-relationships.yaml'

    audit = docs['schema/audit-output.yaml']
    assert audit['version'] == 5
    assert audit['contract_version'] == 'audit-output/5.0'
    confidence = audit['atomic_audit']['confidence_dimensions']
    assert set(confidence) == {
        'evidence_confidence', 'mechanism_confidence', 'underwriting_confidence'
    }
    evidence = audit['atomic_audit']['evidence_for'][0]
    for key in (
        'as_of_date', 'metric_period', 'published_at', 'retrieved_at',
        'claim_type', 'source_type', 'evidence_quality', 'normalization'
    ):
        assert key in evidence, f'missing evidence field {key}'

    benchmark = docs['schema/benchmark.yaml']
    assert benchmark['version'] == 2
    assert benchmark['schema'] == 'benchmark-v2'
    case = benchmark['case']
    assert case['router_version'] == '5.0.0'
    assert case['audit_output_contract'] == '5.0.0'
    row = case['relevance_matrix'][0]
    for key in ('incremental_information', 'decision_impact', 'shared_evidence_with_models', 'same_conclusion_with_models'):
        assert key in row, f'missing benchmark field {key}'
    assert case['completeness']['expected_model_count'] == 100

    print(
        'Calibration validation passed: 100 frozen models, manifest hashes, '
        f'{len(mapped)} mapped page IDs, relationship-aware Router v5, '
        'audit-output v5, benchmark v2.'
    )

if __name__ == '__main__':
    try:
        validate()
    except (AssertionError, KeyError, TypeError, ValueError) as exc:
        print(f'Calibration validation failed: {exc}', file=sys.stderr)
        raise SystemExit(1)
