#!/usr/bin/env python3
import json, math, sys
from collections import defaultdict, deque
from itertools import product
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_250way_sampled_pair_tree_bound as B

T=B.T
PHYS_N=B.PHYS_N
POS=B.POS
N=250
EXPECTED_TREE_COUNT=104924396549289894551742971384283046304785569891463833858811091198784336666266829156720254565496012800000000
EXPECTED_TREE_DIGEST='9c9f0cbe546db2bbfaa6d141f08add9ad3da5dce7397b095847eb8b375358433'
assert PHYS_N == 149

def rsize(m):
    return sum(int(x) for row in m for x in row)

def tree_adjacency(edges):
    adj=[[] for _ in range(N)]
    for u,v in edges:
        adj[u].append(v); adj[v].append(u)
    return tuple(tuple(sorted(x)) for x in adj)

def tree_path(adj,u,v):
    parent={u:-1}
    q=deque([u])
    while q:
        x=q.popleft()
        if x==v: break
        for y in adj[x]:
            if y not in parent:
                parent[y]=x; q.append(y)
    assert v in parent
    out=[]; x=v
    while x!=-1:
        out.append(x); x=parent[x]
    out.reverse()
    return tuple(out)

def directed_messages(edges, rel, states):
    adj=tree_adjacency(edges)
    cache={}
    def msg(u,v):
        key=(u,v)
        if key in cache: return cache[key]
        incoming=[msg(w,u) for w in adj[u] if w!=v]
        m=T.relation_matrix(rel,u,v)
        out=[]
        for sv in range(states[v]):
            z=0
            for su in range(states[u]):
                w=1
                for vec in incoming: w*=vec[su]
                if m[su][sv]: z+=w
            out.append(z)
        cache[key]=tuple(out)
        return cache[key]
    for u,v in edges:
        msg(u,v); msg(v,u)
    assert len(cache)==2*len(edges)
    return adj, cache

def endpoint_joint(p, adj, messages, rel, states):
    weights=[]
    for i,u in enumerate(p):
        prev=p[i-1] if i else None
        nxt=p[i+1] if i+1<len(p) else None
        vec=[]
        for su in range(states[u]):
            w=1
            for x in adj[u]:
                if x==prev or x==nxt: continue
                w*=messages[(x,u)][su]
            vec.append(w)
        weights.append(tuple(vec))
    cur=[[0]*states[p[0]] for _ in range(states[p[0]])]
    for s,w in enumerate(weights[0]): cur[s][s]=w
    for i in range(len(p)-1):
        u,v=p[i],p[i+1]
        m=T.relation_matrix(rel,u,v)
        nxt=[[0]*states[v] for _ in range(states[p[0]])]
        for a in range(states[p[0]]):
            for su in range(states[u]):
                base=cur[a][su]
                if not base: continue
                for sv in range(states[v]):
                    if m[su][sv]:
                        nxt[a][sv]+=base*weights[i+1][sv]
        cur=nxt
    return tuple(tuple(row) for row in cur)

def min_fill_order(n, edge_set):
    nbr=[set() for _ in range(n)]
    for u,v in edge_set:
        nbr[u].add(v); nbr[v].add(u)
    alive=set(range(n)); order=[]; width=0
    while alive:
        best=None
        for x in alive:
            ns=sorted(nbr[x] & alive)
            missing=0
            for i,a in enumerate(ns):
                for b in ns[i+1:]:
                    if b not in nbr[a]: missing+=1
            key=(missing,len(ns),x)
            if best is None or key<best[0]: best=(key,x,ns)
        _,x,ns=best
        width=max(width,len(ns))
        for i,a in enumerate(ns):
            for b in ns[i+1:]:
                nbr[a].add(b); nbr[b].add(a)
        alive.remove(x); order.append(x)
    return tuple(order), width

def exact_factor_count(n, edge_set, rel, states, order):
    factors=[]
    for u,v in edge_set:
        m=T.relation_matrix(rel,u,v)
        data={}
        for a in range(states[u]):
            for b in range(states[v]):
                if m[a][b]: data[(a,b)]=1
        factors.append(((u,v),data))
    peak_scope=2
    for x in order:
        hit=[f for f in factors if x in f[0]]
        if not hit: continue
        factors=[f for f in factors if x not in f[0]]
        union=tuple(sorted(set().union(*(set(s) for s,_ in hit))))
        peak_scope=max(peak_scope,len(union))
        rest=tuple(v for v in union if v!=x)
        pos={v:i for i,v in enumerate(union)}
        hpos=[([pos[v] for v in scope],data) for scope,data in hit]
        out=defaultdict(int)
        ranges=[range(states[v]) for v in union]
        for assignment in product(*ranges):
            z=1
            for inds,data in hpos:
                key=tuple(assignment[i] for i in inds)
                z*=data.get(key,0)
                if not z: break
            if z:
                out[tuple(assignment[pos[v]] for v in rest)]+=z
        factors.append((rest,dict(out)))
    assert all(scope==() for scope,_ in factors)
    total=1
    for _,data in factors:
        total*=data.get((),0)
    return total, peak_scope

