#!/usr/bin/env python3
"""Prepared fourth-level exact fallback for unresolved profile-251 third-level slices.

Activation rule: use only for a third-level grandchild that has actually failed or hit
its runner ceiling. The first three deterministic state splits are reconstructed exactly,
then only that one unresolved grandchild is partitioned by the next deterministic
multistate quotient variable. No successful third-level slice is recomputed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_profile_251_third_level_shard_exact as T3

TARGET = T3.TARGET
BASE_MASS = T3.EXPECTED_BASE_MASS
PARENT_REGRESSION_COUNTS = T3.PARENT_REGRESSION_COUNTS
FOURTH_SHARD_COUNT = 5
HEAVY_PARENT_CHILDREN = ((1, 1), (1, 3), (3, 1), (3, 3))
HEAVY_GRANDCHILDREN = (1, 3)


def run_fourth(parent_shard: int, child_shard: int, grandchild_shard: int, fourth_shard: int, output: Path):
    import _c916_all_current_weighted_context_engine as E
    import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_context_exact as V

    assert (parent_shard, child_shard) in HEAVY_PARENT_CHILDREN
    assert grandchild_shard in HEAVY_GRANDCHILDREN
    assert 0 <= fourth_shard < FOURTH_SHARD_COUNT
    factors = E.load_factor_specs()
    assert len(factors) == 38

    class Counter(V.AuthorityCorrectConstraintCounter):
        _meta = None

        def count_profile(self, domains):
            original = tuple(map(int, domains))
            if sum(int(d).bit_count() for d in original) != TARGET:
                return 1, 0, 0

            first_i, first_mask, first_bits = T3.split_spec(self, E, original)
            assert first_i == T3.FIRST_SPLIT_VARIABLE_INDEX
            assert first_mask == T3.FIRST_SPLIT_DOMAIN_MASK
            assert first_bits == T3.FIRST_SPLIT_BITS
            d1 = list(original)
            d1[first_i] = int(first_bits[parent_shard])
            d1 = tuple(d1)

            second_i, second_mask, second_bits = T3.split_spec(self, E, d1)
            assert second_i == 11 and second_mask == 15 and second_bits == (1, 2, 4, 8)
            d2 = list(d1)
            d2[second_i] = int(second_bits[child_shard])
            d2 = tuple(d2)

            third_i, third_mask, third_bits = T3.split_spec(self, E, d2)
            assert third_i == 14 and third_mask == 15 and third_bits == (1, 2, 4, 8)
            d3 = list(d2)
            d3[third_i] = int(third_bits[grandchild_shard])
            d3 = tuple(d3)

            fourth_i, fourth_mask, fourth_bits = T3.split_spec(self, E, d3)
            assert fourth_i not in (first_i, second_i, third_i)
            Counter._meta = {
                "parent_shard_index": parent_shard,
                "child_shard_index": child_shard,
                "grandchild_shard_index": grandchild_shard,
                "parent_state_bit": int(first_bits[parent_shard]),
                "child_state_bit": int(second_bits[child_shard]),
                "grandchild_state_bit": int(third_bits[grandchild_shard]),
                "first_split_variable_index": first_i,
                "second_split_variable_index": second_i,
                "third_split_variable_index": third_i,
                "fourth_split_variable_index": fourth_i,
                "fourth_split_variable_members": list(map(int, self.variables[fourth_i])),
                "fourth_split_domain_mask": fourth_mask,
                "fourth_split_state_count": len(fourth_bits),
                "fourth_shard_index": fourth_shard,
                "fourth_state_bit": 0 if fourth_shard >= len(fourth_bits) else int(fourth_bits[fourth_shard]),
            }

            if fourth_shard >= len(fourth_bits):
                row = {
                    "model": E.MODEL_LABEL,
                    "domain_state_sum": sum(int(d).bit_count() for d in d3),
                    "exact_count": 0,
                    "calls_delta": 0,
                    "memo_states_total": len(self.memo),
                    "memo_states_delta": 0,
                    "memo_hits_delta": 0,
                    "hyper_prunes_total": self.hyper_prunes,
                    "hyper_rounds_total": self.hyper_rounds,
                    "hyper_checks_total": self.hyper_checks,
                    "constraint_eval_hits_delta": 0,
                    "constraint_eval_misses_delta": 0,
                    "max_context_variables": self.max_context_variables,
                }
                E.PROFILE_ROWS.append(row)
                return 0, self.calls, len(self.memo)

            d4 = list(d3)
            d4[fourth_i] = int(fourth_bits[fourth_shard])
            return super().count_profile(tuple(d4))

    E.PROFILE_ROWS.clear()
    original_counter = V.AuthorityCorrectConstraintCounter
    V.AuthorityCorrectConstraintCounter = Counter
    try:
        base = V.run_model(len(factors), "all_current_fourth_level")
    finally:
        V.AuthorityCorrectConstraintCounter = original_counter

    rows = [row for row in E.PROFILE_ROWS if row["model"] == "all_current_fourth_level"]
    assert len(rows) == 1, rows
    exact = rows[0]
    target_rows = [row for row in base["profile_rows"] if int(row["domain_state_sum"]) == TARGET]
    assert len(target_rows) == 1
    base_row = target_rows[0]
    assert int(base_row["base_mass"]) == BASE_MASS
    raw = int(exact["exact_count"])
    assert int(base_row["m4_pairwise_relaxation_count"]) == raw
    assert raw <= PARENT_REGRESSION_COUNTS[parent_shard]

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "shard": Counter._meta,
        "all_current": {
            "exact_profile_count": raw,
            "exact_weighted_summand": BASE_MASS * raw,
            "base_mass": BASE_MASS,
            "calls_delta": int(exact["calls_delta"]),
            "memo_states_delta": int(exact["memo_states_delta"]),
            "memo_hits_delta": int(exact["memo_hits_delta"]),
            "constraint_eval_hits_delta": int(exact["constraint_eval_hits_delta"]),
            "constraint_eval_misses_delta": int(exact["constraint_eval_misses_delta"]),
            "max_context_variables": int(exact["max_context_variables"]),
        },
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_FOURTH_LEVEL_STATE_SHARD_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("fourth_level_shard_result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_FOURTH_LEVEL_STATE_SHARD_EXACT")
    print("ALPHA_PASS=0")
    return out


def aggregate_grandchild(parent_shard: int, child_shard: int, grandchild_shard: int, directory: Path, output: Path):
    paths = sorted(directory.glob(
        f"profile-251-parent-{parent_shard}-child-{child_shard}-grandchild-{grandchild_shard}-fourth-*.json"
    ))
    assert len(paths) == FOURTH_SHARD_COUNT, [p.name for p in paths]
    rows = [json.loads(p.read_text()) for p in paths]
    by = {int(r["shard"]["fourth_shard_index"]): r for r in rows}
    assert tuple(sorted(by)) == tuple(range(FOURTH_SHARD_COUNT))
    first = by[0]["shard"]
    keys = (
        "parent_shard_index", "child_shard_index", "grandchild_shard_index",
        "first_split_variable_index", "second_split_variable_index",
        "third_split_variable_index", "fourth_split_variable_index",
        "fourth_split_variable_members", "fourth_split_domain_mask",
        "fourth_split_state_count",
    )
    for i in range(1, FOURTH_SHARD_COUNT):
        assert all(by[i]["shard"][k] == first[k] for k in keys)
    assert int(first["fourth_split_state_count"]) <= FOURTH_SHARD_COUNT
    raw = sum(int(by[i]["all_current"]["exact_profile_count"]) for i in range(FOURTH_SHARD_COUNT))
    assert raw <= PARENT_REGRESSION_COUNTS[parent_shard]
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "parent_shard_index": parent_shard,
        "child_shard_index": child_shard,
        "grandchild_shard_index": grandchild_shard,
        "exact_all_current_grandchild_profile_count": raw,
        "exact_all_current_grandchild_weighted_summand": BASE_MASS * raw,
        "fourth_split_metadata": {k: first[k] for k in keys},
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_FOURTH_LEVEL_GRANDCHILD_AGGREGATED_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_FOURTH_LEVEL_GRANDCHILD_AGGREGATE_EXACT")
    print("ALPHA_PASS=0")
    return out



EXPECTED_PROFILE_REGRESSION_COUNT = T3.EXPECTED_PROFILE_REGRESSION_COUNT
EXPECTED_PROFILE_REGRESSION_WEIGHTED = T3.EXPECTED_PROFILE_REGRESSION_WEIGHTED
NINE_PROFILE_ALL_CURRENT_WEIGHTED = T3.NINE_PROFILE_ALL_CURRENT_WEIGHTED
EXPECTED_FIRST_LEVEL = T3.EXPECTED_FIRST_LEVEL
EXPECTED_NESTED_SUCCESS = T3.EXPECTED_NESTED_SUCCESS
CANCELLED_SECOND_LEVEL_CHILDREN = T3.EXPECTED_THIRD_CHILDREN
THIRD_GRANDCHILD_COUNT = T3.GRANDCHILD_SHARD_COUNT


def aggregate_final_with_replacements(
    first_level_directory: Path,
    nested_directory: Path,
    third_level_directory: Path,
    fourth_replacement_directory: Path,
    output: Path,
):
    """Exact final fan-in with one source per third-level grandchild.

    A grandchild may come either from the direct third-level run or from a fourth-level
    replacement aggregate, never both. This prevents accidental double counting when a
    slow direct job later finishes after a replacement was launched.
    """
    first_rows = {}
    for path in sorted(first_level_directory.glob("profile-251-shard-*.json")):
        row = json.loads(path.read_text())
        idx = int(row["shard"]["shard_index"])
        if idx in EXPECTED_FIRST_LEVEL:
            first_rows[idx] = row
    assert tuple(sorted(first_rows)) == tuple(sorted(EXPECTED_FIRST_LEVEL))
    for idx, expected in EXPECTED_FIRST_LEVEL.items():
        row = first_rows[idx]
        assert int(row["regression"]["exact_profile_count"]) == expected["regression"]
        assert int(row["all_current"]["exact_profile_count"]) == expected["all_current"]
        assert int(row["all_current"]["base_mass"]) == BASE_MASS

    nested_rows = {}
    for path in sorted(nested_directory.glob("profile-251-parent-*-child-*.json")):
        row = json.loads(path.read_text())
        key = (int(row["shard"]["parent_shard_index"]), int(row["shard"]["child_shard_index"]))
        if key in EXPECTED_NESTED_SUCCESS:
            nested_rows[key] = row
    assert tuple(sorted(nested_rows)) == tuple(sorted(EXPECTED_NESTED_SUCCESS))
    for key, expected_count in EXPECTED_NESTED_SUCCESS.items():
        row = nested_rows[key]
        assert int(row["all_current"]["exact_profile_count"]) == expected_count
        assert int(row["all_current"]["base_mass"]) == BASE_MASS

    direct = {}
    for path in sorted(third_level_directory.glob("profile-251-parent-*-child-*-grandchild-*.json")):
        row = json.loads(path.read_text())
        key = (
            int(row["shard"]["parent_shard_index"]),
            int(row["shard"]["child_shard_index"]),
            int(row["shard"]["grandchild_shard_index"]),
        )
        if key[:2] in CANCELLED_SECOND_LEVEL_CHILDREN:
            direct[key] = row

    replacements = {}
    for path in sorted(fourth_replacement_directory.glob(
        "profile-251-parent-*-child-*-grandchild-*-fourth-aggregate.json"
    )):
        row = json.loads(path.read_text())
        key = (
            int(row["parent_shard_index"]),
            int(row["child_shard_index"]),
            int(row["grandchild_shard_index"]),
        )
        assert key[:2] in CANCELLED_SECOND_LEVEL_CHILDREN
        replacements[key] = row

    child_totals = {}
    source_rows = []
    for parent, child in CANCELLED_SECOND_LEVEL_CHILDREN:
        subtotal = 0
        for grandchild in range(THIRD_GRANDCHILD_COUNT):
            key = (parent, child, grandchild)
            have_direct = key in direct
            have_replacement = key in replacements
            assert have_direct ^ have_replacement, (
                "exactly one source required",
                key,
                have_direct,
                have_replacement,
            )
            if have_direct:
                row = direct[key]
                raw = int(row["all_current"]["exact_profile_count"])
                weighted = int(row["all_current"]["exact_weighted_summand"])
                source = "third_level_direct"
            else:
                row = replacements[key]
                raw = int(row["exact_all_current_grandchild_profile_count"])
                weighted = int(row["exact_all_current_grandchild_weighted_summand"])
                source = "fourth_level_replacement"
            assert weighted == BASE_MASS * raw
            subtotal += raw
            source_rows.append({
                "parent_shard_index": parent,
                "child_shard_index": child,
                "grandchild_shard_index": grandchild,
                "source": source,
                "exact_profile_count": raw,
                "exact_weighted_summand": weighted,
            })
        assert subtotal <= PARENT_REGRESSION_COUNTS[parent]
        child_totals[(parent, child)] = subtotal

    regression_count = (
        sum(v["regression"] for v in EXPECTED_FIRST_LEVEL.values())
        + PARENT_REGRESSION_COUNTS[1]
        + PARENT_REGRESSION_COUNTS[3]
    )
    assert regression_count == EXPECTED_PROFILE_REGRESSION_COUNT
    assert BASE_MASS * regression_count == EXPECTED_PROFILE_REGRESSION_WEIGHTED

    all_current_count = (
        sum(v["all_current"] for v in EXPECTED_FIRST_LEVEL.values())
        + sum(EXPECTED_NESTED_SUCCESS.values())
        + sum(child_totals.values())
    )
    assert 0 <= all_current_count <= regression_count
    profile_weighted = BASE_MASS * all_current_count
    ten_profile_total = NINE_PROFILE_ALL_CURRENT_WEIGHTED + profile_weighted

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "six_factor_regression_profile_count": regression_count,
        "six_factor_regression_weighted_summand": EXPECTED_PROFILE_REGRESSION_WEIGHTED,
        "exact_all_current_profile_count": all_current_count,
        "exact_all_current_profile_weighted_summand": profile_weighted,
        "cancelled_second_level_child_totals": {
            f"{p}:{c}": child_totals[(p, c)]
            for p, c in CANCELLED_SECOND_LEVEL_CHILDREN
        },
        "grandchild_sources": source_rows,
        "nine_profile_all_current_weighted_sum": NINE_PROFILE_ALL_CURRENT_WEIGHTED,
        "exact_all_current_ten_profile_weighted_count": ten_profile_total,
        "exact_all_current_ten_profile_log2": (
            None if ten_profile_total == 0 else __import__("math").log2(ten_profile_total)
        ),
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_FINAL_FANIN_WITH_FOURTH_LEVEL_REPLACEMENTS_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_FINAL_WITH_FOURTH_LEVEL_REPLACEMENTS_EXACT")
    print("boundary=each third-level grandchild is covered exactly once by either its direct artifact or one exact fourth-level replacement aggregate")
    print("boundary=exact for the current 38-ternary weighted inventory only; later tail3/tail4/tail5 physical factors remain outside")
    print("ALPHA_PASS=0")
    return out


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("fourth")
    s.add_argument("--parent-shard", type=int, required=True)
    s.add_argument("--child-shard", type=int, required=True)
    s.add_argument("--grandchild-shard", type=int, required=True)
    s.add_argument("--fourth-shard", type=int, required=True)
    s.add_argument("--output", type=Path, required=True)
    a = sub.add_parser("aggregate-grandchild")
    a.add_argument("--parent-shard", type=int, required=True)
    a.add_argument("--child-shard", type=int, required=True)
    a.add_argument("--grandchild-shard", type=int, required=True)
    a.add_argument("--directory", type=Path, required=True)
    a.add_argument("--output", type=Path, required=True)
    z = sub.add_parser("aggregate-final-with-replacements")
    z.add_argument("--first-level-directory", type=Path, required=True)
    z.add_argument("--nested-directory", type=Path, required=True)
    z.add_argument("--third-level-directory", type=Path, required=True)
    z.add_argument("--fourth-replacement-directory", type=Path, required=True)
    z.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.mode == "fourth":
        run_fourth(args.parent_shard, args.child_shard, args.grandchild_shard, args.fourth_shard, args.output)
    elif args.mode == "aggregate-grandchild":
        aggregate_grandchild(args.parent_shard, args.child_shard, args.grandchild_shard, args.directory, args.output)
    else:
        aggregate_final_with_replacements(
            args.first_level_directory,
            args.nested_directory,
            args.third_level_directory,
            args.fourth_replacement_directory,
            args.output,
        )


if __name__ == "__main__":
    main()
