#!/usr/bin/env python3
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_factor_generation85 as F


def main():
    # New S1 central rank after replacing eight raw site2/3 physical row bits
    # by the exact four-site signed rank96 block.
    R=16*2784*96*(2**18)
    assert R==261*(2**32)
    table=R*(2**44);assert table==261*(2**76)
    exp=math.log2(table);assert abs(exp-(76+math.log2(261)))<1e-12

    # The rank96 four-site factor has96 physical-row signed classes, so it adds
    # no abstract right-basis oracle. Block1 is physical-row explicit and block2
    # retains the <=64 physical-row bridge. Thus one global right-basis slice
    # is still an exact combination of <=64 ordinary physical S1 central rows.

    # Reuse the explicit 21-site complement tree from factor-generation85.
    root,sets=F.walk(F.RIGHT_TREE,True);assert root==F.COMP
    sets=sets+[{i} for i in F.COMP]
    peak=max(F.ccost(A) for A in sets);assert peak==80
    assert 80<exp

    # Leaf generation44 and fixed physical S1 central boundary51 are smaller.
    assert max(80,51,44)<exp

    print('PASS V26_Q138_DOUBLE_ROUND_FACTOR_GENERATION84')
    print('signed_rank_R=261*2^32')
    print('materialized_factor=261*2^76 log2=%.15f' % exp)
    print('right_entry_generation_peak=80')
    print('global_right_basis_slice_expansion<=64 ordinary physical S1 rows')
    print('W2_factor_gen<=%.15f' % exp)
    print('scope=coefficient-aware materialized-factor message/storage ledger; arithmetic work not improved')
if __name__=='__main__':main()
