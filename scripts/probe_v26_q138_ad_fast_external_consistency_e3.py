#!/usr/bin/env python3
import itertools,sys
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A

SITES=[(j,i) for j in range(1,4) for i in range(31)]
SPECIAL={(1,0),(3,0)}
NONSPECIAL=[z for z in SITES if z not in SPECIAL]
SID={z:k for k,z in enumerate(SITES)}
assert len(SITES)==93 and len(NONSPECIAL)==91


def aff(const=0,sites=()):
    x=const&1
    for z in sites:x ^= 1<<(1+SID[z])
    return x


def ev_aff(e,Zmask):
    # bit0 is the constant; site k is bit1+k.
    return ((e & (1 | (Zmask<<1))).bit_count() & 1)


def zero_mask(Z):
    m=0
    for z in Z:m |= 1<<SID[z]
    return m


def add_form_eq(out,f,rhs_carry=0,lambda_sites=()):
    m,c=f
    out.append((m,aff(c^rhs_carry,lambda_sites)))


def build_base(pos,with_derivative):
    F=D.full_forms(pos)
    out=[]
    # j1..j3: top pattern has carries1. The coefficient rows at bits1..31
    # are always present; only their RHS changes affinely with zero indicators.
    for j in range(1,4):
        for i in range(1,31):
            add_form_eq(out,T.xx(F[j,i,'u'],F[j,i,'v'],F[j,i,'w']),0,((j,i-1),(j,i)))
        # bit31: u=v and u=w are fixed; the triple RHS is top1 xor z30.
        add_form_eq(out,T.xx(F[j,31,'u'],F[j,31,'v']))
        add_form_eq(out,T.xx(F[j,31,'u'],F[j,31,'w']))
        add_form_eq(out,T.xx(F[j,31,'u'],F[j,31,'v'],F[j,31,'w']),1,((j,30),))

    # j4 is forced carry-zero for A/D and has no variable zero indicators.
    j=4
    add_form_eq(out,T.xx(F[j,0,'u'],F[j,0,'v']))
    add_form_eq(out,T.xx(F[j,0,'u'],F[j,0,'w']))
    for i in range(1,31):
        add_form_eq(out,T.xx(F[j,i,'u'],F[j,i,'v'],F[j,i,'w']))
        add_form_eq(out,T.xx(F[j,i,'u'],F[j,i,'v']))
        add_form_eq(out,T.xx(F[j,i,'u'],F[j,i,'w']))
    add_form_eq(out,T.xx(F[j,31,'u'],F[j,31,'v']))
    add_form_eq(out,T.xx(F[j,31,'u'],F[j,31,'w']))
    add_form_eq(out,T.xx(F[j,31,'u'],F[j,31,'v'],F[j,31,'w']))

    if with_derivative:
        top=A.internal_null(pos,D.carries([],ad=True))
        assert top is not None and top[0]==127 and len(top[2])==1
        der=A.derivative_form(F,A.map_internal_to_full(top[2][0]))
        add_form_eq(out,der)
    return F,out


def echelon_symbolic(rows):
    # Gaussian elimination on coefficient rows, while tracking the affine RHS
    # expression in the93 zero indicators. Zero coefficient rows become exact
    # affine consistency constraints on the carry-zero pattern.
    B={};constraints=[]
    for row,e in rows:
        y=row;ee=e
        while y:
            p=y.bit_length()-1
            if p in B:
                r,re=B[p];y^=r;ee^=re
            else:
                B[p]=(y,ee);break
        if not y and ee:constraints.append(ee)
    return B,tuple(constraints)


def reduce_extra(B,row,e):
    y=row;ee=e
    while y:
        p=y.bit_length()-1
        if p not in B:break
        r,re=B[p];y^=r;ee^=re
    return y,ee


