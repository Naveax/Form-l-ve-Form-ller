#!/usr/bin/env python3
import hashlib, io, itertools, json, os, sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O

D,P=O.D,O.P
PHYS_N=O.PHYS_N
MASK=(1<<PHYS_N)-1
M4_PATH=Path(os.environ.get("C916_M4_AUTHORITY","authorities/m4/c916_e0_first_dyadic_four_separator_complete_authority.json"))

def insert_rref(state,x):
    x=int(x)
    if not x: return state
    piv=[]
    for r in state:
        phys=r&MASK
        if phys: piv.append((phys.bit_length()-1,r))
    piv.sort(reverse=True)
    for p,r in piv:
        if (x>>p)&1: x^=r
    phys=x&MASK
    if not phys: return None if ((x>>PHYS_N)&1) else state
    p=phys.bit_length()-1
    out=[r^x if ((r>>p)&1) else r for r in state]; out.append(x)
    return tuple(sorted((r for r in out if r&MASK),reverse=True))

def merge(a,b):
    s=a
    for x in b:
        s=insert_rref(s,x)
        if s is None: break
    return s

def build_anchors(gids):
    e0,_e1,_half=P.C.P.U.H.classify_patterns(); grouped=defaultdict(list)
    for zc in range(4):
        for zs,cls in e0[zc]:
            can=P.C.P.U.H.support_for(O.POS,zs,cls)
            if can is not None: grouped[can].append((zs,cls))
    ordered=list(sorted(grouped.items(),key=lambda kv:kv[0])); assert len(ordered)==250
    anchors={}; codim=Counter()
    for g in gids:
        can,sectors=ordered[g]; assert len(sectors)==4
        _pr,_loc,a=D.projection_anchor(can); rows=tuple(int(m)|(int(rhs)<<PHYS_N) for m,rhs in a["physical_support_constraints"]); s=()
        for x in rows: s=insert_rref(s,x); assert s is not None
        anchors[g]=s; codim[len(rows)]+=1
    assert codim==Counter({7:46,8:32,6:12}); return anchors

def analyze():
    m4=json.loads(M4_PATH.read_text()); gids=tuple(map(int,m4["m4_group_ids"])); assert len(gids)==90
    known_triples={tuple(sorted(map(int,t))) for t in m4["projection_minimal_empty_triples"]}; assert len(known_triples)==5
    with redirect_stdout(io.StringIO()): census,groups=O.build_authority()
    anchors=build_anchors(gids); pair_ok=set(); disjoint=0
    for i,u in enumerate(gids):
        for v in gids[i+1:]:
            rel,_=P.support_relation(groups[u]["projection_anchor"],groups[v]["projection_anchor"],PHYS_N)
            if rel=="disjoint": disjoint+=1
            else: pair_ok.add((u,v))
    assert disjoint==359 and len(pair_ok)==3646
    tested=0; clique4=0; minimal=[]; cache={}
    def pair(u,v): return (min(u,v),max(u,v)) in pair_ok
    def inter2(u,v):
        k=(min(u,v),max(u,v))
        if k not in cache: cache[k]=merge(anchors[k[0]],anchors[k[1]])
        return cache[k]
    for idx,(a,b,c,d) in enumerate(itertools.combinations(gids,4),1):
        tested+=1
        if not (pair(a,b) and pair(a,c) and pair(a,d) and pair(b,c) and pair(b,d) and pair(c,d)): continue
        clique4+=1
        if (a,b,c) in known_triples or (a,b,d) in known_triples or (a,c,d) in known_triples or (b,c,d) in known_triples: continue
        s=inter2(a,b); s=merge(s,anchors[c]) if s is not None else None
        if s is None: raise AssertionError(("unlisted empty triple",a,b,c))
        s=merge(s,anchors[d])
        if s is None: minimal.append((a,b,c,d))
        if idx%250000==0: print("progress",idx,"minimal4",len(minimal),flush=True)
    digest=hashlib.sha256(("\n".join("|".join(map(str,q)) for q in minimal)+("\n" if minimal else "")).encode()).hexdigest()
    out={"position":O.POS,"physical_shared_dimension":PHYS_N,"m4_outputs":90,"all_quadruples_tested":tested,"pairwise_intersecting_quadruples":clique4,"known_minimal_empty_triples":len(known_triples),"minimal_empty_quadruples":len(minimal),"minimal_empty_quadruple_digest_sha256":digest,"minimal_empty_quadruple_list":[list(q) for q in minimal],"pair_disjoint_count":disjoint,"decision":"M4_PROJECTION_MINIMAL_EMPTY_QUADRUPLES_EXACT"}
    print("result",json.dumps(out,sort_keys=True),flush=True); print("PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_PROJECTION_MINIMAL_EMPTY_QUADRUPLES"); print("ALPHA_PASS=0"); return out

if __name__=="__main__": analyze()
