#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CANONICAL_BASE = "https://socioprophet.github.io/ontogenesis/"


def _iter_turtle_candidates(raw_paths):
    for raw in raw_paths:
        path = Path(raw)
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        if path.is_dir():
            yield from sorted(p for p in path.rglob("*.ttl") if p.is_file())
        else:
            if path.suffix != ".ttl":
                raise ValueError(f"Expected a .ttl file or directory, got: {path}")
            yield path


def _load_graph(raw_paths):
    try:
        from rdflib import Graph
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("rdflib is required to run validate_all.py") from exc

    graph = Graph()
    for candidate in _iter_turtle_candidates(raw_paths):
        graph.parse(candidate, format="turtle")
    return graph


def _resolve_local_import(import_iri: str, repo_root: Path) -> Path | None:
    if not import_iri.startswith(CANONICAL_BASE):
        return None

    rel = import_iri.removeprefix(CANONICAL_BASE).lstrip("/")
    base = repo_root / rel
    probes = (
        base,
        Path(f"{base}.ttl"),
        Path(f"{base}.shacl.ttl"),
        Path(f"{base}.context.jsonld"),
    )
    for probe in probes:
        if probe.exists():
            return probe
    return None


def _load_shapes_graph(raw_shapes_path: str, repo_root: Path):
    try:
        from rdflib import Graph
        from rdflib.namespace import OWL
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("rdflib is required to run validate_all.py") from exc

    shapes_path = Path(raw_shapes_path)
    if not shapes_path.is_absolute():
        shapes_path = (repo_root / shapes_path).resolve()

    to_visit = [shapes_path]
    visited: set[Path] = set()
    unresolved_imports: set[str] = set()
    graph = Graph()

    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        if not current.exists():
            raise FileNotFoundError(f"Shapes path does not exist: {current}")
        if current.suffix != ".ttl":
            raise ValueError(f"Expected a .ttl SHACL file, got: {current}")

        doc = Graph()
        doc.parse(current, format="turtle")
        for triple in doc:
            graph.add(triple)
        visited.add(current)

        for imported in doc.objects(None, OWL.imports):
            import_iri = str(imported)
            local = _resolve_local_import(import_iri, repo_root)
            if local is not None:
                to_visit.append(local.resolve())
            else:
                unresolved_imports.add(import_iri)

    return graph, sorted(unresolved_imports)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the Ontogenesis master SHACL pack against one or more Turtle graphs."
    )
    parser.add_argument(
        "--data",
        nargs="+",
        required=True,
        help="One or more Turtle files or directories containing Turtle graphs.",
    )
    parser.add_argument(
        "--shapes",
        default="policy/shapes/master.shacl.ttl",
        help="Path to the master SHACL file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of human text.",
    )
    args = parser.parse_args()

    try:
        from pyshacl import validate
    except Exception as exc:  # pragma: no cover
        print("validate_all.py requires rdflib and pyshacl", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 2

    repo_root = Path.cwd().resolve()
    data_graph = _load_graph(args.data)
    shacl_graph, unresolved_imports = _load_shapes_graph(args.shapes, repo_root)

    conforms, report_graph, report_text = validate(
        data_graph,
        shacl_graph=shacl_graph,
        inference="rdfs",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
        do_owl_imports=bool(unresolved_imports),
    )

    if args.json:
        payload = {
            "conforms": bool(conforms),
            "report_text": report_text,
            "triples": len(data_graph),
            "shapes_path": args.shapes,
            "unresolved_imports": unresolved_imports,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"conforms={bool(conforms)}")
        print(f"triples={len(data_graph)}")
        print(f"shapes={args.shapes}")
        if unresolved_imports:
            print(f"unresolved_imports={len(unresolved_imports)}")
            for iri in unresolved_imports:
                print(f"import={iri}")
        print(report_text)

    return 0 if conforms else 1


if __name__ == "__main__":
    raise SystemExit(main())
