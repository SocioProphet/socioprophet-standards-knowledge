#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load_graph(paths):
    try:
        from rdflib import Graph
    except Exception as exc:
        raise RuntimeError("rdflib is required to run validate_all.py") from exc

    graph = Graph()
    for raw in paths:
        path = Path(raw)
        candidates = sorted(path.rglob("*.ttl")) if path.is_dir() else [path]
        for candidate in candidates:
            if candidate.suffix != ".ttl":
                continue
            graph.parse(candidate.read_text(), format="turtle")
    return graph


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Ontogenesis semantic core SHACL pack against one or more Turtle graphs.")
    parser.add_argument("--data", nargs="+", required=True, help="One or more Turtle files or directories containing Turtle graphs.")
    parser.add_argument("--shapes", default="policy/shapes/master.shacl.ttl", help="Path to the default master SHACL file.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of human text.")
    args = parser.parse_args()

    try:
        from rdflib import Graph
        from pyshacl import validate
    except Exception as exc:
        print("validate_all.py requires rdflib and pyshacl", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 2

    data_graph = _load_graph(args.data)
    shacl_graph = Graph().parse(Path(args.shapes).read_text(), format="turtle")

    conforms, _report_graph, report_text = validate(
        data_graph,
        shacl_graph=shacl_graph,
        inference="rdfs",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
    )

    payload = {
        "conforms": bool(conforms),
        "triples": len(data_graph),
        "shapes_path": args.shapes,
        "report_text": report_text,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"conforms={payload['conforms']}")
        print(f"triples={payload['triples']}")
        print(f"shapes={payload['shapes_path']}")
        print(payload["report_text"])

    return 0 if conforms else 1


if __name__ == "__main__":
    raise SystemExit(main())
