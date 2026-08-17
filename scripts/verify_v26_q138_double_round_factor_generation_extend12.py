#!/usr/bin/env python3
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_factor_generation85 as F


def main():
    # Exact extended block2 rank from the clean Fraction theorem.
    E=21888
    R=16*E*(2**23)
    old=16*2784*(2**26)
    assert R*58==old*57

    table=R*(2**44)
    exp=math.log2(table)
    assert abs(exp-(85.44294349584872-math.log2(58/57)))<1e-12

    # The extended local block has 2^16 physical rows and 2^22 retained columns.
    # Brute-force exact materialization/Gaussian selection of a physical row basis
    # is itself far below the global factor size in the memory/message ledger.
    full_local=(2**16)*(2**22)
    local_U=(2**16)*E
    local_V=E*(2**22)
    assert full_local==2**38
    assert max(full_local,local_U,local_V)<2**39

    # Reuse the clean 21-site complement tree; fixed-physical-row right-entry
    # generation peak stays80.
    root,sets=F.walk(F.RIGHT_TREE,True);assert root==F.COMP
    peak=max(F.ccost(A) for A in sets+[{i} for i in F.COMP]);assert peak==80
    assert peak<exp

    print('PASS V26_Q138_DOUBLE_ROUND_FACTOR_GENERATION_EXTEND12')
    print('extended_block2_rank=21888')
    print('central_S1_rank=16*21888*2^23=%d' % R)
    print('materialized_factor_entries=%d log2=%.15f' % (table,exp))
    print('local_bruteforce_matrix=2^38 local_U_log2=%.15f local_V_log2=%.15f' % (math.log2(local_U),math.log2(local_V)))
    print('right_entry_generation_peak=80')
    print('W2_factor_gen<=%.15f' % exp)
    print('scope=coefficient-aware materialized-factor memory/message ledger; arithmetic work not reduced')
if __name__=='__main__':main()
