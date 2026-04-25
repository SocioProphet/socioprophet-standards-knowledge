#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_schema(abd: dict, schema_path: Path) -> None:
    import jsonschema
    schema = load_json(schema_path)
    jsonschema.validate(abd, schema)


def abd_to_turtle(abd: dict) -> str:
    lines = [
        '@prefix bind: <https://socioprophet.github.io/ontogenesis/Lower/bindings#> .',
        '@prefix ex: <https://socioprophet.github.io/ontogenesis/examples/abd#> .',
        '',
    ]
    for item in abd.get("bindings", []):
        node = f"ex:{item['name']}"
        if item["type"] == "port":
            lines.extend([f"{node} a bind:Port ;", f"    bind:portNumber {int(item['portNumber'])} .", ""])
        elif item["type"] == "device":
            lines.extend([
                f"{node} a bind:DeviceNode ;",
                f"    bind:devicePath \"{item['devicePath']}\" ;",
                f"    bind:ioClaim \"{item['ioClaim']}\" .",
                "",
            ])
        elif item["type"] == "socket":
            lines.extend([f"{node} a bind:SocketEndpoint ;", f"    bind:socketPath \"{item['socketPath']}\" .", ""])
    return "\n".join(lines)


def run_shacl(turtle_text: str, shapes_path: Path) -> tuple[bool, str]:
    from rdflib import Graph
    from pyshacl import validate
    with TemporaryDirectory() as tmpdir:
        data_path = Path(tmpdir) / "abd.ttl"
        data_path.write_text(turtle_text, encoding="utf-8")
        data_graph = Graph().parse(data_path, format="turtle")
        shacl_graph = Graph().parse(shapes_path, format="turtle")
        conforms, _report_graph, report_text = validate(data_graph, shacl_graph=shacl_graph, inference="rdfs", abort_on_first=False, allow_infos=True, allow_warnings=True)
        return bool(conforms), report_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Agent Binding Descriptor with JSON Schema and SHACL.")
    parser.add_argument("--abd", required=True)
    parser.add_argument("--schema", default="Lower/bindings/abd.schema.json")
    parser.add_argument("--shapes", default="Lower/shapes/bindings.shacl.ttl")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    repo_root = Path.cwd().resolve()
    abd_path = (repo_root / args.abd).resolve() if not Path(args.abd).is_absolute() else Path(args.abd)
    schema_path = (repo_root / args.schema).resolve() if not Path(args.schema).is_absolute() else Path(args.schema)
    shapes_path = (repo_root / args.shapes).resolve() if not Path(args.shapes).is_absolute() else Path(args.shapes)

    abd = load_json(abd_path)
    validate_schema(abd, schema_path)
    ttl = abd_to_turtle(abd)
    conforms, report_text = run_shacl(ttl, shapes_path)

    payload = {
        "conforms": conforms,
        "abd_path": str(abd_path),
        "schema_path": str(schema_path),
        "shapes_path": str(shapes_path),
        "binding_count": len(abd.get("bindings", [])),
        "report_text": report_text,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"conforms={payload['conforms']}")
        print(f"abd={payload['abd_path']}")
        print(f"bindings={payload['binding_count']}")
        print(payload['report_text'])

    return 0 if conforms else 1


if __name__ == "__main__":
    raise SystemExit(main())
