#!/usr/bin/env python3
"""Prepared fourth-level exact fallback for one unresolved profile-251 grandchild.

Activation rule: use only after a specific third-level grandchild has failed or hit its
runner ceiling. The first three deterministic quotient-state splits are reconstructed
exactly, then only that failed grandchild is partitioned by one additional variable.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_profile_251_third_level_shard_exact as L3

TARGET = L3.TARGET
EXPECTED_BASE_MASS = L3.EXPECTED_BASE_MASS
SHARD_COUNT = 5


def run(parent: int, child: int, grandchild: int, fourth: int, output: Path) -> dict:
    import _c916_all_current_weighted_context_engine as E
    import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_context_exact as V

    assert parent in (1, 3)
    assert 0 <= child < 4
    assert 0 <= grandchild < 4
    assert 0 <= fourth < SHARD_COUNT
    factors = E.load_factor_specs()
    assert len(factors) == 38

    class Counter(V.AuthorityCorrectConstraintCounter):
        _meta = None

        def count_profile(self, domains):
            original = tuple(map(int, domains))
            if sum(int(d).bit_count() for d in original) != TARGET:
                return 1, 0, 0

            i1, m1, bits1 = L3.split_spec(self, E, original)
            assert i1 == L3.FIRST_SPLIT_VARIABLE_INDEX
            assert m1 == L3.FIRST_SPLIT_DOMAIN_MASK
            d1 = list(original)
            d1[i1] = int(bits1[parent])
            d1 = tuple(d1)

            i2, m2, bits2 = L3.split_spec(self, E, d1)
            assert i2 == 11 and m2 == 15 and bits2 == (1, 2, 4, 8)
            d2 = list(d1)
            d2[i2] = int(bits2[child])
            d2 = tuple(d2)

            i3, m3, bits3 = L3.split_spec(self, E, d2)
            assert grandchild < len(bits3)
            d3 = list(d2)
            d3[i3] = int(bits3[grandchild])
            d3 = tuple(d3)

            i4, m4, bits4 = L3.split_spec(self, E, d3)
            assert i4 not in (i1, i2, i3)
            Counter._meta = {
                "parent_shard_index": parent,
                "child_shard_index": child,
                "grandchild_shard_index": grandchild,
                "first_split_variable_index": i1,
                "second_split_variable_index": i2,
                "third_split_variable_index": i3,
                "third_split_domain_mask": m3,
                "fourth_split_variable_index": i4,
                "fourth_split_variable_members": list(map(int, self.variables[i4])),
                "fourth_split_domain_mask": m4,
                "fourth_split_state_count": len(bits4),
                "fourth_shard_index": fourth,
                "fourth_state_bit": 0 if fourth >= len(bits4) else int(bits4[fourth]),
            }

            if fourth >= len(bits4):
                E.PROFILE_ROWS.append({
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
                })
                return 0, self.calls, len(self.memo)

            d4 = list(d3)
            d4[i4] = int(bits4[fourth])
            return super().count_profile(tuple(d4))

    E.PROFILE_ROWS.clear()
    original_counter = V.AuthorityCorrectConstraintCounter
    V.AuthorityCorrectConstraintCounter = Counter
    try:
        base = V.run_model(len(factors), "all_current_fourth_level")
    finally:
        V.AuthorityCorrectConstraintCounter = original_counter

    rows = [r for r in E.PROFILE_ROWS if r["model"] == "all_current_fourth_level"]
    assert len(rows) == 1
    exact = rows[0]
    target_rows = [r for r in base["profile_rows"] if int(r["domain_state_sum"]) == TARGET]
    assert len(target_rows) == 1
    base_mass = int(target_rows[0]["base_mass"])
    assert base_mass == EXPECTED_BASE_MASS
    raw = int(exact["exact_count"])
    assert int(target_rows[0]["m4_pairwise_relaxation_count"]) == raw
    assert raw <= L3.PARENT_REGRESSION_COUNTS[parent]

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "shard": Counter._meta,
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
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_FOURTH_LEVEL_STATE_SHARD_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("fourth_level_shard_result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_FOURTH_LEVEL_STATE_SHARD_EXACT")
    print("ALPHA_PASS=0")
    return out


def aggregate(parent: int, child: int, grandchild: int, directory: Path, output: Path) -> dict:
    paths = sorted(directory.glob(
        f"profile-251-parent-{parent}-child-{child}-grandchild-{grandchild}-fourth-*.json"
    ))
    assert len(paths) == SHARD_COUNT
    rows = [json.loads(p.read_text()) for p in paths]
    by = {int(r["shard"]["fourth_shard_index"]): r for r in rows}
    assert tuple(sorted(by)) == tuple(range(SHARD_COUNT))
    first = by[0]["shard"]
    stable = (
        "parent_shard_index", "child_shard_index", "grandchild_shard_index",
        "first_split_variable_index", "second_split_variable_index",
        "third_split_variable_index", "third_split_domain_mask",
        "fourth_split_variable_index", "fourth_split_variable_members",
        "fourth_split_domain_mask", "fourth_split_state_count",
    )
    for i in range(1, SHARD_COUNT):
        assert all(by[i]["shard"][k] == first[k] for k in stable)
    raw = sum(int(by[i]["all_current"]["exact_profile_count"]) for i in range(SHARD_COUNT))
    weighted = EXPECTED_BASE_MASS * raw
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "parent_shard_index": parent,
        "child_shard_index": child,
        "grandchild_shard_index": grandchild,
        "exact_all_current_grandchild_profile_count": raw,
        "exact_all_current_grandchild_weighted_summand": weighted,
        "fourth_split_metadata": {k: first[k] for k in stable},
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_FOURTH_LEVEL_GRANDCHILD_AGGREGATED_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_FOURTH_LEVEL_GRANDCHILD_AGGREGATE_EXACT")
    print("ALPHA_PASS=0")
    return out


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("shard")
    for name in ("parent", "child", "grandchild", "fourth"):
        s.add_argument(f"--{name}", type=int, required=True)
    s.add_argument("--output", type=Path, required=True)
    a = sub.add_parser("aggregate")
    for name in ("parent", "child", "grandchild"):
        a.add_argument(f"--{name}", type=int, required=True)
    a.add_argument("--directory", type=Path, required=True)
    a.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.mode == "shard":
        run(args.parent, args.child, args.grandchild, args.fourth, args.output)
    else:
        aggregate(args.parent, args.child, args.grandchild, args.directory, args.output)


if __name__ == "__main__":
    main()
