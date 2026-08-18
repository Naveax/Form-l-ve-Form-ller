#!/usr/bin/env python3
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I

MASK=(1<<128)-1


def reduce_full(row,basis):
    y=row
    for p in sorted(basis, reverse=True):
        if (y>>p)&1:y ^= basis[p]
    return y


def insert_affine(basis,row):
    y=reduce_full(row,basis)
    m=y&MASK
    if not m:return False, ((y>>128)&1)==0, y
    basis[m.bit_length()-1]=y
    return True,True,y


def build_affine(rows):
    B={}
    for r in rows:
        _new,ok,_y=insert_affine(B,r)
        if not ok:return None
    return B


def residual_basis(core_basis,cond):
    B=dict(core_basis);R=[]
    for r in cond:
        new,ok,y=insert_affine(B,r)
        if not ok:return None
        if new:R.append(y)
    return tuple(R)


def span_full(rows):
    out=[0]
    for r in rows:out += [x^r for x in out[:]]
    return tuple(out)


def groups_for(pos):
    raw,_=P.direct_supports(pos)
    C=Counter(can for _t,_z,can in raw)
    odd=[can for can,n in C.items() if n&1]
    G=defaultdict(list)
    for can in odd:
        cond=P.canonical_condition(I.input_condition(can))
        G[cond].append(can)
    return list(G)


def gf2_mask_rank(masks):
    B={};r=0
    for m in masks:
        y=m
        for p in sorted(B,reverse=True):
            if (y>>p)&1:y^=B[p]
        if y:
            B[y.bit_length()-1]=y;r+=1
    return r


def coverage_greedy(group_mask_spans,Kmax):
    reps=[set(s) for s in group_mask_spans]
    selected=[];gains=[]
    for k in range(Kmax):
        cnt=Counter()
        for S in reps:
            for v in S:
                if v:cnt[v]+=1
        if not cnt:break
        v,gain=cnt.most_common(1)[0]
        selected.append(v);gains.append(gain)
        p=v.bit_length()-1
        new=[]
        for S in reps:
            T={x^v if ((x>>p)&1) else x for x in S}
            new.append(T)
        reps=new
        print('greedy_step',k+1,'coverage_gain_groups',gain,
              'remaining_total_projected_span_cells',sum(len(S) for S in reps),flush=True)
    return selected,gains


def coordinate_basis(masks):
    B={};n=0
    for m in masks:
        y=m;c=1<<n
        for p in sorted(B,reverse=True):
            if (y>>p)&1:
                v,cc=B[p];y^=v;c^=cc
        assert y
        B[y.bit_length()-1]=(y,c);n+=1
    return B


def coord_if_member(m,B):
    y=m;c=0
    for p in sorted(B,reverse=True):
        if (y>>p)&1:
            v,cc=B[p];y^=v;c^=cc
    return c if y==0 else None


def fwht_inplace(a):
    n=len(a);h=1
    while h<n:
        M=a.reshape(-1,2*h)
        x=M[:,:h].copy();y=M[:,h:]
        M[:,:h]=x+y
        M[:,h:]=x-y
        h*=2


def exact_bucket_max(group_full_spans,selected,K):
    Q=coordinate_basis(selected[:K])
    n=1<<K
    spec=np.zeros(n,dtype=np.int64)
    idist=Counter()
    for full in group_full_spans:
        inter=[]
        for row in full:
            ell=coord_if_member(row&MASK,Q)
            if ell is not None:inter.append((ell,(row>>128)&1))
        size=len(inter)
        assert size and size&(size-1)==0
        s=size.bit_length()-1
        idist[s]+=1
        weight=1<<(K-s)
        for ell,rhs in inter:spec[ell] += -weight if rhs else weight
    fwht_inplace(spec)
    denom=1<<K
    assert np.all(spec % denom == 0)
    vals=spec//denom
    assert np.all(vals>=0)
    arg=int(np.argmax(vals));mx=int(vals[arg])
    return mx,arg,idist,int(vals.min()),int(vals.max()),int(vals.sum())


def main():
    for pos in 'AD':
        groups=groups_for(pos)
        core_k=6 if pos=='A' else 5
        expected={'A':4531,'D':8629}[pos]
        assert len(groups)==expected
        freq=Counter(r for cond in groups for r in cond)
        core=[r for r,_ in freq.most_common(core_k)]
        core_basis=build_affine(core);assert core_basis is not None

        Rlist=[];full=[];maskspans=[];rd=Counter();bad=0
        allm=[]
        for cond in groups:
            R=residual_basis(core_basis,cond)
            if R is None:
                bad+=1;continue
            rd[len(R)]+=1;Rlist.append(R)
            F=span_full(R);full.append(F)
            S={row&MASK for row in F};maskspans.append(S);allm.extend(S)
        q=gf2_mask_rank(allm)
        print('position',pos,'certified_core_rank',core_k,
              'compatible_groups',len(Rlist),'incompatible_groups',bad,
              'residual_rank_distribution',dict(sorted(rd.items())),
              'full_residual_dual_span_rank',q,flush=True)

        selected,gains=coverage_greedy(maskspans,20)
        print('position',pos,'coverage_greedy_gains',gains,
              'selected_rank',gf2_mask_rank(selected),flush=True)
        for K in (4,8,12,16,20):
            if K>len(selected):continue
            mx,arg,idist,mn,mx2,total=exact_bucket_max(full,selected,K)
            assert mx==mx2
            print('position',pos,'K',K,'coverage_greedy_exact_FWHT_upper',mx,
                  'arg_signature',arg,
                  'group_intersection_dimension_distribution',dict(sorted(idist.items())),
                  'bucket_min',mn,'bucket_sum',total,flush=True)
        print('position',pos,'scope_note=every global active-count maximizer lies in the certified common core; each FWHT bucket maximum is therefore a rigorous global upper')
    print('PASS PROBE V26_Q138_AD_THIRD_COVERAGE_GREEDY_FWHT')
    print('scope=direct-e2 active-condition group-count upper envelopes; inherited e1 corrections remain separate')

if __name__=='__main__':main()
