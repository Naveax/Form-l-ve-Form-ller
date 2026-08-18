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


def qr(B,U):
    comp=[i for i in range(2048) if i not in U]
    rows=[[fwht(v)[i] for i in comp] for v in B.values()]
    return DomainMatrix.from_list(rows,ZZ).rank()


def union(*Bs):
    return S.union_basis(*Bs)


def main():
    for pos in 'BC':
        U=N.weight120_union(pos)
        E=S.grouped_e0_basis(pos)
        H=S.half_basis(pos)
        G=union(E,H)
        qE=qr(E,U);qH=qr(H,U);qG=qr(G,U)
        base=len(U)
        print('position',pos,'direct_e1_support_dim',base,
              'e0_correction_basis_dim',len(E),'e0_quotient_rank',qE,
              'half_correction_basis_dim',len(H),'half_quotient_rank',qH,
              'combined_sign_basis_dim',len(G),'combined_quotient_rank',qG,
              'K1_with_both_corrections<=',base+qG,
              'K1_if_e0_removed<=',base+qH,
              'K1_if_half_removed<=',base+qE,
              'K1_if_both_removed<=',base,flush=True)
        assert base+qG==(812 if pos=='B' else 972)
    print('PASS PROBE V26_Q138_BC_K1_CORRECTION_QUOTIENTS')
    print('scope=exact ZZ Walsh quotient decomposition of the current K1 correction spaces; no alternative K0 rank is assumed')

if __name__=='__main__':main()
