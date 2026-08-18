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
    raw,_=P.direct_supports('D')
    C=Counter(can for _typ,_zs,can in raw)
    odd={can for can,n in C.items() if n&1}
    assert len(odd)==12363

    zmeta=defaultdict(list)
    for _typ,zs,can in raw:
        if can in odd:zmeta[can].append(tuple(zs))

    groups=defaultdict(list)
    for can in odd:
        cond=P.canonical_condition(I.input_condition(can))
        U=set().union(*(set(zs) for zs in zmeta[can]))
        groups[cond].append((can,frozenset(U)))
    assert len(groups)==8629
    assert Counter(map(len,groups.values()))==Counter({1:4895,2:3734})

    data=[]
    for cond,items in groups.items():
        B=G.affine_basis(cond);M=G.singleton_side_map(items[0][0],S,R)
        for can,_U in items[1:]:
            assert eq_on_condition(B,G.singleton_side_map(can,S,R),M)
        U=set().union(*(set(u) for _can,u in items))
        data.append((cond,M,frozenset(U)))

    freq=Counter(r for cond,_M,_U in data for r in cond)
    core=[r for r,_ in freq.most_common(5)]
    assert [freq[r] for r in core]==[8446,8444,8267,8265,8265]
    outside=max(len(data)-freq[r] for r in core)
    assert outside==364
    coreB=G.affine_basis(tuple(core))

    compatible=[]
    for cond,M,U in data:
        rows=tuple(core)+tuple(cond)
        if not consistent(rows):continue
        B=G.affine_basis(rows)
        compatible.append((cond,B,M,U))
    assert len(compatible)==8084

    sites=sorted({z for _cond,_B,_M,U in compatible for z in U})
    assert len(sites)==90
    bysite=defaultdict(list)
    for k,x in enumerate(compatible):
        for z in x[3]:bysite[z].append(k)
    site_templates=[compatible[bysite[z][0]][2] for z in sites]

    reps=[]
    for M in site_templates:
        if not any(eq_on_condition(coreB,M,Tm) for Tm in reps):reps.append(M)
    assert len(reps)==54

    covered=[];uncovered=[]
    for k,(_cond,B,M,_U) in enumerate(compatible):
        if any(eq_on_condition(B,M,Tm) for Tm in reps):covered.append(k)
        else:uncovered.append(k)
    assert len(covered)==4413 and len(uncovered)==3671

    added=0
    for k in uncovered:
        _cond,B,M,_U=compatible[k]
        if any(eq_on_condition(B,M,Tm) for Tm in reps):continue
        reps.append(M);added+=1
    assert added==797 and len(reps)==851

    cover_mult=Counter()
    for _cond,B,M,_U in compatible:
        n=sum(eq_on_condition(B,M,Tm) for Tm in reps)
        assert n>=1
        cover_mult[n]+=1
    assert cover_mult==Counter({1:7390,2:676,3:18})

    direct=max(outside,len(reps))
    assert direct==851
    inherited=171
    total=direct+inherited
    assert total==1022 and total<2048

    print('PASS V26_Q138_PREDECESSOR_LEAF_D_THIRD_RANK1022')
    print('D5_compatible_groups=8084 D5_zero_sites=90 initial_templates=54')
    print('D5_initial_covered=4413 added_templates=797 final_cover=851')
    print('D_outside_D5_direct_upper=364 D_direct_e2_rank_Q<=851')
    print('D_inherited_e1_correction_rank_Q<=171 D_third_index2_rank_Q<=1022')
    print('scope=third dyadic integer-lift rank only; no complete leaf rank or arithmetic-work claim')

if __name__=='__main__':main()
