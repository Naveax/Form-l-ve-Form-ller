#!/usr/bin/env python3
"""Aggregate exact tail7 quotient results against all previously promoted physical tails."""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as TOPO
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_treewidth8_exact as T4
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail6 as S6
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as T3

SUMMARY_DIR = Path(os.environ.get("C916_PHYSICAL_QUOTIENT_TAIL7_SUMMARY_DIR", "tail7-quotient-summaries"))
TAIL5_DIR = Path(os.environ.get("C916_TAIL5_QUOTIENT_DIR", "authorities/tail5-quotient"))
TAIL6_DIR = Path(os.environ.get("C916_TAIL6_QUOTIENT_DIR", "authorities/tail6-quotient"))


def scope_digest(triples, quads):
    payload = json.dumps(
        {"quads": [list(x) for x in sorted(quads)], "triples": [list(x) for x in sorted(triples)]},
        sort_keys=True, separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def load_promoted(directory: Path, prefix: str, target_key: str):
    files = sorted(directory.glob(f"{prefix}_*.json"))
    assert len(files) == 16, (directory, len(files))
    rows = [json.loads(p.read_text()) for p in files]
    by = {int(r[target_key]): r for r in rows}
    assert set(by) == set(range(16))
    scopes = []
    for i in range(16):
        row = by[i]
        qholes = int(row["quotient_holes"])
        raw_holes = int(row["raw_holes"])
        assert bool(row["promotable_to_current_quotient_factor_inventory"]) == (qholes > 0)
        forbidden = tuple(tuple(map(int, x)) for x in row["quotient_hole_tuples"])
        assert len(forbidden) == qholes
        if qholes:
            scopes.append(tuple(map(int, row["triple"])))
        elif raw_holes:
            assert "SIGN_ONLY" in str(row["decision"])
        else:
            assert "PAIRWISE_COMPLETE_NEGATIVE_CONTROL" in str(row["decision"])
    assert len(scopes) == len(set(scopes))
    return tuple(sorted(scopes))


def analyze():
    files = sorted(SUMMARY_DIR.glob("tail7_quotient_*.json"))
    assert len(files) == 16, (SUMMARY_DIR, len(files))
    rows = [json.loads(p.read_text()) for p in files]
    by = {int(r["tail7_target"]): r for r in rows}
    assert set(by) == set(range(16))
    rows = [by[i] for i in range(16)]

    for r in rows:
        qholes = int(r["quotient_holes"])
        raw_holes = int(r["raw_holes"])
        assert bool(r["promotable_to_current_quotient_factor_inventory"]) == (qholes > 0)
        assert len(r["quotient_hole_tuples"]) == qholes
        if qholes:
            assert "DESCENDS_TO_SIGN_REFLECTION_QUOTIENT" in str(r["decision"])
        elif raw_holes:
            assert "SIGN_ONLY" in str(r["decision"])
        else:
            assert "PAIRWISE_COMPLETE_NEGATIVE_CONTROL" in str(r["decision"])

    promotable = [r for r in rows if int(r["quotient_holes"]) > 0]
    sign_only = [r for r in rows if int(r["raw_holes"]) > 0 and int(r["quotient_holes"]) == 0]
    pairwise_complete = [r for r in rows if int(r["raw_holes"]) == 0]
    assert len(promotable) + len(sign_only) + len(pairwise_complete) == 16

    frozen = tuple(tuple(map(int, x)) for x in TOPO.TERNARY_FACTORS)
    tail5 = load_promoted(TAIL5_DIR, "tail5_quotient", "tail5_target")
    assert len(tail5) == 9
    tail6 = load_promoted(TAIL6_DIR, "tail6_quotient", "tail6_target")
    admitted = tuple(T4.TAIL3) + tuple(T4.TAIL4) + tail5 + tail6
    assert not (set(frozen) & set(admitted))
    current = tuple(sorted(set(frozen) | set(admitted)))

    tail7_scopes = tuple(sorted(tuple(map(int, r["triple"])) for r in promotable))
    duplicate = tuple(sorted(set(tail7_scopes) & set(current)))
    new = tuple(sorted(set(tail7_scopes) - set(current)))
    assert not duplicate
    expanded = tuple(sorted(set(current) | set(new)))
    quads = tuple(tuple(map(int, x)) for x in TOPO.QUATERNARY_FACTORS)

    adj = T3.build_graph(expanded + quads)
    edge_count = sum(len(v) for v in adj.values()) // 2
    comps = TOPO.connected_components(adj)
    _order, erows, fill = TOPO.deterministic_min_fill_certificate(adj)
    upper = max((int(r["later_degree"]) for r in erows), default=0)
    clique = T3.exact_maximum_clique(adj)
    lower = max(0, len(clique) - 1)

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "tail7_targets": 16,
        "tail7_promotable_quotient_factors": len(promotable),
        "tail7_sign_only_raw_obstructions": len(sign_only),
        "tail7_pairwise_complete_targets": len(pairwise_complete),
        "tail7_total_quotient_holes": sum(int(r["quotient_holes"]) for r in promotable),
        "promotable_rows": [{
            "tail7_target": int(r["tail7_target"]),
            "triple": list(map(int, r["triple"])),
            "raw_holes": int(r["raw_holes"]),
            "quotient_holes": int(r["quotient_holes"]),
            "quotient_hole_digest_sha256": str(r["quotient_hole_digest_sha256"]),
        } for r in promotable],
        "promotable_scopes_already_known": [list(x) for x in duplicate],
        "new_promotable_scopes": [list(x) for x in new],
        "current_ternary_factor_count": len(current),
        "expanded_candidate_ternary_factor_count": len(expanded),
        "quaternary_factor_count": len(quads),
        "expanded_scope_digest_sha256": scope_digest(expanded, quads),
        "expanded_primal_variables": len(adj),
        "expanded_primal_edges": edge_count,
        "expanded_component_sizes": [len(x) for x in comps],
        "exact_maximum_clique": list(clique),
        "treewidth_lower_bound_from_maximum_clique": lower,
        "deterministic_min_fill_upper_bound": upper,
        "min_fill_edges_added": len(fill),
        "exact_treewidth_if_bounds_match": upper if upper == lower else None,
        "decision": (
            "TAIL7_EXACT_QUOTIENT_PROMOTION_SCOUT_WITH_MATCHING_TREEWIDTH_CERTIFICATE"
            if upper == lower else "TAIL7_EXACT_QUOTIENT_PROMOTION_SCOUT_WITH_TREEWIDTH_BOUNDS"
        ),
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_TAIL7_SUMMARY")
    print("boundary=tail7 relations remain candidate additions until exact quotient jobs and aggregate pass; no weighted count is inferred")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
