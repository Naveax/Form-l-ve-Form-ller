#!/usr/bin/env python3
import itertools
from collections import Counter, defaultdict, deque
from fractions import Fraction

S3={4,5,11,12,13,19,20,21,27,28,29}


def tv(s,t,u,v,w):
    if t!=(s^u^v^w) or not(s or u==v==w):return Fraction(0)
    return Fraction(-1 if ((u^w)&(v^w)) else 1,2**s)
def rankq(A):
    A=[[Fraction(x) for x in r] for r in A];m=len(A);n=len(A[0]);q=0
    for c in range(n):
        p=next((i for i in range(q,m) if A[i][c]),None)
        if p is None:continue
        A[q],A[p]=A[p],A[q];d=A[q][c];A[q]=[x/d for x in A[q]]
        for i in range(m):
            if i!=q and A[i][c]:
                z=A[i][c];A[i]=[A[i][j]-z*A[q][j] for j in range(n)]
        q+=1
        if q==m:break
    return q
def profile(order,fix=None,sumlegs=()):
    fix=dict(fix or {});alllegs=('s','t','u','v','w');V=[x for x in alllegs if x not in fix and x not in sumlegs];D={}
    for b in itertools.product((0,1),repeat=len(V)):
        a=dict(fix);a.update(zip(V,b));z=Fraction(0)
        for sb in itertools.product((0,1),repeat=len(sumlegs)):
            aa=dict(a);aa.update(zip(sumlegs,sb));z+=tv(**aa)
        D[b]=z
    assert set(order)==set(V);out=[]
    for k in range(1,len(order)):
        L=order[:k];R=[x for x in V if x not in L];il=[V.index(x) for x in L];ir=[V.index(x) for x in R];M=[]
        for l in itertools.product((0,1),repeat=len(L)):
            row=[]
            for r in itertools.product((0,1),repeat=len(R)):
                x=[None]*len(V)
                for j,z in zip(il,l):x[j]=z
                for j,z in zip(ir,r):x[j]=z
                row.append(D[tuple(x)])
            M.append(row)
        out.append(rankq(M))
    return out

class H:
    def __init__(self):
        self.factors=[];self.dim={};self.inc=defaultdict(list);self.term={}
    def factor(self,name,edges):
        f=len(self.factors);self.factors.append(name)
        for e,d in edges:
            if e in self.dim:assert self.dim[e]==d
            self.dim[e]=d;self.inc[e].append(f)
    def terminal(self,e,d,side):
        if e in self.dim:assert self.dim[e]==d
        self.dim[e]=d
        if e in self.term:assert self.term[e]==side
        self.term[e]=side

def J(j,x,i):return f'J{j}_{x}_{i}'
def sig(j,i):return f'sig{j}_{i}'
def ext(w,i):return f'{w}_{i}'

def add_addition(h,j):
    for i in range(32):
        if i==0:order=('u','s','v','w');r=(2,3,2)
        elif i==31:order=('u','t','v','w');r=(2,2,2)
        else:order=('u','t','s','v','w');r=(2,3,3,2)
        prev=None
        for k,x in enumerate(order):
            E=[]
            if prev is not None:E.append((prev,r[k-1]))
            if x in ('u','v','w'):E.append((J(j,x,i),2))
            elif x=='t':E.append((sig(j,i-1),2))
            else:E.append((sig(j,i),2))
            if k<len(order)-1:
                a=f'auxJ{j}_{i}_{k}';E.append((a,r[k]));prev=a
            else:prev=None
            h.factor(f'add{j}_{i}_{k}_{x}',E)
def parity(h,name,V):h.factor(name,[(x,2) for x in V])

