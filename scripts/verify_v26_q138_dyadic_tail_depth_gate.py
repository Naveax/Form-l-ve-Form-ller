#!/usr/bin/env python3

TAIL=1935451277056
K=5


def conv(a,b):
    out=[0]*(K+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<=K:out[i+j]+=x*y
    return out


def layer5(seqs):
    c=[1]+[0]*K
    for s in seqs:c=conv(c,s)
    return c[5]


def main():
    generic={
        'A':[3,309,2048,2048,2048,2048],
        'B':[1052,2048,2048,2048,2048,2048],
        'C':[1160,2048,2048,2048,2048,2048],
        'D':[3,310,2048,2048,2048,2048],
    }

    s1={k:v[:] for k,v in generic.items()}
    for k,j in [('A',2),('D',2),('B',1),('C',1)]:s1[k][j]=0
    r1=layer5([s1[x] for x in 'ABCD'])
    assert r1==2067939590144
    assert r1-TAIL==132488313088

    s2={k:v[:] for k,v in s1.items()}
    for k,j in [('A',3),('D',3),('B',2),('C',2)]:s2[k][j]=0
    r2=layer5([s2[x] for x in 'ABCD'])
    assert r2==2004408467456
    assert r2-TAIL==68957190400

    assert r1>TAIL and r2>TAIL

    print('PASS V26_Q138_DYADIC_TAIL_DEPTH_GATE')
    print('tail_budget=%d'%TAIL)
    print('zero_first_unresolved_quartet_layer5=%d excess=%d'%(r1,r1-TAIL))
    print('zero_first_two_unresolved_quartets_layer5=%d excess=%d'%(r2,r2-TAIL))
    print('consequence=successful current-method tail proof needs deeper residue, sharper early bound, or cross-product cancellation')
    print('scope=certificate-method depth gate; not a true-rank or unrestricted-work lower bound')

if __name__=='__main__':main()
