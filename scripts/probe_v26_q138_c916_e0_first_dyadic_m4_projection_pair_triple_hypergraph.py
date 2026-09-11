#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter
from contextlib import redirect_stdout
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O

P=O.P
PHYS_N=O.PHYS_N
POS=O.POS
EXPECTED_M4_NORMAL_RANK=92
EXPECTED_PAIR_ONLY_COUNT=399610858487909714515834935717239427665960696108155457580263111360445
EXPECTED_PAIR_ONLY_LOG2=227.88970623785792
assert PHYS_N==149

def canonical_edges(edges):
    es=sorted(set(int(e) for e in edges if e), key=lambda x:(x.bit_count(),x))
    kept=[]
    for e in es:
        if not any((k & e)==k for k in kept):
            kept.append(e)
    return tuple(kept)

def weighted_hypergraph_count(n,weights,edges):
    memo={}
    calls=0
    max_depth=0
    def rec(active,eds,depth=0):
        nonlocal calls,max_depth
        calls+=1; max_depth=max(max_depth,depth)
        eds=canonical_edges(eds)
        factor=1
        while True:
            singles=0
            for e in eds:
                if e & (e-1)==0:
                    singles |= e
            singles &= active
            if not singles:
                break
            active &= ~singles
            eds=canonical_edges(e for e in eds if not (e & singles))
        used=0
        for e in eds:
            used |= e
        iso=active & ~used
        while iso:
            b=iso & -iso
            factor *= 1 + weights[b.bit_length()-1]
            iso ^= b
        active &= used
        if not active:
            return factor

        key=(active,eds)
        if key in memo:
            return factor*memo[key]

        remaining=active
        comps=[]
        while remaining:
            seed=remaining & -remaining
            comp=seed
            changed=True
            while changed:
                changed=False
                for e in eds:
                    if e & comp:
                        new=e & active & ~comp
                        if new:
                            comp |= new
                            changed=True
            remaining &= ~comp
            comps.append(comp)
        if len(comps)>1:
            z=1
            for comp in comps:
                ce=tuple(e for e in eds if e & comp)
                z*=rec(comp,ce,depth+1)
            memo[key]=z
            return factor*z

        deg=Counter()
        for e in eds:
            x=e
            while x:
                b=x & -x
                deg[b.bit_length()-1]+=1
                x^=b
        candidates=[i for i in range(n) if (active>>i)&1]
        v=max(candidates,key=lambda i:(deg[i],weights[i],-i))
        bit=1<<v

        ex_active=active & ~bit
        ex_edges=tuple(e for e in eds if not (e&bit))
        z0=rec(ex_active,ex_edges,depth+1)

        in_edges=[]
        invalid=False
        for e in eds:
            if e&bit:
                ne=e&~bit
                if ne==0:
                    invalid=True
                    break
                in_edges.append(ne)
            else:
                in_edges.append(e)
        z1=0 if invalid else weights[v]*rec(ex_active,tuple(in_edges),depth+1)
        z=z0+z1
        memo[key]=z
        return factor*z

    total=rec((1<<n)-1,tuple(edges))
    return total,{'memo_states':len(memo),'recursive_calls':calls,'max_recursion_depth':max_depth}

def synthetic_regression():
    n=6
    weights=(2,3,1,4,2,3)
    edges=((1<<0)|(1<<1),
           (1<<1)|(1<<2)|(1<<3),
           (1<<3)|(1<<4)|(1<<5))
    exact,stats=weighted_hypergraph_count(n,weights,edges)
    brute=0
    for mask in range(1<<n):
        if any((mask&e)==e for e in edges):
            continue
        w=1
        for i in range(n):
            if (mask>>i)&1:
                w*=weights[i]
        brute+=w
    assert exact==brute
    return {'weighted_count':exact,'memo_states':stats['memo_states']}

def normal_rank(groups,m4s):
    normals=[]
    for g in m4s:
        normals.extend(int(m) for m,_rhs in groups[g]['projection_anchor']['physical_support_constraints'])
    return P.R.gf2_rank(normals)

