#!/usr/bin/env python3
import itertools, random, sys
from collections import deque
from pathlib import Path
import numpy as np
import opt_einsum as oe

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_leaf_fullrank_witness as W

P=251
N=32
BASE_S1={0,1,2,3,4,5,12,13,14,15,16}

class Dinic:
    def __init__(self,n): self.g=[[] for _ in range(n)]
    def add(self,u,v,c,tag=None):
        a=[v,c,None,tag,c]; b=[u,0,a,None,0]; a[2]=b
        self.g[u].append(a); self.g[v].append(b)
    def flow(self,s,t):
        ans=0
        while True:
            lev=[-1]*len(self.g); lev[s]=0; q=deque([s])
            while q:
                u=q.popleft()
                for e in self.g[u]:
                    if e[1] and lev[e[0]]<0:
                        lev[e[0]]=lev[u]+1; q.append(e[0])
            if lev[t]<0: return ans
            it=[0]*len(self.g)
            def dfs(u,f):
                if u==t:return f
                while it[u]<len(self.g[u]):
                    e=self.g[u][it[u]]
                    if e[1] and lev[e[0]]==lev[u]+1:
                        z=dfs(e[0],min(f,e[1]))
                        if z:
                            e[1]-=z; e[2][1]+=z; return z
                    it[u]+=1
                return 0
            while True:
                z=dfs(s,10**9)
                if not z:break
                ans+=z

def edge_list():
    E=[]
    for i in range(N-1): E.append((i,i+1,4))
    for r in (8,12):
        seen=set()
        for i in range(N):
            j=(i+r)%N; e=tuple(sorted((i,j)))
            if e in seen:continue
            seen.add(e); E.append((e[0],e[1],1))
    return E
E=edge_list()

def flow_complement_terminals(S):
    S=set(S); src=N; snk=N+1; d=Dinic(N+2); sink={}
    for u,v,w in E:
        d.add(u,v,w); d.add(v,u,w)
    for i in range(N):
        if i in S:d.add(src,i,1)
        else:
            d.add(i,snk,1,('sink',i)); sink[i]=d.g[i][-1]
    assert d.flow(src,snk)==11
    T=[i for i,e in sink.items() if e[4]-e[1]]
    assert len(T)==11 and set(T).isdisjoint(S)
    return T

def fix_closed_outputs(A,ls,openbits):
    ls=list(ls); A=A
    for ax in range(len(ls)-1,-1,-1):
        x=ls[ax]
        if x.startswith('out_') and int(x.split('_')[1]) not in openbits:
            A=np.take(A,0,axis=ax); ls.pop(ax)
    return A,ls

def single_network(words,pos,openbits):
    raw=[]
    for j in (4,3,2,1):
        for i in range(N):
            A,ls=W.add_factor(j,i,words,pos,'m')
            A,ls=fix_closed_outputs(A,ls,openbits)
            raw.append((A,ls))
    opens={f'out_{i}' for i in openbits}
    return W.normalize_edges(raw,opens),opens

def contraction_path(factors,outlabs):
    ids={}; q=0
    for A,ls in factors:
        for x in ls:
            if x not in ids:ids[x]=q;q+=1
    args=[]
    for A,ls in factors:args.extend([A,[ids[x] for x in ls]])
    args.append([ids[x] for x in outlabs])
    path,info=oe.contract_path(*args,optimize='greedy')
    return ids,path,info

def execute(factors,outlabs,ids,path):
    work=[(A,[ids[x] for x in ls]) for A,ls in factors]
    for step in path:
        assert len(step)==2,step
        i,j=sorted(step,reverse=True); B,lb=work.pop(i); A,la=work.pop(j)
        sb=set(lb); common=[x for x in la if x in sb]
        axa=[la.index(x) for x in common]; axb=[lb.index(x) for x in common]
        C=np.tensordot(A,B,axes=(axa,axb))%P
        lc=[x for x in la if x not in common]+[x for x in lb if x not in common]
        work.append((C,lc))
    assert len(work)==1
    A,ls=work[0]; target=[ids[x] for x in outlabs]
    A=np.transpose(A,[ls.index(x) for x in target])%P
    return A.reshape(1<<11,1<<11)

def rank_mod(M):
    from flint import nmod_mat
    return nmod_mat(M.tolist(),P).rank()

def candidates():
    rng=random.Random(138)
    return [tuple(rng.getrandbits(32) for _ in range(4)) for __ in range(4)]

def main():
    found={}
    for pos in 'ABCD':
        shift=7 if pos=='B' else 0
        S={(i+shift)%32 for i in BASE_S1}
        T=flow_complement_terminals(S)
        outlabs=[f'out_{i}' for i in sorted(S)]+[f'out_{i}' for i in T]
        print('position',pos,'S',sorted(S),'T',T,flush=True)
        for ci,words in enumerate(candidates()):
            fac,_=single_network(words,pos,S|set(T))
            ids,path,info=contraction_path(fac,outlabs)
            print('candidate',ci,'largest_intermediate',info.largest_intermediate,flush=True)
            M=execute(fac,outlabs,ids,path)
            r=rank_mod(M)
            print('candidate',ci,'rank',r,'words='+','.join(hex(x) for x in words),flush=True)
            if r==2048:
                found[pos]=(ci,words,T); break
    print('summary_found='+repr({k:(v[0],v[2]) for k,v in found.items()}),flush=True)
    if len(found)==4:
        print('PASS V26_Q138_LEAF_S1_MINOR_PROBE fullrank2048 all positions',flush=True)
    else:
        print('INCOMPLETE V26_Q138_LEAF_S1_MINOR_PROBE positions='+''.join(sorted(found)),flush=True)

if __name__=='__main__':main()
