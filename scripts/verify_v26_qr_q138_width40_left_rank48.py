#!/usr/bin/env python3
import argparse,json,itertools,sys,re
from fractions import Fraction
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_algebraic_width40 as V

def tv(s,t,u,v,w):
    if t!=(s^u^v^w) or not(s or u==v==w): return Fraction(0)
    return Fraction(-1 if ((u^w)&(v^w)) else 1,2**s)

def rref_piv(M):
    A=[list(map(Fraction,r)) for r in M];m=len(A);n=len(A[0]);q=0;piv=[]
    for c in range(n):
        p=next((i for i in range(q,m) if A[i][c]),None)
        if p is None:continue
        A[q],A[p]=A[p],A[q];d=A[q][c];A[q]=[x/d for x in A[q]]
        for i in range(m):
            if i!=q and A[i][c]:
                z=A[i][c];A[i]=[A[i][j]-z*A[q][j] for j in range(n)]
        piv.append(c);q+=1
        if q==m:break
    return q,piv

def inv(A):
    n=len(A);M=[[Fraction(A[i][j]) for j in range(n)]+[Fraction(i==j) for j in range(n)] for i in range(n)]
    for c in range(n):
        p=next(i for i in range(c,n) if M[i][c]);M[c],M[p]=M[p],M[c];d=M[c][c];M[c]=[x/d for x in M[c]]
        for i in range(n):
            if i!=c and M[i][c]:
                z=M[i][c];M[i]=[M[i][j]-z*M[c][j] for j in range(2*n)]
    return [r[n:] for r in M]

def solve_fullcol(C,M):
    r=len(C[0]);n=len(M[0]);rr,rows=rref_piv(list(map(list,zip(*C))));assert rr==r
    I=inv([[C[i][j] for j in range(r)] for i in rows]);Ms=[[M[i][j] for j in range(n)] for i in rows]
    return [[sum(I[a][k]*Ms[k][j] for k in range(r)) for j in range(n)] for a in range(r)]

def tt(order,fix,target):
    vals=[]
    for bits in itertools.product((0,1),repeat=len(order)):
        a=dict(fix);a.update(zip(order,bits));vals.append(tv(**a))
    residual=vals;rprev=1;cores=[]
    for tar in target:
        m=rprev*2;n=len(residual)//m;M=[residual[i*n:(i+1)*n] for i in range(m)]
        r,piv=rref_piv(M);assert r==tar
        C=[[M[i][j] for j in piv] for i in range(m)];R=solve_fullcol(C,M)
        cores.append((rprev,2,r,[x for row in C for x in row]));residual=[x for row in R for x in row];rprev=r
    cores.append((rprev,2,1,residual));return cores

def cf(core,labels):
    a,b,c,flat=core;data={};k=0
    for ix in itertools.product(range(a),range(b),range(c)):
        v=flat[k];k+=1
        if v:data[tuple(z for z,d in zip(ix,(a,b,c)) if d>1)]=v
    return [list(labels),data]

def mul(F,G):
    lf,df=F;lg,dg=G;common=[x for x in lf if x in lg];out=lf+[x for x in lg if x not in lf]
    fi={x:i for i,x in enumerate(lf)};gi={x:i for i,x in enumerate(lg)};idx=defaultdict(list)
    for a,v in dg.items():idx[tuple(a[gi[x]] for x in common)].append((a,v))
    pf=[out.index(x) for x in lf];pg=[out.index(x) for x in lg];res=defaultdict(Fraction)
    for af,vf in df.items():
        for ag,vg in idx.get(tuple(af[fi[x]] for x in common),[]):
            z=[None]*len(out)
            for p,x in zip(pf,af):z[p]=x
            for p,x in zip(pg,ag):
                if z[p] is None:z[p]=x
            res[tuple(z)]+=vf*vg
    return [out,{k:v for k,v in res.items() if v}]

def sumout(F,e):
    labs,d=F;k=labs.index(e);res=defaultdict(Fraction)
    for a,v in d.items():res[a[:k]+a[k+1:]]+=v
    return [labs[:k]+labs[k+1:],{k:v for k,v in res.items() if v}]

