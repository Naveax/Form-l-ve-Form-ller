#!/usr/bin/env python3
import math,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed84_multisite as M96
import verify_v26_q138_double_round_factor_generation85 as F

P=1000003

def rank_mod(A,p=P):
    A=np.array(A,dtype=np.int64,copy=True)%p;m,n=A.shape;q=0
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

def gram_generic_pair():
    Ws={(b,d):M96.buildW(b,d) for b in (0,1) for d in (0,1)}
    G=np.zeros((256,256),dtype=np.int64)
    dp=np.array([((r&1)<<1)|(s&1) for r in range(16) for s in range(16)])
    # Generic adjacent S1 pair sites4,5; complement sites20,21. q138 b0=0 on all.
    for q0 in (0,1):
      for q1 in (0,1):
        GM=M96.main_pair_gram(Ws,0,0,q0,q1)
        GC=M96.comp_pair_gram(Ws,q0,q1)
        G += GM*GC[dp[:,None],dp[None,:]]
    return G

def rank_q_dense(M):
    A=[[Fraction(int(x)) for x in row] for row in M];m=len(A);n=len(A[0]);q=0
    for c in range(n):
        p=next((i for i in range(q,m) if A[i][c]),None)
        if p is None:continue
        A[q],A[p]=A[p],A[q];d=A[q][c]
        for j in range(c,n):A[q][j]/=d
        for i in range(m):
            if i!=q and A[i][c]:
                a=A[i][c]
                for j in range(c,n):A[i][j]-=a*A[q][j]
        q+=1
        if q==m:break
    return q

def physical_basis_coordinates(G):
    # Exact echelon basis made from actual physical Gram rows. Keep normalized
    # basis row and its expression in selected physical rows.
    B={};E={};selected=[]
    for i,row0 in enumerate(G):
        r=[Fraction(int(x)) for x in row0];expr={i:Fraction(1)}
        for c in sorted(B):
            if r[c]:
                a=r[c];br=B[c];er=E[c]
                for j in range(c,len(r)):r[j]-=a*br[j]
                for j,x in er.items():
                    z=expr.get(j,Fraction(0))-a*x
                    if z:expr[j]=z
                    elif j in expr:expr.pop(j)
        p=next((j for j,x in enumerate(r) if x),None)
        if p is not None:
            d=r[p]
            for j in range(p,len(r)):r[j]/=d
            expr={j:x/d for j,x in expr.items()}
            B[p]=r;E[p]=expr;selected.append(i)
    assert len(selected)==208
    # Second pass: express every physical row in selected physical rows.
    supports=[];coeffs=set()
    for row0 in G:
        r=[Fraction(int(x)) for x in row0];co={}
        for c in sorted(B):
            if r[c]:
                a=r[c];br=B[c];er=E[c]
                for j in range(c,len(r)):r[j]-=a*br[j]
                for j,x in er.items():co[j]=co.get(j,Fraction(0))+a*x
        assert not any(r)
        co={j:x for j,x in co.items() if x}
        supports.append(len(co));coeffs.update(co.values())
    return selected,supports,coeffs

def main():
    # Dependency rank96 block is independently rechecked by its own workflow;
    # here use its exact value in the product and verify the new disjoint block.
    G=gram_generic_pair();assert G.shape==(256,256)
    assert rank_mod(G)==208
    assert rank_q_dense(G)==208
    sel,supp,coeff=physical_basis_coordinates(G)
    assert len(sel)==208
    assert Counter(supp)==Counter({1:208,3:48}),Counter(supp)
    assert coeff=={Fraction(-1),Fraction(1)},coeff

    R=16*2784*96*208*(2**10)
    assert R==3393*(2**28)
    table=R*(2**44);assert table==3393*(2**72)
    exp=math.log2(table)
    assert abs(exp-(72+math.log2(3393)))<1e-12

    # The factor-generation complement tree stays at80, below the table size.
    root,sets=F.walk(F.RIGHT_TREE,True);assert root==F.COMP
    peak=max(F.ccost(A) for A in sets+[{i} for i in F.COMP]);assert peak==80
    assert peak<exp

    print('PASS V26_Q138_DOUBLE_ROUND_SIGNED83_TWOFACTOR')
    print('generic_four_site_block={4,5,20,21} exact_rank=208/256')
    print('physical_basis_rows=208 dependent_rows=48 each_dependency_support=3 coefficients=+-1')
    print('combined_S1_rank<=16*2784*96*208*2^10=3393*2^28')
    print('two_factor_materialized_dimension=3393*2^72 log2=%.15f' % exp)
    print('right_entry_generation_peak=80')
    print('W_repr_and_factor_gen<=%.15f' % exp)
    print('scope=exact S1-root two-factor representation/materialized-factor upper bound; no arithmetic-work or optimality claim')
if __name__=='__main__':main()
