#!/usr/bin/env python3
import itertools,math,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S

BITS=(13,14,15,16)

def enc(bs):
    z=0
    for b in bs:z=(z<<1)|b
    return z

def dec(z,n):return tuple((z>>(n-1-i))&1 for i in range(n))

def old_j1_basis(D):
    # Exact j1 bits13..16 basis; this is the same object as signed85 block2.
    rows=[]
    for z in itertools.product((0,1),repeat=8):
        A=dict(zip(BITS,z[:4]));B=dict(zip(BITS,z[4:]));r={}
        for s16 in (0,1):
          for us in itertools.product((0,1),repeat=4):
           U=dict(zip(BITS,us))
           for x13,x14 in itertools.product((0,1),repeat=2):
            X={13:x13,14:x14};s=s16;c=Fraction(1);ok=True
            for i in (16,15,14,13):
                base=0 if i==16 else 1 if i==15 else X[i]
                v=base^B[i];w=U[i]^D[i];t=s^A[i]^v^w;q=S.T(s,t,A[i],v,w)
                if not q:ok=False;break
                c*=q;s=t
            if ok:
                k=enc((s16,)+us+(x13,x14)+(s,));r[k]=r.get(k,Fraction(0))+c
        rows.append(r)
    B=S.basis(rows);assert len(B)==112
    return B

def extend_bit12(B,D12):
    # Add physical A12,B12 and close D12 at j1 bit12. Columns become
    # (s16,u12,u13,u14,u15,u16,x12,x13,x14,s11).
    rows=[]
    for v0 in B:
      for A12,B12 in itertools.product((0,1),repeat=2):
        r={}
        for k,a in v0.items():
            s16,u13,u14,u15,u16,x13,x14,s12=dec(k,8)
            for u12,x12 in itertools.product((0,1),repeat=2):
                v=x12^B12;w=u12^D12;s11=s12^A12^v^w
                q=S.T(s12,s11,A12,v,w)
                if q:
                    j=enc((s16,u12,u13,u14,u15,u16,x12,x13,x14,s11))
                    r[j]=r.get(j,Fraction(0))+a*q
        rows.append(r)
    B2=S.basis(rows);assert len(B2)==448
    return B2

def high28(D):
    r={}
    for Cs in itertools.product((0,1),repeat=4):
      for Ws in itertools.product((0,1),repeat=4):
        C=dict(zip((28,29,30,31),Cs));W=dict(zip((28,29,30,31),Ws));s=0;c=Fraction(1);ok=True
        for i in (31,30,29,28):
            v=D[i-16];t=s^C[i]^v^W[i];q=S.T(s,t,C[i],v,W[i])
            if not q:ok=False;break
            c*=q;s=t
        if ok:r[enc(Cs+Ws+(s,))]=c
    return r

def bit0_rows(D16):
    rows=[]
    for C0 in (0,1):
        r={}
        for s0,u40,v312 in itertools.product((0,1),repeat=3):
            q=S.T0(s0,C0,D16,u40^v312)
            if q:r[enc((s0,u40,v312))]=q
        rows.append(r)
    B=S.basis(rows);assert len(B)==2
    return B

def main():
    unions=[];intersections=[];high=[]
    for p in itertools.product((0,1),repeat=4): # D12..15
        D12,D13,D14,D15=p;both=[]
        for D16 in (0,1):
            D={13:D13,14:D14,15:D15,16:D16}
            E=extend_bit12(old_j1_basis(D),D12);both.extend(E)
        u=len(S.basis(both));assert u==472,u
        unions.append(u);intersections.append(448+448-u)
        DD={12:D12,13:D13,14:D14,15:D15,16:0};high.append(high28(DD))
    assert Counter(unions)==Counter({472:16})
    assert Counter(intersections)==Counter({424:16})
    assert len(S.basis(high))==16

    B0=bit0_rows(0);B1=bit0_rows(1)
    assert len(S.basis(B0+B1))==3
    # Two 2D bit0 spaces therefore intersect in dimension1.
    k_inter=1

    # For each independent high-sector p, the two D16 sectors are
    # J0⊗K0 and J1⊗K1. Their intersection is
    # (J0∩J1)⊗(K0∩K1), dimension424*1.
    per=448*2+448*2-424*k_inter
    assert per==1368
    R=16*per
    assert R==21888
    naive=2784*8;assert naive==22272
    assert Fraction(naive,R)==Fraction(58,57)

    old_center=16*2784*(2**26)
    new_center=16*R*(2**23)
    assert Fraction(new_center,old_center)==Fraction(57,58)
    w=math.log2(new_center)+44
    assert abs(w-(85.44294349584872-math.log2(58/57)))<1e-12
    print('PASS V26_Q138_SIGNED_BLOCK2_EXTEND12_RANK21888')
    print('extended_j1_sector_rank=448; D16_pair_union_rank=472 intersection=424 for all16 prefixes')
    print('j2_high_D12..15_span=16; bit0_D16_spaces=2+2 union3 intersection1')
    print('extended_block2_exact_rank=16*1368=21888')
    print('gain_vs_old_block2_times3raw=22272/21888=58/57')
    print('new_S1_message_log2=%.15f' % w)
    print('scope=exact rational representation rank; factor-generation constructivity is a separate ledger')
if __name__=='__main__':main()
