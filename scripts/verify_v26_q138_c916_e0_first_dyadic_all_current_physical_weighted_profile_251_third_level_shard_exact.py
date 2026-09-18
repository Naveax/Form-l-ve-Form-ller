#!/usr/bin/env python3
"""Third-level exact fallback for one unresolved profile-251 nested state slice.

This file is intentionally not wired to an automatic workflow. It is a prepared exact
partition tool to activate only if a currently-running second-level child hits its runner
ceiling. The first two state splits are reconstructed deterministically, then the selected
child is partitioned by one additional deterministic quotient variable.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TARGET = 251
FIRST_SPLIT_VARIABLE_INDEX = 10
FIRST_SPLIT_DOMAIN_MASK = 15
FIRST_SPLIT_BITS = (1, 2, 4, 8)
EXPECTED_BASE_MASS = 243184718013880790060390111206440960000000000
PARENT_REGRESSION_COUNTS = {
    1: 28992243592121418664980014424454848,
    3: 29213007350957748367629983757192384,
}
GRANDCHILD_SHARD_COUNT = 5


def split_spec(counter, engine, domains):
    candidates = []
    raw = tuple(map(int, domains))
    for i, mask in enumerate(raw):
        if len(counter.variables[i]) != 1:
            continue
        width = int(mask).bit_count()
        if width <= 1:
            continue
        pair_neighbors = engine.PAIRWISE_COUNTER._relevant_neighbors(counter, i, counter.ALL, raw)
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


def run_grandchild(parent_shard: int, child_shard: int, grandchild_shard: int, output: Path) -> dict:
    import _c916_all_current_weighted_context_engine as E
    import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_context_exact as V

    assert parent_shard in (1, 3)
    assert 0 <= child_shard < 4
    assert 0 <= grandchild_shard < GRANDCHILD_SHARD_COUNT
    factors = E.load_factor_specs()
    assert len(factors) == 38

    class Counter(V.AuthorityCorrectConstraintCounter):
        _last_meta = None

        def count_profile(self, domains):
            original = tuple(map(int, domains))
            if sum(int(d).bit_count() for d in original) != TARGET:
                return 1, 0, 0

            first_i, first_mask, first_bits = split_spec(self, E, original)
            assert first_i == FIRST_SPLIT_VARIABLE_INDEX
            assert first_mask == FIRST_SPLIT_DOMAIN_MASK
            assert first_bits == FIRST_SPLIT_BITS
            pbit = int(first_bits[parent_shard])
            d1 = list(original)
            d1[first_i] = pbit
            d1 = tuple(d1)

            second_i, second_mask, second_bits = split_spec(self, E, d1)
            assert second_i == 11
            assert second_mask == 15
            assert second_bits == (1, 2, 4, 8)
            cbit = int(second_bits[child_shard])
            d2 = list(d1)
            d2[second_i] = cbit
            d2 = tuple(d2)

            third_i, third_mask, third_bits = split_spec(self, E, d2)
            assert third_i not in (first_i, second_i)
            meta = {
                "parent_shard_index": parent_shard,
                "parent_state_bit": pbit,
                "child_shard_index": child_shard,
                "child_state_bit": cbit,
                "first_split_variable_index": first_i,
                "second_split_variable_index": second_i,
                "third_split_variable_index": third_i,
                "third_split_variable_members": list(map(int, self.variables[third_i])),
                "third_split_domain_mask": third_mask,
                "third_split_state_count": len(third_bits),
                "grandchild_shard_index": grandchild_shard,
                "grandchild_state_bit": 0 if grandchild_shard >= len(third_bits) else int(third_bits[grandchild_shard]),
            }
            Counter._last_meta = dict(meta)

            if grandchild_shard >= len(third_bits):
                row = {
                    "model": E.MODEL_LABEL,
                    "domain_state_sum": sum(int(d).bit_count() for d in d2),
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

            d3 = list(d2)
            d3[third_i] = int(third_bits[grandchild_shard])
            return super().count_profile(tuple(d3))

    E.PROFILE_ROWS.clear()
    original_counter = V.AuthorityCorrectConstraintCounter
    V.AuthorityCorrectConstraintCounter = Counter
    try:
        base = V.run_model(len(factors), "all_current_third_level")
    finally:
        V.AuthorityCorrectConstraintCounter = original_counter

    rows = [row for row in E.PROFILE_ROWS if row["model"] == "all_current_third_level"]
    assert len(rows) == 1, rows
    exact = rows[0]
    target_rows = [row for row in base["profile_rows"] if int(row["domain_state_sum"]) == TARGET]
    assert len(target_rows) == 1
    base_mass = int(target_rows[0]["base_mass"])
    assert base_mass == EXPECTED_BASE_MASS
    raw = int(exact["exact_count"])
    assert int(target_rows[0]["m4_pairwise_relaxation_count"]) == raw
    assert raw <= PARENT_REGRESSION_COUNTS[parent_shard]

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "shard": Counter._last_meta,
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
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_THIRD_LEVEL_STATE_SHARD_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("third_level_shard_result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_THIRD_LEVEL_STATE_SHARD_EXACT")
    print("ALPHA_PASS=0")
    return out


def aggregate_child(parent_shard: int, child_shard: int, directory: Path, output: Path) -> dict:
    paths = sorted(directory.glob(f"profile-251-parent-{parent_shard}-child-{child_shard}-grandchild-*.json"))
    assert len(paths) == GRANDCHILD_SHARD_COUNT, [p.name for p in paths]
    rows = [json.loads(p.read_text()) for p in paths]
    by = {int(r["shard"]["grandchild_shard_index"]): r for r in rows}
    assert tuple(sorted(by)) == tuple(range(GRANDCHILD_SHARD_COUNT))
    first = by[0]["shard"]
    keys = (
        "parent_shard_index", "parent_state_bit", "child_shard_index", "child_state_bit",
        "first_split_variable_index", "second_split_variable_index",
        "third_split_variable_index", "third_split_variable_members",
        "third_split_domain_mask", "third_split_state_count",
    )
    for i in range(1, GRANDCHILD_SHARD_COUNT):
        assert all(by[i]["shard"][k] == first[k] for k in keys)
    assert int(first["third_split_state_count"]) <= GRANDCHILD_SHARD_COUNT
    raw = sum(int(by[i]["all_current"]["exact_profile_count"]) for i in range(GRANDCHILD_SHARD_COUNT))
    assert raw <= PARENT_REGRESSION_COUNTS[parent_shard]
    weighted = EXPECTED_BASE_MASS * raw
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "parent_shard_index": parent_shard,
        "child_shard_index": child_shard,
        "exact_all_current_child_profile_count": raw,
        "exact_all_current_child_weighted_summand": weighted,
        "third_split_metadata": {k: first[k] for k in keys},
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_THIRD_LEVEL_CHILD_AGGREGATED_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_THIRD_LEVEL_CHILD_AGGREGATE_EXACT")
    print("ALPHA_PASS=0")
    return out


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("grandchild")
    s.add_argument("--parent-shard", type=int, required=True)
    s.add_argument("--child-shard", type=int, required=True)
    s.add_argument("--grandchild-shard", type=int, required=True)
    s.add_argument("--output", type=Path, required=True)
    a = sub.add_parser("aggregate-child")
    a.add_argument("--parent-shard", type=int, required=True)
    a.add_argument("--child-shard", type=int, required=True)
    a.add_argument("--directory", type=Path, required=True)
    a.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.mode == "grandchild":
        run_grandchild(args.parent_shard, args.child_shard, args.grandchild_shard, args.output)
    else:
        aggregate_child(args.parent_shard, args.child_shard, args.directory, args.output)


if __name__ == "__main__":
    main()
