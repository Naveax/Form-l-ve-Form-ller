#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_singleton_m2_160way_joint_tree_bound as A
import probe_v26_q138_c916_e0_first_dyadic_m4_support_stratified_joint_candidates as M

T=A.T; PHYS_N=A.PHYS_N; POS=A.POS
N_BASE=160; N_M4=90; N=250
EXPECTED_BASE_COUNT=3554017933804264224365028336898853306322124800000
EXPECTED_BASE_DIGEST='7deca3ac2fa0e6eb498fd6b2b111927787c158d4afe751e9c59c4fc3cb459118'
EXPECTED_M4_DIGEST='bb248e577bf15a60fb28f027ba44c24b243113e33390697396f050afb4443cd4'
EXPECTED_M4_STRICT=901
assert PHYS_N==149

def rsize(m): return sum(int(x) for row in m for x in row)

def adj_from_rel(n, rel):
    a=[[] for _ in range(n)]
    for u,v in rel: a[u].append(v); a[v].append(u)
    return tuple(tuple(sorted(x)) for x in a)

def sparse_kruskal(n, rel, states):
    p=list(range(n)); sz=[1]*n
    def find(x):
        while p[x]!=x:
            p[x]=p[p[x]]; x=p[x]
        return x
    def union(a,b):
        a,b=find(a),find(b)
        if a==b: return False
        if sz[a]<sz[b]: a,b=b,a
        p[b]=a; sz[a]+=sz[b]; return True
    cand=[]
    for (u,v),m in rel.items():
        s=rsize(m); cand.append((Fraction(s,states[u]*states[v]),s,u,v))
    cand.sort(); edges=[]
    for _,_,u,v in cand:
        if union(u,v):
            edges.append((u,v))
            if len(edges)==n-1: break
    T.validate_tree(range(n),edges)
    return tuple(edges)

def sparse_greedy(init_nodes, init_edges, n, rel, states, adj):
    selected=set(init_nodes); edges=list(init_edges); T.validate_tree(selected,edges)
    hist=[]
    while len(selected)<n:
        current,marg=T.tree_count_and_marginals(selected,edges,rel,states)
        best=None
        for u in sorted(selected):
            mu=marg[u]
            for v in adj[u]:
                if v in selected: continue
                m=T.relation_matrix(rel,u,v); deg=tuple(sum(row) for row in m)
                ext=sum(mu[s]*deg[s] for s in range(states[u]))
                key=(ext,rsize(m),max(deg),states[v],u,v)
                if best is None or key<best[0]: best=(key,u,v,deg)
        assert best is not None
        key,u,v,deg=best; selected.add(v); edges.append((u,v))
        hist.append((current,key[0],u,v,rsize(T.relation_matrix(rel,u,v)),deg))
    count,marg=T.tree_count_and_marginals(range(n),edges,rel,states)
    assert hist[-1][1]==count
    return tuple(edges),count,marg,tuple(hist)

def build_combined():
    with redirect_stdout(io.StringIO()):
        base=A.build_real_relations()
        census,groups=M.O.build_authority()
    desc=tuple(base['descriptors']); states0=tuple(base['state_counts']); rel=dict(base['relations'])
    assert len(desc)==160 and len(rel)==12720
    root=base['local'][('s',94)]
    bedges,bcount,_=T.greedy_growth_tree(root,160,rel,states0)
    assert bcount==EXPECTED_BASE_COUNT
    _,_,bdigest=A.tree_digest(bedges,rel,desc)
    assert bdigest==EXPECTED_BASE_DIGEST
    bcheck,bmarg=T.tree_count_and_marginals(range(160),bedges,rel,states0)
    assert bcheck==bcount

    parents=tuple(g for _,g in desc)
    gid2base={g:i for i,(_,g) in enumerate(desc)}
    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4)
    assert len(parents)==160 and len(m4s)==90
    m4node={g:160+i for i,g in enumerate(m4s)}
    descall=desc+tuple(('m4',g) for g in m4s)
    states=states0+tuple(census[g]['image_size'] for g in m4s)
    assert Counter(states[160:])==Counter({7:88,9:2})
    small=tuple(g for g in parents if census[g]['multiplicity']==2 and census[g]['image_size']==3)
    assert small==(53,71,126,149,170,227)
    selected={g:M.select(g,parents,small,census,groups) for g in m4s}
    assert sum(len(x) for x in selected.values())==1080

    ic,mc={},{}; dig=[]; strict=checks=0
    for mg in m4s:
        v=m4node[mg]; mv=tuple(sorted(census[mg]['counts']))
        for meta in selected[mg]:
            pg=int(meta['parent_group_id']); u=gid2base[pg]; pv=tuple(sorted(census[pg]['counts']))
            counts,pm,mm=M.pair_census(groups[pg],groups[mg],PHYS_N,ic,mc)
            assert pm==census[pg]['counts'] and mm==census[mg]['counts']; checks+=2
            mat=tuple(tuple((a,b) in counts for b in mv) for a in pv)
            assert len(mat)==states[u] and len(mat[0])==states[v]
            assert all(any(row) for row in mat)
            assert all(any(mat[a][b] for a in range(len(mat))) for b in range(len(mat[0])))
            rel[(u,v)]=mat
            if rsize(mat)<states[u]*states[v]: strict+=1
            mask=bit=0
            for row in mat:
                for x in row:
                    if x: mask|=1<<bit
                    bit+=1
            dig.append(f'{pg}|{mg}|{len(pv)}x{len(mv)}|{mask:x}')
    mdigest=hashlib.sha256(('\n'.join(sorted(dig))+'\n').encode()).hexdigest()
    assert checks==2160 and strict==EXPECTED_M4_STRICT and mdigest==EXPECTED_M4_DIGEST
    assert len(rel)==13800
    return dict(base=base,census=census,groups=groups,desc=descall,states=states,rel=rel,
                bedges=tuple(bedges),bcount=bcount,bmarg=bmarg,bdigest=bdigest,
                m4s=m4s,m4node=m4node,mdigest=mdigest,checks=checks,strict=strict,
                m4_support_cache=len(ic),m4_moment_cache=len(mc))

