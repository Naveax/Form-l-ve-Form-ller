#!/usr/bin/env python3
import math


def main():
    # First dyadic layer ranks.
    a0,b0,c0,d0=3,1052,1160,3
    p0=a0*b0*c0*d0
    assert p0==10982880

    # Second per-leaf residue ranks. B/C use only the universal 11|21 row cap.
    a1,b1,c1,d1=309,2048,2048,310
    terms={
        'A':a1*b0*c0*d0,
        'B':a0*b1*c0*d0,
        'C':a0*b0*c1*d0,
        'D':a0*b0*c0*d1,
    }
    assert terms=={
        'A':1131236640,
        'B':21381120,
        'C':19390464,
        'D':1134897600,
    }
    p1=sum(terms.values())
    assert p1==2306905824
    assert abs(math.log2(p1)-31.10331196332947)<1e-12

    cumulative=p0+p1
    assert cumulative==2317888704
    assert abs(math.log2(cumulative)-31.110164149389277)<1e-12
    headroom=(2**44)/cumulative
    assert abs(math.log2(headroom)-12.889835850610723)<1e-12

    center=3829*(2**29)
    assert center==2055678722048
    star0=center*p0
    star1=center*p1
    starcum=center*cumulative
    assert star0==22577272722806538240
    assert star1==4742257216165408407552
    assert starcum==4764834488888214945792
    assert abs(math.log2(star0)-64.2915050255997)<1e-12
    assert abs(math.log2(star1)-72.00606390817963)<1e-12
    assert abs(math.log2(starcum)-72.01291609423944)<1e-12

    print('PASS V26_Q138_FOUR_LEAF_TWO_DYADIC_LAYERS')
    print('first_leaf_layer_rank<=10982880')
    print('second_leaf_layer_rank<=2306905824')
    print('second_layer_terms='+repr(terms))
    print('first_two_leaf_layers_cumulative<=2317888704')
    print('first_two_leaf_layers_exponent=%.15f'%math.log2(cumulative))
    print('generic_2^44_headroom_bits=%.15f'%math.log2(headroom))
    print('complete_S1_first_two_layers_channels<=%d'%starcum)
    print('complete_S1_first_two_layers_exponent=%.15f'%math.log2(starcum))
    print('scope=first two exact dyadic layers only; 4*Q2 residual remains; no full representation/work bound lowered')


if __name__=='__main__':main()
