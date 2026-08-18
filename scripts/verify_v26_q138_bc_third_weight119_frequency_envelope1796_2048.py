#!/usr/bin/env python3
import itertools,math,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_predecessor_leaf_fast_nullspace_fourier as Q
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as V

S=sorted(A.S1)


def qrank(sig,zs):
    rows=[]
    for z in zs:rows.extend(sig[z])
    return T.gf2_rank(rows,4)


def fullrank5_candidates(active,inert,sig):
    for r in range(2,6):
        for core in itertools.combinations(active,r):
            if qrank(sig,core)!=4:continue
            for fill in itertools.combinations(inert,5-r):
                yield tuple(sorted(core+fill))


def space_mask(B):
    vals=[0]
    for b in B:vals += [x^b for x in vals]
    out=0
    for x in vals:out |= 1<<x
    return out


def weight119_union(pos,active,inert,sig):
    _,res,free,extra=Q.setup(pos,False)
    U=0;tested=0;maxrank=0;saturation=None;cache={}
    for zs in fullrank5_candidates(active,inert,sig):
        tested+=1
        B=Q.left_space(res,free,extra,zs)
        assert B is not None,(pos,zs)
        maxrank=max(maxrank,len(B))
        key=tuple(sorted(B))
        if key not in cache:cache[key]=space_mask(B)
        U |= cache[key]
        if U.bit_count()==2048:
            saturation=tested;break
    return tested,U,maxrank,saturation,len(cache)


def kernel_and_polar(zs,sig,P):
    rows=[]
    for z in zs:rows.extend(sig[z])
    sol=T.rref([(r,0) for r in rows],n=4);assert sol is not None
    qr,_,K=sol;n=len(K)
    prows=[]
    for a in K:
        row=0
        for j,b in enumerate(K):
            v=0
            for i in range(4):
                if (a>>i)&1:v ^= (P[i]&b).bit_count()&1
            row |= v<<j
        prows.append(row)
    pr=T.gf2_rank(prows,n)
    psol=T.rref([(r,0) for r in prows],n=n);assert psol is not None
    radical=[]
    for coeff in psol[2]:
        d=0
        for j,b in enumerate(K):
            if (coeff>>j)&1:d^=b
        radical.append(d)
    return qr,K,pr,radical


def class4(zs,sig,P):
    qr,K,pr,_=kernel_and_polar(zs,sig,P)
    return 124+qr,len(K),pr


def e2_candidates(k,active,inert,sig,P):
    for r in range(0,min(k,len(active))+1):
        for core in itertools.combinations(active,r):
            ir,n,pr=class4(core,sig,P)
            if k-3+n-pr//2 !=2:continue
            for fill in itertools.combinations(inert,k-r):
                yield tuple(sorted(core+fill)),(ir,n,pr)


def rref_internal(rows):
    rows=list(rows);r=0;piv=[]
    for col in A.internal_cols():
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        piv.append(col);r+=1
    return rows,piv,r


def reduce_by_pivots(row,pivrows,pivcols):
    x=row
    for pr,col in zip(pivrows,pivcols):
        if (x>>col)&1:x^=pr
    return x


def gauss_setup_B():
    F=D.full_forms('B');C0=D.carries([])
    rows,piv,r=rref_internal([m for m,rhs in D.equations(F,C0,hom=True)])
    assert r==124
    pivrows=rows[:r];res=[x for x in rows[r:] if x]
    free=[c for c in A.internal_cols() if c not in set(piv)]
    assert len(free)==4
    extra={}
    for j in range(1,5):
        for i in range(31):
            u,v,w=F[j,i,'u'],F[j,i,'v'],F[j,i,'w']
            aa=T.xx(u,v)[0];bb=T.xx(u,w)[0]
            extra[j,i]=(reduce_by_pivots(aa,pivrows,piv),reduce_by_pivots(bb,pivrows,piv))
    return F,pivrows,piv,res,free,extra


def gauss_left_B(zs,setup,topbasis,sig,P,deriv_cache):
    F,pivrows,piv,res,free,extra=setup
    rows=list(res)
    for z in zs:rows.extend(extra[z])
    qr,K,pr,radical=kernel_and_polar(zs,sig,P)
    for d4 in radical:
        if d4 not in deriv_cache:
            d=0
            for i,b in enumerate(topbasis):
                if (d4>>i)&1:d^=b
            row=A.derivative_form(F,A.map_internal_to_full(d))[0]
            deriv_cache[d4]=reduce_by_pivots(row,pivrows,piv)
        rows.append(deriv_cache[d4])
    r=0
    for col in free:
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    left=[]
    for row in rows[r:]:
        v=0
        for q,i in enumerate(S):
            if (row>>(D.GBASE['BETA']+i))&1:v|=1<<q
        if v:left.append(v)
    B={}
    for x in left:
        while x:
            p=x.bit_length()-1
            if p not in B:B[p]=x;break
            x^=B[p]
    return list(B.values())


