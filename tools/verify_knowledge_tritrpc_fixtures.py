#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Tuple

import yaml
from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_encrypt

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RPC = ROOT / "rpc" / "knowledge.store.v0.yaml"
DEFAULT_FIX = ROOT / "fixtures" / "knowledge_vectors_hex_pathA.txt"
DEFAULT_NON = ROOT / "fixtures" / "knowledge_vectors_hex_pathA.txt.nonces"

KEY = bytes(32)


def _repo_path(value: str | os.PathLike[str]) -> Path:
    p = Path(value)
    return p if p.is_absolute() else ROOT / p


def rpc_path() -> Path:
    return _repo_path(os.environ.get("KC_RPC_CONFIG", str(DEFAULT_RPC)))


def fixture_path() -> Path:
    return _repo_path(os.environ.get("KC_FIXTURE_OVERRIDE", os.environ.get("KC_FIXTURE_OUT", str(DEFAULT_FIX))))


def nonce_path() -> Path:
    return _repo_path(os.environ.get("KC_NONCE_OVERRIDE", os.environ.get("KC_NONCE_OUT", str(DEFAULT_NON))))


def unpack_byte(b: int):
    if b <= 242:
        val = b
        out = [0, 0, 0, 0, 0]
        for j in range(4, -1, -1):
            out[j] = val % 3
            val //= 3
        return out
    if 243 <= b <= 246:
        return None
    raise ValueError("invalid TritPack243 byte")


def tleb3_decode_len(buf: bytes, offset: int) -> Tuple[int, int]:
    i = offset
    trits = []
    while True:
        if i >= len(buf):
            raise ValueError("EOF in TLEB3")
        b = buf[i]
        i += 1
        if b <= 242:
            trits.extend(unpack_byte(b))
        elif 243 <= b <= 246:
            k = (b - 243) + 1
            if i >= len(buf):
                raise ValueError("EOF tail")
            val = buf[i]
            i += 1
            group = [0] * k
            for j in range(k - 1, -1, -1):
                group[j] = val % 3
                val //= 3
            trits.extend(group)

        if len(trits) >= 3:
            val = 0
            used_trits = 0
            for j in range(0, len(trits) // 3):
                c, p1, p0 = trits[3 * j: 3 * j + 3]
                digit = p1 * 3 + p0
                val += digit * (9 ** j)
                if c == 0:
                    used_trits = (j + 1) * 3
                    break
            if used_trits:
                out = bytearray()
                x = 0
                while x + 5 <= used_trits:
                    v = 0
                    for t in trits[x:x + 5]:
                        v = v * 3 + t
                    out.append(v)
                    x += 5
                k = used_trits - x
                if k > 0:
                    out.append(243 + (k - 1))
                    v = 0
                    for t in trits[x:]:
                        v = v * 3 + t
                    out.append(v)
                return val, offset + len(out)


def get_fields_and_laststart(frame: bytes):
    off = 0
    fields = []
    last_start = 0
    while off < len(frame):
        n, val_off = tleb3_decode_len(frame, off)
        last_start = off
        fields.append(frame[val_off: val_off + n])
        off = val_off + n
    return fields, last_start


def _labels_from_rpc(cfg: dict) -> Tuple[str, str]:
    wire = cfg.get("tritrpc_wire", {}) or {}
    schema_label = wire.get("schema_label")
    context_label = wire.get("context_label")
    if not schema_label or not context_label:
        raise SystemExit("RPC config must define tritrpc_wire.schema_label and tritrpc_wire.context_label")
    return schema_label, context_label


def main():
    cfg = yaml.safe_load(rpc_path().read_text(encoding="utf-8"))
    schema_label, context_label = _labels_from_rpc(cfg)
    schema_id = hashlib.sha3_256(schema_label.encode("utf-8")).digest()
    context_id = hashlib.sha3_256(context_label.encode("utf-8")).digest()

    fix = fixture_path()
    non = nonce_path()
    if not fix.exists() or not non.exists():
        raise SystemExit("Missing fixtures. Run tools/generate_knowledge_tritrpc_fixtures.py first.")

    nonces = {}
    for ln in non.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        name, hx = ln.split(" ", 1)
        nonces[name] = bytes.fromhex(hx.strip())

    wire = cfg.get("tritrpc_wire", {}) or {}
    service_expected = wire.get("service", "knowledge.store.v0")

    for ln in fix.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        name, hx = ln.split(" ", 1)
        name_base = name[:-4] if name.endswith(".AUX") else name
        frame = bytes.fromhex(hx.strip())

        nonce = nonces.get(name) or nonces.get(name_base)
        if nonce is None:
            raise SystemExit(f"[FAIL] Missing nonce for {name}")

        fields, last_start = get_fields_and_laststart(frame)
        if len(fields) < 9:
            raise SystemExit(f"[FAIL] Too few fields for {name}: {len(fields)}")

        tag = fields[-1]
        if len(tag) != 16:
            raise SystemExit(f"[FAIL] Tag not 16 bytes for {name}: {len(tag)}")

        aad = frame[:last_start]
        calc = crypto_aead_xchacha20poly1305_ietf_encrypt(b"", aad, nonce, KEY)[-16:]
        if calc != tag:
            raise SystemExit(f"[FAIL] AEAD tag mismatch for {name}")

        if fields[4] != schema_id:
            raise SystemExit(f"[FAIL] SCHEMA_ID mismatch for {name}")
        if fields[5] != context_id:
            raise SystemExit(f"[FAIL] CONTEXT_ID mismatch for {name}")

        svc = fields[6].decode("utf-8")
        mth = fields[7].decode("utf-8")
        if svc != service_expected:
            raise SystemExit(f"[FAIL] SERVICE mismatch for {name}: got {svc}, expected {service_expected}")
        if f"{svc}.{mth}" != name_base:
            raise SystemExit(f"[FAIL] Name mismatch for {name}: decoded {svc}.{mth}")

    print(f"[OK] Knowledge Context TriTRPC fixtures verified for {service_expected} (AEAD + IDs + SERVICE/METHOD).")


if __name__ == "__main__":
    main()
