#!/usr/bin/env python3
import argparse,itertools,json
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path

L=("s","t","u","v","w")
def tv(s,t,u,v,w):
    if t!=(s^u^v^w) or not(s or u==v==w): return Fraction(0)
    return Fraction(-1 if ((u^w)&(v^w)) else 1,2**s)
def rank(A):
    A=[[Fraction(x) for x in r] for r in A]; m=len(A); n=len(A[0]); q=0
    for c in range(n):
        p=next((i for i in range(q,m) if A[i][c]),None)
        if p is None: continue
        A[q],A[p]=A[p],A[q]; d=A[q][c]; A[q]=[x/d for x in A[q]]
        for i in range(m):
            if i!=q and A[i][c]:
                d=A[i][c]; A[i]=[A[i][j]-d*A[q][j] for j in range(n)]
        q+=1
    return q
def tensor(fix=None,sumlegs=()):
    fix=dict(fix or {}); V=[x for x in L if x not in fix and x not in sumlegs]; D={}
    for b in itertools.product((0,1),repeat=len(V)):
        a=dict(fix); a.update(zip(V,b)); z=Fraction(0)
        for sb in itertools.product((0,1),repeat=len(sumlegs)):
            aa=dict(a); aa.update(zip(sumlegs,sb)); z+=tv(**aa)
        D[b]=z
    return V,D
def prof(order,fix=None,sumlegs=()):
    V,D=tensor(fix,sumlegs); assert set(order)==set(V); out=[]
    for k in range(1,len(order)):
        A=order[:k]; B=[x for x in V if x not in A]; ia=[V.index(x) for x in A]; ib=[V.index(x) for x in B]; M=[]
        for a in itertools.product((0,1),repeat=len(A)):
            r=[]
            for b in itertools.product((0,1),repeat=len(B)):
                x=[None]*len(V)
                for j,z in zip(ia,a): x[j]=z
                for j,z in zip(ib,b): x[j]=z
                r.append(D[tuple(x)])
            M.append(r)
        out.append(rank(M))
    return out

class N:
    def __init__(self): self.k=0; self.e={}; self.d={}; self.ops=[]; self.names=[]
    def edge(self,n,d):
        if n in self.e: assert self.d[self.e[n]]==d; return self.e[n]
        x=self.k; self.k+=1; self.e[n]=x; self.d[x]=d; return x
    def add(self,n,I): self.names.append(n); self.ops.append(tuple(I))
def sig(j,k): return f"sig{j}_{k}"
def ph(j,i,x):
    if x=="s": return None if i==31 else sig(j,i)
    if x=="t": return None if i==0 else sig(j,i-1)
    if j==4: return {"u":f"u4_{i}","v":f"v4_{i}"}[x]
    if j==3: return {"u":f"u3_{i}","v":f"v3_{i}","w":f"v4_{(i+8)%32}"}[x]
    if j==2: return {"v":f"v4_{(i+8)%32}","w":f"w2_{i}"}[x]
    if j==1: return {"v":f"v3_{(i+12)%32}","w":f"u3_{i}"}[x]
def rs(j,i):
    if j==3: return [2,3,2] if i==0 else ([2,2,2] if i==31 else [2,3,3,2])
    return [2,2] if i==0 else ([1,1] if i==31 else [2,3,2])
def build(C):
    O={int(k[1:]):tuple(v) for k,v in C["local_orders"].items()}; B=N()
    for j in (4,3,2,1):
        for i in range(32):
            V=[x for x in O[j] if not(x=="t" and i==0) and not(x=="s" and i==31)]; R=rs(j,i); left=None
            for k,x in enumerate(V):
                I=[] if left is None else [left]; p=ph(j,i,x)
                if p is not None: I.append(B.edge(p,2))
                if k<len(V)-1:
                    right=B.edge(f"aux_j{j}_i{i}_k{k}",R[k]); I.append(right); left=right
                else: left=None
                B.add(f"J{j}_i{i}_c{k}_{x}",I)
    for i in range(32): B.add(f"P_i{i}",[B.edge(f"u4_{i}",2),B.edge(f"v3_{(i+12)%32}",2),B.edge(f"w2_{i}",2)])
    return B
def local(C):
    O={int(k[1:]):tuple(v) for k,v in C["local_orders"].items()}
    assert prof(O[3])==[2,3,3,2]
    for f,j in (("w",4),("u",2),("u",1)):
        for z in (0,1):
            assert prof(O[j],{f:z})==[2,3,2]
            assert prof(tuple(x for x in O[j] if x!="t"),{f:z},("t",))==[2,2]
            assert prof(tuple(x for x in O[j] if x!="s"),{f:z,"s":0})==[1,1]
    assert prof(tuple(x for x in O[3] if x!="t"),{},("t",))==[2,3,2]
    assert prof(tuple(x for x in O[3] if x!="s"),{"s":0})==[2,2,2]

def main():
    p=argparse.ArgumentParser(); p.add_argument("cert",nargs="?",default="research/v26/recovered-bit-puncturing-dac/V26_QR_MINIMAL_CORE_WIDTH41_CERTIFICATE.json"); a=p.parse_args()
    C=json.loads(Path(a.cert).read_text()); local(C); B=build(C); assert len(B.ops)==568
    inc=defaultdict(list)
    for v,I in enumerate(B.ops):
        for e in I:
            if B.d[e]>1: inc[e].append(v)
    E=[e for e,V in inc.items() if len(V)>1 and B.d[e]>1]
    Q=C["network_counts"]; assert (len(E),sum(B.d[e]==2 for e in E),sum(B.d[e]==3 for e in E),sum(len(inc[e])==2 for e in E),sum(len(inc[e])==3 for e in E))==(Q["indices_dim_gt_1"],Q["binary_indices"],Q["ternary_indices"],Q["degree2_indices"],Q["degree3_indices"])
    seen=[]; internal=0; maxd=1; maxn=0; maxc=None
    def bd(S):
        nonlocal maxd,maxn,maxc
        d=1;c=Counter()
        for e in E:
            V=inc[e]
            if any(v in S for v in V) and any(v not in S for v in V): d*=B.d[e]; c[B.d[e]]+=1
        if d>maxd: maxd,maxn,maxc=d,len(S),c
    def walk(x,root=False):
        nonlocal internal
        if isinstance(x,int): seen.append(x); bd({x}); return {x}
        internal+=1; A=walk(x[0]); D=walk(x[1]); assert A.isdisjoint(D); S=A|D
        if not root: bd(S)
        return S
    R=walk(C["certificate"]["tree"],True)
    assert R==set(range(568)) and len(seen)==568==len(set(seen)) and internal==567
    assert maxd==2**41==C["certificate"]["max_boundary_dimension"] and maxn==340 and maxc==Counter({2:41})
    print("PASS V26_QR_MINIMAL_CORE_WIDTH41_CERTIFICATE")
    print("tensor_vertices=568 internal_nodes=567 max_boundary_dimension=2^41 local_rank_profiles=PASS")
if __name__=="__main__": main()
