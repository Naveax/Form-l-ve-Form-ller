#!/usr/bin/env python3
import random,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_leaf_ht95 as H

N=32
BASE=H.TREE

def leaves(t):return [t] if isinstance(t,int) else leaves(t[0])+leaves(t[1])
def clusters(t,root=True):
    if isinstance(t,int):return {t},[]
    A,a=clusters(t[0],False);B,b=clusters(t[1],False);S=A|B
    return S,a+b+([] if root else [S])
SHAPE_LEAVES=leaves(BASE);assert sorted(SHAPE_LEAVES)==list(range(N))
_,BASE_CLUSTERS=clusters(BASE,True)
# Represent each cluster by positions in the base-tree leaves.
pos={v:i for i,v in enumerate(SHAPE_LEAVES)}
CPOS=[tuple(sorted(pos[x] for x in S)) for S in BASE_CLUSTERS]

def edges():
    E=[]
    for i in range(N-1):E.append((i,i+1,4))
    for r in (7,8,12,16):
        seen=set()
        for i in range(N):
            j=(i+r)%N;e=tuple(sorted((i,j)))
            if e in seen:continue
            seen.add(e);E.append((e[0],e[1],1))
    return E
E=edges()
def bd(S):
    S=set(S);return sum(w for u,v,w in E if (u in S)!=(v in S))
def cost_perm(p):
    vals=[]
    for C in CPOS:
        S={p[i] for i in C};m=min(len(S),N-len(S));vals.append(min(bd(S),8*m))
    # include singleton clusters too
    for x in p:vals.append(min(bd({x}),8))
    vals.sort(reverse=True)
    return tuple(vals[:12])
def apply_perm(t,p):
    # p indexed by base-tree leaf-position
    mp={v:p[pos[v]] for v in range(N)}
    return mp[t] if isinstance(t,int) else [apply_perm(t[0],p),apply_perm(t[1],p)]

def main():
    rng=random.Random(13888067)
    # Start from current depth-law permutation if available.
    starts=[list(range(N)),[17,1,0,15,18,8,3,6,30,31,22,5,2,25,9,10,16,19,12,27,26,11,21,28,20,14,13,29,24,4,23,7]]
    best=None;bp=None
    for s in starts:
        c=cost_perm(s)
        if best is None or c<best:best,bp=c,s[:]
    print('start_best',best[0],best,bp,flush=True)
    # Multi-restart stochastic swap descent with occasional annealing acceptance.
    for restart in range(20):
        p=bp[:] if restart<5 else rng.sample(range(N),N);c=cost_perm(p);T=4.0
        for it in range(25000):
            i,j=rng.sample(range(N),2);p[i],p[j]=p[j],p[i];nc=cost_perm(p)
            delta=nc[0]-c[0]
            accept=nc<c or (delta<=2 and rng.random()<math.exp(-max(0,delta)/max(T,0.05))*0.02)
            if accept:c=nc
            else:p[i],p[j]=p[j],p[i]
            T*=0.9998
            if c<best:
                best,bp=c,p[:];print('improve',restart,it,'max',best[0],'score',best,'perm',bp,flush=True)
        # deterministic adjacent/all-pair hill descent
        changed=True
        while changed:
            changed=False
            for i in range(N):
                for j in range(i+1,N):
                    p[i],p[j]=p[j],p[i];nc=cost_perm(p)
                    if nc<c:c=nc;changed=True
                    else:p[i],p[j]=p[j],p[i]
            if c<best:best,bp=c,p[:];print('hill_improve',restart,best,bp,flush=True)
    tree=apply_perm(BASE,bp);_,sets=clusters(tree,True)
    exact=max([min(bd(S),8*min(len(S),N-len(S))) for S in sets]+[min(bd({i}),8) for i in range(N)])
    assert exact==best[0]
    print('PASS SEARCH V26_Q138_FULLY_OPEN_COMMON_TREE')
    print('best_found_max='+str(exact))
    print('best_found_score='+repr(best))
    print('permutation='+repr(bp))
    print('tree='+repr(tree))
    print('scope=heuristic search, exact verification of returned tree, no optimality claim')
if __name__=='__main__':main()
