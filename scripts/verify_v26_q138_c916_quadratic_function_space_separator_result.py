#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_quadratic_function_space_separator as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['raw_e0_sectors'] == 577
    assert out['support_groups'] == 250
    assert out['degree2_ambient_coordinates'] == 11176
    assert out['linear_global_rank'] == 149
    assert out['scalar_polynomial_global_rank'] == 199
    assert out['polar_global_rank'] == 171
    assert out['combined_function_global_rank'] == 321

    assert out['linear_tree']['best_width'] == 58
    assert out['linear_tree']['best_order'] == 'multiplicity_then_function'
    assert out['scalar_tree']['best_width'] == 6
    assert out['scalar_tree']['best_order'] == 'multiplicity_then_function'
    assert out['polar_tree']['best_width'] == 12
    assert out['polar_tree']['best_order'] == 'function_rank_ascending'
    assert out['combined_function_tree']['best_width'] == 70
    assert out['combined_function_tree']['best_depth'] == 10
    assert out['combined_function_tree']['best_order'] == 'multiplicity_then_function'
    assert out['combined_function_tree']['candidate_widths'] == {
        'function_rank_ascending': 79,
        'function_rank_descending': 90,
        'multiplicity_then_function': 70,
        'multiplicity_then_linear': 70,
    }
    assert out['combined_function_tree']['best_root_children'] == [
        {'size': 166, 'rank': 206, 'complement_rank': 159, 'lambda': 44},
        {'size': 84, 'rank': 159, 'complement_rank': 206, 'lambda': 44},
    ]
    assert out['combined_function_best_balanced_cut'] == {
        'left_groups': 125,
        'right_groups': 125,
        'left_rank': 169,
        'right_rank': 224,
        'lambda': 72,
    }
    assert out['scalar_best_balanced_cut_under_function_order'] == {
        'left_groups': 125,
        'right_groups': 125,
        'left_rank': 122,
        'right_rank': 83,
        'lambda': 6,
    }
    assert out['linear_best_balanced_cut_under_function_order'] == {
        'left_groups': 125,
        'right_groups': 125,
        'left_rank': 56,
        'right_rank': 148,
        'lambda': 55,
    }

    print('PASS V26_Q138_C916_QUADRATIC_FUNCTION_SPACE_SEPARATOR_RESULT')
    print('linear_width=58')
    print('scalar_polynomial_width=6')
    print('polar_width=12')
    print('combined_function_width=70')
    print('all_linear_scalar_refinement_width=147')
    print('hybrid_linear_width=83')
    print('verdict=QUADRATIC_FUNCTION_SPACE_PRESERVES_SMALL_SEPARATOR_OVERHEAD')
    print('important=function-space lambda is exact, but not by itself an exact nonlinear message-count theorem')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
