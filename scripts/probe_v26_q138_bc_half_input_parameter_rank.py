#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_bc_input_activity_no_gain as N
import probe_v26_q138_predecessor_leaf_bc_half_correction_fullrank_witness as H
import probe_v26_q138_predecessor_leaf_bc_half_correction_active_fast as F

SECTORS=H.SECTORS


def affine_truth_params(bits):
    # Return (freq11,const) for an affine Boolean truth vector; accept complement.
    for f,w in enumerate(H.WALSH):
        if bits==w:return f,0
        if bits==(w^H.ALL):return f,1
    raise AssertionError('non-affine left phase delta')


def input_params(pos,x):
    out=0;shift=0
    # phase parameters: per sector left affine delta (12), right linear21+const1.
    for z in SECTORS:
        qleft,cross,terms=H.sector_phase_data(pos,z,x)
        lin,const,adj=F.right_quadratic(terms)
        # qleft itself is quadratic, so caller will xor against base before decoding.
        out |= qleft<<shift; shift+=2048
        out |= lin<<shift; shift+=21
        out |= (const&1)<<shift; shift+=1
    return out


def main():
    for pos in 'BC':
        can=N.residue_objects(pos)[0][-1]
        sol=T.rref(N.input_equations(can),n=128);assert sol is not None
        rank,x0,basis=sol
        assert rank==5 and len(basis)==123

        base=[]
        for z in SECTORS:
            qleft,cross,terms=H.sector_phase_data(pos,z,x0)
            lin,const,adj=F.right_quadratic(terms)
            base.append((qleft,lin,const,tuple(adj)))

        vectors=[]
        for b in basis:
            packed=0;sh=0
            for i,z in enumerate(SECTORS):
                qleft,cross,terms=H.sector_phase_data(pos,z,x0^b)
                lin,const,adj=F.right_quadratic(terms)
                assert tuple(adj)==base[i][3]
                df,dc=affine_truth_params(qleft^base[i][0])
                packed |= df<<sh; sh+=11
                packed |= dc<<sh; sh+=1
                packed |= (lin^base[i][1])<<sh; sh+=21
                packed |= ((const^base[i][2])&1)<<sh; sh+=1
            vectors.append(packed)

        pr=T.gf2_rank(vectors,4*(11+1+21+1))
        print('position',pos,'active_input_coset_dimension',len(basis),
              'half_correction_phase_parameter_image_rank',pr,
              'parameter_state_count_if_full_image',1<<pr if pr<63 else 'huge',flush=True)

    print('PASS PROBE V26_Q138_BC_HALF_INPUT_PARAMETER_RANK')
    print('scope=rank of active-input coset image into affine phase-shift parameters; support-offset parameters excluded because common support translations preserve rectangle dimensions but may still affect assembled rank')

if __name__=='__main__':main()
