#!/usr/bin/env python3
"""Prepared exact treewidth-8 certificate for the physical inventory through tail5.

Activation requires the clean merged tail5 quotient artifacts. The graph contains the
38 frozen physical ternaries, 10 tail3 promotions, 12 tail4 promotions, nine tail5
promotions, and five physical quaternary scopes.

Upper bound: deterministic min-fill attains width 8.
Lower bound: an exact width-7 decision search exhausts all possibilities after repeatedly
applying the safe simplicial-vertex reduction tw(G)=max(deg(v),tw(G-v)) whenever the
simplicial degree is at most 7. If no width-7 ordering remains, treewidth is at least 8.
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

TAIL5_DIR = Path(os.environ.get("C916_TAIL5_QUOTIENT_DIR", "authorities/tail5-quotient"))
EXPECTED_TAIL5_SCOPES = (
    (62, 181, 182),
    (67, 181, 182),
    (113, 181, 182),
    (114, 181, 182),
    (136, 181, 182),
    (144, 181, 182),
    (154, 181, 182),
    (181, 182, 186),
    (181, 182, 239),
)
EXPECTED_COMPONENT_SIZES = (30, 3, 3, 3, 3, 3)
EXPECTED_FILL_EDGES = ((4, 7), (165, 182))


def load_tail5_scopes():
    files = sorted(TAIL5_DIR.glob("tail5_quotient_*.json"))
    assert len(files) == 16, (TAIL5_DIR, [p.name for p in files])
    rows = [json.loads(p.read_text()) for p in files]
    by = {int(row["tail5_target"]): row for row in rows}
    assert set(by) == set(range(16))

    scopes = []
    holes = 0
    for target in range(16):
        row = by[target]
        qholes = int(row["quotient_holes"])
        assert bool(row["promotable_to_current_quotient_factor_inventory"]) == (qholes > 0)
        if not qholes:
            continue
        scope = tuple(map(int, row["triple"]))
        forbidden = tuple(tuple(map(int, x)) for x in row["quotient_hole_tuples"])
        assert len(forbidden) == qholes
        scopes.append(scope)
        holes += qholes
    assert tuple(sorted(scopes)) == EXPECTED_TAIL5_SCOPES
    assert holes == 31
    return tuple(sorted(scopes))


def build_graph(scopes):
    adj = {}
    for scope in scopes:
        for v in scope:
            adj.setdefault(int(v), set())
        for u, v in itertools.combinations(scope, 2):
            adj[int(u)].add(int(v))
            adj[int(v)].add(int(u))
    return adj


def connected_components(adj):
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
            missing = tuple(
                (u, w)
                for u, w in itertools.combinations(nbs, 2)
                if w not in adj[u]
            )
            candidates.append((len(missing), len(nbs), v, nbs, missing))
        _fill_count, degree, v, nbs, missing = min(candidates)
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


def exact_width_at_most_with_simplicial_reduction(adj0, vertices, k):
    vertices = tuple(vertices)
    index = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    masks = []
    for v in vertices:
        mask = 0
        for u in adj0[v]:
            if u in index:
                mask |= 1 << index[u]
        masks.append(mask)

    visited = 0
    simplicial_reductions = 0

    def is_clique(nb, adjacency):
        scan = nb
        while scan:
            bit = scan & -scan
            i = bit.bit_length() - 1
            scan ^= bit
            wanted = nb & ~(1 << i)
            if (int(adjacency[i]) & wanted) != wanted:
                return False
        return True

    def eliminate(active, adjacency, i, nb):
        neighbors = []
        scan = nb
        while scan:
            bit = scan & -scan
            j = bit.bit_length() - 1
            scan ^= bit
            neighbors.append(j)

        nxt = list(map(int, adjacency))
        new_active = active & ~(1 << i)
        for a in neighbors:
            nxt[a] |= nb & ~(1 << a)
            nxt[a] &= ~(1 << i)
        nxt[i] = 0
        return new_active, tuple(x & new_active for x in nxt)

    @functools.lru_cache(maxsize=None)
    def search(active, adjacency):
        nonlocal visited, simplicial_reductions
        visited += 1
        if active == 0:
            return ()

        # Safe reduction. For simplicial v, tw(G)=max(deg(v),tw(G-v)); when deg(v)<=k
        # it can therefore be eliminated first without losing any width-k solution.
        for i in range(n):
            if not ((active >> i) & 1):
                continue
            nb = int(adjacency[i]) & active & ~(1 << i)
            if nb.bit_count() <= k and is_clique(nb, adjacency):
                simplicial_reductions += 1
                new_active, nxt = eliminate(active, adjacency, i, nb)
                suffix = search(new_active, nxt)
                return None if suffix is None else (i,) + suffix

        candidates = []
        for i in range(n):
            if not ((active >> i) & 1):
                continue
            nb = int(adjacency[i]) & active & ~(1 << i)
            degree = nb.bit_count()
            if degree > k:
                continue
            neighbors = []
            scan = nb
            while scan:
                bit = scan & -scan
                j = bit.bit_length() - 1
                scan ^= bit
                neighbors.append(j)
            fill = sum(
                1
                for a, b in itertools.combinations(neighbors, 2)
                if not ((int(adjacency[a]) >> b) & 1)
            )
            candidates.append((fill, degree, i, nb))

        if not candidates:
            return None

        for _fill, _degree, i, nb in sorted(candidates):
            new_active, nxt = eliminate(active, adjacency, i, nb)
            suffix = search(new_active, nxt)
            if suffix is not None:
                return (i,) + suffix
        return None

    ordering = search((1 << n) - 1, tuple(masks))
    info = search.cache_info()
    return ordering, visited, simplicial_reductions, info


def analyze():
    tail5 = load_tail5_scopes()
    ternary = tuple(T.TERNARY_FACTORS) + tuple(T4.TAIL3) + tuple(T4.TAIL4) + tail5
    assert len(ternary) == 69
    assert len(set(ternary)) == 69
    quads = tuple(T.QUATERNARY_FACTORS)

    adj = build_graph(ternary + quads)
    components = connected_components(adj)
    sizes = tuple(len(row) for row in components)
    assert sizes == EXPECTED_COMPONENT_SIZES
    assert len(adj) == 45

    rows, fills = deterministic_min_fill(adj)
    upper = max(degree for _v, _nbs, degree in rows)
    assert upper == 8
    assert fills == EXPECTED_FILL_EDGES

    large = components[0]
    order7, states7, simplicial7, cache7 = exact_width_at_most_with_simplicial_reduction(
        adj, large, 7
    )
    assert order7 is None

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "frozen_ternary_factors": len(T.TERNARY_FACTORS),
        "tail3_promoted_ternary_factors": len(T4.TAIL3),
        "tail4_promoted_ternary_factors": len(T4.TAIL4),
        "tail5_promoted_ternary_factors": len(tail5),
        "physical_quaternary_factors": len(quads),
        "combined_physical_scopes": len(ternary) + len(quads),
        "primal_variables": len(adj),
        "component_sizes": list(sizes),
        "width7_exhaustive_order_exists": False,
        "width7_states_visited": states7,
        "width7_simplicial_reductions": simplicial7,
        "width7_cache_hits": int(cache7.hits),
        "width7_cache_misses": int(cache7.misses),
        "deterministic_min_fill_upper_bound": upper,
        "deterministic_fill_edges": [list(x) for x in fills],
        "exact_treewidth": 8,
        "decision": "C916_TAIL5_EXPANDED_PHYSICAL_PRIMAL_EXACT_TREEWIDTH_8",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL5_EXPANDED_PHYSICAL_TREEWIDTH8_EXACT")
    print("theorem=no width-7 elimination ordering exists by exact memoized search with safe simplicial reduction, while deterministic elimination attains width 8; therefore the tail5-expanded physical primal graph has exact treewidth 8")
    print("boundary=this is topology only; pairwise, affine, multiplicity, and end-to-end work remain outside")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