def leaf_greedy(c,adj):
    rel,states=c['rel'],c['states']; selected=set(range(160)); edges=list(c['bedges'])
    rem=set(range(160,250)); hist=[]
    while rem:
        current,marg=T.tree_count_and_marginals(selected,edges,rel,states); best=None
        for v in sorted(rem):
            for u in adj[v]:
                if u>=160: continue
                m=T.relation_matrix(rel,u,v); deg=tuple(sum(row) for row in m)
                ext=sum(marg[u][s]*deg[s] for s in range(states[u]))
                key=(ext,rsize(m),max(deg),u,v)
                if best is None or key<best[0]: best=(key,u,v,deg)
        key,u,v,deg=best; selected.add(v); rem.remove(v); edges.append((u,v))
        hist.append((current,key[0],u,v,key[1],deg))
    count,marg=T.tree_count_and_marginals(range(250),edges,rel,states)
    assert hist[-1][1]==count and count>=c['bcount']
    return tuple(edges),count,marg,tuple(hist)

def tree_summary(edges,rel,states,desc):
    hist=Counter(); dens=Counter(); fam=Counter(); deg=Counter(); adj=defaultdict(list); rows=[]
    for u,v in edges:
        m=T.relation_matrix(rel,u,v); s=rsize(m); hist[s]+=1; dens[f'{s}/{states[u]*states[v]}']+=1
        ku,kv=desc[u][0],desc[v][0]
        if 'm4' in (ku,kv): fam['base_m4' if ku!=kv else 'm4_m4']+=1
        elif ku==kv=='s': fam['singleton_singleton']+=1
        elif ku==kv=='m2': fam['m2_m2']+=1
        else: fam['singleton_m2']+=1
        adj[u].append(v); adj[v].append(u)
        mask=bit=0
        for row in m:
            for x in row:
                if x: mask|=1<<bit
                bit+=1
        rows.append(f'{ku}:{desc[u][1]}|{kv}:{desc[v][1]}|{len(m)}x{len(m[0])}|{mask:x}')
    for i in range(250): deg[len(adj[i])]+=1
    m4deg=Counter(len(adj[i]) for i in range(160,250))
    return dict(edge_count=len(edges),edge_joint_image_size_histogram=dict(sorted(hist.items())),
                edge_density_histogram=dict(sorted(dens.items())),edge_family_histogram=dict(sorted(fam.items())),
                node_degree_histogram=dict(sorted(deg.items())),m4_degree_histogram=dict(sorted(m4deg.items())),
                m4_internal_node_count=sum(v for d,v in m4deg.items() if d>1),
                edge_relation_digest_sha256=hashlib.sha256(('\n'.join(rows)+'\n').encode()).hexdigest())

