#!/usr/bin/env python3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_ad_third_direct_e2_condition_group_rank1 as G
import verify_v26_q138_predecessor_leaf_ad_third_e1_correction_rank362_171 as C1
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T

MASK=(1<<128)-1
S=sorted(A.S1);R=A.R1


def eq_on_condition(B,M,U):
    return all(G.implied_zero(B,m^u,b^c) for (m,b),(u,c) in zip(M,U))


def consistent(rows):
    return T.rref([(row&MASK,(row>>128)&1) for row in rows],n=128) is not None


def direct_cover_and_core():
    raw,_=P.direct_supports('D')
    CC=Counter(can for _typ,_zs,can in raw)
    odd={can for can,n in CC.items() if n&1}
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

    data=[]
    for cond,items in groups.items():
        B=G.affine_basis(cond);M=G.singleton_side_map(items[0][0],S,R)
        for can,_U in items[1:]:assert eq_on_condition(B,G.singleton_side_map(can,S,R),M)
        U=set().union(*(set(u) for _can,u in items))
        data.append((cond,M,frozenset(U)))

    freq=Counter(r for cond,_M,_U in data for r in cond)
    core=tuple(r for r,_ in freq.most_common(5))
    assert [freq[r] for r in core]==[8446,8444,8267,8265,8265]
    coreB=G.affine_basis(core)
    compatible=[]
    for cond,M,U in data:
        rows=core+tuple(cond)
        if not consistent(rows):continue
        B=G.affine_basis(rows)
        compatible.append((cond,B,M,U))
    assert len(compatible)==8084

    sites=sorted({z for _cond,_B,_M,U in compatible for z in U})
    assert len(sites)==90
    bysite=defaultdict(list)
    for k,x in enumerate(compatible):
        for z in x[3]:bysite[z].append(k)
    reps=[]
    for z in sites:
        M=compatible[bysite[z][0]][2]
        if not any(eq_on_condition(coreB,M,Tm) for Tm in reps):reps.append(M)
    assert len(reps)==54
    for _cond,B,M,_U in compatible:
        if any(eq_on_condition(B,M,Tm) for Tm in reps):continue
        reps.append(M)
    assert len(reps)==851
    for _cond,B,M,_U in compatible:
        assert any(eq_on_condition(B,M,Tm) for Tm in reps)
    return core,reps,compatible


def main():
    core,reps,direct=direct_cover_and_core()
    direct_cover=len(reps);assert direct_cover==851

    corr=[];types=Counter();outside=0
    for typ,can in C1.e1_supports('D'):
        assert A.cut_intersection(can)==0
        assert C1.left_beta_rank(can)==11
        cond=P.canonical_condition(I.input_condition(can))
        M=G.singleton_side_map(can,S,R)
        rows=core+tuple(cond)
        if not consistent(rows):
            outside+=1
            continue
        B=G.affine_basis(rows)
        corr.append((typ,cond,B,M));types[typ]+=1
    assert sum(types.values())+outside==274
    print('D5_correction_compatible',len(corr),'outside_D5_correction_sectors',outside,
          'D5_correction_type_distribution',dict(types),flush=True)

    covered0=[];uncovered=[]
    for k,(_typ,_cond,B,M) in enumerate(corr):
        if any(eq_on_condition(B,M,Tm) for Tm in reps):covered0.append(k)
        else:uncovered.append(k)
    print('D5_correction_rows_covered_by_direct851',len(covered0),
          'D5_correction_rows_uncovered',len(uncovered),flush=True)

    added=0
    for k in uncovered:
        _typ,_cond,B,M=corr[k]
        if any(eq_on_condition(B,M,Tm) for Tm in reps):continue
        reps.append(M);added+=1
    for _typ,_cond,B,M in corr:
        assert any(eq_on_condition(B,M,Tm) for Tm in reps)

    inside=len(reps)
    # Outside the forced D5 core, direct-e2 row rank is at most364 and the
    # inherited e1 correction has uniform rank at most171. Row-support union
    # therefore has rank at most535 by subadditivity, without requiring any
    # common-template claim outside D5.
    outside_upper=364+171
    global_upper=max(inside,outside_upper)
    print('D5_added_correction_templates',added,
          'D5_combined_direct_correction_row_cover',inside,
          'outside_D5_combined_rank_upper',outside_upper,
          'D_third_combined_row_rank_uniform_upper',global_upper,flush=True)
    print('PASS PROBE V26_Q138_D_THIRD_COMBINED_ROW_COVER')
    print('scope=complete D third binary residue row-rank envelope under the admitted e0-zero lift; no complete leaf Schmidt-rank or arithmetic-work claim')

if __name__=='__main__':main()
