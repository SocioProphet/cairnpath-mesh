#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
from pathlib import Path
import sys

try:
    import jsonschema
except Exception:
    print("ERR: jsonschema not installed. Install: python3 -m pip install jsonschema", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "fixtures"
SCHEMA_PREFIX = "https://socioprophet.org/schemas/"

def canonical_bytes(obj) -> bytes:
    s = json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return s.encode("utf-8")

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def payload_schema_path(payload_schema: str) -> Path:
    if payload_schema.startswith(SCHEMA_PREFIX):
        payload_schema = payload_schema.removeprefix(SCHEMA_PREFIX)
    return SCHEMAS / payload_schema

def load_schema_store():
    store = {}
    for path in SCHEMAS.rglob("*.jsonschema.json"):
        schema = load(path)
        rel = path.relative_to(SCHEMAS).as_posix()
        store[rel] = schema
        store[path.name] = schema
        if "$id" in schema:
            store[schema["$id"]] = schema
    return store

def validate_schema(instance, schema, store):
    resolver = jsonschema.RefResolver.from_schema(schema, store=store)
    validator = jsonschema.Draft202012Validator(schema, resolver=resolver)
    validator.validate(instance)

def main() -> int:
    env_schema = load(SCHEMAS / "envelope" / "frame.v0.jsonschema.json")
    store = load_schema_store()
    ok = True
    for f in sorted(FIXTURES.rglob("*.frame.json")):
        try:
            frame = load(f)
            validate_schema(frame, env_schema, store)
            ps_path = payload_schema_path(frame["payload_schema"])
            ps = load(ps_path)
            validate_schema(frame["payload"], ps, store)
            frame_wo = dict(frame)
            frame_wo.pop("signatures", None)
            h = sha256_hex(canonical_bytes(frame_wo))
            print(f"[OK] {f.relative_to(ROOT)} frame_hash={h}")
        except Exception as e:
            ok = False
            print(f"[FAIL] {f.relative_to(ROOT)}: {e}", file=sys.stderr)
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
