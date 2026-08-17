#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_predecessor_leaf_ad_input_activity as P
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T

S=sorted({0,1,2,3,4,5,12,13,14,15,16})
R=[i for i in range(32) if i not in S]


def rowspace_basis(can,sites):
    # The beta coefficient matrix has one row per canonical external equation.
    # Restrict rows to the requested beta sites and take its F2 row space.
    rows=[]
    for row in can:
        v=0
        for j,i in enumerate(sites):
            if (row>>(128+i))&1:v|=1<<j
        if v:rows.append(v)
    B={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p not in B:B[p]=x;break
            x^=B[p]
    return list(B.values())


def enumerate_space(B):
    vals={0}
    for b in B:vals|={x^b for x in list(vals)}
    return vals


def main():
    for pos in 'AD':
        objs=P.affine_supports(pos)
        UL=set();UR=set();distL={};distR={}
        for kind,z,can in objs:
            BL=rowspace_basis(can,S);BR=rowspace_basis(can,R)
            distL[len(BL)]=distL.get(len(BL),0)+1
            distR[len(BR)]=distR.get(len(BR),0)+1
            UL |= enumerate_space(BL); UR |= enumerate_space(BR)
        print('position',pos,'affine_terms',len(objs),
              'left_constraint_rank_distribution',distL,
              'right_constraint_rank_distribution',distR,
              'left_fourier_frequency_union',len(UL),
              'right_fourier_frequency_union',len(UR),
              'left_global_frequency_span_rank',T.gf2_rank(list(UL),len(S)),
              'right_global_frequency_span_rank',T.gf2_rank(list(UR),len(R)))
    print('PASS PROBE V26_Q138_AD_AFFINE_FOURIER_UNION')
    print('scope=homogeneous affine-factor frequency union; signed quadratic terms excluded')

if __name__=='__main__':main()
