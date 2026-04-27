#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ARTIFACT_TYPES = {
    "GeoEntity", "Place", "Feature", "Asset", "SpaceAsset", "Vessel", "Aircraft",
    "Sensor", "Observation", "Track", "Event", "DecisionCard", "SensitiveGeoPolicy"
}
REQUIRED_TOP = ["artifact_type", "artifact_id", "entity", "relations", "provenance", "governance"]
REQUIRED_ENTITY = ["entity_id", "label", "entity_class"]
REQUIRED_PROVENANCE = ["source_refs", "method", "generated_at"]
REQUIRED_GOVERNANCE = ["knowledge_visibility", "masking_policy", "license_ref"]


def fail(msg: str) -> None:
    print(f"ERR: {msg}", file=sys.stderr)
    raise SystemExit(2)


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path}: invalid JSON: {exc}")
    if not isinstance(data, dict):
        fail(f"{path}: expected top-level object")
    return data


def require_keys(obj: dict, keys: list[str], where: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        fail(f"{where}: missing required keys: {', '.join(missing)}")


def validate_fixture(path: Path) -> None:
    data = load_json(path)
    require_keys(data, REQUIRED_TOP, str(path))
    if data["artifact_type"] not in ARTIFACT_TYPES:
        fail(f"{path}: unsupported artifact_type {data['artifact_type']!r}")
    if not isinstance(data["entity"], dict):
        fail(f"{path}: entity must be object")
    require_keys(data["entity"], REQUIRED_ENTITY, f"{path}:entity")
    if not isinstance(data["relations"], list):
        fail(f"{path}: relations must be array")
    for idx, rel in enumerate(data["relations"]):
        if not isinstance(rel, dict):
            fail(f"{path}: relation[{idx}] must be object")
        require_keys(rel, ["predicate", "object_ref"], f"{path}:relation[{idx}]")
    if not isinstance(data["provenance"], dict):
        fail(f"{path}: provenance must be object")
    require_keys(data["provenance"], REQUIRED_PROVENANCE, f"{path}:provenance")
    if not isinstance(data["provenance"].get("source_refs"), list):
        fail(f"{path}: provenance.source_refs must be array")
    if not isinstance(data["governance"], dict):
        fail(f"{path}: governance must be object")
    require_keys(data["governance"], REQUIRED_GOVERNANCE, f"{path}:governance")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    schema = root / "schemas/jsonschema/multidomain/multidomain_geospatial_knowledge_artifact.v1.schema.json"
    if not schema.exists():
        fail(f"missing schema: {schema.relative_to(root)}")
    load_json(schema)
    fixture_dir = root / "fixtures/multidomain"
    fixtures = sorted(fixture_dir.glob("*.json")) if fixture_dir.exists() else []
    if not fixtures:
        fail("no multidomain knowledge fixtures found")
    for fixture in fixtures:
        validate_fixture(fixture)
    print(f"OK: validated {len(fixtures)} multidomain geospatial knowledge fixture(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
