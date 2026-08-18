#!/usr/bin/env python3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_ad_third_direct_e2_condition_group_rank1 as G
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T

MASK=(1<<128)-1
S=sorted(A.S1);R=A.R1


def eq_on_condition(B,M,U):
    return all(G.implied_zero(B,m^u,b^c) for (m,b),(u,c) in zip(M,U))


def consistent(rows):
    return T.rref([(row&MASK,(row>>128)&1) for row in rows],n=128) is not None


def main():
    raw,_=P.direct_supports('A')
    C=Counter(can for _typ,_zs,can in raw)
    odd={can for can,n in C.items() if n&1}
    assert len(odd)==12098
    zmeta=defaultdict(list)
    for _typ,zs,can in raw:
        if can in odd:zmeta[can].append(tuple(zs))

    groups=defaultdict(list)
    for can in odd:
        cond=P.canonical_condition(I.input_condition(can))
        U=set().union(*(set(zs) for zs in zmeta[can]))
        groups[cond].append((can,frozenset(U)))
    assert len(groups)==4531
    assert Counter(map(len,groups.values()))==Counter({1:617,2:261,3:3653})

    data=[]
    for cond,items in groups.items():
        B=G.affine_basis(cond);M=G.singleton_side_map(items[0][0],R,S)
        for can,_U in items[1:]:
            assert eq_on_condition(B,G.singleton_side_map(can,R,S),M)
        U=set().union(*(set(u) for _can,u in items))
        data.append((cond,M,frozenset(U)))

    freq=Counter(r for cond,_M,_U in data for r in cond)
    core=[r for r,_ in freq.most_common(6)]
    assert [freq[r] for r in core]==[4437,4437,4435,4343,4342,4250]
    coreB=G.affine_basis(tuple(core))

    compatible=[]
    for cond,M,U in data:
        rows=tuple(core)+tuple(cond)
        if not consistent(rows):continue
        B=G.affine_basis(rows)
        compatible.append((cond,B,M,U))
    assert len(compatible)==4067

    sites=sorted({z for _cond,_B,_M,U in compatible for z in U})
    bysite=defaultdict(list)
    for k,x in enumerate(compatible):
        for z in x[3]:bysite[z].append(k)
    site_templates=[compatible[bysite[z][0]][2] for z in sites]

    reps=[]
    for M in site_templates:
        if not any(eq_on_condition(coreB,M,Tm) for Tm in reps):reps.append(M)
    print('A6_compatible_groups',len(compatible),
          'zero_sites_present',len(sites),
          'raw_zero_site_templates',len(site_templates),
          'distinct_zero_site_templates_mod_A6',len(reps),flush=True)

    covered=0;uncovered=[]
    for k,(cond,B,M,U) in enumerate(compatible):
        if any(eq_on_condition(B,M,Tm) for Tm in reps):covered+=1
        else:uncovered.append(k)
    print('A6_zero_site_template_covered',covered,'uncovered',len(uncovered),flush=True)

    added=0
    for k in uncovered:
        cond,B,M,U=compatible[k]
        if any(eq_on_condition(B,M,Tm) for Tm in reps):continue
        reps.append(M);added+=1

    cover_mult=Counter();miss=[]
    for k,(cond,B,M,U) in enumerate(compatible):
        n=sum(eq_on_condition(B,M,Tm) for Tm in reps)
        cover_mult[n]+=1
        if not n:miss.append(k)
    assert not miss

    # Outside the certified A6 core: violating one of first five common
    # literals leaves at most189 groups; inside first5 but sixth-false leaves182.
    outside_upper=189
    inside_upper=len(reps)
    global_upper=max(outside_upper,inside_upper)
    print('A6_added_uncovered_group_templates',added,
          'A6_constructive_global_map_cover_size',inside_upper,
          'A6_cover_multiplicity_distribution',dict(sorted(cover_mult.items())),flush=True)
    print('A_outside_A6_active_group_upper',outside_upper,
          'A_direct_e2_rank_uniform_upper_from_cover',global_upper,
          'A_complete_third_rank_sum_upper',min(2048,global_upper+362),flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_A6_GLOBAL_MAP_COVER')
    print('scope=constructive uniform singleton-row-map cover for A direct-e2 plus known outside-core active-count bound; inherited e1 correction only added by subadditivity')

if __name__=='__main__':main()
