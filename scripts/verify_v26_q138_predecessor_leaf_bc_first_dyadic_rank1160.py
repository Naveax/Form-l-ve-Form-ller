#!/usr/bin/env python3
import itertools
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A


def polar_rows(pos,B):
    F=T.forms(pos,(0,0,0,0,0));q0=T.sign_phase(F,0);rows=[]
    for a in B:
        qa=T.sign_phase(F,a);row=0
        for k,b in enumerate(B):
            z=T.sign_phase(F,a^b)^qa^T.sign_phase(F,b)^q0
            row|=z<<k
        rows.append(row)
    return rows


def radical_directions(pos,B):
    P=polar_rows(pos,B)
    sol=T.rref([(row,0) for row in P],n=len(B))
    assert sol is not None
    dirs=[]
    for c in sol[2]:
        d=0
        for k,b in enumerate(B):
            if (c>>k)&1:d^=b
        dirs.append(d)
    return dirs,T.gf2_rank(P,len(B))


def canonical_support_many(pos,C,extras,expect_internal):
    F=D.full_forms(pos);E=D.equations(F,C,hom=False)+list(extras)
    rows=[m|((rhs&1)<<D.GN) for m,rhs in E]
    r=0
    for col in A.internal_cols():
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    assert r==expect_internal,(pos,r,expect_internal)

    residual=[]
    for row in rows[r:]:
        m=0
        for q,col in enumerate(A.ext_cols()):
            if (row>>col)&1:m|=1<<q
        rhs=(row>>D.GN)&1
        if m or rhs:residual.append(m|(rhs<<160))

    rr=list(residual);q=0
    for col in range(160):
        p=next((k for k in range(q,len(rr)) if (rr[k]>>col)&1),None)
        if p is None:continue
        rr[q],rr[p]=rr[p],rr[q]
        for k in range(len(rr)):
            if k!=q and ((rr[k]>>col)&1):rr[k]^=rr[q]
        q+=1
    for row in rr[q:]:
        if (row&((1<<160)-1))==0 and ((row>>160)&1):return None
    return tuple(rr[:q])


def gauss_nonzero_support(pos,C):
    sol=A.internal_null(pos,C)
    rank,_,B=sol
    dirs,pr=radical_directions(pos,B)
    FF=D.full_forms(pos)
    extras=[A.derivative_form(FF,A.map_internal_to_full(d)) for d in dirs]
    can=canonical_support_many(pos,C,extras,rank)
    return can,(rank,len(B),pr),len(dirs)


def quotient_signature(F,B,j,i):
    u,v,w=F[j,i,'u'],F[j,i,'v'],F[j,i,'w']
    out=[]
    for X,Y in ((u,v),(u,w)):
        m,_=T.xx(X,Y);q=0
        for k,b in enumerate(B):q|=((m&b).bit_count()&1)<<k
        out.append(q)
    return tuple(out)


def rank4(rows):
    return T.gf2_rank(list(rows),4)


def sign_cross_rows(pos,C):
    F,subs,r,eindex=A.internal_substitution(pos,C)
    assert r==128
    L=sorted(A.S1);li={x:k for k,x in enumerate(L)};ri={x:k for k,x in enumerate(A.R1)}
    rows=[0]*len(L)
    for j in range(1,5):
        for i in range(31):
            X=T.xx(F[j,i,'u'],F[j,i,'w'])
            Y=T.xx(F[j,i,'v'],F[j,i,'w'])
            xm,_=A.sub_form(X,subs,eindex);ym,_=A.sub_form(Y,subs,eindex)
            xr=yr=0
            for x in A.R1:
                if (xm>>(128+x))&1:xr|=1<<ri[x]
                if (ym>>(128+x))&1:yr|=1<<ri[x]
            for x in L:
                if (xm>>(128+x))&1:rows[li[x]]^=yr
                if (ym>>(128+x))&1:rows[li[x]]^=xr
    return rows


