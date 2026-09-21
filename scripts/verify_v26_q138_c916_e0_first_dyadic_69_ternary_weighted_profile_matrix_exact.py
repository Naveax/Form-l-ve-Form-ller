#!/usr/bin/env python3
"""Prepared exact weighted profile matrix for the 69-ternary C916 inventory.

This is intentionally a preparation artifact only while the frozen 38-ternary weighted
baseline is still completing.  It appends the ten merged tail3 and twelve merged tail4
exact quotient factors to the existing 38-factor authority without changing pairwise,
affine, quaternary, multiplicity, or separator-profile semantics.

The six-factor historical integer remains the mandatory regression gate because the first
six ternary factors are unchanged and every appended factor is an additional exact
constraint.
"""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path

TARGET_DOMAIN_STATE_SUMS = (83, 88, 95, 100, 102, 134, 154, 251, 288, 302)
EXPECTED_SIX_FACTOR_TOTAL = 90987190266267462495323685079227633113020903735137825407846207198697839001600000
EXPECTED_AFFINE_TOTAL = 100215909735124105069922281032909019043326715916545026952580687530924399001600000
EXPECTED_BASE_FACTOR_COUNT = 38
EXPECTED_TAIL3_FACTOR_COUNT = 10
EXPECTED_TAIL4_FACTOR_COUNT = 12
EXPECTED_TAIL5_FACTOR_COUNT = 9
EXPECTED_TOTAL_FACTOR_COUNT = 69

TAIL3_DIR = Path(os.environ.get("C916_TAIL3_QUOTIENT_DIR", "authorities/tail3-quotient"))
TAIL4_DIR = Path(os.environ.get("C916_TAIL4_QUOTIENT_DIR", "authorities/tail4-quotient"))
TAIL5_DIR = Path(os.environ.get("C916_TAIL5_QUOTIENT_DIR", "authorities/tail5-quotient"))

EXPECTED_TAIL3_SCOPES = (
    (4, 11, 165), (4, 24, 165), (4, 62, 165), (4, 67, 165), (4, 111, 165),
    (4, 113, 165), (4, 114, 165), (4, 136, 165), (4, 144, 165), (4, 165, 181),
)
EXPECTED_TAIL4_SCOPES = (
    (4, 165, 186), (4, 165, 239), (4, 165, 244), (4, 165, 245),
    (4, 165, 249), (4, 181, 182), (7, 181, 182), (8, 181, 182),
    (9, 181, 182), (10, 181, 182), (11, 181, 182), (24, 181, 182),
)
EXPECTED_TAIL5_SCOPES = (
    (62, 181, 182), (67, 181, 182), (113, 181, 182),
    (114, 181, 182), (136, 181, 182), (144, 181, 182),
    (154, 181, 182), (181, 182, 186), (181, 182, 239),
)


def load_promoted(directory: Path, prefix: str, target_key: str, expected_scopes, start_index: int):
    files = sorted(directory.glob(f"{prefix}_*.json"))
    assert len(files) == 16, (directory, [p.name for p in files])
    rows = [json.loads(p.read_text()) for p in files]
    by_target = {int(row[target_key]): row for row in rows}
    assert set(by_target) == set(range(16))

    out = []
    for target in range(16):
        row = by_target[target]
        qholes = int(row["quotient_holes"])
        assert bool(row["promotable_to_current_quotient_factor_inventory"]) == (qholes > 0)
        if qholes == 0:
            continue
        scope = tuple(map(int, row["triple"]))
        qsizes = tuple(map(int, row["quotient_alphabet_sizes"]))
        forbidden = frozenset(tuple(map(int, x)) for x in row["quotient_hole_tuples"])
        assert len(qsizes) == 3
        assert forbidden and len(forbidden) == qholes
        out.append({
            "index": start_index + len(out),
            "scope": scope,
            "qsizes": qsizes,
            "forbidden": forbidden,
            "digest": str(row["quotient_hole_digest_sha256"]),
            "source_target": target,
            "source_tail": prefix,
        })

    assert tuple(sorted(row["scope"] for row in out)) == tuple(sorted(expected_scopes))
    return tuple(out)


