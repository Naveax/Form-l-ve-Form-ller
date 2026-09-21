#!/usr/bin/env python3
"""Exact 16-leaf profile-251 fallback for the prepared 80-ternary weighted model.

The partition uses the same pairwise-only deterministic split heuristic as the frozen
38-ternary fallback, so higher-order factors cannot move partition boundaries.  Profile
251 is split first on variable index 10 and then on index 11, each over the four singleton
quotient states. The 16 leaves are disjoint and cover the profile exactly.

The historical six-factor profile-251 regression integer is not recomputed per leaf.
Instead the final fan-in combines its frozen exact weighted summand with the nine
independently recomputed six-factor profile checkpoints and requires the full historical
ten-profile integer exactly.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

TARGET = 251
STATE_COUNT = 4
EXPECTED_FIRST_INDEX = 10
EXPECTED_SECOND_INDEX = 11
EXPECTED_MASK = 15
EXPECTED_BITS = (1, 2, 4, 8)
EXPECTED_BASE_MASS = 243184718013880790060390111206440960000000000
EXPECTED_PROFILE_REGRESSION_COUNT = 87639022052873245102889951271577152
EXPECTED_PROFILE_REGRESSION_WEIGHTED = 21312470864940260066305006484700721917824185471141115669201479972945920000000000
EXPECTED_SIX_FACTOR_TOTAL = 90987190266267462495323685079227633113020903735137825407846207198697839001600000
NINE_TARGETS = (83, 88, 95, 100, 102, 134, 154, 288, 302)


def split_spec(counter, engine, domains):
    raw = tuple(map(int, domains))
    candidates = []
    for i, mask in enumerate(raw):
        if len(counter.variables[i]) != 1:
            continue
        width = int(mask).bit_count()
        if width <= 1:
            continue
        pair_neighbors = engine.PAIRWISE_COUNTER._relevant_neighbors(
            counter, i, counter.ALL, raw
        )
        candidates.append((-width, -int(pair_neighbors).bit_count(), i))
    assert candidates
    _nw, _nd, i = min(candidates)
    full_mask = int(raw[i])
    bits = []
    scan = full_mask
    while scan:
        bit = scan & -scan
        scan ^= bit
        bits.append(bit)
    return i, full_mask, tuple(bits)


def run_leaf(parent: int, child: int, output: Path) -> dict:
    import _c916_all_current_weighted_context_engine as E
    import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_context_exact as V
    import verify_v26_q138_c916_e0_first_dyadic_80_ternary_weighted_profile_matrix_exact as M

    assert 0 <= parent < STATE_COUNT
    assert 0 <= child < STATE_COUNT
    factors = M.load_extended_factor_specs(E)
    assert len(factors) == M.EXPECTED_TOTAL_FACTOR_COUNT == 80

    original_loader = E.load_factor_specs
    E.load_factor_specs = lambda: factors

    class Counter(V.AuthorityCorrectConstraintCounter):
        _meta = None

        def count_profile(self, domains):
            original = tuple(map(int, domains))
            if sum(int(d).bit_count() for d in original) != TARGET:
                return 1, 0, 0

            first_i, first_mask, first_bits = split_spec(self, E, original)
            assert first_i == EXPECTED_FIRST_INDEX
            assert first_mask == EXPECTED_MASK
            assert first_bits == EXPECTED_BITS
            d1 = list(original)
            d1[first_i] = int(first_bits[parent])
            d1 = tuple(d1)

            second_i, second_mask, second_bits = split_spec(self, E, d1)
            assert second_i == EXPECTED_SECOND_INDEX
            assert second_mask == EXPECTED_MASK
            assert second_bits == EXPECTED_BITS
            d2 = list(d1)
            d2[second_i] = int(second_bits[child])
            d2 = tuple(d2)

            Counter._meta = {
                "parent_index": parent,
                "parent_state_bit": int(first_bits[parent]),
                "child_index": child,
                "child_state_bit": int(second_bits[child]),
                "first_split_variable_index": first_i,
                "first_split_variable_members": list(map(int, self.variables[first_i])),
                "first_split_domain_mask": first_mask,
                "second_split_variable_index": second_i,
                "second_split_variable_members": list(map(int, self.variables[second_i])),
                "second_split_domain_mask": second_mask,
            }
            return super().count_profile(d2)

    E.PROFILE_ROWS.clear()
    original_counter = V.AuthorityCorrectConstraintCounter
    V.AuthorityCorrectConstraintCounter = Counter
    try:
        base = V.run_model(len(factors), "all_current_60_profile251_leaf")
    finally:
        V.AuthorityCorrectConstraintCounter = original_counter
        E.load_factor_specs = original_loader

    rows = [r for r in E.PROFILE_ROWS if r["model"] == "all_current_60_profile251_leaf"]
    assert len(rows) == 1, rows
    exact = rows[0]
    target_rows = [r for r in base["profile_rows"] if int(r["domain_state_sum"]) == TARGET]
    assert len(target_rows) == 1
    base_row = target_rows[0]
    base_mass = int(base_row["base_mass"])
    assert base_mass == EXPECTED_BASE_MASS
    raw = int(exact["exact_count"])
    assert int(base_row["m4_pairwise_relaxation_count"]) == raw
    assert 0 <= raw <= EXPECTED_PROFILE_REGRESSION_COUNT

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "total_ternary_factors": 80,
        "leaf": Counter._meta,
        "all_current": {
            "exact_profile_count": raw,
            "exact_weighted_summand": base_mass * raw,
            "base_mass": base_mass,
            "calls_delta": int(exact["calls_delta"]),
            "memo_states_delta": int(exact["memo_states_delta"]),
            "memo_hits_delta": int(exact["memo_hits_delta"]),
            "constraint_eval_hits_delta": int(exact["constraint_eval_hits_delta"]),
            "constraint_eval_misses_delta": int(exact["constraint_eval_misses_delta"]),
            "max_context_variables": int(exact["max_context_variables"]),
        },
        "decision": "C916_80_TERNARY_WEIGHTED_PROFILE_251_SECOND_LEVEL_LEAF_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("leaf_result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_80_TERNARY_WEIGHTED_PROFILE_251_LEAF_EXACT")
    print("ALPHA_PASS=0")
    return out


def aggregate(profile_directory: Path, leaf_directory: Path, output: Path) -> dict:
    profile_paths = sorted(profile_directory.glob("profile-*.json"))
    profiles = [json.loads(p.read_text()) for p in profile_paths]
    by_target = {int(r["domain_state_sum"]): r for r in profiles}
    assert tuple(sorted(by_target)) == NINE_TARGETS

    leaf_paths = sorted(leaf_directory.glob("profile-251-parent-*-child-*.json"))
    assert len(leaf_paths) == STATE_COUNT * STATE_COUNT
    leaves = [json.loads(p.read_text()) for p in leaf_paths]
    by_leaf = {
        (int(r["leaf"]["parent_index"]), int(r["leaf"]["child_index"])): r
        for r in leaves
    }
    assert tuple(sorted(by_leaf)) == tuple(
        (p, c) for p in range(STATE_COUNT) for c in range(STATE_COUNT)
    )

    for p in range(STATE_COUNT):
        for c in range(STATE_COUNT):
            row = by_leaf[(p, c)]
            meta = row["leaf"]
            assert int(meta["first_split_variable_index"]) == EXPECTED_FIRST_INDEX
            assert int(meta["second_split_variable_index"]) == EXPECTED_SECOND_INDEX
            assert int(meta["first_split_domain_mask"]) == EXPECTED_MASK
            assert int(meta["second_split_domain_mask"]) == EXPECTED_MASK
            assert int(meta["parent_state_bit"]) == EXPECTED_BITS[p]
            assert int(meta["child_state_bit"]) == EXPECTED_BITS[c]
            assert int(row["all_current"]["base_mass"]) == EXPECTED_BASE_MASS

    profile251_count = sum(
        int(row["all_current"]["exact_profile_count"]) for row in leaves
    )
    assert 0 <= profile251_count <= EXPECTED_PROFILE_REGRESSION_COUNT
    profile251_weighted = EXPECTED_BASE_MASS * profile251_count
    assert profile251_weighted == sum(
        int(row["all_current"]["exact_weighted_summand"]) for row in leaves
    )

    nine_regression = sum(
        int(by_target[t]["regression"]["exact_weighted_summand"]) for t in NINE_TARGETS
    )
    regression_total = nine_regression + EXPECTED_PROFILE_REGRESSION_WEIGHTED
    assert regression_total == EXPECTED_SIX_FACTOR_TOTAL

    nine_all_current = sum(
        int(by_target[t]["all_current"]["exact_weighted_summand"]) for t in NINE_TARGETS
    )
    total = nine_all_current + profile251_weighted
    assert 0 <= total <= EXPECTED_SIX_FACTOR_TOTAL

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "separator_domain_profiles": 10,
        "total_ternary_factors": 80,
        "six_factor_regression_expected": EXPECTED_SIX_FACTOR_TOTAL,
        "six_factor_regression_observed": regression_total,
        "profile251_six_factor_regression_count": EXPECTED_PROFILE_REGRESSION_COUNT,
        "profile251_six_factor_regression_weighted_summand": EXPECTED_PROFILE_REGRESSION_WEIGHTED,
        "exact_profile251_all_current_count": profile251_count,
        "exact_profile251_all_current_weighted_summand": profile251_weighted,
        "nine_profile_all_current_weighted_sum": nine_all_current,
        "exact_80_ternary_weighted_count": total,
        "exact_log2": None if total == 0 else math.log2(total),
        "profile251_leaves": [by_leaf[(p, c)] for p in range(STATE_COUNT) for c in range(STATE_COUNT)],
        "profile_rows": [by_target[t] for t in NINE_TARGETS],
        "decision": "C916_COMPLETE_AFFINE_PLUS_80_TERNARY_WEIGHTED_COUNT_WITH_PROFILE251_SECOND_LEVEL_LEAVES_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_80_TERNARY_WEIGHTED_PROFILE_MATRIX_WITH_SHARDED_251_EXACT")
    print("boundary=exact for the finite 80-ternary physical inventory; it is not a completeness theorem or end-to-end work exponent")
    print("ALPHA_PASS=0")
    return out


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("leaf")
    s.add_argument("--parent", type=int, required=True)
    s.add_argument("--child", type=int, required=True)
    s.add_argument("--output", type=Path, required=True)
    a = sub.add_parser("aggregate")
    a.add_argument("--profile-directory", type=Path, required=True)
    a.add_argument("--leaf-directory", type=Path, required=True)
    a.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.mode == "leaf":
        run_leaf(args.parent, args.child, args.output)
    else:
        aggregate(args.profile_directory, args.leaf_directory, args.output)


if __name__ == "__main__":
    main()
