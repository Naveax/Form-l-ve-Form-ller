#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D

S1={0,1,2,3,4,5,12,13,14,15,16}


def map_internal_to_full(b):
    out=0
    for g,off in (('U3',0),('V3',32),('U4',64),('V4',96)):
        for i in range(32):
            if (b>>(off+i))&1:
                out |= 1<<(D.GBASE[g]+i)
    return out


def derivative_form(F,direction):
    # Derivative of q=sum (u xor w)(v xor w) along a fixed internal null vector.
    m=c=0
    for j in range(1,5):
        for i in range(31):
            A=T.xx(F[j,i,'u'],F[j,i,'w'])
            B=T.xx(F[j,i,'v'],F[j,i,'w'])
            a=(A[0]&direction).bit_count()&1
            b=(B[0]&direction).bit_count()&1
            if a:m^=B[0];c^=B[1]
            if b:m^=A[0];c^=A[1]
            c^=a&b
    return m,c


def canonical_external_with_extra(pos,C,extra):
    F=D.full_forms(pos)
    E=D.equations(F,C,hom=False)+[extra]
    rows=[m|((rhs&1)<<D.GN) for m,rhs in E]
    internal=[]
    for g in ('U3','V3','U4','V4'):
        internal += list(range(D.GBASE[g],D.GBASE[g]+32))
    r=0
    for col in internal:
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    assert r==127

    extcols=[]
    for g in ('A0','B0','C0','D0','BETA'):
        extcols += list(range(D.GBASE[g],D.GBASE[g]+32))
    residual=[]
    for row in rows[r:]:
        m=0
        for q,col in enumerate(extcols):
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
        assert not ((row&((1<<160)-1))==0 and ((row>>160)&1))
    return tuple(rr[:q])


def cut_intersection(canon,S=S1):
    r=len(canon);cols=[]
    for i in range(32):
        v=0
        for k,row in enumerate(canon):
            if (row>>(128+i))&1:v|=1<<k
        cols.append(v)
    L=[cols[i] for i in sorted(S)]
    R=[cols[i] for i in range(32) if i not in S]
    a=T.gf2_rank(L,r);b=T.gf2_rank(R,r);ab=T.gf2_rank(L+R,r)
    return a,b,ab,a+b-ab


def main():
    for pos in 'AD':
        # All j4 carries are forced zero; top pattern has nullity1.
        Ctop=D.carries([],ad=True)
        F0=T.forms(pos,(0,0,0,0,0))
        sol=T.rref(D.equations(F0,Ctop,hom=True))
        assert sol is not None
        rank,_,B=sol
        assert rank==127 and len(B)==1

        # Weight92 one-zero sectors: only j1-bit0 and j3-bit0 are full rank.
        dist=Counter();full=[]
        for j in range(1,4):
            for i in range(31):
                C=D.carries([(j,i)],ad=True)
                s=T.rref(D.equations(F0,C,hom=True))
                assert s is not None
                rr=s[0];dist[rr]+=1
                if rr==128:full.append((j,i))
        assert dist==Counter({127:91,128:2}),dist
        assert full==[(1,0),(3,0)],full

        indicators=[]
        for z in full:
            C=D.carries([z],ad=True)
            canon=D.canonical_external_constraints(pos,C)
            assert len(canon)==37
            indicators.append(('weight92-'+str(z),canon))

        # Top-weight93 contributes after division by2 iff the two signs agree.
        # Add derivative(q along null vector)=0 as one affine condition.
        FF=D.full_forms(pos)
        der=derivative_form(FF,map_internal_to_full(B[0]))
        topcanon=canonical_external_with_extra(pos,Ctop,der)
        assert len(topcanon)==37
        indicators.append(('weight93-sign-pair',topcanon))

        for name,canon in indicators:
            a,b,ab,inter=cut_intersection(canon)
            assert inter==0,(pos,name,a,b,ab,inter)

    print('PASS V26_Q138_PREDECESSOR_LEAF_AD_PARITY_RANK3')
    print('natural_scaling_A_D=2^92')
    print('weight92_internal_rank_distribution=127:91,128:2')
    print('weight92_fullrank_sectors={(j1,bit0),(j3,bit0)}')
    print('weight93_top_fiber_nullity=1; parity condition=affine sign derivative zero')
    print('three_surviving_affine_indicators_each_S1_communication_rank=1')
    print('rank_F2((2^92 L_A) mod2 across S1)<=3')
    print('rank_F2((2^92 L_D) mod2 across S1)<=3')
    print('next=lift M=M0+2M1 and analyze the next 2-adic residue')
    print('scope=first 2-adic residue only; no rational Schmidt-rank bound3 claim')


if __name__=='__main__':main()
