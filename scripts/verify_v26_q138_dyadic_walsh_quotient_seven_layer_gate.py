#!/usr/bin/env python3
import math


def conv(a,b,K):
    o=[0]*(K+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<=K:o[i+j]+=x*y
    return o


def product_layer7(a2,b2,c2,d2,deeper=2048):
    K=7
    A=[3,219,a2]+[deeper]*(K-2)
    B=[36,812,b2]+[deeper]*(K-2)
    C=[84,972,c2]+[deeper]*(K-2)
    D=[3,207,d2]+[deeper]*(K-2)
    cur=[1]+[0]*K
    for s in (A,B,C,D):cur=conv(cur,s,K)
    return cur


def main():
    cur=product_layer7(2048,2048,2048,2048)
    expected=[27216,4793472,315450720,9979784064,171359156304,
              1703063715840,10186815307776,38736654106624]
    assert cur==expected
    prefix=sum(cur[:7]);budget=1<<44;tail=budget-prefix
    assert prefix==12071538235392
    assert tail==5520647809024
    center=3829*(1<<29);channels=prefix*center
    assert channels==24815204292884195564322816
    exp=math.log2(channels);current=73+math.log2(3829)
    assert abs(exp-84.3594267039546)<1e-12
    assert abs((current-exp)-0.54332524089557)<1e-12
    assert cur[7]==38736654106624 and cur[7]>tail
    ideal=product_layer7(0,0,0,0)[7]
    assert ideal==1703063715840 and ideal<tail
    print('PASS V26_Q138_DYADIC_WALSH_QUOTIENT_SEVEN_LAYER_GATE')
    print('layers_k0_k7='+repr(cur))
    print('prefix_k0_k6=12071538235392')
    print('remaining_tail_budget=5520647809024')
    print('center_attached_prefix_channels=24815204292884195564322816')
    print('center_attached_prefix_exponent='+repr(exp))
    print('gap_to_current_complete_factor_bits='+repr(current-exp))
    print('generic_k7=38736654106624')
    print('generic_k7_over_tail='+repr(cur[7]/tail))
    print('all_four_index2_zero_k7=1703063715840 < tail')
    print('scope=exact prefix/search gate only; unresolved k>=7 tail prevents complete-factor or work admission')

if __name__=='__main__':main()
