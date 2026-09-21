#!/usr/bin/env python3
"""Prepared exact physical junction compiler through the fourth ternary tail.

Activation boundary: this file must not be promoted until the corrected tail4 quotient
matrix produces clean artifacts for all 16 targets. It then loads only nonempty exact
tail4 quotient-hole relations, adds them to the merged 48-ternary tail3-expanded physical
inventory, builds a deterministic chordal completion, and performs exact junction
sum-product for the physical higher-order layer.
"""
from __future__ import annotations

import itertools
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_compiler_exact as P
import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_forest_exact as J
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_all_known_physical_exact as H
import verify_v26_q138_c916_e0_first_dyadic_tail3_expanded_physical_junction_compiler_exact as E3
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as S

TAIL4_DIR = Path(os.environ.get("C916_TAIL4_QUOTIENT_DIR", "authorities/tail4-quotient"))
EXPECTED_TAIL4_SCOPES = (
    (4, 165, 186),
    (4, 165, 239),
    (4, 165, 244),
    (4, 165, 245),
    (4, 165, 249),
    (4, 181, 182),
    (7, 181, 182),
    (8, 181, 182),
    (9, 181, 182),
    (10, 181, 182),
    (11, 181, 182),
    (24, 181, 182),
)
EXPECTED_TAIL4_FACTOR_COUNT = len(EXPECTED_TAIL4_SCOPES)
TAIL3_PHYSICAL_COUNT = 24336193146014265408978624


def load_tail4_factors():
    files = sorted(TAIL4_DIR.glob("tail4_quotient_*.json"))
    assert len(files) == 16, (TAIL4_DIR, len(files))
    rows = [json.loads(p.read_text()) for p in files]
    by = {int(r["tail4_target"]): r for r in rows}
    assert set(by) == set(range(16))

    factors = []
    for target in range(16):
        row = by[target]
        qholes = int(row["quotient_holes"])
        promotable = bool(row["promotable_to_current_quotient_factor_inventory"])
        assert promotable == (qholes > 0)
        if qholes == 0:
            continue
        scope = tuple(map(int, row["triple"]))
        qsizes = tuple(map(int, row["quotient_alphabet_sizes"]))
        forbidden = frozenset(tuple(map(int, x)) for x in row["quotient_hole_tuples"])
        assert len(forbidden) == qholes
        factors.append({
            "name": f"tail4:{target}",
            "scope": scope,
            "qsizes": qsizes,
            "forbidden": forbidden,
            "digest": str(row["quotient_hole_digest_sha256"]),
        })

    assert len(factors) == EXPECTED_TAIL4_FACTOR_COUNT
    assert tuple(sorted(f["scope"] for f in factors)) == EXPECTED_TAIL4_SCOPES
    return tuple(factors)


def build_graph(scopes):
    adj = {}
    for scope in scopes:
        for v in scope:
            adj.setdefault(int(v), set())
        for u, v in itertools.combinations(scope, 2):
            adj[int(u)].add(int(v))
            adj[int(v)].add(int(u))
    return adj


def deterministic_min_fill(adj0):
    adj = {v: set(nbs) for v, nbs in adj0.items()}
    rows = []
    fill_edges = []
    while adj:
        candidates = []
        for v, nbs0 in adj.items():
            nbs = tuple(sorted(nbs0))
            missing = tuple((u, w) for u, w in itertools.combinations(nbs, 2) if w not in adj[u])
            candidates.append((len(missing), len(nbs), v, nbs, missing))
        _fc, degree, v, nbs, missing = min(candidates)
        rows.append({
            "vertex": v,
            "later_neighbors": list(nbs),
            "later_degree": degree,
            "fill_edges_needed": [list(x) for x in missing],
        })
        for u, w in missing:
            if w not in adj[u]:
                adj[u].add(w)
                adj[w].add(u)
                fill_edges.append((u, w))
        for u in nbs:
            adj[u].remove(v)
        del adj[v]
    return tuple(rows), tuple(fill_edges)


def assign_scope(scope, cliques):
    wanted = set(scope)
    candidates = [i for i, bag in enumerate(cliques) if wanted <= set(bag)]
    assert candidates, scope
    return min(candidates, key=lambda i: (len(cliques[i]), cliques[i], i))


def compile_tables(cliques, factors, qsizes):
    attached = defaultdict(list)
    for factor in factors:
        ci = assign_scope(factor["scope"], cliques)
        attached[ci].append(factor)

    quad_scope = tuple(map(int, H.FIVE_GIDS))
    qci = assign_scope(quad_scope, cliques)
    allowed5 = frozenset(tuple(map(int, row)) for row in H.ALLOWED)
    assert len(allowed5) == 832

    tables = []
    metadata = []
    for ci, bag0 in enumerate(cliques):
        bag = tuple(map(int, bag0))
        pos = {v: p for p, v in enumerate(bag)}
        local = tuple(attached.get(ci, ()))
        allowed = []
        for assignment in itertools.product(*(range(qsizes[v]) for v in bag)):
            ok = True
            for factor in local:
                row = tuple(assignment[pos[v]] for v in factor["scope"])
                if row in factor["forbidden"]:
                    ok = False
                    break
            if ok and ci == qci:
                qrow = tuple(assignment[pos[v]] for v in quad_scope)
                if qrow not in allowed5:
                    ok = False
            if ok:
                allowed.append(tuple(map(int, assignment)))
        assert allowed, (ci, bag)
        tables.append(tuple(allowed))
        metadata.append({
            "clique": ci,
            "bag": list(bag),
            "capacity": math.prod(qsizes[v] for v in bag),
            "allowed_rows": len(allowed),
            "factors": [f["name"] for f in local],
            "contains_compiled_five_quad_relation": ci == qci,
            "table_digest_sha256": P.digest([list(r) for r in allowed]),
        })

    names = {name for row in metadata for name in row["factors"]}
    assert names == {f["name"] for f in factors}
    return tuple(tables), tuple(metadata)


