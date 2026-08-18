#!/usr/bin/env python3
import itertools

TAIL=5_520_647_809_024


def k7(a2,b2,c2,d2):
    seqs=[
        [3,219,a2]+[2048]*5,
        [36,812,b2]+[2048]*5,
        [84,972,c2]+[2048]*5,
        [3,207,d2]+[2048]*5,
    ]
    s=0
    for inds in itertools.product(range(8),repeat=4):
        if sum(inds)!=7:continue
        p=1
        for seq,i in zip(seqs,inds):p*=seq[i]
        s+=p
    return s


def main():
    z=k7(0,2048,2048,0)
    assert z==5_595_612_708_864 and z-TAIL==74_964_899_840
    a=k7(0,2009,2009,0);b=k7(0,2010,2010,0)
    assert a==5_520_524_242_944 and TAIL-a==123_566_080
    assert b==5_522_449_121_280 and b-TAIL==1_801_312_256
    c=k7(362,1055,1055,171);d=k7(362,1056,1056,171)
    assert c==5_519_255_787_951 and TAIL-c==1_392_021_073
    assert d==5_521_642_434_048 and d-TAIL==994_625_024
    print('PASS V26_Q138_K7_AD_ONLY_NO_GO_GATE')
    print('ideal_A_D_zero_B_C_generic_k7=',z,'excess=',z-TAIL)
    print('ideal_A_D_zero_equal_B_C_threshold=2009')
    print('A_D_correction_only_equal_B_C_threshold=1055')
    print('scope=exact k7 search gate only; complete k>=7 tail remains unresolved')

if __name__=='__main__':main()
