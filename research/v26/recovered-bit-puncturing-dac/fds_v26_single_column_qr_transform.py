from __future__ import annotations

"""Exact single-column inverse-QR transform falsifier for recovered V26 D&C work.

This module deliberately depends on the recovered V25 bit-puncturing core. A clean
checkout must provide that exact core before the frozen cap2/cap3 gates can be run.
"""

from collections import defaultdict
import hashlib
import os
from pathlib import Path
import sys
import time
from typing import Dict, Iterable, Mapping, Tuple

EXPECTED_BP_SHA256 = "ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130"
Mask4 = Tuple[int, int, int, int]

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
for dep_dir in (
    REPO_ROOT / "research" / "v25" / "bit-puncturing" / "recovered-runtime",
    REPO_ROOT / "research" / "v25" / "bit-puncturing",
    REPO_ROOT / "research" / "v25" / "boundary-syndrome",
):
    dep = str(dep_dir)
    if dep not in sys.path:
        sys.path.insert(0, dep)

try:
    import fds_v25_bit_puncturing as bp
except ModuleNotFoundError as exc:
    raise RuntimeError(
        "Missing canonical recovered dependency fds_v25_bit_puncturing.py. "
        "Run scripts/rematerialize_v25_trail_dac.py on a source containing the exact "
        "recovered snapshot, then retry. Expected core SHA-256: "
        f"{EXPECTED_BP_SHA256}."
    ) from exc

import fds_v26_second_layer_separator as sep


def recovered_core_sha256() -> str:
    path = os.path.realpath(bp.__file__)
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def assert_recovered_core_provenance() -> None:
    got = recovered_core_sha256()
    if got != EXPECTED_BP_SHA256:
        raise RuntimeError(
            f"Recovered bit-puncturing core SHA-256 mismatch: {got}; "
            f"expected {EXPECTED_BP_SHA256}"
        )


def _signed_merge(items: Iterable[tuple[Mask4, float]]) -> Dict[Mask4, float]:
    out: defaultdict[Mask4, float] = defaultdict(float)
    for masks, coeff in items:
        if coeff:
            out[masks] += float(coeff)
    return {k: v for k, v in out.items() if v != 0.0}


def transform_signed_marginal(
    coeffs: Mapping[Mask4, float],
    *,
    n: int = 32,
    max_sigma_weight: int,
) -> dict:
    """Apply the frozen bounded inverse-QR operator linearly to one signed marginal."""
    t0 = time.perf_counter()
    cache: dict[Mask4, tuple[tuple[Mask4, float], ...]] = {}
    merged: defaultdict[Mask4, float] = defaultdict(float)
    raw_outputs = 0

    for masks, outer_coeff in coeffs.items():
        masks = tuple(int(x) for x in masks)
        local = cache.get(masks)
        if local is None:
            hull = bp.inverse_qr_linear_hull(
                masks,
                n=n,
                beam=None,
                max_sigma_weight=max_sigma_weight,
                min_abs=0.0,
            )
            local = tuple(
                (tuple(int(x) for x in state.masks), float(state.coeff))
                for state in hull
                if state.coeff
            )
            cache[masks] = local
        raw_outputs += len(local)
        oc = float(outer_coeff)
        for out_masks, local_coeff in local:
            v = oc * local_coeff
            if v:
                merged[out_masks] += v

    exact = {k: v for k, v in merged.items() if v != 0.0}
    return {
        "input_support": len(coeffs),
        "unique_local_qr_inputs": len(cache),
        "raw_local_trail_outputs": raw_outputs,
        "support": len(exact),
        "energy": sum(v * v for v in exact.values()),
        "compact_bytes_24": len(exact) * 24,
        "coeffs": exact,
        "sec": time.perf_counter() - t0,
    }


def factorized_then_transform_column(
    *,
    column_index: int,
    n: int = 32,
    max_sigma_weight: int,
) -> dict:
    fdata = sep.first_layer_factors(
        n=n,
        max_sigma_weight=max_sigma_weight,
        local_beam=None,
        min_abs=0.0,
    )
    marginal = sep.factorized_column_marginal_packed(
        fdata,
        column_index,
        return_dict=True,
    )
    transformed = transform_signed_marginal(
        marginal["coeffs"],
        n=n,
        max_sigma_weight=max_sigma_weight,
    )
    transformed["column_index"] = column_index
    transformed["input_energy"] = marginal["energy"]
    return transformed


def explicit_global_then_transform_column(
    *,
    column_index: int,
    n: int = 32,
    max_sigma_weight: int,
) -> dict:
    """Frozen cap2 reference: explicit first-layer global hull, then local QR propagation."""
    hull = bp.inverse_double_round_linear_hull(
        sep.Q138_MASKS,
        n=n,
        beam=None,
        local_beam=None,
        max_sigma_weight=max_sigma_weight,
        min_abs=0.0,
    )
    cq = sep.ch.COL_QR[column_index]
    merged: defaultdict[Mask4, float] = defaultdict(float)
    cache: dict[Mask4, tuple[tuple[Mask4, float], ...]] = {}
    raw_outputs = 0
    t0 = time.perf_counter()

    # Propagate every explicit global first-layer state before marginalization.
    # This keeps the frozen cap2 reference independent of the factorized
    # marginal-then-transform path under test.
    for state in hull:
        in_masks = tuple(int(state.masks[i]) for i in cq)
        local = cache.get(in_masks)
        if local is None:
            qh = bp.inverse_qr_linear_hull(
                in_masks,
                n=n,
                beam=None,
                max_sigma_weight=max_sigma_weight,
                min_abs=0.0,
            )
            local = tuple(
                (tuple(int(x) for x in qstate.masks), float(qstate.coeff))
                for qstate in qh
                if qstate.coeff
            )
            cache[in_masks] = local
        raw_outputs += len(local)
        outer = float(state.coeff)
        for out_masks, local_coeff in local:
            v = outer * local_coeff
            if v:
                merged[out_masks] += v

    exact = {k: v for k, v in merged.items() if v != 0.0}
    return {
        "column_index": column_index,
        "global_first_layer_support": len(hull),
        "unique_local_qr_inputs": len(cache),
        "raw_local_trail_outputs": raw_outputs,
        "support": len(exact),
        "energy": sum(v * v for v in exact.values()),
        "compact_bytes_24": len(exact) * 24,
        "coeffs": exact,
        "sec": time.perf_counter() - t0,
    }


def compare_exact(a: Mapping[Mask4, float], b: Mapping[Mask4, float]) -> dict:
    keys = set(a) | set(b)
    max_err = max(
        (abs(float(a.get(k, 0.0)) - float(b.get(k, 0.0))) for k in keys),
        default=0.0,
    )
    ea = sum(float(v) * float(v) for v in a.values())
    eb = sum(float(v) * float(v) for v in b.values())
    return {
        "support_match": set(a) == set(b),
        "max_coefficient_abs_error": max_err,
        "energy_abs_error": abs(ea - eb),
    }
