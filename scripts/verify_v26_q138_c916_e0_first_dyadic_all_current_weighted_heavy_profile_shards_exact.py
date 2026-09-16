#!/usr/bin/env python3
"""Exact fallback sharding for one heavy C916 all-current separator profile.

This tool is deliberately workflow-free until the profile-matrix authority demonstrates
that a heavy profile still exceeds one runner. It partitions one target profile into a
deterministic tree of disjoint exact domain restrictions. Every leaf is counted by the
same authority-correct 4,005-pair + 19-affine + five-quaternary + 38-ternary weighted
counter. Summing all leaf counts therefore reproduces the unsplit target profile exactly.

No approximation, sampling, beam pruning, or post-hoc truncation is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

TARGET_DOMAIN_STATE_SUMS = (251, 288, 302)
CAPTURE = {}


def stable_digest(obj) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def _choose_split(counter, domains):
    """Match the exact counter's deterministic branch-variable heuristic."""
    best = None
    active = counter.ALL
    scan = active
    while scan:
        bit = scan & -scan
        i = bit.bit_length() - 1
        scan ^= bit
        width = int(domains[i]).bit_count()
        if width <= 1:
            continue
        neighbors = counter._relevant_neighbors(i, active, domains)
        score = (width, -neighbors.bit_count(), i)
        if best is None or score < best[0]:
            best = (score, i)
    return None if best is None else best[1]


def _split_leaves(counter, domains, depth):
    """Return deterministic disjoint closed-domain leaves after `depth` exact splits."""
    root = counter._arc_closure(counter.ALL, tuple(map(int, domains)))
    if root is None:
        return []

    leaves = [((), root)]
    for _level in range(int(depth)):
        next_leaves = []
        for path, current in leaves:
            closed = counter._arc_closure(counter.ALL, current)
            if closed is None:
                continue
            i = _choose_split(counter, closed)
            if i is None:
                next_leaves.append((path, closed))
                continue
            mask = int(closed[i])
            while mask:
                bit = mask & -mask
                mask ^= bit
                state = bit.bit_length() - 1
                child = list(closed)
                child[i] = bit
                child_closed = counter._arc_closure(counter.ALL, tuple(child))
                if child_closed is None:
                    continue
                next_leaves.append((path + ((i, state),), child_closed))
        leaves = next_leaves
        if not leaves:
            break
    return leaves


def _manifest_rows(leaves):
    rows = []
    for index, (path, domains) in enumerate(leaves):
        rows.append(
            {
                "shard_index": index,
                "path": [list(row) for row in path],
                "domain_state_sum": sum(int(mask).bit_count() for mask in domains),
                "domains_sha256": stable_digest(list(map(int, domains))),
            }
        )
    return rows


def _run_driver(target, split_depth, shard_index):
    import _c916_all_current_weighted_context_engine as E
    import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_weighted_context_exact as V

    assert target in TARGET_DOMAIN_STATE_SUMS
    factors = E.load_factor_specs()
    assert len(factors) == len(E.TOPO.TERNARY_FACTORS) == 38
    CAPTURE.clear()

    class ShardCounter(V.AuthorityCorrectConstraintCounter):
        def count_profile(self, domains):
            dsum = sum(int(d).bit_count() for d in domains)
            if dsum != target:
                return 1, 0, 0

            self.memo.clear()
            leaves = _split_leaves(self, domains, split_depth)
            manifest = _manifest_rows(leaves)
            manifest_digest = stable_digest(manifest)
            CAPTURE["manifest"] = manifest
            CAPTURE["manifest_digest"] = manifest_digest

            if shard_index is None:
                CAPTURE["raw_count"] = None
                return 1, 0, 0

            assert 0 <= shard_index < len(leaves), (shard_index, len(leaves))
            path, shard_domains = leaves[shard_index]
            calls_before = self.calls
            memo_before = len(self.memo)
            raw = int(self.solve(self.ALL, shard_domains))
            CAPTURE["raw_count"] = raw
            CAPTURE["path"] = path
            CAPTURE["calls_delta"] = self.calls - calls_before
            CAPTURE["memo_states_delta"] = len(self.memo) - memo_before
            CAPTURE["memo_states_total"] = len(self.memo)
            return raw, CAPTURE["calls_delta"], CAPTURE["memo_states_total"]

    original = V.AuthorityCorrectConstraintCounter
    V.AuthorityCorrectConstraintCounter = ShardCounter
    E.PROFILE_ROWS.clear()
    try:
        base = V.run_model(len(factors), "all_current_shard")
    finally:
        V.AuthorityCorrectConstraintCounter = original

    target_rows = [row for row in base["profile_rows"] if int(row["domain_state_sum"]) == target]
    assert len(target_rows) == 1
    target_row = target_rows[0]
    base_mass = int(target_row["base_mass"])

    dummy_background = 0
    for row in base["profile_rows"]:
        dsum = int(row["domain_state_sum"])
        if dsum == target:
            continue
        assert int(row["m4_pairwise_relaxation_count"]) == 1, (dsum, row)
        dummy_background += int(row["base_mass"])

    if shard_index is None:
        assert int(target_row["m4_pairwise_relaxation_count"]) == 1
        assert int(base["exact_count"]) == dummy_background + base_mass
    else:
        raw = int(CAPTURE["raw_count"])
        assert int(target_row["m4_pairwise_relaxation_count"]) == raw
        assert int(base["exact_count"]) == dummy_background + base_mass * raw

    return base_mass