def analyze():
    frozen = P.load_ternary_factors()
    tail3 = E3.load_tail3_factors()
    tail4 = load_tail4_factors()
    factors = frozen + tail3 + tail4
    assert len(frozen) == 38
    assert len(tail3) == 10
    assert len(tail4) == 12
    assert len(factors) == 60
    scopes = [f["scope"] for f in factors]
    assert len(set(scopes)) == len(scopes)

    quads = tuple(tuple(map(int, q)) for q in T.QUATERNARY_FACTORS)
    adj = build_graph(tuple(scopes) + quads)
    rows, fill_edges = deterministic_min_fill(adj)
    upper = max(int(r["later_degree"]) for r in rows)
    clique = S.exact_maximum_clique(adj)
    lower = len(clique) - 1
    assert lower <= upper

    simple_rows = tuple((int(r["vertex"]), tuple(map(int, r["later_neighbors"]))) for r in rows)
    cliques = J.maximal_cliques(simple_rows)
    forest = J.maximum_intersection_forest(cliques)
    J.verify_running_intersection(cliques, forest)

    qsizes = J.quotient_sizes_from_m4()

    tail3_scopes = tuple(f["scope"] for f in (frozen + tail3)) + quads
    tail3_variables = {v for scope in tail3_scopes for v in scope}
    tail4_variables = {v for scope in (tuple(scopes) + quads) for v in scope}
    newly_introduced_variables = tuple(sorted(tail4_variables - tail3_variables))
    assert newly_introduced_variables == (10,)
    lift_factor = math.prod(qsizes[v] for v in newly_introduced_variables)
    lifted_tail3_count = TAIL3_PHYSICAL_COUNT * lift_factor

    tables, metadata = compile_tables(cliques, factors, qsizes)
    total, component_counts, messages = P.exact_junction_count(cliques, tables, forest)
    assert 0 < total <= lifted_tail3_count

    capacities = [math.prod(qsizes[v] for v in bag) for bag in cliques]
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "frozen_ternary_factors": len(frozen),
        "tail3_promoted_ternary_factors": len(tail3),
        "tail4_promoted_ternary_factors": len(tail4),
        "expanded_ternary_factors": len(factors),
        "physical_quaternary_factors": len(quads),
        "treewidth_lower_bound_from_maximum_clique": lower,
        "deterministic_min_fill_upper_bound": upper,
        "exact_treewidth_if_bounds_match": upper if lower == upper else None,
        "exact_maximum_clique": list(clique),
        "fill_edges": [list(x) for x in fill_edges],
        "maximal_cliques": len(cliques),
        "junction_forest_edges": len(forest),
        "largest_clique_capacity": max(capacities),
        "total_clique_capacity": sum(capacities),
        "largest_compiled_allowed_table": max(map(len, tables)),
        "total_compiled_allowed_rows": sum(map(len, tables)),
        "component_physical_assignment_counts": list(component_counts),
        "exact_tail4_expanded_physical_layer_assignment_count": int(total),
        "exact_tail4_expanded_physical_layer_assignment_log2": math.log2(total),
        "tail3_expanded_physical_layer_assignment_count": TAIL3_PHYSICAL_COUNT,
        "newly_introduced_variables_vs_tail3": list(newly_introduced_variables),
        "tail3_lift_factor_into_tail4_variable_universe": lift_factor,
        "tail3_lifted_assignment_count_in_tail4_variable_universe": lifted_tail3_count,
        "removed_assignments_vs_lifted_tail3_inventory": lifted_tail3_count - total,
        "gain_vs_lifted_tail3_inventory_log2_bits": math.log2(lifted_tail3_count) - math.log2(total),
        "max_positive_separator_message_rows": max((r["positive_message_rows"] for r in messages), default=1),
        "clique_tables": list(metadata),
        "decision": "C916_TAIL4_EXPANDED_PHYSICAL_FACTORS_EXACT_JUNCTION_COUNT",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL4_EXPANDED_PHYSICAL_JUNCTION_COMPILER_EXACT")
    print("boundary=the tail4 layer introduces gid 10, so comparison to the tail3 count is made only after lifting the tail3 authority by gid 10's quotient alphabet size; this count remains physical higher-order only and excludes pairwise, affine, and multiplicity weights")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
