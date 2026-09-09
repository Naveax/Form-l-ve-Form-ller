#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_maximal_support_phase_template_cover as P


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['synthetic_cover_regression_cases'] == 4
    assert out['first_dyadic_term_anchors'] == 340
    assert out['physical_support_components'] == 5
    assert out['physical_support_component_sizes_descending'] == [332, 2, 2, 2, 2]
    assert out['support_relation_histogram'] == {
        'disjoint': 27634, 'equal': 378, 'left_subset_right': 2269,
        'overlap_incomparable': 24026, 'right_subset_left': 3323,
    }
    assert out['containment_pair_polar_rank_histogram'] == {
        0: 491, 2: 2234, 4: 1942, 6: 1208, 8: 95,
    }
    assert out['equal_support_pair_polar_rank_histogram'] == {
        2: 32, 4: 105, 6: 146, 8: 95,
    }
    assert out['strict_containment_pair_polar_rank_histogram'] == {
        0: 491, 2: 2202, 4: 1837, 6: 1062,
    }

    assert out['maximal_support_anchors'] == 52
    assert out['maximal_support_dimension_histogram'] == {140: 4, 142: 48}
    assert out['maximal_support_equal_classes'] == 15
    assert out['maximal_support_equal_class_size_histogram'] == {1: 13, 18: 1, 21: 1}
    assert out['maximal_support_anchors_by_component'] == {0: 48, 1: 1, 2: 1, 3: 1, 4: 1}
    assert out['containing_maximal_candidate_count_histogram'] == {1: 24, 18: 201, 21: 115}

    assert out['minimum_direct_residual_polar_rank_histogram'] == {0: 222, 2: 118}
    assert out['minimum_direct_residual_type_histogram'] == {
        'affine_nonconstant': 170, 'constant': 52, 'quadratic_nonconstant': 118,
    }
    assert out['minimum_direct_residual_polar_rank_by_role'] == {
        'pair_anchor': {0: 144, 2: 93},
        'singleton_anchor': {0: 78, 2: 25},
    }
    assert out['max_minimum_direct_residual_polar_rank'] == 2
    assert out['threshold_coverage'][0]['covered_anchors'] == 222
    assert out['threshold_coverage'][0]['uncovered_anchors'] == 118
    assert out['threshold_coverage'][2]['all_covered'] is True
    assert out['threshold_coverage'][2]['covered_anchors'] == 340
    assert out['threshold_coverage'][2]['uncovered_anchors'] == 0

    assert out['deterministically_chosen_template_anchors'] == 52
    assert out['chosen_template_anchors_by_component'] == {0: 48, 1: 1, 2: 1, 3: 1, 4: 1}
    assert out['chosen_template_assignment_size_histogram'] == {
        1: 8, 2: 27, 3: 6, 4: 2, 5: 1, 7: 1, 10: 1,
        11: 1, 12: 1, 14: 1, 58: 1, 67: 1, 68: 1,
    }

    # The probe's generic decision label says <=4; the exact frozen result is
    # strictly stronger because max_minimum_direct_residual_polar_rank == 2.
    assert out['decision'] == 'MAXIMAL_SUPPORT_ANCHOR_TEMPLATE_COVER_RESIDUAL_POLAR_RANK_LE_4'

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_MAXIMAL_SUPPORT_PHASE_TEMPLATE_COVER_RESULT')
    print('anchors=340')
    print('maximal_support_anchors=52')
    print('maximal_support_equal_classes=15')
    print('minimum_direct_residual_polar_rank_histogram={0:222,2:118}')
    print('max_minimum_direct_residual_polar_rank=2')
    print('rank2_covered_anchors=340')
    print('decision=MAXIMAL_SUPPORT_ANCHOR_TEMPLATE_COVER_RESIDUAL_POLAR_RANK2')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
