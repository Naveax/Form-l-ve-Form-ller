#!/usr/bin/env python3
import itertools,sys
from array import array
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import probe_v26_q138_predecessor_leaf_ad_input_activity as P


def canonical_input_rows(can):
    rows=list(can);r=0
    for col in range(128,160):
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    eq=[]
    for row in rows[r:]:
        m=row&((1<<128)-1);rhs=(row>>160)&1
        if m or rhs:eq.append((m,rhs))
    rr=[m|(rhs<<128) for m,rhs in eq];q=0
    for col in range(128):
        p=next((k for k in range(q,len(rr)) if (rr[k]>>col)&1),None)
        if p is None:continue
        rr[q],rr[p]=rr[p],rr[q]
        for k in range(len(rr)):
            if k!=q and ((rr[k]>>col)&1):rr[k]^=rr[q]
        q+=1
    for row in rr[q:]:
        assert (row&((1<<128)-1))!=0 or ((row>>128)&1)==0
    return tuple(rr[:q])


def build_global_basis(conds):
    B={};q=0
    for cond in conds:
        for row in cond:
            x=row&((1<<128)-1)
            while x:
                p=x.bit_length()-1
                if p not in B:
                    B[p]=(x,q);q+=1;break
                x^=B[p][0]
    return B,q


def express(x,B):
    c=0
    while x:
        p=x.bit_length()-1
        assert p in B
        v,i=B[p];x^=v;c^=1<<i
    return c


def quotient_condition(cond,B,q):
    eq=[]
    for row in cond:
        m=row&((1<<128)-1);rhs=(row>>128)&1
        eq.append((express(m,B),rhs))
    sol=T.rref(eq,n=q);assert sol is not None
    return sol


def enumerate_affine(x0,basis,counts):
    d=len(basis);p=x0;prev=0
    counts[p]+=1
    for k in range(1,1<<d):
        g=k^(k>>1);diff=g^prev
        j=(diff&-diff).bit_length()-1
        p^=basis[j];counts[p]+=1;prev=g


def main():
    for pos in 'AD':
        objs=P.affine_supports(pos)
        conds=[canonical_input_rows(can) for _,_,can in objs]
        assert len(conds)==(271 if pos=='A' else 274)
        B,q=build_global_basis(conds)
        print('position',pos,'global_input_functional_span_rank',q)
        sols=[quotient_condition(c,B,q) for c in conds]
        free_dist={}
        for rank,x0,basis in sols:free_dist[len(basis)]=free_dist.get(len(basis),0)+1
        print('position',pos,'quotient_free_dimension_distribution',free_dist)
        if q<=26:
            counts=array('H',[0])*(1<<q)
            for rank,x0,basis in sols:enumerate_affine(x0,basis,counts)
            mx=max(counts);num=sum(v==mx for v in counts)
            hist={}
            for v in counts:hist[v]=hist.get(v,0)+1
            nz={k:v for k,v in sorted(hist.items()) if k}
            print('position',pos,'EXACT_affine_activity_max',mx,'maximizer_count',num,
                  'nonzero_activity_hist',nz)
        else:
            print('position',pos,'exact_enumeration_skipped_q_gt_26')
    print('PASS PROBE V26_Q138_AD_INPUT_ACTIVITY_QUOTIENT')
    print('scope=quotient geometry; exact max only when enumeration executed')

if __name__=='__main__':main()
