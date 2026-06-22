#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "docs" / "standards" / "053-reasoning-failure-mitigation-and-perturbation.md"
CASE_SCHEMA = ROOT / "schemas" / "jsonschema" / "reasoning-failure-case.v0.1.schema.json"
SUITE_SCHEMA = ROOT / "schemas" / "jsonschema" / "reasoning-perturbation-suite.v0.1.schema.json"
CASE_EXAMPLE = ROOT / "fixtures" / "reasoning-failure" / "reasoning_failure_case.exact_string.example.json"
SUITE_EXAMPLE = ROOT / "fixtures" / "reasoning-failure" / "reasoning_perturbation_suite.exactness.example.json"

ONTOLOGY_PREFIX = "https://socioprophet.github.io/ontogenesis/platform/reasoning-failure#"

REQUIRED_STANDARD_TOKENS = [
    "Standard 053: Reasoning Failure Mitigation and Perturbation v0.1",
    "ReasoningFailureCase",
    "PerturbationSuite",
    "Exactness profile",
    "Evaluator-bias controls",
    "Multimodal contradiction controls",
    "Ontogenesis owns the failure vocabulary",
]


def fail(message: str) -> int:
    print(f"ERR: {message}", file=sys.stderr)
    return 2


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_case(schema: dict, example: dict) -> None:
    required = schema.get("required", [])
    missing = [field for field in required if field not in example]
    require(not missing, f"case example missing required fields: {missing}")
    require(example["kind"] == "ReasoningFailureCase", "case.kind must be ReasoningFailureCase")
    require(example["version"] == "0.1", "case.version must be 0.1")
    require(example["failureModeRefs"], "case.failureModeRefs must not be empty")
    require(
        all(ref.startswith(ONTOLOGY_PREFIX) for ref in example["failureModeRefs"]),
        "failureModeRefs must use Ontogenesis reasoning-failure refs",
    )
    require(example["mitigationRefs"], "case.mitigationRefs must not be empty")
    require(
        all(ref.startswith(ONTOLOGY_PREFIX) for ref in example["mitigationRefs"]),
        "mitigationRefs must use Ontogenesis reasoning-failure refs",
    )
    verifier = example["verifier"]
    require(
        verifier["verifierFamily"] != "llm-judge-advisory" or verifier["llmJudgeOnly"] is False,
        "llm-judge-only cases are not allowed as trusted examples",
    )
    require(example["privacyBoundary"] == "synthetic-only", "bootstrap fixture must be synthetic-only")


def validate_suite(schema: dict, example: dict) -> None:
    required = schema.get("required", [])
    missing = [field for field in required if field not in example]
    require(not missing, f"suite example missing required fields: {missing}")
    require(example["kind"] == "ReasoningPerturbationSuite", "suite.kind must be ReasoningPerturbationSuite")
    require(example["version"] == "0.1", "suite.version must be 0.1")
    require(example["perturbations"], "suite.perturbations must not be empty")
    require(
        any(p["family"] == "identifier-rename" for p in example["perturbations"]),
        "suite must include identifier-rename perturbation",
    )
    require(
        any(p["family"] == "distractor-injection" for p in example["perturbations"]),
        "suite must include distractor-injection perturbation",
    )
    controls = example["evaluatorBiasControls"]
    require(controls["llmJudgeAllowed"] is False, "exactness bootstrap suite must disallow LLM judge")
    require(controls["orderRandomization"] is True, "suite must require order randomization")
    require(controls["contaminationNoteRequired"] is True, "suite must require contamination note")


def main() -> int:
    try:
        for path in [STANDARD, CASE_SCHEMA, SUITE_SCHEMA, CASE_EXAMPLE, SUITE_EXAMPLE]:
            if not path.exists():
                raise FileNotFoundError(path)
        standard = STANDARD.read_text(encoding="utf-8")
        missing_tokens = [token for token in REQUIRED_STANDARD_TOKENS if token not in standard]
        require(not missing_tokens, f"standard missing tokens: {missing_tokens}")

        case_schema = load_json(CASE_SCHEMA)
        suite_schema = load_json(SUITE_SCHEMA)
        case_example = load_json(CASE_EXAMPLE)
        suite_example = load_json(SUITE_EXAMPLE)

        require(case_schema.get("title") == "ReasoningFailureCase", "case schema title mismatch")
        require(suite_schema.get("title") == "ReasoningPerturbationSuite", "suite schema title mismatch")
        validate_case(case_schema, case_example)
        validate_suite(suite_schema, suite_example)
    except FileNotFoundError as exc:
        return fail(f"missing required file: {exc.args[0]}")
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))

    print("OK: validated reasoning-failure standard, schemas, and synthetic fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
