#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import List, Tuple

import yaml
from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_encrypt

ROOT = Path(__file__).resolve().parents[1]
REG  = ROOT / "docs/standards/031-schema-context-id-registry.md"
RPC  = ROOT / "rpc/knowledge.store.v0.yaml"
FIX  = ROOT / "fixtures" / "knowledge_vectors_hex_pathA.txt"
NON  = ROOT / "fixtures" / "knowledge_vectors_hex_pathA.txt.nonces"

KEY = bytes(32)  # 0x00 * 32
AUX_BYTES = b"AUX|KC|v0"  # deterministic AUX bytes for AUX-present fixtures (REQ only)

MAGIC_B2 = bytes.fromhex("f32a")

def tritpack243_pack(trits: List[int]) -> bytes:
    out = bytearray(); i = 0
    while i + 5 <= len(trits):
        v = 0
        for t in trits[i:i+5]:
            if t not in (0,1,2): raise ValueError("invalid trit")
            v = v*3 + t
        out.append(v); i += 5
    k = len(trits) - i
    if k > 0:
        out.append(243 + (k-1))
        v = 0
        for t in trits[i:]:
            v = v*3 + t
        out.append(v)
    return bytes(out)

def tleb3_len_encode(n: int) -> bytes:
    digits = [0] if n == 0 else []
    while n > 0:
        digits.append(n % 9); n //= 9
    trits: List[int] = []
    for i, d in enumerate(digits):
        C = 2 if i < len(digits)-1 else 0
        P1, P0 = divmod(d, 3)
        trits += [C, P1, P0]
    return tritpack243_pack(trits)

def lp(b: bytes) -> bytes:
    return tleb3_len_encode(len(b)) + b

def tritpack_ver() -> bytes:
    return tritpack243_pack([1])

def tritpack_mode() -> bytes:
    return tritpack243_pack([0])

def tritpack_flags(aead: bool, compress: bool) -> bytes:
    return tritpack243_pack([2 if aead else 0, 2 if compress else 0, 0])

def parse_labels(md: str) -> Tuple[str, str]:
    schema_label = None
    context_label = None
    mode = None
    for ln in md.splitlines():
        s = ln.strip()
        if s.startswith("##") and "Avro Path-A payload schema label" in s:
            mode = "schema"; continue
        if s.startswith("##") and "JSON-LD context label" in s:
            mode = "context"; continue
        if mode in ("schema","context") and "Label:" in s and "`" in s:
            parts = s.split("`")
            if len(parts) >= 3:
                val = parts[1].strip()
                if mode == "schema" and not schema_label:
                    schema_label = val
                if mode == "context" and not context_label:
                    context_label = val
        if schema_label and context_label:
            break
    if not schema_label or not context_label:
        raise SystemExit("Could not parse labels from docs/standards/031-schema-context-id-registry.md")
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
    # libsodium: ciphertext = msg || tag; msg is empty => output is tag (16B)
    return crypto_aead_xchacha20poly1305_ietf_encrypt(b"", aad, nonce, KEY)[-16:]

def emit(lines: List[str], nonces: List[str], name: str, nonce: bytes, aad: bytes):
    tag = aead_tag(nonce, aad)
    frame = aad + lp(tag)
    lines.append(f"{name} {frame.hex()}")
    nonces.append(f"{name} {nonce.hex()}")

def main():
    schema_label, context_label = parse_labels(REG.read_text(encoding="utf-8"))
    schema_id  = hashlib.sha3_256(schema_label.encode("utf-8")).digest()
    context_id = hashlib.sha3_256(context_label.encode("utf-8")).digest()

    cfg = yaml.safe_load(RPC.read_text(encoding="utf-8"))
    wire = cfg.get("tritrpc_wire", {}) or {}
    service = wire.get("service", "knowledge.store.v0")
    req_sfx = wire.get("request_method_suffix", "_a.REQ")
    rsp_sfx = wire.get("response_method_suffix", "_a.RESP")

    method_names = [m.get("name") for m in (cfg.get("methods") or []) if isinstance(m, dict) and m.get("name")]
    if not method_names:
        method_names = ["UpsertNote","QueryNotes","UpsertClaim","QueryClaims","UpsertEdge","QueryEdges"]

    FIX.parent.mkdir(parents=True, exist_ok=True)
    lines  = ["# Knowledge Context TriTRPC Path-A fixtures (AEAD on, key=00*32, AUX optional)"]
    nonces = []
    i = 1

    for mn in method_names:
        for sfx in (req_sfx, rsp_sfx):
            method = f"{mn}{sfx}"
            full = f"{service}.{method}"
            payload = ("KC|" + full).encode("utf-8")  # synthetic payload bytes (envelope compliance focus)
            base = build_prefix_fields(schema_id, context_id, service, method, payload)
            nonce = nonce_for(i)

            emit(lines, nonces, full, nonce, base)

            # AUX-present fixture (REQ only)
            if method.endswith(req_sfx):
                base_aux = base + lp(AUX_BYTES)
                emit(lines, nonces, f"{full}.AUX", nonce, base_aux)

            i += 1

    FIX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    NON.write_text("\n".join(nonces) + "\n", encoding="utf-8")
    print(f"[OK] Wrote fixtures: {FIX}")
    print(f"[OK] Wrote nonces:   {NON}")

if __name__ == "__main__":
    main()
