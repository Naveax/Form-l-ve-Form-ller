#!/usr/bin/env python3
import itertools
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D

S1={0,1,2,3,4,5,12,13,14,15,16}
R1=[i for i in range(32) if i not in S1]


def map_internal_to_full(b):
    out=0
    for g,off in (('U3',0),('V3',32),('U4',64),('V4',96)):
        for i in range(32):
            if (b>>(off+i))&1:
                out |= 1<<(D.GBASE[g]+i)
    return out


def derivative_form(F,direction):
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


def internal_cols():
    out=[]
    for g in ('U3','V3','U4','V4'):
        out += list(range(D.GBASE[g],D.GBASE[g]+32))
    return out


def ext_cols():
    out=[]
    for g in ('A0','B0','C0','D0','BETA'):
        out += list(range(D.GBASE[g],D.GBASE[g]+32))
    return out


def canonical_support(pos,C,extra=None,expect_internal=None):
    F=D.full_forms(pos)
    E=D.equations(F,C,hom=False)
    if extra is not None:E=E+[extra]
    rows=[m|((rhs&1)<<D.GN) for m,rhs in E]
    r=0
    for col in internal_cols():
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    if expect_internal is not None:assert r==expect_internal,(pos,r,expect_internal)

    ec=ext_cols(); residual=[]
    for row in rows[r:]:
        m=0
        for q,col in enumerate(ec):
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
        if (row&((1<<160)-1))==0 and ((row>>160)&1):
            return None
    return tuple(rr[:q])


def cut_intersection(canon):
    r=len(canon); cols=[]
    for i in range(32):
        v=0
        for k,row in enumerate(canon):
            if (row>>(128+i))&1:v|=1<<k
        cols.append(v)
    L=[cols[i] for i in sorted(S1)]
    R=[cols[i] for i in R1]
    a=T.gf2_rank(L,r);b=T.gf2_rank(R,r);ab=T.gf2_rank(L+R,r)
    return a+b-ab


def internal_null(pos,C):
    F=T.forms(pos,(0,0,0,0,0))
    sol=T.rref(D.equations(F,C,hom=True))
    assert sol is not None
    return sol


def internal_substitution(pos,C,extra=None):
    F=D.full_forms(pos)
    E=D.equations(F,C,hom=False)
    if extra is not None:E=E+[extra]
    rows=[m|((rhs&1)<<D.GN) for m,rhs in E]
    ints=internal_cols(); r=0; piv=[]
    for col in ints:
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        piv.append(col);r+=1

    ec=ext_cols(); eindex={col:i for i,col in enumerate(ec)}
    subs={}
    for row,p in zip(rows[:r],piv):
        m=0
        for col,ei in eindex.items():
            if (row>>col)&1:m|=1<<ei
        subs[p]=(m,(row>>D.GN)&1)
    for col in ints:
        if col not in subs:subs[col]=(0,0)
    return F,subs,r,eindex


def sub_form(f,subs,eindex):
    m,c=f; outm=0;outc=c
    for col,s in subs.items():
        if (m>>col)&1:
            outm^=s[0];outc^=s[1]
    for col,ei in eindex.items():
        if (m>>col)&1:outm^=1<<ei
    return outm,outc


def sign_cross_rank(pos,C,extra=None):
    F,subs,r,eindex=internal_substitution(pos,C,extra)
    L=sorted(S1); lindex={x:k for k,x in enumerate(L)}
    rindex={x:k for k,x in enumerate(R1)}
    rows=[0]*len(L)
    for j in range(1,5):
        for i in range(31):
            A=T.xx(F[j,i,'u'],F[j,i,'w'])
            B=T.xx(F[j,i,'v'],F[j,i,'w'])
            am,_=sub_form(A,subs,eindex); bm,_=sub_form(B,subs,eindex)
            ar=br=0
            for x in R1:
                if (am>>(128+x))&1:ar|=1<<rindex[x]
                if (bm>>(128+x))&1:br|=1<<rindex[x]
            for x in L:
                if (am>>(128+x))&1:rows[lindex[x]]^=br
                if (bm>>(128+x))&1:rows[lindex[x]]^=ar
    return T.gf2_rank(rows,len(R1)),r