def write_manifest(target, split_depth, output):
    base_mass = _run_driver(target, split_depth, None)
    manifest = list(CAPTURE["manifest"])
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": target,
        "split_depth": split_depth,
        "base_mass": base_mass,
        "leaf_count": len(manifest),
        "manifest_digest_sha256": CAPTURE["manifest_digest"],
        "shards": manifest,
        "decision": "C916_ALL_CURRENT_WEIGHTED_HEAVY_PROFILE_EXACT_SHARD_MANIFEST",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("manifest", json.dumps(out, sort_keys=True), flush=True)
    print("ALPHA_PASS=0", flush=True)


def run_shard(target, split_depth, shard_index, output):
    base_mass = _run_driver(target, split_depth, shard_index)
    manifest = list(CAPTURE["manifest"])
    row = manifest[shard_index]
    raw = int(CAPTURE["raw_count"])
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": target,
        "split_depth": split_depth,
        "manifest_digest_sha256": CAPTURE["manifest_digest"],
        "leaf_count": len(manifest),
        "shard_index": shard_index,
        "path": row["path"],
        "domains_sha256": row["domains_sha256"],
        "base_mass": base_mass,
        "exact_profile_shard_count": raw,
        "exact_weighted_shard_summand": base_mass * raw,
        "calls_delta": int(CAPTURE["calls_delta"]),
        "memo_states_delta": int(CAPTURE["memo_states_delta"]),
        "memo_states_total": int(CAPTURE["memo_states_total"]),
        "decision": "C916_ALL_CURRENT_WEIGHTED_HEAVY_PROFILE_EXACT_SHARD",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("shard_result", json.dumps(out, sort_keys=True), flush=True)
    print("ALPHA_PASS=0", flush=True)


def aggregate(manifest_path, directory, output):
    manifest = json.loads(manifest_path.read_text())
    target = int(manifest["domain_state_sum"])
    split_depth = int(manifest["split_depth"])
    digest = str(manifest["manifest_digest_sha256"])
    leaf_count = int(manifest["leaf_count"])
    assert leaf_count == len(manifest["shards"])

    rows = []
    for path in sorted(directory.glob("shard-*.json")):
        row = json.loads(path.read_text())
        if int(row["domain_state_sum"]) == target and int(row["split_depth"]) == split_depth:
            rows.append(row)
    assert len(rows) == leaf_count, (len(rows), leaf_count)

    by_index = {int(row["shard_index"]): row for row in rows}
    assert set(by_index) == set(range(leaf_count))
    assert len(by_index) == len(rows)

    raw_total = 0
    weighted_total = 0
    base_mass = int(manifest["base_mass"])
    for index in range(leaf_count):
        row = by_index[index]
        expected = manifest["shards"][index]
        assert row["manifest_digest_sha256"] == digest
        assert int(row["base_mass"]) == base_mass
        assert row["path"] == expected["path"]
        assert row["domains_sha256"] == expected["domains_sha256"]
        raw = int(row["exact_profile_shard_count"])
        weighted = int(row["exact_weighted_shard_summand"])
        assert weighted == base_mass * raw
        raw_total += raw
        weighted_total += weighted

    assert weighted_total == base_mass * raw_total
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "domain_state_sum": target,
        "split_depth": split_depth,
        "manifest_digest_sha256": digest,
        "leaf_count": leaf_count,
        "base_mass": base_mass,
        "exact_all_current_profile_count": raw_total,
        "exact_all_current_weighted_summand": weighted_total,
        "decision": "C916_ALL_CURRENT_WEIGHTED_HEAVY_PROFILE_EXACT_SHARDS_AGGREGATED",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(out, sort_keys=True) + "\n")
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_CURRENT_WEIGHTED_HEAVY_PROFILE_SHARDS_EXACT", flush=True)
    print("boundary=exact fallback execution decomposition only; no end-to-end work exponent is inferred", flush=True)
    print("ALPHA_PASS=0", flush=True)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode", required=True)
    p = sub.add_parser("manifest")
    p.add_argument("--domain-state-sum", type=int, required=True, choices=TARGET_DOMAIN_STATE_SUMS)
    p.add_argument("--split-depth", type=int, required=True)
    p.add_argument("--output", type=Path, required=True)
    s = sub.add_parser("shard")
    s.add_argument("--domain-state-sum", type=int, required=True, choices=TARGET_DOMAIN_STATE_SUMS)
    s.add_argument("--split-depth", type=int, required=True)
    s.add_argument("--shard-index", type=int, required=True)
    s.add_argument("--output", type=Path, required=True)
    a = sub.add_parser("aggregate")
    a.add_argument("--manifest", type=Path, required=True)
    a.add_argument("--directory", type=Path, required=True)
    a.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "manifest":
        assert args.split_depth >= 1
        write_manifest(args.domain_state_sum, args.split_depth, args.output)
    elif args.mode == "shard":
        assert args.split_depth >= 1
        run_shard(args.domain_state_sum, args.split_depth, args.shard_index, args.output)
    else:
        aggregate(args.manifest, args.directory, args.output)


if __name__ == "__main__":
    main()
