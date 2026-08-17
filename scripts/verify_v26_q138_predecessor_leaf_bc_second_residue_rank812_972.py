#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import verify_v26_q138_predecessor_leaf_bc_second_residue_support_frequency_nesting as N


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


def main():
    expected={'B':(668,348,144,812),'C':(788,432,184,972)}
    for pos in 'BC':
        U=N.weight120_union(pos)
        support,sign,proj,total=expected[pos]
        assert len(U)==support
        E=S.grouped_e0_basis(pos);H=S.half_basis(pos);G=S.union_basis(E,H)
        assert len(G)==sign
        qr,comp=quotient_rank(G,U)
        assert qr==proj,(pos,qr,proj)
        assert len(U)+qr==total
        print('position',pos,'support_Walsh_dim',len(U),
              'sign_GF2_basis_dim',len(G),'Walsh_complement_coordinates',comp,
              'exact_ZZ_quotient_rank',qr,'combined_second_lift_rank<=',total,flush=True)
    print('PASS V26_Q138_PREDECESSOR_LEAF_BC_SECOND_RESIDUE_RANK812_972')
    print('B_second_integer_lift_rank_Q<=812')
    print('C_second_integer_lift_rank_Q<=972')
    print('supersedes_component_sum_bounds=1016,1220')
    print('scope=second dyadic integer lifts only; no full leaf Schmidt-rank or arithmetic-work claim')

if __name__=='__main__':main()