def contract(factors,openlabels,dims):
    fac=list(factors)
    while True:
        inc=defaultdict(list)
        for i,f in enumerate(fac):
            if f is not None:
                for e in f[0]:inc[e].append(i)
        cand=[e for e in inc if e not in openlabels]
        if not cand:break
        def score(e):
            U=[]
            for i in inc[e]:
                for x in fac[i][0]:
                    if x!=e and x not in U:U.append(x)
            q=1
            for x in U:q*=dims.get(x,2)
            return q
        e=min(cand,key=score);ids=inc[e];H=fac[ids[0]]
        for i in ids[1:]:H=mul(H,fac[i])
        H=sumout(H,e)
        for i in ids:fac[i]=None
        fac.append(H)
    rem=[f for f in fac if f is not None];H=rem[0]
    for f in rem[1:]:H=mul(H,f)
    return H

def rank_rows(rows):
    basis={}
    for r0 in rows:
        r={j:Fraction(x) for j,x in r0.items() if x}
        while r:
            c=min(r)
            if c not in basis:
                q=1/r[c];basis[c]={j:x*q for j,x in r.items()};break
            q=r[c];b=basis[c]
            for j,x in b.items():
                r[j]=r.get(j,Fraction(0))-q*x
                if not r[j]:r.pop(j,None)
    return len(basis)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('cert',nargs='?',default='research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json');a=ap.parse_args()
    C=json.loads(Path(a.cert).read_text());E=V.build_modified(C);B=V.build_original();id2={eid:n for n,eid in B.e.items()};dims={n:B.d[eid] for n,eid in B.e.items()}
    def bd(S):
        d=1
        for _,q,W in E:
            if any(v in S for v in W) and any(v not in S for v in W):d*=q
        return d
    maxnode=[]
    def walk(x):
        if isinstance(x,int):return {x}
        A=walk(x[0]);D=walk(x[1]);S=A|D
        if bd(S)==2**40:maxnode.append((S,A,D))
        return S
    walk(C['certificate']['tree']);assert len(maxnode)==1
    S,A64,B107=maxnode[0];assert (len(S),len(A64),len(B107))==(171,64,107)
    pext={n for n,d,W in E if any(v in S for v in W) and any(v not in S for v in W)}
    na={n for n,d,W in E if any(v in A64 for v in W) and any(v not in A64 for v in W)}
    ext=sorted(pext&na);inter=sorted(na-pext);assert len(ext)==16 and len(inter)==6
    removed=set(C['rank_compression']['removed_original_leaf_ids']);keep=[v for v in range(568) if v not in removed];new2old={i:v for i,v in enumerate(keep)}
    core4=tt(('t','s','v','u'),{'w':0},[2,3,2]);core3=tt(('u','t','s','v','w'),{},[2,3,3,2]);core2={u:tt(('t','w','v','s'),{'u':u},[2,3,2]) for u in(0,1)};core1={u:tt(('w','v','s','t'),{'u':u},[2,3,2]) for u in(0,1)}
    ranks=[]
    for pat in itertools.product((0,1),repeat=6):
        u1=pat[:3];u2=pat[3:];factors=[]
        for nv in sorted(A64):
            ov=new2old[nv];name=B.names[ov];labs=[id2[e] for e in B.ops[ov] if B.d[e]>1]
            if name.startswith('P_i'):
                data={z:Fraction(1) for z in itertools.product((0,1),repeat=3) if z[0]^z[1]^z[2]==0};factors.append([labs,data]);continue
            m=re.match(r'J([1-4])_i(\d+)_c(\d+)_([a-z])',name);j,i,k=int(m.group(1)),int(m.group(2)),int(m.group(3))
            if j==4:co=core4[k]
            elif j==3:co=core3[k]
            elif j==2:co=core2[u2[i-8]][k]
            else:co=core1[u1[i-8]][k]
            factors.append(cf(co,labs))
        H=contract(factors,set(ext+inter),dims);pos={x:i for i,x in enumerate(H[0])};rows=defaultdict(dict)
        def lin(bs):
            z=0
            for b in bs:z=(z<<1)|b
            return z
        for z,v in H[1].items():
            rr=lin([z[pos[x]] for x in ext]);cc=lin([z[pos[x]] for x in inter]);rows[rr][cc]=rows[rr].get(cc,Fraction(0))+v
        ranks.append(rank_rows(rows.values()))
    assert ranks==[48]*64,set(ranks)
    print('PASS V26_QR_Q138_WIDTH40_LEFT_CHILD_RANK48')
    print('topology_interface=64 exact_rank=48 fixed_u_cases=64 all_exact_fraction=PASS')
    print('parity/XOR constants are internal index-state relabelings and do not change matrix rank')
if __name__=='__main__':main()
