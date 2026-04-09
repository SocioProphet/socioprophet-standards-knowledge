from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> str:
    r = subprocess.run(cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if r.returncode != 0:
        print(r.stdout)
        raise AssertionError(f"command failed: {' '.join(cmd)}")
    return r.stdout


def test_masonmark_demo_smoke() -> None:
    py = str(ROOT / '.venv' / 'bin' / 'python') if (ROOT / '.venv' / 'bin' / 'python').exists() else sys.executable
    run([py, 'tools/verify_masonmark_demo.py'])
    report = json.loads((ROOT / 'outputs' / 'masonmark_demo' / 'fixture_run_report.json').read_text(encoding='utf-8'))
    promote = sum(1 for r in report['results'] if r['decision'] == 'promote')
    abstain = sum(1 for r in report['results'] if r['decision'] == 'abstain')
    assert promote >= 3
    assert abstain >= 3
