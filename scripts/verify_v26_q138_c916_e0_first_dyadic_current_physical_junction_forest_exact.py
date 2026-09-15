#!/usr/bin/env python3
"""Exact clique/junction-forest certificate for current C916 physical factors.

The merged topology theorem proves treewidth 5.  This verifier turns that theorem into
the concrete finite state spaces needed by the next exact contraction/counting step.
It independently rebuilds maximal cliques from the zero-fill perfect elimination graph,
constructs a maximum-intersection clique forest, verifies running intersection, and
uses the exact m4 image sizes to compute quotient table sizes.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T

EXPECTED_CLIQUE_DIGEST = "f04178b2510d52ef68ec356fd03d2cb07ec24508d00573e254ab98e8ce505818"
EXPECTED_FOREST_DIGEST = "05fff76b631b4afc62b996307c890ebfdef385c4baa076b219d68057b2fa1a84"
EXPECTED_CLIQUE_COUNT = 21
EXPECTED_FOREST_EDGES = 15
EXPECTED_MAX_CLIQUE_STATES = 4096
EXPECTED_TOTAL_CLIQUE_STATES = 14224
EXPECTED_MAX_SEPARATOR_STATES = 1024
EXPECTED_TOTAL_SEPARATOR_STATES = 1536


def digest(obj) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def build_primal_graph():
    adj = defaultdict(set)
    for scope in T.TERNARY_FACTORS + T.QUATERNARY_FACTORS:
        for v in scope:
            adj[int(v)]
        for u, v in itertools.combinations(scope, 2):
            adj[int(u)].add(int(v))
            adj[int(v)].add(int(u))
    return {v: set(nbs) for v, nbs in adj.items()}


def perfect_elimination_rows(adj0):
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
        fill_count, degree, v, nbs, missing = min(candidates)
        rows.append((v, nbs))
        for u, w in missing:
            adj[u].add(w)
            adj[w].add(u)
            fills.append((u, w))
        for u in nbs:
            adj[u].remove(v)
        del adj[v]
    assert not fills
    assert max(len(nbs) for _v, nbs in rows) == T.EXPECTED_TREEWIDTH
    return tuple(rows)


def maximal_cliques(rows):
    bags = [frozenset((v, *nbs)) for v, nbs in rows]
    maximal = []
    for bag in bags:
        if bag and not any(bag < other for other in bags):
            maximal.append(tuple(sorted(bag)))
    return tuple(sorted(set(maximal), key=lambda row: (-len(row), row)))


def maximum_intersection_forest(cliques):
    edges = []
    sets = tuple(map(set, cliques))
    for i in range(len(cliques)):
        for j in range(i + 1, len(cliques)):
            sep = tuple(sorted(sets[i] & sets[j]))
            if sep:
                edges.append((len(sep), i, j, sep))

    parent = list(range(len(cliques)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    chosen = []
    for weight, i, j, sep in sorted(edges, key=lambda row: (-row[0], row[1], row[2])):
        ri, rj = find(i), find(j)
        if ri == rj:
            continue
        parent[ri] = rj
        chosen.append((i, j, sep))
    return tuple(chosen)


def verify_running_intersection(cliques, forest):
    cadj = defaultdict(set)
    for i, j, _sep in forest:
        cadj[i].add(j)
        cadj[j].add(i)
    variables = sorted({v for bag in cliques for v in bag})
    for v in variables:
        members = {i for i, bag in enumerate(cliques) if v in bag}
        assert members
        root = min(members)
        seen = {root}
        q = deque([root])
        while q:
            i = q.popleft()
            for j in cadj[i]:
                if j in members and j not in seen:
                    seen.add(j)
                    q.append(j)
        assert seen == members, (v, sorted(members), sorted(seen))


def quotient_sizes_from_m4():
    m4 = C.load(C.M4_PATH)
    sizes = {}
    for row in m4["four_parent_relations"]:
        gid = int(row["m4_group_id"])
        cols = int(row["cols"])
        assert cols in (7, 9)
        qsize = (cols + 1) // 2
        old = sizes.setdefault(gid, qsize)
        assert old == qsize
    assert Counter(sizes.values()) == Counter({4: 88, 5: 2})
    assert sorted(g for g, n in sizes.items() if n == 5) == [31, 82]
    return sizes


def analyze():
    adj = build_primal_graph()
    rows = perfect_elimination_rows(adj)
    cliques = maximal_cliques(rows)
    assert len(cliques) == EXPECTED_CLIQUE_COUNT
    assert digest([list(row) for row in cliques]) == EXPECTED_CLIQUE_DIGEST

    forest = maximum_intersection_forest(cliques)
    assert len(forest) == EXPECTED_FOREST_EDGES
    forest_json = [
        {"left": i, "right": j, "separator": list(sep)}
        for i, j, sep in forest
    ]
    assert digest(forest_json) == EXPECTED_FOREST_DIGEST
    verify_running_intersection(cliques, forest)

    # A forest with |C|-k edges has k connected components.  This must agree with the
    # six connected components of the physical primal graph certified by T.
    assert len(cliques) - len(forest) == len(T.EXPECTED_COMPONENT_SIZES) == 6

    qsizes = quotient_sizes_from_m4()
    bag_states = [math.prod(qsizes[v] for v in bag) for bag in cliques]
    sep_states = [math.prod(qsizes[v] for v in sep) for _i, _j, sep in forest]
    assert max(bag_states) == EXPECTED_MAX_CLIQUE_STATES
    assert sum(bag_states) == EXPECTED_TOTAL_CLIQUE_STATES
    assert max(sep_states) == EXPECTED_MAX_SEPARATOR_STATES
    assert sum(sep_states) == EXPECTED_TOTAL_SEPARATOR_STATES

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "physical_factor_scope_digest_sha256": T.EXPECTED_SCOPE_DIGEST,
        "exact_treewidth": T.EXPECTED_TREEWIDTH,
        "maximal_cliques": [list(row) for row in cliques],
        "maximal_clique_count": len(cliques),
        "maximal_clique_digest_sha256": EXPECTED_CLIQUE_DIGEST,
        "junction_forest_edges": forest_json,
        "junction_forest_edge_count": len(forest),
        "junction_forest_digest_sha256": EXPECTED_FOREST_DIGEST,
        "running_intersection_verified": True,
        "junction_components": len(cliques) - len(forest),
        "separator_size_histogram": dict(sorted(Counter(len(sep) for _i, _j, sep in forest).items())),
        "quotient_five_state_group_ids": [31, 82],
        "clique_table_state_histogram": dict(sorted(Counter(bag_states).items())),
        "separator_table_state_histogram": dict(sorted(Counter(sep_states).items())),
        "max_clique_table_states": max(bag_states),
        "sum_clique_table_states": sum(bag_states),
        "max_separator_table_states": max(sep_states),
        "sum_separator_table_states": sum(sep_states),
        "decision": "C916_CURRENT_PHYSICAL_FACTORS_HAVE_EXACT_SMALL_JUNCTION_FOREST",
        "next_exact_step": "compile forbidden quotient tuples into these clique tables and use separator messages, max 1024 states, as the physical higher-order constraint layer inside the weighted counter",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_CURRENT_PHYSICAL_JUNCTION_FOREST_EXACT")
    print("theorem=the 43 currently certified physical higher-order factors admit an exact six-component junction forest with 21 maximal cliques; the largest exact quotient clique table has 4096 states and the largest separator message has 1024 states")
    print("boundary=this certifies the physical-factor layer only; pairwise/affine weighted coupling still has to be conjoined exactly and additional uncertified physical factors may exist")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
