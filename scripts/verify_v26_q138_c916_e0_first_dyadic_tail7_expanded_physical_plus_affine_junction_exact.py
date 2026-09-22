#!/usr/bin/env python3
"""Exact modular junction count for tail7-expanded physical factors plus all 19 affine obstructions."""
from __future__ import annotations
import json,math,sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))

import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_compiler_exact as P
import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_forest_exact as J
import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_junction_compiler_exact as C
import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_treewidth_exact as W
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_all_known_physical_exact as H
import verify_v26_q138_c916_e0_first_dyadic_tail3_expanded_physical_junction_compiler_exact as E3
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_junction_compiler_exact as E4
import verify_v26_q138_c916_e0_first_dyadic_tail5_expanded_physical_junction_compiler_exact as E5
import verify_v26_q138_c916_e0_first_dyadic_tail6_expanded_physical_junction_compiler_exact as E6
import verify_v26_q138_c916_e0_first_dyadic_tail7_expanded_physical_junction_compiler_exact as E7
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_plus_affine_junction_exact as A4
import verify_v26_q138_c916_e0_first_dyadic_tail7_expanded_physical_plus_affine_treewidth12_exact as TOP

TAIL4_COMBINED_COUNT=487658086737909263297551584

def build_model():
    frozen=P.load_ternary_factors()
    t3=E3.load_tail3_factors()
    t4=E4.load_tail4_factors()
    t5=E5.load_tail5_factors()
    t6=E6.load_tail6_factors()
    t7=E7.load_tail7_factors()
    assert (len(frozen),len(t3),len(t4),len(t5),len(t6),len(t7))==(38,10,12,9,11,13)
    ternary=frozen+t3+t4+t5+t6+t7
    assert len(ternary)==93
    scopes=[tuple(f["scope"]) for f in ternary]
    assert len(set(scopes))==93

    affine=C.affine_scopes()
    assert len(affine)==19

    all_scopes=(
        tuple(W.all_scopes())
        + tuple(f["scope"] for f in t3)
        + tuple(f["scope"] for f in t4)
        + tuple(f["scope"] for f in t5)
        + tuple(f["scope"] for f in t6)
        + tuple(f["scope"] for f in t7)
    )
    assert len(all_scopes)==117 and len(set(all_scopes))==117
    adj=W.build_primal_graph(all_scopes)
    rows,fills=W.deterministic_min_fill_certificate(adj)
    width=max(int(r["later_degree"]) for r in rows)
    assert width==12
    assert tuple(map(tuple,fills))==TOP.EXPECTED_FILL_EDGES

    simple=tuple((int(r["vertex"]),tuple(map(int,r["later_neighbors"]))) for r in rows)
    cliques=J.maximal_cliques(simple)
    forest=J.maximum_intersection_forest(cliques)
    J.verify_running_intersection(cliques,forest)
    qsizes=J.quotient_sizes_from_m4()

    attached=defaultdict(list)
    attachments=[]
    for factor in ternary:
        ci=A4.assign_scope(factor["scope"],cliques)
        attached[ci].append(("finite_forbidden",tuple(factor["scope"]),factor["forbidden"],str(factor["name"])))
        attachments.append((str(factor["name"]),ci))

    quad_scope=tuple(map(int,H.FIVE_GIDS))
    quad_allowed=frozenset(tuple(map(int,row)) for row in H.ALLOWED)
    assert len(quad_allowed)==832
    qci=A4.assign_scope(quad_scope,cliques)
    attached[qci].append(("allowed",quad_scope,quad_allowed,"physical_quads:compiled5"))
    attachments.append(("physical_quads:compiled5",qci))

    for ai,scope in enumerate(affine):
        scope=tuple(map(int,scope))
        ci=A4.assign_scope(scope,cliques)
        attached[ci].append(("affine_all_nonzero_forbidden",scope,None,f"affine:{ai}"))
        attachments.append((f"affine:{ai}",ci))

    assert len(attachments)==93+1+19
    return tuple(cliques),tuple(forest),qsizes,dict(attached),tuple(sorted(attachments)),tuple(fills),tuple(all_scopes)

