#!/usr/bin/env python3
"""Exact treewidth-8 certificate for the physical inventory through tail7."""
from __future__ import annotations
import json,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_treewidth8_exact as T4
import verify_v26_q138_c916_e0_first_dyadic_tail5_expanded_physical_treewidth8_exact as T5
import verify_v26_q138_c916_e0_first_dyadic_tail6_expanded_physical_treewidth8_exact as T6

TAIL7_DIR=Path(os.environ.get("C916_TAIL7_QUOTIENT_DIR","authorities/tail7-quotient"))
EXPECTED_TAIL7_SCOPES=((3,7,132),(3,7,137),(3,7,141),(3,7,143),(3,7,155),(3,7,156),(3,7,159),(3,7,160),(3,7,161),(3,7,177),(3,7,178),(3,7,179),(3,7,228))
EXPECTED_COMPONENT_SIZES=(56,3,3)
EXPECTED_FILL_EDGES=((4,7),(165,182))
EXPECTED_WIDTH7_STATES=234

def load_tail7_scopes():
    files=sorted(TAIL7_DIR.glob("tail7_quotient_*.json"))
    assert len(files)==16,(TAIL7_DIR,[p.name for p in files])
    rows=[json.loads(p.read_text()) for p in files]
    by={int(r["tail7_target"]):r for r in rows}; assert set(by)==set(range(16))
    scopes=[]; holes=0
    for i in range(16):
        r=by[i]; q=int(r["quotient_holes"])
        assert bool(r["promotable_to_current_quotient_factor_inventory"])==(q>0)
        if not q: continue
        forbidden=tuple(tuple(map(int,x)) for x in r["quotient_hole_tuples"])
        assert len(forbidden)==q
        scopes.append(tuple(map(int,r["triple"]))); holes+=q
    assert tuple(sorted(scopes))==EXPECTED_TAIL7_SCOPES
    assert holes==37
    return tuple(sorted(scopes))

def analyze():
    t7=load_tail7_scopes()
    ternary=tuple(T.TERNARY_FACTORS)+tuple(T4.TAIL3)+tuple(T4.TAIL4)+tuple(T5.EXPECTED_TAIL5_SCOPES)+tuple(T6.EXPECTED_TAIL6_SCOPES)+t7
    assert len(ternary)==93 and len(set(ternary))==93
    quads=tuple(T.QUATERNARY_FACTORS)
    adj=T6.build_graph(ternary+quads)
    comps=T6.components(adj); sizes=tuple(len(c) for c in comps)
    assert sizes==EXPECTED_COMPONENT_SIZES and len(adj)==62
    rows,fills=T6.min_fill(adj); upper=max(d for _v,_n,d in rows)
    assert upper==8 and fills==EXPECTED_FILL_EDGES
    order7,states,simp,info=T6.exact_width_at_most(adj,comps[0],7)
    assert order7 is None and states==EXPECTED_WIDTH7_STATES
    out={"position":"C","physical_shared_dimension":149,"frozen_ternary_factors":38,
         "tail3_promoted_ternary_factors":10,"tail4_promoted_ternary_factors":12,
         "tail5_promoted_ternary_factors":9,"tail6_promoted_ternary_factors":11,
         "tail7_promoted_ternary_factors":13,"physical_quaternary_factors":5,
         "combined_physical_scopes":98,"primal_variables":len(adj),"component_sizes":list(sizes),
         "width7_exhaustive_order_exists":False,"width7_states_visited":states,
         "width7_simplicial_reductions":simp,"width7_cache_hits":int(info.hits),
         "width7_cache_misses":int(info.misses),"deterministic_min_fill_upper_bound":upper,
         "deterministic_fill_edges":[list(x) for x in fills],"exact_treewidth":8,
         "decision":"C916_TAIL7_EXPANDED_PHYSICAL_PRIMAL_EXACT_TREEWIDTH_8"}
    print("result",json.dumps(out,sort_keys=True),flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL7_EXPANDED_PHYSICAL_TREEWIDTH8_EXACT")
    print("theorem=no width-7 elimination ordering exists by exact memoized search with safe simplicial reduction, while deterministic elimination attains width 8")
    print("boundary=physical higher-order topology only; pairwise, affine, multiplicity and end-to-end work remain outside")
    print("ALPHA_PASS=0")
    return out
if __name__=="__main__": analyze()