def canonical_left_mask(can):
    assert can is not None
    rows=[]
    for row in can:
        v=0
        for q,i in enumerate(S):
            if (row>>(128+i))&1:v|=1<<q
        if v:rows.append(v)
    B={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p not in B:B[p]=x;break
            x^=B[p]
    return space_mask(list(B.values()))


def main():
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    F0=T.forms('B',(0,0,0,0,0));base=A.internal_null('B',D.carries([]))
    assert base[0]==124 and len(base[2])==4
    sig={z:V.quotient_signature(F0,base[2],*z) for z in sites}
    inert=[z for z in sites if sig[z]==(0,0)]
    active=[z for z in sites if sig[z]!=(0,0)]
    assert len(inert)==95 and len(active)==29
    P=V.polar_rows('B',base[2]);assert T.gf2_rank(P,4)==2

    core={r:sum(qrank(sig,z)==4 for z in itertools.combinations(active,r)) for r in range(2,6)}
    assert core=={2:4,3:104,4:1301,5:10425},core
    assert core[2]*95+core[3]==484
    assert core[2]*math.comb(95,2)+core[3]*95+core[4]==29041
    total5=core[2]*math.comb(95,3)+core[3]*math.comb(95,2)+core[4]*95+core[5]
    assert total5==1_152_040

    # Full-rank weight119 candidate envelopes.
    bt,UB5,bmax,bsat,bspaces=weight119_union('B',active,inert,sig)
    assert (bt,UB5.bit_count(),bmax,bsat)==(1_152_040,1796,8,None)

    # Exact fast Gauss-support construction for the lower e=2 classes.
    setup=gauss_setup_B();deriv={}
    expected_classes={
        2:Counter({(124,4,2):4465,(125,3,0):686}),
        3:Counter({(125,3,2):66570,(126,2,0):63174}),
        4:Counter({(127,1,0):450840}),
    }
    lower={};reps={}
    for k in (2,3,4):
        U=0;classes=Counter();maxrank=0;count=0
        for zs,cls in e2_candidates(k,active,inert,sig,P):
            count+=1;classes[cls]+=1
            B=gauss_left_B(zs,setup,base[2],sig,P,deriv)
            maxrank=max(maxrank,len(B));U |= space_mask(B)
            reps.setdefault(cls,zs)
        assert classes==expected_classes[k],(k,classes)
        assert U.bit_count()==1712,(k,U.bit_count())
        assert maxrank<=8
        lower[k]=U
        print('position B','zero_count',k,'e2_patterns',count,
              'class_distribution',dict(classes),'left_frequency_union',U.bit_count(),
              'max_individual_left_rank',maxrank,flush=True)

    assert lower[2]==lower[3]==lower[4]
    Ulow=lower[2]
    assert Ulow & ~UB5 ==0
    assert (UB5 & ~Ulow).bit_count()==84

    # Cross-check one representative from every lower e=2 nullity/polar class
    # against the full canonical Gauss-support construction.
    for cls,zs in sorted(reps.items()):
        can,got,rd=V.gauss_nonzero_support('B',D.carries(zs))
        assert got==cls and can is not None,(cls,zs,got)
        fast=space_mask(gauss_left_B(zs,setup,base[2],sig,P,deriv))
        exact=canonical_left_mask(can)
        assert fast==exact,(cls,zs)

    # C candidate homogeneous envelope saturates, closing only this method.
    ct,UC5,cmax,csat,cspaces=weight119_union('C',active,inert,sig)
    assert (ct,UC5.bit_count(),cmax,csat)==(934_476,2048,8,934_476)

    print('position B','weight119_fullrank_candidates',bt,
          'weight119_candidate_union',UB5.bit_count(),'distinct_weight119_left_spaces',bspaces,
          'lower_e2_common_union',Ulow.bit_count(),'weight119_extra_frequencies',84,flush=True)
    print('position C','weight119_candidates_until_saturation',ct,
          'candidate_union',UC5.bit_count(),'distinct_left_spaces_until_saturation',cspaces,flush=True)
    print('PASS V26_Q138_BC_THIRD_WEIGHT119_FREQUENCY_ENVELOPE1796_2048')
    print('PASS V26_Q138_BC_THIRD_DIRECT_E2_SUPPORT_ENVELOPE1796')
    print('active_core_rank4_counts=2:4,3:104,4:1301,5:10425')
    print('B_direct_e2_support_only_left_factor_envelope<=1796')
    print('C_weight119_fullrank_candidate_homogeneous_envelope=2048_NO_GAIN')
    print('scope=direct e2 leading support parity only; inherited third corrections and complete b2/c2 remain open')

if __name__=='__main__':main()
