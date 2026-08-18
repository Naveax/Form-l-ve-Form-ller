#!/usr/bin/env python3
import sys
from collections import Counter,defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_ad_third_direct_e2_supports as P
import probe_v26_q138_predecessor_leaf_ad_input_activity as I
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_ad_third_direct_e2_condition_group_rank1 as G
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T

MASK=(1<<128)-1
S=sorted(A.S1)
R=A.R1


def eval_map(M,x):
    z=0
    for j,(m,b) in enumerate(M):
        bit=((m&x).bit_count()&1)^b
        z |= bit<<j
    return z


def linear_image_rank(M,basis):
    rows=[]
    for d in basis:
        z=0
        for j,(m,b) in enumerate(M):
            z |= (((m&d).bit_count()&1)<<j)
        rows.append(z)
    return T.gf2_rank(rows,len(M)),rows


def canonical_subspace(rows,n):
    R=[x for x in rows if x];r=0
    for col in range(n):
        p=next((k for k in range(r,len(R)) if (R[k]>>col)&1),None)
        if p is None:continue
        R[r],R[p]=R[p],R[r]
        for k in range(len(R)):
            if k!=r and ((R[k]>>col)&1):R[k]^=R[r]
        r+=1
    return tuple(R[:r])


def reduce_mod_span(x,B):
    y=x
    for row in B:
        p=(row&-row).bit_length()-1
        if (y>>p)&1:y^=row
    return y


def main():
    raw,_=P.direct_supports('D')
    C=Counter(can for _,_,can in raw)
    odd=[can for can,n in C.items() if n&1]
    groups=defaultdict(list)
    for can in odd:
        cond=P.canonical_condition(I.input_condition(can))
        groups[cond].append(can)
    assert len(groups)==8629

    image_dim=Counter(); affine_desc=Counter(); linear_desc=Counter();
    maxdim=-1; examples=[]
    for cond,cans in groups.items():
        eq=[(row&MASK,(row>>128)&1) for row in cond]
        sol=T.rref(eq,n=128); assert sol is not None
        _,x0,basis=sol
        M=G.singleton_side_map(cans[0],S,R)
        d,rows=linear_image_rank(M,basis)
        image_dim[d]+=1
        B=canonical_subspace(rows,11)
        # canonical affine coset representative by reducing the basepoint modulo image span
        off=eval_map(M,x0)
        # canonical_subspace uses low-pivot RREF, so reduce with its pivot rows
        off=reduce_mod_span(off,B)
        linear_desc[B]+=1
        affine_desc[(B,off)]+=1
        if d>maxdim:
            maxdim=d;examples=[(cond,off,B)]
        elif d==maxdim and len(examples)<4:examples.append((cond,off,B))

    print('D_condition_groups',len(groups))
    print('D_left_singleton_image_dimension_distribution',dict(sorted(image_dim.items())))
    print('D_distinct_linear_image_subspaces',len(linear_desc))
    print('D_distinct_affine_image_cosets',len(affine_desc))
    print('D_max_image_dimension',maxdim)
    print('D_top_linear_subspace_multiplicities',Counter(linear_desc.values()).most_common(12))
    print('D_top_affine_coset_multiplicities',Counter(affine_desc.values()).most_common(12))
    print('PASS PROBE V26_Q138_AD_THIRD_D_LEFT_SINGLETON_IMAGES')
    print('scope=exact per-condition affine image geometry; no uniform 65-row theorem claimed')

if __name__=='__main__':main()
