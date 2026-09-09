#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_all_overlap_phase_census as P


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['synthetic_component_regression_cases'] == 5
    assert out['first_dyadic_term_anchors'] == 340
    assert out['all_unordered_anchor_pairs'] == 57630
    assert out['physical_overlap_pairs'] == 29996
    assert out['physical_disjoint_pairs'] == 27634

    assert out['support_relation_histogram'] == {
        'disjoint': 27634,
        'equal': 378,
        'left_subset_right': 2269,
        'overlap_incomparable': 24026,
        'right_subset_left': 3323,
    }
    assert out['all_overlap_sign_difference_polar_rank_histogram'] == {
        0: 13812, 2: 9821, 4: 4972, 6: 1296, 8: 95,
    }
    assert out['all_overlap_sign_difference_type_histogram'] == {
        'affine_nonconstant': 13808,
        'constant': 4,
        'quadratic_nonconstant': 16184,
    }
    assert out['all_overlap_intersection_codimension_histogram'] == {
        7: 363, 8: 376, 9: 3826, 10: 2624, 11: 11250,
        12: 3096, 13: 8131, 14: 120, 15: 210,
    }

    c = out['component_summary_by_polar_rank_threshold']
    assert c[0]['component_count'] == 9
    assert c[0]['component_sizes_descending'] == [325, 2, 2, 2, 2, 2, 2, 2, 1]
    for t in (2, 4, 6, 8):
        assert c[t]['component_count'] == 5
        assert c[t]['component_sizes_descending'] == [332, 2, 2, 2, 2]
        assert c[t]['component_roots'] == [
            [0, 0], [158, 0], [180, 0], [236, 0], [238, 0],
        ]

    support = out['physical_support_overlap_graph']
    assert support['component_count'] == 5
    assert support['component_sizes_descending'] == [332, 2, 2, 2, 2]
    assert support['component_roots'] == [
        [0, 0], [158, 0], [180, 0], [236, 0], [238, 0],
    ]

    assert out['rank_le_4_cross_component_overlap_pairs'] == 0
    assert out['rank_le_4_cross_component_polar_rank_histogram'] == {}
    assert out['rank_le_4_cross_component_pair_rank_histogram'] == {}
    assert out['rank_le_4_internal_polar_rank_histogram_by_component'] == {
        0: {0: 13808, 2: 9821, 4: 4972, 6: 1296, 8: 95},
        1: {0: 1}, 2: {0: 1}, 3: {0: 1}, 4: {0: 1},
    }
    assert out['minimal_polar_rank_threshold_reaching_support_connectivity'] == 2
    assert out['decision'] == 'FIRST_DYADIC_ALL_OVERLAP_SUPPORT_GRAPH_MULTIPLE_COMPONENTS'

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_OVERLAP_PHASE_CENSUS_RESULT')
    print('anchors=340')
    print('all_pairs=57630')
    print('physical_overlap_pairs=29996')
    print('physical_disjoint_pairs=27634')
    print('support_components=5')
    print('support_component_sizes=[332,2,2,2,2]')
    print('overlap_polar_rank_histogram={0:13812,2:9821,4:4972,6:1296,8:95}')
    print('cross_component_overlap_pairs=0')
    print('decision=FIRST_DYADIC_ALL_OVERLAP_SUPPORT_GRAPH_MULTIPLE_COMPONENTS')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
