#!/usr/bin/env python3
"""Exact profile-matrix execution for the C916 all-current weighted count.

The ten separator-domain profiles in the frozen width-3 base authority are independent
summands.  Running them separately changes only scheduling: every profile still uses the
same exact 4,005-pair quotient model, complete 19 affine all-nonzero obstructions, five
compiled physical quaternary factors, all current ternary factors, and multiplicity
weights.  The aggregate mode adds the ten exact weighted summands and rechecks the
historical six-factor regression integer before admitting an all-current integer.
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


def run_profile(target: int, output: Path) -> dict:
    import _c916_all_current_weighted_context_engine as E
    import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_context_exact as V

    assert target in TARGET_DOMAIN_STATE_SUMS
    factors = E.load_factor_specs()
    assert len(factors) == len(E.TOPO.TERNARY_FACTORS) == 38

    class TargetProfileCounter(V.AuthorityCorrectConstraintCounter):
        def count_profile(self, domains):
            dsum = sum(int(d).bit_count() for d in domains)
            if dsum != target:
                return 0, 0, 0
            return super().count_profile(domains)

    def run_one(limit: int, label: str) -> dict:
        E.PROFILE_ROWS.clear()
        original = V.AuthorityCorrectConstraintCounter
        V.AuthorityCorrectConstraintCounter = TargetProfileCounter
        try:
            base = V.run_model(limit, label)
        finally:
            V.AuthorityCorrectConstraintCounter = original

        rows = [row for row in E.PROFILE_ROWS if row["model"] == label]
        assert len(rows) == 1, (label, target, rows)
        exact_row = rows[0]
        base_rows = [
            row for row in base["profile_rows"]
            if int(row["domain_state_sum"]) == target
        ]
        assert len(base_rows) == 1
        base_row = base_rows[0]
        raw = int(exact_row["exact_count"])
        weighted = int(base["exact_count"])
        base_mass = int(base_row["base_mass"])
        assert int(base_row["m4_pairwise_relaxation_count"]) == raw
        assert weighted == base_mass * raw
        return {
            "label": label,
            "domain_state_sum": target,
            "base_mass": base_mass,
            "exact_profile_count": raw,
            "exact_weighted_summand": weighted,
            "calls_delta": int(exact_row["calls_delta"]),
            "memo_states_delta": int(exact_row["memo_states_delta"]),
            "memo_hits_delta": int(exact_row["memo_hits_delta"]),
            "constraint_eval_hits_delta": int(exact_row["constraint_eval_hits_delta"]),
            "constraint_eval_misses_delta": int(exact_row["constraint_eval_misses_delta"]),
            "max_context_variables": int(exact_row["max_context_variables"]),
        }

    regression = run_one(6, "six_factor_regression")
    full = run_one(len(factors), "all_current")
    assert full["base_mass"] == regression["base_mass"]
    assert 0 <= full["exact_profile_count"] <= regression["exact_profile_count"]

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": target,
        "regression": regression,
        "all_current": full,
        "decision": "C916_ALL_CURRENT_WEIGHTED_EXACT_PROFILE_SUMMAND",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("profile_result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_CURRENT_PHYSICAL_WEIGHTED_PROFILE_EXACT", flush=True)
    print("ALPHA_PASS=0", flush=True)
    return out


def aggregate(directory: Path, output: Path) -> dict:
    rows = []
    for path in sorted(directory.glob("profile-*.json")):
        rows.append(json.loads(path.read_text()))
    assert len(rows) == len(TARGET_DOMAIN_STATE_SUMS), [p.name for p in directory.glob("*")]

    by_target = {int(row["domain_state_sum"]): row for row in rows}
    assert tuple(sorted(by_target)) == tuple(sorted(TARGET_DOMAIN_STATE_SUMS))
    assert len(by_target) == len(rows)

    regression_total = sum(int(row["regression"]["exact_weighted_summand"]) for row in rows)
    all_current_total = sum(int(row["all_current"]["exact_weighted_summand"]) for row in rows)
    assert regression_total == EXPECTED_SIX_FACTOR_TOTAL, (regression_total, EXPECTED_SIX_FACTOR_TOTAL)
    assert 0 <= all_current_total <= regression_total <= EXPECTED_AFFINE_TOTAL

    for target, row in sorted(by_target.items()):
        assert int(row["regression"]["domain_state_sum"]) == target
        assert int(row["all_current"]["domain_state_sum"]) == target
        assert int(row["all_current"]["base_mass"]) == int(row["regression"]["base_mass"])
        assert int(row["all_current"]["exact_profile_count"]) <= int(row["regression"]["exact_profile_count"])

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "separator_domain_profiles": len(rows),
        "domain_state_sums": list(sorted(by_target)),
        "six_factor_regression_expected": EXPECTED_SIX_FACTOR_TOTAL,
        "six_factor_regression_observed": regression_total,
        "all_order_affine_support_exact_count": EXPECTED_AFFINE_TOTAL,
        "exact_all_current_physical_weighted_count": all_current_total,
        "exact_log2": None if all_current_total == 0 else math.log2(all_current_total),
        "state_bits": all_current_total.bit_length(),
        "removed_weighted_assignments_vs_six_factor_checkpoint": regression_total - all_current_total,
        "removed_weighted_assignments_vs_affine": EXPECTED_AFFINE_TOTAL - all_current_total,
        "gain_vs_six_factor_checkpoint_log2_bits": None if all_current_total == 0 else math.log2(regression_total) - math.log2(all_current_total),
        "gain_vs_affine_log2_bits": None if all_current_total == 0 else math.log2(EXPECTED_AFFINE_TOTAL) - math.log2(all_current_total),
        "profile_rows": [by_target[target] for target in sorted(by_target)],
        "decision": "C916_COMPLETE_AFFINE_SUPPORT_PLUS_ALL_CURRENT_EXACT_PHYSICAL_QUOTIENT_FACTORS_WEIGHTED_COUNT_PROFILE_MATRIX",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_CURRENT_PHYSICAL_WEIGHTED_PROFILE_MATRIX_EXACT", flush=True)
    print("theorem=the ten exact separator-domain profile summands reproduce the historical six-factor checkpoint and sum to the exact all-current weighted count under the current certified factor inventory", flush=True)
    print("boundary=no end-to-end work exponent is inferred; additional untested higher-order physical image constraints may still exist", flush=True)
    print("ALPHA_PASS=0", flush=True)
    return out


def main() -> None:
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
