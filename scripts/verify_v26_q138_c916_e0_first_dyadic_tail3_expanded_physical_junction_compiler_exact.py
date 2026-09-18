#!/usr/bin/env python3
"""Compile the frozen physical layer plus ten exact tail3 quotient factors into width-6 junction tables."""
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

TAIL3_DIR = Path(os.environ.get("C916_TAIL3_QUOTIENT_DIR", "authorities/tail3-quotient"))
OLD_PHYSICAL_COUNT = 31704503579053764899189904
EXPECTED_TAIL3_SCOPES = (
    (4, 11, 165), (4, 24, 165), (4, 62, 165), (4, 67, 165), (4, 111, 165),
    (4, 113, 165), (4, 114, 165), (4, 136, 165), (4, 144, 165), (4, 165, 181),
)


def load_tail3_factors():
    files = sorted(TAIL3_DIR.glob("tail3_quotient_*.json"))
    assert len(files) == 16, (TAIL3_DIR, len(files))
    rows = [json.loads(p.read_text()) for p in files]
    by = {int(r["tail3_target"]): r for r in rows}
    assert set(by) == set(range(16))
    out = []
    for target in range(16):
        row = by[target]
        if int(row["quotient_holes"]) == 0:
            continue
        scope = tuple(map(int, row["triple"]))
        qsizes = tuple(map(int, row["quotient_alphabet_sizes"]))
        forbidden = frozenset(tuple(map(int, x)) for x in row["quotient_hole_tuples"])
        assert forbidden and len(forbidden) == int(row["quotient_holes"])
        out.append({
            "name": f"tail3:{target}",
            "scope": scope,
            "qsizes": qsizes,
            "forbidden": forbidden,
            "digest": str(row["quotient_hole_digest_sha256"]),
        })
    assert tuple(sorted(x["scope"] for x in out)) == EXPECTED_TAIL3_SCOPES
    return tuple(out)


def build_graph(scopes):
    adj = {}
    for scope in scopes:
        for v in scope:
            adj.setdefault(int(v), set())
        for u, v in itertools.combinations(scope, 2):
            adj[int(u)].add(int(v))
            adj[int(v)].add(int(u))
    return adj


def min_fill_rows(adj0):
    adj = {v: set(nbs) for v, nbs in adj0.items()}
    rows = []
    fills = []
    while adj:
        candidates = []
        for v, nbs0 in adj.items():
            nbs = tuple(sorted(nbs0))
            missing = tuple((u, w) for u, w in itertools.combinations(nbs, 2) if w not in adj[u])
            candidates.append((len(missing), len(nbs), v, nbs, missing))
        _fc, _deg, v, nbs, missing = min(candidates)
        rows.append((v, nbs))
        for u, w in missing:
            adj[u].add(w)
            adj[w].add(u)
            fills.append((u, w))
        for u in nbs:
            adj[u].remove(v)
        del adj[v]
    return tuple(rows), tuple(fills)


def compile_tables(cliques, factors, qsizes):
    attached = defaultdict(list)
    for factor in factors:
        ci = P.assign_factor_to_clique(factor["scope"], cliques)
        attached[ci].append(factor)

    quad_scope = tuple(map(int, H.FIVE_GIDS))
    qci = P.assign_factor_to_clique(quad_scope, cliques)
    allowed5 = frozenset(tuple(map(int, row)) for row in H.ALLOWED)
    assert len(allowed5) == 832

    tables = []
    attachments = []
    for ci, bag0 in enumerate(cliques):
        bag = tuple(map(int, bag0))
        pos = {v: p for p, v in enumerate(bag)}
        allowed = []
        local = tuple(attached.get(ci, ()))
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
        attachments.append({
            "clique": ci,
            "bag": list(bag),
            "capacity": math.prod(qsizes[v] for v in bag),
            "allowed_rows": len(allowed),
            "factors": [f["name"] for f in local],
            "contains_compiled_five_quad_relation": ci == qci,
            "table_digest_sha256": P.digest([list(r) for r in allowed]),
        })

    names = {name for row in attachments for name in row["factors"]}
    assert names == {f["name"] for f in factors}
    assert sum(bool(row["contains_compiled_five_quad_relation"]) for row in attachments) == 1
    return tuple(tables), tuple(attachments), qci


def analyze():
    old = P.load_ternary_factors()
    tail3 = load_tail3_factors()
    assert not ({f["scope"] for f in old} & {f["scope"] for f in tail3})
    factors = old + tail3

    scopes = tuple(f["scope"] for f in factors) + tuple(tuple(map(int, q)) for q in T.QUATERNARY_FACTORS)
    adj = build_graph(scopes)
    rows, fill_edges = min_fill_rows(adj)
    width = max(len(nbs) for _v, nbs in rows)
    assert width == 6
    assert len(fill_edges) == 1

    cliques = J.maximal_cliques(rows)
    forest = J.maximum_intersection_forest(cliques)
    J.verify_running_intersection(cliques, forest)
    components = T.connected_components(adj)
    assert tuple(len(c) for c in components) == (28, 3, 3, 3, 3, 3)
    assert len(cliques) - len(forest) == 6

    qsizes = J.quotient_sizes_from_m4()
    tables, attachments, qci = compile_tables(cliques, factors, qsizes)
    total, component_counts, messages = P.exact_junction_count(cliques, tables, forest)
    assert 0 < total <= OLD_PHYSICAL_COUNT

    capacities = [math.prod(qsizes[v] for v in bag) for bag in cliques]
    allowed_sizes = [len(tab) for tab in tables]
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "frozen_ternary_factors": len(old),
        "tail3_promoted_ternary_factors": len(tail3),
        "expanded_ternary_factors": len(factors),
        "physical_quaternary_factors": len(T.QUATERNARY_FACTORS),
        "deterministic_triangulation_width": width,
        "fill_edges": [list(x) for x in fill_edges],
        "maximal_cliques": len(cliques),
        "junction_forest_edges": len(forest),
        "compiled_quad_clique": qci,
        "clique_table_capacity_sum": sum(capacities),
        "clique_table_allowed_rows_sum": sum(allowed_sizes),
        "largest_clique_capacity": max(capacities),
        "largest_compiled_allowed_table": max(allowed_sizes),
        "component_physical_assignment_counts": list(component_counts),
        "exact_expanded_physical_layer_assignment_count": int(total),
        "exact_expanded_physical_layer_assignment_log2": math.log2(total),
        "old_physical_layer_assignment_count": OLD_PHYSICAL_COUNT,
        "removed_assignments_vs_frozen_38": OLD_PHYSICAL_COUNT - total,
        "gain_vs_frozen_38_log2_bits": math.log2(OLD_PHYSICAL_COUNT) - math.log2(total),
        "max_positive_separator_message_rows": max((r["positive_message_rows"] for r in messages), default=1),
        "attachments": list(attachments),
        "decision": "C916_FROZEN_PLUS_TAIL3_EXACT_PHYSICAL_FACTORS_COMPILE_INTO_WIDTH6_JUNCTION_TABLES",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL3_EXPANDED_PHYSICAL_JUNCTION_COMPILER_EXACT")
    print("theorem=the frozen 38 ternary physical quotient factors, ten exact tail3 promoted ternaries, and the five exact quaternary factors compile into an exact width-6 junction forest whose sum-product count is the emitted integer")
    print("boundary=this is the physical higher-order layer alone; dense pairwise relations, affine constraints, and multiplicity weights are not folded into this count")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
