#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str | Path) -> Any:
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def stable_digest(obj: Any) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def ensure_demo_sqlite(physical_bindings: dict[str, Any]) -> None:
    demo_targets = [b for b in physical_bindings.get('bindings', {}).values() if b.get('engine') == 'sqlite']
    if not demo_targets:
        return
    db_path = ROOT / 'data' / 'grant_stewardship_demo.sqlite'
    if db_path.exists():
        return
    sql_path = ROOT / 'data' / 'grant_stewardship_demo.sql'
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(sql_path.read_text(encoding='utf-8'))
        conn.commit()
    finally:
        conn.close()


def _safe_table_name(table: str) -> str:
    import re
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', table):
        raise ValueError(f"Invalid table name: {table!r}")
    return table


def sqlite_columns(binding: dict[str, Any]) -> list[str]:
    db = ROOT / binding['database'] if not Path(binding['database']).is_absolute() else Path(binding['database'])
    table = _safe_table_name(binding['table'])
    conn = sqlite3.connect(db)
    try:
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table})")
        return [r[1] for r in cur.fetchall()]
    finally:
        conn.close()


def execute_sql(binding: dict[str, Any], sql: str) -> list[dict[str, Any]]:
    db = ROOT / binding['database'] if not Path(binding['database']).is_absolute() else Path(binding['database'])
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        cur.execute(sql)
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


def validate_binding_manifest(doc: dict[str, Any]) -> list[str]:
    errors = []
    for key in ['pack_version', 'family_id', 'logical_contracts', 'id_blocks']:
        if key not in doc:
            errors.append(f'missing binding_manifest.{key}')
    for contract in doc.get('logical_contracts', []):
        for key in ['schema_id', 'logical_view', 'approved_columns', 'allowlisted_ops', 'denylisted_ops']:
            if key not in contract:
                errors.append(f"missing logical_contract.{contract.get('schema_id','<unknown>')}.{key}")
    return errors


def validate_fixture_corpus(doc: dict[str, Any]) -> list[str]:
    errors = []
    for key in ['pack_version', 'family_id', 'fixtures', 'acceptance_gate']:
        if key not in doc:
            errors.append(f'missing fixture_corpus.{key}')
    for fixture in doc.get('fixtures', []):
        for key in ['fixture_id', 'schema_id', 'class', 'utterance', 'expected_decision']:
            if key not in fixture:
                errors.append(f"missing fixture.{fixture.get('fixture_id','<unknown>')}.{key}")
    return errors
