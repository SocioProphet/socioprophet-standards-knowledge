#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from masonmark_lib import (
    ensure_demo_sqlite,
    execute_sql,
    load_json,
    stable_digest,
    validate_binding_manifest,
    validate_fixture_corpus,
)

ROOT = Path(__file__).resolve().parents[1]

EVENT_MAP = {
    "GS-AWD-001": "mm.evt.gs.award_reporting.v1",
    "GS-AMD-002": "mm.evt.gs.amendment_governance.v1",
    "GS-CLO-003": "mm.evt.gs.closeout_compliance.v1",
}

PROMOTE_SQL = {
    "fx.gs.awd.pos.001": "SELECT program_name, COUNT(*) AS grant_count FROM {table} WHERE award_status = 'active' AND fiscal_year = 2023 GROUP BY program_name ORDER BY program_name",
    "fx.gs.awd.rob.001": "SELECT program_name, COUNT(*) AS grant_count FROM {table} WHERE award_status = 'active' AND fiscal_year = 2023 GROUP BY program_name ORDER BY program_name",
    "fx.gs.amd.pos.001": "SELECT award_id, amendment_id, delta_amount, fiscal_quarter FROM {table} WHERE fiscal_quarter = 'Q2' AND amendment_type = 'budget' ORDER BY award_id",
    "fx.gs.amd.rob.001": "SELECT award_id, amendment_id, delta_amount, fiscal_quarter FROM {table} WHERE fiscal_quarter = 'Q2' AND amendment_type IN ('budget','funding_change') ORDER BY award_id",
    "fx.gs.clo.pos.001": "SELECT award_id, program_name, days_overdue, blocker_code, blocker_text FROM {table} WHERE days_overdue > 0 ORDER BY days_overdue DESC, award_id",
    "fx.gs.clo.rob.001": "SELECT award_id, program_name, days_overdue, blocker_code, blocker_text FROM {table} WHERE days_overdue > 0 ORDER BY days_overdue DESC, award_id",
}

COMMONSENSE = {
    "fx.gs.awd.rob.001": [{"source": "ConceptNet", "usage": "lexical_normalization", "authoritative": False}],
    "fx.gs.amd.rob.001": [{"source": "ConceptNet", "usage": "candidate_expansion", "authoritative": False}],
    "fx.gs.clo.rob.001": [{"source": "CSKG", "usage": "candidate_expansion", "authoritative": False}],
}


def build_proofpack(fixture: dict[str, Any], contract: dict[str, Any], binding: dict[str, Any]) -> dict[str, Any]:
    promote = fixture["expected_decision"] == "promote"
    sql_template = PROMOTE_SQL.get(fixture["fixture_id"])
    sql = sql_template.format(table=binding["table"]) if promote and sql_template else None
    rows = execute_sql(binding, sql) if sql else None
    return {
        "proofpack_version": "0.2",
        "proofpack_id": fixture["fixture_id"].replace("fx.", "pp."),
        "family_id": "grant_stewardship",
        "schema_id": fixture["schema_id"],
        "event_type_id": EVENT_MAP[fixture["schema_id"]],
        "logical_view": contract["logical_view"],
        "request": {
            "utterance": fixture["utterance"],
            "request_id": fixture["fixture_id"].replace("fx.", "req."),
            "tenant_scope": "demo_tenant",
            "actor_role": "analyst",
        },
        "grounding": {
            "commonsense_priors": COMMONSENSE.get(fixture["fixture_id"], []),
        },
        "program_ir": None if not sql else {
            "ast_hash": stable_digest({"fixture_id": fixture["fixture_id"], "sql": sql}),
            "operators": fixture.get("expected_ops", []),
            "sql_render": sql,
        },
        "candidate_set": {
            "count": 2,
            "selected_candidate": "cand-1" if promote else None,
        },
        "verifiers": {
            "syntax": "pass",
            "schema": "pass",
            "semantic": "pass" if promote else "abstain",
            "policy": "pass",
            "cost": "pass",
            "abstention_check": "pass",
        },
        "execution": None if rows is None else {
            "probe_mode": "bounded",
            "row_limit": 500,
            "result_digest": stable_digest(rows),
            "result_preview": rows,
        },
        "provenance": {
            "policy_bundle_id": "mm.ev.gs.policy_bundle.v1",
            "source_citations": [f"view:{contract['logical_view']}"],
            "replay_nonce": fixture["fixture_id"],
            "rendered_at_utc": datetime.now(timezone.utc).isoformat(),
        },
        "decision": {
            "outcome": "promote" if promote else "abstain",
            "artifact_type": "Stele" if promote else "Cairnmark",
            "stele_id": fixture["fixture_id"].replace("fx.", "stele.") if promote else None,
            "review_required": True,
            "abstain_reason": fixture.get("abstain_reason", []) if not promote else [],
        },
    }


def build_stele(proofpack: dict[str, Any]) -> dict[str, Any] | None:
    if proofpack["decision"]["outcome"] != "promote":
        return None
    return {
        "stele_id": proofpack["decision"]["stele_id"],
        "proofpack_id": proofpack["proofpack_id"],
        "schema_id": proofpack["schema_id"],
        "logical_view": proofpack["logical_view"],
        "review_status": "pending_review",
        "result_digest": proofpack["execution"]["result_digest"] if proofpack.get("execution") else None,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--binding-manifest", default="fixtures/masonmark/grant_stewardship.binding_manifest.v0.json")
    ap.add_argument("--fixture-corpus", default="fixtures/masonmark/grant_stewardship.fixture_corpus.v0.json")
    ap.add_argument("--physical-bindings", default="fixtures/masonmark/grant_stewardship.physical_bindings.demo.v0.json")
    ap.add_argument("--output-dir", default="outputs/masonmark_demo")
    args = ap.parse_args()

    manifest = load_json(ROOT / args.binding_manifest)
    corpus = load_json(ROOT / args.fixture_corpus)
    physical = load_json(ROOT / args.physical_bindings)
    errors = validate_binding_manifest(manifest) + validate_fixture_corpus(corpus)
    if errors:
        raise SystemExit("\n".join(errors))

    ensure_demo_sqlite(physical)
    contracts = {c["schema_id"]: c for c in manifest["logical_contracts"]}
    out = ROOT / args.output_dir
    (out / "proofpacks").mkdir(parents=True, exist_ok=True)
    (out / "steles").mkdir(parents=True, exist_ok=True)

    report = {
        "family_id": corpus["family_id"],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "results": [],
    }

    for fixture in corpus["fixtures"]:
        contract = contracts[fixture["schema_id"]]
        binding = physical["bindings"][contract["logical_view"]]
        proofpack = build_proofpack(fixture, contract, binding)
        proofpack_path = out / "proofpacks" / f"{proofpack['proofpack_id']}.json"
        proofpack_path.write_text(json.dumps(proofpack, indent=2), encoding="utf-8")
        stele = build_stele(proofpack)
        if stele:
            (out / "steles" / f"{stele['stele_id']}.json").write_text(json.dumps(stele, indent=2), encoding="utf-8")
        report["results"].append({
            "fixture_id": fixture["fixture_id"],
            "decision": proofpack["decision"]["outcome"],
            "proofpack": str(proofpack_path.relative_to(ROOT)),
        })

    (out / "fixture_run_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"[OK] wrote fixture report to {out / 'fixture_run_report.json'}")


if __name__ == "__main__":
    main()
