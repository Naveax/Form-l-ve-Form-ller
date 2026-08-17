#!/usr/bin/env python3
import itertools, sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_qr_q138_right_map_reachable_hull197 as H
import verify_v26_qr_q138_right_map_rank_conditioning as R
import verify_v26_qr_q138_physical_rank_envelope27 as P

MASK_NAMES=(
    'u1_3','u2_3','u1_4','u2_4','u1_5','u2_5',
    'u1_6','u2_6','u1_7','u2_7','u2_8','u2_31',
)
PRIME=1000000007


def add_basis_q(B,row):
    r={j:Fraction(v) for j,v in row.items() if v}
    while r:
        c=min(r)
        if c not in B:
            q=1/r[c]; B[c]={j:x*q for j,x in r.items()}; return True
        a=r[c]; b=B[c]
        for j,x in b.items():
            r[j]=r.get(j,Fraction(0))-a*x
            if not r[j]: r.pop(j,None)
    return False


def reduce_q(row,B,pindex):
    r={j:Fraction(v) for j,v in row.items() if v}; out={}
    while r:
        c=min(r); assert c in B,('outside exact span',c)
        a=r[c]; out[pindex[c]]=out.get(pindex[c],Fraction(0))+a
        for j,x in B[c].items():
            r[j]=r.get(j,Fraction(0))-a*x
            if not r[j]: r.pop(j,None)
    return {j:x for j,x in out.items() if x}


def modfrac(x,p=PRIME):
    return (x.numerator%p)*pow(x.denominator%p,p-2,p)%p


def add_basis_mod(B,row,p=PRIME):
    r={j:(v%p) for j,v in row.items() if v%p}
    while r:
        c=min(r)
        if c not in B:
            inv=pow(r[c],p-2,p); B[c]={j:(x*inv)%p for j,x in r.items()}; return True
        a=r[c]; b=B[c]
        for j,x in b.items():
            z=(r.get(j,0)-a*x)%p
            if z:r[j]=z
            else:r.pop(j,None)
    return False


def flat_parent(Prows):
    out={}
    for a,row in enumerate(Prows):
        for j,x in row.items():
            if x:out[a*64+j]=x
    return out


def build_objects(cert):
    ctx=H.setup(cert); intA=ctx[6]
    assert intA==['aux_j2_i8_k0','aux_j4_i11_k0','aux_j4_i16_k0','sig1_7','sig3_7','sig4_7']
    PHYS=list(itertools.product((0,1),repeat=2))
    Ks={(u1,u2):H.transfer(ctx,4,(u1,u2,0)) for u1,u2 in PHYS}
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
        if close_ref is None:close_ref=close
        assert close==close_ref; closures[c]=C7
    rctx=R.setup(cert); assert rctx[9]==intA
    L=P.row_basis(R.left_rows(rctx,(0,0,0),(0,0,0))); assert len(L)==48
    return intA,prefix,closures,close_ref,L


def parent_flat(ctrl,intA,prefix,closures,close_ref,L):
    G=P.gram_rows(intA,close_ref,prefix[ctrl[:8]],closures[ctrl[8:]])
    return flat_parent(P.parent_rows(L,G))


def tt_profile(Drows,rankdim=124):
    out=[]; nbits=12
    for k in range(1,nbits+1):
        B={}; ns=1<<(nbits-k)
        for pref in range(1<<k):
            row={}
            for suff in range(ns):
                d=Drows[(pref<<(nbits-k))|suff]; base=suff*rankdim
                for lam,x in d.items():row[base+lam]=x
            add_basis_q(B,row)
        out.append(len(B)); print('tt_cut',k,'rank',len(B),flush=True)
    return out


def main():
    cert=sys.argv[1] if len(sys.argv)>1 else 'research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json'
    intA,prefix,closures,close_ref,L=build_objects(cert)
    ctrls=list(itertools.product((0,1),repeat=12))

    # Prime-field witness finds 124 independent physical masks.
    M={}; witnesses=[]
    for n,ctrl in enumerate(ctrls,1):
        q=parent_flat(ctrl,intA,prefix,closures,close_ref,L)
        if add_basis_mod(M,{j:modfrac(x) for j,x in q.items()}): witnesses.append(ctrl)
        if n%512==0:print('mod-span',n,len(M),flush=True)
    assert len(M)==124,len(M); assert len(witnesses)==124

    # The witness matrices are also independent over Q.
    F={}
    for ctrl in witnesses:
        assert add_basis_q(F,parent_flat(ctrl,intA,prefix,closures,close_ref,L))
    assert len(F)==124
    fpiv=sorted(F); findex={p:i for i,p in enumerate(fpiv)}

    # Every physical mask is exactly in that rational 124-dimensional family span.
    D=[]; nnz=0
    for n,ctrl in enumerate(ctrls,1):
        d=reduce_q(parent_flat(ctrl,intA,prefix,closures,close_ref,L),F,findex)
        D.append(d); nnz+=len(d)
        if n%512==0:print('exact-cover',n,'selector_nnz',nnz,flush=True)

    # The row directions of the 124 family basis matrices generate exactly U47.
    U={}
    for mat in F.values():
        byrow=[{} for _ in range(48)]
        for ij,x in mat.items():byrow[ij//64][ij%64]=x
        for row in byrow:add_basis_q(U,row)
    assert len(U)==47,len(U)
    upiv=sorted(U); uindex={p:i for i,p in enumerate(upiv)}

    # Fixed kernel K(lambda,a,r) from family sectors to left48 x U47.
    knnz=0
    for mat in F.values():
        byrow=[{} for _ in range(48)]
        for ij,x in mat.items():byrow[ij//64][ij%64]=x
        for row in byrow:knnz+=len(reduce_q(row,U,uindex))

    profile=tt_profile(D,124); maxchi=max(profile)

    print('PASS V26_QR_Q138_MASK_COEFF124_TT')
    print('mask_order='+','.join(MASK_NAMES))
    print('exact_parent_matrix_family_rank=124')
    print('common_parent_interface_span=47')
    print('mask_selector_shape=4096x124 selector_nnz='+str(nnz))
    print('kernel_shape=124x48x47 kernel_nnz='+str(knnz))
    print('exact_tt_profile='+','.join(map(str,profile)))
    print('exact_tt_max_bond='+str(maxchi))
    print('DEPENDENCY parent_rank_envelope=5..27 is verified separately by verify_v26_qr_q138_physical_rank_envelope27.py')

if __name__=='__main__':main()
