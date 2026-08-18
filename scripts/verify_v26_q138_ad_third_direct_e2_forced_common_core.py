#!/usr/bin/env python3
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T

MASK=(1<<128)-1
RHSBIT=1<<128


def solve(rows):
    return T.rref([(r&MASK,(r>>128)&1) for r in rows],n=128)


def groups_for(pos):
    raw,_=P.direct_supports(pos)
    C=Counter(can for _t,_z,can in raw)
    odd=[can for can,n in C.items() if n&1]
    G=defaultdict(list)
    for can in odd:
        cond=P.canonical_condition(I.input_condition(can))
        G[cond].append(can)
    return list(G)


def stats(groups,node):
    ns=solve(node);assert ns is not None
    nr=ns[0];U=0;rd=Counter();mu=Fraction(0,1)
    for cond in groups:
        s=solve(tuple(node)+tuple(cond))
        if s is None:continue
        r=s[0]-nr;assert r>=0
        U+=1;rd[r]+=1;mu+=Fraction(1,1<<r)
    return U,rd,mu


def main():
    GA=groups_for('A');assert len(GA)==4531
    fA=Counter(r for c in GA for r in c);topA=[r for r,_ in fA.most_common(7)]
    assert [fA[r] for r in topA[:6]]==[4437,4437,4435,4343,4342,4250]
    A5=tuple(topA[:5]);A6=tuple(topA[:6])
    u5,r5,m5=stats(GA,A5);u6,r6,m6=stats(GA,A6)
    uf,rf,mf=stats(GA,A5+(topA[5]^RHSBIT,))
    assert (u5,r5,m5)==(4249,Counter({5:3787,4:455,3:7}),Fraction(4725,32))
    assert (u6,r6,m6)==(4067,Counter({4:3700,3:364,2:3}),Fraction(555,2))
    assert (uf,rf,mf)==(182,Counter({4:87,3:91,2:4}),Fraction(285,16))
    assert solve(A6+(topA[6],)) is None
    lowerA=(m6.numerator+m6.denominator-1)//m6.denominator
    assert lowerA==278
    assert max(len(GA)-fA[r] for r in topA[:5])==189 < lowerA
    assert uf < lowerA

    GD=groups_for('D');assert len(GD)==8629
    fD=Counter(r for c in GD for r in c);topD=[r for r,_ in fD.most_common(6)]
    assert [fD[r] for r in topD]==[8446,8444,8267,8265,8265,7392]
    D5=tuple(topD[:5]);D6=tuple(topD)
    d5,rd5,md5=stats(GD,D5);d6,rd6,md6=stats(GD,D6)
    df,rdf,mdf=stats(GD,D5+(topD[5]^RHSBIT,))
    assert (d5,rd5,md5)==(8084,Counter({6:3294,5:4129,4:649,3:12}),Fraction(3561,16))
    assert (d6,rd6,md6)==(7070,Counter({5:2911,4:3622,3:531,2:6}),Fraction(12327,32))
    assert (df,rdf,mdf)==(1014,Counter({5:383,4:507,3:118,2:6}),Fraction(1917,32))
    lowerD=(md6.numerator+md6.denominator-1)//md6.denominator
    assert lowerD==386
    assert max(len(GD)-fD[r] for r in topD[:5])==364 < lowerD
    assert df>lowerD

    print('PASS V26_Q138_AD_THIRD_DIRECT_E2_FORCED_COMMON_CORE')
    print('A_forced_common_core_rank=6 A_global_active_lower>=278 A_core_compatible=4067')
    print('D_forced_common_core_rank=5 D_global_active_lower>=386 D_core_compatible=8084')
    print('scope=direct-e2 active-condition geometry only; complete third residues remain open')

if __name__=='__main__':main()
