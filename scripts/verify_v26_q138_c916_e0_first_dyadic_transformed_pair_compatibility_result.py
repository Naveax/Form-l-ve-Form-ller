#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_transformed_pair_compatibility as P


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['synthetic_pair_regression_cases'] == 2304
    assert out['raw_e0_sectors'] == 577
    assert out['support_groups'] == 250
    assert out['even_multiplicity_support_groups'] == 147
    assert out['transformed_first_dyadic_pairs'] == 237

    assert out['support_relation_histogram'] == {
        'disjoint': 28,
        'equal': 6,
        'left_subset_right': 4,
        'overlap_incomparable': 112,
        'right_subset_left': 87,
    }
    assert out['amplitude_delta_histogram'] == {0: 132, 1: 105}
    assert out['intersection_constraint_rank_histogram'] == {
        1: 4, 2: 5, 3: 89, 4: 82, 5: 29,
    }
    assert out['sign_difference_type_histogram'] == {
        'affine_nonconstant': 201,
        'constant': 2,
        'quadratic_nonconstant': 6,
    }
    assert out['sign_difference_polar_rank_histogram'] == {0: 203, 2: 6}
    assert out['overlap_arithmetic_histogram'] == {
        'equal_amplitude_affine_switch': 111,
        'equal_amplitude_quadratic_switch': 6,
        'equal_amplitude_same_sign': 1,
        'no_overlap': 28,
        'unequal_amplitude_no_cancellation': 91,
    }
    assert out['global_pair_class_histogram'] == {
        'disjoint_support_residual': 28,
        'genuine_residual': 209,
    }
    assert out['global_pair_class_histogram'].get('exact_equal_transform', 0) == 0
    assert out['global_pair_class_histogram'].get('exact_zero_transform', 0) == 0
    assert out['first_dyadic_min_nonzero_valuation_histogram'] == {
        3: 21, 4: 139, 5: 77,
    }
    assert out['valuation_gain_over_naive_histogram'] == {0: 231, 1: 6}

    assert out['support_relation_by_multiplicity'] == {
        2: {
            'disjoint': 4,
            'equal': 4,
            'left_subset_right': 4,
            'overlap_incomparable': 35,
            'right_subset_left': 10,
        },
        4: {
            'disjoint': 24,
            'equal': 2,
            'overlap_incomparable': 77,
            'right_subset_left': 77,
        },
    }
    assert out['global_pair_class_by_multiplicity'] == {
        2: {'disjoint_support_residual': 4, 'genuine_residual': 53},
        4: {'disjoint_support_residual': 24, 'genuine_residual': 156},
    }
    assert out['sign_difference_polar_rank_by_multiplicity'] == {
        2: {0: 49, 2: 4},
        4: {0: 154, 2: 2},
    }
    assert out['amplitude_delta_by_multiplicity'] == {
        2: {0: 41, 1: 16},
        4: {0: 91, 1: 89},
    }

    assert len(out['groups']) == 147
    assert sum(len(g['pairs']) for g in out['groups']) == 237
    assert all(
        rec['global_pair_class'] in {'disjoint_support_residual', 'genuine_residual'}
        for group in out['groups']
        for rec in group['pairs']
    )
    assert sum(
        rec['sign_difference_polar_rank'] == 2
        for group in out['groups']
        for rec in group['pairs']
        if rec['sign_difference_polar_rank'] is not None
    ) == 6

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_TRANSFORMED_PAIR_COMPATIBILITY_RESULT')
    print('pairs=237')
    print('overlapping_pairs=209')
    print('disjoint_pairs=28')
    print('sign_difference_polar_rank_histogram={0:203,2:6}')
    print('exact_zero_pairs=0')
    print('exact_equal_pairs=0')
    print('valuation_gain_one_pairs=6')
    print('decision=TRANSFORMED_PAIR_SIGN_DIFFERENCE_POLAR_RANK0_2')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
