#!/usr/bin/env python3
import itertools,math,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed85 as S

P=1000003


def tsign(s,t,u,v,w):
    if t!=(s^u^v^w) or not(s or u==v==w):return 0
    return -1 if ((u^w)&(v^w)) else 1

def buildW(b0,d1):
    # Exact central q138 fused site tensor scaled by16.
    # External physical inputs are A,B,C,d0,d1. Outputs A/C/D are fixed0;
    # b0=Bout[i+7] is fixed by q138 and is1 only at site3.
    W=np.zeros((16,16,16,16),dtype=np.int16)
    for A,B,C,d0 in itertools.product((0,1),repeat=4):
        r=(A<<3)|(B<<2)|(C<<1)|d0
        for tb in itertools.product((0,1),repeat=4):
            t4,t3,t2,t1=tb;ti=(t4<<3)|(t3<<2)|(t2<<1)|t1
            for sb in itertools.product((0,1),repeat=4):
                s4,s3,s2,s1=sb;si=(s4<<3)|(s3<<2)|(s2<<1)|s1
                scale=1<<(4-(s4+s3+s2+s1))
                for K0,K1,z0,z1 in itertools.product((0,1),repeat=4):
                    ki=(K0<<3)|(K1<<2)|(z0<<1)|z1;v=0
                    for x in (0,1):
                        a=tsign(s4,t4,x,z0,b0)
                        if not a:continue
                        for q in (0,1):
                            b=tsign(s3,t3,q,K0^b0,z1)
                            if not b:continue
                            c=tsign(s2,t2,C,z1^d1,x^K1)
                            if not c:continue
                            d=tsign(s1,t1,A,K1^B,q^d0)
                            if d:v+=a*b*c*d*scale
                    W[r,ti,si,ki]=v
    return W

def rank_mod(A,p=P):
    A=np.array(A,dtype=np.int64,copy=True)%p;m,n=A.shape;q=0
    for c in range(n):
        nz=np.flatnonzero(A[q:,c])
        if not len(nz):continue
        k=q+int(nz[0])
        if k!=q:A[[q,k]]=A[[k,q]]
        A[q]=(A[q]*pow(int(A[q,c]),p-2,p))%p
        ids=np.flatnonzero(A[:,c]);ids=ids[ids!=q]
        if len(ids):
            f=A[ids,c].copy();A[ids]=(A[ids]-f[:,None]*A[q][None,:])%p
        q+=1
        if q==m:break
    return q

def main_pair_gram(Ws,blo,bhi,q0,q1):
    A=Ws[(blo,q0)].astype(np.int32);B=Ws[(bhi,q1)].astype(np.int32)
    # Contract the four adjacent carry channels exactly. Boundary carries and
    # K/z channels remain relaxed independent retained columns.
    M=np.einsum('atmk,bmsl->abtskl',A,B,optimize=True,dtype=np.int64).reshape(256,-1)
    return M@M.T

def comp_pair_gram(Ws,q0,q1):
    # Complement sites18,19: A/B/C are retained columns; d0 are q0,q1;
    # d1 are the repeated physical row bits D2,D3.
    rows=[]
    for D2,D3 in itertools.product((0,1),repeat=2):
        A=Ws[(0,D2)][[(abc<<1)|q0 for abc in range(8)]].astype(np.int32)
        B=Ws[(0,D3)][[(abc<<1)|q1 for abc in range(8)]].astype(np.int32)
        M=np.einsum('atmk,bmsl->abtskl',A,B,optimize=True,dtype=np.int64).reshape(-1)
        rows.append(M)
    M=np.stack(rows)
    return M@M.T

def gram_four_site():
    Ws={(b,d):buildW(b,d) for b in (0,1) for d in (0,1)}
    G=np.zeros((256,256),dtype=np.int64)
    # Row index is (ABC2,D2,ABC3,D3). Complement D18,D19 are summed columns.
    dp=np.array([((r&1)<<1)|(s&1) for r in range(16) for s in range(16)])
    for q0,q1 in itertools.product((0,1),repeat=2):
        GM=main_pair_gram(Ws,0,1,q0,q1)  # q138 b0=1 only at site3
        GC=comp_pair_gram(Ws,q0,q1)
        G += GM*GC[dp[:,None],dp[None,:]]
    return G

def signed_classes(G):
    zero=[];C={}
    for i,row in enumerate(G):
        if np.all(row==0):zero.append(i);continue
        a=row.tobytes();b=(-row).tobytes();key=a if a<=b else b
        C.setdefault(key,[]).append(i)
    return zero,C

def tree_bound(newS1):
    # Recount frozen HT tree. Signed85 already proved all noncritical nodes<=80.
    s1_exp=math.log2(newS1)+44
    s2_exp=79+math.log2(31)
    assert s1_exp>s2_exp and s1_exp>80
    return s1_exp,s2_exp

def main():
    G=gram_four_site();assert G.shape==(256,256)
    zero,C=signed_classes(G)
    assert len(zero)==64
    assert len(C)==96
    assert Counter(map(len,C.values()))==Counter({2:96})
    assert rank_mod(G)==96
    # Signed-class upper bound96 + odd-prime lower bound96 => rank_Q(G)=96.
    # For the real/rational coefficient matrix M, rank(MM^T)=rank(M), hence
    # the relaxed four-site coefficient map has exact rank96.
    R=16*2784*96*(2**18)
    assert R==261*(2**32)
    old=87*(2**35);assert Fraction(R,old)==Fraction(3,8)
    w,s2=tree_bound(R)
    assert abs(w-(76+math.log2(261)))<1e-12
    print('PASS V26_Q138_DOUBLE_ROUND_SIGNED84_MULTISITE')
    print('four_site_block={2,3,18,19} physical_row_bits=8 raw_dimension=256')
    print('gram_zero_rows=64 signed_nonzero_classes=96 class_sizes=2 exact_rank_Q=96')
    print('rank_center_S1<=16*2784*96*2^18=261*2^32')
    print('S1_message<=261*2^76 log2=%.15f' % w)
    print('S2_message_log2=%.15f' % s2)
    print('gain_vs_signed85=%.15f bits' % math.log2(8/3))
    print('scope=exact representation upper bound; long-range K/z columns were relaxed independently, so later identifications cannot increase row rank')
if __name__=='__main__':main()
