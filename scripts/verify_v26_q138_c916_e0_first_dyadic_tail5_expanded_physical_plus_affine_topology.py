#!/usr/bin/env python3
"""Prepared topology sizing for tail5-expanded physical + complete affine factors.

Activation requires the clean tail5 quotient artifacts.  This adds the nine exact tail5
ternary scopes to the merged tail4 physical+affine topology, computes an exact
maximum-clique lower bound, deterministic min-fill and deterministic beam upper bounds,
and reports junction clique capacities without materializing constraint tables.
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_treewidth_exact as W
import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_forest_exact as J
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_treewidth8_exact as T4
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_plus_affine_topology as TOP4
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as S

TAIL5_DIR = Path(os.environ.get("C916_TAIL5_QUOTIENT_DIR", "authorities/tail5-quotient"))


def load_tail5_scopes():
    files = sorted(TAIL5_DIR.glob("tail5_quotient_*.json"))
    assert len(files) == 16, (TAIL5_DIR, len(files))
    rows = [json.loads(p.read_text()) for p in files]
    by = {int(r["tail5_target"]): r for r in rows}
    assert set(by) == set(range(16))
    scopes = []
    holes = 0
    for target in range(16):
        row = by[target]
        qholes = int(row["quotient_holes"])
        assert bool(row["promotable_to_current_quotient_factor_inventory"]) == (qholes > 0)
        if qholes:
            scopes.append(tuple(map(int, row["triple"])))
            holes += qholes
    scopes = tuple(sorted(scopes))
    assert len(scopes) == 9
    assert holes == 31
    assert len(set(scopes)) == len(scopes)
    return scopes, holes


def analyze():
    tail5, holes = load_tail5_scopes()
    scopes = tuple(W.all_scopes()) + tuple(T4.TAIL3) + tuple(T4.TAIL4) + tail5
    # 38 frozen ternaries + 5 physical quads + 19 affine + 10 tail3 + 12 tail4 + 9 tail5
    assert len(scopes) == 93
    assert len(set(scopes)) == len(scopes)
    adj = W.build_primal_graph(scopes)

    deterministic_rows, deterministic_fills = W.deterministic_min_fill_certificate(adj)
    deterministic_upper = max(int(row["later_degree"]) for row in deterministic_rows)

    beam_rows, beam_fills, beam_upper = TOP4.beam_elimination_certificate(
        adj, beam_width=2048, branch_factor=10
    )
    if beam_upper < deterministic_upper:
        rows, fills, upper, source = beam_rows, beam_fills, beam_upper, "deterministic_beam_2048x10"
    else:
        rows, fills, upper, source = (
            deterministic_rows,
            deterministic_fills,
            deterministic_upper,
            "deterministic_min_fill",
        )

    clique = S.exact_maximum_clique(adj)
    lower = len(clique) - 1
    assert lower <= upper

    simple_rows = tuple(
        (int(row["vertex"]), tuple(map(int, row["later_neighbors"])))
        for row in rows
    )
    cliques = J.maximal_cliques(simple_rows)
    forest = J.maximum_intersection_forest(cliques)
    J.verify_running_intersection(cliques, forest)
    qsizes = J.quotient_sizes_from_m4()
    capacities = [math.prod(qsizes[v] for v in bag) for bag in cliques]

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "combined_higher_order_scopes": len(scopes),
        "tail5_promoted_ternary_factors": len(tail5),
        "tail5_total_quotient_holes": holes,
        "primal_variables": len(adj),
        "treewidth_lower_bound_from_exact_maximum_clique": lower,
        "exact_maximum_clique": list(clique),
        "deterministic_min_fill_upper_bound": deterministic_upper,
        "beam_2048x10_upper_bound": beam_upper,
        "selected_upper_bound": upper,
        "selected_elimination_source": source,
        "exact_treewidth_if_bounds_match": upper if lower == upper else None,
        "selected_fill_edges": [list(map(int, x)) for x in fills],
        "maximal_cliques": len(cliques),
        "junction_forest_edges": len(forest),
        "largest_clique_variables": max(map(len, cliques)),
        "largest_clique_capacity": max(capacities),
        "total_clique_capacity": sum(capacities),
        "decision": (
            "C916_TAIL5_EXPANDED_PHYSICAL_PLUS_AFFINE_TOPOLOGY_EXACT_TREEWIDTH"
            if lower == upper
            else "C916_TAIL5_EXPANDED_PHYSICAL_PLUS_AFFINE_TOPOLOGY_BOUNDS"
        ),
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL5_EXPANDED_PHYSICAL_PLUS_AFFINE_TOPOLOGY")
    if lower == upper:
        print(f"theorem=matching exact clique lower bound and explicit elimination prove exact treewidth {upper}")
    else:
        print(f"boundary=treewidth is bounded only: {lower} <= tw <= {upper}")
    print("boundary=topology only; no higher-order assignment count or weighted count is inferred")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
