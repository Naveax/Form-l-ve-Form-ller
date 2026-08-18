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
S=sorted(A.S1)
R=A.R1


def linear_image_rank(M,basis):
    rows=[]
    for d in basis:
        z=0
        for j,(m,_b) in enumerate(M):
            z |= (((m&d).bit_count()&1)<<j)
        rows.append(z)
    return T.gf2_rank(rows,len(M))


def main():
    raw,_=P.direct_supports('D')
    C=Counter(can for _typ,_zs,can in raw)
    odd=[can for can,n in C.items() if n&1]
    assert len(odd)==12363
    groups=defaultdict(list)
    for can in odd:
        cond=P.canonical_condition(I.input_condition(can))
        groups[cond].append(can)
    assert len(groups)==8629
    assert Counter(map(len,groups.values()))==Counter({1:4895,2:3734})

    dimdist=Counter(); imagedist=Counter(); total=0; maxdim=0
    for cond,cans in groups.items():
        eq=[(row&MASK,(row>>128)&1) for row in cond]
        sol=T.rref(eq,n=128); assert sol is not None
        rank,x0,basis=sol[:3]
        assert rank==len(cond)
        B=G.affine_basis(cond)
        M=G.singleton_side_map(cans[0],S,R)
        for can in cans[1:]:
            U=G.singleton_side_map(can,S,R)
            assert all(G.implied_zero(B,m^u,b^c) for (m,b),(u,c) in zip(M,U))
        d=len(basis); q=linear_image_rank(M,basis)
        dimdist[d]+=1; imagedist[q]+=1; total += 1<<d; maxdim=max(maxdim,d)

    print('D_condition_groups',len(groups),
          'condition_free_dimension_distribution',dict(sorted(dimdist.items())),
          'left11_singleton_image_dimension_distribution',dict(sorted(imagedist.items())),
          'max_condition_free_dimension',maxdim,
          'total_group_point_incidences',total,flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_D_CONDITION_DIMENSIONS')
    print('scope=exact D direct-e2 condition/image geometry only; no assembled-rank theorem')

if __name__=='__main__':main()