def prepare(pos,with_derivative):
    F,base=build_base(pos,with_derivative)
    B,constraints=echelon_symbolic(base)
    extras={}
    for z in SITES:
        j,i=z
        q=[]
        for f in (T.xx(F[j,i,'u'],F[j,i,'v']),T.xx(F[j,i,'u'],F[j,i,'w'])):
            m,c=f
            q.append(reduce_extra(B,m,aff(c)))
        extras[z]=tuple(q)
    return B,constraints,extras


def consistent(prep,Z):
    _B,constraints,extras=prep
    zm=zero_mask(Z)
    if any(ev_aff(e,zm) for e in constraints):return False
    # Solve only the reduced equality rows selected by the zero sites.
    basis={}
    for z in Z:
        for q,e in extras[z]:
            rhs=ev_aff(e,zm)
            y=q;bb=rhs
            while y:
                p=y.bit_length()-1
                if p in basis:
                    r,b=basis[p];y^=r;bb^=b
                else:
                    basis[p]=(y,bb);break
            if not y and bb:return False
    return True


def families(e):
    # Direct valuation-e candidates from the rank127/rank128 zero-set law:
    # e nonspecial zeros (nullity1) and e+1 zeros containing >=1 special (full).
    nulls=itertools.combinations(NONSPECIAL,e)
    fulls=[]
    for s in sorted(SPECIAL):
        fulls.extend(tuple(sorted((s,)+zs)) for zs in itertools.combinations(NONSPECIAL,e))
    if e>=1:
        sp=tuple(sorted(SPECIAL))
        fulls.extend(tuple(sorted(sp+zs)) for zs in itertools.combinations(NONSPECIAL,e-1))
    assert len(fulls)==2*__import__('math').comb(91,e)+(__import__('math').comb(91,e-1) if e>=1 else 0)
    assert len(set(fulls))==len(fulls)
    return nulls,fulls


def count_family(prep_null,prep_full,e,collect_bad=False):
    nulls,fulls=families(e)
    rn=bn=rf=bf=0;badn=[];badf=[]
    for Z in nulls:
        if consistent(prep_null,Z):rn+=1
        else:
            bn+=1
            if collect_bad:badn.append(Z)
    for Z in fulls:
        if consistent(prep_full,Z):rf+=1
        else:
            bf+=1
            if collect_bad:badf.append(Z)
    return (rn,bn,rf,bf,badn,badf)


def main():
    known={
        'A':{1:(90,1,181,2),2:(4003,92,8095,186)},
        'D':{1:(91,0,183,0),2:(4091,4,8272,9)},
    }
    for pos in 'AD':
        pn=prepare(pos,True)
        pf=prepare(pos,False)
        print('position',pos,'null_base_rank',len(pn[0]),'null_symbolic_constraints',len(pn[1]),
              'full_base_rank',len(pf[0]),'full_symbolic_constraints',len(pf[1]),flush=True)
        for e in (1,2):
            got=count_family(pn,pf,e,collect_bad=(e==2))
            tup=got[:4]
            assert tup==known[pos][e],(pos,e,tup,known[pos][e])
            print('position',pos,'validation_e',e,
                  'null_reachable_impossible',tup[:2],
                  'full_reachable_impossible',tup[2:4],flush=True)
            if e==2:
                print('position',pos,'e2_null_impossible_examples',got[4][:16],flush=True)
                print('position',pos,'e2_full_impossible_examples',got[5][:16],flush=True)

        e=3
        got=count_family(pn,pf,e)
        rn,bn,rf,bf=got[:4]
        assert rn+bn==121485
        assert rf+bf==247065
        print('position',pos,'DIRECT_E3_EXTERNAL_COUNTS',
              'null3_reachable',rn,'null3_impossible',bn,
              'full4_reachable',rf,'full4_impossible',bf,
              'total_reachable',rn+rf,'total_impossible',bn+bf,flush=True)

    print('PASS PROBE V26_Q138_AD_FAST_EXTERNAL_CONSISTENCY_E3')
    print('scope=exact external reachability counts for direct valuation-e3 families after validating the quotient solver against all known e1/e2 counts; no map-cover/rank claim')

if __name__=='__main__':main()
