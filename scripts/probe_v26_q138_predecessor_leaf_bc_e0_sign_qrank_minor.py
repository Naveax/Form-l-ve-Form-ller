#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
from flint import nmod_mat
import probe_v26_q138_predecessor_leaf_bc_e0_sign_left_factors as E
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_first_dyadic_rank1160 as B
import probe_v26_q138_predecessor_leaf_ad_affine_fourier_union as F

P=65521
TARGET=2048


def collect(pos,limit=TARGET):
    e0,e1,half=H.classify_patterns();seen=set();out=[]
    for k in range(4):
        for zs,cls in e0[k]:
            can=H.support_for(pos,zs,cls)
            if can is None:continue
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
                    seen.add(v);out.append(v)
                    if len(out)>=limit:return out
    return out


def row(v):
    return [(P-1 if (v>>i)&1 else 1) for i in range(TARGET)]


def main():
    for pos in 'BC':
        vs=collect(pos,TARGET)
        assert len(vs)==TARGET,(pos,len(vs))
        M=nmod_mat([row(v) for v in vs],P)
        r=M.rank()
        print('position',pos,'deterministic_sign_vectors',len(vs),'modulus',P,
              'minor_rank_mod_p',r,'full',r==TARGET,flush=True)
    print('PASS PROBE V26_Q138_BC_E0_SIGN_QRANK_MINOR')
    print('scope=mod-p rank of first deterministic 2048 left sign factors; full rank proves rational left-factor span2048, deficiency does not by itself upper-bound full family')

if __name__=='__main__':main()
