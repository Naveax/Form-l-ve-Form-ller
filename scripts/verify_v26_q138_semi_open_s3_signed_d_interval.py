#!/usr/bin/env python3
import itertools, math
from collections import Counter
import numpy as np

P=1000003
INT_NAMES=['s4','t4','s3','t3','s2','t2','s1','t1','K0','K1','z0','z1']
EXT_NAMES=['Ain','Bin','Cin','O','d0','d1']
NAMES=INT_NAMES+EXT_NAMES
TIN=['t4','t3','t2','t1','K0','K1']
SOUT=['s4','s3','s2','s1','K0','K1']
CARRY_T=['t4','t3','t2','t1']
CARRY_S=['s4','s3','s2','s1']
OTHER={11:['t4','t3','t2','t1','K0','K1','z0'],19:['t4','t3','t2','t1','K0','K1','d1'],27:['t4','t3','t2','t1','K0','K1','z1']}

def tsign(s,t,u,v,w):
    if t!=(s^u^v^w) or not(s or u==v==w):return 0
    return -1 if ((u^w)&(v^w)) else 1

def enc(bs):
    z=0
    for b in bs:z=(z<<1)|b
    return z

def build_site_D():
    F=np.zeros((64,4096),dtype=np.int16)
    for extbits in itertools.product((0,1),repeat=6):
        Ain,Bin,Cin,O,d0,d1=extbits;e=enc(extbits)
        for ib in itertools.product((0,1),repeat=12):
            s4,t4,s3,t3,s2,t2,s1,t1,K0,K1,z0,z1=ib
            Aout=Cout=b0=0;Dout=O
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
    A=F.reshape((2,)*18);old=EXT_NAMES+INT_NAMES
    return np.transpose(A,[old.index(n) for n in NAMES])

def flatten(T,row):
    col=[n for n in NAMES if n not in row]
    return np.transpose(T,[NAMES.index(n) for n in row+col]).reshape(1<<len(row),-1)

def gram(T,row):
    M=flatten(T,row).astype(np.int64);return M@M.T

def rank_mod(A,p=P):
    A=np.array(A,dtype=np.int64,copy=True)%p;m,n=A.shape;q=0
    for c in range(n):
        nz=np.flatnonzero(A[q:,c])
        if not len(nz):continue
        k=q+int(nz[0])
        if k!=q:A[[q,k]]=A[[k,q]]
        A[q]=(A[q]*pow(int(A[q,c]),p-2,p))%p
        ids=np.flatnonzero(A[q+1:,c])+q+1
        if len(ids):
            f=A[ids,c].copy();A[ids]=(A[ids]-f[:,None]*A[q][None,:])%p
        q+=1
        if q==m:break
    return q

def signed_reps(M):
    C={};zero=0
    for i,row in enumerate(M):
        if np.all(row==0):zero+=1;continue
        a=row.tobytes();b=(-row).tobytes();key=a if a<=b else b
        C.setdefault(key,i)
    return list(C.values()),zero

def sparse_relations(M,p=P):
    basis={};deps=[]
    for i in range(M.shape[0]):
        row={int(c):int(M[i,c])%p for c in np.flatnonzero(M[i])};coef={i:1}
        while row:
            c=min(row)
            if c not in basis:
                inv=pow(row[c],p-2,p)
                row={j:(v*inv)%p for j,v in row.items() if (v*inv)%p}
                coef={j:(v*inv)%p for j,v in coef.items() if (v*inv)%p}
                basis[c]=(row,coef);break
            br,bc=basis[c];a=row[c]
            for j,v in br.items():
                nv=(row.get(j,0)-a*v)%p
                if nv:row[j]=nv
                elif j in row:del row[j]
            for j,v in bc.items():
                nv=(coef.get(j,0)-a*v)%p
                if nv:coef[j]=nv
                elif j in coef:del coef[j]
        else:deps.append(coef)
    return len(basis),deps

def cen(v):return v if v<=P//2 else v-P

def main():
    T=build_site_D();q=16
    GA=gram(T,TIN+CARRY_S).reshape(64,q,64,q)
    GB=gram(T,CARRY_T+SOUT).reshape(q,64,q,64)
    G=np.einsum('lqLQ,qrQR->lrLR',GA,GB,optimize=True).reshape(4096,4096)
    reps,zero=signed_reps(G)
    assert zero==1520 and len(reps)==1760,(zero,len(reps))
    r,deps=sparse_relations(G[reps]);assert r==1016 and len(deps)==744,(r,len(deps))
    # Every modular dependency lifts to an exact integer relation; hence rank_Q<=1016.
    for d in deps:
        z=np.zeros(4096,dtype=np.int64)
        for j,a in d.items():z+=cen(a)*G[reps[j]]
        assert not np.any(z)
    # rank mod P gives rank_Q>=1016, so interval rank is exactly1016.
    for s,row in OTHER.items():
        M=flatten(T,row);assert rank_mod(M)==96
        reps0,z0=signed_reps(M);assert z0==0 and len(reps0)==96
    D=1016*(96**3)*(2**24);assert D==3429*(2**42)
    print('PASS V26_Q138_SEMI_OPEN_S3_SIGNED_D_INTERVAL')
    print('D_interval_4_5_exact_rank=1016/4096')
    print('gram_zero_rows=1520 signed_reps=1760 exact_extra_relations=744')
    print('D_other_entry_ranks=11:96,19:96,27:96')
    print('D_rank<=1016*96^3*2^24=3429*2^42 log2=%.15f' % math.log2(D))
    print('scope=exact rational representation upper bound on S3/complement; no global lower bound or constructive/work claim')
if __name__=='__main__':main()
