#!/usr/bin/env python3
"""Exact physical-only junction compiler for the 93-ternary inventory through tail7."""
from __future__ import annotations
import json,math,os,sys
from collections import defaultdict,deque
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_compiler_exact as P
import verify_v26_q138_c916_e0_first_dyadic_current_physical_junction_forest_exact as J
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T
import verify_v26_q138_c916_e0_first_dyadic_tail3_expanded_physical_junction_compiler_exact as E3
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_junction_compiler_exact as E4
import verify_v26_q138_c916_e0_first_dyadic_tail5_expanded_physical_junction_compiler_exact as E5
import verify_v26_q138_c916_e0_first_dyadic_tail6_expanded_physical_junction_compiler_exact as E6
import verify_v26_q138_c916_e0_first_dyadic_tail7_expanded_physical_treewidth8_exact as E7

TAIL7_DIR=Path(os.environ.get("C916_TAIL7_QUOTIENT_DIR","authorities/tail7-quotient"))
TAIL6_COUNT=4105358999847018371670430244544
EXPECTED_COMPONENTS=3

def exact_junction_count(cliques,tables,forest):
    cadj=[[] for _ in range(len(cliques))]
    for i,j,sep in forest:
        sep=tuple(map(int,sep)); cadj[i].append((j,sep)); cadj[j].append((i,sep))
    seen=set(); component_counts=[]; message_rows=[]
    for root in range(len(cliques)):
        if root in seen: continue
        parent={root:None}; parent_sep={}; order=[]; q=deque([root]); seen.add(root)
        while q:
            i=q.popleft(); order.append(i)
            for j,sep in cadj[i]:
                if j in parent: continue
                parent[j]=i; parent_sep[j]=sep; seen.add(j); q.append(j)
        messages={}
        for i in reversed(order):
            bag=tuple(cliques[i]); pos={v:p for p,v in enumerate(bag)}
            p=parent[i]; sep_to_parent=tuple(parent_sep[i]) if p is not None else ()
            accum=defaultdict(int)
            for assignment in tables[i]:
                weight=1
                for child,sep in cadj[i]:
                    if parent.get(child)!=i: continue
                    key=tuple(assignment[pos[v]] for v in sep)
                    weight*=int(messages[child].get(key,0))
                    if weight==0: break
                if weight==0: continue
                key=() if p is None else tuple(assignment[pos[v]] for v in sep_to_parent)
                accum[key]+=weight
            if p is None:
                assert set(accum)<={()}; component_counts.append(int(accum.get((),0)))
            else:
                messages[i]=dict(accum)
                message_rows.append({"child":i,"parent":p,"separator":list(sep_to_parent),
                                     "positive_message_rows":len(accum),
                                     "message_weight_sum":sum(accum.values())})
    assert len(component_counts)==EXPECTED_COMPONENTS,component_counts
    return math.prod(component_counts),tuple(component_counts),tuple(message_rows)

def load_tail7_factors():
    files=sorted(TAIL7_DIR.glob("tail7_quotient_*.json")); assert len(files)==16
    rows=[json.loads(p.read_text()) for p in files]
    by={int(r["tail7_target"]):r for r in rows}; assert set(by)==set(range(16))
    out=[]; holes=0
    for i in range(16):
        r=by[i]; q=int(r["quotient_holes"])
        assert bool(r["promotable_to_current_quotient_factor_inventory"])==(q>0)
        if not q: continue
        forbidden=frozenset(tuple(map(int,x)) for x in r["quotient_hole_tuples"])
        assert len(forbidden)==q; holes+=q
        out.append({"name":f"tail7:{i}","scope":tuple(map(int,r["triple"])),
                    "qsizes":tuple(map(int,r["quotient_alphabet_sizes"])),
                    "forbidden":forbidden,"digest":str(r["quotient_hole_digest_sha256"])})
    assert tuple(sorted(f["scope"] for f in out))==E7.EXPECTED_TAIL7_SCOPES
    assert holes==37
    return tuple(out)

