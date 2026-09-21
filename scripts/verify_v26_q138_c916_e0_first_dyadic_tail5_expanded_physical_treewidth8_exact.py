#!/usr/bin/env python3
"""Exact treewidth-8 certificate for the physical inventory through tail5.

The lower bound is inherited by graph monotonicity from the merged tail4 physical primal
graph, whose exact treewidth is 8. The tail5 graph contains every tail4 primal edge and
adds only exact quotient-factor edges. A deterministic min-fill elimination of the tail5
graph has width 8, so the two certified bounds meet exactly.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_treewidth8_exact as T4
import verify_v26_q138_c916_e0_first_dyadic_tail5_expanded_physical_topology as T5

TAIL4_EXACT_TREEWIDTH = 8


def analyze():
    # Reuse the exact tail5 artifact gate and topology construction.
    tail5_scopes, tail5_holes = T5.load_tail5_scopes()
    assert len(tail5_scopes) == 9
    assert tail5_holes == 31

    current = tuple(sorted(set(T4.T.TERNARY_FACTORS) | set(T4.TAIL3) | set(T4.TAIL4)))
    assert len(current) == 60
    quads = tuple(tuple(map(int, q)) for q in T4.T.QUATERNARY_FACTORS)
    tail5_graph = T5.build_graph(tuple(sorted(set(current) | set(tail5_scopes))) + quads)

    # The merged tail4 authority proves tw(G4)=8. Verify G4 is literally a subgraph
    # of the tail5 graph before using treewidth monotonicity.
    _tail4_scopes, tail4_graph = T4.build_graph()
    for v, neighbors in tail4_graph.items():
        assert v in tail5_graph
        assert set(neighbors) <= set(tail5_graph[v]), (v, neighbors - tail5_graph[v])

    rows, fills = T5.min_fill(tail5_graph)
    upper = max((len(nbs) for _v, nbs in rows), default=0)
    assert upper == TAIL4_EXACT_TREEWIDTH

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "tail4_exact_treewidth_lower_authority": TAIL4_EXACT_TREEWIDTH,
        "tail4_primal_is_subgraph_of_tail5": True,
        "tail5_promoted_ternary_factors": len(tail5_scopes),
        "tail5_total_quotient_holes": tail5_holes,
        "deterministic_min_fill_upper_bound": upper,
        "deterministic_fill_edges": [list(map(int, row)) for row in fills],
        "exact_treewidth": TAIL4_EXACT_TREEWIDTH,
        "decision": "C916_TAIL5_EXPANDED_PHYSICAL_PRIMAL_EXACT_TREEWIDTH_8_BY_SUBGRAPH_MONOTONICITY",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL5_EXPANDED_PHYSICAL_TREEWIDTH8_EXACT")
    print("theorem=tail4 exact treewidth 8 gives a monotone lower bound because its primal graph is an explicit subgraph of tail5, while deterministic tail5 elimination attains width 8")
    print("boundary=physical topology only; no assignment-count or weighted-work claim follows")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
