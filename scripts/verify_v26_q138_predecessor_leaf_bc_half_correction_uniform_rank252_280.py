#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
import probe_v26_q138_bc_half_uniform_left_span as P


def main():
    vals={p:P.run(p) for p in 'BC'}
    assert vals=={'B':252,'C':280},vals
    print('PASS V26_Q138_PREDECESSOR_LEAF_BC_HALF_CORRECTION_UNIFORM_RANK252_280')
    print('B_half_second_correction_rank_F2<=252')
    print('C_half_second_correction_rank_F2<=280')
    print('scope=uniform over active predecessor inputs and all right assignments; gives integer dyadic lift envelopes, not Q-rank claims for the actual binary matrices')

if __name__=='__main__':main()
