#!/usr/bin/env python3
"""Prepared exact treewidth certificate for the physical inventory through tail5.

The clean tail5 aggregate gives an exact maximum-clique lower bound 6 and a deterministic
min-fill upper bound 8.  This verifier closes that two-bit gap on the unique 30-variable
large component using exhaustive labeled filled-graph elimination search:

  * if no width-7 ordering exists, exact treewidth is 8;
  * otherwise test width 6;
  * if width 6 exists, the clique lower bound makes treewidth exactly 6;
  * if width 6 fails, treewidth is exactly 7.

Activation requires the clean tail5 quotient artifacts.  This is topology only.
"""
from __future__ import annotations

import functools
import itertools
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_treewidth8_exact as T4
import verify_v26_q138_c916_e0_first_dyadic_tail5_expanded_physical_topology as T5
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as S

EXPECTED_COMPONENT_SIZES = (30, 3, 3, 3, 3, 3)
EXPECTED_LOWER = 6
EXPECTED_UPPER = 8


def components(adj):
    unseen = set(adj)
    out = []
    while unseen:
        root = min(unseen)
        stack = [root]
        comp = set()
        while stack:
            v = stack.pop()
            if v in comp:
                continue
            comp.add(v)
            unseen.discard(v)
            stack.extend(adj[v] - comp)
        out.append(tuple(sorted(comp)))
    return tuple(sorted(out, key=lambda row: (-len(row), row)))


def build_graph():
    tail5, holes = T5.load_tail5_scopes()
    assert len(tail5) == 9
    assert holes == 31
    ternary = tuple(sorted(set(T.TERNARY_FACTORS) | set(T4.TAIL3) | set(T4.TAIL4) | set(tail5)))
    assert len(ternary) == 69
    quads = tuple(tuple(map(int, q)) for q in T.QUATERNARY_FACTORS)
    adj = T5.build_graph(ternary + quads)
    return ternary, quads, adj


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


def replay_width(adj0, vertices, ordering_indices):
    vertices = tuple(vertices)
    adj = {v: set(u for u in adj0[v] if u in vertices) for v in vertices}
    width = 0
    ordering = []
    for idx in ordering_indices:
        v = vertices[int(idx)]
        assert v in adj
        nbs = tuple(sorted(adj[v]))
        width = max(width, len(nbs))
        ordering.append(v)
        for a, b in itertools.combinations(nbs, 2):
            adj[a].add(b)
            adj[b].add(a)
        for u in nbs:
            adj[u].remove(v)
        del adj[v]
    assert not adj
    return width, tuple(ordering)


def analyze():
    ternary, quads, adj = build_graph()
    comps = components(adj)
    sizes = tuple(len(row) for row in comps)
    assert sizes == EXPECTED_COMPONENT_SIZES

    clique = S.exact_maximum_clique(adj)
    lower = len(clique) - 1
    assert lower == EXPECTED_LOWER

    rows, fills = T5.min_fill(adj)
    upper = max(len(nbs) for _v, nbs in rows)
    assert upper == EXPECTED_UPPER

    large = comps[0]
    order7, states7, cache7 = exact_width_at_most(adj, large, 7)
    if order7 is None:
        exact = 8
        order6 = None
        states6 = 0
        cache6_hits = 0
        cache6_misses = 0
        witness_order = None
    else:
        replay7, ordering7 = replay_width(adj, large, order7)
        assert replay7 <= 7
        order6, states6, cache6 = exact_width_at_most(adj, large, 6)
        cache6_hits = int(cache6.hits)
        cache6_misses = int(cache6.misses)
        if order6 is None:
            exact = 7
            witness_order = ordering7
        else:
            replay6, ordering6 = replay_width(adj, large, order6)
            assert replay6 <= 6
            exact = 6
            witness_order = ordering6

    assert lower <= exact <= upper
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "expanded_ternary_factors": len(ternary),
        "physical_quaternary_factors": len(quads),
        "component_sizes": list(sizes),
        "exact_maximum_clique": list(clique),
        "clique_lower_bound": lower,
        "deterministic_min_fill_upper_bound": upper,
        "width7_order_exists": order7 is not None,
        "width7_states_visited": states7,
        "width7_cache_hits": int(cache7.hits),
        "width7_cache_misses": int(cache7.misses),
        "width6_order_exists": order6 is not None if order7 is not None else None,
        "width6_states_visited": states6,
        "width6_cache_hits": cache6_hits,
        "width6_cache_misses": cache6_misses,
        "exact_treewidth": exact,
        "witness_elimination_order_if_available": None if witness_order is None else list(witness_order),
        "decision": "C916_TAIL5_EXPANDED_PHYSICAL_PRIMAL_EXACT_TREEWIDTH",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL5_EXPANDED_PHYSICAL_TREEWIDTH_EXACT")
    print(f"theorem=exhaustive elimination search plus the clique lower bound and width-8 explicit completion prove exact treewidth {exact}")
    print("boundary=topology only; no physical assignment count or weighted work count is inferred")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
