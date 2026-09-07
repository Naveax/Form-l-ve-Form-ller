#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_bc_direct_e1_aggregate_mod3_rank as G

EXTENDED_COLUMNS = 1 << 14  # 16384 deterministic Gray-code columns


def main():
    G.MAX_COLUMNS = EXTENDED_COLUMNS
    rank, used = G.run_position('B')
    assert rank >= 1536, (rank, used)
    if rank == G.NROW:
        print('PASS PROBE V26_Q138_B_DIRECT_E1_AGGREGATE_MOD3_FULL_RANK_EXTENDED')
        print('theorem=at the deterministic reachable predecessor witness, the complete direct-e1 B aggregate has rank_F3=2048, hence exact rank_Q=2048')
        print('columns_examined', used)
        print('consequence=no uniform subgeneric rational-rank upper bound exists for the complete direct-e1 B aggregate')
    else:
        print('PASS PROBE V26_Q138_B_DIRECT_E1_AGGREGATE_MOD3_EXTENDED_LOWER_BOUND')
        print('rank_F3_lower_bound', rank, 'columns_examined', used)
        print('scope=extended deterministic sampled-column lower bound only; non-full result is not an upper bound')


if __name__ == '__main__':
    main()
