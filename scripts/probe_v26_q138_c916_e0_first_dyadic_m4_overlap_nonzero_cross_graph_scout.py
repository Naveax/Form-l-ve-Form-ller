#!/usr/bin/env python3
import io, json, os, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O

P = O.P
PHYS_N = O.PHYS_N
M4_PATH = Path(os.environ.get("C916_M4_AUTHORITY","authorities/m4/c916_e0_first_dyadic_four_separator_complete_authority.json"))
EXPECTED_ZC_DIGEST = "7ce0219e86206aeac622bd423b1341cb47f8681564f19319c96823fcb4d4fab1"
EXPECTED_REL_HIST = {"disjoint":359,"equal":55,"left_subset_right":312,"overlap_incomparable":2766,"right_subset_left":513}
HUBS=(19,20,23,61,83,129,134,139,140,157,232)
ISOLATES=(158,180,236,238)

def components(nodes,adj):
    unseen=set(nodes); out=[]
    while unseen:
        root=min(unseen); stack=[root]; comp=set()
        while stack:
            v=stack.pop()
            if v in comp: continue
            comp.add(v); stack.extend(adj[v]&unseen)
        unseen-=comp; out.append(tuple(sorted(comp)))
    return tuple(sorted(out,key=lambda c:(-len(c),c)))

def degeneracy(nodes,adj):
    work={v:set(adj[v]) for v in nodes}; d=0; order=[]
    while work:
        v=min(work,key=lambda x:(len(work[x]),x)); d=max(d,len(work[v])); order.append(v)
        for u in tuple(work[v]): work[u].discard(v)
        del work[v]
    return d,order

def min_fill_width(nodes,adj):
    work={v:set(adj[v]) for v in nodes}; width=0; fill=0; order=[]
    while work:
        def key(v):
            ns=sorted(work[v]); missing=0
            for i,u in enumerate(ns):
                for w in ns[i+1:]:
                    if w not in work[u]: missing+=1
            return (missing,len(ns),v)
        v=min(work,key=key); ns=sorted(work[v]); width=max(width,len(ns)); order.append(v)
        for i,u in enumerate(ns):
            for w in ns[i+1:]:
                if w not in work[u]: work[u].add(w); work[w].add(u); fill+=1
        for u in ns: work[u].discard(v)
        del work[v]
    return width,fill,order

def analyze():
    m4=json.loads(M4_PATH.read_text()); assert m4["zero_cross_pair_digest_sha256"]==EXPECTED_ZC_DIGEST
    zc={tuple(sorted(map(int,e))) for e in m4["zero_cross_pairs"]}; assert len(zc)==1318
    with redirect_stdout(io.StringIO()): census,groups=O.build_authority()
    gids=tuple(g for g in range(250) if census[g]["multiplicity"]==4); assert len(gids)==90
    H=set(HUBS); I=set(ISOLATES); L=set(gids)-H-I; assert len(L)==75
    relhist=Counter(); ov_zc=[]; ov_nz=[]; sig=Counter(); dimhist=Counter(); classhist=Counter(); shapehist=Counter(); adj={g:set() for g in gids}
    for i,u in enumerate(gids):
        for v in gids[i+1:]:
            rel,inter=P.support_relation(groups[u]["projection_anchor"],groups[v]["projection_anchor"],PHYS_N); relhist[rel]+=1
            if rel!="overlap_incomparable": continue
            assert inter is not None; pair=(u,v); dim=len(inter[2])
            if pair in zc: ov_zc.append(pair); continue
            ov_nz.append(pair); adj[u].add(v); adj[v].add(u)
            cu="h" if u in H else "i" if u in I else "l"; cv="h" if v in H else "i" if v in I else "l"; cls="".join(sorted((cu,cv)))
            shape=f"{census[u]['image_size']}x{census[v]['image_size']}"; dimhist[dim]+=1; classhist[cls]+=1; shapehist[shape]+=1; sig[(cls,dim,shape)]+=1
    assert dict(sorted(relhist.items()))==EXPECTED_REL_HIST; assert len(ov_zc)==766; assert len(ov_nz)==2000
    comps=components(gids,adj); deg,degorder=degeneracy(gids,adj); mfwidth,fill,mforder=min_fill_width(gids,adj); dh=Counter(len(adj[g]) for g in gids)
    out={"position":O.POS,"physical_shared_dimension":PHYS_N,"multiplicity4_outputs":90,"support_relation_histogram":dict(sorted(relhist.items())),"overlap_incomparable_pairs":2766,"overlap_zero_cross_pairs":len(ov_zc),"overlap_nonzero_cross_pairs":len(ov_nz),"overlap_nonzero_cross_endpoint_class_histogram":dict(sorted(classhist.items())),"overlap_nonzero_cross_intersection_dimension_histogram":dict(sorted(dimhist.items())),"overlap_nonzero_cross_shape_histogram":dict(sorted(shapehist.items())),"overlap_nonzero_cross_signature_histogram":[{"endpoint_class":k[0],"intersection_dimension":k[1],"shape":k[2],"count":v} for k,v in sorted(sig.items())],"graph_edges":len(ov_nz),"graph_degree_histogram":dict(sorted(dh.items())),"graph_component_sizes":[len(c) for c in comps],"graph_degeneracy_lower_bound":deg,"graph_min_fill_width_upper_bound":mfwidth,"graph_min_fill_added_edges":fill,"degeneracy_order":degorder,"min_fill_order":mforder,"decision":"M4_OVERLAP_NONZERO_CROSS_GRAPH_STRUCTURALLY_CLASSIFIED"}
    print("result",json.dumps(out,sort_keys=True),flush=True); print("PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_OVERLAP_NONZERO_CROSS_GRAPH_SCOUT"); print("scope=structural classification only; no new value-level joint-image census"); print("ALPHA_PASS=0"); return out

if __name__=="__main__": analyze()
