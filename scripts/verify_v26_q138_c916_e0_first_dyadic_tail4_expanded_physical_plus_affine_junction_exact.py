#!/usr/bin/env python3
"""Exact junction compiler for tail4-expanded physical factors plus complete affine activity constraints."""
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
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_junction_compiler_exact as E4
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as S

OLD_COMBINED_COUNT = 610_168_911_320_611_717_122_698_496
EXPECTED_TERNARY_COUNT = 60
EXPECTED_AFFINE_COUNT = 19


def beam_elimination_certificate(adj0, beam_width=512, branch_factor=6):
    """Deterministically search for a narrower chordal completion.

    This is an upper-bound search only. Any returned ordering is explicitly verified by
    replay because a heuristic failure must never be promoted to a lower-bound claim.
    """
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
                    max(width, len(nbs)),
                    len(missing),
                    len(nbs),
                    v,
                    nbs,
                    missing,
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
                score = (nwidth, nfill_total, sum(len(ns) for ns in nadj.values()), tuple(x["vertex"] for x in nrows))
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
    tail4 = E4.load_tail4_factors()
    assert len(old) == 38 and len(tail3) == 10 and len(tail4) == 12
    old_scopes = {f["scope"] for f in old}
    tail3_scopes = {f["scope"] for f in tail3}
    tail4_scopes = {f["scope"] for f in tail4}
    assert not (old_scopes & tail3_scopes)
    assert not (old_scopes & tail4_scopes)
    assert not (tail3_scopes & tail4_scopes)
    ternary = old + tail3 + tail4

    affine = C.affine_scopes()
    assert len(affine) == EXPECTED_AFFINE_COUNT

    scopes = tuple(W.all_scopes()) + tuple(f["scope"] for f in tail3) + tuple(f["scope"] for f in tail4)
    adj = W.build_primal_graph(scopes)
    deterministic_rows, deterministic_fill_edges = W.deterministic_min_fill_certificate(adj)
    deterministic_upper = max(int(row["later_degree"]) for row in deterministic_rows)
    beam_rows, beam_fill_edges, beam_upper = beam_elimination_certificate(
        adj, beam_width=2048, branch_factor=10
    )
    if beam_upper < deterministic_upper:
        rows, fill_edges = beam_rows, beam_fill_edges
        upper = beam_upper
        elimination_source = "deterministic_beam_2048x10"
    else:
        rows, fill_edges = deterministic_rows, deterministic_fill_edges
        upper = deterministic_upper
        elimination_source = "deterministic_min_fill"
    clique = S.exact_maximum_clique(adj)
    lower = len(clique) - 1
    assert lower <= upper, (lower, upper, clique)
    exact_treewidth = upper if lower == upper else None

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
        "tail4_promoted_ternary_factors": len(tail4),
        "expanded_ternary_factors": len(ternary),
        "physical_quaternary_factors": 5,
        "affine_constraints": len(affine),
        "treewidth_lower_bound_from_maximum_clique": lower,
        "deterministic_min_fill_upper_bound": deterministic_upper,
        "beam_search_upper_bound": beam_upper,
        "selected_elimination_upper_bound": upper,
        "selected_elimination_source": elimination_source,
        "exact_treewidth_if_bounds_match": exact_treewidth,
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
        "tail3_physical_plus_affine_assignment_count": OLD_COMBINED_COUNT,
        "removed_assignments_vs_tail3_inventory": OLD_COMBINED_COUNT - total,
        "gain_vs_tail3_inventory_log2_bits": math.log2(OLD_COMBINED_COUNT) - math.log2(total),
        "max_positive_separator_rows": max((row["positive_rows"] for row in messages), default=1),
        "clique_tables": list(metadata),
        "decision": (
            "C916_TAIL4_EXPANDED_PHYSICAL_PLUS_COMPLETE_AFFINE_EXACT_JUNCTION_TABLES_WITH_EXACT_TREEWIDTH"
            if exact_treewidth is not None
            else "C916_TAIL4_EXPANDED_PHYSICAL_PLUS_COMPLETE_AFFINE_EXACT_JUNCTION_TABLES_WITH_TREEWIDTH_BOUNDS"
        ),
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL4_EXPANDED_PHYSICAL_PLUS_AFFINE_JUNCTION_EXACT")
    print("theorem=the frozen physical inventory plus ten exact tail3 and twelve exact tail4 quotient factors and all 19 authority-correct affine activity obstructions compile exactly into the emitted chordal junction model")
    if exact_treewidth is None:
        print("boundary=treewidth is not claimed exact; the emitted maximum-clique lower bound and deterministic elimination upper bound remain distinct")
    print("boundary=this excludes the dense 4005 pairwise quotient relation layer and multiplicity weights, so it is not a weighted work exponent")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
