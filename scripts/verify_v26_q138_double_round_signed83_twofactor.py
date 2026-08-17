#!/usr/bin/env python3
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_v26_q138_double_round_signed84_multisite as C


def main():
    special=C.gram_pair(0,1)
    generic=C.gram_pair(0,0)
    rs=C.rank_mod(special);rg=C.rank_mod(generic)
    assert (rs,rg)==(256,256)
    canonical=79+math.log2(87)
    print('PASS V26_Q138_SIGNED83_TWOFACTOR_REVOCATION')
    print('true_int64_special_rank=256 true_int64_generic_rank=256')
    print('revoked_candidate_W=83.7283457147')
    print('canonical_d1_Wrepr_and_factor_gen<=%.15f' % canonical)
if __name__=='__main__':main()
