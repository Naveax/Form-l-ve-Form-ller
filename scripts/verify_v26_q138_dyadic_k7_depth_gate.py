#!/usr/bin/env python3

TAIL=1480964449920


def conv(a,b,K):
    o=[0]*(K+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<=K:o[i+j]+=x*y
    return o


def layer7(zero_through):
    # zero_through=1: no unresolved residues are idealized away.
    # zero_through=2: index2 is zero; zero_through=3: indices2,3 are zero.
    base={'A':[3,219],'B':[36,1016],'C':[84,1220],'D':[3,207]}
    seq=[]
    for p in 'ABCD':
        s=base[p][:]
        for i in range(2,8):s.append(0 if i<=zero_through else 2048)
        seq.append(s)
    cur=[1]+[0]*7
    for s in seq:cur=conv(cur,s,7)
    return cur[7]


def main():
    generic=layer7(1)
    only_next_zero=layer7(2)
    next_two_zero=layer7(3)
    assert generic==48838228148224
    assert only_next_zero==2288332406784
    assert next_two_zero==1438633525248
    assert only_next_zero>TAIL
    assert next_two_zero<TAIL
    print('PASS V26_Q138_DYADIC_K7_DEPTH_GATE')
    print('tail_budget=1480964449920')
    print('generic_k7=48838228148224')
    print('even_if_all_four_index2_residues_zero_k7=2288332406784 > tail')
    print('if_all_four_index2_and_index3_residues_zero_k7=1438633525248 < tail')
    print('consequence=single-next-residue-only route is insufficient under generic deeper caps; must touch deeper residues, sharpen earlier envelopes, or use product-level cancellation')

if __name__=='__main__':main()
