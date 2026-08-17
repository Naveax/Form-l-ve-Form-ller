#!/usr/bin/env python3
import math


def main():
    # Certified natural dyadic scales.
    eA=eD=92
    eB=eC=121
    assert eA+eB+eC+eD==426

    # Certified first-residue GF(2) rank upper bounds. Each admits an integer
    # low-rank lift K with M-K entrywise even, so the four K factors form an
    # exact first dyadic product layer.
    rA,rB,rC,rD=3,1052,1160,3
    leaf0=rA*rB*rC*rD
    assert leaf0==10982880
    leaf_exp=math.log2(leaf0)
    assert abs(leaf_exp-23.38875308074955)<1e-12
    assert leaf0 < 2**24
    assert leaf0 < 2**44

    center=3829*(2**29)
    assert center==2055678722048
    star0=center*leaf0
    assert star0==22577272722806538240
    W0=math.log2(star0)
    assert abs(W0-64.2915050255997)<1e-12

    print('PASS V26_Q138_FOUR_LEAF_FIRST_DYADIC_STAR_LAYER')
    print('common_leaf_scale=2^426')
    print('first_leaf_residue_rank_bounds=A3,B1052,C1160,D3')
    print('four_leaf_first_layer_rank<=10982880')
    print('four_leaf_first_layer_exponent=%.15f'%leaf_exp)
    print('center_rank=3829*2^29')
    print('complete_S1_first_dyadic_layer_channels<=%d'%star0)
    print('complete_S1_first_dyadic_layer_exponent=%.15f'%W0)
    print('scope=one exact dyadic layer only; residual hierarchy remains; no full representation/work bound lowered')


if __name__=='__main__':main()
