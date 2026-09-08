#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_aggregate_e0_scalar_separator as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['raw_e0_sectors'] == 577
    assert out['support_groups'] == 250
    assert out['global_refined_rank'] == 149
    assert out['aggregate_scalar_polar_rank_histogram'] == {
        2: 8, 4: 53, 6: 71, 8: 11, 10: 3, 12: 1,
        136: 6, 138: 50, 140: 41, 142: 6,
    }
    assert out['refined_rank_histogram'] == {
        13: 18, 14: 74, 15: 46, 16: 5, 17: 4, 145: 36, 146: 67,
    }
    assert out['extra_rank_histogram'] == {
        1: 11, 2: 79, 3: 47, 4: 9, 5: 1,
        124: 30, 125: 59, 126: 12, 127: 2,
    }
    assert out['scalar_linear_cut_histogram'] == {0: 30, 1: 220}
    assert out['groups_with_no_extra_rank'] == 0
    assert out['groups_reaching_full_rank'] == 0
    assert out['min_refined_rank'] == 13
    assert out['max_refined_rank'] == 146
    assert out['max_extra_rank'] == 127
    assert out['best_balanced_cut'] == {
        'name': 'multiplicity_then_refined_half',
        'left_groups': 125,
        'right_groups': 125,
        'left_rank': 147,
        'right_rank': 149,
        'lambda': 147,
    }
    assert out['path_widths'] == {
        'original_rank_ascending': 149,
        'refined_rank_ascending': 149,
        'refined_rank_descending': 147,
        'multiplicity_then_refined': 147,
    }
    assert out['recursive_widths'] == {
        'refined_rank_ascending': 147,
        'refined_rank_descending': 147,
        'multiplicity_then_refined': 147,
    }
    assert out['best_recursive_order'] == 'multiplicity_then_refined'
    assert out['best_recursive_width'] == 147
    assert out['best_recursive_depth'] == 10
    assert out['best_recursive_root_children'] == [
        {'size': 166, 'rank': 148, 'complement_rank': 123, 'lambda': 122},
        {'size': 84, 'rank': 123, 'complement_rank': 148, 'lambda': 122},
    ]

    print('PASS V26_Q138_C916_AGGREGATE_E0_SCALAR_SEPARATOR_RESULT')
    print('C_aggregate_scalar_refined_recursive_width=147')
    print('C_aggregate_scalar_refined_balanced_lambda=147')
    print('verdict=AGGREGATE_SCALAR_LINEAR_REFINEMENT_NEAR_MONOLITHIC')
    print('important=aggregate refinement is less restrictive than sectorwise refinement but still not a useful contraction width')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
