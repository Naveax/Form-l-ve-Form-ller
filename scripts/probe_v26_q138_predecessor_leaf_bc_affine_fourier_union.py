#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_bc_input_activity_no_gain as N
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as F
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A

S=F.S;R=F.R


def main():
    for pos in 'BC':
        objs,total=N.residue_objects(pos)
        affine=objs[:-1];assert len(affine)==103
        UL=set();UR=set();distL={};distR={};dists={}
        for can in affine:
            BL=F.rowspace_basis(can,S);BR=F.rowspace_basis(can,R)
            distL[len(BL)]=distL.get(len(BL),0)+1
            distR[len(BR)]=distR.get(len(BR),0)+1
            d=A.cut_intersection(can);dists[d]=dists.get(d,0)+1
            UL |= F.enumerate_space(BL);UR |= F.enumerate_space(BR)
        print('position',pos,'affine_supports',len(affine),'intersection_distribution',dists,
              'left_constraint_rank_distribution',distL,
              'right_constraint_rank_distribution',distR,
              'left_fourier_frequency_union',len(UL),
              'right_fourier_frequency_union',len(UR),
              'left_global_frequency_span_rank',T.gf2_rank(list(UL),len(S)),
              'right_global_frequency_span_rank',T.gf2_rank(list(UR),len(R)),
              'old_affine_sum_bound',total-16)
    print('PASS PROBE V26_Q138_BC_AFFINE_FOURIER_UNION')
    print('scope=affine-support homogeneous Fourier union only; signed four-sector term excluded')

if __name__=='__main__':main()
