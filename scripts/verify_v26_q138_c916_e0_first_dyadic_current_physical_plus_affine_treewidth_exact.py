#!/usr/bin/env python3
"""Exact topology certificate for current physical + complete affine-support factors.

The current physical quotient factor layer alone has exact treewidth 5.  This verifier
adds the complete 19 affine-support obstructions and asks the more relevant structural
question for the next weighted compiler: how wide is their combined higher-order primal
graph before the dense pairwise quotient layer is considered?

The certificate is exact:
  * lower bound: an explicit K10 clique forces treewidth >= 9;
  * upper bound: deterministic min-fill elimination has maximum later degree 9.

Hence the combined current physical + affine-support higher-order layer has exact
treewidth 9.  This is a topology theorem only, not the final weighted count.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T
import verify_v26_q138_c916_e0_first_dyadic_projection_hyperedges_eventmask_vector_exact as V
import verify_v26_q138_c916_e0_first_dyadic_all_order_affine_support_exact as A

EXPECTED_SCOPE_COUNT = 62
EXPECTED_VARIABLE_COUNT = 48
EXPECTED_EDGE_COUNT = 178
EXPECTED_COMPONENT_SIZES = (36, 3, 3, 3, 3)
EXPECTED_TREEWIDTH = 9
EXPECTED_K10 = (3, 5, 7, 8, 9, 62, 67, 104, 113, 165)
EXPECTED_FILL_EDGE_COUNT = 13
EXPECTED_SCOPE_DIGEST = "a002bd0269a35b2c9894fe73009edb6ca8e6e2cf9179ef77f73588bde9c9dc1b"


def digest_scopes(scopes) -> str:
    payload = json.dumps(
        [list(row) for row in sorted(scopes, key=lambda r: (len(r), tuple(r)))],
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def all_scopes():
    m4 = C.load(C.M4_PATH)
    affine_triples = tuple(tuple(map(int, row)) for row in m4["projection_minimal_empty_triples"])
    assert len(affine_triples) == 5
    affine = affine_triples + V.QUADS + (A.AFFINE_FIVE,) + A.EXTRA_SIX
    assert len(affine) == A.EVENT_COUNT == 19
    scopes = tuple(tuple(map(int, row)) for row in (T.TERNARY_FACTORS + T.QUATERNARY_FACTORS + affine))
    assert len(scopes) == EXPECTED_SCOPE_COUNT
    assert len(set(scopes)) == EXPECTED_SCOPE_COUNT
    assert digest_scopes(scopes) == EXPECTED_SCOPE_DIGEST
    return scopes


def build_primal_graph(scopes):
    adj = {}
    for scope in scopes:
        assert len(scope) == len(set(scope))
        for v in scope:
            adj.setdefault(v, set())
        for u, v in itertools.combinations(scope, 2):
            adj[u].add(v)
            adj[v].add(u)
    return adj


def connected_components(adj):
    unseen = set(adj)
    out = []
    while unseen:
        root = min(unseen)
        q = deque([root])
        comp = set()
        while q:
            v = q.popleft()
            if v in comp:
                continue
            comp.add(v)
            unseen.discard(v)
            q.extend(sorted(adj[v] - comp))
        out.append(tuple(sorted(comp)))
    return tuple(sorted(out, key=lambda row: (-len(row), row)))


def deterministic_min_fill_certificate(adj0):
    adj = {v: set(nbs) for v, nbs in adj0.items()}
    rows = []
    fill_edges = []
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
        fill_count, degree, v, nbs, missing = min(candidates)
        rows.append(
            {
                "vertex": v,
                "later_neighbors": list(nbs),
                "later_degree": degree,
                "fill_edges_needed": [list(row) for row in missing],
            }
        )
        for u, w in missing:
            if w not in adj[u]:
                adj[u].add(w)
                adj[w].add(u)
                fill_edges.append((u, w))
        for u in nbs:
            adj[u].remove(v)
        del adj[v]
    return tuple(rows), tuple(fill_edges)


def analyze():
    scopes = all_scopes()
    adj = build_primal_graph(scopes)
    assert len(adj) == EXPECTED_VARIABLE_COUNT
    edge_count = sum(len(nbs) for nbs in adj.values()) // 2
    assert edge_count == EXPECTED_EDGE_COUNT

    components = connected_components(adj)
    component_sizes = tuple(len(row) for row in components)
    assert component_sizes == EXPECTED_COMPONENT_SIZES

    # Exact lower bound.
    for u, v in itertools.combinations(EXPECTED_K10, 2):
        assert v in adj[u], (u, v)

    # Exact upper bound from an explicit deterministic elimination certificate.
    rows, fill_edges = deterministic_min_fill_certificate(adj)
    width = max(row["later_degree"] for row in rows)
    assert width == EXPECTED_TREEWIDTH
    assert len(fill_edges) == EXPECTED_FILL_EDGE_COUNT
    assert len(rows) == EXPECTED_VARIABLE_COUNT

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "current_physical_scopes": len(T.TERNARY_FACTORS) + len(T.QUATERNARY_FACTORS),
        "complete_affine_support_scopes": A.EVENT_COUNT,
        "combined_higher_order_scopes": len(scopes),
        "combined_scope_digest_sha256": EXPECTED_SCOPE_DIGEST,
        "primal_variables": len(adj),
        "primal_edges": edge_count,
        "connected_component_sizes": list(component_sizes),
        "k10_lower_bound_witness": list(EXPECTED_K10),
        "deterministic_min_fill_width": width,
        "fill_edges_added": len(fill_edges),
        "exact_treewidth": width,
        "largest_bag_variables": width + 1,
        "perfect_elimination_order": [row["vertex"] for row in rows],
        "fill_edges": [list(row) for row in fill_edges],
        "decision": "C916_CURRENT_PHYSICAL_PLUS_COMPLETE_AFFINE_HIGHER_ORDER_PRIMAL_TREEWIDTH_IS_EXACTLY_9",
        "next_exact_step": "compile the combined physical and affine higher-order relations into width-9 bags, then couple those bag messages to the pairwise weighted recursion instead of treating physical and affine constraints as separate scan/event layers",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_CURRENT_PHYSICAL_PLUS_AFFINE_TREEWIDTH_EXACT")
    print("theorem=the combined higher-order primal graph of all 43 current physical quotient factors and the complete 19 affine-support obstructions has exact treewidth 9: an explicit K10 gives the lower bound and deterministic min-fill elimination gives the matching upper bound")
    print("boundary=this excludes the dense 4005 pairwise quotient relation layer and does not by itself produce the final weighted count")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
