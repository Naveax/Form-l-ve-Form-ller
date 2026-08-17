#!/usr/bin/env python3
import itertools,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))

P=1000003

def tsign(s,t,u,v,w):
    if t!=(s^u^v^w) or not(s or u==v==w):return 0
    return -1 if ((u^w)&(v^w)) else 1

def buildW(b0,d1):
    W=np.zeros((16,16,16,16),dtype=np.int16)
    for A,B,C,d0 in itertools.product((0,1),repeat=4):
        r=(A<<3)|(B<<2)|(C<<1)|d0
        for t4,t3,t2,t1 in itertools.product((0,1),repeat=4):
            ti=(t4<<3)|(t3<<2)|(t2<<1)|t1
            for s4,s3,s2,s1 in itertools.product((0,1),repeat=4):
                si=(s4<<3)|(s3<<2)|(s2<<1)|s1
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
    # CRITICAL: cast inputs to int64 before einsum. The revoked draft passed
    # int32 inputs together with dtype=int64; optimized numpy einsum still
    # returned int32 on some builds, so the subsequent Gram multiplication
    # overflowed and created false ranks96/208.
    A=Ws[(blo,q0)].astype(np.int64);B=Ws[(bhi,q1)].astype(np.int64)
    M=np.einsum('atmk,bmsl->abtskl',A,B,optimize=True).reshape(256,-1)
    assert M.dtype==np.int64
    return M@M.T

def comp_pair_gram(Ws,q0,q1):
    rows=[]
    for D0,D1 in itertools.product((0,1),repeat=2):
        A=Ws[(0,D0)][[(abc<<1)|q0 for abc in range(8)]].astype(np.int64)
        B=Ws[(0,D1)][[(abc<<1)|q1 for abc in range(8)]].astype(np.int64)
        M=np.einsum('atmk,bmsl->abtskl',A,B,optimize=True).reshape(-1)
        assert M.dtype==np.int64
        rows.append(M)
    M=np.stack(rows);return M@M.T

def gram_pair(blo,bhi):
    Ws={(b,d):buildW(b,d) for b in (0,1) for d in (0,1)}
    dp=np.array([((r&1)<<1)|(s&1) for r in range(16) for s in range(16)])
    G=np.zeros((256,256),dtype=np.int64)
    for q0,q1 in itertools.product((0,1),repeat=2):
        GM=main_pair_gram(Ws,blo,bhi,q0,q1)
        GC=comp_pair_gram(Ws,q0,q1)
        G += GM*GC[dp[:,None],dp[None,:]]
    return G

def main():
    special=gram_pair(0,1)   # sites2,3; q138 Bout special at site3
    generic=gram_pair(0,0)   # e.g. sites4,5
    assert not np.any(np.all(special==0,axis=1))
    assert not np.any(np.all(generic==0,axis=1))
    rs=rank_mod(special);rg=rank_mod(generic)
    assert (rs,rg)==(256,256),(rs,rg)
    print('PASS V26_Q138_DOUBLE_ROUND_MULTISITE_OVERFLOW_CORRECTION')
    print('special_four_site_true_int64_gram_rank_mod=256/256')
    print('generic_four_site_true_int64_gram_rank_mod=256/256')
    print('revoked_false_candidates=special96,generic208,Wrepr84.0279,Wrepr83.7283')
    print('cause=int32 Gram overflow from optimized numpy einsum with int32 inputs')
    print('canonical_d1_remains_signed85/factor-generation85 until a new clean exact reduction is found')
if __name__=='__main__':main()
