#!/usr/bin/env python3
import itertools, math
from fractions import Fraction
from collections import Counter

N=32
TREE=[[[[13,12],[14,[16,15]]],[[3,[4,5]],[2,[0,1]]]],[[[[17,18],[21,[20,19]]],[[26,25],[24,[23,22]]]],[[[27,28],[6,[8,7]]],[[9,[10,11]],[29,[30,31]]]]]]
S1=frozenset({0,1,2,3,4,5,12,13,14,15,16})
S2=frozenset({6,7,8,9,10,11,27,28,29,30,31})


def T(s,t,u,v,w):
    if t!=(s^u^v^w): return Fraction(0)
    if s==0 and not(u==v==w): return Fraction(0)
    return Fraction(-1 if ((u^w)&(v^w)) else 1,2**s)


def T0(s,u,v,w):
    if s==0 and not(u==v==w): return Fraction(0)
    return Fraction(-1 if ((u^w)&(v^w)) else 1,2**s)


def basis(rows):
    B={}
    for r0 in rows:
        r={j:Fraction(v) for j,v in r0.items() if v}
        while r:
            c=min(r);a=r[c]
            if c not in B:
                q=1/a;B[c]={j:x*q for j,x in r.items()};break
            q=a;b=B[c]
            for j,x in b.items():
                z=r.get(j,Fraction(0))-q*x
                if z:r[j]=z
                elif j in r:r.pop(j)
    return list(B.values())


def block1_rank():
    # Row bits A0,B0,C15,C16,D0. Every central occurrence of these five
    # physical row variables is included: j1 bit0 and j2 bits15,16.
    rows=[]
    for A0,B0,C15,C16,D0 in itertools.product((0,1),repeat=5):
        r={}
        for s216,v215,s214,s10,u30,v312 in itertools.product((0,1),repeat=6):
            x=Fraction(0)
            for s215 in (0,1):
                x+=T(s216,s215,C16,D0,0)*T(s215,s214,C15,v215,1)
            if not x:continue
            y=T0(s10,A0,v312^B0,u30^D0)
            if not y:continue
            k=0
            for b in (s216,v215,s214,s10,u30,v312):k=(k<<1)|b
            r[k]=x*y
        rows.append(r)
    return len(basis(rows))


def j1_segment_basis(D):
    # j1 bits13..16. Row bits A13..16,B13..16; D13..16 fixed by sector.
    bits=[13,14,15,16];rows=[]
    for z in itertools.product((0,1),repeat=8):
        A=dict(zip(bits,z[:4]));Bv=dict(zip(bits,z[4:]));r={}
        for s16 in (0,1):
          for uvals in itertools.product((0,1),repeat=4):
           u3=dict(zip(bits,uvals))
           for x13,x14 in itertools.product((0,1),repeat=2):
            vx={13:x13,14:x14};s=s16;c=Fraction(1);ok=True
            for i in (16,15,14,13):
                base=0 if i==16 else 1 if i==15 else vx[i]
                v=base^Bv[i];w=u3[i]^D[i]
                t=s^A[i]^v^w;q=T(s,t,A[i],v,w)
                if not q:ok=False;break
                c*=q;s=t
            if ok:
                k=0
                for b in (s16,)+uvals+(x13,x14)+(s,):k=(k<<1)|b
                r[k]=r.get(k,Fraction(0))+c
        rows.append(r)
    B=basis(rows);assert len(B)==112
    return B,256


def j2_high_vector(D):
    # j2 bits29..31 close the second occurrences of D13..15.
    r={}
    for Cs in itertools.product((0,1),repeat=3):
      for ws in itertools.product((0,1),repeat=3):
        C=dict(zip((29,30,31),Cs));wv=dict(zip((29,30,31),ws));s=0;c=Fraction(1);ok=True
        for i in (31,30,29):
            v=D[i-16];t=s^C[i]^v^wv[i];q=T(s,t,C[i],v,wv[i])
            if not q:ok=False;break
            c*=q;s=t
        if ok:
            k=0
            for b in Cs+ws+(s,):k=(k<<1)|b
            r[k]=r.get(k,Fraction(0))+c
    return r,128


