#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from masonmark_lib import load_json, validate_binding_manifest, ensure_demo_sqlite, sqlite_columns

ROOT = Path(__file__).resolve().parents[1]


def generate_readiness(binding_manifest: dict[str, Any], physical_bindings: dict[str, Any]) -> dict[str, Any]:
    ensure_demo_sqlite(physical_bindings)
    contracts = []
    ready = deferred = failed = 0
    for contract in binding_manifest['logical_contracts']:
        lv = contract['logical_view']
        binding = physical_bindings['bindings'].get(lv)
        checks = []
        missing = []
        unexpected = []
        status = 'ready'
        if not binding:
            status = 'failed'
            checks.append({'name': 'binding_present', 'status': 'failed', 'detail': 'missing'})
        else:
            checks.append({'name': 'binding_present', 'status': 'passed', 'detail': lv})
            if binding.get('read_only_asserted') is True:
                checks.append({'name': 'read_only_asserted', 'status': 'passed', 'detail': True})
            else:
                status = 'deferred'
                checks.append({'name': 'read_only_asserted', 'status': 'deferred', 'detail': binding.get('read_only_asserted')})
            if binding.get('steward_owner') and binding.get('steward_owner') != 'CHANGE_ME':
                checks.append({'name': 'steward_owner', 'status': 'passed', 'detail': binding.get('steward_owner')})
            else:
                status = 'deferred' if status != 'failed' else status
                checks.append({'name': 'steward_owner', 'status': 'deferred', 'detail': binding.get('steward_owner')})
            if binding.get('engine') == 'sqlite' and binding.get('database') and binding.get('table'):
                try:
                    actual = sqlite_columns(binding)
                    required = [c['name'] for c in contract['approved_columns']]
                    missing = [c for c in required if c not in actual]
                    unexpected = [c for c in actual if c not in required]
                    if missing:
                        status = 'failed'
                        checks.append({'name': 'required_columns', 'status': 'failed', 'detail': {'missing': missing}})
                    else:
                        checks.append({'name': 'required_columns', 'status': 'passed', 'detail': {'count': len(required)}})
                    checks.append({'name': 'unexpected_columns', 'status': 'passed', 'detail': {'count': len(unexpected)}})
                except Exception as exc:
                    status = 'failed'
                    checks.append({'name': 'sqlite_introspection', 'status': 'failed', 'detail': str(exc)})
            else:
                status = 'deferred' if status != 'failed' else status
                checks.append({'name': 'physical_introspection', 'status': 'deferred', 'detail': 'requires live validation'})
        if status == 'ready':
            ready += 1
        elif status == 'deferred':
            deferred += 1
        else:
            failed += 1
        contracts.append({'schema_id': contract['schema_id'], 'logical_view': lv, 'status': status, 'checks': checks, 'missing_columns': missing, 'unexpected_columns': unexpected})
    return {'environment': physical_bindings['environment'], 'generated_at_utc': datetime.now(timezone.utc).isoformat(), 'summary': {'contracts_total': len(contracts), 'contracts_ready': ready, 'contracts_deferred': deferred, 'contracts_failed': failed}, 'contracts': contracts}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--binding-manifest', default='fixtures/masonmark/grant_stewardship.binding_manifest.v0.json')
    ap.add_argument('--physical-bindings', default='fixtures/masonmark/grant_stewardship.physical_bindings.demo.v0.json')
    ap.add_argument('--output-json', default='outputs/masonmark_binding_readiness_report.demo.json')
    args = ap.parse_args()
    binding_manifest = load_json(ROOT / args.binding_manifest)
    physical_bindings = load_json(ROOT / args.physical_bindings)
    errors = validate_binding_manifest(binding_manifest)
    if errors:
        raise SystemExit('\n'.join(errors))
    report = generate_readiness(binding_manifest, physical_bindings)
    out = ROOT / args.output_json
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f"[OK] wrote readiness report to {out}")


if __name__ == '__main__':
    main()
