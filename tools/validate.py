#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
import unicodedata
from pathlib import Path

import jsonschema
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "fixtures"


def nfc(x):
    if isinstance(x, str):
        return unicodedata.normalize("NFC", x)
    if isinstance(x, list):
        return [nfc(i) for i in x]
    if isinstance(x, dict):
        return {nfc(k): nfc(v) for k, v in x.items()}
    return x


def canonical_bytes(obj) -> bytes:
    return json.dumps(nfc(obj), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def iter_refs(obj):
    if isinstance(obj, dict):
        if isinstance(obj.get("$ref"), str):
            yield obj["$ref"]
        for value in obj.values():
            yield from iter_refs(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_refs(item)


def has_pointer(doc, ref: str) -> bool:
    if ref == "#":
        return True
    if not ref.startswith("#/"):
        return True
    cur = doc
    for token in ref[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, dict) and token in cur:
            cur = cur[token]
        else:
            return False
    return True


def main() -> int:
    ok = True
    for schema_path in sorted(SCHEMAS.rglob("*.jsonschema.json")):
        try:
            schema = load(schema_path)
            Draft202012Validator.check_schema(schema)
            for ref in iter_refs(schema):
                if not has_pointer(schema, ref):
                    raise ValueError(f"unresolved internal ref {ref}")
            print(f"[OK] schema {schema_path.relative_to(ROOT)}")
        except Exception as exc:
            ok = False
            print(f"[FAIL] schema {schema_path.relative_to(ROOT)}: {exc}")

    env_schema = load(SCHEMAS / "envelope" / "frame.v0.jsonschema.json")
    for fixture_path in sorted(FIXTURES.glob("*.frame.json")):
        try:
            frame = load(fixture_path)
            jsonschema.validate(frame, env_schema)
            payload_schema = load(SCHEMAS / frame["payload_schema"])
            jsonschema.validate(frame["payload"], payload_schema)
            frame_wo = dict(frame)
            frame_wo.pop("signatures", None)
            digest = hashlib.sha256(canonical_bytes(frame_wo)).hexdigest()
            print(f"[OK] fixture {fixture_path.name} frame_hash={digest}")
        except Exception as exc:
            ok = False
            print(f"[FAIL] fixture {fixture_path.name}: {exc}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
