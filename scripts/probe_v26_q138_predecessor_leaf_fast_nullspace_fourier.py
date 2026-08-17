#!/usr/bin/env python3
import itertools,sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as FU

S=sorted({0,1,2,3,4,5,12,13,14,15,16})


def internal_cols():
    out=[]
    for g in ('U3','V3','U4','V4'):
        out += list(range(D.GBASE[g],D.GBASE[g]+32))
    return out


def rref_internal(rows):
    rows=list(rows);r=0;piv=[]
    for col in internal_cols():
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


def setup(pos,ad=False):
    F=D.full_forms(pos);C=D.carries([],ad=ad)
    base=[m for m,rhs in D.equations(F,C,hom=True)]
    rows,piv,r=rref_internal(base)
    expected=127 if ad else 124
    assert r==expected,(pos,r)
    pivrows=rows[:r];res=[x for x in rows[r:] if x]
    allint=internal_cols();free=[c for c in allint if c not in set(piv)]
    assert len(free)==128-r

    extra={}
    js=range(1,4) if ad else range(1,5)
    for j in js:
        for i in range(31):
            u,v,w=F[j,i,'u'],F[j,i,'v'],F[j,i,'w']
            a=T.xx(u,v)[0];b=T.xx(u,w)[0]
            extra[j,i]=(reduce_by_pivots(a,pivrows,piv),reduce_by_pivots(b,pivrows,piv))
    return F,res,free,extra


def left_space(base_res,free,extra,zs):
    rows=list(base_res)
    for z in zs:rows.extend(extra[z])
    r=0
    for col in free:
        p=next((k for k in range(r,len(rows)) if (rows[k]>>col)&1),None)
        if p is None:continue
        rows[r],rows[p]=rows[p],rows[r]
        for k in range(len(rows)):
            if k!=r and ((rows[k]>>col)&1):rows[k]^=rows[r]
        r+=1
    # Full internal rank iff all base-null directions are killed.
    if r<len(free):return None
    extrows=rows[r:]
    left=[]
    for row in extrows:
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


def enumerate_space(B):
    out={0}
    for b in B:out|={x^b for x in list(out)}
    return out


def validate_bc():
    # Compare fast homogeneous left spaces to full canonical supports on the
    # four known weight122 rank128 pairs.
    pairs=[((1,0),(2,0)),((1,0),(4,0)),((2,0),(3,0)),((3,0),(4,0))]
    for pos in 'BC':
        F,res,free,extra=setup(pos,False)
        for z in pairs:
            fast=set(enumerate_space(left_space(res,free,extra,z)))
            can=D.canonical_external_constraints(pos,D.carries(z))
            # convert old 160-bit canonical rows to left beta rowspace
            rows=[]
            for row in can:
                m=row&((1<<160)-1);v=0
                for q,i in enumerate(S):
                    if (m>>(128+i))&1:v|=1<<q
                if v:rows.append(v)
            B={}
            for x in rows:
                while x:
                    p=x.bit_length()-1
                    if p not in B:B[p]=x;break
                    x^=B[p]
            slow=enumerate_space(list(B.values()))
            assert fast==slow,(pos,z,len(fast),len(slow))


def run_bc_weight120():
    sites=[(j,i) for j in range(1,5) for i in range(31)]
    for pos in 'BC':
        F,res,free,extra=setup(pos,False);U=set();tested=full=0;growth=[]
        for z in itertools.combinations(sites,4):
            tested+=1
            B=left_space(res,free,extra,z)
            if B is None:continue
            full+=1
            before=len(U);U|=enumerate_space(B)
            if len(U)>before and len(growth)<30:growth.append((tested,z,len(B),len(U)))
            if len(U)==2048:break
        print('BC_weight120',pos,'tested',tested,'fullrank_patterns_seen',full,
              'left_frequency_union',len(U),'saturated',len(U)==2048,
              'growth',repr(growth),flush=True)


def run_ad_weight90():
    sites=[(j,i) for j in range(1,4) for i in range(31)]
    special={(1,0),(3,0)}
    triples=[z for z in itertools.combinations(sites,3) if set(z)&special]
    assert len(triples)==8281
    for pos in 'AD':
        F,res,free,extra=setup(pos,True);U=set();full=0;growth=[]
        for idx,z in enumerate(triples,1):
            B=left_space(res,free,extra,z)
            assert B is not None,(pos,z)
            full+=1
            before=len(U);U|=enumerate_space(B)
            if len(U)>before and len(growth)<30:growth.append((idx,z,len(B),len(U)))
            if len(U)==2048:break
        print('AD_weight90',pos,'tested',idx,'fullrank_seen',full,
              'left_frequency_union',len(U),'saturated',len(U)==2048,
              'growth',repr(growth),flush=True)


def main():
    validate_bc()
    print('FAST_QUOTIENT_VALIDATED_AGAINST_WEIGHT122_FULL_CANONICAL')
    run_bc_weight120()
    run_ad_weight90()
    print('PASS PROBE V26_Q138_FAST_NULLSPACE_FOURIER')
    print('scope=homogeneous frequency saturation probes only; no next-residue theorem')

if __name__=='__main__':main()
