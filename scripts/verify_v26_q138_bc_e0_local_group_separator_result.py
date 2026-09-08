#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_local_group_separator as P

EXPECTED = {
    'B': {
        'groups': 251,
        'global': {'support': 149, 'frequency': 149, 'combined': 149},
        'local_hist': {20: 4, 21: 104, 22: 35, 23: 18, 24: 8, 25: 67, 26: 14, 28: 1},
        'max_pair_overlap': 24,
        'balanced': {
            'name': 'multiplicity_half',
            'left_groups': 125,
            'right_groups': 126,
            'left_rank': 61,
            'right_rank': 149,
            'lambda': 61,
        },
        'path_max': {
            'canonical': 124,
            'local_rank_ascending': 85,
            'local_rank_descending': 96,
            'multiplicity_then_rank': 85,
        },
    },
    'C': {
        'groups': 250,
        'global': {'support': 149, 'frequency': 147, 'combined': 149},
        'local_hist': {19: 4, 20: 14, 21: 87, 22: 16, 23: 36, 24: 10, 25: 71, 26: 11, 27: 1},
        'max_pair_overlap': 24,
        'balanced': {
            'name': 'multiplicity_half',
            'left_groups': 125,
            'right_groups': 125,
            'left_rank': 57,
            'right_rank': 149,
            'lambda': 57,
        },
        'path_max': {
            'canonical': 114,
            'local_rank_ascending': 92,
            'local_rank_descending': 89,
            'multiplicity_then_rank': 92,
        },
    },
}


def main():
    out = {pos: P.analyze(pos) for pos in 'BC'}
    for pos, exp in EXPECTED.items():
        got = out[pos]
        assert got['support_groups'] == exp['groups'], (pos, got['support_groups'])
        assert got['global_ranks'] == exp['global'], (pos, got['global_ranks'])
        assert got['local_combined_rank_histogram'] == exp['local_hist'], (
            pos,
            got['local_combined_rank_histogram'],
        )
        assert got['max_pair_overlap']['dimension'] == exp['max_pair_overlap'], (
            pos,
            got['max_pair_overlap'],
        )
        assert got['best_sampled_balanced_cut'] == exp['balanced'], (
            pos,
            got['best_sampled_balanced_cut'],
        )
        path_max = {
            name: profile['max_lambda']
            for name, profile in got['order_profiles'].items()
        }
        assert path_max == exp['path_max'], (pos, path_max)

    print('PASS V26_Q138_BC_E0_LOCAL_GROUP_SEPARATOR_RESULT')
    print('B_linear_path_width<=85 B_balanced_lambda=61')
    print('C_linear_path_width<=89 C_balanced_lambda=57')
    print('scope=frozen exact GF2 regression for PR112 local linear separator measurements')
    print('not_included=optimal branchwidth, quadratic scalar phase, grouped-e0 carry, complete B2/C2, W_repr, alpha, arithmetic-work, ranking/search, full-round')


if __name__ == '__main__':
    main()
