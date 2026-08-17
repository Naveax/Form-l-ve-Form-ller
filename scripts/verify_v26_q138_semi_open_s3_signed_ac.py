#!/usr/bin/env python3
import itertools, math
from collections import Counter
import numpy as np

P=1000003
S3={4,5,11,12,13,19,20,21,27,28,29}
INT_NAMES=['s4','t4','s3','t3','s2','t2','s1','t1','K0','K1','z0','z1']
EXT_NAMES=['Ain','Bin','Cin','O','d0','d1']
NAMES=INT_NAMES+EXT_NAMES
ROW_NAMES={
    4:['t4','t3','t2','t1','K0','K1'],
    11:['t4','t3','t2','t1','K0','K1','z0'],
    19:['t4','t3','t2','t1','K0','K1','d1'],
    27:['t4','t3','t2','t1','K0','K1','z1'],
}
EXPECTED={
    'A':{4:48,11:60,19:96,27:96},
    'C':{4:48,11:72,19:96,27:96},
}
A_DIM=405*(2**46)
C_DIM=243*(2**47)
SEMI_PRODUCT=98415*(2**203)

def tsign(s,t,u,v,w):
    if t!=(s^u^v^w) or not(s or u==v==w): return 0
    return -1 if ((u^w)&(v^w)) else 1

def enc(bs):
    z=0
    for b in bs:z=(z<<1)|b
    return z

def build_site(orient):
    # Exact one-output/open-four-input fused site tensor, multiplied by16.
    # The other three output masks are fixed zero. The 12 internal bits are
    # the fused channels used by the exact EC common-tree skeleton.
    F=np.zeros((64,4096),dtype=np.int16)
    for extbits in itertools.product((0,1),repeat=6):
        Ain,Bin,Cin,O,d0,d1=extbits;e=enc(extbits)
        for ib in itertools.product((0,1),repeat=12):
            s4,t4,s3,t3,s2,t2,s1,t1,K0,K1,z0,z1=ib
            Aout=Cout=Dout=b0=0
            if orient=='A':Aout=O
            elif orient=='C':Cout=O
            else:raise AssertionError(orient)
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
    A=F.reshape((2,)*18)
    old=EXT_NAMES+INT_NAMES
    perm=[old.index(n) for n in NAMES]
    return np.transpose(A,perm)

def flatten(T,row_names):
    col_names=[n for n in NAMES if n not in row_names]
    perm=[NAMES.index(n) for n in row_names+col_names]
    return np.transpose(T,perm).reshape(1<<len(row_names),1<<len(col_names))

def rank_mod(M,p=P):
    A=np.array(M,dtype=np.int64)%p;m,n=A.shape;q=0
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

def signed_class_count(M):
    # Exact upper bound over Q: every nonzero row belongs to one equality/sign
    # class. If there are r such classes, the row span has dimension at most r.
    assert not np.any(np.all(M==0,axis=1))
    C={}
    for i,row in enumerate(M):
        a=row.tobytes();b=(-row).tobytes();key=a if a<b else b
        C.setdefault(key,[]).append(i)
    return len(C),Counter(len(v) for v in C.values())

def main():
    dims={}
    for o in ('A','C'):
        T=build_site(o);prod=1;raw=0
        for s in (4,11,19,27):
            rn=ROW_NAMES[s];M=flatten(T,rn);r=EXPECTED[o][s]
            classes,mults=signed_class_count(M)
            assert classes==r,(o,s,classes,r,mults)
            # Lower bound over Q: rank r modulo P witnesses a nonzero r-minor
            # of the integral scaled matrix, hence rank_Q >= r.
            rm=rank_mod(M);assert rm==r,(o,s,rm,r)
            prod*=r;raw+=len(rn)
        assert raw==27
        dims[o]=prod*(2**30)
    assert dims['A']==A_DIM
    assert dims['C']==C_DIM
    assert math.log2(A_DIM)<55 and math.log2(C_DIM)<55
    assert A_DIM*(2**55)*C_DIM*(2**55)==SEMI_PRODUCT
    print('PASS V26_Q138_SEMI_OPEN_S3_SIGNED_AC')
    print('A_local_ranks=4:48,11:60,19:96,27:96 => A_rank<=405*2^46 log2=%.15f' % math.log2(A_DIM))
    print('C_local_ranks=4:48,11:72,19:96,27:96 => C_rank<=243*2^47 log2=%.15f' % math.log2(C_DIM))
    print('B,D retain generic cap 2^55 each')
    print('four_semi_open_product<=98415*2^203 log2=%.15f' % math.log2(SEMI_PRODUCT))
    print('semi_open_gain_vs_220=%.15f bits' % (220-math.log2(SEMI_PRODUCT)))
    print('scope=exact rational signed fused-channel upper bounds on S3/complement; no global lower bound or constructive/work claim')
if __name__=='__main__':main()
