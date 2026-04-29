# Semantic-core SHACL fixtures

This directory contains the fixture graphs used by the repository SHACL validation gate.

## Files

- `semantic_core_conforms.ttl` — a positive fixture that should pass the current `policy/shapes/master.shacl.ttl` entry surface.
- `semantic_core_violates.ttl` — a negative fixture that should fail the same entry surface.

## What the fixtures prove

The `verify-shacl` Make target exercises the repaired repository validator at `policy/tools/validate_all.py` against both fixtures.

The conforming fixture proves that the widened semantic-core pack accepts a representative valid graph covering:

- Prophet mutating command carrier signatures
- Atomic binding ports, device nodes, and socket endpoints
- Human sensitive-record consent
- SocioProphet experiment and metric constraints

The violating fixture proves that the same pack rejects representative invalid graph fragments covering:

- unsigned carrier claims
- invalid binding ports, device paths, and socket paths
- sensitive records without consent
- invalid task metrics
- invalid numeric metric values

## How to run

```bash
make verify-shacl
```

The target should pass only when the conforming fixture validates successfully and the violating fixture fails validation.

## Scope

These fixtures are smoke fixtures for semantic-core CI. They do not exhaustively cover every SHACL rule. Add focused fixtures as the semantic-core pack gains new shape families.
