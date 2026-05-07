#!/usr/bin/env python3
"""Validate canonical GRLPlus schemas and fixtures.

This is intentionally dependency-light and aligned with this repo's executable
standards style: schemas define shape, fixtures exercise shape, and this tool
returns non-zero on contract drift.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable


ROOT = Path(__file__).resolve().parents[1]
MODEL_SCHEMA = ROOT / "schemas/jsonschema/grlplus/model.schema.json"
LINT_SCHEMA = ROOT / "schemas/jsonschema/grlplus/lint-report.schema.json"
METRICS_SCHEMA = ROOT / "schemas/jsonschema/grlplus/metrics-report.schema.json"
FIXTURE_ROOT = ROOT / "fixtures/grlplus"


def die(msg: str, code: int = 2) -> None:
    print(f"[grlplus-validate] ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def load_json(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        die(f"failed to parse JSON {path}: {e}")
    if not isinstance(data, dict):
        die(f"{path} must parse to a JSON object")
    return data


def require_paths(paths: Iterable[Path]) -> None:
    for path in paths:
        if not path.exists():
            die(f"required file missing: {path}")


def validate_with_jsonschema(instance_path: Path, schema_path: Path) -> None:
    try:
        import jsonschema  # type: ignore
    except Exception as e:
        die(f"missing dependency: jsonschema is required ({e})")
    instance = load_json(instance_path)
    schema = load_json(schema_path)
    try:
        jsonschema.validate(instance, schema)
    except Exception as e:
        die(f"schema validation failed: {instance_path} against {schema_path}: {e}")


def check_unique_model_ids(model_path: Path) -> None:
    model = load_json(model_path)
    seen: dict[str, str] = {}
    collections = {
        "actors": model.get("actors", []),
        "elements": model.get("elements", []),
        "edges": model.get("edges", []),
        "decomposition_groups": model.get("decomposition_groups", []),
        "arguments": model.get("arguments", []),
        "argument_links": model.get("argument_links", []),
        "trace_links": model.get("trace_links", []),
        "evidence": model.get("evidence", []),
    }
    for collection_name, items in collections.items():
        if not isinstance(items, list):
            die(f"{model_path}: {collection_name} must be a list")
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                die(f"{model_path}: {collection_name}[{i}] must be an object")
            item_id = item.get("id")
            if not isinstance(item_id, str) or not item_id.strip():
                die(f"{model_path}: {collection_name}[{i}] missing non-empty id")
            if item_id in seen:
                die(f"{model_path}: duplicate id {item_id!r} in {collection_name}; first seen in {seen[item_id]}")
            seen[item_id] = collection_name


def main() -> int:
    require_paths([MODEL_SCHEMA, LINT_SCHEMA, METRICS_SCHEMA])
    require_paths([
        FIXTURE_ROOT / "models/model.launch.json",
        FIXTURE_ROOT / "reports/lint.model.launch.json",
        FIXTURE_ROOT / "reports/metrics.model.launch.json",
    ])

    validate_with_jsonschema(FIXTURE_ROOT / "models/model.launch.json", MODEL_SCHEMA)
    validate_with_jsonschema(FIXTURE_ROOT / "reports/lint.model.launch.json", LINT_SCHEMA)
    validate_with_jsonschema(FIXTURE_ROOT / "reports/metrics.model.launch.json", METRICS_SCHEMA)
    check_unique_model_ids(FIXTURE_ROOT / "models/model.launch.json")

    print("[grlplus-validate] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
