#!/usr/bin/env python3
import hashlib, io, json, math, sys
from collections import Counter
from contextlib import redirect_stdout
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O
import probe_v26_q138_c916_e0_first_dyadic_m4_m4_nonzero_correlation_joint_images as J
import probe_v26_q138_c916_e0_first_dyadic_singleton_m2_cross_joint_image as X
import probe_v26_q138_c916_e0_first_dyadic_m4_projection_pair_triple_hypergraph as H

P=O.P
PHYS_N=O.PHYS_N
POS=O.POS
EXPECTED_PROJECTION_TRIPLE_DIGEST='3dd086974c55e495828bff85119cb542435b7498c69decc7fe5e9247316452a4'
EXPECTED_DISJOINT=359
EXPECTED_EQUAL_ZERO_CROSS=10
EXPECTED_SUBSET_ZERO_CROSS=183
assert PHYS_N==149

def fwht(a):
    a=list(a); h=1; n=len(a)
    while h<n:
        for i in range(0,n,2*h):
            for j in range(i,i+h):
                x=a[j]; y=a[j+h]
                a[j]=x+y; a[j+h]=x-y
        h*=2
    return a

def expand_mask(comp, positions):
    out=0
    for j,p in enumerate(positions):
        if (comp>>j)&1: out |= 1<<p
    return out

def has_simultaneous_nonzero(left,right,ambient,icache):
    lt,rt=tuple(left['terms']),tuple(right['terms'])
    assert len(lt)==len(rt)==4
    terms=lt+rt
    assert len({int(t['term_id']) for t in terms})==8
    full=(1<<8)-1
    mcache={}
    active_order=sorted(range(full+1),key=lambda a:(-a.bit_count(),a))
    for active in active_order:
        positions=tuple(i for i in range(8) if (active>>i)&1)
        k=len(positions)
        def exact(char):
            total=0
            for u in X.submasks(full ^ active):
                z=X.character_moment(terms,active|u,char,ambient,icache,mcache)
                total += -z if u.bit_count() & 1 else z
            return total
        size=exact(0)
        assert size>=0
        if not size: continue
        vals=[]
        for comp in range(1<<k):
            char=expand_mask(comp,positions)
            vals.append(exact(char))
        pops=fwht(vals)
        div=1<<k
        for negc,num in enumerate(pops):
            assert num%div==0
            pop=num//div
            assert pop>=0
            if not pop: continue
            neg=expand_mask(negc,positions)
            lv=rv=0
            for i,t in enumerate(terms):
                if not ((active>>i)&1): continue
                z=int(t['coefficient'])
                if (neg>>i)&1: z=-z
                if i<4: lv+=z
                else: rv+=z
            if lv!=0 and rv!=0:
                return True,len(mcache)
    return False,len(mcache)

def synthetic_regression():
    n=5
    anchors=[
        P.make_synthetic_anchor((),n,'linear'),
        P.make_synthetic_anchor(((1,0),),n,'quadratic'),
        P.make_synthetic_anchor(((2,1),),n,'one'),
        P.make_synthetic_anchor(((4,0),),n,'linear'),
        P.make_synthetic_anchor(((8,1),),n,'quadratic'),
        P.make_synthetic_anchor(((16,0),),n,'linear'),
        P.make_synthetic_anchor(((3,1),),n,'one'),
        P.make_synthetic_anchor(((5,0),),n,'quadratic'),
    ]
    def term(i,a,c):
        return {'term_id':i,'group_id':-1,'kind':'synthetic','coefficient':c,'anchor':a,'ambient_dimension':n}
    left={'terms':tuple(term(i+1,anchors[i],(1,-1,2,-2)[i]) for i in range(4))}
    right={'terms':tuple(term(i+5,anchors[i+4],(2,1,-2,-1)[i]) for i in range(4))}
    got,_=has_simultaneous_nonzero(left,right,n,{})
    brute=any(X.eval_group(left,x)!=0 and X.eval_group(right,x)!=0 for x in range(1<<n))
    assert got==brute
    return {'domain_points_checked':1<<n,'simultaneous_nonzero':got}

def projection_minimal_empty_triples(m4s,groups,pair_disjoint):
    triples=[]
    for a,b,c in combinations(m4s,3):
        if (a,b) in pair_disjoint or (a,c) in pair_disjoint or (b,c) in pair_disjoint:
            continue
        constraints=(list(groups[a]['projection_anchor']['physical_support_constraints'])+
                     list(groups[b]['projection_anchor']['physical_support_constraints'])+
                     list(groups[c]['projection_anchor']['physical_support_constraints']))
        if P.C.P.U.T.rref(constraints,n=PHYS_N) is None:
            triples.append((a,b,c))
    digest=hashlib.sha256((''.join(f'{a}|{b}|{c}\n' for a,b,c in triples)).encode()).hexdigest()
    assert digest==EXPECTED_PROJECTION_TRIPLE_DIGEST
    assert len(triples)==5
    return tuple(triples)

