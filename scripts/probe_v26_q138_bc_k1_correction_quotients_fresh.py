#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from sympy.polys.domains import GF
from sympy.polys.matrices import DomainMatrix
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import verify_v26_q138_predecessor_leaf_bc_second_residue_support_frequency_nesting as N

P=65521


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


def qr_mod(B,U):
    comp=[i for i in range(2048) if i not in U]
    rows=[[fwht(v)[i] % P for i in comp] for v in B.values()]
    return DomainMatrix.from_list(rows,GF(P)).rank()


def union(*Bs):
    return S.union_basis(*Bs)


def main():
    # Canonical exact ZZ combined-quotient theorem:
    # B:668+144=812, C:788+184=972.
    expected={'B':(668,144,812),'C':(788,184,972)}
    for pos in 'BC':
        U=N.weight120_union(pos)
        E=S.grouped_e0_basis(pos)
        H=S.half_basis(pos)
        G=union(E,H)
        base,qG,total=expected[pos]
        assert len(U)==base and base+qG==total
        # By construction span(E),span(H) are subspaces of span(G)=span(E union H).
        assert len(G)==(348 if pos=='B' else 432)

        mE=qr_mod(E,U);mH=qr_mod(H,U)
        # For integer matrices rank_Fp <= rank_Q. Since E,H are subspaces of G,
        # rank_Q(E/W), rank_Q(H/W) <= rank_Q(G/W)=qG. Equality of the modular
        # lower bound with qG therefore certifies exact rational equality.
        certE=(mE==qG);certH=(mH==qG)
        print('position',pos,'direct_e1_support_dim',base,
              'combined_exact_quotient_rank',qG,
              'e0_correction_basis_dim',len(E),'e0_modp_quotient_rank',mE,
              'e0_exact_equals_combined_if_true',certE,
              'half_correction_basis_dim',len(H),'half_modp_quotient_rank',mH,
              'half_exact_equals_combined_if_true',certH,
              'K1_if_e0_removed_upper_if_half_full',base+qG if certH else 'unresolved',
              'K1_if_half_removed_upper_if_e0_full',base+qG if certE else 'unresolved',
              'K1_if_both_removed',base,flush=True)

    print('PASS PROBE V26_Q138_BC_K1_CORRECTION_QUOTIENTS_MODULAR')
    print('scope=mod-p lower certificates plus canonical exact combined-quotient upper; equality certifies whether either correction family alone already fills the full K1 quotient')

if __name__=='__main__':main()
