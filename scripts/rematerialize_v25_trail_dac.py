#!/usr/bin/env python3
from __future__ import annotations

"""Locate and restore the exact recovered V25 trail-D&C runtime from trusted bytes.

The script never accepts a rewritten substitute as canonical. It prefers a ZIP
whose SHA-256 equals the frozen recovered snapshot hash and restores runtime files
only from that verified container. If the complete snapshot is unavailable, it may
restore the exact canonical bit-puncturing core by its file-level SHA-256 alone,
while explicitly marking snapshot/runtime provenance incomplete.
"""

import argparse
from io import BytesIO
import hashlib
import json
from pathlib import Path
import zipfile

SNAPSHOT_SHA256 = "fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6"
CORE_SHA256 = "ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130"
TEST_SHA256 = "30284e9db228032b2d76aeaf872c1903405e1c86ab1a364eec4feab9a62c0350"
CERT_SHA256 = "576b0f13d0983a76fb7e07f2e5a224ad890bd6d14b4ca2614a8c0ea012f5ee20"

RUNTIME_BASENAMES = (
    "fds_v25_bit_puncturing.py",
    "fds_v25_chacha.py",
    "fds_v25_pnb_orbit.py",
)
MAX_ENTRY_BYTES = 128 * 1024 * 1024
MAX_RECURSION = 4


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_zip(data: bytes) -> bool:
    return len(data) >= 4 and data[:4] == b"PK\x03\x04"


def _find_hash_bytes(data: bytes, label: str, target_sha256: str, depth: int = 0):
    if sha256_bytes(data) == target_sha256:
        return data, label
    if depth >= MAX_RECURSION or not _is_zip(data):
        return None

    try:
        zf = zipfile.ZipFile(BytesIO(data))
    except zipfile.BadZipFile:
        return None

    with zf:
        for info in zf.infolist():
            if info.is_dir() or info.file_size > MAX_ENTRY_BYTES:
                continue
            child = zf.read(info)
            child_label = f"{label}!{info.filename}"
            if sha256_bytes(child) == target_sha256:
                return child, child_label
            if info.filename.lower().endswith(".zip") or _is_zip(child):
                found = _find_hash_bytes(child, child_label, target_sha256, depth + 1)
                if found is not None:
                    return found
    return None


def find_hashed_bytes(path: Path, target_sha256: str):
    path = path.resolve()
    if path.is_file():
        if path.stat().st_size > MAX_ENTRY_BYTES:
            return None
        return _find_hash_bytes(path.read_bytes(), str(path), target_sha256)

    if not path.is_dir():
        raise FileNotFoundError(path)

    for candidate in sorted(p for p in path.rglob("*") if p.is_file()):
        if candidate.stat().st_size > MAX_ENTRY_BYTES:
            continue
        found = _find_hash_bytes(candidate.read_bytes(), str(candidate), target_sha256)
        if found is not None:
            return found
    return None


def find_snapshot(path: Path):
    return find_hashed_bytes(path, SNAPSHOT_SHA256)


def find_core(path: Path):
    return find_hashed_bytes(path, CORE_SHA256)


def inspect_verified_snapshot(snapshot: bytes, locator: str) -> dict:
    if sha256_bytes(snapshot) != SNAPSHOT_SHA256:
        raise ValueError("snapshot hash mismatch")

    runtime: dict[str, dict] = {}
    hash_hits: dict[str, list[dict]] = {
        "core": [],
        "test": [],
        "cert": [],
    }

    with zipfile.ZipFile(BytesIO(snapshot)) as zf:
        for info in zf.infolist():
            if info.is_dir() or info.file_size > MAX_ENTRY_BYTES:
                continue
            data = zf.read(info)
            digest = sha256_bytes(data)
            base = Path(info.filename).name

            if base in RUNTIME_BASENAMES:
                if base in runtime:
                    raise RuntimeError(f"duplicate runtime basename in snapshot: {base}")
                runtime[base] = {
                    "member": info.filename,
                    "bytes": len(data),
                    "sha256": digest,
                    "_data": data,
                }

            if digest == CORE_SHA256:
                hash_hits["core"].append({"member": info.filename, "bytes": len(data)})
            if digest == TEST_SHA256:
                hash_hits["test"].append({"member": info.filename, "bytes": len(data)})
            if digest == CERT_SHA256:
                hash_hits["cert"].append({"member": info.filename, "bytes": len(data)})

    core = runtime.get("fds_v25_bit_puncturing.py")
    if core is None:
        raise RuntimeError("verified snapshot lacks fds_v25_bit_puncturing.py")
    if core["sha256"] != CORE_SHA256:
        raise RuntimeError(
            "verified snapshot core filename exists but source hash does not match frozen authority"
        )

    public_runtime = {
        name: {k: v for k, v in row.items() if k != "_data"}
        for name, row in runtime.items()
    }
    return {
        "snapshot_locator": locator,
        "snapshot_sha256": SNAPSHOT_SHA256,
        "runtime": public_runtime,
        "hash_hits": hash_hits,
        "_runtime_private": runtime,
    }


