#!/usr/bin/env python3
"""Prepared exact physical junction compiler through the fifth ternary tail.

Activation boundary: this file must not be promoted until the tail5 quotient matrix and
aggregate pass cleanly. It loads only nonempty exact tail5 quotient-hole relations, adds
them to the merged 60-ternary tail4-expanded physical inventory, builds a deterministic
chordal completion, and performs exact junction sum-product for the physical higher-order
layer. Any variables first introduced by tail5 are handled by lifting the tail4 authority
into the expanded quotient-variable universe before monotonic comparison.
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
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_junction_compiler_exact as E4
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as S

TAIL5_DIR = Path(os.environ.get("C916_TAIL5_QUOTIENT_DIR", "authorities/tail5-quotient"))
TAIL4_PHYSICAL_COUNT = 75309497737888679701161264


def load_tail5_factors():
    files = sorted(TAIL5_DIR.glob("tail5_quotient_*.json"))
    assert len(files) == 16, (TAIL5_DIR, len(files))
    rows = [json.loads(p.read_text()) for p in files]
    by = {int(r["tail5_target"]): r for r in rows}
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
        assert len(qsizes) == 3
        assert forbidden and len(forbidden) == qholes
        factors.append({
            "name": f"tail5:{target}",
            "scope": scope,
            "qsizes": qsizes,
            "forbidden": forbidden,
            "digest": str(row["quotient_hole_digest_sha256"]),
        })
    assert factors
    assert len({f["scope"] for f in factors}) == len(factors)
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
    tail4 = E4.load_tail4_factors()
    tail5 = load_tail5_factors()
    assert len(frozen) == 38
    assert len(tail3) == 10
    assert len(tail4) == 12
    assert len(tail5) == 9

    prior = frozen + tail3 + tail4
    prior_scopes = {f["scope"] for f in prior}
    tail5_scopes = {f["scope"] for f in tail5}
    assert not (prior_scopes & tail5_scopes)
    factors = prior + tail5
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
    prior_scopes_all = tuple(f["scope"] for f in prior) + quads
    expanded_scopes_all = tuple(scopes) + quads
    prior_variables = {v for scope in prior_scopes_all for v in scope}
    expanded_variables = {v for scope in expanded_scopes_all for v in scope}
    newly_introduced_variables = tuple(sorted(expanded_variables - prior_variables))
    lift_factor = math.prod(qsizes[v] for v in newly_introduced_variables)
    lifted_prior_count = TAIL4_PHYSICAL_COUNT * lift_factor

    tables, metadata = compile_tables(cliques, factors, qsizes)
    total, component_counts, messages = P.exact_junction_count(cliques, tables, forest)
    assert 0 < total <= lifted_prior_count

    capacities = [math.prod(qsizes[v] for v in bag) for bag in cliques]
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "frozen_ternary_factors": len(frozen),
        "tail3_promoted_ternary_factors": len(tail3),
        "tail4_promoted_ternary_factors": len(tail4),
        "tail5_promoted_ternary_factors": len(tail5),
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
        "exact_tail5_expanded_physical_layer_assignment_count": int(total),
        "exact_tail5_expanded_physical_layer_assignment_log2": math.log2(total),
        "tail4_expanded_physical_layer_assignment_count": TAIL4_PHYSICAL_COUNT,
        "newly_introduced_variables_vs_tail4": list(newly_introduced_variables),
        "tail4_lift_factor_into_tail5_variable_universe": lift_factor,
        "tail4_lifted_assignment_count_in_tail5_variable_universe": lifted_prior_count,
        "removed_assignments_vs_lifted_tail4_inventory": lifted_prior_count - total,
        "gain_vs_lifted_tail4_inventory_log2_bits": math.log2(lifted_prior_count) - math.log2(total),
        "max_positive_separator_message_rows": max((r["positive_message_rows"] for r in messages), default=1),
        "clique_tables": list(metadata),
        "decision": "C916_TAIL5_EXPANDED_PHYSICAL_FACTORS_EXACT_JUNCTION_COUNT",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL5_EXPANDED_PHYSICAL_JUNCTION_COMPILER_EXACT")
    print("boundary=activation requires the clean tail5 quotient aggregate; prior-count comparison is made only after lifting any newly introduced quotient variables")
    print("boundary=this count remains physical higher-order only and excludes pairwise, affine, and multiplicity weights")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
