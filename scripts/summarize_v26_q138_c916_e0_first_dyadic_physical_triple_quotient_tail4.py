#!/usr/bin/env python3
"""Aggregate exact tail4 quotient results and update candidate physical topology bounds."""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as TOPO
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as T3

SUMMARY_DIR = Path(os.environ.get("C916_PHYSICAL_QUOTIENT_TAIL4_SUMMARY_DIR", "tail4-quotient-summaries"))
TAIL3_PROMOTED = (
    (4, 11, 165), (4, 24, 165), (4, 62, 165), (4, 67, 165), (4, 111, 165),
    (4, 113, 165), (4, 114, 165), (4, 136, 165), (4, 144, 165), (4, 165, 181),
)


def scope_digest(triples, quads):
    payload=json.dumps({"quads":[list(x) for x in sorted(quads)],"triples":[list(x) for x in sorted(triples)]},sort_keys=True,separators=(",",":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def analyze():
    files=sorted(SUMMARY_DIR.glob("tail4_quotient_*.json"))
    assert len(files)==16, (SUMMARY_DIR,len(files))
    rows=[json.loads(p.read_text()) for p in files]
    by={int(r["tail4_target"]):r for r in rows}
    assert set(by)==set(range(16))
    rows=[by[i] for i in range(16)]
    promotable=[r for r in rows if int(r["quotient_holes"])>0]
    sign_only=[r for r in rows if int(r["raw_holes"])>0 and int(r["quotient_holes"])==0]
    pairwise_complete=[r for r in rows if int(r["raw_holes"])==0]

    old=tuple(tuple(map(int,x)) for x in TOPO.TERNARY_FACTORS)
    assert not (set(TAIL3_PROMOTED) & set(old))
    tail4_scopes=tuple(sorted(tuple(map(int,r["triple"])) for r in promotable))
    dup=tuple(sorted(set(tail4_scopes) & (set(old)|set(TAIL3_PROMOTED))))
    new=tuple(sorted(set(tail4_scopes) - set(old) - set(TAIL3_PROMOTED)))
    expanded=tuple(sorted(set(old)|set(TAIL3_PROMOTED)|set(new)))
    quads=tuple(tuple(map(int,x)) for x in TOPO.QUATERNARY_FACTORS)

    adj=T3.build_graph(expanded+quads)
    edge_count=sum(len(v) for v in adj.values())//2
    comps=TOPO.connected_components(adj)
    _order, erows, fill=TOPO.deterministic_min_fill_certificate(adj)
    upper=max((int(r["later_degree"]) for r in erows),default=0)
    clique=T3.exact_maximum_clique(adj)
    lower=max(0,len(clique)-1)
    exact=upper if upper==lower else None

    out={
        "position":"C","physical_shared_dimension":149,
        "tail4_targets":16,
        "tail4_promotable_quotient_factors":len(promotable),
        "tail4_sign_only_raw_obstructions":len(sign_only),
        "tail4_pairwise_complete_targets":len(pairwise_complete),
        "tail4_total_quotient_holes":sum(int(r["quotient_holes"]) for r in promotable),
        "promotable_rows":[{
            "tail4_target":int(r["tail4_target"]),"triple":list(map(int,r["triple"])),
            "raw_holes":int(r["raw_holes"]),"quotient_holes":int(r["quotient_holes"]),
            "quotient_hole_digest_sha256":str(r["quotient_hole_digest_sha256"])
        } for r in promotable],
        "promotable_scopes_already_known":[list(x) for x in dup],
        "new_promotable_scopes":[list(x) for x in new],
        "frozen_ternary_factor_count":len(old),
        "tail3_promoted_factor_count":len(TAIL3_PROMOTED),
        "expanded_candidate_ternary_factor_count":len(expanded),
        "quaternary_factor_count":len(quads),
        "expanded_scope_digest_sha256":scope_digest(expanded,quads),
        "expanded_primal_variables":len(adj),
        "expanded_primal_edges":edge_count,
        "expanded_component_sizes":[len(x) for x in comps],
        "exact_maximum_clique":list(clique),
        "treewidth_lower_bound_from_maximum_clique":lower,
        "deterministic_min_fill_upper_bound":upper,
        "min_fill_edges_added":len(fill),
        "exact_treewidth_if_bounds_match":exact,
        "decision":"TAIL4_EXACT_QUOTIENT_PROMOTION_SCOUT_WITH_MATCHING_TREEWIDTH_CERTIFICATE" if exact is not None else "TAIL4_EXACT_QUOTIENT_PROMOTION_SCOUT_WITH_TREEWIDTH_BOUNDS",
    }
    print("result",json.dumps(out,sort_keys=True),flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_TAIL4_SUMMARY")
    print("boundary=these exact quotient factors remain candidate additions until a weighted integration authority is rebuilt")
    print("ALPHA_PASS=0")
    return out

if __name__=="__main__":
    analyze()
