#!/usr/bin/env python3
"""Prepared topology authority for the physical inventory through tail5.

Activation requires a clean 16-target tail5 quotient aggregate. The verifier loads only
nonempty exact quotient-hole relations, checks they are new relative to the merged
60-ternary inventory, then reports exact maximum-clique lower and deterministic min-fill
upper bounds plus clique capacities. It deliberately stops before table materialization.
"""
from __future__ import annotations

import itertools
import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T
import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_forest_exact as J
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_treewidth8_exact as T4
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as S

TAIL5_DIR = Path(os.environ.get("C916_TAIL5_QUOTIENT_DIR", "authorities/tail5-quotient"))


def load_tail5_scopes():
    files = sorted(TAIL5_DIR.glob("tail5_quotient_*.json"))
    assert len(files) == 16, (TAIL5_DIR, len(files))
    rows = [json.loads(p.read_text()) for p in files]
    by = {int(row["tail5_target"]): row for row in rows}
    assert set(by) == set(range(16))

    scopes = []
    holes = 0
    for target in range(16):
        row = by[target]
        qholes = int(row["quotient_holes"])
        assert bool(row["promotable_to_current_quotient_factor_inventory"]) == (qholes > 0)
        if qholes:
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


def min_fill(adj0):
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
        rows.append((v, nbs))
        for u, w in missing:
            if w not in adj[u]:
                adj[u].add(w)
                adj[w].add(u)
                fills.append((u, w))
        for u in nbs:
            adj[u].remove(v)
        del adj[v]
    return tuple(rows), tuple(fills)


def analyze():
    tail5, tail5_holes = load_tail5_scopes()
    current = tuple(sorted(set(T.TERNARY_FACTORS) | set(T4.TAIL3) | set(T4.TAIL4)))
    assert len(current) == 60
    assert not (set(current) & set(tail5))
    ternary = tuple(sorted(set(current) | set(tail5)))
    quads = tuple(tuple(map(int, q)) for q in T.QUATERNARY_FACTORS)

    adj = build_graph(ternary + quads)
    rows, fills = min_fill(adj)
    upper = max((len(nbs) for _v, nbs in rows), default=0)
    clique = S.exact_maximum_clique(adj)
    lower = max(0, len(clique) - 1)
    assert lower <= upper

    cliques = J.maximal_cliques(rows)
    forest = J.maximum_intersection_forest(cliques)
    J.verify_running_intersection(cliques, forest)
    qsizes = J.quotient_sizes_from_m4()
    capacities = [math.prod(qsizes[v] for v in bag) for bag in cliques]

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "tail5_promoted_ternary_factors": len(tail5),
        "tail5_total_quotient_holes": tail5_holes,
        "tail5_promoted_scopes": [list(x) for x in tail5],
        "current_ternary_factors": len(current),
        "expanded_ternary_factors": len(ternary),
        "physical_quaternary_factors": len(quads),
        "primal_variables": len(adj),
        "treewidth_lower_bound_from_exact_maximum_clique": lower,
        "exact_maximum_clique": list(clique),
        "deterministic_min_fill_upper_bound": upper,
        "exact_treewidth_if_bounds_match": upper if lower == upper else None,
        "fill_edges": [list(x) for x in fills],
        "maximal_cliques": len(cliques),
        "junction_forest_edges": len(forest),
        "largest_clique_capacity": max(capacities),
        "total_clique_capacity": sum(capacities),
        "decision": (
            "C916_TAIL5_EXPANDED_PHYSICAL_TOPOLOGY_EXACT_TREEWIDTH"
            if lower == upper
            else "C916_TAIL5_EXPANDED_PHYSICAL_TOPOLOGY_BOUNDS"
        ),
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL5_EXPANDED_PHYSICAL_TOPOLOGY")
    if lower == upper:
        print(f"theorem=matching clique lower bound and explicit elimination prove exact treewidth {upper}")
    else:
        print(f"boundary=treewidth is bounded only: {lower} <= tw <= {upper}")
    print("boundary=topology only; no physical assignment count or weighted work count is inferred")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
