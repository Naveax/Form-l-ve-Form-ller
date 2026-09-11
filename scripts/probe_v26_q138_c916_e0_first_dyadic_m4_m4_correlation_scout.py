#!/usr/bin/env python3
import json, math, sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O

D=O.D; P=O.P; POS=O.POS; PHYS_N=O.PHYS_N; TOP_K=8
assert PHYS_N==149

def analyze():
    census,groups=O.build_authority()
    m4s=tuple(g for g in range(250) if census[g]['multiplicity']==4)
    assert len(m4s)==90
    assert Counter(census[g]['image_size'] for g in m4s)==Counter({7:88,9:2})
    norms={g:O.norm2(census[g]['counts']) for g in m4s}
    cache={}
    for g in m4s:
        assert D.group_inner(groups[g],groups[g],cache)==norms[g]

    pair_count=0; zero=0; relation_hist=Counter(); rho_hist=Counter()
    all_rows=[]; by_node=defaultdict(list)
    for ai,g in enumerate(m4s):
        for h in m4s[ai+1:]:
            inner=D.group_inner(groups[g],groups[h],cache)
            rho=Fraction(inner*inner,norms[g]*norms[h])
            assert 0<=rho<1
            if inner==0: zero+=1
            if rho==0: bucket='0'
            elif rho>=Fraction(1,2): bucket='[1/2,1)'
            elif rho>=Fraction(1,4): bucket='[1/4,1/2)'
            elif rho>=Fraction(1,16): bucket='[1/16,1/4)'
            else: bucket='(0,1/16)'
            rho_hist[bucket]+=1
            rel,inter=P.support_relation(groups[g]['projection_anchor'],groups[h]['projection_anchor'],PHYS_N)
            relation_hist[rel]+=1
            rec={'left_group_id':g,'right_group_id':h,
                 'left_image_size':census[g]['image_size'],'right_image_size':census[h]['image_size'],
                 'inner_product':int(inner),'rho2_numerator':int(rho.numerator),
                 'rho2_denominator':int(rho.denominator),
                 'projection_support_relation':rel,
                 'projection_intersection_dimension':None if inter is None else len(inter[2])}
            key=(rho,abs(inner),-census[g]['image_size']*census[h]['image_size'],-g,-h)
            all_rows.append((key,rec))
            by_node[g].append((rho,abs(inner),-census[h]['image_size'],-h,h,rec))
            by_node[h].append((rho,abs(inner),-census[g]['image_size'],-g,g,rec))
            pair_count+=1
    assert pair_count==90*89//2==4005

    all_rows.sort(key=lambda x:x[0],reverse=True)
    maxrho=all_rows[0][0][0]
    selected=set(); per_node={}
    for g in m4s:
        rows=sorted(by_node[g],reverse=True); top=rows[:TOP_K]
        per_node[str(g)]=[
            {'other_group_id':r[4],
             'rho2_numerator':int(r[0].numerator),'rho2_denominator':int(r[0].denominator),
             'inner_product':int(r[1]),
             'projection_support_relation':r[5]['projection_support_relation'],
             'projection_intersection_dimension':r[5]['projection_intersection_dimension']}
            for r in top]
        for r in top: selected.add(tuple(sorted((g,r[4]))))

    if zero==pair_count: decision='M4_M4_ALL_PAIRWISE_ORTHOGONAL'
    elif zero: decision='M4_M4_MIXED_ZERO_AND_NONZERO_CORRELATION'
    else: decision='M4_M4_ALL_PAIRS_NONZERO_CORRELATION'

    out={'position':POS,'physical_shared_dimension':PHYS_N,'multiplicity4_outputs':90,
         'm4_m4_pairs':pair_count,'zero_inner_product_pairs':zero,
         'nonzero_inner_product_pairs':pair_count-zero,
         'projection_support_relation_histogram':dict(sorted(relation_hist.items())),
         'correlation_squared_bucket_histogram':dict(sorted(rho_hist.items())),
         'maximum_exact_correlation_squared':{'numerator':int(maxrho.numerator),
             'denominator':int(maxrho.denominator),'float':float(maxrho)},
         'top_k_per_m4':TOP_K,'top_k_union_candidate_pairs':len(selected),
         'global_strongest_pairs_top40':[r for _,r in all_rows[:40]],
         'per_m4_top_neighbors':per_node,'term_inner_cache_entries':len(cache),
         'decision':decision}
    print('result',json.dumps(out,sort_keys=True),flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_M4_M4_CORRELATION_SCOUT')
    print('scope=exact full-domain inner-product/correlation census across all 4005 unordered multiplicity-4 output pairs')
    print('purpose=decide whether correlation can rank a bounded candidate layer before expensive exact eight-term m4-m4 joint-image evaluation')
    print('important=correlation is only a selector; zero correlation does not imply Cartesian nonlinear joint image')
    print('ALPHA_PASS=0')
    return out

if __name__=='__main__': analyze()
