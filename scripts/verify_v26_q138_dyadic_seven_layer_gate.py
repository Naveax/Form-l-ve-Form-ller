#!/usr/bin/env python3
import math


def conv(a,b,K):
    out=[0]*(K+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<=K:out[i+j]+=x*y
    return out


def main():
    K=7
    A=[3,219]+[2048]*K
    B=[36,1016]+[2048]*K
    C=[84,1220]+[2048]*K
    D=[3,207]+[2048]*K
    cur=[1]+[0]*K
    for s in (A,B,C,D):cur=conv(cur,s,K)
    expected=[27216,5028048,352812816,12065376240,221554487136,
              2288332406784,13588911456256,48838228148224]
    assert cur==expected,(cur,expected)
    prefix=sum(cur[:7]);budget=1<<44;tail=budget-prefix
    assert prefix==16111221594496
    assert tail==1480964449920 and prefix<budget
    center=3829*(1<<29)
    exp=math.log2(prefix*center)
    current=73+math.log2(3829)
    assert abs(exp-84.77588306544745)<1e-12
    assert abs((current-exp)-0.12686887940272)<1e-12
    assert cur[7]==48838228148224 and cur[7]>tail
    print('PASS V26_Q138_DYADIC_SEVEN_LAYER_GATE')
    print('layers_k0_k7='+repr(cur))
    print('prefix_k0_k6=16111221594496')
    print('generic_leaf_budget=17592186044416')
    print('remaining_tail_budget=1480964449920')
    print('center_attached_prefix_exponent='+repr(exp))
    print('gap_to_current_complete_factor_bits='+repr(current-exp))
    print('generic_k7=48838228148224')
    print('generic_k7_over_tail='+repr(cur[7]/tail))
    print('scope=exact prefix/search gate only; unresolved k>=7 tail prevents complete-factor or work admission')

if __name__=='__main__':main()
