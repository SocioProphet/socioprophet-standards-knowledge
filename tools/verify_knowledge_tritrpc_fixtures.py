#!/usr/bin/env python3
from __future__ import annotations
import re, hashlib
from pathlib import Path
from typing import Tuple
import yaml
from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_encrypt

ROOT = Path(__file__).resolve().parents[1]
REG  = ROOT / "docs/standards/031-schema-context-id-registry.md"
RPC  = ROOT / "rpc/knowledge.store.v0.yaml"
FIX  = ROOT / "fixtures" / "knowledge_vectors_hex_pathA.txt"
NON  = ROOT / "fixtures" / "knowledge_vectors_hex_pathA.txt.nonces"

KEY = bytes(32)

def unpack_byte(b: int):
    if b <= 242:
        val = b
        out = [0,0,0,0,0]
        for j in range(4,-1,-1):
            out[j] = val % 3; val //= 3
        return out
    elif 243 <= b <= 246:
        return None
    raise ValueError("invalid TritPack243 byte")

def tleb3_decode_len(buf: bytes, offset: int) -> Tuple[int, int]:
    i = offset; trits = []
    while True:
        if i >= len(buf): raise ValueError("EOF in TLEB3")
        b = buf[i]; i += 1
        if b <= 242:
            trits.extend(unpack_byte(b))
        elif 243 <= b <= 246:
            k = (b - 243) + 1
            if i >= len(buf): raise ValueError("EOF tail")
            val = buf[i]; i += 1
            group = [0]*k
            for j in range(k-1,-1,-1):
                group[j] = val % 3; val //= 3
            trits.extend(group)

        if len(trits) >= 3:
            val = 0; used_trits = 0
            for j in range(0, len(trits)//3):
                C,P1,P0 = trits[3*j:3*j+3]
                digit = P1*3 + P0
                val += digit * (9**j)
                if C == 0:
                    used_trits = (j+1)*3
                    break
            if used_trits:
                out = bytearray(); x=0
                while x+5 <= used_trits:
                    v=0
                    for t in trits[x:x+5]: v=v*3+t
                    out.append(v); x+=5
                k = used_trits-x
                if k>0:
                    out.append(243+(k-1))
                    v=0
                    for t in trits[x:]: v=v*3+t
                    out.append(v)
                return val, offset + len(out)

def get_fields_and_laststart(frame: bytes):
    off = 0; fields = []; last_start = 0
    while off < len(frame):
        n, val_off = tleb3_decode_len(frame, off)
        last_start = off
        fields.append(frame[val_off:val_off+n])
        off = val_off + n
    return fields, last_start

def parse_labels(md: str):
    m1 = re.search(r"## Avro Path-A payload schema label\s*- Label: `([^`]+)`", md, re.S)
    m2 = re.search(r"## JSON-LD context label\s*- Label: `([^`]+)`", md, re.S)
    if not (m1 and m2): raise SystemExit("Could not parse labels from 031-schema-context-id-registry.md")
    return m1.group(1), m2.group(1)

def main():
    schema_label, context_label = parse_labels(REG.read_text(encoding="utf-8"))
    schema_id  = hashlib.sha3_256(schema_label.encode("utf-8")).digest()
    context_id = hashlib.sha3_256(context_label.encode("utf-8")).digest()

    if not FIX.exists() or not NON.exists():
        raise SystemExit("Missing fixtures. Run tools/generate_knowledge_tritrpc_fixtures.py first.")

    nonces = {}
    for ln in NON.read_text().splitlines():
        ln = ln.strip()
        if not ln: continue
        name, hx = ln.split(" ", 1)
        nonces[name] = bytes.fromhex(hx.strip())

    cfg = yaml.safe_load(RPC.read_text(encoding="utf-8"))
    wire = cfg.get("tritrpc_wire", {}) or {}
    service_expected = wire.get("service", "knowledge.store.v0")

    for ln in FIX.read_text().splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        name, hx = ln.split(" ", 1)
        frame = bytes.fromhex(hx.strip())

        if name not in nonces:
            raise SystemExit(f"[FAIL] Missing nonce for {name}")

        fields, last_start = get_fields_and_laststart(frame)
        tag = fields[-1]
        aad = frame[:last_start]
        calc = crypto_aead_xchacha20poly1305_ietf_encrypt(b"", aad, nonces[name], KEY)[-16:]
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
        if f"{svc}.{mth}" != name:
            raise SystemExit(f"[FAIL] Name mismatch for {name}: decoded {svc}.{mth}")

    print("[OK] Knowledge Context TriTRPC fixtures verified (AEAD + IDs + SERVICE/METHOD).")

if __name__ == "__main__":
    main()
