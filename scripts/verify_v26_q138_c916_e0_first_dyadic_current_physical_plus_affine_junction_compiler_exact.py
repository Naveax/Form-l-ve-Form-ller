#!/usr/bin/env python3
"""Compile the current physical + complete affine-support layer with correct activity semantics.

The combined higher-order topology is the already-certified width-9 primal graph. This
verifier compiles the 38 exact ternary physical quotient factors, the exact conjunction
of the five quaternary physical factors, and all 19 affine-support obstructions into that
junction forest.

Affine semantics are authority-critical: an affine scope is forbidden when every endpoint
is NONZERO in the sign-reflection quotient. The maximal local quotient-state index is the
zero state, and any zero endpoint clears the affine conflict. The earlier singleton
all-zero translation was the opposite relation and is intentionally rejected here.

The resulting count is for the combined higher-order layer only. The dense 4,005 pairwise
quotient relation layer and multiplicity weights remain outside this verifier.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from collections import defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_compiler_exact as P
import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_forest_exact as J
import verify_v26_q138_c916_e0_first_dyadic_projection_hyperedges_eventmask_vector_exact as V
import verify_v26_q138_c916_e0_first_dyadic_all_order_affine_support_exact as A
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_all_known_physical_exact as H
import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_treewidth_exact as W

EXPECTED_TERNARY_COUNT = 38
EXPECTED_CLIQUE_COUNT = 26
EXPECTED_COMPONENT_COUNT = 5
EXPECTED_FOREST_EDGES = EXPECTED_CLIQUE_COUNT - EXPECTED_COMPONENT_COUNT
EXPECTED_MAX_CLIQUE_CAPACITY = 1_048_576
EXPECTED_TOTAL_CLIQUE_CAPACITY = 5_023_824


def digest(obj) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def affine_scopes():
    m4 = P.J.C.load(P.J.C.M4_PATH)
    triples = tuple(tuple(map(int, row)) for row in m4["projection_minimal_empty_triples"])
    assert len(triples) == 5
    rows = triples + V.QUADS + (A.AFFINE_FIVE,) + A.EXTRA_SIX
    assert len(rows) == A.EVENT_COUNT == 19
    assert A.Q.digest_rows(tuple(sorted(rows, key=lambda r: (len(r), tuple(r))))) == A.EXPECTED_CONFLICT_DIGEST
    return tuple(tuple(map(int, row)) for row in rows)


def build_cliques_and_forest():
    scopes = W.all_scopes()
    adj = W.build_primal_graph(scopes)
    rows, fill_edges = W.deterministic_min_fill_certificate(adj)
    assert max(row["later_degree"] for row in rows) == W.EXPECTED_TREEWIDTH == 9
    assert len(fill_edges) == W.EXPECTED_FILL_EDGE_COUNT == 13

    simple_rows = tuple((int(row["vertex"]), tuple(map(int, row["later_neighbors"]))) for row in rows)
    cliques = J.maximal_cliques(simple_rows)
    assert len(cliques) == EXPECTED_CLIQUE_COUNT
    assert max(map(len, cliques)) == 10

    forest = J.maximum_intersection_forest(cliques)
    assert len(forest) == EXPECTED_FOREST_EDGES
    J.verify_running_intersection(cliques, forest)
    return cliques, forest, tuple(fill_edges)


def assign_scope(scope, cliques):
    wanted = set(scope)
    candidates = [i for i, bag in enumerate(cliques) if wanted <= set(bag)]
    assert candidates, scope
    return min(candidates, key=lambda i: (len(cliques[i]), cliques[i], i))


def compile_tables(cliques, qsizes, ternary, affine):
    constraints = defaultdict(list)
    attachments = []

    for factor in ternary:
        ci = assign_scope(factor["scope"], cliques)
        name = str(factor["name"])
        constraints[ci].append(("finite_forbidden", factor["scope"], factor["forbidden"], name))
        attachments.append((name, ci))

    quad_scope = tuple(map(int, H.FIVE_GIDS))
    quad_allowed = frozenset(tuple(map(int, row)) for row in H.ALLOWED)
    assert len(quad_allowed) == 832
    qci = assign_scope(quad_scope, cliques)
    constraints[qci].append(("allowed", quad_scope, quad_allowed, "physical_quads:compiled5"))
    attachments.append(("physical_quads:compiled5", qci))

    for ai, scope in enumerate(affine):
        ci = assign_scope(scope, cliques)
        constraints[ci].append(("affine_all_nonzero_forbidden", scope, None, f"affine:{ai}"))
        attachments.append((f"affine:{ai}", ci))

    assert len(attachments) == EXPECTED_TERNARY_COUNT + 1 + A.EVENT_COUNT

    tables = []
    metadata = []
    for ci, raw_bag in enumerate(cliques):
        bag = tuple(map(int, raw_bag))
        pos = {v: p for p, v in enumerate(bag)}
        capacity = math.prod(qsizes[v] for v in bag)
        allowed_rows = []

        for assignment in itertools.product(*(range(qsizes[v]) for v in bag)):
            ok = True
            for kind, scope, relation, _name in constraints.get(ci, ()):
                row = tuple(assignment[pos[v]] for v in scope)
                if kind == "finite_forbidden":
                    if row in relation:
                        ok = False
                        break
                elif kind == "allowed":
                    if row not in relation:
                        ok = False
                        break
                else:
                    assert kind == "affine_all_nonzero_forbidden"
                    # Zero is the maximal quotient-state index. A conflict survives
                    # exactly when every endpoint is nonzero.
                    if all(state != qsizes[v] - 1 for state, v in zip(row, scope)):
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

    return tuple(tables), tuple(metadata), tuple(sorted(attachments))


def exact_junction_count(cliques, tables, forest):
    cadj = [[] for _ in cliques]
    for i, j, sep in forest:
        sep = tuple(map(int, sep))
        cadj[i].append((j, sep))
        cadj[j].append((i, sep))

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
    cliques, forest, fill_edges = build_cliques_and_forest()
    qsizes = J.quotient_sizes_from_m4()
    capacities = [math.prod(qsizes[v] for v in bag) for bag in cliques]
    assert max(capacities) == EXPECTED_MAX_CLIQUE_CAPACITY
    assert sum(capacities) == EXPECTED_TOTAL_CLIQUE_CAPACITY

    ternary = P.load_ternary_factors()
    assert len(ternary) == EXPECTED_TERNARY_COUNT
    affine = affine_scopes()
    tables, metadata, attachments = compile_tables(cliques, qsizes, ternary, affine)
    total, components, messages = exact_junction_count(cliques, tables, forest)
    assert total > 0

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "affine_constraint_semantics": "all-nonzero forbidden; maximal local quotient-state index is zero",
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
        "decision": "C916_CURRENT_PHYSICAL_PLUS_COMPLETE_AFFINE_ACTIVITY_CORRECT_WIDTH9_JUNCTION_TABLES",
        "next_exact_step": "use these authority-correct combined higher-order relations inside the exact weighted pairwise quotient recursion, retaining the six-factor historical checkpoint as a regression gate",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_CURRENT_PHYSICAL_PLUS_AFFINE_JUNCTION_COMPILER_EXACT")
    print("theorem=all current physical higher-order quotient factors and the complete 19 affine all-nonzero activity obstructions compile exactly into the certified width-9 chordal completion and admit exact junction-tree sum-product")
    print("boundary=this excludes the dense 4005 pairwise quotient relation layer and multiplicity weights, so it is not the final weighted count")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