def analyze():
    # Mandatory representation regression. The same dense-mask + modular junction engine
    # must reproduce the merged tail4 physical+affine authority before the larger model
    # is admitted.
    r_cliques,r_forest,r_qsizes,r_attached,_ra,_rf,_rn=A4.build_model()
    r_masks,_rmeta=A4.build_allowed_masks(r_cliques,r_qsizes,r_attached)
    regression_total,*_=A4.modular_exact_count("tail4_regression",r_cliques,r_masks,r_forest,r_qsizes)
    assert regression_total==TAIL4_COMBINED_COUNT,regression_total
    print(f"modular_regression_tail4_exact_count={regression_total}",flush=True)
    del r_masks

    cliques,forest,qsizes,attached,attachments,fills,all_scopes=build_model()
    masks,metadata=A4.build_allowed_masks(cliques,qsizes,attached)
    total,universe_bound,primes,modulus_product,residue_rows=A4.modular_exact_count(
        "tail7_expanded",cliques,masks,forest,qsizes
    )

    tail4_scopes=tuple(W.all_scopes())+tuple(E4.TAIL3 if hasattr(E4,"TAIL3") else ())+tuple()
    # Use the factor loaders instead of module constants for the aligned comparison.
    frozen=P.load_ternary_factors()
    t3=E3.load_tail3_factors()
    t4=E4.load_tail4_factors()
    prior_scopes=tuple(W.all_scopes())+tuple(f["scope"] for f in t3)+tuple(f["scope"] for f in t4)
    prior_vars={v for scope in prior_scopes for v in scope}
    current_vars={v for scope in all_scopes for v in scope}
    newvars=tuple(sorted(current_vars-prior_vars))
    lift=math.prod(qsizes[v] for v in newvars)
    lifted=TAIL4_COMBINED_COUNT*lift
    assert 0<total<=lifted

    capacities=[int(mask.size) for mask in masks]
    out={
        "position":"C",
        "physical_shared_dimension":149,
        "affine_constraint_semantics":"all-nonzero forbidden; maximal local quotient-state index is zero",
        "frozen_ternary_factors":38,
        "tail3_promoted_ternary_factors":10,
        "tail4_promoted_ternary_factors":12,
        "tail5_promoted_ternary_factors":9,
        "tail6_promoted_ternary_factors":11,
        "tail7_promoted_ternary_factors":13,
        "expanded_ternary_factors":93,
        "physical_quaternary_factors":5,
        "affine_constraints":19,
        "exact_treewidth":12,
        "fill_edges":[list(map(int,x)) for x in fills],
        "maximal_cliques":len(cliques),
        "junction_forest_edges":len(forest),
        "largest_clique_capacity":max(capacities),
        "total_clique_capacity":sum(capacities),
        "largest_compiled_allowed_table":max(int(r["allowed_rows"]) for r in metadata),
        "total_compiled_allowed_rows":sum(int(r["allowed_rows"]) for r in metadata),
        "constraint_attachments":[list(x) for x in attachments],
        "quotient_variables_in_model":len(current_vars),
        "modular_regression_tail4_exact_count":regression_total,
        "full_assignment_universe_bound":universe_bound,
        "crt_primes":list(primes),
        "crt_modulus_product":modulus_product,
        "modular_residues":residue_rows,
        "exact_tail7_expanded_physical_plus_affine_assignment_count":int(total),
        "exact_tail7_expanded_physical_plus_affine_assignment_log2":math.log2(total),
        "tail4_physical_plus_affine_assignment_count":TAIL4_COMBINED_COUNT,
        "newly_introduced_variables_vs_tail4_combined":list(newvars),
        "tail4_lift_factor_into_tail7_combined_universe":lift,
        "tail4_lifted_assignment_count_in_tail7_combined_universe":lifted,
        "removed_assignments_vs_lifted_tail4_inventory":lifted-total,
        "gain_vs_lifted_tail4_inventory_log2_bits":math.log2(lifted)-math.log2(total),
        "clique_tables":list(metadata),
        "decision":"C916_TAIL7_EXPANDED_PHYSICAL_PLUS_COMPLETE_AFFINE_EXACT_MODULAR_JUNCTION_COUNT",
    }
    print("result",json.dumps(out,sort_keys=True),flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL7_EXPANDED_PHYSICAL_PLUS_AFFINE_JUNCTION_EXACT")
    print("theorem=the dense-mask modular junction engine reproduces the merged tail4 combined authority exactly, then CRT counts all 93 ternary physical factors, the compiled five-quaternary physical relation, and all 19 authority-correct affine obstructions")
    print("boundary=this excludes the dense 4005 pairwise quotient relation layer and multiplicity weights, so it is not a weighted work exponent")
    print("ALPHA_PASS=0")
    return out

if __name__=="__main__":
    analyze()