def analyze():
    c=build_combined(); rel,states,desc=c['rel'],c['states'],c['desc']; adj=adj_from_rel(250,rel)
    assert all(adj[i] for i in range(250))
    assert all(len(adj[i])==12 for i in range(160,250))
    isolated=1
    for s in states: isolated*=s
    assert isolated==(4**103)*(3**6)*(5**51)*(7**88)*(9**2)

    ledges,lcount,_,lhist=leaf_greedy(c,adj)
    kedges=sparse_kruskal(250,rel,states); kcount,_=T.tree_count_and_marginals(range(250),kedges,rel,states)

    local={d:i for i,d in enumerate(desc)}
    roots=[local[d] for d in [('s',94),('s',209),('m2',21),('m4',20),('m4',31),('m4',83)]]
    rres=[]; bestroot=None
    for root in roots:
        e,count,_,h=sparse_greedy((root,),(),250,rel,states,adj)
        rec=(count,root,e,h); rres.append(rec)
        if bestroot is None or (count,root)<(bestroot[0],bestroot[1]): bestroot=rec

    pc=[]
    for (u,v),m in rel.items():
        s=rsize(m); pc.append((Fraction(s,states[u]*states[v]),s,u,v))
    pc.sort(); preseeds=[(u,v) for _,_,u,v in pc[:6]]
    pres=[]; bestpair=None
    for u,v in preseeds:
        e,count,_,h=sparse_greedy((u,v),((u,v),),250,rel,states,adj)
        rec=(count,u,v,e,h); pres.append(rec)
        if bestpair is None or (count,u,v)<(bestpair[0],bestpair[1],bestpair[2]): bestpair=rec

    cand={'frozen_160_tree_plus_m4_leaf_greedy':lcount,
          'sparse_250_kruskal':kcount,
          'sparse_250_best_root_greedy':bestroot[0],
          'sparse_250_best_pair_seed_greedy':bestpair[0]}
    method,bound=min(cand.items(),key=lambda kv:(kv[1],kv[0]))
    emap={'frozen_160_tree_plus_m4_leaf_greedy':ledges,'sparse_250_kruskal':kedges,
          'sparse_250_best_root_greedy':bestroot[2],'sparse_250_best_pair_seed_greedy':bestpair[3]}
    edges=emap[method]; check,marg=T.tree_count_and_marginals(range(250),edges,rel,states)
    assert check==bound and len(edges)==249
    blog=math.log2(bound); ilog=math.log2(isolated)
    poshist=Counter(sum(int(w>0) for w in ws) for ws in marg.values())
    if bound<(1<<149): decision='C916_250WAY_SAMPLED_PAIR_TREE_BOUND_BELOW_PHYSICAL_149'
    elif bound<isolated: decision='C916_250WAY_SAMPLED_PAIR_TREE_BOUND_STRICTLY_BELOW_ISOLATED_ONLY'
    else: decision='C916_250WAY_SAMPLED_PAIR_TREE_BOUND_NO_STRICT_GAIN'
    out={'position':POS,'physical_shared_dimension':149,'outputs':250,'singleton_outputs':103,
         'multiplicity2_outputs':57,'multiplicity4_outputs':90,'base_pair_relations':12720,
         'sampled_base_m4_relations':1080,'sampled_base_m4_strict_relations':c['strict'],
         'combined_relation_edges':len(rel),'m4_pair_marginal_crosschecks':c['checks'],
         'frozen_160_tree_assignment_count':c['bcount'],'frozen_160_tree_log2':math.log2(c['bcount']),
         'frozen_160_tree_digest':c['bdigest'],'m4_candidate_digest':c['mdigest'],
         'isolated_cartesian_state_count':isolated,'isolated_cartesian_log2':ilog,
         'isolated_cartesian_state_bits':(isolated-1).bit_length(),'candidate_tree_counts':cand,
         'leaf_only_history_final_count':lhist[-1][1],
         'selected_root_greedy':[{'kind':desc[r][0],'group_id':desc[r][1],'tree_count':count}
                                 for count,r,_,_ in sorted(rres)],
         'selected_pair_seed_greedy':[{'left_kind':desc[u][0],'left_group_id':desc[u][1],
             'right_kind':desc[v][0],'right_group_id':desc[v][1],
             'initial_joint_image_size':rsize(T.relation_matrix(rel,u,v)),'tree_count':count}
             for count,u,v,_,_ in sorted(pres)],
         'selected_tree_method':method,'selected_tree_consistent_assignment_count':bound,
         'selected_tree_consistent_log2':blog,'selected_tree_state_bits':(bound-1).bit_length(),
         'tree_gain_vs_isolated_log2_bits':ilog-blog,'tree_gap_vs_physical_log2_bits':blog-149,
         'selected_tree':dict(tree_summary(edges,rel,states,desc),
             node_marginal_positive_state_count_histogram=dict(sorted(poshist.items())),
             edges=[{'left_kind':desc[u][0],'left_group_id':desc[u][1],
                     'right_kind':desc[v][0],'right_group_id':desc[v][1],
                     'joint_image_size':rsize(T.relation_matrix(rel,u,v))} for u,v in edges]),
         'cached_m4_support_intersections':c['m4_support_cache'],
         'cached_m4_character_moments':c['m4_moment_cache'],'decision':decision}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_250WAY_SAMPLED_PAIR_TREE_BOUND')
    print('scope=rigorous 250-output pair-tree upper bound from all 12720 exact singleton/m2 pair relations plus 1080 exact support-stratified base-to-m4 relations')
    print('theorem=every true 250-output tuple satisfies the selected pair relations, so every spanning tree on this sampled relation graph gives a valid exact-DP superset bound')
    print('important=m4 nodes may be internal tree nodes; m4-m4 relations and the unprobed base-m4 pairs remain outside the sampled graph')
    print('next=if the pair-tree bound stays above 2^149, move to cycle/junction-tree exact counting instead of adding more leaf constraints')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
