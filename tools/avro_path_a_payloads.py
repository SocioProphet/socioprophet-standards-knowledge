#!/usr/bin/env python3
from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Tuple

from fastavro import schemaless_writer
from fastavro.schema import parse_schema

ROOT = Path(__file__).resolve().parents[1]
AVPR = ROOT / "schemas" / "avro" / "knowledge.store.v0" / "knowledge.store.v0.avpr"

def _load_protocol() -> dict:
    return json.loads(AVPR.read_text(encoding="utf-8"))

def _named_schemas(protocol: dict) -> dict:
    """Parse protocol types into a registry that resolves BOTH short and fully-qualified names.

    fastavro qualifies field types using the enclosing record namespace.
    Our wrapper request records live in the protocol namespace, so types must resolve
    as e.g. socioprophet.knowledge.v0.Note as well as Note.
    """
    named = {}
    ns = protocol.get("namespace", "") or ""
    for typ in protocol.get("types", []):
        # Ensure named types inherit the protocol namespace unless they already specify one.
        if isinstance(typ, dict):
            tt = dict(typ)
            if ns and "namespace" not in tt and "name" in tt and "." not in str(tt["name"]):
                tt["namespace"] = ns
            parse_schema(tt, named_schemas=named)
        else:
            parse_schema(typ, named_schemas=named)

    # Add alias keys so both "Note" and "socioprophet.knowledge.v0.Note" resolve.
    if ns:
        for k, v in list(named.items()):
            if isinstance(k, str) and "." not in k:
                named[f"{ns}.{k}"] = v

    return named

def _req_schema(protocol: dict, named: dict, msg_name: str) -> dict:
    # Build the implicit request record schema for a message
    msg = protocol["messages"][msg_name]
    fields = [{"name": p["name"], "type": p["type"]} for p in msg["request"]]
    req = {
        "type": "record",
        "name": msg_name,  # e.g. UpsertNote_a_REQ
        "namespace": protocol.get("namespace", ""),
        "fields": fields,
    }
    parsed = parse_schema(req, named_schemas=named)
    # Attach registry hints so fastavro can resolve named types when writing
    try:
        parsed['__named_schemas'] = named
        parsed['__fastavro_parsed'] = True
    except Exception:
        pass
    return parsed

def _type_schema(protocol: dict, named: dict, type_name: str) -> dict:
    # Named type already registered; parse a thin alias record if needed
    # For schemaless_writer we can pass the named schema dict directly via named lookup.
    # fastavro stores parsed schemas in named dict under full name keys; simplest is parse a record wrapper.
    # But for records, passing the named schema value works.
    # We'll locate it by suffix match if needed.
    for k, v in named.items():
        if k.endswith("." + type_name) or k == type_name:
            return v
    raise KeyError(f"Type not found: {type_name}")

def _encode(schema: dict, datum: dict, named: dict | None = None) -> bytes:
    """Encode Avro bytes deterministically with named-type resolution.

    fastavro.schemaless_writer will parse schemas; we force parse_schema(schema, named_schemas=...)
    to ensure fully-qualified named types like socioprophet.knowledge.v0.Note resolve.
    """
    buf = BytesIO()
    if isinstance(schema, dict):
        schema = parse_schema(schema, named_schemas=(named or {}))
    schemaless_writer(buf, schema, datum)
    return buf.getvalue()

def sample_objects() -> dict:
    # Deterministic sample values covering all message types
    actor = {"actor_id": "human:fixture", "actor_type": "human", "display_name": None}
    assertion = {"asserted_by": actor, "asserted_at": "2000-01-01T00:00:00Z", "confidence": 0.5, "method": None}

    note = {
        "note_id": "note_fixture",
        "title": "Fixture Note",
        "body": "Hello Avro",
        "format": "markdown",
        "tags": [],
        "aliases": [],
        "source": None,
        "created_at": "2000-01-01T00:00:00Z",
        "updated_at": None,
        "provenance": [],
    }

    claim = {
        "claim_id": "claim_fixture",
        "statement": "Fixture claim statement.",
        "claim_type": "fact",
        "evidence": [],
        "assertion": assertion,
        "validation": None,
        "created_at": "2000-01-01T00:00:00Z",
        "updated_at": None,
        "provenance": [],
    }

    edge = {
        "edge_id": "edge_fixture",
        "subject": {"node_type": "note", "ref": "note_fixture", "anchor": None},
        "predicate": "part_of",
        "object": {"node_type": "workspace", "ref": "ws_fixture", "anchor": None},
        "qualifiers": [],
        "assertion": assertion,
        "validation": None,
        "provenance": [],
    }

    query = {
        "query_id": None,
        "text": None,
        "tags_any": [],
        "limit": 50,
        "cursor": None,
    }

    ack = {"ok": True, "message": None, "error_code": None}
    noteset = {"notes": [note], "next_cursor": None}
    claimset = {"claims": [claim], "next_cursor": None}
    edgeset = {"edges": [edge], "next_cursor": None}

    return {
        "note": note,
        "claim": claim,
        "edge": edge,
        "query": query,
        "ack": ack,
        "noteset": noteset,
        "claimset": claimset,
        "edgeset": edgeset,
    }

def payload_for_method(service: str, method: str) -> bytes:
    """
    method is the TriTRPC method field string (e.g. UpsertNote_a.REQ or QueryNotes_a.RESP)
    We map it to:
      - request: Avro implicit request record (message) encoding
      - response: Avro encoding of the response type
    """
    proto = _load_protocol()
    named = _named_schemas(proto)
    samples = sample_objects()

    # method naming conventions:
    # requests are "<Message>_a.REQ" and the avpr message key is "<Message>_a_REQ"
    # responses are "<Message>_a.RESP" and response type is declared in avpr messages map
    if method.endswith("_a.REQ"):
        msg_key = method.replace("_a.REQ", "_a_REQ")
        schema = _req_schema(proto, named, msg_key)
        # Determine which param field exists and fill it deterministically
        req_fields = [f["name"] for f in schema["fields"]]
        datum = {}
        for f in req_fields:
            if f == "note": datum[f] = samples["note"]
            elif f == "claim": datum[f] = samples["claim"]
            elif f == "edge": datum[f] = samples["edge"]
            elif f == "query": datum[f] = samples["query"]
            else:
                raise KeyError(f"Unknown request param: {f}")
        return _encode(schema, datum, named)

    if method.endswith("_a.RESP"):
        msg_key = method.replace("_a.RESP", "_a_REQ")
        resp_type = proto["messages"][msg_key]["response"]
        schema = _type_schema(proto, named, resp_type)
        if resp_type == "Ack": datum = samples["ack"]
        elif resp_type == "NoteSet": datum = samples["noteset"]
        elif resp_type == "ClaimSet": datum = samples["claimset"]
        elif resp_type == "EdgeSet": datum = samples["edgeset"]
        else:
            raise KeyError(f"Unknown response type: {resp_type}")
        return _encode(schema, datum, named)

    raise ValueError(f"Unexpected method suffix: {method}")