def main():
    sites=[(j,i) for j in range(1,5) for i in range(31)]

    # All-one B/C homogeneous system has a 4D nullspace. Every zero carry adds
    # two restrictions in this quotient. Enumerate full-rank weight121 triples
    # only in this 4D matroid.
    F0=T.forms('B',(0,0,0,0,0));base=A.internal_null('B',D.carries([]))
    assert base[0]==124 and len(base[2])==4
    sig={z:quotient_signature(F0,base[2],*z) for z in sites}
    full121=[]
    for z in itertools.combinations(sites,3):
        rows=[]
        for x in z:rows.extend(sig[x])
        if rank4(rows)==4:full121.append(z)
    assert len(full121)==484

    # Weight123 classes and parity-relevant subset.
    classes123=Counter();keep123=[]
    for z in sites:
        cls=D.internal_class('B',D.carries([z]));classes123[cls]+=1
        if cls in ((125,3,2),(126,2,0)):keep123.append((z,cls))
    assert classes123==Counter({(124,4,2):95,(125,3,2):14,(125,3,0):7,(126,2,0):8})
    assert len(keep123)==22

    # Weight122 exact class distribution.
    classes122=Counter();rank127=[];rank128=[]
    for z in itertools.combinations(sites,2):
        cls=D.internal_class('B',D.carries(z));classes122[cls]+=1
        if cls[0]==127:rank127.append(z)
        if cls[0]==128:rank128.append(z)
    assert classes122==Counter({(124,4,2):4465,(125,3,2):1372,(125,3,0):686,
                               (126,2,0):1025,(127,1,0):74,(128,0,0):4})
    expected128=[((1,0),(2,0)),((1,0),(4,0)),((2,0),(3,0)),((3,0),(4,0))]
    assert rank128==expected128

    expected={
        'B':{'raw':581,'mult':Counter({1:103,4:91,2:57}),
             'odd':Counter({3:63,4:31,2:9}),'affine':1036,'total':1052,'imp121':0},
        'C':{'raw':577,'mult':Counter({1:103,4:90,2:57}),
             'odd':Counter({3:60,4:41,2:2}),'affine':1144,'total':1160,'imp121':4},
    }

    for pos in 'BC':
        affine=[];imp121=[]

        # Weight121 unique-solution indicators.
        for z in full121:
            can=A.canonical_support(pos,D.carries(z),expect_internal=128)
            if can is None:imp121.append(z)
            else:affine.append(can)
        assert len(imp121)==expected[pos]['imp121']
        if pos=='C':
            assert set(imp121)=={
                ((1,0),(2,0),(3,11)),((1,0),(3,11),(4,0)),
                ((2,0),(3,0),(3,11)),((3,0),(3,11),(4,0))}

        # Weight122 nullity-one equal-sign indicators.
        for z in rank127:
            can,cls,rd=gauss_nonzero_support(pos,D.carries(z))
            assert cls==(127,1,0) and rd==1 and can is not None
            affine.append(can)

        # Weight123 parity-relevant nonzero-Gauss indicators.
        for z,cls0 in keep123:
            can,cls,rd=gauss_nonzero_support(pos,D.carries([z]))
            assert cls==cls0 and can is not None
            affine.append(can)

        # Weight124 top nonzero-Gauss indicator.
        can,cls,rd=gauss_nonzero_support(pos,D.carries([]))
        assert cls==(124,4,2) and rd==2 and can is not None
        affine.append(can)

        assert len(affine)==expected[pos]['raw']
        C=Counter(affine)
        assert Counter(C.values())==expected[pos]['mult']
        odd=[can for can,n in C.items() if n&1]
        assert len(odd)==103
        d=Counter(A.cut_intersection(can) for can in odd)
        assert d==expected[pos]['odd'],(pos,d)
        affine_bound=sum(n*(1<<k) for k,n in d.items())
        assert affine_bound==expected[pos]['affine']

        # Four weight122 rank128 sectors share one support. Their combined
        # half-integral parity is q1 xor q2 xor q3 xor q4 on that support.
        supports=[A.canonical_support(pos,D.carries(z),expect_internal=128) for z in rank128]
        assert all(x==supports[0] for x in supports)
        sd=A.cut_intersection(supports[0]);assert sd==2
        rows=[0]*len(A.S1)
        for z in rank128:
            qrows=sign_cross_rows(pos,D.carries(z))
            rows=[a^b for a,b in zip(rows,qrows)]
        qrank=T.gf2_rank(rows,len(A.R1));assert qrank==2
        signed_bound=(1<<sd)*(qrank+2)
        assert signed_bound==16

        total=affine_bound+signed_bound
        assert total==expected[pos]['total']
        print('position',pos,'fullrank_weight121',len(full121)-len(imp121),
              'odd_affine_supports',len(odd),'intersection_distribution',dict(d),
              'affine_rank_bound',affine_bound,'four_sector_signed_bound',signed_bound,
              'first_residue_rank_bound',total)

    print('PASS V26_Q138_PREDECESSOR_LEAF_BC_FIRST_DYADIC_RANK1160')
    print('natural_scaling_B_C=2^121')
    print('rank_F2((2^121 L_B) mod2 across S1)<=1052')
    print('rank_F2((2^121 L_C) mod2 across S1)<=1160')
    print('both_bounds_strictly_below_generic_2048')
    print('scope=first dyadic residue only; no rational Schmidt-rank or arithmetic-work reduction claim')


if __name__=='__main__':main()
