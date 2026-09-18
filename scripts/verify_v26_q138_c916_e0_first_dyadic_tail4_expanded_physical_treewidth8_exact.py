#!/usr/bin/env python3
"""Exact treewidth-8 certificate for the physical inventory through tail4.

Activation boundary: the twelve tail4 scopes are admitted only after the corrected
tail4 quotient aggregate certifies the exact nonempty quotient-hole relations.  Given
those scopes, this verifier proves exact treewidth 8 by exhaustive nonexistence of a
width-7 elimination ordering on the 29-variable large component and an explicit
deterministic width-8 elimination with two fill edges.
"""
from __future__ import annotations

import functools
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T

TAIL3 = (
    (4, 11, 165), (4, 24, 165), (4, 62, 165), (4, 67, 165), (4, 111, 165),
    (4, 113, 165), (4, 114, 165), (4, 136, 165), (4, 144, 165), (4, 165, 181),
)
TAIL4 = (
    (4, 165, 186), (4, 165, 239), (4, 165, 244), (4, 165, 245),
    (4, 165, 249), (4, 181, 182), (7, 181, 182), (8, 181, 182),
    (9, 181, 182), (10, 181, 182), (11, 181, 182), (24, 181, 182),
)
EXPECTED_COMPONENT_SIZES = (29, 3, 3, 3, 3, 3)
EXPECTED_FILL_EDGES = ((4, 7), (165, 182))
EXPECTED_WIDTH7_STATES = 655360


def build_graph():
    scopes = tuple(T.TERNARY_FACTORS) + TAIL3 + TAIL4 + tuple(T.QUATERNARY_FACTORS)
    assert len(scopes) == 65
    assert len(set(scopes)) == len(scopes)
    adj = {}
    for scope in scopes:
        for v in scope:
            adj.setdefault(int(v), set())
        for u, v in itertools.combinations(scope, 2):
            adj[int(u)].add(int(v))
            adj[int(v)].add(int(u))
    return scopes, adj


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


def deterministic_min_fill(adj0):
    adj = {v: set(nbs) for v, nbs in adj0.items()}
    rows = []
    fills = []
    while adj:
        candidates = []
        for v, nbs0 in adj.items():
            nbs = tuple(sorted(nbs0))
            missing = tuple((u, w) for u, w in itertools.combinations(nbs, 2) if w not in adj[u])
            candidates.append((len(missing), len(nbs), v, nbs, missing))
        _fc, degree, v, nbs, missing = min(candidates)
        rows.append((v, nbs, degree))
        for u, w in missing:
            if w not in adj[u]:
                adj[u].add(w)
                adj[w].add(u)
                fills.append((u, w))
        for u in nbs:
            adj[u].remove(v)
        del adj[v]
    return tuple(rows), tuple(fills)


def exact_width_at_most(adj0, vertices, k):
    vertices = tuple(vertices)
    index = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    masks = [0] * n
    for v in vertices:
        i = index[v]
        mask = 0
        for u in adj0[v]:
            if u in index:
                mask |= 1 << index[u]
        masks[i] = mask

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
    scopes, adj = build_graph()
    comps = components(adj)
    sizes = tuple(len(c) for c in comps)
    assert sizes == EXPECTED_COMPONENT_SIZES
    assert len(adj) == 44

    rows, fills = deterministic_min_fill(adj)
    upper = max(degree for _v, _nbs, degree in rows)
    assert upper == 8
    assert fills == EXPECTED_FILL_EDGES

    large = comps[0]
    ordering7, states7, cache7 = exact_width_at_most(adj, large, 7)
    assert ordering7 is None
    assert states7 == EXPECTED_WIDTH7_STATES

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "frozen_ternary_factors": len(T.TERNARY_FACTORS),
        "tail3_promoted_ternary_factors": len(TAIL3),
        "tail4_promoted_ternary_factors": len(TAIL4),
        "physical_quaternary_factors": len(T.QUATERNARY_FACTORS),
        "combined_physical_scopes": len(scopes),
        "primal_variables": len(adj),
        "component_sizes": list(sizes),
        "width7_exhaustive_order_exists": False,
        "width7_exhaustive_states_visited": states7,
        "width7_cache_hits": int(cache7.hits),
        "width7_cache_misses": int(cache7.misses),
        "deterministic_min_fill_upper_bound": upper,
        "deterministic_fill_edges": [list(x) for x in fills],
        "exact_treewidth": 8,
        "decision": "C916_TAIL4_EXPANDED_PHYSICAL_PRIMAL_EXACT_TREEWIDTH_8",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL4_EXPANDED_PHYSICAL_TREEWIDTH8_EXACT")
    print("theorem=no width-7 elimination ordering exists by exhaustive labeled filled-state search, while deterministic elimination attains width 8; therefore the tail4-expanded physical primal graph has exact treewidth 8")
    print("boundary=scope activation still depends on the clean corrected tail4 quotient aggregate; this is topology only and not a weighted count")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
