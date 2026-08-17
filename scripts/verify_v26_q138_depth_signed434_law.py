#!/usr/bin/env python3
import itertools, math
from fractions import Fraction
from collections import Counter

N=32
TREE=[[[[27,13],[29,[21,4]]],[[28,[12,5]],[11,[20,19]]]],[[[[25,0],[2,[26,1]]],[[9,18],[17,[10,3]]]],[[[22,8],[24,[23,16]]],[[30,[31,6]],[14,[15,7]]]]]]
S3=frozenset({4,5,11,12,13,19,20,21,27,28,29})


def T(s,t,u,v,w):
    if t!=(s^u^v^w):return Fraction(0)
    if s==0 and not(u==v==w):return Fraction(0)
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


def j1_basis(D):
    # j1 bits29..27. Row bits A27..29,B27..29; D27..29 fixed sector.
    rows=[]
    for z in itertools.product((0,1),repeat=6):
        A=dict(zip((27,28,29),z[:3]));Bv=dict(zip((27,28,29),z[3:]));r={}
        for s29 in (0,1):
          for xv in itertools.product((0,1),repeat=3):
            x=dict(zip((27,28,29),xv));s=s29;c=Fraction(1);ok=True
            for i in (29,28,27):
                u=A[i]
                v=x[i]^Bv[i]
                w=(1 if i==27 else 0)^D[i]
                t=s^u^v^w;q=T(s,t,u,v,w)
                if not q:ok=False;break
                c*=q;s=t
            if ok:
                k=0
                for b in (s29,)+xv+(s,):k=(k<<1)|b
                r[k]=c
        rows.append(r)
    return basis(rows)


def j2_basis(D):
    # j2 bits13..11. Row bits C11..13; D27..29 are the same sector variables.
    rows=[]
    for Cv in itertools.product((0,1),repeat=3):
        C=dict(zip((11,12,13),Cv));r={}
        for s13 in (0,1):
          for wv0 in itertools.product((0,1),repeat=3):
            wv=dict(zip((11,12,13),wv0));s=s13;c=Fraction(1);ok=True
            for i in (13,12,11):
                u=C[i];v=D[i+16];w=wv[i]
                t=s^u^v^w;q=T(s,t,u,v,w)
                if not q:ok=False;break
                c*=q;s=t
            if ok:
                k=0
                for b in (s13,)+wv0+(s,):k=(k<<1)|b
                r[k]=c
        rows.append(r)
    return basis(rows)


def signed_block_rank():
    vec=[];sector=Counter()
    for dv in itertools.product((0,1),repeat=3):
        D=dict(zip((27,28,29),dv));B1=j1_basis(D);B2=j2_basis(D)
        sector[(len(B1),len(B2))]+=1
        for a in B1:
          for b in B2:
            v={ia*32+ib:va*vb for ia,va in a.items() for ib,vb in b.items()}
            vec.append(v)
    B=basis(vec)
    assert sector==Counter({(30,8):6,(22,8):2}),sector
    assert len(vec)==1792
    assert len(B)==434,len(B)
    return 434


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
EC=edges((8,12,16));EO=edges((7,8,12,16))

def bd(S,E):
    S=set(S);return sum(w for u,v,w in E if (u in S)!=(v in S))

def walk(t,root=False):
    if isinstance(t,int):return {t},[]
    A,a=walk(t[0]);B,b=walk(t[1]);S=A|B
    return S,a+b+([] if root else [frozenset(S)])

def caps(S):
    m=min(len(S),N-len(S))
    return (m,min(bd(S,EC),4*m),min(bd(S,EC),5*m),min(bd(S,EO),8*m),4*m)

def central(S):
    m,c,s,f,v=caps(S);F=frozenset(S);C=frozenset(set(range(N))-set(F))
    if F==S3 or C==S3:
        return min(float(c),32+math.log2(434))
    return float(c)

def depth_cost(S,d):
    m,c,s,f,v=caps(S)
    return central(S)+4*s+(8*d-12)*f+4*v


def main():
    r=signed_block_rank();assert r==434
    root,sets=walk(TREE,True);assert root==set(range(N))
    generic={d:max(caps(S)[1]+4*caps(S)[2]+(8*d-12)*caps(S)[3]+4*caps(S)[4] for S in sets) for d in range(2,10)}
    assert generic=={d:520*d-340 for d in range(2,10)},generic
    vals={d:max(depth_cost(S,d) for S in sets) for d in range(2,10)}
    for d,v in vals.items():
        target=520*d-352+math.log2(434)
        assert abs(v-target)<1e-12,(d,v,target)
    print('PASS V26_Q138_DEPTH_SIGNED434_LAW')
    print('S3='+','.join(map(str,sorted(S3))))
    print('signed_block_row_bits=12 raw_states=4096 exact_rank=434')
    print('S3_central_rank<=434*2^32')
    print('d>=2 W_repr(d)<=520*d-352+log2(434)')
    print('verified='+','.join(f'{d}:{vals[d]:.12f}' for d in sorted(vals)))
    print('slope=520; intercept improved by %.12f bits' % (12-math.log2(434)))
    print('scope=exact representation/message bound; no arithmetic-work or optimality claim')

if __name__=='__main__':main()
