#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from io import BytesIO
from pathlib import Path
from typing import Any

from fastavro import schemaless_writer
from fastavro.schema import parse_schema

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AVPR = ROOT / "schemas" / "avro" / "knowledge.store.v0" / "knowledge.store.v0.avpr"
DEFAULT_RPC = ROOT / "rpc" / "knowledge.store.v0.yaml"


def _repo_path(value: str | os.PathLike[str]) -> Path:
    p = Path(value)
    return p if p.is_absolute() else ROOT / p


def avpr_path() -> Path:
    return _repo_path(os.environ.get("KC_AVRO_PROTOCOL", str(DEFAULT_AVPR)))


def _load_protocol(path: str | os.PathLike[str] | None = None) -> dict:
    return json.loads((avpr_path() if path is None else _repo_path(path)).read_text(encoding="utf-8"))


def _named_schemas(protocol: dict) -> dict:
    """Parse protocol types into a fastavro registry.

    The registry resolves both short names (Note) and fully-qualified names
    (socioprophet.knowledge.vN.Note), which keeps implicit request records
    stable across protocol versions.
    """
    named: dict[str, Any] = {}
    ns = protocol.get("namespace", "") or ""
    for typ in protocol.get("types", []):
        if isinstance(typ, dict):
            tt = dict(typ)
            if ns and "namespace" not in tt and "name" in tt and "." not in str(tt["name"]):
                tt["namespace"] = ns
            parse_schema(tt, named_schemas=named)
        else:
            parse_schema(typ, named_schemas=named)

    if ns:
        for key, value in list(named.items()):
            if isinstance(key, str) and "." not in key:
                named[f"{ns}.{key}"] = value

    return named


def _raw_type_map(protocol: dict) -> dict[str, Any]:
    ns = protocol.get("namespace", "") or ""
    out: dict[str, Any] = {}
    for typ in protocol.get("types", []):
        if not isinstance(typ, dict) or "name" not in typ:
            continue
        name = str(typ["name"])
        out[name] = typ
        if ns and "." not in name:
            out[f"{ns}.{name}"] = typ
    return out


def _req_schema(protocol: dict, named: dict, msg_name: str) -> dict:
    msg = protocol["messages"][msg_name]
    fields = [{"name": p["name"], "type": p["type"]} for p in msg["request"]]
    req = {
        "type": "record",
        "name": msg_name,
        "namespace": protocol.get("namespace", ""),
        "fields": fields,
    }
    parsed = parse_schema(req, named_schemas=named)
    try:
        parsed["__named_schemas"] = named
        parsed["__fastavro_parsed"] = True
    except Exception:
        pass
    return parsed


def _type_schema(protocol: dict, named: dict, type_name: str) -> dict:
    for key, value in named.items():
        if key == type_name or (isinstance(key, str) and key.endswith("." + type_name)):
            return value
    raise KeyError(f"Type not found: {type_name}")


def _encode(schema: dict, datum: dict, named: dict | None = None) -> bytes:
    buf = BytesIO()
    if isinstance(schema, dict):
        schema = parse_schema(schema, named_schemas=(named or {}))
    schemaless_writer(buf, schema, datum)
    return buf.getvalue()


def _sample_primitive(type_name: str, field_name: str) -> Any:
    if type_name == "null":
        return None
    if type_name == "boolean":
        return True
    if type_name in ("int", "long"):
        return 1
    if type_name in ("float", "double"):
        return 0.5
    if type_name == "bytes":
        return b""
    if type_name == "string":
        return f"{field_name or 'value'}_fixture"
    raise KeyError(type_name)


def _normalize_default(value: Any, schema_spec: Any) -> Any:
    if isinstance(schema_spec, str) and schema_spec == "bytes" and isinstance(value, str):
        return value.encode("utf-8")
    if isinstance(schema_spec, list):
        non_null = [x for x in schema_spec if x != "null"]
        if value is None:
            return None
        if len(non_null) == 1:
            return _normalize_default(value, non_null[0])
    return value


