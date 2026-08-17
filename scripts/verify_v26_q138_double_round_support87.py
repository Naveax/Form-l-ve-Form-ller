#!/usr/bin/env python3
import itertools, math

N=32
TREE=[[[[13,12],[14,[16,15]]],[[3,[4,5]],[2,[0,1]]]],[[[[17,18],[21,[20,19]]],[[26,25],[24,[23,22]]]],[[[27,28],[6,[8,7]]],[[9,[10,11]],[29,[30,31]]]]]]
S1=frozenset({0,1,2,3,4,5,12,13,14,15,16})
S2=frozenset({6,7,8,9,10,11,27,28,29,30,31})


def step(s,u,v,w):
    """Exact local modular-addition support recurrence at one bit."""
    if s==0 and not (u==v==w):
        return None
    return s^u^v^w


def s1_support_bound():
    # q138 central j4 has fixed output mask 2^3. MSB conservation gives
    # msb(u4)=msb(v4)=3. Since j3 output satisfies w3_i=v4_{i+8},
    # msb(w3)=msb(u3)=msb(v3)=27.
    # Hence for j2, z2w=u4 xor ROR12(v3) has z2w_15=1 and
    # z2w_16..19=0, while z2v_16=D_0 because v4_24=0.
    allowed=[]
    for C15,C16,D0 in itertools.product((0,1),repeat=3):
        ok=False
        # The sigma entering bit16 is allowed to be either value. z2v_15 is
        # existential because D31 is outside S1.
        for s16 in (0,1):
            s15=step(s16,C16,D0,0)
            if s15 is None:
                continue
            for z2v15 in (0,1):
                if step(s15,C15,z2v15,1) is not None:
                    ok=True
                    break
            if ok:
                break
        if ok:
            allowed.append((C15,C16,D0))
    expected={(0,0,0),(0,1,1),(1,0,0),(1,0,1),(1,1,0),(1,1,1)}
    assert set(allowed)==expected
    # Equivalently C15=0 => C16=D0. Six of the eight triples survive.
    rows=6*(2**(44-3))
    assert rows==3*(2**42)
    return rows


def s2_top_compatible(A,D):
    # A,D encode bits27..31, with bit0 corresponding to physical bit27.
    # msb(u3)=27. Therefore j1 output w1=u3 xor D obeys
    # w31..w28=D31..D28 and w27=1 xor D27.
    w=(D & 0b11110) | ((1^(D&1))<<0)
    if w:
        h=w.bit_length()-1
        # Addition MSB conservation: A must have the same highest set top bit.
        return ((A>>h)&1)==1 and (A>>(h+1))==0
    # If no bit27..31 of w is set, A cannot have a bit27..31 set either.
    return A==0


def s2_support_bound():
    pairs=[(A,D) for A in range(32) for D in range(32) if s2_top_compatible(A,D)]
    assert len(pairs)==342
    # The other 34 physical boundary bits are unrestricted for this safe count.
    return 342*(2**34)


def central_edges():
    E=[]
    for i in range(N-1):
        E.append((i,i+1,4))
    for r in (8,12,16):
        seen=set()
        for i in range(N):
            j=(i+r)%N
            e=tuple(sorted((i,j)))
            if e in seen:
                continue
            seen.add(e)
            E.append((e[0],e[1],1))
    return E

E=central_edges()


def graph_boundary(S):
    S=set(S)
    return sum(w for u,v,w in E if (u in S)!=(v in S))


def generic_dim(S):
    m=min(len(S),N-len(S))
    central=min(graph_boundary(S),4*m)
    leaves=4*m
    return 2**(central+leaves)


def tree_nodes():
    out=[]
    def walk(t,root=False):
        if isinstance(t,int):
            return {t}
        A=walk(t[0]);B=walk(t[1]);S=A|B
        if not root:
            out.append(frozenset(S))
        return S
    root=walk(TREE,True)
    assert root==set(range(N))
    out.extend(frozenset({i}) for i in range(N))
    return out


def main():
    c1=s1_support_bound()
    c2=s2_support_bound()
    comp1=frozenset(set(range(N))-set(S1))
    comp2=frozenset(set(range(N))-set(S2))
    def improved_dim(S):
        F=frozenset(S)
        if F in (S1,comp1):
            return c1*(2**44)
        if F in (S2,comp2):
            return c2*(2**44)
        return generic_dim(F)
    nodes=tree_nodes()
    assert max(generic_dim(S) for S in nodes)==2**88
    mx=max(improved_dim(S) for S in nodes)
    assert mx==3*(2**86)
    assert c2*(2**44)<mx
    print('PASS V26_Q138_DOUBLE_ROUND_SUPPORT87')
    print('S1_rule=C15=0=>C16=D0; allowed_local_triples=6/8; central_rows<=3*2^42')
    print('S2_allowed_A_D_top_pairs=342/1024; central_rows<=342*2^34')
    print('max_message_dimension=3*2^86')
    print('W2_repr<=86+log2(3)=%.15f' % math.log2(mx))
    print('scope=exact representation existence; constructive factor-generation ledger remains <=95')

if __name__=='__main__':
    main()