def load_extended_factor_specs(E):
    base = tuple(E.load_factor_specs())
    assert len(base) == EXPECTED_BASE_FACTOR_COUNT
    tail3 = load_promoted(
        TAIL3_DIR, "tail3_quotient", "tail3_target",
        EXPECTED_TAIL3_SCOPES, len(base),
    )
    tail4 = load_promoted(
        TAIL4_DIR, "tail4_quotient", "tail4_target",
        EXPECTED_TAIL4_SCOPES, len(base) + len(tail3),
    )
    tail5 = load_promoted(
        TAIL5_DIR, "tail5_quotient", "tail5_target",
        EXPECTED_TAIL5_SCOPES, len(base) + len(tail3) + len(tail4),
    )
    assert len(tail3) == EXPECTED_TAIL3_FACTOR_COUNT
    assert len(tail4) == EXPECTED_TAIL4_FACTOR_COUNT
    assert len(tail5) == EXPECTED_TAIL5_FACTOR_COUNT
    factors = base + tail3 + tail4 + tail5
    assert len(factors) == EXPECTED_TOTAL_FACTOR_COUNT
    scopes = tuple(row["scope"] for row in factors)
    assert len(set(scopes)) == len(scopes)
    assert tuple(row["index"] for row in factors) == tuple(range(len(factors)))
    return factors


def run_profile(target: int, output: Path) -> dict:
    import _c916_all_current_weighted_context_engine as E
    import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_context_exact as V

    assert target in TARGET_DOMAIN_STATE_SUMS
    factors = load_extended_factor_specs(E)
    original_loader = E.load_factor_specs
    E.load_factor_specs = lambda: factors

    class TargetProfileCounter(V.AuthorityCorrectConstraintCounter):
        def count_profile(self, domains):
            dsum = sum(int(d).bit_count() for d in domains)
            if dsum != target:
                return 1, 0, 0
            return super().count_profile(domains)

    def run_one(limit: int, label: str) -> dict:
        E.PROFILE_ROWS.clear()
        original_counter = V.AuthorityCorrectConstraintCounter
        V.AuthorityCorrectConstraintCounter = TargetProfileCounter
        try:
            base = V.run_model(limit, label)
        finally:
            V.AuthorityCorrectConstraintCounter = original_counter

        rows = [row for row in E.PROFILE_ROWS if row["model"] == label]
        assert len(rows) == 1, (label, target, rows)
        exact_row = rows[0]
        base_rows = list(base["profile_rows"])
        assert len(base_rows) == len(TARGET_DOMAIN_STATE_SUMS)
        target_rows = [row for row in base_rows if int(row["domain_state_sum"]) == target]
        assert len(target_rows) == 1
        base_row = target_rows[0]

        raw = int(exact_row["exact_count"])
        base_mass = int(base_row["base_mass"])
        weighted = base_mass * raw
        assert int(base_row["m4_pairwise_relaxation_count"]) == raw

        dummy_background = 0
        for row in base_rows:
            dsum = int(row["domain_state_sum"])
            if dsum == target:
                continue
            assert int(row["m4_pairwise_relaxation_count"]) == 1, (dsum, row)
            dummy_background += int(row["base_mass"])
        assert int(base["exact_count"]) == dummy_background + weighted

        return {
            "label": label,
            "domain_state_sum": target,
            "base_mass": base_mass,
            "exact_profile_count": raw,
            "exact_weighted_summand": weighted,
            "scheduler_dummy_background": dummy_background,
            "calls_delta": int(exact_row["calls_delta"]),
            "memo_states_delta": int(exact_row["memo_states_delta"]),
            "memo_hits_delta": int(exact_row["memo_hits_delta"]),
            "constraint_eval_hits_delta": int(exact_row["constraint_eval_hits_delta"]),
            "constraint_eval_misses_delta": int(exact_row["constraint_eval_misses_delta"]),
            "max_context_variables": int(exact_row["max_context_variables"]),
        }

    try:
        regression = run_one(6, "six_factor_regression")
        if int(regression["exact_profile_count"]) == 0:
            full = {
                **regression,
                "label": "all_current_69_ternary",
                "exact_profile_count": 0,
                "exact_weighted_summand": 0,
                "derived_from_zero_regression_by_monotonicity": True,
                "calls_delta": 0,
                "memo_states_delta": 0,
                "memo_hits_delta": 0,
                "constraint_eval_hits_delta": 0,
                "constraint_eval_misses_delta": 0,
            }
        else:
            full = run_one(len(factors), "all_current_69_ternary")
            full["derived_from_zero_regression_by_monotonicity"] = False
    finally:
        E.load_factor_specs = original_loader

    assert full["base_mass"] == regression["base_mass"]
    assert 0 <= int(full["exact_profile_count"]) <= int(regression["exact_profile_count"])

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": target,
        "base_ternary_factors": EXPECTED_BASE_FACTOR_COUNT,
        "tail3_promoted_ternary_factors": EXPECTED_TAIL3_FACTOR_COUNT,
        "tail4_promoted_ternary_factors": EXPECTED_TAIL4_FACTOR_COUNT,
        "tail5_promoted_ternary_factors": EXPECTED_TAIL5_FACTOR_COUNT,
        "total_ternary_factors": EXPECTED_TOTAL_FACTOR_COUNT,
        "regression": regression,
        "all_current": full,
        "decision": "C916_69_TERNARY_WEIGHTED_EXACT_PROFILE_SUMMAND",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("profile_result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_60_TERNARY_WEIGHTED_PROFILE_EXACT")
    print("ALPHA_PASS=0")
    return out