def j2_bit0_basis(D16):
    # j2 bit0 closes the second occurrence of D16 and includes row bit C0.
    rows=[]
    for C0 in (0,1):
        r={}
        for s0,u40,v312 in itertools.product((0,1),repeat=3):
            q=T0(s0,C0,D16,u40^v312)
            if q:r[(s0<<2)|(u40<<1)|v312]=q
        rows.append(r)
    B=basis(rows);assert len(B)==2
    return B,8


def kron3(a,b,c,db,dc):
    out={}
    for ia,va in a.items():
      for ib,vb in b.items():
       q=(ia*db+ib)*dc
       for ic,vc in c.items():out[q+ic]=va*vb*vc
    return out


def block2_rank():
    # Row bits A13..16,B13..16,D13..16,C0 = 13 physical S1 bits.
    # D13..15 second occurrences are included at j2 bits29..31; D16 at j2 bit0.
    vec=[]
    for ds in itertools.product((0,1),repeat=4):
        D=dict(zip((13,14,15,16),ds))
        B1,d1=j1_segment_basis(D);H,d2=j2_high_vector(D);B0,d3=j2_bit0_basis(D[16])
        for a in B1:
            for c in B0:vec.append(kron3(a,H,c,d2,d3))
    assert len(vec)==3584
    return len(basis(vec))


def s2_sector_rank(D):
    # j1 bits31..27. A/B are the ten row bits; D top five is kept as an
    # explicit sector because those D bits also occur in j2 elsewhere.
    rows=[]
    for A in range(32):
      for B in range(32):
        r={}
        for vlow in range(32):
          for s26want in (0,1):
            s=0;c=Fraction(1);ok=True
            for i in (31,30,29,28,27):
                u=(A>>(i-27))&1
                v=((vlow>>(i-27))&1)^((B>>(i-27))&1)
                di=(D>>(i-27))&1
                w=(1^di) if i==27 else di
                t=s^u^v^w;q=T(s,t,u,v,w)
                if not q:ok=False;break
                c*=q;s=t
            if ok and s==s26want:r[(vlow<<1)|s26want]=c
        rows.append(r)
    return len(basis(rows))


def graph_edges():
    E=[]
    for i in range(31):E.append((i,i+1,4))
    for d in (8,12,16):
        seen=set()
        for i in range(32):
            j=(i+d)%32;e=tuple(sorted((i,j)))
            if e in seen:continue
            seen.add(e);E.append((e[0],e[1],1))
    return E
E=graph_edges()

def gb(S):
    S=set(S);return sum(w for u,v,w in E if (u in S)!=(v in S))

def generic_dim(S):
    m=min(len(S),32-len(S));return 2**(min(gb(S),4*m)+4*m)

def nodes():
    out=[]
    def walk(t,root=False):
        if isinstance(t,int):return {t}
        A=walk(t[0]);B=walk(t[1]);S=A|B
        if not root:out.append(frozenset(S))
        return S
    assert walk(TREE,True)==set(range(32))
    out.extend(frozenset({i}) for i in range(32));return out


def main():
    r1=block1_rank();assert r1==16,r1
    r2=block2_rank();assert r2==2784,r2
    center1=r1*r2*(2**26)
    assert center1==87*(2**35)

    rs=[s2_sector_rank(D) for D in range(32)]
    assert Counter(rs)==Counter({64:30,32:2}),Counter(rs)
    rtop=sum(rs);assert rtop==1984==31*64
    center2=rtop*(2**29);assert center2==31*(2**35)

    comp1=frozenset(set(range(32))-set(S1));comp2=frozenset(set(range(32))-set(S2))
    def dim(S):
        F=frozenset(S)
        if F in (S1,comp1):return center1*(2**44)
        if F in (S2,comp2):return center2*(2**44)
        return generic_dim(F)
    mx=max(dim(S) for S in nodes())
    assert mx==87*(2**79)
    assert max(generic_dim(S) for S in nodes())==2**88

    print('PASS V26_Q138_DOUBLE_ROUND_SIGNED85')
    print('S1_block1_rank=16 row_bits=5')
    print('S1_block2_rank=2784 row_bits=13')
    print('S1_central_rank<=87*2^35')
    print('S2_top_sector_ranks=32,32,30x64 sum=1984=31*2^6')
    print('S2_central_rank<=31*2^35')
    print('max_message_dimension=87*2^79')
    print('W2_repr<=79+log2(87)=%.15f' % math.log2(mx))
    print('scope=exact representation existence; constructive ledger remains <=95')

if __name__=='__main__':main()
