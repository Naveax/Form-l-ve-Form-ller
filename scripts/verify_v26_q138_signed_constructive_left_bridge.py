#!/usr/bin/env python3
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S


def main():
    r1=S.block1_rank();r2=S.block2_rank();assert (r1,r2)==(16,2784)
    center1=r1*r2*(2**26);assert center1==87*(2**35)
    # Any exact rank factorization of the two explicit local block matrices can
    # be stored with these dense-factor envelopes. The signed85 verifier gives
    # block1 shape 32x64 and block2 shape 8192x2^18.
    u1=32*r1;v1=r1*64
    u2=(2**13)*r2;v2=r2*(2**18)
    assert max(u1,v1,u2,v2)<2**30
    # The complete S1 left factor has 44 physical row bits and center1 rank channels.
    left1=(2**44)*center1
    assert left1==87*(2**79)
    # S2 top rank is 1984=31*64; remaining29 raw bits.
    rs=[S.s2_sector_rank(D) for D in range(32)];rtop=sum(rs);assert rtop==1984
    center2=rtop*(2**29);assert center2==31*(2**35)
    left2=(2**44)*center2;assert left2==31*(2**79)
    print('PASS V26_Q138_SIGNED_CONSTRUCTIVE_LEFT_BRIDGE')
    print('S1_local_factor_max_log2=%.15f' % math.log2(max(u1,v1,u2,v2)))
    print('S1_dense_left_factor=87*2^79 log2=%.15f' % math.log2(left1))
    print('S2_dense_left_factor=31*2^79 log2=%.15f' % math.log2(left2))
    print('all_left_generation/storage_envelopes<94')
    print('scope=constructive left/row-side bridge only; full constructive94 requires a right/complement factor contraction certificate')

if __name__=='__main__':main()