def analyze():
    syn=synthetic_regression()
    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4)
    assert len(m4s)==90
    assert normal_rank(groups,m4s)==EXPECTED_M4_NORMAL_RANK
    local={g:i for i,g in enumerate(m4s)}
    weights=tuple(int(census[g]['image_size'])-1 for g in m4s)
    assert Counter(weights)==Counter({6:88,8:2})
    assert all(0 in census[g]['counts'] for g in m4s)

    pair_edges=[]
    pair_disjoint=set()
    support_hist=Counter()
    for i,u in enumerate(m4s):
        for v in m4s[i+1:]:
            rel,_inter=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
            support_hist[rel]+=1
            if rel=='disjoint':
                pair_disjoint.add((u,v))
                pair_edges.append((1<<local[u])|(1<<local[v]))
    assert len(pair_edges)==359
    assert support_hist['disjoint']==359

    pair_count,pair_stats=weighted_hypergraph_count(len(m4s),weights,pair_edges)
    assert pair_count==EXPECTED_PAIR_ONLY_COUNT, (pair_count,EXPECTED_PAIR_ONLY_COUNT)

    triple_edges=[]
    triple_gid=[]
    triple_degree=Counter()
    tested_pairwise_intersecting=0
    for idx,(a,b,c) in enumerate(combinations(m4s,3),1):
        if (min(a,b),max(a,b)) in pair_disjoint or (min(a,c),max(a,c)) in pair_disjoint or (min(b,c),max(b,c)) in pair_disjoint:
            continue
        tested_pairwise_intersecting+=1
        constraints=(list(groups[a]['projection_anchor']['physical_support_constraints'])+
                     list(groups[b]['projection_anchor']['physical_support_constraints'])+
                     list(groups[c]['projection_anchor']['physical_support_constraints']))
        sol=P.C.P.U.T.rref(constraints,n=PHYS_N)
        if sol is None:
            mask=(1<<local[a])|(1<<local[b])|(1<<local[c])
            triple_edges.append(mask)
            triple_gid.append((a,b,c))
            triple_degree[a]+=1; triple_degree[b]+=1; triple_degree[c]+=1
        if idx%20000==0:
            print('progress triples',idx,'minimal_empty',len(triple_edges),flush=True)

    triple_digest=hashlib.sha256((''.join(f'{a}|{b}|{c}\n' for a,b,c in triple_gid)).encode()).hexdigest()
    combined_edges=tuple(pair_edges)+tuple(triple_edges)
    exact_count,stats=weighted_hypergraph_count(len(m4s),weights,combined_edges)
    assert 0<exact_count<=pair_count
    elog=math.log2(exact_count)
    gain=EXPECTED_PAIR_ONLY_LOG2-elog

    decision=('M4_PROJECTION_PAIR_TRIPLE_HYPERGRAPH_STRICTLY_BEATS_PAIR_ONLY'
              if exact_count<pair_count else
              'M4_PROJECTION_PAIR_TRIPLE_HYPERGRAPH_NO_GAIN')
    out={
        'position':POS,
        'physical_shared_dimension':PHYS_N,
        'm4_outputs':len(m4s),
        'm4_projection_normal_span_rank':EXPECTED_M4_NORMAL_RANK,
        'synthetic_weighted_hypergraph_regression':syn,
        'support_relation_histogram':dict(sorted(support_hist.items())),
        'pair_disjoint_edges':len(pair_edges),
        'all_m4_triples':math.comb(len(m4s),3),
        'pairwise_intersecting_triples_tested':tested_pairwise_intersecting,
        'minimal_empty_anchor_triples':len(triple_edges),
        'minimal_empty_triple_digest_sha256':triple_digest,
        'minimal_empty_triple_vertex_degree_histogram':dict(sorted(Counter(triple_degree.values()).items())),
        'minimal_empty_triple_top_vertices':[{'group_id':g,'degree':d} for g,d in sorted(triple_degree.items(),key=lambda x:(-x[1],x[0]))[:20]],
        'pair_only_exact_weighted_count':pair_count,
        'pair_only_exact_log2':math.log2(pair_count),
        'pair_only_dp_stats':pair_stats,
        'pair_plus_triple_exact_weighted_count':exact_count,
        'pair_plus_triple_exact_log2':elog,
        'gain_vs_pair_only_log2_bits':gain,
        'pair_plus_triple_state_bits':(exact_count-1).bit_length(),
        'dp_stats':stats,
        'decision':decision,
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_PROJECTION_PAIR_TRIPLE_HYPERGRAPH')
    print('scope=exact weighted count of all m4 nonzero-label assignments whose support avoids every disjoint anchor pair and every pairwise-intersecting but jointly empty anchor triple')
    print('theorem=every true nonzero-output support has nonempty projection-anchor intersection; therefore pair/triple empty intersections are rigorous forbidden hyperedges and the weighted hypergraph count upper-bounds the true 90-output m4 image')
    print('important=this uses isolated nonzero label multiplicities inside every feasible support, so it remains an upper bound rather than an exact physical image count')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
