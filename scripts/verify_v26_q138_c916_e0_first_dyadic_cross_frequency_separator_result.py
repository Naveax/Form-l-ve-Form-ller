#!/usr/bin/env python3
import probe_v26_q138_c916_e0_first_dyadic_cross_frequency_separator as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['support_groups'] == 250
    assert out['global_refined_rank'] == 149
    assert out['base_rank_histogram'] == {11: 24, 12: 107, 13: 15, 14: 1, 19: 4, 20: 14, 21: 85}
    assert out['anchor_cross_rank_histogram'] == {10: 8, 11: 152, 13: 1, 14: 73, 15: 14, 16: 2}
    assert out['difference_cross_rank_histogram'] == {0: 103, 1: 6, 2: 11, 3: 57, 4: 26, 5: 40, 6: 3, 7: 4}
    assert out['combined_cross_rank_histogram'] == {10: 7, 11: 96, 12: 6, 13: 12, 14: 25, 15: 11, 16: 36, 17: 19, 18: 31, 19: 3, 20: 1, 21: 3}
    assert out['refined_rank_histogram'] == {19: 4, 20: 14, 21: 87, 22: 16, 23: 36, 24: 10, 25: 71, 26: 11, 27: 1}
    assert out['extra_rank_histogram'] == {0: 103, 10: 9, 11: 48, 12: 2, 13: 81, 14: 7}
    assert out['groups_with_no_extra_rank'] == 103
    assert out['max_extra_rank'] == 14
    assert out['recursive_widths'] == {
        'base_multiplicity_then_rank': 85,
        'multiplicity_then_refined': 83,
        'refined_rank_ascending': 83,
        'refined_rank_descending': 80,
    }
    assert out['best_recursive_order'] == 'refined_rank_descending'
    assert out['best_recursive_width'] == 80
    assert out['best_recursive_depth'] == 11
    assert out['best_balanced_cut'] == {
        'name': 'multiplicity_then_refined_half',
        'left_groups': 125,
        'right_groups': 125,
        'left_rank': 57,
        'right_rank': 149,
        'lambda': 57,
    }
    assert out['best_recursive_root_children'] == [
        {'size': 83, 'rank': 127, 'complement_rank': 70, 'lambda': 48},
        {'size': 167, 'rank': 70, 'complement_rank': 127, 'lambda': 48},
    ]
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_CROSS_FREQUENCY_SEPARATOR_RESULT')
    print('decision=CROSS_FREQUENCY_LINEAR_SKELETON_WIDTH_80')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
