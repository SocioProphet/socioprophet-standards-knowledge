#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_docs(paths):
    import yaml
    docs = []
    for raw in paths:
        path = Path(raw)
        candidates = sorted(path.rglob('*.yaml')) + sorted(path.rglob('*.yml')) if path.is_dir() else [path]
        for candidate in candidates:
            with candidate.open('r', encoding='utf-8') as fh:
                for doc in yaml.safe_load_all(fh):
                    if isinstance(doc, dict):
                        docs.append((str(candidate), doc))
    return docs


def platform(doc):
    annotations = ((doc.get('metadata') or {}).get('annotations') or {})
    value = annotations.get('socioprophet.io/platform') or annotations.get('prophet.socioprophet.io/platform')
    return str(value).lower() if value else ''


def required_entries(doc):
    annotations = ((doc.get('metadata') or {}).get('annotations') or {})
    raw = annotations.get('socioprophet.io/required-tolerations') or annotations.get('prophet.socioprophet.io/required-tolerations') or ''
    return [item.strip().lower() for item in str(raw).split(',') if item.strip()]


def pod_spec(doc):
    return (((doc.get('spec') or {}).get('template') or {}).get('spec') or {})


def toleration_strings(doc):
    out = []
    for item in pod_spec(doc).get('tolerations', []) or []:
        if isinstance(item, dict):
            parts = []
            for key in ('key', 'operator', 'value', 'effect'):
                if item.get(key) not in (None, ''):
                    parts.append(f'{key}={item[key]}')
            out.append(';'.join(parts).lower())
    return out


def check_doc(source, doc):
    if doc.get('kind') != 'Deployment':
        return []
    problems = []
    tolerations = toleration_strings(doc)
    for required in required_entries(doc):
        if not any(required in item for item in tolerations):
            problems.append({'source': source, 'reason': 'missing-required-toleration', 'required': required})
    if platform(doc) == 'kubeedge' and not any('edge' in item for item in tolerations):
        problems.append({'source': source, 'reason': 'missing-edge-toleration'})
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description='Check K8s scheduling toleration policy fixtures.')
    parser.add_argument('--manifest', nargs='+', required=True)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    docs = load_docs(args.manifest)
    problems = []
    for source, doc in docs:
        problems.extend(check_doc(source, doc))
    payload = {'conforms': not problems, 'documents': len(docs), 'problems': problems}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"conforms={payload['conforms']}")
        for problem in problems:
            print(f"{problem['source']}: {problem['reason']}")
    return 0 if not problems else 1


if __name__ == '__main__':
    raise SystemExit(main())
