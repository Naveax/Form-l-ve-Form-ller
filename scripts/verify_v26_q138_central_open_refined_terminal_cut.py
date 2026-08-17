#!/usr/bin/env python3
import itertools,math,sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_minimal_core_width41 as M
import verify_v26_q138_double_round_leaf_ht95 as H

N=32
GEN_ORDER=('u','t','s','v','w')
T4_ORDER=('t','s','v','u')
INF=10**6

class Dinic:
    def __init__(self,n):self.g=[[] for _ in range(n)]
    def add(self,u,v,c):
        a=[v,c,None];b=[u,0,a];a[2]=b;self.g[u].append(a);self.g[v].append(b)
    def flow(self,s,t):
        ans=0
        while True:
            lev=[-1]*len(self.g);lev[s]=0;q=[s]
            for u in q:
                for v,c,r in self.g[u]:
                    if c and lev[v]<0:lev[v]=lev[u]+1;q.append(v)
            if lev[t]<0:return ans
            it=[0]*len(self.g)
            def dfs(u,f):
                if u==t:return f
                while it[u]<len(self.g[u]):
                    e=self.g[u][it[u]];v,c,r=e
                    if c and lev[v]==lev[u]+1:
                        z=dfs(v,min(f,c))
                        if z:e[1]-=z;r[1]+=z;return z
                    it[u]+=1
                return 0
            while True:
                z=dfs(s,INF)
                if not z:break
                ans+=z
    def reachable(self,s):
        seen={s};q=[s]
        for u in q:
            for v,c,r in self.g[u]:
                if c and v not in seen:seen.add(v);q.append(v)
        return seen

class Net:
    def __init__(self):self.factors={};self.indices={};self.dims={};self.k=0
    def factor(self,name):self.factors.setdefault(name,set());return name
    def index(self,name,dim=2):
        if name in self.dims:assert self.dims[name]==dim
        else:self.dims[name]=dim;self.indices[name]=set()
        return name
    def inc(self,f,x,dim=2):
        self.factor(f);self.index(x,dim);self.factors[f].add(x);self.indices[x].add(f)


def sig(j,i):return f'sig{j}_{i}'
def xor3(B,name,a,b,c):
    f='X_'+name
    for x in (a,b,c):B.inc(f,x,2)

def auxname(j,i,k):return f'aux_j{j}_i{i}_k{k}'


def legvar(j,i,x):
    if x=='t':return sig(j,i-1)
    if x=='s':return sig(j,i)
    if j==4:return {'u':f'u4_{i}','v':f'v4_{i}'}[x]
    if j==3:return {'u':f'u3_{i}','v':f'v3_{i}','w':f'v4_{(i+8)%N}'}[x]
    if j==2:
        return {'u':f'C_{i}','v':f'z2v_{i}','w':f'z2w_{i}'}[x]
    if j==1:
        return {'u':f'A_{i}','v':f'z1v_{i}','w':f'z1w_{i}'}[x]
    raise KeyError((j,i,x))


def add_tt(B,j,i):
    if j==4:
        order=T4_ORDER;fix={'w':1 if i==3 else 0}
    else:
        order=GEN_ORDER;fix={}
    sumlegs=()
    if i==0:sumlegs=('t',)
    if i==31:fix=dict(fix);fix['s']=0
    rem=tuple(x for x in order if x not in fix and x not in sumlegs)
    prof=M.prof(rem,fix,sumlegs)
    # Local profiles are exact ranks of the addition bit tensor under this order.
    if 0<i<31:
        if j==4:assert prof==[2,3,2],(j,i,prof)
        else:assert prof==[2,3,3,2],(j,i,prof)
    left=None
    for k,x in enumerate(rem):
        f=f'J{j}_{i}_{k}_{x}'
        if left is not None:B.inc(f,left,B.dims[left])
        B.inc(f,legvar(j,i,x),2)
        if k<len(rem)-1:
            d=prof[k];right=auxname(j,i,k);B.index(right,d);B.inc(f,right,d);left=right
        else:left=None


