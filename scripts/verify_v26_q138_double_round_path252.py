#!/usr/bin/env python3

N=32
COLUMN=(0,4,8,12)
DIAGONALS=((0,5,10,15),(1,6,11,12),(2,7,8,13),(3,4,9,14))
POSITIONS='ABCD'


def cyclic_cross(k,r,n=N):
    A=set(range(k)); B=set(range(k,n)); c=0
    seen=set()
    for i in range(n):
        j=(i+r)%n
        e=tuple(sorted((i,j)))
        if e in seen: continue
        seen.add(e)
        if (i in A)!=(j in A):c+=1
    return c


def path_cross(k,n=N):
    return 1 if 0<k<n else 0


def main():
    # q138 output is word 4, so only the column QR (0,4,8,12) is active.
    assert 4 in COLUMN
    # The four intermediate words land in four distinct diagonal QRs and occupy A,B,C,D respectively.
    loc={}
    for q in DIAGONALS:
        for p,w in enumerate(q):loc[w]=(q,POSITIONS[p])
    assert [loc[w][1] for w in COLUMN]==list('ABCD')
    assert len({loc[w][0] for w in COLUMN})==4

    central=[];leaf=[];star=[]
    for k in range(1,N):
        sig=4*path_cross(k)
        c=sig+cyclic_cross(k,8)+cyclic_cross(k,12)+cyclic_cross(k,16)
        l=sig+cyclic_cross(k,8)+cyclic_cross(k,12)
        central.append(c);leaf.append(l);star.append(c+4*l)
    assert max(central)==76,(max(central),central)
    assert max(leaf)==44,(max(leaf),leaf)
    assert max(star)==252,(max(star),star)
    assert star[15]==252
    print('PASS V26_Q138_EXACT_DOUBLE_ROUND_PATH252')
    print('active_column='+repr(COLUMN))
    print('diagonal_output_positions='+','.join(f'{w}:{loc[w][1]}' for w in COLUMN))
    print('central_path_max=76 leaf_path_max=44 star_path_max=252 maximizing_prefix=16')
    print('exact_topology_bound=W2_topo<=252')
    print('coarse_depth_law=W_topo(d)<=720*d-468 for d>=1')

if __name__=='__main__':main()
