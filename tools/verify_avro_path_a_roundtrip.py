#!/usr/bin/env python3
from __future__ import annotations

import os
from io import BytesIO
from pathlib import Path

import yaml
from fastavro import schemaless_reader
from fastavro.schema import parse_schema

from avro_path_a_payloads import (
    ROOT,
    _load_protocol,
    _named_schemas,
    _raw_type_map,
    _req_schema,
    _type_schema,
    sample_for_schema,
    payload_for_method,
)

DEFAULT_RPC = ROOT / "rpc" / "knowledge.store.v0.yaml"


def _repo_path(value: str | os.PathLike[str]) -> Path:
    p = Path(value)
    return p if p.is_absolute() else ROOT / p


def rpc_path() -> Path:
    return _repo_path(os.environ.get("KC_RPC_CONFIG", str(DEFAULT_RPC)))


def ensure_parsed(schema: dict, named: dict) -> dict:
    if isinstance(schema, dict) and not schema.get("__fastavro_parsed", False):
        try:
            schema = parse_schema(schema, named_schemas=named)
        except Exception:
            pass
    return schema


def _wire_suffixes() -> tuple[str, str, str]:
    cfg = yaml.safe_load(rpc_path().read_text(encoding="utf-8"))
    wire = cfg.get("tritrpc_wire", {}) or {}
    return (
        wire.get("service", "knowledge.store.v0"),
        wire.get("request_method_suffix", "_a.REQ"),
        wire.get("response_method_suffix", "_a.RESP"),
    )


def decode_req(method: str):
    proto = _load_protocol()
    named = _named_schemas(proto)
    msg_key = method.replace("_a.REQ", "_a_REQ")
    schema = ensure_parsed(_req_schema(proto, named, msg_key), named)
    service, _, _ = _wire_suffixes()
    payload = payload_for_method(service, method)
    return schemaless_reader(BytesIO(payload), schema)


def decode_resp(method: str):
    proto = _load_protocol()
    named = _named_schemas(proto)
    msg_key = method.replace("_a.RESP", "_a_REQ")
    resp_type = proto["messages"][msg_key]["response"]
    schema = ensure_parsed(_type_schema(proto, named, resp_type), named)
    service, _, _ = _wire_suffixes()
    payload = payload_for_method(service, method)
    return resp_type, schemaless_reader(BytesIO(payload), schema)


def main():
    proto = _load_protocol()
    type_map = _raw_type_map(proto)
    service, req_sfx, rsp_sfx = _wire_suffixes()

    for msg_key, msg in (proto.get("messages") or {}).items():
        if not msg_key.endswith("_a_REQ"):
            continue

        method_base = msg_key[:-len("_a_REQ")]
        req_method = f"{method_base}{req_sfx}"
        resp_method = f"{method_base}{rsp_sfx}"

        req_obj = decode_req(req_method)
        expected_req = {
            param["name"]: sample_for_schema(param["type"], type_map, param["name"])
            for param in msg["request"]
        }
        if req_obj != expected_req:
            raise SystemExit(f"[FAIL] {req_method}: decoded request mismatch")

        resp_type, resp_obj = decode_resp(resp_method)
        if resp_type != msg["response"]:
            raise SystemExit(f"[FAIL] {resp_method}: response type mismatch got {resp_type} expected {msg['response']}")
        expected_resp = sample_for_schema(msg["response"], type_map, str(msg["response"]).lower())
        if resp_obj != expected_resp:
            raise SystemExit(f"[FAIL] {resp_method}: decoded response mismatch")

    print(f"[OK] Avro Path-A round-trip verified for {service} (REQ + RESP).")


if __name__ == "__main__":
    main()
