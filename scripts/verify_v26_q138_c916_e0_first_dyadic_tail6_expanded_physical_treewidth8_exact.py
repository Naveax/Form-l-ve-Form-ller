#!/usr/bin/env python3
"""Exact treewidth-8 certificate for the physical inventory through tail6."""
from __future__ import annotations
import functools,itertools,json,os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as T
import verify_v26_q138_c916_e0_first_dyadic_tail4_expanded_physical_treewidth8_exact as T4
import verify_v26_q138_c916_e0_first_dyadic_tail5_expanded_physical_treewidth8_exact as T5

TAIL6_DIR=Path(os.environ.get("C916_TAIL6_QUOTIENT_DIR","authorities/tail6-quotient"))
EXPECTED_TAIL6_SCOPES=(
 (3,6,7),(3,7,18),(3,7,22),(3,7,30),(3,7,33),(3,7,69),
 (3,7,88),(3,7,89),(181,182,244),(181,182,245),(181,182,249),
)
EXPECTED_COMPONENT_SIZES=(40,3,3,3,3)

def load_tail6_scopes():
    files=sorted(TAIL6_DIR.glob("tail6_quotient_*.json"))
    assert len(files)==16,(TAIL6_DIR,[p.name for p in files])
    rows=[json.loads(p.read_text()) for p in files]
    by={int(r["tail6_target"]):r for r in rows}
    assert set(by)==set(range(16))
    scopes=[]; holes=0
    for i in range(16):
        r=by[i]; q=int(r["quotient_holes"])
        assert bool(r["promotable_to_current_quotient_factor_inventory"])==(q>0)
        if q:
            forbidden=tuple(tuple(map(int,x)) for x in r["quotient_hole_tuples"])
            assert len(forbidden)==q
            scopes.append(tuple(map(int,r["triple"]))); holes+=q
    assert tuple(sorted(scopes))==EXPECTED_TAIL6_SCOPES
    assert holes==35
    return tuple(sorted(scopes))

def build_graph(scopes):
    adj={}
    for scope in scopes:
        for v in scope: adj.setdefault(int(v),set())
        for u,v in itertools.combinations(scope,2):
            adj[int(u)].add(int(v)); adj[int(v)].add(int(u))
    return adj

def components(adj):
    unseen=set(adj); out=[]
    while unseen:
        root=min(unseen); stack=[root]; comp=set()
        while stack:
            v=stack.pop()
            if v in comp: continue
            comp.add(v); unseen.discard(v); stack.extend(adj[v]-comp)
        out.append(tuple(sorted(comp)))
    return tuple(sorted(out,key=lambda x:(-len(x),x)))

def min_fill(adj0):
    adj={v:set(ns) for v,ns in adj0.items()}; rows=[]; fills=[]
    while adj:
        cand=[]
        for v,ns0 in adj.items():
            ns=tuple(sorted(ns0))
            missing=tuple((a,b) for a,b in itertools.combinations(ns,2) if b not in adj[a])
            cand.append((len(missing),len(ns),v,ns,missing))
        _fc,deg,v,ns,missing=min(cand)
        rows.append((v,ns,deg))
        for a,b in missing:
            if b not in adj[a]:
                adj[a].add(b); adj[b].add(a); fills.append((a,b))
        for a in ns: adj[a].remove(v)
        del adj[v]
    return tuple(rows),tuple(fills)

