#!/usr/bin/env python3
import itertools,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as F
import probe_v26_q138_predecessor_leaf_bc_second_residue_correction_classes as C
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import probe_v26_q138_predecessor_leaf_fast_nullspace_fourier as Q


def freq(can):
    return F.enumerate_space(F.rowspace_basis(can,F.S))


def weight120_union_fast(pos):
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    _,res,free,extra=Q.setup(pos,False)
    U=set();full=0
    for zs in itertools.combinations(sites,4):
        B=Q.left_space(res,free,extra,zs)
        if B is None:continue
        full+=1;U |= Q.enumerate_space(B)
    assert full==29041
    expected=668 if pos=='B' else 788
    assert len(U)==expected,(pos,len(U),expected)
    return U


def main():
    e0,e1,half=H.classify_patterns()
    for pos in 'BC':
        U120=weight120_union_fast(pos)

        raw1=[]
        for k in range(4):
            for zs,cls in e1[k]:
                can=H.support_for(pos,zs,cls)
                if can is not None:raw1.append(can)
        CC=Counter(raw1);odd1=[can for can,n in CC.items() if n&1]
        U1=set()
        for can in odd1:U1 |= freq(can)
        assert len(U1)==(320 if pos=='B' else 704)

        raw0=[]
        for k in range(4):
            for zs,cls in e0[k]:
                can=H.support_for(pos,zs,cls)
                if can is not None:raw0.append(can)
        U0=set()
        for can in raw0:U0 |= freq(can)
        assert len(U0)==(92 if pos=='B' else 104)

        print('position',pos,
              'weight120_union',len(U120),'e1_odd_union',len(U1),'intersection_120_e1',len(U120&U1),
              'combined_120_e1_union',len(U120|U1),
              'raw_e0_union',len(U0),'e0_intersection_combined',len(U0&(U120|U1)),
              'combined_with_raw_e0_union',len(U120|U1|U0),flush=True)

    print('PASS PROBE V26_Q138_BC_SECOND_RESIDUE_FREQUENCY_OVERLAP')
    print('scope=homogeneous support-indicator frequency overlap; sign-negative and half-sector Boolean corrections excluded')

if __name__=='__main__':main()
