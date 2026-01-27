#!/usr/bin/env python3
from __future__ import annotations

from io import BytesIO

from fastavro import schemaless_reader
from fastavro.schema import parse_schema

from avro_path_a_payloads import (
    _load_protocol,
    _named_schemas,
    _req_schema,
    _type_schema,
    sample_objects,
    payload_for_method,
)

def ensure_parsed(schema: dict, named: dict) -> dict:
    # fastavro marks parsed schemas with __fastavro_parsed; if absent, try parsing with named registry.
    if isinstance(schema, dict) and not schema.get("__fastavro_parsed", False):
        try:
            schema = parse_schema(schema, named_schemas=named)
        except Exception:
            # If it's already a parsed/named object in this fastavro version, keep as-is.
            pass
    return schema

def decode_req(method: str):
    proto = _load_protocol()
    named = _named_schemas(proto)
    msg_key = method.replace("_a.REQ", "_a_REQ")
    schema = _req_schema(proto, named, msg_key)
    schema = ensure_parsed(schema, named)
    payload = payload_for_method("knowledge.store.v0", method)
    buf = BytesIO(payload)
    obj = schemaless_reader(buf, schema)
    return named, obj

def decode_resp(method: str):
    proto = _load_protocol()
    named = _named_schemas(proto)
    msg_key = method.replace("_a.RESP", "_a_REQ")
    resp_type = proto["messages"][msg_key]["response"]
    schema = _type_schema(proto, named, resp_type)
    schema = ensure_parsed(schema, named)
    payload = payload_for_method("knowledge.store.v0", method)
    buf = BytesIO(payload)
    obj = schemaless_reader(buf, schema)
    return resp_type, obj

def main():
    samples = sample_objects()

    req_checks = {
        "UpsertNote_a.REQ":  ("note", samples["note"]),
        "QueryNotes_a.REQ":  ("query", samples["query"]),
        "UpsertClaim_a.REQ": ("claim", samples["claim"]),
        "QueryClaims_a.REQ": ("query", samples["query"]),
        "UpsertEdge_a.REQ":  ("edge", samples["edge"]),
        "QueryEdges_a.REQ":  ("query", samples["query"]),
    }

    for method, (field, expected) in req_checks.items():
        _, obj = decode_req(method)
        if field not in obj:
            raise SystemExit(f"[FAIL] {method}: missing field {field} in decoded request: {obj}")
        if obj[field] != expected:
            raise SystemExit(f"[FAIL] {method}: decoded request mismatch for {field}")

    resp_checks = {
        "UpsertNote_a.RESP":  ("Ack", samples["ack"]),
        "QueryNotes_a.RESP":  ("NoteSet", samples["noteset"]),
        "UpsertClaim_a.RESP": ("Ack", samples["ack"]),
        "QueryClaims_a.RESP": ("ClaimSet", samples["claimset"]),
        "UpsertEdge_a.RESP":  ("Ack", samples["ack"]),
        "QueryEdges_a.RESP":  ("EdgeSet", samples["edgeset"]),
    }

    for method, (type_name, expected) in resp_checks.items():
        got_type, obj = decode_resp(method)
        if got_type != type_name:
            raise SystemExit(f"[FAIL] {method}: response type mismatch got {got_type} expected {type_name}")
        if obj != expected:
            raise SystemExit(f"[FAIL] {method}: decoded response mismatch")

    print("[OK] Avro Path-A round-trip verified for knowledge.store.v0 (REQ + RESP).")

if __name__ == "__main__":
    main()
