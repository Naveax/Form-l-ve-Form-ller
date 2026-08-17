#!/usr/bin/env python3
import itertools, math
from functools import lru_cache
import numpy as np

P=1000003
S3={4,5,11,12,13,19,20,21,27,28,29}


def tsign(s,t,u,v,w):
    if t!=(s^u^v^w) or not(s or u==v==w):return 0
    return -1 if ((u^w)&(v^w)) else 1

def enc(bs):
    z=0
    for b in bs:z=(z<<1)|b
    return z


def build_site(orient):
    # Exact fused one-output/open-four-input site tensor, scaled by16.
    # External local bits are Ain,Bin,Cin,O,d0,d1. O is the one open output
    # word; the other three output masks are fixed zero.  b0 represents Bout[i+7],
    # hence for orientation B the physical output bit Bout[j] is located at site j-7.
    F=np.zeros((64,4096),dtype=np.int16)
    for extbits in itertools.product((0,1),repeat=6):
        Ain,Bin,Cin,O,d0,d1=extbits;e=enc(extbits)
        for ib in itertools.product((0,1),repeat=12):
            s4,t4,s3,t3,s2,t2,s1,t1,K0,K1,z0,z1=ib
            Aout=Cout=Dout=b0=0
            if orient=='A':Aout=O
            elif orient=='B':b0=O
            elif orient=='C':Cout=O
            else:Dout=O
            scale=1<<(4-(s4+s3+s2+s1));v=0
            for x in (0,1):
                a=tsign(s4,t4,x,z0^Dout,Cout^b0)
                if not a:continue
                for q in (0,1):
                    b=tsign(s3,t3,q,K0^b0,Aout^z1)
                    if not b:continue
                    c=tsign(s2,t2,Cin,z1^d1,x^K1)
                    if not c:continue
                    d=tsign(s1,t1,Ain,K1^Bin,q^d0)
                    if d:v+=a*b*c*d*scale
            if v:F[e,enc(ib)]=v
    return F

FS={o:build_site(o) for o in 'ABCD'}


def rowmask(i,orient):
    flags=[i in S3,i in S3,i in S3,((i+7)%32 in S3) if orient=='B' else (i in S3)]
    return enc(flags),sum(flags)

@lru_cache(None)
def site_cross_gram(orient,mask,d0a,d1a,d0b,d1b):
    rowpos=[p for p in range(4) if (mask>>(3-p))&1]
    colpos=[p for p in range(4) if p not in rowpos]
    nr=1<<len(rowpos);nc=1<<len(colpos)
    A=np.zeros((nr,nc*4096),dtype=np.int16);B=np.zeros_like(A)
    for rb in itertools.product((0,1),repeat=len(rowpos)):
        ri=enc(rb);base=[None]*4
        for p,b in zip(rowpos,rb):base[p]=b
        for cb in itertools.product((0,1),repeat=len(colpos)):
            ci=enc(cb);v=base.copy()
            for p,b in zip(colpos,cb):v[p]=b
            A[ri,ci*4096:(ci+1)*4096]=FS[orient][enc(v+[d0a,d1a])]
            B[ri,ci*4096:(ci+1)*4096]=FS[orient][enc(v+[d0b,d1b])]
    return (A.astype(np.int64)@B.astype(np.int64).T)%P

def rank_mod(A):
    A=np.array(A,dtype=np.int64)%P;m,n=A.shape;q=0
    for c in range(n):
        nz=np.flatnonzero(A[q:,c])
        if not len(nz):continue
        k=q+int(nz[0])
        if k!=q:A[[q,k]]=A[[k,q]]
        A[q]=(A[q]*pow(int(A[q,c]),P-2,P))%P
        ids=np.flatnonzero(A[:,c]);ids=ids[ids!=q]
        if len(ids):
            fac=A[ids,c].copy()
            A[ids]=(A[ids]-fac[:,None]*A[q][None,:])%P
        q+=1
        if q==m:break
    return q

def pair_rank(i,orient):
    j=i+16;mi,ki=rowmask(i,orient);mj,kj=rowmask(j,orient)
    di=i in S3;dj=j in S3;kd=int(di)+int(dj)
    cfg=[]
    for b in itertools.product((0,1),repeat=ki+kj+kd):
        p=0;ri=enc(b[p:p+ki]);p+=ki;rj=enc(b[p:p+kj]);p+=kj;D={}
        if di:D[i]=b[p];p+=1
        if dj:D[j]=b[p];p+=1
        cfg.append((ri,rj,D))
    n=len(cfg);G=np.zeros((n,n),dtype=np.int64);dcols=[x for x in (i,j) if x not in S3]
    for a,(ria,rja,Da) in enumerate(cfg):
        for b in range(a,n):
            rib,rjb,Db=cfg[b];z=0
            for cb in itertools.product((0,1),repeat=len(dcols)):
                C=dict(zip(dcols,cb))
                Dia=Da.get(i,C.get(i));Dja=Da.get(j,C.get(j));Dib=Db.get(i,C.get(i));Djb=Db.get(j,C.get(j))
                Gi=site_cross_gram(orient,mi,Dia,Dja,Dib,Djb)
                Gj=site_cross_gram(orient,mj,Dja,Dia,Djb,Dib)
                z+=int(Gi[ria,rib])*int(Gj[rja,rjb])
            G[a,b]=G[b,a]=z%P
    return n,rank_mod(G)


def main():
    # In the ChaCha diagonal layer feeding central column (0,4,8,12), the four
    # predecessor diagonals contribute local output words A,B,C,D respectively:
    # (0,5,10,15)->A0; (3,4,9,14)->B4; (2,7,8,13)->C8; (1,6,11,12)->D12.
    totals={}
    for o in 'ABCD':
        raw=ranklog=0;active=[]
        for i in range(16):
            n,r=pair_rank(i,o)
            if n>1:
                active.append((i,i+16,n,r));raw+=int(round(math.log2(n)));ranklog+=math.log2(r)
                assert r==n,(o,i,n,r)
        assert raw==55 and abs(ranklog-55)<1e-12,(o,raw,ranklog)
        totals[o]=active
    print('PASS V26_Q138_SEMI_OPEN_S3_PAIR_FULLRANK')
    print('orientations=A,B,C,D all occurrence-closed i<->i+16 pair factors are full row rank modulo odd prime')
    print('sum_pair_log2_rank=55 for each orientation, exactly matching the physical 5*|S3| Hilbert cap')
    print('scope=falsifies this local pair-factor compression route only; not a global lower bound on semi-open QR Schmidt rank')

if __name__=='__main__':main()
