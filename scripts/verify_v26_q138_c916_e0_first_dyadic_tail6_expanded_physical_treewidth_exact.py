#!/usr/bin/env python3
"""Prepared exact treewidth solver for the physical inventory through tail6.

Activation requires the clean tail6 quotient artifacts. The verifier reconstructs the
full physical primal graph through tail6, obtains deterministic min-fill and exact
maximum-clique bounds, then exactly decides every width k from the clique lower bound
upward using memoized elimination with the safe simplicial-vertex reduction. The first
feasible k is therefore the exact treewidth.
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
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as S

TAIL5_DIR = Path(os.environ.get("C916_TAIL5_QUOTIENT_DIR", "authorities/tail5-quotient"))
TAIL6_DIR = Path(os.environ.get("C916_TAIL6_QUOTIENT_DIR", "authorities/tail6-quotient"))

EXPECTED_TAIL5_COUNT = 9
EXPECTED_TAIL5_HOLES = 31


def load_promoted(directory: Path, prefix: str, target_key: str):
    files = sorted(directory.glob(f"{prefix}_*.json"))
    assert len(files) == 16, (directory, [p.name for p in files])
    rows = [json.loads(p.read_text()) for p in files]
    by = {int(row[target_key]): row for row in rows}
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
    assert len(scopes) == len(set(scopes))
    return tuple(sorted(scopes)), holes


def build_graph(scopes):
    adj = {}
    for scope in scopes:
        for v in scope:
            adj.setdefault(int(v), set())
        for u, v in itertools.combinations(scope, 2):
            adj[int(u)].add(int(v))
            adj[int(v)].add(int(u))
    return adj


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


def min_fill(adj0):
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
    return ordering, visited, simplicial_reductions, search.cache_info()


def analyze():
    tail5, tail5_holes = load_promoted(TAIL5_DIR, "tail5_quotient", "tail5_target")
    assert len(tail5) == EXPECTED_TAIL5_COUNT
    assert tail5_holes == EXPECTED_TAIL5_HOLES

    tail6, tail6_holes = load_promoted(TAIL6_DIR, "tail6_quotient", "tail6_target")
    prior = tuple(T.TERNARY_FACTORS) + tuple(T4.TAIL3) + tuple(T4.TAIL4) + tail5
    assert len(prior) == 69
    assert len(set(prior)) == 69
    assert not (set(prior) & set(tail6))

    ternary = prior + tail6
    quads = tuple(T.QUATERNARY_FACTORS)
    adj = build_graph(ternary + quads)
    comps = components(adj)

    rows, fills = min_fill(adj)
    upper = max((degree for _v, _nbs, degree in rows), default=0)
    clique = S.exact_maximum_clique(adj)
    lower = max(0, len(clique) - 1)
    assert lower <= upper

    decision_rows = []
    exact = None
    large = comps[0]
    for k in range(lower, upper + 1):
        ordering, states, simplicial, cache = exact_width_at_most(adj, large, k)
        feasible = ordering is not None
        decision_rows.append({
            "k": k,
            "feasible": feasible,
            "states_visited": states,
            "simplicial_reductions": simplicial,
            "cache_hits": int(cache.hits),
            "cache_misses": int(cache.misses),
        })
        if feasible:
            exact = k
            break

    assert exact is not None
    assert exact <= upper

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "tail5_promoted_ternary_factors": len(tail5),
        "tail6_promoted_ternary_factors": len(tail6),
        "tail6_total_quotient_holes": tail6_holes,
        "expanded_ternary_factors": len(ternary),
        "physical_quaternary_factors": len(quads),
        "primal_variables": len(adj),
        "component_sizes": [len(row) for row in comps],
        "exact_maximum_clique": list(clique),
        "initial_treewidth_lower_bound": lower,
        "deterministic_min_fill_upper_bound": upper,
        "deterministic_fill_edges": [list(x) for x in fills],
        "width_decisions": decision_rows,
        "exact_treewidth": exact,
        "decision": "C916_TAIL6_EXPANDED_PHYSICAL_PRIMAL_EXACT_TREEWIDTH",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL6_EXPANDED_PHYSICAL_TREEWIDTH_EXACT")
    print("theorem=exact width-decision search with safe simplicial reduction finds the minimum feasible elimination width between the exact clique lower bound and explicit min-fill upper bound")
    print("boundary=activation requires clean tail6 quotient artifacts; this is topology only and not a weighted count")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
