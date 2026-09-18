#!/usr/bin/env python3
"""Aggregate exact tail3 quotient results and scout the expanded physical topology.

Only targets with a nonempty exactly certified quotient-hole relation are added to the
structural candidate inventory.  The topology section reports a deterministic min-fill
upper bound and an exact maximum-clique lower bound; it calls the treewidth exact only if
those independently meet.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as TOPO

SUMMARY_DIR = Path(os.environ.get("C916_PHYSICAL_QUOTIENT_TAIL3_SUMMARY_DIR", "tail3-quotient-summaries"))


def build_graph(scopes):
    adj = {}
    for scope in scopes:
        scope = tuple(map(int, scope))
        assert len(scope) == len(set(scope))
        for v in scope:
            adj.setdefault(v, set())
        for u, v in itertools.combinations(scope, 2):
            adj[u].add(v)
            adj[v].add(u)
    return adj


def exact_maximum_clique(adj):
    best = ()

    def visit(r, p, x):
        nonlocal best
        if len(r) + len(p) <= len(best):
            return
        if not p and not x:
            cand = tuple(sorted(r))
            if len(cand) > len(best) or (len(cand) == len(best) and cand < best):
                best = cand
            return
        union = p | x
        pivot = max(union, key=lambda u: len(p & adj[u])) if union else None
        candidates = sorted(p - (adj[pivot] if pivot is not None else set()))
        for v in candidates:
            visit(r | {v}, p & adj[v], x & adj[v])
            p.remove(v)
            x.add(v)
            if len(r) + len(p) <= len(best):
                break

    visit(set(), set(adj), set())
    return best


def scope_digest(triples, quads):
    payload = json.dumps(
        {"quads": [list(x) for x in sorted(quads)], "triples": [list(x) for x in sorted(triples)]},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def analyze():
    files = sorted(SUMMARY_DIR.glob("tail3_quotient_*.json"))
    assert len(files) == 16, (SUMMARY_DIR, len(files))
    rows = [json.loads(path.read_text()) for path in files]
    by_target = {int(row["tail3_target"]): row for row in rows}
    assert len(by_target) == 16 and set(by_target) == set(range(16))
    rows = [by_target[i] for i in range(16)]

    triples = [tuple(map(int, row["triple"])) for row in rows]
    assert len(set(triples)) == 16
    for row in rows:
        assert bool(row["promotable_to_current_quotient_factor_inventory"]) == (int(row["quotient_holes"]) > 0)

    promotable = [row for row in rows if int(row["quotient_holes"]) > 0]
    sign_only = [row for row in rows if int(row["raw_holes"]) > 0 and int(row["quotient_holes"]) == 0]
    pairwise_complete = [row for row in rows if int(row["raw_holes"]) == 0]

    old_triples = tuple(tuple(map(int, x)) for x in TOPO.TERNARY_FACTORS)
    old_set = set(old_triples)
    promoted_scopes = tuple(tuple(map(int, row["triple"])) for row in promotable)
    duplicate_scopes = tuple(sorted(scope for scope in promoted_scopes if scope in old_set))
    new_scopes = tuple(sorted(scope for scope in promoted_scopes if scope not in old_set))
    expanded_triples = tuple(sorted(set(old_triples) | set(new_scopes)))
    quads = tuple(tuple(map(int, x)) for x in TOPO.QUATERNARY_FACTORS)

    adj = build_graph(expanded_triples + quads)
    edge_count = sum(len(vs) for vs in adj.values()) // 2
    components = TOPO.connected_components(adj)
    _order, elimination_rows, fill_edges = TOPO.deterministic_min_fill_certificate(adj)
    upper = max((int(row["later_degree"]) for row in elimination_rows), default=0)
    clique = exact_maximum_clique(adj)
    lower = max(0, len(clique) - 1)
    exact_width = upper if upper == lower else None

    promoted_rows = [
        {
            "tail3_target": int(row["tail3_target"]),
            "triple": list(map(int, row["triple"])),
            "raw_holes": int(row["raw_holes"]),
            "quotient_holes": int(row["quotient_holes"]),
            "quotient_hole_digest_sha256": str(row["quotient_hole_digest_sha256"]),
        }
        for row in promotable
    ]
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "tail3_targets": 16,
        "tail3_promotable_quotient_factors": len(promotable),
        "tail3_sign_only_raw_obstructions": len(sign_only),
        "tail3_pairwise_complete_targets": len(pairwise_complete),
        "tail3_total_quotient_holes": sum(int(row["quotient_holes"]) for row in promotable),
        "promotable_rows": promoted_rows,
        "promotable_scopes_already_in_frozen_38": [list(x) for x in duplicate_scopes],
        "new_promotable_scopes": [list(x) for x in new_scopes],
        "frozen_ternary_factor_count": len(old_triples),
        "expanded_candidate_ternary_factor_count": len(expanded_triples),
        "quaternary_factor_count": len(quads),
        "expanded_scope_digest_sha256": scope_digest(expanded_triples, quads),
        "expanded_primal_variables": len(adj),
        "expanded_primal_edges": edge_count,
        "expanded_component_sizes": [len(x) for x in components],
        "exact_maximum_clique": list(clique),
        "treewidth_lower_bound_from_maximum_clique": lower,
        "deterministic_min_fill_upper_bound": upper,
        "min_fill_edges_added": len(fill_edges),
        "exact_treewidth_if_bounds_match": exact_width,
        "decision": (
            "TAIL3_EXACT_QUOTIENT_PROMOTION_SCOUT_WITH_MATCHING_TREEWIDTH_CERTIFICATE"
            if exact_width is not None
            else "TAIL3_EXACT_QUOTIENT_PROMOTION_SCOUT_WITH_TREEWIDTH_BOUNDS"
        ),
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_TAIL3_SUMMARY")
    if exact_width is not None:
        print("theorem=for the exactly promotable tail3 quotient relations, the expanded physical-factor primal graph has exact treewidth equal to the matching maximum-clique lower bound and deterministic elimination upper bound")
    else:
        print("boundary=the quotient relations are exact, but the expanded topology currently has only the reported clique lower bound and elimination upper bound; no exact treewidth is claimed")
    print("boundary=this is a structural scout only; the new candidate factors are not yet included in the frozen weighted all-current count")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
