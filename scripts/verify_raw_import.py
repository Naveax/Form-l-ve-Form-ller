from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL_MANIFEST = ROOT / "archive/RAW_IMPORT_FULL_MANIFEST.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_manifest() -> dict:
    return json.loads(FULL_MANIFEST.read_text(encoding="utf-8"))


def verify_directory(source: Path, manifest: dict) -> dict:
    want = {x["name"]: x for x in manifest["files"]}
    got = {p.name: p for p in source.iterdir() if p.is_file()}
    missing = sorted(set(want) - set(got))
    extra = sorted(set(got) - set(want))
    bad = []
    for name, rec in want.items():
        p = got.get(name)
        if p is None:
            continue
        data = p.read_bytes()
        sha = sha256_bytes(data)
        if len(data) != rec["bytes"] or sha != rec["sha256"]:
            bad.append({"name": name, "bytes": len(data), "sha256": sha})
    return {"mode": "directory", "missing": missing, "extra": extra, "bad": bad,
            "ok": not missing and not extra and not bad}


def verify_zip(source: Path, manifest: dict) -> dict:
    want = {x["name"]: x for x in manifest["files"]}
    with zipfile.ZipFile(source) as z:
        got = {x.filename.rstrip("/"): x for x in z.infolist() if not x.is_dir()}
        missing = sorted(set(want) - set(got))
        extra = sorted(set(got) - set(want))
        bad = []
        for name, rec in want.items():
            if name not in got:
                continue
            data = z.read(name)
            sha = sha256_bytes(data)
            if len(data) != rec["bytes"] or sha != rec["sha256"]:
                bad.append({"name": name, "bytes": len(data), "sha256": sha})
    return {"mode": "zip", "missing": missing, "extra": extra, "bad": bad,
            "ok": not missing and not extra and not bad}


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify a rematerialized raw-import directory or ZIP against the canonical full manifest.")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--source-dir", type=Path)
    group.add_argument("--archive", type=Path)
    args = ap.parse_args()
    manifest = load_manifest()

    if args.source_dir:
        result = verify_directory(args.source_dir, manifest)
    elif args.archive:
        result = verify_zip(args.archive, manifest)
    else:
        # Manifest-only self-check. This intentionally does not pretend the bulk bytes
        # are present in Git. It verifies count/total uniqueness bookkeeping only.
        files = manifest["files"]
        names = [x["name"] for x in files]
        result = {
            "mode": "manifest-only",
            "file_count": len(files),
            "declared_file_count": manifest["file_count"],
            "total_bytes": sum(x["bytes"] for x in files),
            "declared_total_bytes": manifest["total_bytes"],
            "unique_names": len(names) == len(set(names)),
        }
        result["ok"] = (
            result["file_count"] == result["declared_file_count"]
            and result["total_bytes"] == result["declared_total_bytes"]
            and result["unique_names"]
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
