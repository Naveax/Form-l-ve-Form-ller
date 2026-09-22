#!/usr/bin/env python3
"""Generic exact adaptive path sharder for C916 weighted profile 251.

This is a performance-only representation of the same frozen 38-ternary weighted model.
A shard path is a sequence of singleton-state indices chosen by repeatedly applying the
same deterministic pairwise-only split heuristic. Because every split partitions one
current domain into disjoint singleton states, siblings are disjoint and their union is
exactly the parent shard.

Example:
  --path 1,3,1 --next-shard 2
reconstructs deterministic splits 0..2 with state indices (1,3,1), then fixes the next
split to state index 2 and counts that exact child. The same tool works at arbitrary
depth, so a child that still reaches the runner ceiling can be split again without a new
mathematical implementation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TARGET = 251
EXPECTED_BASE_MASS = 243184718013880790060390111206440960000000000
EXPECTED_PROFILE_REGRESSION_COUNT = 87639022052873245102889951271577152
MAX_SHARD_COUNT = 5


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


def parse_path(text: str):
    text = text.strip()
    if not text:
        return ()
    out = tuple(int(x) for x in text.split(","))
    assert all(x >= 0 for x in out)
    return out


def run_child(path_indices, next_shard: int, output: Path):
    import _c916_all_current_weighted_context_engine as E
    import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_context_exact as V

    path_indices = tuple(map(int, path_indices))
    assert 0 <= next_shard < MAX_SHARD_COUNT
    factors = E.load_factor_specs()
    assert len(factors) == 38

    class Counter(V.AuthorityCorrectConstraintCounter):
        _meta = None

        def count_profile(self, domains):
            original = tuple(map(int, domains))
            if sum(int(d).bit_count() for d in original) != TARGET:
                return 1, 0, 0

            current = original
            steps = []
            for depth, state_index in enumerate(path_indices):
                vi, full_mask, bits = split_spec(self, E, current)
                assert 0 <= state_index < len(bits), (depth, state_index, bits)
                bit = int(bits[state_index])
                steps.append({
                    "depth": depth,
                    "variable_index": vi,
                    "variable_members": list(map(int, self.variables[vi])),
                    "domain_mask": int(full_mask),
                    "state_count": len(bits),
                    "state_index": state_index,
                    "state_bit": bit,
                })
                nxt = list(current)
                nxt[vi] = bit
                current = tuple(nxt)

            vi, full_mask, bits = split_spec(self, E, current)
            child_bit = 0 if next_shard >= len(bits) else int(bits[next_shard])
            next_meta = {
                "depth": len(path_indices),
                "variable_index": vi,
                "variable_members": list(map(int, self.variables[vi])),
                "domain_mask": int(full_mask),
                "state_count": len(bits),
                "state_index": next_shard,
                "state_bit": child_bit,
            }
            Counter._meta = {
                "path_indices": list(path_indices),
                "path_steps": steps,
                "next_split": next_meta,
            }

            if next_shard >= len(bits):
                row = {
                    "model": E.MODEL_LABEL,
                    "domain_state_sum": sum(int(d).bit_count() for d in current),
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

            nxt = list(current)
            nxt[vi] = child_bit
            return super().count_profile(tuple(nxt))

    E.PROFILE_ROWS.clear()
    original_counter = V.AuthorityCorrectConstraintCounter
    V.AuthorityCorrectConstraintCounter = Counter
    try:
        base = V.run_model(len(factors), "all_current_adaptive_path")
    finally:
        V.AuthorityCorrectConstraintCounter = original_counter

    rows = [r for r in E.PROFILE_ROWS if r["model"] == "all_current_adaptive_path"]
    assert len(rows) == 1, rows
    exact = rows[0]
    target_rows = [r for r in base["profile_rows"] if int(r["domain_state_sum"]) == TARGET]
    assert len(target_rows) == 1
    base_row = target_rows[0]
    assert int(base_row["base_mass"]) == EXPECTED_BASE_MASS
    raw = int(exact["exact_count"])
    assert int(base_row["m4_pairwise_relaxation_count"]) == raw
    assert 0 <= raw <= EXPECTED_PROFILE_REGRESSION_COUNT

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "shard": Counter._meta,
        "all_current": {
            "exact_profile_count": raw,
            "exact_weighted_summand": EXPECTED_BASE_MASS * raw,
            "base_mass": EXPECTED_BASE_MASS,
            "calls_delta": int(exact["calls_delta"]),
            "memo_states_delta": int(exact["memo_states_delta"]),
            "memo_hits_delta": int(exact["memo_hits_delta"]),
            "constraint_eval_hits_delta": int(exact["constraint_eval_hits_delta"]),
            "constraint_eval_misses_delta": int(exact["constraint_eval_misses_delta"]),
            "max_context_variables": int(exact["max_context_variables"]),
        },
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_ADAPTIVE_PATH_CHILD_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("adaptive_shard_result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_ADAPTIVE_PATH_CHILD_EXACT")
    print("ALPHA_PASS=0")
    return out


def aggregate(path_indices, directory: Path, output: Path):
    path_indices = tuple(map(int, path_indices))
    prefix = "-".join(map(str, path_indices)) if path_indices else "root"
    paths = sorted(directory.glob(f"profile-251-path-{prefix}-child-*.json"))
    assert len(paths) == MAX_SHARD_COUNT, [p.name for p in paths]
    rows = [json.loads(p.read_text()) for p in paths]
    by_child = {int(r["shard"]["next_split"]["state_index"]): r for r in rows}
    assert tuple(sorted(by_child)) == tuple(range(MAX_SHARD_COUNT))

    first = by_child[0]["shard"]
    shared_keys = ("path_indices", "path_steps")
    for i in range(1, MAX_SHARD_COUNT):
        row = by_child[i]["shard"]
        assert all(row[k] == first[k] for k in shared_keys)
        for k in ("variable_index", "variable_members", "domain_mask", "state_count"):
            assert row["next_split"][k] == first["next_split"][k]

    assert tuple(map(int, first["path_indices"])) == path_indices
    state_count = int(first["next_split"]["state_count"])
    assert 1 <= state_count <= MAX_SHARD_COUNT
    for i in range(state_count):
        assert int(by_child[i]["shard"]["next_split"]["state_bit"]) > 0
    for i in range(state_count, MAX_SHARD_COUNT):
        assert int(by_child[i]["shard"]["next_split"]["state_bit"]) == 0
        assert int(by_child[i]["all_current"]["exact_profile_count"]) == 0

    raw = sum(int(by_child[i]["all_current"]["exact_profile_count"]) for i in range(MAX_SHARD_COUNT))
    weighted = sum(int(by_child[i]["all_current"]["exact_weighted_summand"]) for i in range(MAX_SHARD_COUNT))
    assert weighted == EXPECTED_BASE_MASS * raw
    assert raw <= EXPECTED_PROFILE_REGRESSION_COUNT

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "path_indices": list(path_indices),
        "next_split_variable_index": int(first["next_split"]["variable_index"]),
        "next_split_variable_members": first["next_split"]["variable_members"],
        "next_split_domain_mask": int(first["next_split"]["domain_mask"]),
        "next_split_state_count": state_count,
        "exact_parent_profile_count": raw,
        "exact_parent_weighted_summand": weighted,
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_ADAPTIVE_PATH_PARENT_AGGREGATED_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_ADAPTIVE_PATH_PARENT_AGGREGATE_EXACT")
    print("ALPHA_PASS=0")
    return out


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)

    s = sub.add_parser("child")
    s.add_argument("--path", default="")
    s.add_argument("--next-shard", type=int, required=True)
    s.add_argument("--output", type=Path, required=True)

    a = sub.add_parser("aggregate")
    a.add_argument("--path", default="")
    a.add_argument("--directory", type=Path, required=True)
    a.add_argument("--output", type=Path, required=True)

    args = p.parse_args()
    path_indices = parse_path(args.path)
    if args.mode == "child":
        run_child(path_indices, args.next_shard, args.output)
    else:
        aggregate(path_indices, args.directory, args.output)


if __name__ == "__main__":
    main()