def analyze():
    frozen=P.load_ternary_factors(); t3=E3.load_tail3_factors(); t4=E4.load_tail4_factors()
    t5=E5.load_tail5_factors(); t6=E6.load_tail6_factors(); t7=load_tail7_factors()
    assert (len(frozen),len(t3),len(t4),len(t5),len(t6),len(t7))==(38,10,12,9,11,13)
    prior=frozen+t3+t4+t5+t6; factors=prior+t7
    scopes=[f["scope"] for f in factors]; assert len(scopes)==93 and len(set(scopes))==93
    quads=tuple(tuple(map(int,q)) for q in T.QUATERNARY_FACTORS)
    adj=E5.build_graph(tuple(scopes)+quads)
    rows,fill_edges=E5.deterministic_min_fill(adj)
    upper=max(int(r["later_degree"]) for r in rows); assert upper==8
    assert tuple(map(tuple,fill_edges))==E7.EXPECTED_FILL_EDGES
    simple=tuple((int(r["vertex"]),tuple(map(int,r["later_neighbors"]))) for r in rows)
    cliques=J.maximal_cliques(simple); forest=J.maximum_intersection_forest(cliques); J.verify_running_intersection(cliques,forest)
    qsizes=J.quotient_sizes_from_m4()
    prior_vars={v for scope in tuple(f["scope"] for f in prior)+quads for v in scope}
    expanded_vars={v for scope in tuple(scopes)+quads for v in scope}
    newvars=tuple(sorted(expanded_vars-prior_vars))
    lift=math.prod(qsizes[v] for v in newvars); lifted=TAIL6_COUNT*lift
    tables,meta=E5.compile_tables(cliques,factors,qsizes)
    total,components,messages=exact_junction_count(cliques,tables,forest)
    assert 0<total<=lifted
    capacities=[math.prod(qsizes[v] for v in bag) for bag in cliques]
    out={"position":"C","physical_shared_dimension":149,"frozen_ternary_factors":38,
         "tail3_promoted_ternary_factors":10,"tail4_promoted_ternary_factors":12,
         "tail5_promoted_ternary_factors":9,"tail6_promoted_ternary_factors":11,
         "tail7_promoted_ternary_factors":13,"expanded_ternary_factors":93,
         "physical_quaternary_factors":5,"exact_treewidth":8,"fill_edges":[list(x) for x in fill_edges],
         "maximal_cliques":len(cliques),"junction_forest_edges":len(forest),
         "largest_clique_capacity":max(capacities),"total_clique_capacity":sum(capacities),
         "largest_compiled_allowed_table":max(map(len,tables)),
         "total_compiled_allowed_rows":sum(map(len,tables)),
         "component_physical_assignment_counts":list(components),
         "exact_tail7_expanded_physical_layer_assignment_count":int(total),
         "exact_tail7_expanded_physical_layer_assignment_log2":math.log2(total),
         "tail6_expanded_physical_layer_assignment_count":TAIL6_COUNT,
         "newly_introduced_variables_vs_tail6":list(newvars),
         "tail6_lift_factor_into_tail7_variable_universe":lift,
         "tail6_lifted_assignment_count_in_tail7_variable_universe":lifted,
         "removed_assignments_vs_lifted_tail6_inventory":lifted-total,
         "gain_vs_lifted_tail6_inventory_log2_bits":math.log2(lifted)-math.log2(total),
         "max_positive_separator_message_rows":max((r["positive_message_rows"] for r in messages),default=1),
         "clique_tables":list(meta),
         "decision":"C916_TAIL7_EXPANDED_PHYSICAL_FACTORS_EXACT_JUNCTION_COUNT"}
    print("result",json.dumps(out,sort_keys=True),flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL7_EXPANDED_PHYSICAL_JUNCTION_COMPILER_EXACT")
    print("boundary=prior physical count is compared only after lifting newly introduced quotient variables")
    print("boundary=physical higher-order layer only; pairwise, affine, multiplicity and end-to-end work remain outside")
    print("ALPHA_PASS=0")
    return out
if __name__=="__main__": analyze()
