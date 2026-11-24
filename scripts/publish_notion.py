#!/usr/bin/env python3
"""Incremental, guarded GitHub-to-Notion course publisher."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import random
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION = '2026-03-11'
RETRYABLE = {429, 500, 502, 503, 504, 529}
MARKER = 'GitHub content SHA256: '

class PublishError(Exception):
    pass

def request(method, page_id, token, body=None, attempts=4, opener=urlopen, sleeper=time.sleep):
    url = f'https://api.notion.com/v1/pages/{page_id}/markdown'
    data = json.dumps(body, ensure_ascii=False).encode() if body is not None else None
    for attempt in range(attempts):
        req = Request(url, data=data, method=method, headers={
            'Authorization': f'Bearer {token}', 'Notion-Version': VERSION,
            'Content-Type': 'application/json',
        })
        try:
            with opener(req, timeout=90) as response:
                if response.status != 200:
                    raise PublishError(f'Unexpected Notion HTTP {response.status}')
                return json.load(response)
        except HTTPError as exc:
            if exc.code not in RETRYABLE or attempt == attempts - 1:
                raise PublishError(f'Notion HTTP {exc.code} for {page_id}') from None
            retry_after = exc.headers.get('Retry-After')
            delay = min(30, float(retry_after)) if retry_after and retry_after.replace('.', '', 1).isdigit() else min(30, 2 ** attempt + random.random())
        except (URLError, TimeoutError) as exc:
            if attempt == attempts - 1:
                raise PublishError(f'Notion connection failure for {page_id}: {type(exc).__name__}') from None
            delay = min(30, 2 ** attempt + random.random())
        sleeper(delay)
    raise AssertionError('unreachable')

def validate_response(page, page_id):
    if page.get('object') != 'page_markdown' or page.get('id', '').replace('-', '') != page_id:
        raise PublishError(f'Unexpected Notion response for {page_id}')
    if page.get('truncated') or page.get('unknown_block_ids'):
        raise PublishError(f'Notion returned incomplete page {page_id}')
    if page.get('warnings'):
        raise PublishError(f'Notion reported content warnings for {page_id}')
    return page.get('markdown', '')

def desired(entry):
    body = (ROOT / entry['github_path']).read_text(encoding='utf-8').rstrip()
    def absolute_link(match):
        label, target = match.groups()
        if target.startswith(('./', '../')) or (':' not in target and not target.startswith(('/', '#'))):
            resolved = (ROOT / entry['github_path']).parent.joinpath(target.split('#')[0]).resolve()
            if not resolved.is_relative_to(ROOT / 'docs'):
                raise PublishError(f'Link leaves docs: {target}')
            site_path = resolved.relative_to(ROOT / 'docs').as_posix()
            site_path = re.sub(r'\.md$', '/', site_path)
            if site_path == 'index/':
                site_path = ''
            fragment = '#' + target.split('#', 1)[1] if '#' in target else ''
            target = f'https://tanghuaizhe.github.io/mental-models-audit/{site_path}{fragment}'
        return f'[{label}]({target})'
    body = re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)', absolute_link, body)
    source = f"https://github.com/TangHuaiZhe/mental-models-audit/blob/main/{entry['github_path']}"
    return f'{body}\n\n---\n\n[GitHub 唯一内容源]({source}) · {MARKER}{entry["content_hash"].removeprefix("sha256:")}\n'

def publish(manifest, apply, model_id=None, state_path=None, token=None, client=request):
    entries = manifest['models']
    if model_id:
        entries = [e for e in entries if e['model_id'] == model_id]
        if not entries:
            raise PublishError(f'Unknown model ID {model_id}')
    state = {'started_at': datetime.now(timezone.utc).isoformat(), 'mode': 'apply' if apply else 'dry-run', 'results': []}
    if apply and not token:
        raise PublishError('NOTION_API_KEY is required for apply')
    failures = 0
    for entry in entries:
        item = {'model_id': entry['model_id'], 'page_id': entry['notion_page_id'], 'content_hash': entry['content_hash']}
        try:
            if not apply:
                item['status'] = 'would_publish' if entry['mapping_status'] == 'verified' else 'mapping_missing' if entry['mapping_status'] == 'missing' else 'mapping_unverified'
            elif entry['mapping_status'] != 'verified':
                raise PublishError('mapping is unverified')
            else:
                before = validate_response(client('GET', entry['notion_page_id'], token), entry['notion_page_id'])
                marker = MARKER + entry['content_hash'].removeprefix('sha256:')
                if marker in before:
                    item['status'] = 'unchanged'
                else:
                    after = client('PATCH', entry['notion_page_id'], token, {
                        'type': 'replace_content', 'replace_content': {'new_str': desired(entry)},
                        'markdown_version': 'v2', 'allow_async': False,
                    })
                    validate_response(after, entry['notion_page_id'])
                    reread = validate_response(client('GET', entry['notion_page_id'], token), entry['notion_page_id'])
                    if marker not in reread:
                        raise PublishError('post-write verification marker missing')
                    item['status'] = 'published'
                    item['last_sync'] = datetime.now(timezone.utc).isoformat()
                    entry['last_sync'] = item['last_sync']
        except (PublishError, OSError) as exc:
            item['status'] = 'failed'
            item['error'] = str(exc)
            failures += 1
        state['results'].append(item)
        print(f"{entry['model_id']}: {item['status']}" + (f" ({item['error']})" if 'error' in item else ''))
        if state_path:
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    state['finished_at'] = datetime.now(timezone.utc).isoformat()
    if state_path:
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    return failures

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Write verified mappings to Notion')
    parser.add_argument('--model-id', help='Publish only one model, e.g. 001')
    parser.add_argument('--state', type=Path, default=ROOT / '.notion-publish-state.json')
    parser.add_argument('--write-manifest', action='store_true', help='Persist last_sync after successful apply')
    args = parser.parse_args()
    path = ROOT / 'content-manifest.yaml'
    manifest = yaml.safe_load(path.read_text())
    failures = publish(manifest, args.apply, args.model_id, args.state, os.environ.get('NOTION_API_KEY'))
    if args.apply and args.write_manifest and not failures:
        path.write_text(yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False, width=120))
    return 1 if failures else 0

if __name__ == '__main__':
    sys.exit(main())
