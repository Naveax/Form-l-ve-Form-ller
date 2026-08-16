from __future__ import annotations

import hashlib
import importlib.util
from io import BytesIO
import json
from pathlib import Path
import zipfile


def _load_module():
    script = Path(__file__).with_name("rematerialize_v25_trail_dac.py")
    spec = importlib.util.spec_from_file_location("rematerialize_v25_trail_dac", script)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _zip_bytes(entries: dict[str, bytes]) -> bytes:
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in entries.items():
            zf.writestr(name, data)
    return buf.getvalue()


def test_nested_snapshot_recovery_and_restore(tmp_path):
    r = _load_module()
    core = b"canonical-core-synthetic\n"
    chacha = b"chacha-synthetic\n"
    pnb = b"pnb-synthetic\n"
    test = b"test-synthetic\n"
    cert = b"cert-synthetic\n"
    snapshot = _zip_bytes(
        {
            "src/fds_v25_bit_puncturing.py": core,
            "src/fds_v25_chacha.py": chacha,
            "src/fds_v25_pnb_orbit.py": pnb,
            "tests/test_core.py": test,
            "cert/summary.json": cert,
        }
    )
    outer = _zip_bytes({"nested/backup.zip": snapshot})
    source = tmp_path / "outer.zip"
    source.write_bytes(outer)

    r.CORE_SHA256 = hashlib.sha256(core).hexdigest()
    r.SNAPSHOT_SHA256 = hashlib.sha256(snapshot).hexdigest()
    r.TEST_SHA256 = hashlib.sha256(test).hexdigest()
    r.CERT_SHA256 = hashlib.sha256(cert).hexdigest()

    found = r.find_snapshot(source)
    assert found is not None
    report = r.inspect_verified_snapshot(*found)
    assert report["runtime"]["fds_v25_bit_puncturing.py"]["sha256"] == r.CORE_SHA256

    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    target = r.restore(report, repo_root)
    assert hashlib.sha256((target / "fds_v25_bit_puncturing.py").read_bytes()).hexdigest() == r.CORE_SHA256


def test_nested_core_only_recovery_is_explicitly_incomplete(tmp_path):
    r = _load_module()
    core = b"exact-core-only-synthetic\n"
    inner = _zip_bytes({"odd/path/not_named_core.bin": core})
    outer = _zip_bytes({"deeper.zip": inner})
    source = tmp_path / "core-only-outer.zip"
    source.write_bytes(outer)

    r.CORE_SHA256 = hashlib.sha256(core).hexdigest()
    r.SNAPSHOT_SHA256 = "0" * 64

    assert r.find_snapshot(source) is None
    found = r.find_core(source)
    assert found is not None
    assert found[0] == core
    assert "!deeper.zip!" in found[1]

    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    target = r.restore_core_only(*found, repo_root)
    assert (target / "fds_v25_bit_puncturing.py").read_bytes() == core

    provenance = json.loads((target / "RECOVERED_CORE_PROVENANCE.json").read_text())
    assert provenance["core_verified"] is True
    assert provenance["snapshot_verified"] is False
    assert provenance["runtime_complete"] is False
