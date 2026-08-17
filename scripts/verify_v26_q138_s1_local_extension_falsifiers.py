#!/usr/bin/env python3
import itertools
from fractions import Fraction


def T(s,t,u,v,w):
    if t!=(s^u^v^w):return Fraction(0)
    if s==0 and not(u==v==w):return Fraction(0)
    return Fraction(-1 if ((u^w)&(v^w)) else 1,2**s)

def T0(s,u,v,w):
    if s==0 and not(u==v==w):return Fraction(0)
    return Fraction(-1 if ((u^w)&(v^w)) else 1,2**s)

def rank_sparse(rows):
    B={}
    for r0 in rows:
        r={j:Fraction(v) for j,v in r0.items() if v}
        while r:
            c=min(r);a=r[c]
            if c not in B:
                B[c]={j:x/a for j,x in r.items()};break
            b=B[c]
            for j,x in b.items():
                z=r.get(j,Fraction(0))-a*x
                if z:r[j]=z
                elif j in r:r.pop(j)
    return len(B)

def block1_c1314_rank():
    # Extend the clean rank16 block1 downward through j2 bits14,13.
    # Row bits: A0,B0,C13,C14,C15,C16,D0 (7 bits).
    # Retained columns keep all other local inputs independent, which is a safe
    # relaxation for a rank upper bound. Shared carry sigma2_14 is contracted.
    rows=[]
    for A0,B0,C13,C14,C15,C16,D0 in itertools.product((0,1),repeat=7):
        r={}
        for s216,v215,s212,s10,u30,v312,v214,w214,v213,w213 in itertools.product((0,1),repeat=10):
            z=Fraction(0)
            for s215,s214,s213 in itertools.product((0,1),repeat=3):
                a=T(s216,s215,C16,D0,0)
                if not a:continue
                b=T(s215,s214,C15,v215,1)
                if not b:continue
                c=T(s214,s213,C14,v214,w214)
                if not c:continue
                d=T(s213,s212,C13,v213,w213)
                if d:z+=a*b*c*d
            if not z:continue
            y=T0(s10,A0,v312^B0,u30^D0)
            if not y:continue
            k=0
            for q in (s216,v215,s212,s10,u30,v312,v214,w214,v213,w213):k=(k<<1)|q
            r[k]=z*y
        rows.append(r)
    return rank_sparse(rows),sum(not r for r in rows)

def main():
    r,z=block1_c1314_rank()
    assert r==64 and z==32,(r,z)
    print('PASS V26_Q138_S1_LOCAL_EXTENSION_FALSIFIERS')
    print('block1_plus_C13_C14_exact_relaxed_rank=64=16*4 zero_rows=32')
    print('scope=closes this local carry-extension route only; not a lower bound on full S1 central rank')
if __name__=='__main__':main()
