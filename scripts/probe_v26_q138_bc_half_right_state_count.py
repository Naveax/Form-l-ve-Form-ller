#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_bc_input_activity_no_gain as N
import probe_v26_q138_predecessor_leaf_bc_half_correction_fullrank_witness as H
import probe_v26_q138_predecessor_leaf_bc_half_correction_active_fast as F


def state_count(pos,input128):
    eq=H.common_support_data(pos,input128)
    stable=F.support_table(eq)
    phase=[]
    for z in H.SECTORS:
        qleft,cross,terms=H.sector_phase_data(pos,z,input128)
        lin,const,adj=F.right_quadratic(terms)
        phase.append((cross,lin,const,adj))
    syn=0;y=0;prev=0
    qR=[d[2] for d in phase];shift=[0]*4
    states=set();active_states=set()
    for step in range(1<<21):
        if step:
            gray=step^(step>>1);diff=gray^prev;t=(diff&-diff).bit_length()-1
            oldy=y
            for i,(cross,lin,const,adj) in enumerate(phase):
                qR[i]^=((lin>>t)&1)^((adj[t]&oldy).bit_count()&1)
                shift[i]^=cross[t]
            for j,(lm,rm,rhs) in enumerate(eq):
                if (rm>>t)&1:syn^=1<<j
            y^=1<<t;prev=gray
        st=syn;sh=8
        for i in range(4):
            st|=shift[i]<<sh;sh+=11
            st|=qR[i]<<sh;sh+=1
        states.add(st)
        if stable[syn]:active_states.add(st)
    return len(states),len(active_states)


def main():
    for pos in 'BC':
        can=N.residue_objects(pos)[0][-1]
        sol=T.rref(N.input_equations(can),n=128);assert sol is not None
        rank,x0,basis=sol;assert rank==5
        for name,x in [('base',x0)]+[(f'shift{k}',x0^basis[k]) for k in range(3)]:
            ns,na=state_count(pos,x)
            print('position',pos,'case',name,'right_state_count',ns,'active_support_state_count',na,flush=True)
    print('PASS PROBE V26_Q138_BC_HALF_RIGHT_STATE_COUNT')
    print('scope=distinct exact right-state signatures controlling half-correction columns; tested fixed inputs only')

if __name__=='__main__':main()
