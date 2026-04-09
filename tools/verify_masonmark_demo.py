#!/usr/bin/env python3
from __future__ import annotations
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if r.returncode != 0:
        print(r.stdout)
        raise SystemExit(f"[FAIL] Command failed: {' '.join(cmd)}")


def main() -> None:
    py = str(ROOT / '.venv' / 'bin' / 'python') if (ROOT / '.venv' / 'bin' / 'python').exists() else 'python3'

    # 1) readiness
    readiness_out = ROOT / 'outputs' / 'masonmark_binding_readiness_report.demo.json'
    run([py, 'tools/masonmark_readiness.py', '--output-json', str(readiness_out)])
    rep = json.loads(readiness_out.read_text(encoding='utf-8'))
    summ = rep['summary']
    if summ['contracts_failed'] != 0:
        raise SystemExit(f"[FAIL] readiness contracts_failed={summ['contracts_failed']}")

    # 2) run fixtures
    outdir = ROOT / 'outputs' / 'masonmark_demo'
    run([py, 'tools/masonmark_run_fixtures.py', '--output-dir', str(outdir)])
    fr = json.loads((outdir / 'fixture_run_report.json').read_text(encoding='utf-8'))
    promote = sum(1 for r in fr['results'] if r['decision'] == 'promote')
    abstain = sum(1 for r in fr['results'] if r['decision'] == 'abstain')
    if promote < 3 or abstain < 3:
        raise SystemExit(f"[FAIL] fixture decisions unexpected: promote={promote} abstain={abstain}")

    print(f"[OK] Masonmark demo verified: promote={promote} abstain={abstain}; readiness_failed={summ['contracts_failed']}")


if __name__ == '__main__':
    main()
