#!/usr/bin/env python3
import sys
from collections import Counter,defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A

MASK=(1<<128)-1
S=sorted(A.S1)
R=A.R1


def affine_basis(cond):
    B={}
    for row in cond:
        y=row&MASK; b=(row>>128)&1
        while y:
            p=y.bit_length()-1
            if p in B:
                rr=B[p]; y^=rr&MASK; b^=(rr>>128)&1
            else:
                B[p]=y|(b<<128); break
        assert y or not b
    return B


def implied_zero(B,m,b):
    y=m; bb=b
    while y:
        p=y.bit_length()-1
        if p not in B:return False
        rr=B[p]; y^=rr&MASK; bb^=(rr>>128)&1
    return bb==0


def singleton_side_map(can,keep,elim):
    rows=list(can); r=0
    for i in elim:
        col=128+i
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    rr=rows[r:]; q=0; piv=[]
    for qq,i in enumerate(keep):
        col=128+i
        p=next((k for k in range(q,len(rr)) if (rr[k]>>col)&1),None)
        if p is None:continue
        rr[q],rr[p]=rr[p],rr[q]
        for k in range(len(rr)):
            if k!=q and ((rr[k]>>col)&1):rr[k]^=rr[q]
        piv.append(qq); q+=1
    assert q==len(keep),(len(keep),q)
    out=[None]*len(keep)
    for row,p in zip(rr[:q],piv):
        # all kept beta variables except the pivot were eliminated
        for j,i in enumerate(keep):
            if j!=p:assert not ((row>>(128+i))&1)
        out[p]=(row&MASK,(row>>160)&1)
    assert all(z is not None for z in out)
    return tuple(out)


def main():
    expected={
        'A':(12098,4531,Counter({3:3653,2:261,1:617})),
        'D':(12363,8629,Counter({2:3734,1:4895})),
    }
    for pos in 'AD':
        raw,_=P.direct_supports(pos)
        C=Counter(can for _,_,can in raw)
        odd=[can for can,n in C.items() if n&1]
        assert len(odd)==expected[pos][0],(pos,len(odd))
        assert all(A.cut_intersection(can)==0 for can in odd)
        G=defaultdict(list)
        for can in odd:
            cond=P.canonical_condition(I.input_condition(can))
            G[cond].append(can)
        assert len(G)==expected[pos][1]
        assert Counter(map(len,G.values()))==expected[pos][2]

        keep,elim=(R,S) if pos=='A' else (S,R)
        for cond,cans in G.items():
            B=affine_basis(cond)
            M0=singleton_side_map(cans[0],keep,elim)
            for can in cans[1:]:
                M=singleton_side_map(can,keep,elim)
                for (m,b),(m0,b0) in zip(M,M0):
                    assert implied_zero(B,m^m0,b^b0),(pos,cond)
        side='right21' if pos=='A' else 'left11'
        print('position',pos,'odd_direct_supports',len(odd),
              'distinct_predecessor_conditions',len(G),
              'condition_support_multiplicity',dict(sorted(Counter(map(len,G.values())).items())),
              'all_cut_intersection_zero',True,
              'common_singleton_side_per_condition',side,
              'condition_group_binary_rank_Q<=1',flush=True)
    print('PASS V26_Q138_PREDECESSOR_LEAF_AD_THIRD_DIRECT_E2_CONDITION_GROUP_RANK1')
    print('A_direct_e2_rank_Q(x)<=number_of_active_distinct_A_conditions_among_4531')
    print('D_direct_e2_rank_Q(x)<=number_of_active_distinct_D_conditions_among_8629')
    print('scope=direct e=2 component only; inherited e1 correction and assembled cross-group overlap remain separate')

if __name__=='__main__':main()