def build():
    h=H()
    for j in (4,3,2,1):add_addition(h,j)
    for i in range(32):
        parity(h,f'R1_{i}',[J(4,'w',i),ext('Cout',i),ext('Bout',(i+7)%32)])
        parity(h,f'R2_{i}',[J(3,'w',i),ext('Aout',i),J(4,'v',(i+8)%32),ext('Dout',(i+8)%32)])
        parity(h,f'R3_{i}',[J(2,'v',i),J(4,'v',(i+8)%32),ext('Dout',(i+8)%32),ext('Din',(i+16)%32)])
        parity(h,f'R4_{i}',[J(2,'w',i),J(4,'u',i),J(3,'v',(i+12)%32),ext('Bout',(i+19)%32)])
        parity(h,f'R5_{i}',[J(1,'u',i),ext('Ain',i)])
        parity(h,f'R6_{i}',[J(1,'v',i),J(3,'v',(i+12)%32),ext('Bin',i),ext('Bout',(i+19)%32)])
        parity(h,f'R7_{i}',[J(1,'w',i),J(3,'u',i),ext('Din',i)])
        parity(h,f'R8_{i}',[J(2,'u',i),ext('Cin',i)])
    for w in ('Ain','Bin','Cin','Din','Aout','Bout','Cout','Dout'):
        for i in range(32):h.terminal(ext(w,i),2,int(i in S3))
    return h

class Dinic:
    def __init__(self,n):self.g=[[] for _ in range(n)]
    def add(self,u,v,c):
        self.g[u].append([v,c,len(self.g[v])]);self.g[v].append([u,0,len(self.g[u])-1])
    def flow(self,s,t):
        ans=0;INF=10**18
        while True:
            lv=[-1]*len(self.g);lv[s]=0;q=deque([s])
            while q:
                u=q.popleft()
                for v,c,r in self.g[u]:
                    if c and lv[v]<0:lv[v]=lv[u]+1;q.append(v)
            if lv[t]<0:break
            it=[0]*len(self.g)
            def dfs(u,f):
                if u==t:return f
                while it[u]<len(self.g[u]):
                    e=self.g[u][it[u]];v,c,r=e
                    if c and lv[v]==lv[u]+1:
                        z=dfs(v,min(f,c))
                        if z:
                            e[1]-=z;self.g[v][r][1]+=z;return z
                    it[u]+=1
                return 0
            while True:
                z=dfs(s,INF)
                if not z:break
                ans+=z
        seen={s};q=deque([s])
        while q:
            u=q.popleft()
            for v,c,r in self.g[u]:
                if c and v not in seen:seen.add(v);q.append(v)
        return ans,seen

def mincut(h):
    # Unit-cost hypergraph cut gives a rigorous lower bound on the true log2-dimension cut,
    # because every nontrivial index has dimension at least2. Standard directed reduction:
    # for hyperedge e, source-side incidence forces e_in source; sink-side incidence forces
    # e_out sink; the only finite arc e_in->e_out costs one if the hyperedge is split.
    edges=list(h.dim);F=len(h.factors);SRC=F+2*len(edges);SNK=SRC+1;D=Dinic(SNK+1);INF=10**6
    for k,e in enumerate(edges):
        a=F+2*k;b=a+1;D.add(a,b,1)
        ent=list(h.inc[e])
        if e in h.term:ent.append(SRC if h.term[e] else SNK)
        for v in ent:D.add(v,a,INF);D.add(b,v,INF)
    val,reach=D.flow(SRC,SNK);assert val==86,val
    cut=[]
    for k,e in enumerate(edges):
        a=F+2*k;b=a+1
        if a in reach and b not in reach:cut.append(e)
    assert len(cut)==86
    assert Counter(h.dim[e] for e in cut)==Counter({2:86})
    # Lower bound: every real log2(dim) cut costs >= its number of split hyperedges >=86.
    # Upper bound: this exact unit min-cut uses only binary edges, so its real cost is exactly86.
    return cut

def main():
    assert profile(('u','t','s','v','w'))==[2,3,3,2]
    assert profile(('u','s','v','w'),{},('t',))==[2,3,2]
    assert profile(('u','t','v','w'),{'s':0})==[2,2,2]
    h=build()
    assert len(h.factors)==888
    assert len(h.dim)==1268
    assert Counter(h.dim.values())==Counter({2:1024,3:244})
    assert len(h.term)==256 and all(h.inc[e] for e in h.term)
    mincut(h)
    print('PASS V26_Q138_FULLY_OPEN_REFINED_S3_CUT86')
    print('factors=888 indices=1268 binary=1024 ternary=244 external_terminals=256')
    print('unit_hypergraph_mincut=86; witness_cut=86_binary => exact log2_dimension_mincut=86')
    print('known_fused_common_tree_cap=65; refined minimal-TT opening does not improve the slope cap')
    print('scope=scoped refined-hypergraph topology falsifier, not a lower bound on true Walsh Schmidt rank')
if __name__=='__main__':main()
