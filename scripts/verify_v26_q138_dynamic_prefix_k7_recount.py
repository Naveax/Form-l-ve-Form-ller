#!/usr/bin/env python3
import itertools

BUDGET=1<<44


def layers(a2,b2,c2,d2):
    seqs=[
        [3,219,a2]+[2048]*6,
        [36,812,b2]+[2048]*6,
        [84,972,c2]+[2048]*6,
        [3,207,d2]+[2048]*6,
    ]
    out=[]
    for k in range(8):
        s=0
        for inds in itertools.product(range(k+1),repeat=4):
            if sum(inds)!=k:continue
            p=1
            for seq,i in zip(seqs,inds):p*=seq[i]
            s+=p
        out.append(s)
    return out


def poly(a,b,c,d):
    return (210*a*b*c +1056*a*b*d +399936*a*b
            +848*a*c*d +257952*a*c +1141248*a*d +3127931904*a
            +222*b*c*d +58908*b*c +412608*b*d +1168937856*b
            +268128*c*d +930192576*c +3188419584*d
            +2858783053824)


def s07(a,b,c,d):return sum(layers(a,b,c,d))


def main():
    for a in (0,1,17,2048):
        for b in (0,2,31,2048):
            for c in (0,3,29,2048):
                for d in (0,5,23,2048):
                    assert s07(a,b,c,d)==poly(a,b,c,d)

    generic=s07(2048,2048,2048,2048)
    assert generic==50_808_192_342_016 and generic>BUDGET

    v=layers(0,2048,2048,0)
    assert sum(v[:7])==1_809_267_529_728
    assert v[7]==5_595_612_708_864
    assert sum(v)==7_404_880_238_592
    assert BUDGET-sum(v)==10_187_305_805_824

    corr=s07(362,2048,2048,171)
    assert corr==10_598_653_759_488 and corr<BUDGET

    assert s07(1902,2048,2048,0)<=BUDGET
    assert s07(1903,2048,2048,0)>BUDGET
    assert s07(0,2048,2048,1847)<=BUDGET
    assert s07(0,2048,2048,1848)>BUDGET
    assert s07(706,2048,2048,706)<=BUDGET
    assert s07(707,2048,2048,707)>BUDGET
    assert s07(1068,1068,1068,1068)<=BUDGET
    assert s07(1069,1069,1069,1069)>BUDGET

    print('PASS V26_Q138_DYNAMIC_PREFIX_K7_RECOUNT')
    print('generic_sum_k0_k7=',generic,'excess=',generic-BUDGET)
    print('AD_zero_BC_generic_sum_k0_k7=',sum(v),'remaining=',BUDGET-sum(v))
    print('AD_correction_only_BC_generic_sum_k0_k7=',corr,'remaining=',BUDGET-corr)
    print('conditional_BC_generic_A_max_with_D0=1902')
    print('conditional_BC_generic_D_max_with_A0=1847')
    print('conditional_BC_generic_equal_AD_max=706')
    print('equal_all_index2_dynamic_prefix_max=1068')
    print('scope=dynamic partial sum k0..k7 only; complete k>=8 tail remains unresolved')

if __name__=='__main__':main()
# clean PR trigger
