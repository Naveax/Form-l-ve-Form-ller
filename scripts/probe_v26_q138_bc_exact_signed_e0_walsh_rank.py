#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
import verify_v26_q138_predecessor_leaf_bc_fourier_lift_rank36_84 as F0
import verify_v26_q138_predecessor_leaf_bc_input_activity_no_gain as N0
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as F
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S


def fwht(bits):
    a=[1 if (bits>>x)&1 else 0 for x in range(2048)]
    h=1
    while h<2048:
        for i in range(0,2048,2*h):
            for j in range(i,i+h):
                x=a[j];y=a[j+h]
                a[j]=x+y;a[j+h]=x-y
        h*=2
    return a


def quotient_rank(B,U):
    comp=[i for i in range(2048) if i not in U]
    rows=[]
    for v in B.values():
        w=fwht(v);rows.append([w[i] for i in comp])
    return DomainMatrix.from_list(rows,ZZ).rank(),len(comp)


def support_union(pos):
    objs,total=N0.residue_objects(pos)
    affine=objs[:-1]
    assert len(affine)==103
    U=set()
    for can in affine:
        BL=F.rowspace_basis(can,F.S)
        U |= F.enumerate_space(BL)
    return U


def main():
    for pos in 'BC':
        U=support_union(pos)
        expected_u=16 if pos=='B' else 64
        assert len(U)==expected_u,(pos,len(U))
        E=S.grouped_e0_basis(pos)
        expected_e=272 if pos=='B' else 388
        assert len(E)==expected_e,(pos,len(E))
        qr,comp=quotient_rank(E,U)
        total=len(U)+qr
        print('position',pos,
              'e0_support_Walsh_dim',len(U),
              'grouped_e0_sign_GF2_basis_dim',len(E),
              'Walsh_complement_coordinates',comp,
              'exact_ZZ_sign_quotient_rank',qr,
              'exact_signed_e0_left_space_rank_bound',total,flush=True)
        # Exact signed raw-e0 aggregate = support-sum - 2*negative-sign part.
        # Multiplying the sign part by -2 does not change its rational left
        # factor span. Hence support space + exact sign quotient gives a valid
        # uniform rational rank bound for the complete exact signed e0 family.
        assert total<=2048
    print('PASS PROBE V26_Q138_BC_EXACT_SIGNED_E0_WALSH_RANK')
    print('scope=exact-signed valuation-e0 aggregate left-factor upper bound only; dyadic lift/correction theorem requires comparing this bound with the existing K0 choice')

if __name__=='__main__':main()
