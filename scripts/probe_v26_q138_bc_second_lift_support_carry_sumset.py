#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_bc_second_residue_support_frequency_nesting as N


def xor_sumset(U):
    U=list(U)
    return {a^b for a in U for b in U}


def main():
    expected={'B':668,'C':788}
    for pos in 'BC':
        U=N.weight120_union(pos)
        assert len(U)==expected[pos],(pos,len(U))
        S=xor_sumset(U)
        print('position',pos,'second_support_frequency_space',len(U),
              'pairwise_xor_sumset',len(S),'missing_from_full2048',2048-len(S),flush=True)
    print('PASS PROBE V26_Q138_BC_SECOND_LIFT_SUPPORT_CARRY_SUMSET')
    print('interpretation=natural integer support-lift XOR-vs-sum third-bit carry has left frequencies inside U120 xor U120; if sumset=2048 this coarse route gives no subgeneric correction bound')
    print('scope=coarse support-lift carry correction only; no complete b2/c2 claim')

if __name__=='__main__':main()
# clean PR trigger v2
