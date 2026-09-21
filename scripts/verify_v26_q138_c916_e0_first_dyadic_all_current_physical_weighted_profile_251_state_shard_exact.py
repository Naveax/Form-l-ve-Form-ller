#!/usr/bin/env python3
"""Exact state-sharded fallback for the C916 domain-state-sum 251 profile.

This does not change the mathematical model. It partitions the profile by the quotient
state of one deterministic variable and solves each disjoint state slice independently.
The split variable is selected from the unmodified profile domains by largest domain,
then largest pairwise-only relevant degree, then variable index. Pairwise-only degree is
used so the same partition is chosen by the six-factor regression and all-current models.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TARGET = 251
SHARD_COUNT = 5
EXPECTED_REGRESSION_PROFILE_COUNT = 87639022052873245102889951271577152
EXPECTED_BASE_MASS = 243184718013880790060390111206440960000000000
EXPECTED_REGRESSION_WEIGHTED = 21312470864940260066305006484700721917824185471141115669201479972945920000000000


def run_shard(shard_index: int, output: Path) -> dict:
    import _c916_all_current_weighted_context_engine as E
    import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_context_exact as V

    assert 0 <= shard_index < SHARD_COUNT
    factors = E.load_factor_specs()
    assert len(factors) == 38

    class TargetShardCounter(V.AuthorityCorrectConstraintCounter):
        def _split_spec(self, domains):
            candidates = []
            raw = tuple(map(int, domains))
            for i, mask in enumerate(raw):
                if len(self.variables[i]) != 1:
                    continue
                width = int(mask).bit_count()
                if width <= 1:
                    continue
                # Stable across the regression and all-current models: ignore higher-order
                # neighbors when choosing the partition variable.
                pair_neighbors = E.PAIRWISE_COUNTER._relevant_neighbors(self, i, self.ALL, raw)
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

        def count_profile(self, domains):
            dsum = sum(int(d).bit_count() for d in domains)
            if dsum != TARGET:
                return 1, 0, 0

            split_i, split_mask, bits = self._split_spec(domains)
            self._c916_split_meta = {
                "split_variable_index": split_i,
                "split_variable_members": list(map(int, self.variables[split_i])),
                "split_domain_mask": split_mask,
                "split_state_count": len(bits),
                "shard_index": shard_index,
                "shard_state_bit": 0 if shard_index >= len(bits) else int(bits[shard_index]),
            }
            if shard_index >= len(bits):
                row = {
                    "model": E.MODEL_LABEL,
                    "domain_state_sum": TARGET,
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

            nd = list(map(int, domains))
            nd[split_i] = int(bits[shard_index])
            return super().count_profile(tuple(nd))

    def run_one(limit: int, label: str) -> dict:
        E.PROFILE_ROWS.clear()
        original = V.AuthorityCorrectConstraintCounter
        V.AuthorityCorrectConstraintCounter = TargetShardCounter
        try:
            base = V.run_model(limit, label)
        finally:
            V.AuthorityCorrectConstraintCounter = original

        rows = [row for row in E.PROFILE_ROWS if row["model"] == label]
        assert len(rows) == 1, (label, rows)
        exact_row = rows[0]
        base_rows = list(base["profile_rows"])
        target_rows = [row for row in base_rows if int(row["domain_state_sum"]) == TARGET]
        assert len(target_rows) == 1
        base_row = target_rows[0]
        raw = int(exact_row["exact_count"])
        base_mass = int(base_row["base_mass"])
        assert base_mass == EXPECTED_BASE_MASS
        assert int(base_row["m4_pairwise_relaxation_count"]) == raw

        return {
            "label": label,
            "exact_profile_count": raw,
            "exact_weighted_summand": base_mass * raw,
            "base_mass": base_mass,
            "calls_delta": int(exact_row["calls_delta"]),
            "memo_states_delta": int(exact_row["memo_states_delta"]),
            "memo_hits_delta": int(exact_row["memo_hits_delta"]),
            "constraint_eval_hits_delta": int(exact_row["constraint_eval_hits_delta"]),
            "constraint_eval_misses_delta": int(exact_row["constraint_eval_misses_delta"]),
            "max_context_variables": int(exact_row["max_context_variables"]),
        }

    # The subclass instance is not returned by the legacy driver, so record split metadata
    # through a class-level hook populated by count_profile.
    TargetShardCounter._last_split_meta = None
    original_count = TargetShardCounter.count_profile

    def hooked_count(self, domains):
        out = original_count(self, domains)
        if sum(int(d).bit_count() for d in domains) == TARGET:
            TargetShardCounter._last_split_meta = dict(self._c916_split_meta)
        return out

    TargetShardCounter.count_profile = hooked_count

    regression = run_one(6, "six_factor_regression")
    regression_split = dict(TargetShardCounter._last_split_meta)
    full = run_one(len(factors), "all_current")
    full_split = dict(TargetShardCounter._last_split_meta)
    assert regression_split == full_split, (regression_split, full_split)
    assert int(full["exact_profile_count"]) <= int(regression["exact_profile_count"])

    result = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "shard": regression_split,
        "regression": regression,
        "all_current": full,
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_STATE_SHARD_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, sort_keys=True) + "\n")
    print("shard_result", json.dumps(result, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_STATE_SHARD_EXACT", flush=True)
    print("ALPHA_PASS=0", flush=True)
    return result


def aggregate(directory: Path, output: Path) -> dict:
    paths = sorted(directory.glob("profile-251-shard-*.json"))
    assert len(paths) == SHARD_COUNT, [p.name for p in paths]
    rows = [json.loads(p.read_text()) for p in paths]
    by_shard = {int(row["shard"]["shard_index"]): row for row in rows}
    assert tuple(sorted(by_shard)) == tuple(range(SHARD_COUNT))

    split_keys = ("split_variable_index", "split_variable_members", "split_domain_mask", "split_state_count")
    first = rows[0]["shard"]
    for row in rows[1:]:
        assert all(row["shard"][k] == first[k] for k in split_keys)
    assert int(first["split_state_count"]) <= SHARD_COUNT

    regression_count = sum(int(row["regression"]["exact_profile_count"]) for row in rows)
    regression_weighted = sum(int(row["regression"]["exact_weighted_summand"]) for row in rows)
    all_current_count = sum(int(row["all_current"]["exact_profile_count"]) for row in rows)
    all_current_weighted = sum(int(row["all_current"]["exact_weighted_summand"]) for row in rows)
    assert regression_count == EXPECTED_REGRESSION_PROFILE_COUNT
    assert regression_weighted == EXPECTED_REGRESSION_WEIGHTED
    assert all_current_count <= regression_count
    assert all_current_weighted == EXPECTED_BASE_MASS * all_current_count

    result = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "split_variable_index": first["split_variable_index"],
        "split_variable_members": first["split_variable_members"],
        "split_domain_mask": first["split_domain_mask"],
        "split_state_count": first["split_state_count"],
        "six_factor_regression_profile_count": regression_count,
        "six_factor_regression_weighted_summand": regression_weighted,
        "exact_all_current_profile_count": all_current_count,
        "exact_all_current_weighted_summand": all_current_weighted,
        "shards": [by_shard[i] for i in range(SHARD_COUNT)],
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_STATE_SHARDS_AGGREGATED_EXACT",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, sort_keys=True) + "\n")
    print("result", json.dumps(result, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_STATE_SHARDS_AGGREGATE_EXACT", flush=True)
    print("ALPHA_PASS=0", flush=True)
    return result


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)
    s = sub.add_parser("shard")
    s.add_argument("--shard-index", type=int, required=True)
    s.add_argument("--output", type=Path, required=True)
    a = sub.add_parser("aggregate")
    a.add_argument("--directory", type=Path, required=True)
    a.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.mode == "shard":
        run_shard(args.shard_index, args.output)
    else:
        aggregate(args.directory, args.output)


if __name__ == "__main__":
    main()
