#!/usr/bin/env python3
"""Exact mixed-depth fan-in for the frozen C916 weighted profile 251.

Purpose: a workflow matrix can end with some heavy third-level grandchildren successful
and others failed/timed out. GitHub then skips a normal needs-based aggregate. This
verifier accepts the successful direct artifacts and exact adaptive-path aggregate
artifacts only for the missing grandchildren, proves that every disjoint partition cell
is covered exactly once, reproduces the frozen six-factor profile regression authority,
and emits the exact profile-251 plus ten-profile all-current weighted total.

No leaf is counted twice. A heavy path (parent, child, grandchild) must be represented by
exactly one of:
  1. its direct third-level artifact, or
  2. one adaptive-path aggregate whose path_indices equal that exact triple.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

TARGET = 251
BASE_MASS = 243184718013880790060390111206440960000000000

EXPECTED_PROFILE_REGRESSION_COUNT = 87639022052873245102889951271577152
EXPECTED_PROFILE_REGRESSION_WEIGHTED = 21312470864940260066305006484700721917824185471141115669201479972945920000000000
EXPECTED_SIX_FACTOR_TOTAL = 90987190266267462495323685079227633113020903735137825407846207198697839001600000
NINE_PROFILE_ALL_CURRENT_WEIGHTED = 60466057993339377805360951649299438000780926039785945671307235903773039001600000
NINE_PROFILE_REGRESSION_WEIGHTED = 69674719401327202429018678594526911195196718263996709738644727225751919001600000

EXPECTED_FIRST_LEVEL = {
    0: {"regression": 0, "all_current": 0},
    2: {"regression": 29433771109794078070279953089929920, "all_current": 25499419387557506549575054803442368},
    4: {"regression": 0, "all_current": 0},
}
EXPECTED_PARENT_REGRESSION = {
    1: 28992243592121418664980014424454848,
    3: 29213007350957748367629983757192384,
}
EXPECTED_NESTED_SUCCESS = {
    (1, 0): 0,
    (1, 2): 0,
    (1, 4): 0,
    (3, 0): 0,
    (3, 2): 8499806462519168849858351601147456,
    (3, 4): 0,
}
HEAVY_PAIRS = ((1, 1), (1, 3), (3, 1), (3, 3))
GRANDCHILDREN = (0, 1, 2, 3)


def load_first_level(directory: Path):
    rows = {}
    for path in sorted(directory.glob("profile-251-shard-*.json")):
        row = json.loads(path.read_text())
        idx = int(row["shard"]["shard_index"])
        if idx in EXPECTED_FIRST_LEVEL:
            rows[idx] = row
    assert tuple(sorted(rows)) == tuple(sorted(EXPECTED_FIRST_LEVEL))

    for idx, expected in EXPECTED_FIRST_LEVEL.items():
        row = rows[idx]
        assert int(row["regression"]["base_mass"]) == BASE_MASS
        assert int(row["all_current"]["base_mass"]) == BASE_MASS
        assert int(row["regression"]["exact_profile_count"]) == expected["regression"]
        assert int(row["all_current"]["exact_profile_count"]) == expected["all_current"]
    return rows


def load_nested(directory: Path):
    rows = {}
    for path in sorted(directory.glob("profile-251-parent-*-child-*.json")):
        row = json.loads(path.read_text())
        key = (
            int(row["shard"]["parent_shard_index"]),
            int(row["shard"]["child_shard_index"]),
        )
        if key in EXPECTED_NESTED_SUCCESS:
            rows[key] = row

    assert tuple(sorted(rows)) == tuple(sorted(EXPECTED_NESTED_SUCCESS))
    for key, expected in EXPECTED_NESTED_SUCCESS.items():
        row = rows[key]
        assert int(row["all_current"]["base_mass"]) == BASE_MASS
        assert int(row["all_current"]["exact_profile_count"]) == expected
    return rows


def load_direct_third(directory: Path):
    rows = {}
    for path in sorted(directory.glob("profile-251-parent-*-child-*-grandchild-*.json")):
        row = json.loads(path.read_text())
        key = (
            int(row["shard"]["parent_shard_index"]),
            int(row["shard"]["child_shard_index"]),
            int(row["shard"]["grandchild_shard_index"]),
        )
        if key[:2] not in HEAVY_PAIRS or key[2] not in GRANDCHILDREN:
            continue
        assert key not in rows, key
        assert int(row["all_current"]["base_mass"]) == BASE_MASS
        rows[key] = row
    return rows


def load_adaptive(directory: Path):
    rows = {}
    for path in sorted(directory.glob("profile-251-path-*-aggregate.json")):
        row = json.loads(path.read_text())
        indices = tuple(map(int, row["path_indices"]))
        if len(indices) != 3:
            continue
        key = indices
        if key[:2] not in HEAVY_PAIRS or key[2] not in GRANDCHILDREN:
            continue
        assert key not in rows, key
        raw = int(row["exact_parent_profile_count"])
        weighted = int(row["exact_parent_weighted_summand"])
        assert weighted == BASE_MASS * raw
        rows[key] = row
    return rows


def analyze(first_level_directory: Path, nested_directory: Path, direct_third_directory: Path, adaptive_directory: Path, output: Path):
    first = load_first_level(first_level_directory)
    nested = load_nested(nested_directory)
    direct = load_direct_third(direct_third_directory)
    adaptive = load_adaptive(adaptive_directory)

    heavy_counts = {}
    source_rows = []
    for p, c in HEAVY_PAIRS:
        for g in GRANDCHILDREN:
            key = (p, c, g)
            has_direct = key in direct
            has_adaptive = key in adaptive
            assert has_direct ^ has_adaptive, (
                "heavy cell must have exactly one source",
                key,
                has_direct,
                has_adaptive,
            )
            if has_direct:
                raw = int(direct[key]["all_current"]["exact_profile_count"])
                weighted = int(direct[key]["all_current"]["exact_weighted_summand"])
                assert weighted == BASE_MASS * raw
                source = "direct_third_level"
            else:
                raw = int(adaptive[key]["exact_parent_profile_count"])
                weighted = int(adaptive[key]["exact_parent_weighted_summand"])
                assert weighted == BASE_MASS * raw
                source = "adaptive_path_aggregate"

            assert 0 <= raw <= EXPECTED_PARENT_REGRESSION[p]
            heavy_counts[key] = raw
            source_rows.append({
                "path": list(key),
                "source": source,
                "exact_profile_count": raw,
                "exact_weighted_summand": weighted,
            })

    regression_count = (
        sum(v["regression"] for v in EXPECTED_FIRST_LEVEL.values())
        + EXPECTED_PARENT_REGRESSION[1]
        + EXPECTED_PARENT_REGRESSION[3]
    )
    assert regression_count == EXPECTED_PROFILE_REGRESSION_COUNT
    assert BASE_MASS * regression_count == EXPECTED_PROFILE_REGRESSION_WEIGHTED
    assert (
        NINE_PROFILE_REGRESSION_WEIGHTED + EXPECTED_PROFILE_REGRESSION_WEIGHTED
        == EXPECTED_SIX_FACTOR_TOTAL
    )

    profile251_count = (
        sum(v["all_current"] for v in EXPECTED_FIRST_LEVEL.values())
        + sum(EXPECTED_NESTED_SUCCESS.values())
        + sum(heavy_counts.values())
    )
    assert 0 <= profile251_count <= EXPECTED_PROFILE_REGRESSION_COUNT

    profile251_weighted = BASE_MASS * profile251_count
    total = NINE_PROFILE_ALL_CURRENT_WEIGHTED + profile251_weighted
    assert 0 <= total <= EXPECTED_SIX_FACTOR_TOTAL

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": TARGET,
        "partition_coverage": {
            "first_level_terminal_shards": sorted(EXPECTED_FIRST_LEVEL),
            "nested_terminal_cells": [list(k) for k in sorted(EXPECTED_NESTED_SUCCESS)],
            "heavy_third_level_cells": len(heavy_counts),
            "heavy_cells_from_direct_third_level": sum(1 for r in source_rows if r["source"] == "direct_third_level"),
            "heavy_cells_from_adaptive_fallback": sum(1 for r in source_rows if r["source"] == "adaptive_path_aggregate"),
        },
        "heavy_cell_sources": source_rows,
        "six_factor_regression_profile_count": regression_count,
        "six_factor_regression_weighted_summand": EXPECTED_PROFILE_REGRESSION_WEIGHTED,
        "exact_all_current_profile_count": profile251_count,
        "exact_all_current_profile_weighted_summand": profile251_weighted,
        "nine_profile_all_current_weighted_sum": NINE_PROFILE_ALL_CURRENT_WEIGHTED,
        "exact_all_current_ten_profile_weighted_count": total,
        "exact_all_current_ten_profile_log2": None if total == 0 else math.log2(total),
        "historical_six_factor_total": EXPECTED_SIX_FACTOR_TOTAL,
        "decision": "C916_ALL_CURRENT_WEIGHTED_PROFILE_251_MIXED_DEPTH_EXACT_FANIN",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PROFILE_251_MIXED_DEPTH_FINAL_EXACT")
    print("boundary=exact for the frozen 38-ternary physical inventory plus complete affine, quaternary, pairwise, and multiplicity model; later tail3/tail4/tail5 factors are not included")
    print("ALPHA_PASS=0")
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--first-level-directory", type=Path, required=True)
    p.add_argument("--nested-directory", type=Path, required=True)
    p.add_argument("--direct-third-directory", type=Path, required=True)
    p.add_argument("--adaptive-directory", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    analyze(
        args.first_level_directory,
        args.nested_directory,
        args.direct_third_directory,
        args.adaptive_directory,
        args.output,
    )


if __name__ == "__main__":
    main()
