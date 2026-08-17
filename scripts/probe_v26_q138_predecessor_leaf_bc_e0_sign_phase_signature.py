#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_predecessor_leaf_bc_e0_sign_left_factors as E
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as F


def add_basis(Basis,x):
    y=x
    while y:
        p=y.bit_length()-1
        if p not in Basis:
            Basis[p]=y;return True
        y^=Basis[p]
    return False


def main():
    e0,e1,half=H.classify_patterns()
    for pos in 'BC':
        Basis={};seen=set();consistent=0
        for k in range(4):
            for zs,cls in e0[k]:
                can=H.support_for(pos,zs,cls)
                if can is None:continue
                consistent+=1
                Cmask=D.carries(zs);sol=A.internal_null(pos,Cmask)
                dirs,pr=B.radical_directions(pos,sol[2])
                FF=D.full_forms(pos)
                extras=[A.derivative_form(FF,A.map_internal_to_full(d)) for d in dirs]
                qbits,crossB,rank=E.left_chirp_and_cross(pos,Cmask,extras)
                SF=F.enumerate_space(F.rowspace_basis(can,F.S));CF=F.enumerate_space(crossB)
                for a in SF:
                    for b in CF:
                        v=E.canonical_sign_vector(qbits,a^b)
                        if v in seen:continue
                        seen.add(v);add_basis(Basis,v)
        basis=list(Basis.values())
        r=len(basis)
        sigs=set()
        for x in range(2048):
            s=0
            for i,q in enumerate(basis):
                s|=((q>>x)&1)<<i
            sigs.add(s)
        print('position',pos,'consistent_e0_sectors',consistent,
              'distinct_sign_left_factors_up_to_scalar',len(seen),
              'boolean_phase_span_rank',r,
              'distinct_evaluation_signatures',len(sigs),
              'uniform_Q_span_upper_bound_for_all_phase_sign_vectors',len(sigs),flush=True)
    print('PASS PROBE V26_Q138_BC_E0_SIGN_PHASE_SIGNATURE')
    print('lemma=for phase space V, sign-character span dimension is bounded by number of distinct evaluation functionals x->(q_i(x)) on the left domain')
    print('scope=e0 sign left-factor family only; support/right assembly and half-sector correction separate')

if __name__=='__main__':main()
