#!/usr/bin/env python3
import itertools,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as F


def canonical_condition(cond):
    rank,eq=cond;rows=[m|((rhs&1)<<128) for m,rhs in eq];r=0
    for col in range(128):
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    return tuple(rows[:r])


def direct_supports(pos):
    sites=[(j,i) for j in range(1,4) for i in range(31)]
    FF=D.full_forms(pos);raw=[];stats=Counter()
    # k=2, weight91, top nullity survives: n=1, e=k-1+n=2.
    for zs in itertools.combinations(sites,2):
        C=D.carries(zs,ad=True);sol=A.internal_null(pos,C)
        if sol[0]!=127:continue
        assert len(sol[2])==1
        der=A.derivative_form(FF,A.map_internal_to_full(sol[2][0]))
        can=A.canonical_support(pos,C,der,127)
        if can is None:stats['w91_external_impossible']+=1;continue
        raw.append(('w91n1',zs,can));stats['w91_reachable']+=1
    # k=3, weight90, full rank: n=0, e=k-1=2.
    for zs in itertools.combinations(sites,3):
        C=D.carries(zs,ad=True);sol=A.internal_null(pos,C)
        if sol[0]!=128:continue
        can=A.canonical_support(pos,C,expect_internal=128)
        if can is None:stats['w90_external_impossible']+=1;continue
        raw.append(('w90full',zs,can));stats['w90_reachable']+=1
    return raw,stats


def main():
    for pos in 'AD':
        raw,stats=direct_supports(pos)
        C=Counter(can for _,_,can in raw)
        odd=[can for can,n in C.items() if n&1]
        mult=Counter(C.values())
        cuts=Counter(A.cut_intersection(can) for can in odd)
        U=set()
        for can in odd:U |= F.enumerate_space(F.rowspace_basis(can,F.S))
        conds=[canonical_condition(I.input_condition(can)) for can in odd]
        G=Counter(conds)
        print('position',pos,'raw_direct_e2',len(raw),'sector_stats',dict(stats),
              'canonical_support_groups',len(C),'multiplicity_distribution',dict(sorted(mult.items())),
              'odd_supports',len(odd),'cut_intersection_distribution',dict(sorted(cuts.items())),
              'odd_left_frequency_union',len(U),'distinct_input_conditions',len(G),
              'input_condition_multiplicity_distribution',dict(sorted(Counter(G.values()).items())),flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_DIRECT_E2_SUPPORTS')
    print('scope=exact direct e=2 support-indicator component only; higher-bit corrections from e=0/e=1 sectors remain separate')

if __name__=='__main__':main()
