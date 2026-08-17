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
    seqs=[
        [3,219]+[2048]*(K-1),
        [1052]+[2048]*K,
        [1160]+[2048]*K,
        [3,207]+[2048]*(K-1),
    ]
    co=[1]+[0]*K
    for s in seqs:co=conv(co,s,K)
    expected=[10982880,1600340544,76184143968,1351960461312,10725441372160,42810709344256]
    assert co==expected,co

    prefix=sum(co[:5]);assert prefix==12155197300864
    generic=2**44;assert generic==17592186044416
    head=generic-prefix;assert head==5436988743552
    assert prefix<generic and co[5]>head
    assert abs(math.log2(prefix)-43.46663854464549)<1e-12
    assert abs(math.log2(generic/prefix)-0.5333614553545056)<1e-12
    assert abs(co[5]/head-7.87397424631923)<1e-12

    center=3829*(2**29);assert center==2055678722048
    star=center*prefix
    assert star==24987180453681406486249472
    W=math.log2(star);assert abs(W-84.36939048949566)<1e-12
    current=73+math.log2(3829)
    assert abs(current-W-0.533361455354509)<1e-12

    # Revised idealized depth sanity: zero first unresolved A2,D2,B1,C1.
    ideal=[
        [3,219,0,2048,2048,2048],
        [1052,0,2048,2048,2048,2048],
        [1160,0,2048,2048,2048,2048],
        [3,207,0,2048,2048,2048],
    ]
    z=[1]+[0]*K
    for s in ideal:z=conv(z,s,K)
    assert z[5]==1351960461312
    assert z[5]<head

    print('PASS V26_Q138_DYADIC_ACTIVITY_SHARPENED_PREFIX_GATE')
    print('layer_rank_bounds_k0_to_k5='+','.join(map(str,co)))
    print('prefix_k0_to_k4=%d'%prefix)
    print('new_tail_budget=%d'%head)
    print('headroom_bits=%.15f'%math.log2(generic/prefix))
    print('generic_k5_over_tail_budget=%.15f'%(co[5]/head))
    print('complete_S1_prefix_channels=%d'%star)
    print('complete_S1_prefix_exponent=%.15f'%W)
    print('ideal_zero_first_unresolved_quartet_k5=%d'%z[5])
    print('scope=updated prefix/tail search gate only; no complete representation/factor-generation/work bound lowered')

if __name__=='__main__':main()
