#!/usr/bin/env python3
from __future__ import annotations
import time, statistics
from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parents[1]

def run(cmd: list[str]) -> float:
    t0 = time.perf_counter()
    r = subprocess.run(cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    dt = time.perf_counter() - t0
    if r.returncode != 0:
        print(r.stdout)
        raise SystemExit(f"[FAIL] Command failed: {' '.join(cmd)}")
    return dt

def main():
    # Ensure hygiene first
    run(["make", "hygiene"])
    # Baseline: current generator already includes AUX vectors; to simulate no-aux we can filter verification input.
    # For v0, we'll measure generator+verify as-is, and measure verify-only on filtered fixture file as "no_aux".
    fixture = ROOT / "fixtures" / "knowledge_vectors_hex_pathA.txt"
    if not fixture.exists():
        run([str(ROOT/".venv/bin/python") if (ROOT/".venv/bin/python").exists() else "python3", "tools/generate_knowledge_tritrpc_fixtures.py"])

    lines = fixture.read_text().splitlines()
    header = [ln for ln in lines if ln.startswith("#")]
    body = [ln for ln in lines if ln and not ln.startswith("#")]
    no_aux = header + [ln for ln in body if ".AUX " not in ln]

    tmp = ROOT / "benchmarks" / "results" / "knowledge_vectors_hex_pathA.no_aux.txt"
    tmp.write_text("\n".join(no_aux) + "\n")

    # measure verify on filtered file by temporarily swapping the fixture path via env var
    env = dict(**os.environ)
    env["KC_FIXTURE_OVERRIDE"] = str(tmp)

    def verify(dt_list):
        cmd = [str(ROOT/".venv/bin/python") if (ROOT/".venv/bin/python").exists() else "python3", "tools/verify_knowledge_tritrpc_fixtures.py"]
        t0 = time.perf_counter()
        r = subprocess.run(cmd, cwd=str(ROOT), env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        dt = time.perf_counter() - t0
        if r.returncode != 0:
            print(r.stdout)
            raise SystemExit("[FAIL] verify failed under KC_FIXTURE_OVERRIDE")
        dt_list.append(dt)

    import os
    # no_aux verify timings
    no_aux_times = []
    for _ in range(5):
        verify(no_aux_times)

    # aux-inclusive: regenerate + verify timings
    aux_times = []
    for _ in range(5):
        dt = run([str(ROOT/".venv/bin/python") if (ROOT/".venv/bin/python").exists() else "python3", "tools/generate_knowledge_tritrpc_fixtures.py"])
        dt2 = run([str(ROOT/".venv/bin/python") if (ROOT/".venv/bin/python").exists() else "python3", "tools/verify_knowledge_tritrpc_fixtures.py"])
        aux_times.append(dt + dt2)

    def summarize(xs):
        return {"min": min(xs), "p50": statistics.median(xs), "p95": sorted(xs)[int(0.95*(len(xs)-1))], "max": max(xs)}

    print("[OK] no_aux verify seconds:", summarize(no_aux_times))
    print("[OK] with_aux gen+verify seconds:", summarize(aux_times))

if __name__ == "__main__":
    main()