def sample_for_schema(schema_spec: Any, type_map: dict[str, Any], field_name: str = "value", depth: int = 0) -> Any:
    """Generate deterministic sample data for Avro schemas.

    This is intentionally conservative: fields with defaults use defaults,
    required arrays get one deterministic element, and optional unions default
    to null. The goal is fixture stability, not semantic richness.
    """
    if depth > 20:
        return None

    if isinstance(schema_spec, list):
        if "null" in schema_spec:
            return None
        return sample_for_schema(schema_spec[0], type_map, field_name, depth + 1)

    if isinstance(schema_spec, str):
        if schema_spec in {"null", "boolean", "int", "long", "float", "double", "bytes", "string"}:
            return _sample_primitive(schema_spec, field_name)
        target = type_map.get(schema_spec) or next((v for k, v in type_map.items() if k.endswith("." + schema_spec)), None)
        if target is None:
            raise KeyError(f"Unknown Avro type: {schema_spec}")
        return sample_for_schema(target, type_map, field_name, depth + 1)

    if isinstance(schema_spec, dict):
        typ = schema_spec.get("type")

        if isinstance(typ, list):
            return sample_for_schema(typ, type_map, field_name, depth + 1)

        if isinstance(typ, dict):
            return sample_for_schema(typ, type_map, field_name, depth + 1)

        if typ == "record":
            obj: dict[str, Any] = {}
            for field in schema_spec.get("fields", []):
                fname = field["name"]
                fschema = field["type"]
                if "default" in field:
                    obj[fname] = _normalize_default(field["default"], fschema)
                else:
                    obj[fname] = sample_for_schema(fschema, type_map, fname, depth + 1)
            return obj

        if typ == "enum":
            symbols = schema_spec.get("symbols") or []
            if not symbols:
                raise ValueError(f"Enum has no symbols: {schema_spec.get('name')}")
            return symbols[0]

        if typ == "array":
            if "default" in schema_spec:
                return schema_spec["default"]
            return [sample_for_schema(schema_spec["items"], type_map, field_name, depth + 1)]

        if typ == "map":
            return {}

        if isinstance(typ, str):
            return sample_for_schema(typ, type_map, field_name, depth + 1)

    raise TypeError(f"Unsupported Avro schema fragment: {schema_spec!r}")


def sample_objects() -> dict:
    proto = _load_protocol()
    type_map = _raw_type_map(proto)
    out: dict[str, Any] = {}
    for name, schema in type_map.items():
        short = name.rsplit(".", 1)[-1]
        if short not in out and isinstance(schema, dict) and schema.get("type") == "record":
            out[short.lower()] = sample_for_schema(schema, type_map, short.lower())
    return out


def payload_for_method(service: str, method: str) -> bytes:
    """Return deterministic Avro Path-A payload bytes for a TriTRPC method.

    `service` is accepted for API compatibility and fixture readability; the
    active protocol comes from KC_AVRO_PROTOCOL or the v0 default.
    """
    proto = _load_protocol()
    named = _named_schemas(proto)
    type_map = _raw_type_map(proto)

    if method.endswith("_a.REQ"):
        msg_key = method.replace("_a.REQ", "_a_REQ")
        msg = proto["messages"][msg_key]
        schema = _req_schema(proto, named, msg_key)
        datum = {
            param["name"]: sample_for_schema(param["type"], type_map, param["name"])
            for param in msg["request"]
        }
        return _encode(schema, datum, named)

    if method.endswith("_a.RESP"):
        msg_key = method.replace("_a.RESP", "_a_REQ")
        resp_type = proto["messages"][msg_key]["response"]
        schema = _type_schema(proto, named, resp_type)
        datum = sample_for_schema(resp_type, type_map, resp_type.lower())
        return _encode(schema, datum, named)

    raise ValueError(f"Unexpected method suffix: {method}")
