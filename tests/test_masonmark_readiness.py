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


def test_masonmark_readiness_demo() -> None:
    py = str(ROOT / '.venv' / 'bin' / 'python') if (ROOT / '.venv' / 'bin' / 'python').exists() else sys.executable
    out = ROOT / 'outputs' / 'masonmark_binding_readiness_report.demo.json'
    run([py, 'tools/masonmark_readiness.py', '--output-json', str(out)])
    rep = json.loads(out.read_text(encoding='utf-8'))
    assert rep['summary']['contracts_total'] == 3
    assert rep['summary']['contracts_failed'] == 0