def build():
    B=Net()
    for j in (4,3,2,1):
        for i in range(N):add_tt(B,j,i)
    # Reduced backward-mask relations for fixed outputs Af=Cf=Df=0 and q7 fixed.
    # Constants are invertible relabelings and do not change graph/rank bounds.
    for i in range(N):
        xor3(B,f't2w_{i}',f'z2w_{i}',f'u4_{i}',f'v3_{(i+12)%N}')
        xor3(B,f't2v_{i}',f'z2v_{i}',f'v4_{(i+8)%N}',f'D_{(i+16)%N}')
        xor3(B,f't1w_{i}',f'z1w_{i}',f'u3_{i}',f'D_{i}')
        xor3(B,f't1v_{i}',f'z1v_{i}',f'v3_{(i+12)%N}',f'B_{i}')
    # External factors terminate the four open input-word mask bits at each site.
    for w in 'ABCD':
        for i in range(N):B.inc(f'EXT_{w}_{i}',f'{w}_{i}',2)
    # Internal non-TT variables should all be genuinely connected; physical D has
    # degree three because it participates locally and at offset16.
    for x,fs in B.indices.items():
        if x.startswith(('A_','B_','C_','D_')):assert any(f.startswith('EXT_') for f in fs)
        elif x.startswith('aux_'):assert len(fs)==2,(x,fs)
        else:assert len(fs)>=2,(x,fs)
    return B


def terminal_cut(B,S):
    # Safe binary-exponent capacities: dim2 ->1, dim3 ->2. Replacing dim3 by4
    # only enlarges the represented bond and therefore preserves an upper bound.
    node={};n=0
    def nid(key):
        nonlocal n
        if key not in node:node[key]=n;n+=1
        return node[key]
    SRC=nid(('SRC',));SNK=nid(('SNK',))
    for f in B.factors:nid(('F',f))
    for x in B.indices:nid(('Iin',x));nid(('Iout',x))
    D=Dinic(n)
    for x,dim in B.dims.items():
        cap=1 if dim==2 else 2
        D.add(nid(('Iin',x)),nid(('Iout',x)),cap)
    for f,xs in B.factors.items():
        u=nid(('F',f))
        for x in xs:
            D.add(u,nid(('Iin',x)),INF);D.add(nid(('Iout',x)),u,INF)
    S=set(S)
    for w in 'ABCD':
        for i in range(N):
            f=nid(('F',f'EXT_{w}_{i}'))
            if i in S:D.add(SRC,f,INF)
            else:D.add(f,SNK,INF)
    val=D.flow(SRC,SNK);reach=D.reachable(SRC)
    cut=[]
    for x,dim in B.dims.items():
        if nid(('Iin',x)) in reach and nid(('Iout',x)) not in reach:
            cut.append((x,dim,1 if dim==2 else 2))
    assert sum(c for x,d,c in cut)==val
    return val,cut


def maximizing_sets():
    root,nodes=H.walk(H.TREE,True);out=[]
    for S,g,c,l,t in nodes:
        if t==88:out.append(set(S))
    for i in range(N):
        S={i}
        if H.message_exponent(S)==88:out.append(S)
    # Current HT88 tree has exactly three maximizing clusters.
    uniq=[]
    for S in out:
        if S not in uniq:uniq.append(S)
    assert len(uniq)==3,[sorted(x) for x in uniq]
    return uniq


def main():
    B=build();sets=maximizing_sets();vals=[]
    for q,S in enumerate(sets,1):
        v,cut=terminal_cut(B,S);vals.append(v)
        print('partition',q,'size',len(S),'sites',sorted(S),'refined_binary_exponent_cut',v,flush=True)
        print('cut_dim_counts', {d:sum(1 for x,dd,c in cut if dd==d) for d in (2,3)}, 'cut_items',cut,flush=True)
    print('PASS V26_Q138_CENTRAL_OPEN_REFINED_TERMINAL_CUT')
    print('safe_refined_cut_exponents='+','.join(map(str,vals)))
    print('generic_physical_bound=44')
    print('best_safe_central_exponent='+str(max(vals)))
    print('NOTE dim3 TT bonds charged as two binary bits, so cuts are conservative exact upper bounds')

if __name__=='__main__':main()
