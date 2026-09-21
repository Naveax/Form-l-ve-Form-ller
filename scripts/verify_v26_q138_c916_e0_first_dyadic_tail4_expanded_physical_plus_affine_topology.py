#!/usr/bin/env python3
"""Topology-only certificate for tail4-expanded physical + complete affine factors.

This intentionally stops before clique-table enumeration. It reports an exact
maximum-clique lower bound and two explicit chordal-completion upper bounds, allowing
the junction compiler to be sized before any potentially large table is materialized.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_treewidth_exact as W
import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_forest_exact as J
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_treewidth8_exact as T4
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as S



def beam_elimination_certificate(adj0, beam_width=2048, branch_factor=10):
    initial = ({v: set(nbs) for v, nbs in adj0.items()}, [], [], 0, 0)
    beam = [initial]

    def signature(adj):
        return tuple((v, tuple(sorted(adj[v]))) for v in sorted(adj))

    for _depth in range(len(adj0)):
        children = {}
        for adj, rows, fills, width, fill_total in beam:
            candidates = []
            for v, nbs0 in adj.items():
                nbs = tuple(sorted(nbs0))
                missing = tuple(
                    (u, w)
                    for u, w in itertools.combinations(nbs, 2)
                    if w not in adj[u]
                )
                candidates.append((
                    max(width, len(nbs)), len(missing), len(nbs), v, nbs, missing
                ))
            for _neww, fcount, degree, v, nbs, missing in sorted(candidates)[:branch_factor]:
                nadj = {x: set(ns) for x, ns in adj.items()}
                nfills = list(fills)
                for u, w in missing:
                    if w not in nadj[u]:
                        nadj[u].add(w)
                        nadj[w].add(u)
                        nfills.append((u, w))
                for u in nbs:
                    nadj[u].remove(v)
                del nadj[v]
                nrows = rows + [{
                    "vertex": v,
                    "later_neighbors": list(nbs),
                    "later_degree": degree,
                    "fill_edges_needed": [list(x) for x in missing],
                }]
                nwidth = max(width, degree)
                nfill_total = fill_total + fcount
                sig = signature(nadj)
                score = (
                    nwidth, nfill_total, sum(len(ns) for ns in nadj.values()),
                    tuple(x["vertex"] for x in nrows),
                )
                old = children.get(sig)
                if old is None or score < old[0]:
                    children[sig] = (score, (nadj, nrows, nfills, nwidth, nfill_total))
        ranked = sorted(children.values(), key=lambda x: x[0])
        beam = [state for _score, state in ranked[:beam_width]]
        assert beam

    best = min(beam, key=lambda s: (s[3], s[4], tuple(r["vertex"] for r in s[1])))
    _adj, rows, fills, width, _fill_total = best
    assert not _adj and len(rows) == len(adj0)
    return tuple(rows), tuple(fills), int(width)


def analyze():
    scopes = tuple(W.all_scopes()) + tuple(T4.TAIL3) + tuple(T4.TAIL4)
    assert len(scopes) == 84
    assert len(set(scopes)) == len(scopes)
    adj = W.build_primal_graph(scopes)

    deterministic_rows, deterministic_fills = W.deterministic_min_fill_certificate(adj)
    deterministic_upper = max(int(row["later_degree"]) for row in deterministic_rows)

    beam_rows, beam_fills, beam_upper = beam_elimination_certificate(
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
            "C916_TAIL4_EXPANDED_PHYSICAL_PLUS_AFFINE_TOPOLOGY_EXACT_TREEWIDTH"
            if lower == upper
            else "C916_TAIL4_EXPANDED_PHYSICAL_PLUS_AFFINE_TOPOLOGY_BOUNDS"
        ),
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL4_EXPANDED_PHYSICAL_PLUS_AFFINE_TOPOLOGY")
    if lower == upper:
        print(f"theorem=matching lower and upper certificates prove exact treewidth {upper}")
    else:
        print(f"boundary=treewidth is bounded only: {lower} <= tw <= {upper}")
    print("boundary=topology only; no higher-order assignment count or weighted count is inferred")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
