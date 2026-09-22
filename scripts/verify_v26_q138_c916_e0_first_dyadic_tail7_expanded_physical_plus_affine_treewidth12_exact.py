#!/usr/bin/env python3
"""Exact treewidth-12 certificate for the physical inventory through tail7 plus all 19 affine obstructions."""
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_treewidth_exact as W
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_treewidth8_exact as T4
import verify_v26_q138_c916_e0_first_dyadic_tail5_expanded_physical_treewidth8_exact as T5
import verify_v26_q138_c916_e0_first_dyadic_tail6_expanded_physical_treewidth8_exact as T6
import verify_v26_q138_c916_e0_first_dyadic_tail7_expanded_physical_treewidth8_exact as T7

EXPECTED_COMPONENT_SIZES=(58,3,3)
EXPECTED_FILL_EDGES=(
    (12,113),(6,181),(67,186),(3,184),(7,184),(4,7),(165,182),
    (5,24),(3,114),(7,114),(8,24),(24,113),(8,11),(11,113),
    (4,112),(112,165),
)
EXPECTED_WIDTH11_STATES=6986

def analyze():
    scopes=(
        tuple(W.all_scopes())
        + tuple(T4.TAIL3)
        + tuple(T4.TAIL4)
        + tuple(T5.EXPECTED_TAIL5_SCOPES)
        + tuple(T6.EXPECTED_TAIL6_SCOPES)
        + tuple(T7.EXPECTED_TAIL7_SCOPES)
    )
    assert len(scopes)==117 and len(set(scopes))==117
    adj=W.build_primal_graph(scopes)
    assert len(adj)==64
    components=W.connected_components(adj)
    sizes=tuple(len(c) for c in components)
    assert sizes==EXPECTED_COMPONENT_SIZES

    rows,fills=W.deterministic_min_fill_certificate(adj)
    upper=max(int(r["later_degree"]) for r in rows)
    assert upper==12
    assert tuple(map(tuple,fills))==EXPECTED_FILL_EDGES

    order11,states11,simp11,cache11=T6.exact_width_at_most(adj,components[0],11)
    assert order11 is None
    assert states11==EXPECTED_WIDTH11_STATES

    order12,states12,simp12,cache12=T6.exact_width_at_most(adj,components[0],12)
    assert order12 is not None

    out={
        "position":"C",
        "physical_shared_dimension":149,
        "physical_ternary_factors":93,
        "physical_quaternary_factors":5,
        "complete_affine_support_scopes":19,
        "combined_higher_order_scopes":len(scopes),
        "primal_variables":len(adj),
        "component_sizes":list(sizes),
        "width11_exhaustive_order_exists":False,
        "width11_states_visited":states11,
        "width11_simplicial_reductions":simp11,
        "width11_cache_hits":int(cache11.hits),
        "width11_cache_misses":int(cache11.misses),
        "width12_order_exists":True,
        "width12_states_visited":states12,
        "width12_simplicial_reductions":simp12,
        "width12_cache_hits":int(cache12.hits),
        "width12_cache_misses":int(cache12.misses),
        "deterministic_min_fill_upper_bound":upper,
        "deterministic_fill_edges":[list(x) for x in fills],
        "exact_treewidth":12,
        "decision":"C916_TAIL7_EXPANDED_PHYSICAL_PLUS_COMPLETE_AFFINE_PRIMAL_EXACT_TREEWIDTH_12",
    }
    print("result",json.dumps(out,sort_keys=True),flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL7_EXPANDED_PHYSICAL_PLUS_AFFINE_TREEWIDTH12_EXACT")
    print("theorem=no width-11 elimination ordering exists by exact memoized search with safe simplicial reduction, while deterministic elimination attains width 12")
    print("boundary=higher-order physical plus affine topology only; dense pairwise relations, multiplicity and end-to-end work remain outside")
    print("ALPHA_PASS=0")
    return out

if __name__=="__main__":
    analyze()
