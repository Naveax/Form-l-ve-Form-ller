#!/usr/bin/env python3
import io, json, sys
from collections import Counter, defaultdict, deque
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O

P = O.P
PHYS_N = O.PHYS_N
assert PHYS_N == 149
EXPECTED_LEFT = 312
EXPECTED_RIGHT = 513
EXPECTED_EDGES = 825

def components(adj):
    unseen=set(adj); out=[]
    while unseen:
        root=min(unseen); q=[root]; unseen.remove(root); comp=[]
        while q:
            v=q.pop(); comp.append(v)
            for u in adj[v]:
                if u in unseen:
                    unseen.remove(u); q.append(u)
        out.append(tuple(sorted(comp)))
    return tuple(sorted(out,key=lambda c:(-len(c),c)))

def min_fill_order(adj):
    work={v:set(ns) for v,ns in adj.items()}; order=[]; width=0; fill_added=0
    while work:
        best=None
        for v,ns in work.items():
            nsl=sorted(ns); fill=0
            for i,a in enumerate(nsl):
                wa=work[a]
                for b in nsl[i+1:]:
                    if b not in wa: fill+=1
            key=(fill,len(ns),v)
            if best is None or key<best[0]: best=(key,v)
        v=best[1]; ns=sorted(work[v]); width=max(width,len(ns))
        for i,a in enumerate(ns):
            for b in ns[i+1:]:
                if b not in work[a]:
                    work[a].add(b); work[b].add(a); fill_added+=1
        for u in ns: work[u].remove(v)
        del work[v]; order.append(v)
    return tuple(order),width,fill_added

def degeneracy(adj):
    work={v:set(ns) for v,ns in adj.items()}; k=0; order=[]
    while work:
        v=min(work,key=lambda x:(len(work[x]),x)); d=len(work[v]); k=max(k,d); order.append(v)
        for u in list(work[v]): work[u].remove(v)
        del work[v]
    return k,tuple(order)

def analyze():
    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4)
    assert len(m4s)==90
    adj={g:set() for g in m4s}; direction=Counter(); interdim=Counter(); oriented=[]
    for i,u in enumerate(m4s):
        for v in m4s[i+1:]:
            rel,inter=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
            if rel not in ('left_subset_right','right_subset_left'): continue
            assert inter is not None
            adj[u].add(v); adj[v].add(u); direction[rel]+=1; interdim[(rel,len(inter[2]))]+=1
            oriented.append((u,v) if rel=='left_subset_right' else (v,u))
    assert sum(direction.values())==EXPECTED_EDGES
    assert direction==Counter({'left_subset_right':EXPECTED_LEFT,'right_subset_left':EXPECTED_RIGHT})
    comps=components(adj); deg=Counter(len(adj[g]) for g in m4s); dgen,_=degeneracy(adj)
    mf_order,mf_width,mf_fill=min_fill_order(adj)
    succ=defaultdict(set); indeg={g:0 for g in m4s}
    for a,b in oriented:
        if b not in succ[a]: succ[a].add(b); indeg[b]+=1
    q=deque(sorted(g for g in m4s if indeg[g]==0)); topo=[]
    while q:
        v=q.popleft(); topo.append(v)
        for u in sorted(succ[v]):
            indeg[u]-=1
            if indeg[u]==0: q.append(u)
    assert len(topo)==len(m4s)
    longest={g:1 for g in m4s}; parent={}
    for v in topo:
        for u in succ[v]:
            if longest[v]+1>longest[u]: longest[u]=longest[v]+1; parent[u]=v
    end=max(m4s,key=lambda g:(longest[g],-g)); chain=[end]
    while chain[-1] in parent: chain.append(parent[chain[-1]])
    chain=tuple(reversed(chain))
    out={
        'position':O.POS,'physical_shared_dimension':PHYS_N,'m4_outputs':len(m4s),
        'subset_support_edges':EXPECTED_EDGES,'left_subset_right_edges':direction['left_subset_right'],
        'right_subset_left_edges':direction['right_subset_left'],'degree_histogram':dict(sorted(deg.items())),
        'minimum_degree':min(deg),'maximum_degree':max(deg),'connected_components':len(comps),
        'component_size_histogram':dict(sorted(Counter(map(len,comps)).items())),
        'largest_component_size':len(comps[0]),'degeneracy_lower_bound_on_treewidth':dgen,
        'min_fill_induced_width_upper_bound':mf_width,'min_fill_added_fill_edges':mf_fill,
        'min_fill_order':list(mf_order),'longest_strict_subset_chain_length':len(chain),
        'longest_strict_subset_chain_group_ids':list(chain),
        'direction_intersection_dimension_histogram':[
            {'support_relation':r,'intersection_dimension':d,'count':n} for (r,d),n in sorted(interdim.items())],
        'decision':'M4_SUBSET_SUPPORT_GRAPH_STRUCTURE_MEASURED'}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_SUBSET_SUPPORT_GRAPH_STRUCTURE')
    print('scope=projection-support containment graph only; no value-level relation masks are evaluated')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
