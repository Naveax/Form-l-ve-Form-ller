#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_selected_template_common_phase_overlap as P

EXPECTED = {
    2: {
        'selected_templates': 39,
        'support_relation_histogram': {'disjoint': 284, 'equal': 123, 'overlap_incomparable': 334},
        'physical_overlap_edges': 457,
        'physical_overlap_component_sizes': [35, 1, 1, 1, 1],
        'rank_hist': {0: 34, 2: 139, 4: 111, 6: 136, 8: 37},
        'type_hist': {'affine_nonconstant': 34, 'quadratic_nonconstant': 423},
        'same_class': {2: 1, 4: 29, 6: 56, 8: 37},
        'cross_class': {0: 34, 2: 138, 4: 82, 6: 80},
    },
    4: {
        'selected_templates': 22,
        'support_relation_histogram': {'disjoint': 95, 'equal': 6, 'overlap_incomparable': 130},
        'physical_overlap_edges': 136,
        'physical_overlap_component_sizes': [18, 1, 1, 1, 1],
        'rank_hist': {0: 18, 2: 66, 4: 23, 6: 29},
        'type_hist': {'affine_nonconstant': 18, 'quadratic_nonconstant': 118},
        'same_class': {4: 1, 6: 5},
        'cross_class': {0: 18, 2: 66, 4: 22, 6: 24},
    },
    6: {
        'selected_templates': 18,
        'support_relation_histogram': {'disjoint': 71, 'overlap_incomparable': 82},
        'physical_overlap_edges': 82,
        'physical_overlap_component_sizes': [14, 1, 1, 1, 1],
        'rank_hist': {0: 14, 2: 56, 4: 12},
        'type_hist': {'affine_nonconstant': 14, 'quadratic_nonconstant': 68},
        'same_class': {},
        'cross_class': {0: 14, 2: 56, 4: 12},
    },
    8: {
        'selected_templates': 18,
        'support_relation_histogram': {'disjoint': 71, 'overlap_incomparable': 82},
        'physical_overlap_edges': 82,
        'physical_overlap_component_sizes': [14, 1, 1, 1, 1],
        'rank_hist': {0: 16, 2: 46, 4: 12, 6: 8},
        'type_hist': {'affine_nonconstant': 16, 'quadratic_nonconstant': 66},
        'same_class': {},
        'cross_class': {0: 16, 2: 46, 4: 12, 6: 8},
    },
}


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['thresholds'] == [2, 4, 6, 8]
    assert out['compatible_thresholds'] == []
    assert out['decision'] == 'SELECTED_TEMPLATE_COMMON_PHASE_ON_UNION_REFUTED_FOR_R2_R4_R6_R8'

    for threshold, exp in EXPECTED.items():
        rec = out['results'][threshold]
        assert rec['threshold'] == threshold
        assert rec['selected_templates'] == exp['selected_templates']
        assert rec['template_pair_count'] == exp['selected_templates'] * (exp['selected_templates'] - 1) // 2
        assert rec['support_relation_histogram'] == exp['support_relation_histogram']
        assert rec['physical_overlap_edges'] == exp['physical_overlap_edges']
        assert rec['physical_overlap_component_sizes'] == exp['physical_overlap_component_sizes']
        assert rec['overlap_sign_difference_polar_rank_histogram'] == exp['rank_hist']
        assert rec['overlap_sign_difference_type_histogram'] == exp['type_hist']
        assert rec['same_support_class_overlap_rank_histogram'] == exp['same_class']
        assert rec['cross_support_class_overlap_rank_histogram'] == exp['cross_class']
        assert rec['constant_overlap_edges'] == 0
        assert rec['constant_overlap_component_sizes'] == [1] * exp['selected_templates']
        assert rec['nonconstant_overlap_edges'] == exp['physical_overlap_edges']
        assert rec['common_phase_on_union_mod_template_constants_exists'] is False
        assert rec['ambient_quadratic_extension_not_tested'] is True
        cocycle = rec['constant_difference_cocycle']
        assert cocycle['consistent'] is True
        assert cocycle['component_sizes'] == [1] * exp['selected_templates']
        assert cocycle['offset_histogram'] == {0: exp['selected_templates']}
        assert cocycle['first_contradictions'] == []
        assert rec['first_nonconstant_overlap_examples']

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SELECTED_TEMPLATE_COMMON_PHASE_OVERLAP_RESULT')
    print('decision=SELECTED_TEMPLATE_COMMON_PHASE_ON_UNION_REFUTED_FOR_R2_R4_R6_R8')
    print('certificate=every physical selected-template overlap is nonconstant at all four frozen Pareto thresholds; constant overlap edge count is zero')
    print('important=ambient quadratic extension is unnecessary because union gluing is already refuted on overlaps')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