def synthetic_regression():
    states=(2,3,2,2)
    rel={
        (0,1):((True,True,False),(False,True,True)),
        (1,2):((True,False),(True,True),(False,True)),
        (2,3):((True,True),(False,True)),
        (0,3):((True,False),(True,True)),
    }
    tree=((0,1),(1,2),(2,3))
    tc,_=T.tree_count_and_marginals(range(4),tree,rel,states)
    adj,msg=directed_messages(tree,rel,states)
    p=tree_path(adj,0,3)
    joint=endpoint_joint(p,adj,msg,rel,states)
    chord=T.relation_matrix(rel,0,3)
    cc=sum(joint[a][b] for a in range(2) for b in range(2) if chord[a][b])
    brute=0
    for a in product(*[range(s) for s in states]):
        ok=True
        for u,v in tree+((0,3),):
            if not T.relation_matrix(rel,u,v)[a[u]][a[v]]: ok=False; break
        brute+=int(ok)
    one=set(tuple(sorted(e)) for e in tree); one.add((0,3))
    order,width=min_fill_order(4,one)
    ve,peak=exact_factor_count(4,one,rel,states,order)
    assert tc>=cc==brute==ve and width<=2 and peak<=3
    return {'tree_count':tc,'one_chord_count':cc,'induced_width':width,'peak_factor_scope':peak}

def analyze():
    syn=synthetic_regression()
    c=B.build_combined()
    rel,states,desc=c['rel'],c['states'],c['desc']
    adj_all=B.adj_from_rel(N,rel)
    root=next(i for i,d in enumerate(desc) if d==('s',94))
    edges,count,_marg,_hist=B.sparse_greedy((root,),(),N,rel,states,adj_all)
    assert count==EXPECTED_TREE_COUNT and len(edges)==N-1
    summary=B.tree_summary(edges,rel,states,desc)
    assert summary['edge_relation_digest_sha256']==EXPECTED_TREE_DIGEST

    tree_set={tuple(sorted(e)) for e in edges}
    tadj,messages=directed_messages(edges,rel,states)
    candidates=[]
    for (u,v),m in rel.items():
        e=tuple(sorted((u,v)))
        if e in tree_set: continue
        p=tree_path(tadj,u,v)
        joint=endpoint_joint(p,tadj,messages,rel,states)
        assert sum(sum(row) for row in joint)==count
        chord=T.relation_matrix(rel,u,v)
        cc=sum(joint[a][b] for a in range(states[u]) for b in range(states[v]) if chord[a][b])
        assert 0 < cc <= count
        candidates.append((cc,len(p)-1,rsize(m),u,v,p))
    candidates.sort(key=lambda x:(x[0],x[1],x[2],x[3],x[4]))

    selected=[]; used_tree_edges=set()
    for rec in candidates:
        cc,plen,rs,u,v,p=rec
        if cc==count: continue
        pedges={tuple(sorted((p[i],p[i+1]))) for i in range(len(p)-1)}
        if pedges & used_tree_edges: continue
        selected.append(rec); used_tree_edges |= pedges

    cactus_edges=set(tree_set)
    for _,_,_,u,v,_ in selected: cactus_edges.add(tuple(sorted((u,v))))
    order,width=min_fill_order(N,cactus_edges)
    assert width<=2
    cactus_count,peak=exact_factor_count(N,cactus_edges,rel,states,order)
    assert peak<=3 and 0 < cactus_count <= count

    first_check=None
    if selected:
        cc,plen,rs,u,v,p=selected[0]
        one=set(tree_set); one.add(tuple(sorted((u,v))))
        o,w=min_fill_order(N,one)
        ve,pk=exact_factor_count(N,one,rel,states,o)
        assert ve==cc and w<=2 and pk<=3
        first_check={'left':desc[u],'right':desc[v],'tree_path_edges':plen,
                     'relation_size':rs,'one_chord_count':cc,
                     'log2_gain':math.log2(count)-math.log2(cc)}

    clog=math.log2(cactus_count)
    if cactus_count < (1<<PHYS_N):
        decision='C916_250WAY_SAMPLED_CACTUS_BOUND_BELOW_PHYSICAL_149'
    elif cactus_count < count:
        decision='C916_250WAY_SAMPLED_CACTUS_STRICTLY_BEATS_TREE_ONLY'
    else:
        decision='C916_250WAY_SAMPLED_CACTUS_NO_GAIN'
    out={
        'position':POS,'physical_shared_dimension':PHYS_N,'outputs':N,
        'synthetic_regression':syn,
        'available_relation_edges':len(rel),
        'frozen_tree_edge_count':len(edges),
        'frozen_tree_count':count,
        'frozen_tree_log2':math.log2(count),
        'frozen_tree_digest':summary['edge_relation_digest_sha256'],
        'non_tree_available_edges':len(candidates),
        'strict_single_chord_candidates':sum(1 for x in candidates if x[0] < count),
        'selected_edge_disjoint_chords':len(selected),
        'selected_fundamental_cycle_tree_edges':len(used_tree_edges),
        'certified_induced_width':width,
        'peak_factor_scope':peak,
        'cactus_edge_count':len(cactus_edges),
        'cactus_exact_assignment_count':cactus_count,
        'cactus_exact_log2':clog,
        'gain_vs_tree_log2_bits':math.log2(count)-clog,
        'gap_vs_physical_log2_bits':clog-PHYS_N,
        'first_selected_chord_crosscheck':first_check,
        'selected_chords':[
            {'left_kind':desc[u][0],'left_group_id':desc[u][1],
             'right_kind':desc[v][0],'right_group_id':desc[v][1],
             'tree_path_edges':plen,'relation_size':rs,
             'single_chord_count':cc,
             'single_chord_log2_gain':math.log2(count)-math.log2(cc)}
            for cc,plen,rs,u,v,p in selected
        ],
        'decision':decision,
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_250WAY_SAMPLED_CACTUS_BOUND')
    print('scope=exact cycle-aware CSP count from the frozen PR184 tree plus edge-disjoint fundamental-cycle chords chosen from the same 13800 exact sampled pair relations')
    print('theorem=edge-disjoint fundamental tree paths form a cactus; explicit min-fill order certifies induced width <=2 and exact variable elimination counts all relation-consistent assignments')
    print('important=this remains a sampled pair-relation upper bound; m4-m4 and unsampled base-m4 relations are not silently invented')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
