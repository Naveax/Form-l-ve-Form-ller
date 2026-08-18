#!/usr/bin/env python3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T

MASK=(1<<128)-1
RHSBIT=1<<128


def reduce_full(row,basis):
    y=row
    for p in sorted(basis, reverse=True):
        if (y>>p)&1:y ^= basis[p]
    return y


def insert_row(basis,row):
    y=reduce_full(row,basis)
    m=y&MASK
    if not m:
        return False, ((y>>128)&1)==0, y
    p=m.bit_length()-1
    basis[p]=y
    return True, True, y


def build_basis(rows):
    B={}
    for r in rows:
        new,ok,_=insert_row(B,r)
        if not ok:return None
    return B


def residual_basis(node_basis,cond):
    B=dict(node_basis);R=[]
    for r in cond:
        new,ok,y=insert_row(B,r)
        if not ok:return None
        if new:R.append(y)
    return tuple(R)


def span_rows(rows):
    out=[]
    for bits in range(1,1<<len(rows)):
        z=0
        b=bits;j=0
        while b:
            if b&1:z^=rows[j]
            b>>=1;j+=1
        out.append(z)
    return out


def groups_for(pos):
    raw,_=P.direct_supports(pos)
    C=Counter(can for _t,_z,can in raw)
    odd=[can for can,n in C.items() if n&1]
    G=defaultdict(list)
    for can in odd:
        cond=P.canonical_condition(I.input_condition(can))
        G[cond].append(can)
    return list(G)


def select_masks(mask_counts,node_basis,kmax=12):
    cand=[]
    for m,c in mask_counts.items():
        n0=c[0];n1=c[1]
        if n0 and n1:
            cand.append((min(n0,n1),n0+n1,max(n0,n1),m,n0,n1))
    cand.sort(reverse=True)
    sel=[];B={}
    for score,total,mx,m,n0,n1 in cand:
        y=reduce_full(m,B)&MASK
        if not y:continue
        p=y.bit_length()-1;B[p]=y
        sel.append((m,score,total,n0,n1))
        if len(sel)>=kmax:break
    return cand,sel


def combo_masks(masks):
    K=len(masks);C=[0]*(1<<K)
    for s in range(1,1<<K):
        l=s&-s;j=l.bit_length()-1
        C[s]=C[s^l]^masks[j]
    return C


def bucket_upper(group_implied,selected,K):
    masks=[x[0] for x in selected[:K]]
    combos=combo_masks(masks)
    inv={m:s for s,m in enumerate(combos)}
    assert len(inv)==1<<K
    buckets=[0]*(1<<K)
    rankdist=Counter();allowed_size_dist=Counter()
    for imp in group_implied:
        eq=[]
        for row in imp:
            m=row&MASK
            ell=inv.get(m)
            if ell is not None and ell:
                eq.append((ell,(row>>128)&1))
        sol=T.rref(eq,n=K)
        assert sol is not None
        rank,x0,basis=sol
        rankdist[rank]+=1;allowed_size_dist[1<<len(basis)]+=1
        vals=[x0]
        for d in basis:
            vals += [v^d for v in vals[:]]
        assert len(vals)==1<<(K-rank)
        for s in vals:buckets[s]+=1
    mx=max(buckets);arg=buckets.index(mx)
    return mx,arg,rankdist,allowed_size_dist,Counter(buckets)


def main():
    for pos in 'AD':
        groups=groups_for(pos);N=len(groups)
        freq=Counter(r for cond in groups for r in cond)
        top=[r for r,_ in freq.most_common(5)]
        node_basis=build_basis(top);assert node_basis is not None and len(node_basis)==5

        residuals=[];implied=[];mask_counts=defaultdict(lambda:[0,0])
        incompatible=0;rd=Counter()
        for cond in groups:
            R=residual_basis(node_basis,cond)
            if R is None:
                incompatible+=1;continue
            rd[len(R)]+=1;residuals.append(R)
            imp=span_rows(R);implied.append(imp)
            seen=set()
            for row in imp:
                m=row&MASK;rhs=(row>>128)&1
                assert m and m not in seen
                seen.add(m);mask_counts[m][rhs]+=1

        U=len(residuals)
        cand,selected=select_masks(mask_counts,node_basis,12)
        print('position',pos,'global_groups',N,'V5_compatible_groups',U,
              'V5_incompatible_groups',incompatible,
              'V5_residual_rank_distribution',dict(sorted(rd.items())),
              'distinct_implied_linear_masks',len(mask_counts),flush=True)
        print('position',pos,'top_balanced_implied_masks',
              [(a,b,c,d,e) for a,b,c,_m,d,e in cand[:20]],flush=True)
        print('position',pos,'selected_independent_masks',
              [(score,total,n0,n1) for _m,score,total,n0,n1 in selected],flush=True)
        if not selected:
            print('position',pos,'NO_BALANCED_MASKS',flush=True);continue
        for K in [k for k in (1,2,4,6,8,10,12) if k<=len(selected)]:
            mx,arg,rankdist,asizedist,bdist=bucket_upper(implied,selected,K)
            print('position',pos,'K',K,'exact_signature_bucket_upper',mx,
                  'arg_signature',arg,
                  'group_projection_constraint_rank_distribution',dict(sorted(rankdist.items())),
                  'group_allowed_signature_count_distribution',dict(sorted(asizedist.items())),
                  'bucket_count_minmax',(min(bdist),max(bdist)),flush=True)
        print('position',pos,'scope_note=global maximizer lies in V5 by clean common-core forcing theorem; signature bucket maximum is therefore a uniform active-group upper')
    print('PASS PROBE V26_Q138_AD_THIRD_V5_SIGNATURE_ENVELOPE')
    print('scope=active rank-one condition-group upper envelopes for direct-e2; inherited e1 correction remains separate')

if __name__=='__main__':main()
