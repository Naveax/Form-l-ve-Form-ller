#!/usr/bin/env python3
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed84_multisite as C


def main():
    # Corrected nonoverflowing four-site Grams are full rank, so the premise of
    # the historical factor-generation84 candidate is false.
    special=C.gram_pair(0,1);generic=C.gram_pair(0,0)
    assert C.rank_mod(special)==256
    assert C.rank_mod(generic)==256
    canonical=79+math.log2(87)
    print('PASS V26_Q138_FACTOR_GENERATION84_REVOCATION')
    print('false_rank96_and_rank208_candidates_rejected_by_true_int64_grams')
    print('canonical_W2_factor_gen<=%.15f' % canonical)
    print('authority=V26_Q138_DOUBLE_ROUND_FACTOR_GENERATION85_THEOREM')
if __name__=='__main__':main()
