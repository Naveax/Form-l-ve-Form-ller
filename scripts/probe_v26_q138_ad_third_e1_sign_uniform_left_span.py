#!/usr/bin/env python3
import itertools,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A

S=sorted(A.S1)
LEFT_EXT=[128+i for i in S]
LEFT_SET=set(LEFT_EXT)
RIGHT_EXT=[i for i in range(160) if i not in LEFT_SET]
RIDX={e:k for k,e in enumerate(RIGHT_EXT)}
ALL=(1<<2048)-1
WALSH=[]
for f in range(1<<11):
    z=0
    for x in range(1<<11):
        if (f&x).bit_count()&1:z|=1<<x
    WALSH.append(z)


def insert(B,x):
    y=x
    while y:
        p=y.bit_length()-1
        if p not in B:
            B[p]=y;return True
        y^=B[p]
    return False


def row_basis(rows):
    B={}
    for x in rows:
        if x:insert(B,x)
    return list(B.values())


def split_left(m):
    z=0
    for q,e in enumerate(LEFT_EXT):
        if (m>>e)&1:z|=1<<q
    return z


def phase_left_data(pos,C,extra=None):
    F,subs,r,eindex=A.internal_substitution(pos,C,extra)
    qbits=0;cols=[0]*len(RIGHT_EXT)
    for j in range(1,5):
        for i in range(31):
            X=T.xx(F[j,i,'u'],F[j,i,'w'])
            Y=T.xx(F[j,i,'v'],F[j,i,'w'])
            xm,xc=A.sub_form(X,subs,eindex);ym,yc=A.sub_form(Y,subs,eindex)
            xl=split_left(xm);yl=split_left(ym)
            qbits ^= WALSH[xl]&WALSH[yl]
            if xc:qbits^=WALSH[yl]
            if yc:qbits^=WALSH[xl]
            if xc&yc:qbits^=ALL
            for e in RIGHT_EXT:
                if (ym>>e)&1:cols[RIDX[e]]^=xl
                if (xm>>e)&1:cols[RIDX[e]]^=yl
    return qbits,row_basis(cols),r


def left_support_mask(can):
    rows=list(can);r=0
    # Eliminate every non-left external variable. Residual rows are exactly
    # the affine constraints on the11 S1 beta variables.
    for col in RIGHT_EXT:
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    eq=[]
    for row in rows[r:]:
        m=0
        for q,e in enumerate(LEFT_EXT):
            if (row>>e)&1:m|=1<<q
        rhs=(row>>160)&1
        if m or rhs:eq.append((m,rhs))
    sol=T.rref(eq,n=11)
    assert sol is not None
    mask=0
    for x in range(1<<11):
        if all(((m&x).bit_count()&1)==rhs for m,rhs in eq):mask|=1<<x
    assert mask
    return mask,sol[0]


def sectors(pos):
    sites=[(j,i) for j in range(1,4) for i in range(31)]
    FF=D.full_forms(pos);out=[]
    # e=1 weight91 full-rank sectors.
    for zs in itertools.combinations(sites,2):
        C=D.carries(zs,ad=True)
        if A.internal_null(pos,C)[0]!=128:continue
        can=A.canonical_support(pos,C,expect_internal=128)
        if can is not None:out.append(('w91full',zs,C,None,can))
    # e=1 weight92 nullity-one equal-sign sectors.
    for z in sites:
        C=D.carries([z],ad=True);sol=A.internal_null(pos,C)
        if sol[0]!=127:continue
        assert len(sol[2])==1
        extra=A.derivative_form(FF,A.map_internal_to_full(sol[2][0]))
        can=A.canonical_support(pos,C,extra,127)
        if can is not None:out.append(('w92n1',(z,),C,extra,can))
    return out


def main():
    expected={'A':271,'D':274}
    for pos in 'AD':
        G={};cross=Counter();support=Counter();types=Counter()
        ss=sectors(pos);assert len(ss)==expected[pos]
        for typ,zs,C,extra,can in ss:
            types[typ]+=1
            # Existing second-residue theorem proves cut intersection zero.
            assert A.cut_intersection(can)==0
            sm,sr=left_support_mask(can);support[sr]+=1
            qbits,cb,ir=phase_left_data(pos,C,extra)
            cross[len(cb)]+=1
            if typ=='w91full':assert ir==128
            else:assert ir==127
            for v in [sm,sm&qbits]+[sm&WALSH[f] for f in cb]:insert(G,v)
        print('position',pos,'e1_sector_count',len(ss),'type_distribution',dict(types),
              'left_support_rank_distribution',dict(sorted(support.items())),
              'cross_rank_distribution',dict(sorted(cross.items())),
              'uniform_e1_negative_sign_left_span_F2<=',len(G),flush=True)
    print('PASS PROBE V26_Q138_AD_THIRD_E1_SIGN_UNIFORM_LEFT_SPAN')
    print('interpretation=choose the e0 negative-sign second-layer lift with coefficient -1, so e0 contributes no third-residue correction; this probe bounds the remaining e1 negative-sign correction span')
    print('scope=correction component only; direct e=2 support component remains separate')

if __name__=='__main__':main()
