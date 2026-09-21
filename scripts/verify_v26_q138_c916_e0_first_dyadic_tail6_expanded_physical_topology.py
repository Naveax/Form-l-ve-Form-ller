#!/usr/bin/env python3
"""Prepared topology authority for the physical inventory through tail6.

Activation requires a clean 16-target tail6 quotient aggregate. The verifier reconstructs
the merged 69-ternary inventory from frozen + tail3 + tail4 + tail5 exact quotient factors,
adds only nonempty tail6 quotient relations, then reports exact maximum-clique lower and
explicit deterministic min-fill upper bounds. No physical assignment count is inferred.
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
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail6 as S6
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as S

TAIL6_DIR = Path(os.environ.get("C916_TAIL6_QUOTIENT_DIR", "authorities/tail6-quotient"))


def load_tail6_scopes():
    files = sorted(TAIL6_DIR.glob("tail6_quotient_*.json"))
    assert len(files) == 16, (TAIL6_DIR, len(files))
    rows = [json.loads(p.read_text()) for p in files]
    by = {int(row["tail6_target"]): row for row in rows}
    assert set(by) == set(range(16))

    scopes = []
    holes = 0
    sign_only = 0
    pairwise_complete = 0
    for target in range(16):
        row = by[target]
        qholes = int(row["quotient_holes"])
        raw_holes = int(row["raw_holes"])
        assert bool(row["promotable_to_current_quotient_factor_inventory"]) == (qholes > 0)
        if qholes:
            scope = tuple(map(int, row["triple"]))
            forbidden = tuple(tuple(map(int, x)) for x in row["quotient_hole_tuples"])
            assert len(forbidden) == qholes
            scopes.append(scope)
            holes += qholes
        elif raw_holes:
            sign_only += 1
        else:
            pairwise_complete += 1

    assert len(scopes) == len(set(scopes))
    return tuple(sorted(scopes)), holes, sign_only, pairwise_complete


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
            missing = tuple(
                (u, w)
                for u, w in itertools.combinations(nbs, 2)
                if w not in adj[u]
            )
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
    tail5 = S6.load_tail5_scopes()
    tail6, tail6_holes, sign_only, pairwise_complete = load_tail6_scopes()

    current = tuple(sorted(set(T.TERNARY_FACTORS) | set(T4.TAIL3) | set(T4.TAIL4) | set(tail5)))
    assert len(T.TERNARY_FACTORS) == 38
    assert len(T4.TAIL3) == 10
    assert len(T4.TAIL4) == 12
    assert len(tail5) == 9
    assert len(current) == 69
    assert not (set(current) & set(tail6))

    ternary = tuple(sorted(set(current) | set(tail6)))
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
        "current_ternary_factors": len(current),
        "tail6_promoted_ternary_factors": len(tail6),
        "tail6_total_quotient_holes": tail6_holes,
        "tail6_sign_only_raw_obstructions": sign_only,
        "tail6_pairwise_complete_targets": pairwise_complete,
        "tail6_promoted_scopes": [list(x) for x in tail6],
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
            "C916_TAIL6_EXPANDED_PHYSICAL_TOPOLOGY_EXACT_TREEWIDTH"
            if lower == upper
            else "C916_TAIL6_EXPANDED_PHYSICAL_TOPOLOGY_BOUNDS"
        ),
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL6_EXPANDED_PHYSICAL_TOPOLOGY")
    if lower == upper:
        print(f"theorem=matching clique lower bound and explicit elimination prove exact treewidth {upper}")
    else:
        print(f"boundary=treewidth is bounded only: {lower} <= tw <= {upper}")
    print("boundary=activation requires clean tail6 quotient artifacts; topology only, no physical assignment count or weighted work count is inferred")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