def main():
    sites=[(j,i) for j in range(1,4) for i in range(31)]
    special={(1,0),(3,0)}
    expected={
        'A':{'w91':181,'w92':90,'cross':[11,10,11],'bound':309},
        'D':{'w91':183,'w92':91,'cross':[10,10,10],'bound':310},
    }

    for pos in 'AD':
        # Weight92: 91 nullity-one sectors and exactly two full-rank sectors.
        full92=[]; null92=[]
        for z in sites:
            sol=internal_null(pos,D.carries([z],ad=True))
            if sol[0]==128:full92.append(z)
            else:
                assert sol[0]==127 and len(sol[2])==1
                null92.append((z,sol[2][0]))
        assert full92==[(1,0),(3,0)]
        assert len(null92)==91

        # Weight91 full-rank sectors: exactly all pairs containing one special site.
        full91=[]
        for z in itertools.combinations(sites,2):
            if internal_null(pos,D.carries(z,ad=True))[0]==128:full91.append(z)
        assert len(full91)==183
        assert all(set(z)&special for z in full91)

        reachable91=[]
        for z in full91:
            can=canonical_support(pos,D.carries(z,ad=True),expect_internal=128)
            if can is None:continue
            assert cut_intersection(can)==0
            reachable91.append(z)

        reachable92=[]
        FF=D.full_forms(pos)
        for z,b in null92:
            der=derivative_form(FF,map_internal_to_full(b))
            can=canonical_support(pos,D.carries([z],ad=True),der,127)
            if can is None:continue
            assert cut_intersection(can)==0
            reachable92.append(z)

        assert len(reachable91)==expected[pos]['w91'],(pos,len(reachable91))
        assert len(reachable92)==expected[pos]['w92'],(pos,len(reachable92))
        if pos=='A':
            assert set(full91)-set(reachable91)=={((1,0),(2,15)),((2,15),(3,0))}
            assert set(z for z,_ in null92)-set(reachable92)=={(2,15)}

        # Three signed quadratic terms: two weight92 unique solutions and the
        # weight93 equal-sign top fiber. Their supports all factor across S1.
        cross=[]
        for z in full92:
            C=D.carries([z],ad=True)
            can=canonical_support(pos,C,expect_internal=128)
            assert can is not None and cut_intersection(can)==0
            q,r=sign_cross_rank(pos,C)
            assert r==128
            cross.append(q)

        Ctop=D.carries([],ad=True)
        sol=internal_null(pos,Ctop)
        assert sol[0]==127 and len(sol[2])==1
        der=derivative_form(FF,map_internal_to_full(sol[2][0]))
        can=canonical_support(pos,Ctop,der,127)
        assert can is not None and cut_intersection(can)==0
        q,r=sign_cross_rank(pos,Ctop,der)
        assert r==127
        cross.append(q)
        assert cross==expected[pos]['cross'],(pos,cross)

        # Rank-one affine terms plus q-gated terms of rank <= cross_rank+2.
        bound=len(reachable91)+len(reachable92)+sum(x+2 for x in cross)
        assert bound==expected[pos]['bound']
        print('position',pos,'reachable_weight91_rank1',len(reachable91),
              'reachable_weight92_nullity1_rank1',len(reachable92),
              'quadratic_cross_ranks',cross,'second_residue_rank_bound',bound)

    print('PASS V26_Q138_PREDECESSOR_LEAF_AD_SECOND_DYADIC_RANK310')
    print('exact_lift=2^92 L = M0 + 2 M1')
    print('rank_F2(M0)<=3')
    print('rank_F2(M1_A mod2)<=309')
    print('rank_F2(M1_D mod2)<=310')
    print('scope=second dyadic residue only; no rational Schmidt-rank or arithmetic-work reduction claim')


if __name__=='__main__':main()
