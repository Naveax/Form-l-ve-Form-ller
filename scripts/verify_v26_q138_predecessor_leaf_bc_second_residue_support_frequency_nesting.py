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


def union_freq(supports):
    U=set()
    for can in supports:
        U |= F.enumerate_space(F.rowspace_basis(can,F.S))
    return U


def weight120_union(pos):
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    _,res,free,extra=Q.setup(pos,False)
    U=set();full=0
    for zs in itertools.combinations(sites,4):
        B=Q.left_space(res,free,extra,zs)
        if B is None:continue
        full+=1;U |= Q.enumerate_space(B)
    assert full==29041
    return U


def main():
    e0,e1,half=H.classify_patterns()
    assert [len(e1[k]) for k in range(4)]==[0,102,2397,8196]
    assert [len(e0[k]) for k in range(4)]==[1,22,74,484]
    assert len(half)==4

    for pos in 'BC':
        U120=weight120_union(pos)
        assert len(U120)==(668 if pos=='B' else 788)

        raw1=[]
        for k in range(4):
            for zs,cls in e1[k]:
                can=H.support_for(pos,zs,cls)
                if can is not None:raw1.append(can)
        CC=Counter(raw1);odd1=[can for can,n in CC.items() if n&1]
        U1=union_freq(odd1)
        assert len(U1)==(320 if pos=='B' else 704)

        raw0=[]
        for k in range(4):
            for zs,cls in e0[k]:
                can=H.support_for(pos,zs,cls)
                if can is not None:raw0.append(can)
        U0=union_freq(raw0)
        assert len(raw0)==(581 if pos=='B' else 577)
        assert len(U0)==(92 if pos=='B' else 104)

        assert U1 <= U120
        assert U0 <= U120
        assert len(U120|U1|U0)==len(U120)
        print('position',pos,'U120',len(U120),'Ue1',len(U1),'Ue0_support',len(U0),
              'e1_subset_weight120',True,'e0_support_subset_weight120',True,
              'support_only_second_residue_rank_bound',len(U120),flush=True)

    print('PASS V26_Q138_PREDECESSOR_LEAF_BC_SECOND_RESIDUE_SUPPORT_FREQUENCY_NESTING')
    print('B_support_only_second_residue_integer_lift_rank<=668')
    print('C_support_only_second_residue_integer_lift_rank<=788')
    print('scope=support-indicator part only; e0 sign-negative and half-sector second-bit corrections remain')

if __name__=='__main__':main()
