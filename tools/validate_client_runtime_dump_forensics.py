#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "docs" / "standards" / "052-client-runtime-object-dump-forensics.md"
SCHEMA = ROOT / "schemas" / "jsonschema" / "client-runtime-diagnostic-record.schema.json"
ARTIFACT_SET_SCHEMA = ROOT / "schemas" / "jsonschema" / "knowledge-context-artifact-set.schema.json"
UNSAFE = ROOT / "fixtures" / "client-runtime-dump" / "unsafe.synthetic.txt"
SAFE = ROOT / "fixtures" / "client-runtime-dump" / "safe.redacted.txt"
EXAMPLE = ROOT / "fixtures" / "client-runtime-dump" / "client_runtime_diagnostic_record.example.json"
MAPPING = ROOT / "fixtures" / "client-runtime-dump" / "knowledge_context_mapping.example.json"

REQUIRED_FILES = [STANDARD, SCHEMA, ARTIFACT_SET_SCHEMA, UNSAFE, SAFE, EXAMPLE, MAPPING]

REQUIRED_STANDARD_TOKENS = [
    "Client Runtime Object Dump Forensics and Redaction v0.1",
    "MUST treat raw browser console/object dumps as sensitive",
    "Runtime graph interpretation rules",
    "Event logging controls",
    "Source-card and favicon guidance",
    "ClientRuntimeDiagnosticRecord",
]

REQUIRED_SCHEMA_TOKENS = [
    "ClientRuntimeDiagnosticRecord",
    "sourceClass",
    "nativeObjectLogged",
    "removedClasses",
    "framework_random_suffixes",
    "severity",
]

REQUIRED_ARTIFACT_SET_SCHEMA_TOKENS = [
    "KnowledgeContextArtifactSet",
    "Note",
    "Claim",
    "Annotation",
    "MeriotopographicEdge",
    "ProvenanceRecord",
    "derives_from",
    "redacted_by",
    "anchors_to",
]

REQUIRED_UNSAFE_TOKENS = [
    "SYNTHETIC_COOKIE_MATERIAL",
    "SYNTHETIC_CLIENT_AUTH_INFO",
    "SYNTHETIC_CONVERSATION_ID",
    "__reactContainer$SYNTHETIC",
    "containerInfo",
]

REQUIRED_SAFE_TOKENS = [
    "REDACTED_COOKIE_BLOB",
    "REDACTED_PRIVATE_ROUTE",
    "REDACTED_SUFFIX",
    "containerInfo",
]

REQUIRED_MAPPING_KINDS = {
    "Note",
    "Claim",
    "Annotation",
    "MeriotopographicEdge",
    "ProvenanceRecord",
}

REQUIRED_MAPPING_PREDICATES = {"derives_from", "redacted_by", "anchors_to"}

FORBIDDEN_FIXTURE_REGEXES = [
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"),
    re.compile(r"https://[^\\s]+/(?:private|conversation|tenant|workspace|account)/[^\\s\\]\\)]+"),
]


def fail(message: str) -> int:
    print(f"ERR: {message}", file=sys.stderr)
    return 2


def require_tokens(label: str, text: str, tokens: list[str]) -> None:
    missing = [token for token in tokens if token not in text]
    if missing:
        raise ValueError(f"{label} missing required tokens: {missing}")


def reject_forbidden_fixture_text(label: str, text: str) -> None:
    hits: list[str] = []
    for regex in FORBIDDEN_FIXTURE_REGEXES:
        hits.extend(match.group(0) for match in regex.finditer(text))
    if hits:
        raise ValueError(f"{label} contains forbidden non-synthetic diagnostic text: {hits[:3]}")


def require_example_matches_schema_shape(schema: dict, example: dict) -> None:
    required = schema.get("required", [])
    missing = [key for key in required if key not in example]
    if missing:
        raise ValueError(f"example missing schema-required keys: {missing}")

    if example.get("kind") != "ClientRuntimeDiagnosticRecord":
        raise ValueError("example.kind must be ClientRuntimeDiagnosticRecord")
    if example.get("version") != "0.1":
        raise ValueError("example.version must be 0.1")

    event = example.get("event")
    if not isinstance(event, dict):
        raise ValueError("example.event must be an object")
    if event.get("nativeObjectLogged") is not False:
        raise ValueError("example.event.nativeObjectLogged must be false")

    redaction = example.get("redaction")
    if not isinstance(redaction, dict):
        raise ValueError("example.redaction must be an object")
    removed = redaction.get("removedClasses")
    if not isinstance(removed, list) or "cookies" not in removed or "auth_session" not in removed:
        raise ValueError("example.redaction.removedClasses must include cookies and auth_session")

    if example.get("severity") not in {"informational", "low", "medium", "high"}:
        raise ValueError("example.severity must be informational, low, medium, or high")


