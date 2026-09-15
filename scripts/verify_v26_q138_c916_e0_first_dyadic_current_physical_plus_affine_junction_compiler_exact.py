#!/usr/bin/env python3
"""Compile current physical + complete affine-support constraints into width-9 tables.

This is the executable companion to the exact treewidth-9 topology certificate.  It
compiles all currently certified physical higher-order quotient relations together with
the complete 19 affine-support obstructions into clique tables on the deterministic
width-9 chordal completion, then performs exact junction-tree sum-product.

The resulting count concerns this combined higher-order layer only.  The dense 4,005
pairwise quotient relation layer and its multiplicity weights remain outside this pass.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import sys
from collections import defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T
import verify_v26_q138_c916_e0_first_dyadic_projection_hyperedges_eventmask_vector_exact as V
import verify_v26_q138_c916_e0_first_dyadic_all_order_affine_support_exact as A
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_all_known_physical_exact as H
import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_treewidth_exact as W

FACTOR_DIR = Path(os.environ.get("C916_CURRENT_PHYSICAL_FACTOR_DIR", "authorities/current-physical-factors"))
EXPECTED_TERNARY_COUNT = 38
EXPECTED_CLIQUE_COUNT = 26
EXPECTED_COMPONENT_COUNT = 5
EXPECTED_FOREST_EDGES = EXPECTED_CLIQUE_COUNT - EXPECTED_COMPONENT_COUNT
EXPECTED_MAX_CLIQUE_CAPACITY = 1_048_576
EXPECTED_TOTAL_CLIQUE_CAPACITY = 5_023_824


def digest(obj) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def quotient_sizes():
    m4 = C.load(C.M4_PATH)
    out = {}
    for row in m4["four_parent_relations"]:
        gid = int(row["m4_group_id"])
        qsize = (int(row["cols"]) + 1) // 2
        old = out.setdefault(gid, qsize)
        assert old == qsize
    assert len(out) == 90
    assert sorted(g for g, n in out.items() if n == 5) == [31, 82]
    return out


def affine_scopes():
    m4 = C.load(C.M4_PATH)
    triples = tuple(tuple(map(int, row)) for row in m4["projection_minimal_empty_triples"])
    assert len(triples) == 5
    rows = triples + V.QUADS + (A.AFFINE_FIVE,) + A.EXTRA_SIX
    assert len(rows) == A.EVENT_COUNT == 19
    return tuple(tuple(map(int, row)) for row in rows)


def load_ternary_factors():
    rows = []
    for i, expected_scope in enumerate(T.TERNARY_FACTORS):
        row = json.loads((FACTOR_DIR / f"factor_{i:02d}.json").read_text())
        assert int(row["inventory_index"]) == i
        scope = tuple(map(int, row["triple"]))
        assert scope == tuple(map(int, expected_scope))
        qholes = frozenset(tuple(map(int, x)) for x in row["quotient_hole_tuples"])
        qsizes = tuple(map(int, row["quotient_alphabet_sizes"]))
        assert qholes and len(qholes) == int(row["quotient_holes"])
        rows.append({"name": f"physical_ternary:{i}", "scope": scope, "qsizes": qsizes, "forbidden": qholes})
    assert len(rows) == EXPECTED_TERNARY_COUNT
    return tuple(rows)


def elimination_cliques(scopes):
    adj = W.build_primal_graph(scopes)
    rows, fill_edges = W.deterministic_min_fill_certificate(adj)
    assert max(row["later_degree"] for row in rows) == W.EXPECTED_TREEWIDTH == 9
    assert len(fill_edges) == W.EXPECTED_FILL_EDGE_COUNT == 13
    bags = [frozenset((row["vertex"], *row["later_neighbors"])) for row in rows]
    maximal = []
    for bag in bags:
        if bag and not any(bag < other for other in bags):
            maximal.append(tuple(sorted(bag)))
    maximal = tuple(sorted(set(maximal), key=lambda row: (-len(row), row)))
    assert len(maximal) == EXPECTED_CLIQUE_COUNT
    assert max(map(len, maximal)) == 10
    return maximal, fill_edges


def maximum_intersection_forest(cliques):
    sets = tuple(map(set, cliques))
    edges = []
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
    for _weight, i, j, sep in sorted(edges, key=lambda row: (-row[0], row[1], row[2])):
        ri, rj = find(i), find(j)
        if ri == rj:
            continue
        parent[ri] = rj
        chosen.append((i, j, sep))
    assert len(chosen) == EXPECTED_FOREST_EDGES
    return tuple(chosen)


def verify_running_intersection(cliques, forest):
    cadj = defaultdict(set)
    for i, j, _sep in forest:
        cadj[i].add(j)
        cadj[j].add(i)
    for v in sorted({x for bag in cliques for x in bag}):
        members = {i for i, bag in enumerate(cliques) if v in bag}
        root = min(members)
        q = deque([root])
        seen = {root}
        while q:
            i = q.popleft()
            for j in cadj[i]:
                if j in members and j not in seen:
                    seen.add(j)
                    q.append(j)
        assert seen == members, (v, sorted(members), sorted(seen))


def assign_scope(scope, cliques):
    s = set(scope)
    candidates = [i for i, bag in enumerate(cliques) if s <= set(bag)]
    assert candidates, scope
    return min(candidates, key=lambda i: (len(cliques[i]), cliques[i], i))


def compile_tables(cliques, qsizes, ternary, affine):
    constraints = defaultdict(list)
    attachment_rows = []

    for factor in ternary:
        ci = assign_scope(factor["scope"], cliques)
        constraints[ci].append(("forbidden", factor["scope"], factor["forbidden"], factor["name"]))
        attachment_rows.append((factor["name"], ci))

    quad_scope = tuple(map(int, H.FIVE_GIDS))
    quad_allowed = frozenset(tuple(map(int, row)) for row in H.ALLOWED)
    assert len(quad_allowed) == 832
    qci = assign_scope(quad_scope, cliques)
    constraints[qci].append(("allowed", quad_scope, quad_allowed, "physical_quads:compiled5"))
    attachment_rows.append(("physical_quads:compiled5", qci))

    for ai, scope in enumerate(affine):
        ci = assign_scope(scope, cliques)
        forbidden = frozenset((tuple(qsizes[v] - 1 for v in scope),))
        constraints[ci].append(("forbidden", scope, forbidden, f"affine:{ai}"))
        attachment_rows.append((f"affine:{ai}", ci))

    assert len(attachment_rows) == 38 + 1 + 19
    tables = []
    metadata = []
    for ci, bag in enumerate(cliques):
        bag = tuple(map(int, bag))
        pos = {v: p for p, v in enumerate(bag)}
        capacity = math.prod(qsizes[v] for v in bag)
        allowed_rows = []
        for assignment in itertools.product(*(range(qsizes[v]) for v in bag)):
            ok = True
            for kind, scope, relation, _name in constraints.get(ci, ()):
                row = tuple(assignment[pos[v]] for v in scope)
                if kind == "forbidden":
                    if row in relation:
                        ok = False
                        break
                else:
                    if row not in relation:
                        ok = False
                        break
            if ok:
                allowed_rows.append(tuple(map(int, assignment)))
        allowed_rows = tuple(allowed_rows)
        assert allowed_rows, (ci, bag)
        tables.append(allowed_rows)
        metadata.append(
            {
                "clique": ci,
                "bag": list(bag),
                "capacity": capacity,
                "allowed_rows": len(allowed_rows),
                "constraints": [row[3] for row in constraints.get(ci, ())],
                "table_digest_sha256": digest([list(row) for row in allowed_rows]),
            }
        )
    return tuple(tables), tuple(metadata), tuple(sorted(attachment_rows))


def exact_junction_count(cliques, tables, forest):
    cadj = [[] for _ in cliques]
    for i, j, sep in forest:
        cadj[i].append((j, tuple(sep)))
        cadj[j].append((i, tuple(sep)))

    seen = set()
    component_counts = []
    message_rows = []
    for root in range(len(cliques)):
        if root in seen:
            continue
        parent = {root: None}
        parent_sep = {}
        order = []
        q = deque([root])
        seen.add(root)
        while q:
            i = q.popleft()
            order.append(i)
            for j, sep in cadj[i]:
                if j in parent:
                    continue
                parent[j] = i
                parent_sep[j] = sep
                seen.add(j)
                q.append(j)

        messages = {}
        for i in reversed(order):
            bag = tuple(cliques[i])
            pos = {v: p for p, v in enumerate(bag)}
            p = parent[i]
            sep_parent = tuple(parent_sep[i]) if p is not None else ()
            accum = defaultdict(int)
            for assignment in tables[i]:
                weight = 1
                for child, sep in cadj[i]:
                    if parent.get(child) != i:
                        continue
                    key = tuple(assignment[pos[v]] for v in sep)
                    weight *= int(messages[child].get(key, 0))
                    if weight == 0:
                        break
                if weight == 0:
                    continue
                key = () if p is None else tuple(assignment[pos[v]] for v in sep_parent)
                accum[key] += weight
            if p is None:
                component_counts.append(int(accum.get((), 0)))
            else:
                messages[i] = dict(accum)
                message_rows.append(
                    {
                        "child": i,
                        "parent": p,
                        "separator": list(sep_parent),
                        "positive_rows": len(accum),
                        "weight_sum": sum(accum.values()),
                    }
                )

    assert len(component_counts) == EXPECTED_COMPONENT_COUNT
    assert all(x > 0 for x in component_counts)
    return math.prod(component_counts), tuple(component_counts), tuple(message_rows)


def analyze():
    scopes = W.all_scopes()
    cliques, fill_edges = elimination_cliques(scopes)
    forest = maximum_intersection_forest(cliques)
    verify_running_intersection(cliques, forest)

    qsizes = quotient_sizes()
    capacities = [math.prod(qsizes[v] for v in bag) for bag in cliques]
    assert max(capacities) == EXPECTED_MAX_CLIQUE_CAPACITY
    assert sum(capacities) == EXPECTED_TOTAL_CLIQUE_CAPACITY

    ternary = load_ternary_factors()
    affine = affine_scopes()
    tables, metadata, attachments = compile_tables(cliques, qsizes, ternary, affine)
    total, components, messages = exact_junction_count(cliques, tables, forest)
    assert total > 0

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "exact_treewidth": W.EXPECTED_TREEWIDTH,
        "maximal_cliques": len(cliques),
        "junction_forest_edges": len(forest),
        "fill_edges": len(fill_edges),
        "largest_clique_capacity": max(capacities),
        "total_clique_capacity": sum(capacities),
        "largest_compiled_allowed_table": max(map(len, tables)),
        "total_compiled_allowed_rows": sum(map(len, tables)),
        "constraint_attachments": [list(row) for row in attachments],
        "component_assignment_counts": list(components),
        "exact_physical_plus_affine_assignment_count": int(total),
        "exact_physical_plus_affine_assignment_log2": math.log2(total),
        "max_positive_separator_rows": max((row["positive_rows"] for row in messages), default=1),
        "messages": list(messages),
        "clique_tables": list(metadata),
        "decision": "C916_CURRENT_PHYSICAL_PLUS_COMPLETE_AFFINE_COMPILE_EXACTLY_INTO_WIDTH9_JUNCTION_TABLES",
        "next_exact_step": "use these combined higher-order clique tables as a single propagation/message layer inside the exact weighted pairwise quotient recursion, with the six-factor historical checkpoint retained as a regression gate",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_CURRENT_PHYSICAL_PLUS_AFFINE_JUNCTION_COMPILER_EXACT")
    print("theorem=all current physical higher-order quotient factors and the complete 19 affine-support obstructions compile exactly into the certified width-9 chordal completion and admit exact junction-tree sum-product")
    print("boundary=this still excludes the dense 4005 pairwise quotient relation layer and multiplicity weights, so it is not the final weighted count")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
