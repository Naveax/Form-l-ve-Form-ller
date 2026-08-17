#!/usr/bin/env python3
import math


def conv(a,b,K):
    out=[0]*(K+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<=K:out[i+j]+=x*y
    return out


def main():
    K=6
    seqs=[
        [3,219]+[2048]*(K-1),
        [36]+[2048]*K,
        [84]+[2048]*K,
        [3,207]+[2048]*(K-1),
    ]
    co=[1]+[0]*K
    for s in seqs:co=conv(co,s,K)
    expected=[27216,6076512,528287760,22588489728,499782844416,5718621093888,33271289282560]
    assert co==expected,co

    prefix=sum(co[:6]);assert prefix==6241526819520
    generic=2**44;assert generic==17592186044416
    tail=generic-prefix;assert tail==11350659224896
    assert co[6]>tail
    assert abs(math.log2(prefix)-42.50503612695195)<1e-12
    assert abs(math.log2(generic/prefix)-1.49496387304805)<1e-12
    assert abs(co[6]/tail-2.9312208765447143)<1e-12

    center=3829*(2**29);assert center==2055678722048
    star=center*prefix
    assert star==12830573875979191540776960
    W=math.log2(star);assert abs(W-83.4077880718021)<1e-12
    current=73+math.log2(3829)
    assert abs(current-W-1.4949638730480643)<1e-12

    print('PASS V26_Q138_DYADIC_FOURIER_SHARPENED_SIX_LAYER_GATE')
    print('layer_rank_bounds_k0_to_k6='+','.join(map(str,co)))
    print('prefix_k0_to_k5=%d'%prefix)
    print('new_tail_budget=%d'%tail)
    print('headroom_bits=%.15f'%math.log2(generic/prefix))
    print('generic_k6_over_tail_budget=%.15f'%(co[6]/tail))
    print('complete_S1_prefix_channels=%d'%star)
    print('complete_S1_prefix_exponent=%.15f'%W)
    print('scope=updated six-layer search gate only; unresolved k>=6 tail prevents full representation/factor-generation/work claim')

if __name__=='__main__':main()
