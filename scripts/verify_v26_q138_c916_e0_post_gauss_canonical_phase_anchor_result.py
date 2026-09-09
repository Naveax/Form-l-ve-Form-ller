#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_post_gauss_canonical_phase_anchor as P


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['synthetic_pullback_regression_cases'] == 576
    assert out['frozen_pair_physical_pullback_regression_cases'] == 237
    assert out['frozen_pair_support_relation_histogram_reproduced'] == {
        'disjoint': 28,
        'equal': 6,
        'left_subset_right': 4,
        'overlap_incomparable': 112,
        'right_subset_left': 87,
    }
    assert out['frozen_pair_overlap_sign_difference_polar_rank_histogram_reproduced'] == {
        0: 203, 2: 6,
    }

    assert out['sector_transforms'] == 577
    assert out['first_dyadic_term_anchors'] == 340
    assert out['first_dyadic_pair_mates'] == 237
    assert out['canonical_root'] == {
        'group_id': 1,
        'sector_index': 0,
        'multiplicity': 1,
        'role': 'singleton_anchor',
        'physical_support_dimension': 140,
        'physical_support_codimension': 9,
        'normalized_sign_polar_rank': 132,
        'log2_abs_nonzero_gauss': 5,
    }

    assert out['root_comparisons'] == 576
    assert out['root_support_relation_histogram'] == {
        'disjoint': 222,
        'left_subset_right': 21,
        'overlap_incomparable': 333,
    }
    assert out['root_intersection_dimension_histogram'] == {
        136: 62, 137: 102, 138: 147, 139: 22, 140: 21,
    }
    assert out['root_intersection_codimension_histogram'] == {
        9: 21, 10: 22, 11: 147, 12: 102, 13: 62,
    }
    assert out['root_overlap_sign_difference_type_histogram'] == {
        'affine_nonconstant': 219,
        'quadratic_nonconstant': 135,
    }
    assert out['root_overlap_sign_difference_polar_rank_histogram'] == {
        0: 219, 2: 120, 4: 15,
    }
    assert out['root_overlap_constant_difference_bit_histogram'] == {}

    assert out['first_dyadic_term_anchor_support_relation_histogram'] == {
        'disjoint': 139,
        'left_subset_right': 18,
        'overlap_incomparable': 182,
    }
    assert out['first_dyadic_term_anchor_overlap_sign_difference_polar_rank_histogram'] == {
        0: 149, 2: 45, 4: 6,
    }
    assert out['first_dyadic_term_anchor_disjoint_from_root'] == 139
    assert out['first_dyadic_term_anchor_max_overlap_sign_difference_polar_rank'] == 4

    assert out['pair_mate_support_relation_histogram'] == {
        'disjoint': 83,
        'left_subset_right': 3,
        'overlap_incomparable': 151,
    }
    assert out['pair_mate_overlap_sign_difference_polar_rank_histogram'] == {
        0: 70, 2: 75, 4: 9,
    }
    assert out['pair_mate_disjoint_from_root'] == 83
    assert out['pair_mate_max_overlap_sign_difference_polar_rank'] == 4

    assert out['all_sector_disjoint_from_root'] == 222
    assert out['all_sector_max_overlap_sign_difference_polar_rank'] == 4
    assert out['decision'] == 'CANONICAL_SINGLETON_PHASE_ANCHOR_REQUIRES_REFINEMENT'

    print('PASS V26_Q138_C916_E0_POST_GAUSS_CANONICAL_PHASE_ANCHOR_RESULT')
    print('sector_transforms=577')
    print('first_dyadic_term_anchors=340')
    print('pair_mates=237')
    print('root_disjoint_all=222')
    print('root_overlap_rank_histogram={0:219,2:120,4:15}')
    print('term_anchor_disjoint_from_root=139')
    print('term_anchor_overlap_rank_histogram={0:149,2:45,4:6}')
    print('decision=CANONICAL_SINGLETON_PHASE_ANCHOR_REQUIRES_REFINEMENT')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
