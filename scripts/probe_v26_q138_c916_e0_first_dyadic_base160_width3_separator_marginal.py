#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import defaultdict
from contextlib import redirect_stdout
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_base160_certified_width3 as W

A=W.A
T=W.T
C=W.C
PHYS_N=W.PHYS_N
POS=W.POS
N=W.N
PARENT_GIDS=(1,2,13,14)
EXPECTED_COUNT=103580346297435478039507934992782327762124800000
EXPECTED_LOG2=156.1813707466197
EXPECTED_TREE_COUNT=W.EXPECTED_TREE_COUNT
EXPECTED_TREE_DIGEST=W.EXPECTED_TREE_DIGEST
assert PHYS_N==149 and N==160

def mask_of(matrix):
    z=0; bit=0
    for row in matrix:
        for x in row:
            if x:
                z |= 1<<bit
            bit+=1
    return z

def reconstruct_graph():
    with redirect_stdout(io.StringIO()):
        base=A.build_real_relations()
    desc=base['descriptors']; states=base['state_counts']; rel=base['relations']; local=base['local']
    root=local[('s',94)]
    tree,count,_=T.greedy_growth_tree(root,N,rel,states)
    assert count==EXPECTED_TREE_COUNT
    _,_,dig=A.tree_digest(tree,rel,desc)
    assert dig==EXPECTED_TREE_DIGEST
    graph={tuple(sorted(e)) for e in tree}
    pool,strict_total,strict_non_tree=W.candidate_pool(rel,states,graph)
    scored=W.score_by_tree(tree,rel,states,pool)
    accepted=[]
    for cc,plen,rs,u,v in scored:
        key=tuple(sorted((u,v)))
        if key in graph:
            continue
        trial=set(graph); trial.add(key)
        order,width=C.min_fill_order(N,trial)
        if width<=3:
            graph=trial
            accepted.append((cc,plen,rs,u,v,width))
    order,width=C.min_fill_order(N,graph)
    assert width==3 and len(accepted)==83 and len(graph)==242
    exact,peak=C.exact_factor_count(N,graph,rel,states,order)
    assert exact==EXPECTED_COUNT and peak<=4
    return base,tuple(sorted(graph)),tuple(order),tuple(accepted),strict_total,strict_non_tree

def exact_factor_count_fixed(edge_set,rel,states,order,fixed):
    factors=[]
    for u,v in edge_set:
        m=T.relation_matrix(rel,u,v)
        data={}
        ur=(fixed[u],) if u in fixed else range(states[u])
        vr=(fixed[v],) if v in fixed else range(states[v])
        for a in ur:
            for b in vr:
                if m[a][b]:
                    data[(a,b)]=1
        factors.append(((u,v),data))
    peak=2
    for x in order:
        hit=[f for f in factors if x in f[0]]
        if not hit:
            continue
        factors=[f for f in factors if x not in f[0]]
        union=tuple(sorted(set().union(*(set(s) for s,_ in hit))))
        peak=max(peak,len(union))
        rest=tuple(v for v in union if v!=x)
        pos={v:i for i,v in enumerate(union)}
        hpos=[([pos[v] for v in scope],data) for scope,data in hit]
        out=defaultdict(int)
        ranges=[(fixed[v],) if v in fixed else range(states[v]) for v in union]
        for assignment in product(*ranges):
            z=1
            for inds,data in hpos:
                key=tuple(assignment[i] for i in inds)
                z*=data.get(key,0)
                if not z:
                    break
            if z:
                out[tuple(assignment[pos[v]] for v in rest)]+=z
        factors.append((rest,dict(out)))
    assert all(scope==() for scope,_ in factors)
    total=1
    for _scope,data in factors:
        total*=data.get((),0)
    return total,peak

def synthetic_fixed_regression():
    states=(2,3,2,2,2)
    rel={
        (0,1):((True,True,False),(False,True,True)),
        (1,2):((True,False),(True,True),(False,True)),
        (2,3):((True,True),(False,True)),
        (0,3):((True,False),(True,True)),
        (1,4):((True,True),(False,True),(True,False)),
    }
    edges=tuple(rel)
    order=(2,3,1,0,4)
    seps=(0,4)
    table={}
    brute={}
    for assn in product(range(2),range(2)):
        fixed=dict(zip(seps,assn))
        table[assn],peak=exact_factor_count_fixed(edges,rel,states,order,fixed)
        assert peak<=3
        c=0
        for a in product(*[range(s) for s in states]):
            if tuple(a[v] for v in seps)!=assn:
                continue
            if all(rel[(u,v)][a[u]][a[v]] for u,v in edges):
                c+=1
        brute[assn]=c
    assert table==brute
    return {'total':sum(table.values()),'positive_entries':sum(v>0 for v in table.values())}

