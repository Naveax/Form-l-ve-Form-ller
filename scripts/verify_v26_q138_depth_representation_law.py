#!/usr/bin/env python3

N=32
BASE_TREE=[[[[13,12],[14,[16,15]]],[[3,[4,5]],[2,[0,1]]]],[[[[17,18],[21,[20,19]]],[[26,25],[24,[23,22]]]],[[[27,28],[6,[8,7]]],[[9,[10,11]],[29,[30,31]]]]]]
# Label permutation found by finite tree search; the theorem uses only the explicit
# tree below, not any claim that the search was optimal.
PERM=[17,1,0,15,18,8,3,6,30,31,22,5,2,25,9,10,16,19,12,27,26,11,21,28,20,14,13,29,24,4,23,7]

def relabel(t):return PERM[t] if isinstance(t,int) else [relabel(t[0]),relabel(t[1])]
TREE=relabel(BASE_TREE)

def edges(offsets):
    E=[]
    for i in range(N-1):E.append((i,i+1,4))
    for r in offsets:
        seen=set()
        for i in range(N):
            j=(i+r)%N;e=tuple(sorted((i,j)))
            if e in seen:continue
            seen.add(e);E.append((e[0],e[1],1))
    return E
EC=edges((8,12,16))       # fixed-output/open-input and one-output/open-input reduced skeleton
EO=edges((7,8,12,16))     # fully open QR skeleton

def bd(S,E):
    S=set(S);return sum(w for u,v,w in E if (u in S)!=(v in S))

def walk(t,root=False):
    if isinstance(t,int):return {t},[]
    A,a=walk(t[0]);B,b=walk(t[1]);assert A.isdisjoint(B);S=A|B
    return S,a+b+([] if root else [S])

def caps(S):
    m=min(len(S),N-len(S))
    central=min(bd(S,EC),4*m)   # 4 open input-word bits/site, fixed output
    semi=min(bd(S,EC),5*m)      # 4 open inputs + one open output word/site
    full=min(bd(S,EO),8*m)      # 4 inputs + 4 outputs open
    earliest_vec=4*m            # fixed input, four output words: arbitrary 128-bit vector
    return m,central,semi,full,earliest_vec

def depth_cost(S,d):
    assert d>=2
    m,c,s,f,v=caps(S)
    # Layer count for d inverse double rounds after the fixed q138 output:
    # 1 final central + 4 semi-open + (8d-12) fully-open QRs + 4 earliest vectors.
    return c+4*s+(8*d-12)*f+4*v

def main():
    root,sets=walk(TREE,True);assert root==set(range(N))
    # Fully-open per-QR graph/rank envelope on this explicit common tree.
    fullmax=max(caps(S)[3] for S in sets);assert fullmax==67,fullmax
    # d=2 is the endpoint; thereafter every extra double round adds 8 full QRs,
    # each contributing at most 67 on this same tree.
    d2=max(depth_cost(S,2) for S in sets);assert d2==708,d2
    for d in range(2,9):
        mx=max(depth_cost(S,d) for S in sets)
        assert mx<=536*d-364,(d,mx,536*d-364)
        print('d',d,'verified_max',mx,'linear_bound',536*d-364)
    # d=1 uses the sharper special five-QR HT88 theorem, not the d>=2 layer formula.
    print('PASS V26_Q138_DEPTH_REPRESENTATION_LAW')
    print('d=1 exact_structural_bound=88')
    print('d>=2 exact_common_tree_bound=W_repr(d)<=536*d-364')
    print('d2_bound=708 fully_open_per_QR_common_tree_bound=67')
    print('tree='+repr(TREE))
    print('scope=representation/message upper bound for fixed outer input masks; no arithmetic-work or optimality claim')
if __name__=='__main__':main()
