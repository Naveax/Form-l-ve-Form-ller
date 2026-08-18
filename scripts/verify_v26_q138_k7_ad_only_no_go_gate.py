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


def poly(a,b,c,d):
    return (207*a*b*c +972*a*b*d +178176*a*b +812*a*c*d +79872*a*c
            +245760*a*d +2652831744*a +219*b*c*d +12288*b*c
            +178176*b*d +1029758976*b +79872*c*d +845733888*c
            +2699624448*d +1703063715840)


def main():
    # Polynomial identity on a deterministic finite interpolation grid.
    for a in (0,1,17,2048):
        for b in (0,2,31,2048):
            for c in (0,3,29,2048):
                for d in (0,5,23,2048):
                    assert k7(a,b,c,d)==poly(a,b,c,d)

    z=k7(0,2048,2048,0)
    assert z==5_595_612_708_864 and z-TAIL==74_964_899_840

    # Necessary A and D thresholds even with all other index-2 ranks zero.
    a0=k7(1439,0,0,0);a1=k7(1440,0,0,0)
    assert a0==5_520_488_595_456 and TAIL-a0==159_213_568
    assert a1==5_523_141_427_200 and a1-TAIL==2_493_618_176
    d0=k7(0,0,0,1414);d1=k7(0,0,0,1415)
    assert d0==5_520_332_685_312 and TAIL-d0==315_123_712
    assert d1==5_523_032_309_760 and d1-TAIL==2_384_500_736

    x0=k7(0,2009,2009,0);x1=k7(0,2010,2010,0)
    assert x0==5_520_524_242_944 and TAIL-x0==123_566_080
    assert x1==5_522_449_121_280 and x1-TAIL==1_801_312_256

    c0=k7(362,1055,1055,171);c1=k7(362,1056,1056,171)
    assert c0==5_519_255_787_951 and TAIL-c0==1_392_021_073
    assert c1==5_521_642_434_048 and c1-TAIL==994_625_024

    print('PASS V26_Q138_K7_AD_ONLY_NO_GO_GATE')
    print('ideal_A_D_zero_B_C_generic_k7=',z,'excess=',z-TAIL)
    print('necessary_A_index2_max=1439')
    print('necessary_D_index2_max=1414')
    print('ideal_A_D_zero_equal_B_C_threshold=2009')
    print('A_D_correction_only_equal_B_C_threshold=1055')
    print('scope=exact k7 search gate only; complete k>=7 tail remains unresolved')

if __name__=='__main__':main()
