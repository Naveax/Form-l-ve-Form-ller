#!/usr/bin/env python3
"""Exact topology certificate for all currently quotient-certified C916 physical factors.

This is deliberately a mathematics/topology verifier.  It does not infer a weighted
count.  The factor scopes are the 38 merged ternary quotient factors through PR #282
plus the five merged quaternary quotient factors from PR #250.

The certificate proves the primal graph is chordal with exact treewidth 5:
* lower bound: an explicit K6 clique;
* upper bound: deterministic zero-fill elimination with maximum later degree 5.

That means the physical higher-order constraints themselves admit an exact junction-
tree compilation with bags of at most six quotient variables.  This result is the
structural bridge needed before rebuilding the all-current-factor weighted counter.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter, deque


TERNARY_FACTORS = (
    (5, 181, 182),
    (11, 12, 24),
    (62, 67, 104),
    (111, 112, 113),
    (69, 82, 87),
    (130, 131, 132),
    (178, 179, 184),
    (19, 20, 23),
    (61, 83, 129),
    (3, 4, 165),
    (3, 5, 7),
    (3, 7, 8),
    (3, 7, 9),
    (3, 7, 11),
    (3, 7, 12),
    (3, 7, 24),
    (3, 7, 62),
    (3, 7, 67),
    (3, 7, 104),
    (3, 7, 111),
    (3, 7, 112),
    (3, 7, 113),
    (3, 7, 136),
    (3, 7, 144),
    (3, 7, 165),
    (3, 7, 181),
    (3, 7, 182),
    (3, 7, 183),
    (3, 7, 185),
    (3, 7, 186),
    (3, 7, 239),
    (3, 7, 244),
    (3, 7, 245),
    (3, 7, 249),
    (3, 181, 182),
    (4, 5, 165),
    (4, 8, 165),
    (4, 9, 165),
)

QUATERNARY_FACTORS = (
    (4, 5, 8, 9),
    (4, 5, 8, 114),
    (4, 5, 9, 114),
    (4, 8, 9, 114),
    (5, 8, 9, 114),
)

EXPECTED_SCOPE_DIGEST = "00aeb41c026d1350c90c5efbb2d33d5c306eccbf570ea0b654a87db09f4f96f3"
EXPECTED_K6 = (3, 4, 5, 8, 9, 165)
EXPECTED_TREEWIDTH = 5
EXPECTED_COMPONENT_SIZES = (28, 3, 3, 3, 3, 3)
EXPECTED_FACTOR_COUNT = 43
EXPECTED_VARIABLE_COUNT = 43


def scope_digest() -> str:
    payload = json.dumps(
        {
            "quads": [list(row) for row in sorted(QUATERNARY_FACTORS)],
            "triples": [list(row) for row in sorted(TERNARY_FACTORS)],
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def build_primal_graph():
    adj: dict[int, set[int]] = {}
    for scope in TERNARY_FACTORS + QUATERNARY_FACTORS:
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
    order = []
    rows = []
    fill_edges = []
    while adj:
        candidates = []
        for v, nbs0 in adj.items():
            nbs = sorted(nbs0)
            missing = []
            for i, u in enumerate(nbs):
                for w in nbs[i + 1 :]:
                    if w not in adj[u]:
                        missing.append((u, w))
            candidates.append((len(missing), len(nbs), v, tuple(missing)))
        fill_count, degree, v, missing = min(candidates)
        nbs = tuple(sorted(adj[v]))
        rows.append({
            "vertex": v,
            "later_neighbors": list(nbs),
            "later_degree": degree,
            "fill_edges_needed": [list(e) for e in missing],
        })
        for u, w in missing:
            if w not in adj[u]:
                adj[u].add(w)
                adj[w].add(u)
                fill_edges.append((u, w))
        for u in nbs:
            adj[u].remove(v)
        del adj[v]
        order.append(v)
    return tuple(order), tuple(rows), tuple(fill_edges)


def maximal_bags(rows):
    bags = []
    for row in rows:
        bag = frozenset((row["vertex"], *row["later_neighbors"]))
        if bag and all(
            all((u == v or u in original_adj[v]) for u, v in itertools.combinations(sorted(bag), 2))
            for _ in (0,)
        ):
            bags.append(bag)
    maximal = []
    for bag in bags:
        if not any(bag < other for other in bags):
            maximal.append(tuple(sorted(bag)))
    return tuple(sorted(set(maximal), key=lambda row: (-len(row), row)))


def analyze():
    global original_adj
    assert len(TERNARY_FACTORS) == 38
    assert len(set(TERNARY_FACTORS)) == len(TERNARY_FACTORS)
    assert len(QUATERNARY_FACTORS) == 5
    assert len(set(QUATERNARY_FACTORS)) == len(QUATERNARY_FACTORS)
    assert len(TERNARY_FACTORS) + len(QUATERNARY_FACTORS) == EXPECTED_FACTOR_COUNT
    assert scope_digest() == EXPECTED_SCOPE_DIGEST

    original_adj = build_primal_graph()
    assert len(original_adj) == EXPECTED_VARIABLE_COUNT
    edge_count = sum(len(v) for v in original_adj.values()) // 2

    # Exact lower bound: a K6 subgraph forces treewidth >= 5.
    for u, v in itertools.combinations(EXPECTED_K6, 2):
        assert v in original_adj[u], (u, v)

    components = connected_components(original_adj)
    component_sizes = tuple(len(row) for row in components)
    assert component_sizes == EXPECTED_COMPONENT_SIZES

    # Exact upper bound: this deterministic elimination requires no fill at all and
    # has maximum later-neighborhood size 5.  Hence the primal graph is chordal
    # and treewidth <= 5.  Together with K6, treewidth == 5.
    order, rows, fill_edges = deterministic_min_fill_certificate(original_adj)
    width = max(row["later_degree"] for row in rows)
    assert not fill_edges
    assert width == EXPECTED_TREEWIDTH
    assert len(order) == EXPECTED_VARIABLE_COUNT

    bags = maximal_bags(rows)
    assert max(map(len, bags)) == EXPECTED_TREEWIDTH + 1
    assert EXPECTED_K6 in bags

    incidence = Counter(v for scope in TERNARY_FACTORS + QUATERNARY_FACTORS for v in scope)
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "ternary_quotient_factors": len(TERNARY_FACTORS),
        "quaternary_quotient_factors": len(QUATERNARY_FACTORS),
        "all_current_physical_factor_scopes": EXPECTED_FACTOR_COUNT,
        "scope_digest_sha256": EXPECTED_SCOPE_DIGEST,
        "primal_variables": len(original_adj),
        "primal_edges": edge_count,
        "connected_component_sizes": list(component_sizes),
        "zero_fill_perfect_elimination": True,
        "fill_edges_added": 0,
        "exact_treewidth": width,
        "largest_bag_variables": width + 1,
        "k6_lower_bound_witness": list(EXPECTED_K6),
        "perfect_elimination_order": list(order),
        "maximal_cliques": [list(row) for row in bags],
        "maximal_clique_count": len(bags),
        "highest_factor_incidence": [[v, c] for v, c in incidence.most_common(10)],
        "decision": "C916_ALL_CURRENT_PHYSICAL_QUOTIENT_HYPERGRAPH_IS_CHORDAL_TREEWIDTH_5",
        "next_exact_step": "compile the 38 ternary and five quaternary quotient relations into width-5 clique tables, then conjoin those tables with the pairwise/all-order-affine weighted recursion instead of tracking every forbidden tuple as an independent event bit",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_CURRENT_PHYSICAL_HYPERGRAPH_TREEWIDTH_EXACT")
    print("theorem=the primal graph of all 43 currently quotient-certified physical higher-order factors is chordal with exact treewidth 5: K6 gives the lower bound and a zero-fill perfect elimination order gives the matching upper bound")
    print("boundary=this is a topology theorem for the currently certified physical factors; it is not yet the global weighted count and it does not prove that no additional physical factors exist")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