def require_mapping_matches_artifact_set_schema_shape(schema: dict, mapping: dict) -> None:
    required = schema.get("required", [])
    missing = [key for key in required if key not in mapping]
    if missing:
        raise ValueError(f"mapping missing artifact-set schema-required keys: {missing}")

    if mapping.get("kind") != "KnowledgeContextArtifactSet":
        raise ValueError("mapping.kind must be KnowledgeContextArtifactSet")
    if mapping.get("version") != "0.1":
        raise ValueError("mapping.version must be 0.1")
    if not mapping.get("id"):
        raise ValueError("mapping.id must be present")
    if not mapping.get("sourceStandard"):
        raise ValueError("mapping.sourceStandard must be present")


def require_mapping_shape(mapping: dict) -> None:
    artifacts = mapping.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("mapping.artifacts must be a non-empty list")

    kinds = {artifact.get("kind") for artifact in artifacts if isinstance(artifact, dict)}
    missing_kinds = sorted(REQUIRED_MAPPING_KINDS - kinds)
    if missing_kinds:
        raise ValueError(f"mapping missing artifact kinds: {missing_kinds}")

    predicates = {
        artifact.get("predicate")
        for artifact in artifacts
        if isinstance(artifact, dict) and artifact.get("kind") == "MeriotopographicEdge"
    }
    missing_predicates = sorted(REQUIRED_MAPPING_PREDICATES - predicates)
    if missing_predicates:
        raise ValueError(f"mapping missing required predicates: {missing_predicates}")

    provenance_ids = {
        artifact.get("id")
        for artifact in artifacts
        if isinstance(artifact, dict) and artifact.get("kind") == "ProvenanceRecord"
    }
    if "provenance:client-runtime-dump.synthetic.redaction.v0" not in provenance_ids:
        raise ValueError("mapping missing synthetic redaction provenance record")


def main() -> int:
    try:
        for path in REQUIRED_FILES:
            if not path.exists():
                raise FileNotFoundError(path)

        standard_text = STANDARD.read_text(encoding="utf-8")
        schema_text = SCHEMA.read_text(encoding="utf-8")
        artifact_set_schema_text = ARTIFACT_SET_SCHEMA.read_text(encoding="utf-8")
        unsafe_text = UNSAFE.read_text(encoding="utf-8")
        safe_text = SAFE.read_text(encoding="utf-8")
        mapping_text = MAPPING.read_text(encoding="utf-8")

        require_tokens("standard", standard_text, REQUIRED_STANDARD_TOKENS)
        require_tokens("schema", schema_text, REQUIRED_SCHEMA_TOKENS)
        require_tokens("artifact-set schema", artifact_set_schema_text, REQUIRED_ARTIFACT_SET_SCHEMA_TOKENS)
        require_tokens("unsafe fixture", unsafe_text, REQUIRED_UNSAFE_TOKENS)
        require_tokens("safe fixture", safe_text, REQUIRED_SAFE_TOKENS)
        reject_forbidden_fixture_text("unsafe fixture", unsafe_text)
        reject_forbidden_fixture_text("safe fixture", safe_text)
        reject_forbidden_fixture_text("mapping fixture", mapping_text)

        schema = json.loads(schema_text)
        example = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        require_example_matches_schema_shape(schema, example)

        artifact_set_schema = json.loads(artifact_set_schema_text)
        mapping = json.loads(mapping_text)
        require_mapping_matches_artifact_set_schema_shape(artifact_set_schema, mapping)
        require_mapping_shape(mapping)
    except FileNotFoundError as exc:
        return fail(f"missing required file: {exc.args[0]}")
    except Exception as exc:  # noqa: BLE001 - validator should surface direct error text
        return fail(str(exc))

    print("OK: validated client runtime dump forensics schemas, fixtures, knowledge mapping, and synthetic-only guards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
