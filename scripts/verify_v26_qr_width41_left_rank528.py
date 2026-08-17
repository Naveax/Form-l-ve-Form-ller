#!/usr/bin/env python3
from fractions import Fraction
from collections import defaultdict
from itertools import product


def tv(s,t,u,v,w):
    if t != (s ^ u ^ v ^ w) or not (s or u == v == w):
        return Fraction(0)
    return Fraction(-1 if ((u ^ w) & (v ^ w)) else 1, 2**s)


def rref_rank_pivcols(M):
    A=[list(map(Fraction,row)) for row in M]
    m=len(A); n=len(A[0]); r=0; piv=[]
    for c in range(n):
        p=next((i for i in range(r,m) if A[i][c]),None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]
        d=A[r][c]; A[r]=[x/d for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                q=A[i][c]
                A[i]=[A[i][j]-q*A[r][j] for j in range(n)]
        piv.append(c); r+=1
        if r==m: break
    return r,piv


def invert(A):
    n=len(A)
    M=[[Fraction(A[i][j]) for j in range(n)]+[Fraction(int(i==j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p=next(i for i in range(c,n) if M[i][c])
        M[c],M[p]=M[p],M[c]
        d=M[c][c]; M[c]=[x/d for x in M[c]]
        for i in range(n):
            if i!=c and M[i][c]:
                q=M[i][c]
                M[i]=[M[i][j]-q*M[c][j] for j in range(2*n)]
    return [row[n:] for row in M]


def solve_fullcol(C,M):
    r=len(C[0]); n=len(M[0])
    rr,rows=rref_rank_pivcols(list(map(list,zip(*C))))
    assert rr==r
    Csub=[[C[i][j] for j in range(r)] for i in rows]
    I=invert(Csub)
    Msub=[[M[i][j] for j in range(n)] for i in rows]
    return [[sum(I[a][k]*Msub[k][j] for k in range(r)) for j in range(n)] for a in range(r)]


def tt_t4_fixed_w(w=0):
    vals=[]
    for t,s,v,u in product((0,1),repeat=4):
        vals.append(tv(s,t,u,v,w))
    residual=vals; rprev=1; targets=[2,3,2]; cores=[]
    for k in range(3):
        m=rprev*2; n=len(residual)//m
        M=[residual[i*n:(i+1)*n] for i in range(m)]
        r,piv=rref_rank_pivcols(M); assert r==targets[k]
        C=[[M[i][j] for j in piv] for i in range(m)]
        R=solve_fullcol(C,M)
        cores.append((rprev,2,r,[x for row in C for x in row]))
        residual=[x for row in R for x in row]; rprev=r
    cores.append((rprev,2,1,residual))
    return cores


def core_factor(core, labels):
    a,b,c,flat=core
    shape=(a,b,c); data={}; k=0
    for ix in product(*[range(d) for d in shape]):
        val=flat[k]; k+=1
        if val:
            kept=[]
            for z,d in zip(ix,shape):
                if d>1: kept.append(z)
            data[tuple(kept)]=val
    return [list(labels),data]


def sparse_mul(F,G):
    lf,df=F; lg,dg=G
    common=[x for x in lf if x in lg]
    out=lf+[x for x in lg if x not in lf]
    fi={x:i for i,x in enumerate(lf)}; gi={x:i for i,x in enumerate(lg)}
    index=defaultdict(list)
    for ag,vg in dg.items():
        index[tuple(ag[gi[x]] for x in common)].append((ag,vg))
    oiF=[out.index(x) for x in lf]; oiG=[out.index(x) for x in lg]
    res=defaultdict(Fraction)
    for af,vf in df.items():
        key=tuple(af[fi[x]] for x in common)
        for ag,vg in index.get(key,[]):
            vals=[None]*len(out)
            for p,z in zip(oiF,af): vals[p]=z
            for p,z in zip(oiG,ag):
                if vals[p] is None: vals[p]=z
            res[tuple(vals)] += vf*vg
    return [out,{k:v for k,v in res.items() if v}]


def sparse_sumout(F,e):
    labs,d=F; k=labs.index(e); out=labs[:k]+labs[k+1:]
    res=defaultdict(Fraction)
    for a,v in d.items(): res[a[:k]+a[k+1:]] += v
    return [out,{k:v for k,v in res.items() if v}]


def contract_factors(factors, open_labels):
    fac=list(factors)
    while True:
        incid=defaultdict(list)
        for i,f in enumerate(fac):
            if f is None: continue
            for e in f[0]: incid[e].append(i)
        candidates=[e for e,ids in incid.items() if e not in open_labels and len(ids)>=1]
        if not candidates: break
        def score(e):
            ids=incid[e]; U=[]
            for i in ids:
                for x in fac[i][0]:
                    if x!=e and x not in U: U.append(x)
            n=1
            for x in U: n*=3 if x=='a27' else 2
            return n
        e=min(candidates,key=score); ids=incid[e]
        H=fac[ids[0]]
        for i in ids[1:]: H=sparse_mul(H,fac[i])
        H=sparse_sumout(H,e)
        for i in ids: fac[i]=None
        fac.append(H)
    rem=[f for f in fac if f is not None]
    H=rem[0]
    for f in rem[1:]: H=sparse_mul(H,f)
    return H


def build_A():
    C=tt_t4_fixed_w(0)
    factors=[]
    included={23:[1,2,3],24:[0,1,2,3],25:[0,1,2],26:[0,1,2,3],27:[0,1],28:[0,1,2,3],29:[0]}
    for i,ks in included.items():
        physical=['t','s','v','u']
        for k in ks:
            labs=[]
            if k>0: labs.append(f'a{i}_{k-1}')
            x=physical[k]
            if x=='t': labs.append(f's4_{i-1}')
            elif x=='s': labs.append(f's4_{i}')
            elif x=='v': labs.append(f'v4_{i}')
            else: labs.append(f'u4_{i}')
            if k<3: labs.append(f'a{i}_{k}')
            labs=[('a27' if z=='a27_1' else z) for z in labs]
            factors.append(core_factor(C[k],labs))
    data={}
    for u,q,w in product((0,1),repeat=3):
        if u^q^w==0: data[(u,q,w)]=Fraction(1)
    factors.append([['u4_26','q','w2_26'],data])
    rows=['a23_0','u4_23','u4_24','a25_2','w2_26','a29_0']
    cols=['v4_23','v4_24','v4_25','v4_26','a27','u4_28']
    open_labels=set(rows+cols+['q','r'])
    for f in factors:
        f[0][:]=[('r' if x=='v4_28' else x) for x in f[0]]
    return contract_factors(factors,open_labels),rows,cols


def lin(vals,dims):
    z=0
    for v,d in zip(vals,dims): z=z*d+v
    return z


def sector_rows(F,rows,fixed,cols):
    labs,data=F; pos={x:i for i,x in enumerate(labs)}
    rd=[2]*len(rows); cd=[3 if x=='a27' else 2 for x in cols]
    R=[defaultdict(Fraction) for _ in range(2**len(rows))]
    for a,val in data.items():
        if any(a[pos[x]]!=v for x,v in fixed.items()): continue
        i=lin([a[pos[x]] for x in rows],rd)
        j=lin([a[pos[x]] for x in cols],cd)
        R[i][j]+=val
    return R


def sparse_rank(rows):
    basis={}
    for r0 in rows:
        r={j:Fraction(v) for j,v in r0.items() if v}
        while r:
            c=min(r)
            if c not in basis:
                q=1/r[c]; r={j:v*q for j,v in r.items()}; basis[c]=r; break
            b=basis[c]; q=r[c]
            for j,v in b.items():
                z=r.get(j,Fraction(0))-q*v
                if z: r[j]=z
                elif j in r: del r[j]
    return len(basis)


def concat_col_rank(R0,n0,R1,n1):
    rows=[]
    for a,b in zip(R0,R1):
        d=dict(a)
        for j,v in b.items(): d[n0+j]=v
        rows.append(d)
    return sparse_rank(rows)


def T2(u,v):
    return [[tv(s,t,u,v,w) for t in (0,1)] for w,s in product((0,1),repeat=2)]


def T3(w):
    return [[tv(s,t,u,v,w) for t,v in product((0,1),repeat=2)] for u,s in product((0,1),repeat=2)]


def kron_rows(A,B,nB):
    out=[]
    for ra in A:
        for rb in B:
            d={}
            for ja,va in ra.items():
                for jb,vb in rb.items(): d[ja*nB+jb]=va*vb
            out.append(d)
    return out


def dense_rows(M):
    return [{j:v for j,v in enumerate(row) if v} for row in M]


def add_rows(A,B):
    out=[]
    for a,b in zip(A,B):
        d=dict(a)
        for j,v in b.items():
            z=d.get(j,Fraction(0))+v
            if z: d[j]=z
            elif j in d: del d[j]
        out.append(d)
    return out


def B_rows(u2,kv,kw,r):
    A=T2(u2,r^kv); B=T3(r^kw)
    M=[]
    for i2 in range(4):
        for i3 in range(4):
            M.append([A[i2][j2]*B[i3][j3] for j2 in range(2) for j3 in range(4)])
    return dense_rows(M)


def F1(u1):
    M=[[Fraction(0) for _ in range(4)] for _ in range(4)]
    for w,t in product((0,1),repeat=2):
        for v,s in product((0,1),repeat=2):
            M[2*w+t][2*v+s]=tv(s,t,u1,v,w)
    return M


def main():
    F,arows,acols=build_A()
    A={}
    for q in (0,1):
        R=[]
        for r in (0,1):
            X=sector_rows(F,arows,{'q':q,'r':r},acols)
            R.append(X)
        ranks=[sparse_rank(x) for x in R]
        union=concat_col_rank(R[0],96,R[1],96)
        assert ranks==[18,17] and union==18
        A[q]=R

    for u2,kv,kw in product((0,1),repeat=3):
        for q in (0,1):
            B0=B_rows(u2,kv,kw,0); B1=B_rows(u2,kv,kw,1)
            assert sparse_rank(B0)==6 and sparse_rank(B1)==6
            assert concat_col_rank(B0,8,B1,8)==10
            K0=kron_rows(A[q][0],B0,8)
            K1=kron_rows(A[q][1],B1,8)
            assert sparse_rank(add_rows(K0,K1))==176

    for u1 in (0,1):
        M=F1(u1)
        Q0=[row[:2] for row in M]; Q1=[row[2:] for row in M]
        r0=rref_rank_pivcols(Q0)[0]; r1=rref_rank_pivcols(Q1)[0]
        union=rref_rank_pivcols([Q0[i]+Q1[i] for i in range(4)])[0]
        assert sorted((r0,r1))==[1,2] and union==3
        assert (r0+r1)*176 == 528

    print('PASS V26_QR_WIDTH41_LEFT_MAP_RANK528')
    print('A_sector_ranks=18,17 A_union=18 B_sector_rank=6 B_union=10 F2_rank=176 F1_sector_ranks=2+1 L_rank=528')

if __name__=='__main__': main()
