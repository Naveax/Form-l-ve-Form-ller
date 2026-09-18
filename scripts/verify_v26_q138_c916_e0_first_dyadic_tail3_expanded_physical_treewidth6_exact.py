#!/usr/bin/env python3
"""Exact treewidth-6 certificate for the frozen physical inventory plus tail3 promotions.

The merged tail3 quotient summary left a one-bit gap: maximum clique gave treewidth >= 5
while deterministic min-fill gave treewidth <= 6.  This verifier closes that gap exactly.

For k=5 it exhaustively enumerates every possible first elimination vertex whose current
filled degree is at most k, memoizing each labeled filled graph state.  Treewidth <= k is
equivalent to the existence of such an elimination ordering.  Exhaustion with no ordering
therefore proves treewidth > 5.  The deterministic min-fill width-6 ordering supplies the
matching upper bound.
"""
from __future__ import annotations

import functools
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T

TAIL3_PROMOTED = (
    (4, 11, 165), (4, 24, 165), (4, 62, 165), (4, 67, 165), (4, 111, 165),
    (4, 113, 165), (4, 114, 165), (4, 136, 165), (4, 144, 165), (4, 165, 181),
)
EXPECTED_LARGE_COMPONENT = (
    3, 4, 5, 7, 8, 9, 11, 12, 24, 62, 67, 104, 111, 112, 113, 114, 136,
    144, 165, 181, 182, 183, 185, 186, 239, 244, 245, 249,
)


def build_graph():
    triples = tuple(tuple(map(int, x)) for x in T.TERNARY_FACTORS) + TAIL3_PROMOTED
    quads = tuple(tuple(map(int, x)) for x in T.QUATERNARY_FACTORS)
    adj = {}
    for scope in triples + quads:
        for v in scope:
            adj.setdefault(v, set())
        for u, v in itertools.combinations(scope, 2):
            adj[u].add(v)
            adj[v].add(u)
    return triples, quads, adj


def exact_width_at_most(adj0, vertices, k):
    vertices = tuple(vertices)
    index = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    masks = [0] * n
    for v in vertices:
        i = index[v]
        m = 0
        for u in adj0[v]:
            if u in index:
                m |= 1 << index[u]
        masks[i] = m

    visited = 0

    @functools.lru_cache(maxsize=None)
    def search(active, adjacency):
        nonlocal visited
        visited += 1
        if active == 0:
            return ()

        candidates = []
        for i in range(n):
            if not ((active >> i) & 1):
                continue
            nb = int(adjacency[i]) & active & ~(1 << i)
            degree = nb.bit_count()
            if degree > k:
                continue
            ns = [j for j in range(n) if (nb >> j) & 1]
            fill = 0
            for a, b in itertools.combinations(ns, 2):
                if not ((int(adjacency[a]) >> b) & 1):
                    fill += 1
            candidates.append((fill, degree, i, nb))

        if not candidates:
            return None

        for _fill, _degree, i, nb in sorted(candidates):
            nxt = list(map(int, adjacency))
            ns = [j for j in range(n) if (nb >> j) & 1]
            for a in ns:
                nxt[a] |= nb & ~(1 << a)
                nxt[a] &= ~(1 << i)
            nxt[i] = 0
            new_active = active & ~(1 << i)
            nxt = tuple(x & new_active for x in nxt)
            suffix = search(new_active, nxt)
            if suffix is not None:
                return (i,) + suffix
        return None

    ordering = search((1 << n) - 1, tuple(masks))
    return ordering, visited, search.cache_info()


def analyze():
    triples, quads, adj = build_graph()
    comps = T.connected_components(adj)
    sizes = tuple(len(x) for x in comps)
    assert sizes == (28, 3, 3, 3, 3, 3), sizes
    large = tuple(comps[0])
    assert large == EXPECTED_LARGE_COMPONENT

    order5, visited5, cache5 = exact_width_at_most(adj, large, 5)
    assert order5 is None

    _order, rows, fill_edges = T.deterministic_min_fill_certificate(adj)
    upper = max(int(row["later_degree"]) for row in rows)
    assert upper == 6

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "frozen_ternary_factors": len(T.TERNARY_FACTORS),
        "tail3_promoted_ternary_factors": len(TAIL3_PROMOTED),
        "quaternary_factors": len(T.QUATERNARY_FACTORS),
        "expanded_ternary_factors": len(triples),
        "component_sizes": list(sizes),
        "large_component_vertices": list(large),
        "width5_exhaustive_order_exists": False,
        "width5_exhaustive_states_visited": visited5,
        "width5_cache_hits": int(cache5.hits),
        "width5_cache_misses": int(cache5.misses),
        "deterministic_min_fill_upper_bound": upper,
        "deterministic_min_fill_edges_added": len(fill_edges),
        "exact_treewidth": 6,
        "decision": "C916_FROZEN_PLUS_TAIL3_PROMOTED_PHYSICAL_PRIMAL_EXACT_TREEWIDTH_6",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL3_EXPANDED_PHYSICAL_TREEWIDTH6_EXACT")
    print("theorem=no width-5 elimination ordering exists by exhaustive labeled-state search, while deterministic elimination attains width 6; therefore the expanded physical primal graph has exact treewidth 6")
    print("boundary=this is a topology theorem only; it does not itself change any weighted count")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