def exact_width_at_most(adj0,vertices,k):
    vertices=tuple(vertices); idx={v:i for i,v in enumerate(vertices)}; n=len(vertices)
    masks=[]
    for v in vertices:
        m=0
        for u in adj0[v]:
            if u in idx: m|=1<<idx[u]
        masks.append(m)
    visited=0; simp=0
    def is_clique(nb,adj):
        s=nb
        while s:
            bit=s&-s; i=bit.bit_length()-1; s^=bit
            wanted=nb&~(1<<i)
            if (int(adj[i])&wanted)!=wanted:return False
        return True
    def eliminate(active,adj,i,nb):
        ns=[]; s=nb
        while s:
            bit=s&-s; j=bit.bit_length()-1; s^=bit; ns.append(j)
        nxt=list(map(int,adj)); new=active&~(1<<i)
        for a in ns:
            nxt[a]|=nb&~(1<<a); nxt[a]&=~(1<<i)
        nxt[i]=0
        return new,tuple(x&new for x in nxt)
    @functools.lru_cache(None)
    def search(active,adj):
        nonlocal visited,simp
        visited+=1
        if active==0:return ()
        for i in range(n):
            if not((active>>i)&1):continue
            nb=int(adj[i])&active&~(1<<i)
            if nb.bit_count()<=k and is_clique(nb,adj):
                simp+=1; new,nxt=eliminate(active,adj,i,nb)
                suffix=search(new,nxt)
                return None if suffix is None else (i,)+suffix
        cand=[]
        for i in range(n):
            if not((active>>i)&1):continue
            nb=int(adj[i])&active&~(1<<i); deg=nb.bit_count()
            if deg>k:continue
            ns=[j for j in range(n) if (nb>>j)&1]
            fill=sum(1 for a,b in itertools.combinations(ns,2) if not((int(adj[a])>>b)&1))
            cand.append((fill,deg,i,nb))
        if not cand:return None
        for _f,_d,i,nb in sorted(cand):
            new,nxt=eliminate(active,adj,i,nb)
            suffix=search(new,nxt)
            if suffix is not None:return (i,)+suffix
        return None
    ordering=search((1<<n)-1,tuple(masks))
    return ordering,visited,simp,search.cache_info()

def analyze():
    t6=load_tail6_scopes()
    ternary=tuple(T.TERNARY_FACTORS)+tuple(T4.TAIL3)+tuple(T4.TAIL4)+tuple(T5.EXPECTED_TAIL5_SCOPES)+t6
    assert len(ternary)==80 and len(set(ternary))==80
    quads=tuple(T.QUATERNARY_FACTORS)
    adj=build_graph(ternary+quads)
    comps=components(adj); sizes=tuple(len(c) for c in comps)
    assert sizes==EXPECTED_COMPONENT_SIZES and len(adj)==52
    rows,fills=min_fill(adj); upper=max(d for _v,_n,d in rows)
    assert upper==8 and len(fills)==2
    order7,states,simp,info=exact_width_at_most(adj,comps[0],7)
    assert order7 is None
    out={"position":"C","physical_shared_dimension":149,"frozen_ternary_factors":38,
         "tail3_promoted_ternary_factors":10,"tail4_promoted_ternary_factors":12,
         "tail5_promoted_ternary_factors":9,"tail6_promoted_ternary_factors":11,
         "physical_quaternary_factors":5,"combined_physical_scopes":85,
         "primal_variables":len(adj),"component_sizes":list(sizes),
         "width7_exhaustive_order_exists":False,"width7_states_visited":states,
         "width7_simplicial_reductions":simp,"width7_cache_hits":int(info.hits),
         "width7_cache_misses":int(info.misses),"deterministic_min_fill_upper_bound":upper,
         "deterministic_fill_edges":[list(x) for x in fills],"exact_treewidth":8,
         "decision":"C916_TAIL6_EXPANDED_PHYSICAL_PRIMAL_EXACT_TREEWIDTH_8"}
    print("result",json.dumps(out,sort_keys=True),flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_TAIL6_EXPANDED_PHYSICAL_TREEWIDTH8_EXACT")
    print("theorem=no width-7 elimination ordering exists by exact memoized search with safe simplicial reduction, while deterministic elimination attains width 8")
    print("boundary=physical higher-order topology only; pairwise, affine, multiplicity and end-to-end work remain outside")
    print("ALPHA_PASS=0")
    return out
if __name__=="__main__": analyze()
