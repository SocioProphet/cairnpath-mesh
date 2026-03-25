#!/usr/bin/env python3
from __future__ import annotations
import json, hashlib, unicodedata
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

def nfc(x):
    if isinstance(x, str):
        return unicodedata.normalize("NFC", x)
    if isinstance(x, list):
        return [nfc(i) for i in x]
    if isinstance(x, dict):
        return {nfc(k): nfc(v) for k, v in x.items()}
    return x

def canonical_bytes(obj) -> bytes:
    obj = nfc(obj)
    s = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return s.encode("utf-8")

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def main() -> int:
    env_schema = load(SCHEMAS/"envelope"/"frame.v0.jsonschema.json")
    ok = True
    for f in sorted(FIXTURES.glob("*.frame.json")):
        try:
            frame = load(f)
            jsonschema.validate(frame, env_schema)
            ps = load(SCHEMAS / frame["payload_schema"])
            jsonschema.validate(frame["payload"], ps)
            frame_wo = dict(frame)
            frame_wo.pop("signatures", None)
            h = sha256_hex(canonical_bytes(frame_wo))
            print(f"[OK] {f.name} frame_hash={h}")
        except Exception as e:
            ok = False
            print(f"[FAIL] {f.name}: {e}", file=sys.stderr)
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
