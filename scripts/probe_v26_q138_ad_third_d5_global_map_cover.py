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
    eq=[(row&MASK,(row>>128)&1) for row in rows]
    return T.rref(eq,n=128) is not None


def main():
    raw,_=P.direct_supports('D')
    groups=defaultdict(list)
    for typ,zs,can in raw:
        cond=P.canonical_condition(I.input_condition(can))
        groups[cond].append((tuple(zs),can))
    assert len(groups)==8629

    data=[]
    for cond,items in groups.items():
        B=G.affine_basis(cond);M=G.singleton_side_map(items[0][1],S,R)
        for _zs,can in items[1:]:
            assert eq_on_condition(B,G.singleton_side_map(can,S,R),M)
        U=set().union(*(set(zs) for zs,_can in items))
        data.append((cond,M,frozenset(U)))

    freq=Counter(r for cond,_M,_U in data for r in cond)
    core=[r for r,_ in freq.most_common(5)]
    assert [freq[r] for r in core]==[8446,8444,8267,8265,8265]
    coreB=G.affine_basis(tuple(core))

    compatible=[]
    for cond,M,U in data:
        rows=tuple(core)+tuple(cond)
        if not consistent(rows):continue
        B=G.affine_basis(rows)
        compatible.append((cond,B,M,U))
    assert len(compatible)==8084

    # Historical one-template-per-zero-site family.
    sites=sorted({z for _cond,_B,_M,U in compatible for z in U})
    assert len(sites)==93
    bysite=defaultdict(list)
    for k,x in enumerate(compatible):
        for z in x[3]:bysite[z].append(k)
    site_templates=[compatible[bysite[z][0]][2] for z in sites]

    # Collapse site templates that are already the same affine map on the D5 core.
    reps=[]
    for M in site_templates:
        if not any(eq_on_condition(coreB,M,Tm) for Tm in reps):reps.append(M)
    print('D5_compatible_groups',len(compatible),
          'raw_zero_site_templates',len(site_templates),
          'distinct_zero_site_templates_mod_D5',len(reps),flush=True)

    covered=0;uncovered=[]
    for k,(cond,B,M,U) in enumerate(compatible):
        if any(eq_on_condition(B,M,Tm) for Tm in reps):covered+=1
        else:uncovered.append(k)
    print('D5_zero_site_template_covered',covered,'uncovered',len(uncovered),flush=True)

    # Deterministic constructive cover: whenever a group is still uncovered,
    # add its own affine map as one global template. The final family is a
    # rigorous uniform row-count upper on D5, regardless of minimality.
    added=0
    for k in uncovered:
        cond,B,M,U=compatible[k]
        if any(eq_on_condition(B,M,Tm) for Tm in reps):continue
        reps.append(M);added+=1
    # Verify all groups are covered by the final global map family.
    miss=[]
    cover_mult=Counter()
    for k,(cond,B,M,U) in enumerate(compatible):
        n=sum(eq_on_condition(B,M,Tm) for Tm in reps)
        cover_mult[n]+=1
        if not n:miss.append(k)
    assert not miss

    outside_upper=max(len(data)-freq[r] for r in core)
    inside_upper=len(reps)
    global_upper=max(outside_upper,inside_upper)
    print('D5_added_uncovered_group_templates',added,
          'D5_constructive_global_map_cover_size',inside_upper,
          'D5_cover_multiplicity_distribution',dict(sorted(cover_mult.items())),flush=True)
    print('D_outside_D5_active_group_upper',outside_upper,
          'D_direct_e2_rank_uniform_upper_from_cover',global_upper,
          'D_complete_third_rank_sum_upper',min(2048,global_upper+171),flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_D5_GLOBAL_MAP_COVER')
    print('scope=constructive uniform singleton-row-map cover for D direct-e2 plus known outside-core active-count bound; inherited e1 correction only added by subadditivity')

if __name__=='__main__':main()
