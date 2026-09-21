#!/usr/bin/env python3
"""Aggregate exact tail6 quotient results against the certified inventory through tail5.

The current inventory is reconstructed from frozen + tail3 + tail4 scopes and the clean
tail5 target artifacts. This avoids hardcoding the still-running tail5 promoted set in a
future tail6 verifier.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_treewidth8_exact as T4
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as S

TAIL5_DIR = Path(os.environ.get("C916_TAIL5_QUOTIENT_DIR", "authorities/tail5-quotient"))
TAIL6_DIR = Path(os.environ.get("C916_TAIL6_QUOTIENT_DIR", "tail6-quotient-summaries"))


def digest_scopes(triples, quads):
    payload = json.dumps(
        {
            "quads": [list(x) for x in sorted(quads)],
            "triples": [list(x) for x in sorted(triples)],
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def load_promoted(directory: Path, prefix: str, target_key: str):
    files = sorted(directory.glob(f"{prefix}_*.json"))
    assert len(files) == 16, (directory, [p.name for p in files])
    rows = [json.loads(p.read_text()) for p in files]
    by = {int(row[target_key]): row for row in rows}
    assert set(by) == set(range(16))
    promoted = []
    for target in range(16):
        row = by[target]
        qholes = int(row["quotient_holes"])
        assert bool(row["promotable_to_current_quotient_factor_inventory"]) == (qholes > 0)
        if qholes:
            promoted.append(tuple(map(int, row["triple"])))
    assert len(promoted) == len(set(promoted))
    return tuple(sorted(promoted)), tuple(by[i] for i in range(16))


def analyze():
    tail5, tail5_rows = load_promoted(TAIL5_DIR, "tail5_quotient", "tail5_target")
    tail6, tail6_rows = load_promoted(TAIL6_DIR, "tail6_quotient", "tail6_target")

    frozen = tuple(tuple(map(int, x)) for x in T.TERNARY_FACTORS)
    prior_promoted = tuple(T4.TAIL3) + tuple(T4.TAIL4)
    current = tuple(sorted(set(frozen) | set(prior_promoted) | set(tail5)))
    assert len(current) == len(frozen) + len(prior_promoted) + len(tail5)

    duplicate = tuple(sorted(set(tail6) & set(current)))
    new = tuple(sorted(set(tail6) - set(current)))
    assert not duplicate
    expanded = tuple(sorted(set(current) | set(new)))
    quads = tuple(tuple(map(int, q)) for q in T.QUATERNARY_FACTORS)

    adj = S.build_graph(expanded + quads)
    edge_count = sum(len(nbs) for nbs in adj.values()) // 2
    comps = T.connected_components(adj)
    _order, rows, fills = T.deterministic_min_fill_certificate(adj)
    upper = max((int(row["later_degree"]) for row in rows), default=0)
    clique = S.exact_maximum_clique(adj)
    lower = max(0, len(clique) - 1)

    tail6_promoted_rows = [
        row for row in tail6_rows if int(row["quotient_holes"]) > 0
    ]
    tail6_sign_only = [
        row for row in tail6_rows
        if int(row["raw_holes"]) > 0 and int(row["quotient_holes"]) == 0
    ]
    tail6_pairwise_complete = [
        row for row in tail6_rows if int(row["raw_holes"]) == 0
    ]

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "tail5_promoted_factor_count": len(tail5),
        "tail6_targets": 16,
        "tail6_promotable_quotient_factors": len(tail6_promoted_rows),
        "tail6_sign_only_raw_obstructions": len(tail6_sign_only),
        "tail6_pairwise_complete_targets": len(tail6_pairwise_complete),
        "tail6_total_quotient_holes": sum(
            int(row["quotient_holes"]) for row in tail6_promoted_rows
        ),
        "tail6_promoted_scopes": [list(x) for x in tail6],
        "current_ternary_factor_count_before_tail6": len(current),
        "expanded_candidate_ternary_factor_count": len(expanded),
        "physical_quaternary_factors": len(quads),
        "expanded_scope_digest_sha256": digest_scopes(expanded, quads),
        "expanded_primal_variables": len(adj),
        "expanded_primal_edges": edge_count,
        "expanded_component_sizes": [len(x) for x in comps],
        "exact_maximum_clique": list(clique),
        "treewidth_lower_bound_from_maximum_clique": lower,
        "deterministic_min_fill_upper_bound": upper,
        "min_fill_edges_added": len(fills),
        "exact_treewidth_if_bounds_match": upper if lower == upper else None,
        "decision": (
            "TAIL6_EXACT_QUOTIENT_PROMOTION_SCOUT_WITH_MATCHING_TREEWIDTH_CERTIFICATE"
            if lower == upper
            else "TAIL6_EXACT_QUOTIENT_PROMOTION_SCOUT_WITH_TREEWIDTH_BOUNDS"
        ),
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_TAIL6_SUMMARY")
    print("boundary=current inventory is reconstructed from clean tail5 artifacts; no weighted count is inferred")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
