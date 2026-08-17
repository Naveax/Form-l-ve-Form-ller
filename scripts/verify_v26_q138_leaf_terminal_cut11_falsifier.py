#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_leaf_ht95 as H

N=32
INF=10**6

class D:
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

def edge_list():
    E=[]
    for i in range(N-1):E.append((i,i+1,4))
    for r in (8,12):
        seen=set()
        for i in range(N):
            j=(i+r)%N;e=tuple(sorted((i,j)))
            if e in seen:continue
            seen.add(e);E.append((e[0],e[1],1))
    return E
E=edge_list()

def terminal_cut(S):
    # One physical open output bit per site, plus reduced exact leaf site graph.
    SRC=N;SNK=N+1;din=D(N+2)
    for u,v,w in E:
        din.add(u,v,w);din.add(v,u,w)
    S=set(S)
    for i in range(N):
        # terminal edge of capacity1 represents the one open output-word bit
        if i in S:din.add(SRC,i,1)
        else:din.add(i,SNK,1)
    return din.flow(SRC,SNK)

def critical_sets():
    root,nodes=H.walk(H.TREE,True);out=[]
    for rec in nodes:
        S=rec[0]
        # HT88 critical sets are 11/21 and had final exponent88.
        if H.message_exponent(S)==88:out.append(set(S))
    uniq=[]
    for S in out:
        if S not in uniq:uniq.append(S)
    assert len(uniq)==3
    return uniq

def main():
    vals=[]
    for q,S in enumerate(critical_sets(),1):
        v=terminal_cut(S);vals.append(v)
        assert v==min(len(S),N-len(S))==11,(q,v,S)
        print('partition',q,'size',len(S),'sites',sorted(S),'leaf_terminal_cut',v)
    print('PASS V26_Q138_LEAF_TERMINAL_CUT11_FALSIFIER')
    print('critical_leaf_cuts=11,11,11 generic_physical_rank_exponent=11')
    print('consequence=reduced leaf topology cannot improve the generic 2^11 rank bound on HT88 critical partitions')
    print('next_required_object=actual coefficient Schmidt rank for the specified fixed leaf input mask')
if __name__=='__main__':main()
