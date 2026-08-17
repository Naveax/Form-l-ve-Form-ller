#!/usr/bin/env python3
import itertools, sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_right_map_reachable_hull197 as H
import verify_v26_qr_q138_right_map_rank_conditioning as R
import verify_v26_qr_q138_physical_rank_envelope27 as P
import verify_v26_qr_q138_width40_left_rank48 as Q

PHYS=list(itertools.product((0,1),repeat=2))
MASK_NAMES=(
    'u1_3','u2_3','u1_4','u2_4','u1_5','u2_5',
    'u1_6','u2_6','u1_7','u2_7','u2_8','u2_31',
)


def add_basis(B, row):
    r={j:Fraction(v) for j,v in row.items() if v}
    while r:
        c=min(r)
        if c not in B:
            q=1/r[c]
            B[c]={j:x*q for j,x in r.items()}
            return True
        q=r[c]; b=B[c]
        for j,x in b.items():
            r[j]=r.get(j,Fraction(0))-q*x
            if not r[j]: r.pop(j,None)
    return False


def coords_in_basis(v,B,pindex):
    r={j:Fraction(x) for j,x in v.items() if x}
    out={}
    while r:
        c=min(r)
        assert c in B, ('outside common U47',c)
        a=r[c]
        if a: out[pindex[c]]=out.get(pindex[c],Fraction(0))+a
        for j,x in B[c].items():
            r[j]=r.get(j,Fraction(0))-a*x
            if not r[j]: r.pop(j,None)
    return {j:x for j,x in out.items() if x}


def build_transfer_objects(cert):
    ctx=H.setup(cert)
    intA=ctx[6]
    assert intA==['aux_j2_i8_k0','aux_j4_i11_k0','aux_j4_i16_k0','sig1_7','sig3_7','sig4_7']
    Ks={(u1,u2):H.transfer(ctx,4,(u1,u2,0)) for u1,u2 in PHYS}
    for uv in PHYS:
        assert Ks[uv]==H.transfer(ctx,5,(uv[0],uv[1],0))==H.transfer(ctx,6,(uv[0],uv[1],0))
    prefix={}
    for bits in itertools.product((0,1),repeat=8):
        u13,u23,u14,u24,u15,u25,u16,u26=bits
        vecs=H.boundary(ctx,(u13,u23,0))
        for uv in ((u14,u24),(u15,u25),(u16,u26)):
            vecs={z:H.image(v,Ks[uv]) for z,v in vecs.items()}
        prefix[bits]=vecs
    closures={}; close_ref=None
    for c in itertools.product((0,1),repeat=4):
        C7,close=P.closure7(ctx,*c)
        if close_ref is None: close_ref=close
        assert close==close_ref
        closures[c]=C7
    return ctx,intA,prefix,closures,close_ref


def common_left_basis(cert,intA):
    rctx=R.setup(cert)
    assert rctx[9]==intA
    L=P.row_basis(R.left_rows(rctx,(0,0,0),(0,0,0)))
    assert len(L)==48
    for u1 in itertools.product((0,1),repeat=3):
        for u2 in itertools.product((0,1),repeat=3):
            B=P.row_basis(R.left_rows(rctx,u1,u2))
            assert len(B)==48
            assert len(P.row_basis(L+B))==48
    return L


def parent_for(ctrl,intA,close_ref,prefix,closures,L):
    pb=ctrl[:8]; cb=ctrl[8:]
    G=P.gram_rows(intA,close_ref,prefix[pb],closures[cb])
    return P.parent_rows(L,G)


def main():
    cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json'
    ctx,intA,prefix,closures,close_ref=build_transfer_objects(cert)
    L=common_left_basis(cert,intA)

    # Freeze a deterministic common rational U47 basis in lexicographic mask order.
    U={}
    ranks=[]
    ctrls=list(itertools.product((0,1),repeat=12))
    for n,ctrl in enumerate(ctrls,1):
        Prows=parent_for(ctrl,intA,close_ref,prefix,closures,L)
        PB=P.row_basis(Prows); ranks.append(len(PB))
        for row in PB: add_basis(U,row)
        if n%512==0: print(f'common-span progress {n}/4096 dim={len(U)}',flush=True)
    assert len(U)==47,len(U)
    pivots=sorted(U); pindex={p:i for i,p in enumerate(pivots)}

    # Exact flattening mask | (left48,U47).  Each mask contributes one 48x47 coefficient matrix.
    F={}; nnz_total=0
    for n,ctrl in enumerate(ctrls,1):
        Prows=parent_for(ctrl,intA,close_ref,prefix,closures,L)
        flat={}
        for a,row in enumerate(Prows):
            cc=coords_in_basis(row,U,pindex)
            for r,x in cc.items():
                flat[a*47+r]=x
        nnz_total+=len(flat)
        add_basis(F,flat)
        if n%256==0: print(f'coefficient-family progress {n}/4096 rank={len(F)}',flush=True)
    family_rank=len(F)

    # Sanity: the tensor output really lives in 48 x U47, and mask-specific matrix rank
    # reproduces the admitted parent rank envelope.
    assert min(ranks)==5 and max(ranks)==27
    assert family_rank==124,family_rank

    print('PASS V26_QR_Q138_MASK_TO_U47_COEFF_TENSOR')
    print('mask_order='+','.join(MASK_NAMES))
    print('common_parent_basis_dimension=47 pivots='+','.join(map(str,pivots)))
    print('left_coordinate_dimension=48')
    print('exact_mask_to_coefficient_flattening_rank=124')
    print(f'coefficient_tensor_shape=4096x48x47 total_sparse_nnz={nnz_total}')
    print('per_mask_parent_rank_min=5 per_mask_parent_rank_max=27')

if __name__=='__main__':
    main()