def restore(report: dict, repo_root: Path) -> Path:
    target = repo_root / "research" / "v25" / "bit-puncturing" / "recovered-runtime"
    target.mkdir(parents=True, exist_ok=True)

    runtime = report["_runtime_private"]
    for name in RUNTIME_BASENAMES:
        row = runtime.get(name)
        if row is None:
            continue
        (target / name).write_bytes(row["_data"])

    manifest = {
        "snapshot_locator": report["snapshot_locator"],
        "snapshot_sha256": report["snapshot_sha256"],
        "runtime": report["runtime"],
        "hash_hits": report["hash_hits"],
        "restored_to": str(target.relative_to(repo_root)),
    }
    (target / "RECOVERED_SNAPSHOT_PROVENANCE.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return target


def restore_core_only(core: bytes, locator: str, repo_root: Path) -> Path:
    if sha256_bytes(core) != CORE_SHA256:
        raise ValueError("core hash mismatch")
    target = repo_root / "research" / "v25" / "bit-puncturing" / "recovered-runtime"
    target.mkdir(parents=True, exist_ok=True)
    (target / "fds_v25_bit_puncturing.py").write_bytes(core)
    manifest = {
        "recovery_mode": "core_only",
        "core_locator": locator,
        "core_sha256": CORE_SHA256,
        "core_verified": True,
        "snapshot_verified": False,
        "runtime_complete": False,
        "restored_to": str(target.relative_to(repo_root)),
        "warning": "Exact canonical core restored without the canonical snapshot; companion runtime provenance remains unresolved until separately verified.",
    }
    (target / "RECOVERED_CORE_PROVENANCE.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="snapshot/core file, outer ZIP, or directory")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (default: inferred from scripts/)",
    )
    parser.add_argument(
        "--restore",
        action="store_true",
        help="write verified runtime files into research/v25/bit-puncturing/recovered-runtime/",
    )
    args = parser.parse_args()

    found = find_snapshot(args.source)
    if found is not None:
        snapshot, locator = found
        report = inspect_verified_snapshot(snapshot, locator)
        report["recovery_mode"] = "snapshot"
        report["snapshot_verified"] = True
        report["core_verified"] = True
        report["runtime_complete"] = all(name in report["runtime"] for name in RUNTIME_BASENAMES)
        if args.restore:
            restored = restore(report, args.repo_root.resolve())
            report["restored_to"] = str(restored)
        report.pop("_runtime_private", None)
        report["ok"] = True
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    core_found = find_core(args.source)
    if core_found is not None:
        core, locator = core_found
        report = {
            "ok": True,
            "recovery_mode": "core_only",
            "core_locator": locator,
            "core_sha256": CORE_SHA256,
            "core_verified": True,
            "snapshot_verified": False,
            "runtime_complete": False,
            "warning": "Exact canonical core found without the canonical snapshot; do not claim full snapshot provenance or run new measurements until dependencies and the historical baseline are verified.",
        }
        if args.restore:
            restored = restore_core_only(core, locator, args.repo_root.resolve())
            report["restored_to"] = str(restored)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    print(
        json.dumps(
            {
                "ok": False,
                "reason": "exact recovered snapshot/core SHA-256 not found",
                "expected_snapshot_sha256": SNAPSHOT_SHA256,
                "expected_core_sha256": CORE_SHA256,
            },
            indent=2,
        )
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
