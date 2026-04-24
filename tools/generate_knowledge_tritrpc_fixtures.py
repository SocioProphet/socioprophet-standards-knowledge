#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import List, Tuple

import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent))

import yaml
from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_encrypt

from avro_path_a_payloads import ROOT, payload_for_method

DEFAULT_RPC = ROOT / "rpc" / "knowledge.store.v0.yaml"
DEFAULT_FIX = ROOT / "fixtures" / "knowledge_vectors_hex_pathA.txt"
DEFAULT_NON = ROOT / "fixtures" / "knowledge_vectors_hex_pathA.txt.nonces"

KEY = bytes(32)  # 0x00 * 32
MAGIC_B2 = bytes.fromhex("f32a")


def _repo_path(value: str | os.PathLike[str]) -> Path:
    p = Path(value)
    return p if p.is_absolute() else ROOT / p


def rpc_path() -> Path:
    return _repo_path(os.environ.get("KC_RPC_CONFIG", str(DEFAULT_RPC)))


def fixture_path() -> Path:
    return _repo_path(os.environ.get("KC_FIXTURE_OUT", str(DEFAULT_FIX)))


def nonce_path() -> Path:
    return _repo_path(os.environ.get("KC_NONCE_OUT", str(DEFAULT_NON)))


def tritpack243_pack(trits: List[int]) -> bytes:
    out = bytearray()
    i = 0
    while i + 5 <= len(trits):
        v = 0
        for t in trits[i:i + 5]:
            if t not in (0, 1, 2):
                raise ValueError("invalid trit")
            v = v * 3 + t
        out.append(v)
        i += 5
    k = len(trits) - i
    if k > 0:
        out.append(243 + (k - 1))
        v = 0
        for t in trits[i:]:
            v = v * 3 + t
        out.append(v)
    return bytes(out)


def tleb3_len_encode(n: int) -> bytes:
    digits = [0] if n == 0 else []
    while n > 0:
        digits.append(n % 9)
        n //= 9
    trits: List[int] = []
    for i, d in enumerate(digits):
        c = 2 if i < len(digits) - 1 else 0
        p1, p0 = divmod(d, 3)
        trits += [c, p1, p0]
    return tritpack243_pack(trits)


def lp(b: bytes) -> bytes:
    return tleb3_len_encode(len(b)) + b


def tritpack_ver() -> bytes:
    return tritpack243_pack([1])


def tritpack_mode() -> bytes:
    return tritpack243_pack([0])


def tritpack_flags(aead: bool, compress: bool) -> bytes:
    return tritpack243_pack([2 if aead else 0, 2 if compress else 0, 0])


def _labels_from_rpc(cfg: dict) -> Tuple[str, str]:
    wire = cfg.get("tritrpc_wire", {}) or {}
    schema_label = wire.get("schema_label")
    context_label = wire.get("context_label")
    if not schema_label or not context_label:
        raise SystemExit("RPC config must define tritrpc_wire.schema_label and tritrpc_wire.context_label")
    return schema_label, context_label


def nonce_for(i: int) -> bytes:
    return (b"\x05" * 20) + i.to_bytes(4, "big")  # 24B


def build_prefix_fields(schema_id: bytes, context_id: bytes, service: str, method: str, payload: bytes) -> bytes:
    fields = [
        MAGIC_B2,
        tritpack_ver(),
        tritpack_mode(),
        tritpack_flags(aead=True, compress=False),
        schema_id,
        context_id,
        service.encode("utf-8"),
        method.encode("utf-8"),
        payload,
    ]
    out = bytearray()
    for f in fields:
        out += lp(f)
    return bytes(out)


def aead_tag(nonce: bytes, aad: bytes) -> bytes:
    return crypto_aead_xchacha20poly1305_ietf_encrypt(b"", aad, nonce, KEY)[-16:]


def emit(lines: List[str], nonces: List[str], name: str, nonce: bytes, aad: bytes):
    tag = aead_tag(nonce, aad)
    frame = aad + lp(tag)
    lines.append(f"{name} {frame.hex()}")
    nonces.append(f"{name} {nonce.hex()}")


def main():
    cfg = yaml.safe_load(rpc_path().read_text(encoding="utf-8"))
    schema_label, context_label = _labels_from_rpc(cfg)
    schema_id = hashlib.sha3_256(schema_label.encode("utf-8")).digest()
    context_id = hashlib.sha3_256(context_label.encode("utf-8")).digest()

    wire = cfg.get("tritrpc_wire", {}) or {}
    service = wire.get("service", "knowledge.store.v0")
    req_sfx = wire.get("request_method_suffix", "_a.REQ")
    rsp_sfx = wire.get("response_method_suffix", "_a.RESP")

    method_names = [m.get("name") for m in (cfg.get("methods") or []) if isinstance(m, dict) and m.get("name")]
    if not method_names:
        raise SystemExit(f"No methods found in RPC config: {rpc_path()}")

    fix = fixture_path()
    non = nonce_path()
    fix.parent.mkdir(parents=True, exist_ok=True)
    non.parent.mkdir(parents=True, exist_ok=True)

    aux_bytes = os.environ.get("KC_AUX_BYTES", f"AUX|KC|{service}").encode("utf-8")
    lines = [f"# Knowledge Context TriTRPC Path-A fixtures for {service} (AEAD on, key=00*32, AUX optional)"]
    nonces: List[str] = []
    i = 1

    for mn in method_names:
        for sfx in (req_sfx, rsp_sfx):
            method = f"{mn}{sfx}"
            full = f"{service}.{method}"
            payload = payload_for_method(service, method)
            base = build_prefix_fields(schema_id, context_id, service, method, payload)
            nonce = nonce_for(i)

            emit(lines, nonces, full, nonce, base)

            if method.endswith(req_sfx):
                emit(lines, nonces, f"{full}.AUX", nonce, base + lp(aux_bytes))

            i += 1

    fix.write_text("\n".join(lines) + "\n", encoding="utf-8")
    non.write_text("\n".join(nonces) + "\n", encoding="utf-8")
    print(f"[OK] Wrote fixtures: {fix}")
    print(f"[OK] Wrote nonces:   {non}")


if __name__ == "__main__":
    main()
