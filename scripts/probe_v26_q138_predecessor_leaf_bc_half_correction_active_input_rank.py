#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_bc_input_activity_no_gain as N
import probe_v26_q138_predecessor_leaf_bc_half_correction_fullrank_witness as H


def common_support(pos):
    objs,total=N.residue_objects(pos)
    can=objs[-1]
    return can


def main():
    for pos in 'BC':
        can=common_support(pos)
        eq=N.input_equations(can)
        sol=T.rref(eq,n=128)
        assert sol is not None
        rank,x0,basis=sol
        print('position',pos,'common_support_input_condition_rank',rank,
              'coset_dimension',len(basis),'canonical_active_input',hex(x0),flush=True)
        r,y,n=H.run(pos,x0)
        print('position',pos,'active_input_half_correction_rank',r,
              'right_processed',y,'nonzero_columns',n,flush=True)
        # Also test the first few independent coset shifts to see whether rank is stable.
        for j,b in enumerate(basis[:3]):
            xx=x0^b
            r2,y2,n2=H.run(pos,xx)
            print('position',pos,'shift',j,'input',hex(xx),'rank',r2,
                  'right_processed',y2,'nonzero_columns',n2,flush=True)
    print('PASS PROBE V26_Q138_BC_HALF_CORRECTION_ACTIVE_INPUT_RANK')
    print('scope=fixed active-input GF2 rank witnesses for half-sector second correction; not a uniform upper bound')

if __name__=='__main__':main()
