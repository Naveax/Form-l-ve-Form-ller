#!/usr/bin/env python3
"""Aggregate exact tail9 quotient results against the merged 105-ternary physical inventory."""
from __future__ import annotations
import hashlib,json,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as TOPO
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_treewidth8_exact as T4
import summarize_v26_q138_c916_e0_first_dyadic_physical_triple_quotient_tail3 as T3
SUMMARY_DIR=Path(os.environ.get("C916_PHYSICAL_QUOTIENT_TAIL9_SUMMARY_DIR","tail9-quotient-summaries"))
TAIL5_DIR=Path(os.environ.get("C916_TAIL5_QUOTIENT_DIR","authorities/tail5-quotient"))
TAIL6_DIR=Path(os.environ.get("C916_TAIL6_QUOTIENT_DIR","authorities/tail6-quotient"))
TAIL7_DIR=Path(os.environ.get("C916_TAIL7_QUOTIENT_DIR","authorities/tail7-quotient"))
TAIL8_DIR=Path(os.environ.get("C916_TAIL8_QUOTIENT_DIR","authorities/tail8-quotient"))
def load_scopes(directory,prefix,target_key,expected_count,expected_holes):
    files=sorted(directory.glob(f"{prefix}_*.json")); assert len(files)==16,(directory,len(files))
    rows=[json.loads(p.read_text()) for p in files]; by={int(r[target_key]):r for r in rows}; assert set(by)==set(range(16))
    scopes=tuple(sorted(tuple(map(int,by[i]["triple"])) for i in range(16) if int(by[i]["quotient_holes"])>0))
    assert len(scopes)==expected_count
    assert sum(int(by[i]["quotient_holes"]) for i in range(16))==expected_holes
    return scopes
def digest(triples,quads):
    payload=json.dumps({"quads":[list(x) for x in sorted(quads)],"triples":[list(x) for x in sorted(triples)]},sort_keys=True,separators=(",",":"))
    return hashlib.sha256(payload.encode()).hexdigest()
def analyze():
    files=sorted(SUMMARY_DIR.glob("tail9_quotient_*.json")); assert len(files)==16
    rows=[json.loads(p.read_text()) for p in files]; by={int(r["tail9_target"]):r for r in rows}; assert set(by)==set(range(16)); rows=[by[i] for i in range(16)]
    promotable=[r for r in rows if int(r["quotient_holes"])>0]
    sign_only=[r for r in rows if int(r["raw_holes"])>0 and int(r["quotient_holes"])==0]
    pairwise_complete=[r for r in rows if int(r["raw_holes"])==0]
    frozen=tuple(tuple(map(int,x)) for x in TOPO.TERNARY_FACTORS)
    t5=load_scopes(TAIL5_DIR,"tail5_quotient","tail5_target",9,31)
    t6=load_scopes(TAIL6_DIR,"tail6_quotient","tail6_target",11,35)
    t7=load_scopes(TAIL7_DIR,"tail7_quotient","tail7_target",13,37)
    t8=load_scopes(TAIL8_DIR,"tail8_quotient","tail8_target",12,36)
    admitted=tuple(T4.TAIL3)+tuple(T4.TAIL4)+t5+t6+t7+t8
    assert len(frozen)==38 and len(admitted)==67 and not(set(frozen)&set(admitted))
    current=tuple(sorted(set(frozen)|set(admitted))); assert len(current)==105
    t8=tuple(sorted(tuple(map(int,r["triple"])) for r in promotable))
    duplicate=tuple(sorted(set(t8)&set(current))); new=tuple(sorted(set(t8)-set(current)))
    expanded=tuple(sorted(set(current)|set(new)))
    quads=tuple(tuple(map(int,x)) for x in TOPO.QUATERNARY_FACTORS)
    adj=T3.build_graph(expanded+quads); edges=sum(len(v) for v in adj.values())//2
    comps=TOPO.connected_components(adj); _order,erows,fill=TOPO.deterministic_min_fill_certificate(adj)
    upper=max((int(r["later_degree"]) for r in erows),default=0); clique=T3.exact_maximum_clique(adj); lower=max(0,len(clique)-1)
    out={"position":"C","physical_shared_dimension":149,"tail9_targets":16,
         "tail9_promotable_quotient_factors":len(promotable),"tail9_sign_only_raw_obstructions":len(sign_only),
         "tail9_pairwise_complete_targets":len(pairwise_complete),"tail9_total_quotient_holes":sum(int(r["quotient_holes"]) for r in promotable),
         "promotable_rows":[{"tail9_target":int(r["tail9_target"]),"triple":list(map(int,r["triple"])),"raw_holes":int(r["raw_holes"]),"quotient_holes":int(r["quotient_holes"]),"quotient_hole_digest_sha256":str(r["quotient_hole_digest_sha256"])} for r in promotable],
         "promotable_scopes_already_known":[list(x) for x in duplicate],"new_promotable_scopes":[list(x) for x in new],
         "current_ternary_factor_count":len(current),"expanded_candidate_ternary_factor_count":len(expanded),
         "quaternary_factor_count":len(quads),"expanded_scope_digest_sha256":digest(expanded,quads),
         "expanded_primal_variables":len(adj),"expanded_primal_edges":edges,"expanded_component_sizes":[len(x) for x in comps],
         "exact_maximum_clique":list(clique),"treewidth_lower_bound_from_maximum_clique":lower,
         "deterministic_min_fill_upper_bound":upper,"min_fill_edges_added":len(fill),
         "exact_treewidth_if_bounds_match":upper if upper==lower else None,
         "decision":("TAIL9_EXACT_QUOTIENT_PROMOTION_SCOUT_WITH_MATCHING_TREEWIDTH_CERTIFICATE" if upper==lower else "TAIL9_EXACT_QUOTIENT_PROMOTION_SCOUT_WITH_TREEWIDTH_BOUNDS")}
    print("result",json.dumps(out,sort_keys=True),flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_PHYSICAL_TRIPLE_QUOTIENT_TAIL9_SUMMARY")
    print("boundary=tail9 relations remain candidate additions until exact quotient jobs and aggregate pass; no weighted count is inferred")
    print("ALPHA_PASS=0")
    return out
if __name__=="__main__": analyze()