def analyze():
    syn=synthetic_fixed_regression()
    base,graph,order,accepted,strict_total,strict_non_tree=reconstruct_graph()
    desc=base['descriptors']; states=base['state_counts']; rel=base['relations']; local=base['local']
    sep=tuple(local[('s',g)] for g in PARENT_GIDS)
    assert all(states[x]==4 for x in sep)

    marginal={}
    max_peak=0
    for i,assn in enumerate(product(range(4),repeat=4),1):
        fixed=dict(zip(sep,assn))
        count,peak=exact_factor_count_fixed(graph,rel,states,order,fixed)
        marginal[assn]=count
        max_peak=max(max_peak,peak)
        if i%64==0:
            print('progress separator',i,'/ 256','positive',sum(v>0 for v in marginal.values()),flush=True)
    assert sum(marginal.values())==EXPECTED_COUNT
    assert max_peak<=4

    edge_rows=[]
    digest_rows=[]
    for u,v in graph:
        m=T.relation_matrix(rel,u,v)
        mask=mask_of(m)
        edge_rows.append({
            'u':u,'v':v,'left_kind':desc[u][0],'left_group_id':desc[u][1],
            'right_kind':desc[v][0],'right_group_id':desc[v][1],
            'rows':states[u],'cols':states[v],'mask_hex':f'{mask:x}',
        })
        digest_rows.append(f'{desc[u][0]}:{desc[u][1]}|{desc[v][0]}:{desc[v][1]}|{states[u]}x{states[v]}|{mask:x}')
    gdigest=hashlib.sha256(('\n'.join(digest_rows)+'\n').encode()).hexdigest()

    positive=[{'states':list(a),'count':c} for a,c in sorted(marginal.items()) if c]
    mdigest=hashlib.sha256((''.join(f'{"|".join(map(str,a))}|{c}\n' for a,c in sorted(marginal.items()))).encode()).hexdigest()

    artifact={
        'position':POS,'physical_shared_dimension':PHYS_N,
        'base_outputs':N,'exact_graph_count':EXPECTED_COUNT,
        'exact_graph_log2':EXPECTED_LOG2,'graph_edges':edge_rows,
        'graph_relation_digest_sha256':gdigest,
        'separator_group_ids':list(PARENT_GIDS),
        'separator_local_indices':list(sep),
        'separator_positive_marginal':positive,
        'separator_marginal_digest_sha256':mdigest,
        'elimination_order':list(order),
    }
    ap=Path('artifacts/c916_e0_first_dyadic_base160_width3_separator_authority.json')
    ap.parent.mkdir(parents=True,exist_ok=True)
    ap.write_text(json.dumps(artifact,sort_keys=True,separators=(',',':'))+'\n')

    out={
        'position':POS,'physical_shared_dimension':PHYS_N,'outputs':N,
        'synthetic_fixed_regression':syn,
        'strict_pair_relations':strict_total,'strict_non_tree_relations':strict_non_tree,
        'accepted_chords':len(accepted),'final_edges':len(graph),
        'certified_induced_width':3,'peak_factor_scope':max_peak,
        'exact_assignment_count':EXPECTED_COUNT,'exact_log2':math.log2(EXPECTED_COUNT),
        'separator_group_ids':list(PARENT_GIDS),
        'separator_assignments':256,
        'separator_positive_entries':len(positive),
        'separator_zero_entries':256-len(positive),
        'separator_marginal_digest_sha256':mdigest,
        'graph_relation_digest_sha256':gdigest,
        'largest_separator_mass':max(marginal.values()),
        'smallest_positive_separator_mass':min(c for c in marginal.values() if c),
        'authority_artifact_path':str(ap),
        'decision':'C916_BASE160_WIDTH3_FOUR_SINGLETON_SEPARATOR_MARGINAL_EXACT',
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_BASE160_WIDTH3_SEPARATOR_MARGINAL')
    print('scope=exact four-singleton separator marginal for the frozen PR200 242-edge certified-width3 base160 factor graph')
    print('theorem=each of 256 fixed separator assignments is counted exactly with the same certified width3 elimination order; their sum reproduces the frozen PR200 exact count')
    print('important=this is an authority for later contraction with m4 family factors, not a new physical-image theorem by itself')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