def aggregate(directory: Path, output: Path) -> dict:
    rows = [json.loads(path.read_text()) for path in sorted(directory.glob("profile-*.json"))]
    assert len(rows) == len(TARGET_DOMAIN_STATE_SUMS)
    by_target = {int(row["domain_state_sum"]): row for row in rows}
    assert tuple(sorted(by_target)) == TARGET_DOMAIN_STATE_SUMS

    regression_total = sum(int(row["regression"]["exact_weighted_summand"]) for row in rows)
    total = sum(int(row["all_current"]["exact_weighted_summand"]) for row in rows)
    assert regression_total == EXPECTED_SIX_FACTOR_TOTAL
    assert 0 <= total <= regression_total <= EXPECTED_AFFINE_TOTAL

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "separator_domain_profiles": len(rows),
        "domain_state_sums": list(TARGET_DOMAIN_STATE_SUMS),
        "base_ternary_factors": EXPECTED_BASE_FACTOR_COUNT,
        "tail3_promoted_ternary_factors": EXPECTED_TAIL3_FACTOR_COUNT,
        "tail4_promoted_ternary_factors": EXPECTED_TAIL4_FACTOR_COUNT,
        "tail5_promoted_ternary_factors": EXPECTED_TAIL5_FACTOR_COUNT,
        "total_ternary_factors": EXPECTED_TOTAL_FACTOR_COUNT,
        "six_factor_regression_expected": EXPECTED_SIX_FACTOR_TOTAL,
        "six_factor_regression_observed": regression_total,
        "all_order_affine_support_exact_count": EXPECTED_AFFINE_TOTAL,
        "exact_69_ternary_weighted_count": total,
        "exact_log2": None if total == 0 else math.log2(total),
        "state_bits": total.bit_length(),
        "profile_rows": [by_target[target] for target in TARGET_DOMAIN_STATE_SUMS],
        "decision": "C916_COMPLETE_AFFINE_PLUS_60_TERNARY_WEIGHTED_COUNT_PROFILE_MATRIX_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_60_TERNARY_WEIGHTED_PROFILE_MATRIX_EXACT")
    print("boundary=exact for the finite 69-ternary physical inventory; it is not a completeness theorem or end-to-end work exponent")
    print("ALPHA_PASS=0")
    return out


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    p = sub.add_parser("profile")
    p.add_argument("--domain-state-sum", type=int, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = sub.add_parser("aggregate")
    a.add_argument("--directory", type=Path, required=True)
    a.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "profile":
        run_profile(args.domain_state_sum, args.output)
    else:
        aggregate(args.directory, args.output)


if __name__ == "__main__":
    main()
