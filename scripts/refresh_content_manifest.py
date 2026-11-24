#!/usr/bin/env python3
"""Refresh or check course content hashes in content-manifest.yaml."""
import argparse
import hashlib
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'content-manifest.yaml'


def expected_hash(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()


def refresh(manifest, write=False):
    changed = []
    for entry in manifest['models']:
        path = ROOT / entry['github_path']
        digest = expected_hash(path)
        if entry.get('content_hash') != digest:
            changed.append((entry['model_id'], entry.get('content_hash'), digest))
            if write:
                entry['content_hash'] = digest
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--write',
        action='store_true',
        help='Update stale hashes in content-manifest.yaml',
    )
    args = parser.parse_args()

    manifest = yaml.safe_load(MANIFEST.read_text(encoding='utf-8'))
    changed = refresh(manifest, write=args.write)

    if not changed:
        print('Content manifest hashes are current.')
        return 0

    for model_id, old, new in changed:
        print(f'{model_id}: {old} -> {new}')

    if args.write:
        MANIFEST.write_text(
            yaml.safe_dump(
                manifest,
                allow_unicode=True,
                sort_keys=False,
                width=120,
            ),
            encoding='utf-8',
        )
        print(f'Updated {len(changed)} manifest hash(es).')
        return 0

    print(
        'Stale manifest hashes detected. Run the refresh_content_manifest '
        'script with --write after intentionally changing course files.',
        file=sys.stderr,
    )
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
