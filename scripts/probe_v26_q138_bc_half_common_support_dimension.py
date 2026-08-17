#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_bc_input_activity_no_gain as N
import probe_v26_q138_predecessor_leaf_bc_half_correction_fullrank_witness as H


def main():
    for pos in 'BC':
        can=N.residue_objects(pos)[0][-1]
        ieq=N.input_equations(can);isol=T.rref(ieq,n=128);assert isol is not None
        irank,input0,ibasis=isol
        eq=[]
        for row in can:
            ext=row&((1<<160)-1);rhs=(row>>160)&1
            lm,rm,im=H.split_ext(ext)
            rhs ^= (im&input0).bit_count()&1
            beta=0
            for q,i in enumerate(H.S):
                if (lm>>q)&1:beta|=1<<i
            for q,i in enumerate(H.R):
                if (rm>>q)&1:beta|=1<<i
            eq.append((beta,rhs))
        sol=T.rref(eq,n=32);assert sol is not None
        brank,beta0,bbasis=sol
        print('position',pos,'input_condition_rank',irank,'input_coset_dimension',len(ibasis),
              'active_input',hex(input0),'beta_support_rank',brank,
              'beta_support_dimension',len(bbasis),'beta_support_size',1<<len(bbasis),
              'beta_particular',hex(beta0),flush=True)
    print('PASS PROBE V26_Q138_BC_HALF_COMMON_SUPPORT_DIMENSION')

if __name__=='__main__':main()
