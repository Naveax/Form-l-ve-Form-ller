#!/usr/bin/env python3
import itertools,sys
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S


def enc(bs):
    z=0
    for b in bs:z=(z<<1)|b
    return z

def j1_basis(D):
    rows=[]
    for A0,B0,A1,B1,A2,B2 in itertools.product((0,1),repeat=6):
        r={}
        for s2,k2,q2,k1,q1,v0,q0 in itertools.product((0,1),repeat=7):
            z=Fraction(0)
            for s1,s0 in itertools.product((0,1),repeat=2):
                a=S.T(s2,s1,A2,k2^B2,q2^D[2])
                if not a:continue
                b=S.T(s1,s0,A1,k1^B1,q1^D[1])
                if not b:continue
                c=S.T0(s0,A0,v0^B0,q0^D[0])
                if c:z+=a*b*c
            if z:r[enc((s2,k2,q2,k1,q1,v0,q0))]=z
        rows.append(r)
    B=S.basis(rows);assert len(B)==64
    return B

def j2_basis(D):
    rows=[]
    for C15,C16 in itertools.product((0,1),repeat=2):
        r={}
        for cols in itertools.product((0,1),repeat=9):
            s18,C18,x18,w18,C17,x17,w17,v15,s14=cols;z=Fraction(0)
            for s17,s16,s15 in itertools.product((0,1),repeat=3):
                a=S.T(s18,s17,C18,x18^D[2],w18)
                if not a:continue
                b=S.T(s17,s16,C17,x17^D[1],w17)
                if not b:continue
                c=S.T(s16,s15,C16,D[0],0)
                if not c:continue
                d=S.T(s15,s14,C15,v15,1)
                if d:z+=a*b*c*d
            if z:r[enc(cols)]=z
        rows.append(r)
    B=S.basis(rows);assert len(B)==3
    return B

def main():
    V=[]
    for ds in itertools.product((0,1),repeat=3):
        D=dict(enumerate(ds));J=j1_basis(D);K=j2_basis(D)
        assert (len(J),len(K))==(64,3)
        for a in J:
            for b in K:
                r={}
                for i,x in a.items():
                    for j,y in b.items():r[(i<<9)|j]=x*y
                V.append(r)
    assert len(V)==8*64*3==1536
    u=len(S.basis(V));assert u==1024,u
    print('PASS V26_Q138_BLOCK1_TWO_SITE_EXTENSION_FALSIFIER')
    print('D012_sectors=8 j1_rank=64 j2_rank=3 exact_union_rank=1024')
    print('naive_block1_times_six_raw_bits=16*2^6=1024')
    print('scope=closes this occurrence-closed two-site block1 extension route only; not a lower bound on full S1 rank')
if __name__=='__main__':main()
