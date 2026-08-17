#!/usr/bin/env python3
import itertools
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as F
import probe_v26_q138_predecessor_leaf_bc_weight120_fourier_saturation as P


def main():
    sites,sig=P.quotient_data()
    assert len(sites)==124
    total=0;full_patterns=[]
    for zs in itertools.combinations(sites,4):
        total+=1
        if P.qrank4(zs,sig)==4:full_patterns.append(zs)
    assert total==9381251,total
    assert len(full_patterns)==29041,len(full_patterns)

    expected={'B':(29021,668),'C':(28549,788)}
    for pos in 'BC':
        union=set();consistent=0
        for zs in full_patterns:
            can=A.canonical_support(pos,D.carries(zs),expect_internal=128)
            if can is None:continue
            consistent+=1
            B=F.rowspace_basis(can,F.S)
            union |= F.enumerate_space(B)
        ec,eu=expected[pos]
        assert consistent==ec,(pos,consistent,ec)
        assert len(union)==eu,(pos,len(union),eu)
        assert eu<2048
        print('position',pos,'four_zero_patterns',total,'internal_rank128',len(full_patterns),
              'affine_consistent',consistent,'left_walsh_frequency_union',len(union),
              'weight120_integer_lift_rank_bound',len(union),flush=True)

    print('PASS V26_Q138_PREDECESSOR_LEAF_BC_SECOND_RESIDUE_WEIGHT120_RANK668_788')
    print('B_weight120_second_residue_component_rank_Q_lift<=668')
    print('C_weight120_second_residue_component_rank_Q_lift<=788')
    print('scope=weight120 component only; weight121..124 correction terms remain; no complete second-residue/full-leaf/work claim')


if __name__=='__main__':main()
