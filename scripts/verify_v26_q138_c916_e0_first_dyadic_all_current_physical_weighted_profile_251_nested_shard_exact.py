#!/usr/bin/env python3
"""Second-level exact shards for the two unresolved C916 profile-251 state slices.

Run 35118377359 completed first-level shards 0, 2 and 4 exactly.  Shards 1 and 3
completed their six-factor regression slices but exceeded the job ceiling while solving
the all-current model.  This verifier preserves the exact model and partitions only
those two unresolved first-level slices by a second deterministic quotient variable.

The final aggregate reuses the three successful first-level artifacts, requires the
independently frozen first-level regression slices to sum to the exact profile-251
regression authority, and then forms the exact ten-profile all-current weighted total.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

TARGET = 251
CHILD_SHARD_COUNT = 5
PARENTS = (1, 3)
FIRST_SPLIT_VARIABLE_INDEX = 10
FIRST_SPLIT_DOMAIN_MASK = 15
FIRST_SPLIT_BITS = (1, 2, 4, 8)
EXPECTED_BASE_MASS = 243184718013880790060390111206440960000000000

EXPECTED_PARENT_REGRESSION_COUNTS = {
    1: 28992243592121418664980014424454848,
    3: 29213007350957748367629983757192384,
}
EXPECTED_FIRST_LEVEL_REGRESSION_COUNTS = {
    0: 0,
    2: 29433771109794078070279953089929920,
    4: 0,
}
EXPECTED_FIRST_LEVEL_ALL_CURRENT_COUNTS = {
    0: 0,
    2: 25499419387557506549575054803442368,
    4: 0,
}
EXPECTED_PROFILE_REGRESSION_COUNT = 87639022052873245102889951271577152
EXPECTED_PROFILE_REGRESSION_WEIGHTED = 21312470864940260066305006484700721917824185471141115669201479972945920000000000
NINE_PROFILE_ALL_CURRENT_WEIGHTED = 60466057993339377805360951649299438000780926039785945671307235903773039001600000
NINE_PROFILE_REGRESSION_WEIGHTED = 69674719401327202429018678594526911195196718263996709738644727225751919001600000
EXPECTED_SIX_FACTOR_TOTAL = 90987190266267462495323685079227633113020903735137825407846207198697839001600000


def _split_spec(counter, engine, domains):
    candidates = []
    raw = tuple(map(int, domains))
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
    _neg_width, _neg_degree, i = min(candidates)
    full_mask = int(raw[i])
    bits = []
    scan = full_mask
    while scan:
        bit = scan & -scan
        scan ^= bit
        bits.append(bit)
    return i, full_mask, tuple(bits)


def run_child(parent_shard: int, child_shard: int, output: Path) -> dict:
    import _c916_all_current_weighted_context_engine as E
    import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_context_exact as V

    assert parent_shard in PARENTS
    assert 0 <= child_shard < CHILD_SHARD_COUNT
    factors = E.load_factor_specs()
    assert len(factors) == 38

    class NestedCounter(V.AuthorityCorrectConstraintCounter):
        _last_meta = None

        def count_profile(self, domains):
            original = tuple(map(int, domains))
            if sum(int(d).bit_count() for d in original) != TARGET:
                return 1, 0, 0

            first_i, first_mask, first_bits = _split_spec(self, E, original)
            assert first_i == FIRST_SPLIT_VARIABLE_INDEX
            assert first_mask == FIRST_SPLIT_DOMAIN_MASK
            assert first_bits == FIRST_SPLIT_BITS

            parent_bit = int(first_bits[parent_shard])
            parent_domains = list(original)
            parent_domains[first_i] = parent_bit
            parent_domains = tuple(parent_domains)

            second_i, second_mask, second_bits = _split_spec(self, E, parent_domains)
            assert second_i != first_i
            meta = {
                "parent_shard_index": parent_shard,
                "parent_state_bit": parent_bit,
                "first_split_variable_index": first_i,
                "first_split_domain_mask": first_mask,
                "second_split_variable_index": second_i,
                "second_split_variable_members": list(map(int, self.variables[second_i])),
                "second_split_domain_mask": second_mask,
                "second_split_state_count": len(second_bits),
                "child_shard_index": child_shard,
                "child_state_bit": 0 if child_shard >= len(second_bits) else int(second_bits[child_shard]),
            }
            NestedCounter._last_meta = dict(meta)

            if child_shard >= len(second_bits):
                row = {
                    "model": E.MODEL_LABEL,
                    "domain_state_sum": sum(int(d).bit_count() for d in parent_domains),
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

            nd = list(parent_domains)
            nd[second_i] = int(second_bits[child_shard])
            return super().count_profile(tuple(nd))

    E.PROFILE_ROWS.clear()
    original_counter = V.AuthorityCorrectConstraintCounter
    V.AuthorityCorrectConstraintCounter = NestedCounter
    try:
        base = V.run_model(len(factors), "all_current_nested")
    finally:
        V.AuthorityCorrectConstraintCounter = original_counter

    rows = [row for row in E.PROFILE_ROWS if row["model"] == "all_current_nested"]
    assert len(rows) == 1, rows
    exact_row = rows[0]
    target_rows = [
        row for row in base["profile_rows"]
        if int(row["domain_state_sum"]) == TARGET
    ]
    assert len(target_rows) == 1
    base_row = target_rows[0]
    raw = int(exact_row["exact_count"])
    base_mass = int(base_row["base_mass"])
    assert base_mass == EXPECTED_BASE_MASS
    assert int(base_row["m4_pairwise_relaxation_count"]) == raw
    assert raw <= EXPECTED_PARENT_REGRESSION_COUNTS[parent_shard]

    result = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "shard": NestedCounter._last_meta,
        "all_current": {
            "exact_profile_count": raw,
            "exact_weighted_summand": base_mass * raw,
            "base_mass": base_mass,
            "calls_delta": int(exact_row["calls_delta"]),
            "memo_states_delta": int(exact_row["memo_states_delta"]),
            "memo_hits_delta": int(exact_row["memo_hits_delta"]),
            "constraint_eval_hits_delta": int(exact_row["constraint_eval_hits_delta"]),
            "constraint_eval_misses_delta": int(exact_row["constraint_eval_misses_delta"]),
            "max_context_variables": int(exact_row["max_context_variables"]),
        },
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_NESTED_STATE_SHARD_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, sort_keys=True) + "\n")
    print("nested_shard_result", json.dumps(result, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_NESTED_STATE_SHARD_EXACT", flush=True)
    print("ALPHA_PASS=0", flush=True)
    return result


def aggregate(first_level_directory: Path, nested_directory: Path, output: Path) -> dict:
    first_paths = sorted(first_level_directory.glob("profile-251-shard-*.json"))
    first_rows = [json.loads(p.read_text()) for p in first_paths]
    first = {int(row["shard"]["shard_index"]): row for row in first_rows}
    assert tuple(sorted(first)) == (0, 2, 4), tuple(sorted(first))

    for idx in (0, 2, 4):
        row = first[idx]
        assert int(row["shard"]["split_variable_index"]) == FIRST_SPLIT_VARIABLE_INDEX
        assert int(row["shard"]["split_domain_mask"]) == FIRST_SPLIT_DOMAIN_MASK
        assert int(row["regression"]["exact_profile_count"]) == EXPECTED_FIRST_LEVEL_REGRESSION_COUNTS[idx]
        assert int(row["all_current"]["exact_profile_count"]) == EXPECTED_FIRST_LEVEL_ALL_CURRENT_COUNTS[idx]

    nested_paths = sorted(nested_directory.glob("profile-251-parent-*-child-*.json"))
    assert len(nested_paths) == len(PARENTS) * CHILD_SHARD_COUNT, [p.name for p in nested_paths]
    nested_rows = [json.loads(p.read_text()) for p in nested_paths]

    parent_totals = {}
    parent_meta = {}
    for parent in PARENTS:
        rows = [
            row for row in nested_rows
            if int(row["shard"]["parent_shard_index"]) == parent
        ]
        assert len(rows) == CHILD_SHARD_COUNT
        by_child = {int(row["shard"]["child_shard_index"]): row for row in rows}
        assert tuple(sorted(by_child)) == tuple(range(CHILD_SHARD_COUNT))
        m0 = by_child[0]["shard"]
        keys = (
            "parent_state_bit",
            "first_split_variable_index",
            "first_split_domain_mask",
            "second_split_variable_index",
            "second_split_variable_members",
            "second_split_domain_mask",
            "second_split_state_count",
        )
        for row in rows[1:]:
            assert all(row["shard"][k] == m0[k] for k in keys)
        assert int(m0["second_split_state_count"]) <= CHILD_SHARD_COUNT
        total = sum(int(row["all_current"]["exact_profile_count"]) for row in rows)
        assert total <= EXPECTED_PARENT_REGRESSION_COUNTS[parent]
        parent_totals[parent] = total
        parent_meta[parent] = m0

    regression_count = (
        sum(EXPECTED_FIRST_LEVEL_REGRESSION_COUNTS.values())
        + sum(EXPECTED_PARENT_REGRESSION_COUNTS.values())
    )
    assert regression_count == EXPECTED_PROFILE_REGRESSION_COUNT
    assert EXPECTED_BASE_MASS * regression_count == EXPECTED_PROFILE_REGRESSION_WEIGHTED
    assert (
        NINE_PROFILE_REGRESSION_WEIGHTED + EXPECTED_PROFILE_REGRESSION_WEIGHTED
        == EXPECTED_SIX_FACTOR_TOTAL
    )

    all_current_count = (
        sum(EXPECTED_FIRST_LEVEL_ALL_CURRENT_COUNTS.values())
        + sum(parent_totals.values())
    )
    assert all_current_count <= EXPECTED_PROFILE_REGRESSION_COUNT
    profile_weighted = EXPECTED_BASE_MASS * all_current_count
    ten_profile_weighted = NINE_PROFILE_ALL_CURRENT_WEIGHTED + profile_weighted
    assert ten_profile_weighted <= EXPECTED_SIX_FACTOR_TOTAL

    result = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "first_level_source_run_id": 35118377359,
        "first_level_completed_shards": [0, 2, 4],
        "nested_parent_shards": list(PARENTS),
        "nested_parent_totals": {str(k): int(v) for k, v in sorted(parent_totals.items())},
        "nested_parent_split_metadata": {str(k): parent_meta[k] for k in sorted(parent_meta)},
        "six_factor_regression_profile_count": regression_count,
        "six_factor_regression_weighted_summand": EXPECTED_PROFILE_REGRESSION_WEIGHTED,
        "exact_all_current_profile_count": all_current_count,
        "exact_all_current_profile_weighted_summand": profile_weighted,
        "nine_profile_all_current_weighted_sum": NINE_PROFILE_ALL_CURRENT_WEIGHTED,
        "exact_all_current_ten_profile_weighted_count": ten_profile_weighted,
        "exact_all_current_ten_profile_log2": None if ten_profile_weighted == 0 else math.log2(ten_profile_weighted),
        "historical_six_factor_total": EXPECTED_SIX_FACTOR_TOTAL,
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_NESTED_SHARDS_AND_TEN_PROFILE_TOTAL_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, sort_keys=True) + "\n")
    print("result", json.dumps(result, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_NESTED_SHARDS_AGGREGATE_EXACT", flush=True)
    print("boundary=exact for the current 38 ternary plus five quaternary physical quotient inventory and the complete affine/pairwise weighted model; additional untested physical constraints remain possible", flush=True)
    print("ALPHA_PASS=0", flush=True)
    return result


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("child")
    s.add_argument("--parent-shard", type=int, required=True)
    s.add_argument("--child-shard", type=int, required=True)
    s.add_argument("--output", type=Path, required=True)
    a = sub.add_parser("aggregate")
    a.add_argument("--first-level-directory", type=Path, required=True)
    a.add_argument("--nested-directory", type=Path, required=True)
    a.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.mode == "child":
        run_child(args.parent_shard, args.child_shard, args.output)
    else:
        aggregate(args.first_level_directory, args.nested_directory, args.output)


if __name__ == "__main__":
    main()