def analyze():
    syn=synthetic_regression()
    with redirect_stdout(io.StringIO()):
        census,groups=O.build_authority()
    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4)
    assert len(m4s)==90
    local={g:i for i,g in enumerate(m4s)}
    weights=tuple(int(census[g]['image_size'])-1 for g in m4s)
    assert Counter(weights)==Counter({6:88,8:2})

    icache={}
    support_hist=Counter()
    zero_hist=Counter()
    zero_pairs=[]
    pair_disjoint=set()
    tested=0
    early_nonzero=0
    moment_cache_total=0
    for pi,(u,v) in enumerate(combinations(m4s,2),1):
        rel,_=P.support_relation(groups[u]['projection_anchor'],groups[v]['projection_anchor'],PHYS_N)
        support_hist[rel]+=1
        if rel=='disjoint':
            pair_disjoint.add((u,v))
            zero_pairs.append((u,v))
            zero_hist[rel]+=1
        else:
            tested+=1
            has,mn=has_simultaneous_nonzero(groups[u],groups[v],PHYS_N,icache)
            moment_cache_total+=mn
            if has:
                early_nonzero+=1
            else:
                zero_pairs.append((u,v))
                zero_hist[rel]+=1
        if pi%250==0:
            print('progress pairs',pi,'/',math.comb(90,2),'zero_cross',len(zero_pairs),
                  'nonzero_witness',early_nonzero,flush=True)

    assert len(pair_disjoint)==EXPECTED_DISJOINT
    assert zero_hist['equal']==EXPECTED_EQUAL_ZERO_CROSS, zero_hist
    assert zero_hist['left_subset_right']+zero_hist['right_subset_left']==EXPECTED_SUBSET_ZERO_CROSS, zero_hist

    pair_digest=hashlib.sha256((''.join(f'{u}|{v}\n' for u,v in zero_pairs)).encode()).hexdigest()
    pair_edges=tuple((1<<local[u])|(1<<local[v]) for u,v in zero_pairs)
    graph_count,graph_stats=H.weighted_hypergraph_count(len(m4s),weights,pair_edges)

    triples=projection_minimal_empty_triples(m4s,groups,pair_disjoint)
    triple_edges=tuple((1<<local[a])|(1<<local[b])|(1<<local[c]) for a,b,c in triples)
    combined_count,combined_stats=H.weighted_hypergraph_count(len(m4s),weights,pair_edges+triple_edges)
    assert 0<combined_count<=graph_count

    redundant_triples=sum(any((((1<<local[a])|(1<<local[b])|(1<<local[c])) & e)==e for e in pair_edges)
                          for a,b,c in triples)
    out={
        'position':POS,'physical_shared_dimension':PHYS_N,'m4_outputs':len(m4s),
        'synthetic_simultaneous_nonzero_regression':syn,
        'support_relation_histogram':dict(sorted(support_hist.items())),
        'non_disjoint_pairs_exactly_tested':tested,
        'zero_cross_pair_count':len(zero_pairs),
        'zero_cross_support_relation_histogram':dict(sorted(zero_hist.items())),
        'zero_cross_pair_digest_sha256':pair_digest,
        'overlap_incomparable_zero_cross_pairs':zero_hist['overlap_incomparable'],
        'exact_nonzero_witness_pairs':early_nonzero,
        'support_intersection_cache_entries':len(icache),
        'per_pair_character_moment_cache_entries_summed':moment_cache_total,
        'zero_cross_graph_exact_weighted_count':graph_count,
        'zero_cross_graph_exact_log2':math.log2(graph_count),
        'zero_cross_graph_state_bits':(graph_count-1).bit_length(),
        'zero_cross_graph_dp_stats':graph_stats,
        'projection_minimal_empty_triples':len(triples),
        'projection_triples_redundant_after_zero_cross_graph':redundant_triples,
        'zero_cross_plus_projection_triples_exact_weighted_count':combined_count,
        'zero_cross_plus_projection_triples_exact_log2':math.log2(combined_count),
        'zero_cross_plus_projection_triples_state_bits':(combined_count-1).bit_length(),
        'combined_dp_stats':combined_stats,
        'gain_vs_pr192_pair_only_log2_bits':227.88970623785792-math.log2(combined_count),
        'gain_vs_pr197_projection_pair_triple_log2_bits':224.59037822806647-math.log2(combined_count),
        'decision':'M4_COMPLETE_ZERO_CROSS_GRAPH_COUNT_EXACT',
    }
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_COMPLETE_ZERO_CROSS_GRAPH')
    print('scope=exact complete m4-m4 zero-cross graph: every unordered m4 pair is either structurally disjoint or exactly tested for existence of any simultaneous-nonzero physical state')
    print('theorem=every true m4 nonzero-support set is independent in this complete zero-cross graph; adding the frozen PR197 minimal-empty projection triples remains rigorous')
    print('important=non-zero-cross pairs may still have other nonlinear restrictions; this count uses only the exact zero-cross predicate plus the five projection triples')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__':
    analyze()
