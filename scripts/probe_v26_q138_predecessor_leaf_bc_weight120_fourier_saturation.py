#!/usr/bin/env python3
import itertools,sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as F


def quotient_data():
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    F0=T.forms('B',(0,0,0,0,0));base=A.internal_null('B',D.carries([]))
    assert base[0]==124 and len(base[2])==4
    sig={z:B.quotient_signature(F0,base[2],*z) for z in sites}
    return sites,sig


def qrank4(zs,sig):
    rows=[]
    for z in zs:rows.extend(sig[z])
    return B.rank4(rows)


def main():
    sites,sig=quotient_data()
    for pos in 'BC':
        UL=set();tested=0;full=0;consistent=0
        first=[]
        for zs in itertools.combinations(sites,4):
            tested+=1
            if qrank4(zs,sig)!=4:continue
            full+=1
            can=A.canonical_support(pos,D.carries(zs),expect_internal=128)
            if can is None:continue
            consistent+=1
            BL=F.rowspace_basis(can,F.S)
            before=len(UL);UL |= F.enumerate_space(BL)
            if len(first)<20 and len(UL)>before:first.append((zs,len(BL),len(UL)))
            if len(UL)==2048:break
        print('position',pos,'tested_four_zero_patterns',tested,'rank128_patterns_seen',full,
              'affine_consistent_seen',consistent,'left_frequency_union',len(UL),
              'saturated',len(UL)==2048,'first_growth_events',repr(first),flush=True)
    print('PASS PROBE V26_Q138_BC_WEIGHT120_FOURIER_SATURATION')
    print('scope=deterministic early-stop probe of weight120 rank128 sectors only; no second-residue theorem')

if __name__=='__main__':main()
