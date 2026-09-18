#!/usr/bin/env python3
"""Exact junction compiler for tail3-expanded physical factors plus complete affine activity constraints."""
from __future__ import annotations

import itertools
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_compiler_exact as P
import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_forest_exact as J
import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_junction_compiler_exact as C
import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_treewidth_exact as W
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_all_known_physical_exact as H
import verify_v26_q138_c916_e0_first_dyadic_all_order_affine_support_exact as A
import verify_v26_q138_c916_e0_first_dyadic_tail3_expanded_physical_junction_compiler_exact as E
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as S

OLD_COMBINED_COUNT = 681_934_454_409_791_000_768_011_200
EXPECTED_TERNARY_COUNT = 48
EXPECTED_AFFINE_COUNT = 19


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

    assert len(attachments) == EXPECTED_TERNARY_COUNT + 1 + EXPECTED_AFFINE_COUNT

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
                    if all(state != qsizes[v] - 1 for state, v in zip(row, scope)):
                        ok = False
                        break
            if ok:
                allowed_rows.append(tuple(map(int, assignment)))

        allowed_rows = tuple(allowed_rows)
        assert allowed_rows, (ci, bag)
        tables.append(allowed_rows)
        metadata.append({
            "clique": ci,
            "bag": list(bag),
            "capacity": capacity,
            "allowed_rows": len(allowed_rows),
            "constraints": [x[3] for x in constraints.get(ci, ())],
            "table_digest_sha256": C.digest([list(row) for row in allowed_rows]),
        })

    names = {name for row in metadata for name in row["constraints"]}
    assert {f"affine:{i}" for i in range(EXPECTED_AFFINE_COUNT)} <= names
    assert "physical_quads:compiled5" in names
    return tuple(tables), tuple(metadata), tuple(sorted(attachments))


def analyze():
    old = P.load_ternary_factors()
    tail3 = E.load_tail3_factors()
    assert len(old) == 38 and len(tail3) == 10
    assert not ({f["scope"] for f in old} & {f["scope"] for f in tail3})
    ternary = old + tail3

    affine = C.affine_scopes()
    assert len(affine) == EXPECTED_AFFINE_COUNT

    scopes = tuple(W.all_scopes()) + tuple(f["scope"] for f in tail3)
    adj = W.build_primal_graph(scopes)
    rows, fill_edges = W.deterministic_min_fill_certificate(adj)
    upper = max(int(row["later_degree"]) for row in rows)
    clique = S.exact_maximum_clique(adj)
    lower = len(clique) - 1
    assert lower == upper, (lower, upper, clique)
    exact_treewidth = upper

    simple_rows = tuple((int(row["vertex"]), tuple(map(int, row["later_neighbors"]))) for row in rows)
    cliques = J.maximal_cliques(simple_rows)
    forest = J.maximum_intersection_forest(cliques)
    J.verify_running_intersection(cliques, forest)

    qsizes = J.quotient_sizes_from_m4()
    capacities = [math.prod(qsizes[v] for v in bag) for bag in cliques]
    tables, metadata, attachments = compile_tables(cliques, qsizes, ternary, affine)
    total, components, messages = C.exact_junction_count(cliques, tables, forest)
    assert 0 < total <= OLD_COMBINED_COUNT

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "affine_constraint_semantics": "all-nonzero forbidden; maximal local quotient-state index is zero",
        "frozen_ternary_factors": len(old),
        "tail3_promoted_ternary_factors": len(tail3),
        "expanded_ternary_factors": len(ternary),
        "physical_quaternary_factors": 5,
        "affine_constraints": len(affine),
        "exact_treewidth": exact_treewidth,
        "exact_maximum_clique": list(clique),
        "fill_edges": [list(map(int, x)) for x in fill_edges],
        "maximal_cliques": len(cliques),
        "junction_forest_edges": len(forest),
        "largest_clique_capacity": max(capacities),
        "total_clique_capacity": sum(capacities),
        "largest_compiled_allowed_table": max(map(len, tables)),
        "total_compiled_allowed_rows": sum(map(len, tables)),
        "constraint_attachments": [list(x) for x in attachments],
        "component_assignment_counts": list(components),
        "exact_expanded_physical_plus_affine_assignment_count": int(total),
        "exact_expanded_physical_plus_affine_assignment_log2": math.log2(total),
        "old_physical_plus_affine_assignment_count": OLD_COMBINED_COUNT,
        "removed_assignments_vs_frozen_38": OLD_COMBINED_COUNT - total,
        "gain_vs_frozen_38_log2_bits": math.log2(OLD_COMBINED_COUNT) - math.log2(total),
        "max_positive_separator_rows": max((row["positive_rows"] for row in messages), default=1),
        "clique_tables": list(metadata),
        "decision": "C916_TAIL3_EXPANDED_PHYSICAL_PLUS_COMPLETE_AFFINE_EXACT_JUNCTION_TABLES",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL3_EXPANDED_PHYSICAL_PLUS_AFFINE_JUNCTION_EXACT")
    print("theorem=the frozen physical inventory plus ten exact tail3 quotient factors and all 19 authority-correct affine activity obstructions compile into the emitted exact junction model")
    print("boundary=this excludes the dense 4005 pairwise quotient relation layer and multiplicity weights, so it is not a weighted work exponent")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
