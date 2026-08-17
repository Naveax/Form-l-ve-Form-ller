#!/usr/bin/env python3
import math


def conv(a,b,K):
    out=[0]*(K+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<=K:out[i+j]+=x*y
    return out


def main():
    K=5
    # Recursive per-leaf layer envelopes. Unknown residual layers use only the
    # universal 2^11 row-rank cap2048.
    seqs=[
        [3,309]+[2048]*(K-1),
        [1052]+[2048]*K,
        [1160]+[2048]*K,
        [3,310]+[2048]*(K-1),
    ]
    co=[1]+[0]*K
    for s in seqs:co=conv(co,s,K)
    expected=[
        10982880,
        2306905824,
        140380802112,
        2067939590144,
        13446096486400,
        49193897820160,
    ]
    assert co==expected,co

    prefix=sum(co[:5])
    assert prefix==15656734767360
    generic=2**44
    assert generic==17592186044416
    assert prefix<generic
    headroom=generic-prefix
    assert headroom==1935451277056
    assert abs(math.log2(generic/prefix)-0.16815139841502408)<1e-12
    assert co[5]>generic
    assert co[5]>headroom
    assert abs(co[5]/headroom-25.417275238769356)<1e-12

    center=3829*(2**29)
    star_prefix=center*prefix
    assert star_prefix==32185216518011095382753280
    W=math.log2(star_prefix)
    assert abs(W-84.73460054643513)<1e-12
    current=73+math.log2(3829)
    assert abs((current-W)-0.16815139841503424)<1e-12

    print('PASS V26_Q138_DYADIC_FIVE_LAYER_PREFIX_GATE')
    print('layer_rank_bounds_k0_to_k5='+','.join(map(str,co)))
    print('prefix_k0_to_k4=%d'%prefix)
    print('generic_four_leaf_budget_2^44=%d'%generic)
    print('remaining_tail_budget=%d'%headroom)
    print('remaining_headroom_bits=%.15f'%math.log2(generic/prefix))
    print('generic_layer5_over_tail_budget=%.15f'%(co[5]/headroom))
    print('complete_S1_prefix_channels=%d'%star_prefix)
    print('complete_S1_prefix_exponent=%.15f'%W)
    print('tail_requirement=sum_rank_k>=5 < %d'%headroom)
    print('scope=prefix gate only; unresolved dyadic tail prevents any full representation/work reduction claim')


if __name__=='__main__':main()
