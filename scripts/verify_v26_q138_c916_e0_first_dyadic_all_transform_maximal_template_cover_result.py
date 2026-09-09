#!/usr/bin/env python3
import io
from contextlib import redirect_stdout

import probe_v26_q138_c916_e0_first_dyadic_all_transform_maximal_template_cover as P

EXPECTED_PREVIOUS = {
    '(61, 1)': {'is_support_maximal_all_transform': True, 'owner_class': 6, 'support_dimension': 140},
    '(61, 3)': {'is_support_maximal_all_transform': True, 'owner_class': 7, 'support_dimension': 140},
    '(227, 1)': {'is_support_maximal_all_transform': True, 'owner_class': 14, 'support_dimension': 140},
}


def main():
    buf = io.StringIO()
    with redirect_stdout(buf):
        out = P.analyze()

    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['all_transforms'] == 577
    assert out['role_histogram'] == {
        'pair_anchor': 237,
        'pair_mate': 237,
        'singleton_anchor': 103,
    }
    assert out['support_maximal_all_transform_templates'] == 62
    assert out['support_maximal_role_histogram'] == {
        'pair_anchor': 26,
        'pair_mate': 10,
        'singleton_anchor': 26,
    }
    assert out['support_maximal_dimension_histogram'] == {140: 7, 142: 55}
    assert out['support_maximal_equal_classes'] == 18
    assert out['support_maximal_equal_class_size_histogram'] == {1: 16, 21: 1, 25: 1}
    assert out['max_support_class_candidate_roots'] == 25
    assert out['owner_class_count_histogram'] == {1: 577}
    assert out['multiple_owner_transform_count'] == 0
    assert out['first_multiple_owner_examples'] == []
    assert out['previous_anchor_uncovered_transform_status'] == EXPECTED_PREVIOUS
    assert out['minimum_direct_residual_rank_histogram'] == {0: 413, 2: 164}
    assert out['minimum_direct_residual_rank_by_role'] == {
        'pair_anchor': {0: 147, 2: 90},
        'pair_mate': {0: 188, 2: 49},
        'singleton_anchor': {0: 78, 2: 25},
    }
    assert out['exact_classwise_set_cover_allowed'] is False
    assert out['threshold_results'] == {}
    assert out['decision'] == 'ALL_TRANSFORM_MAXIMAL_CLASS_TOO_LARGE_FOR_ENUMERATION_25'

    profiles = out['support_maximal_class_profiles']
    assert len(profiles) == 18
    assert profiles[0]['candidate_roots'] == 25
    assert profiles[0]['support_dimension'] == 142
    assert profiles[0]['role_histogram'] == {
        'pair_anchor': 5, 'pair_mate': 4, 'singleton_anchor': 16,
    }
    assert profiles[1]['candidate_roots'] == 21
    assert profiles[1]['support_dimension'] == 142
    assert profiles[1]['role_histogram'] == {
        'pair_anchor': 8, 'pair_mate': 3, 'singleton_anchor': 10,
    }
    assert sum(p['candidate_roots'] for p in profiles) == 62

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_TRANSFORM_MAXIMAL_TEMPLATE_COVER_RESULT')
    print('transforms=577')
    print('support_maximal_templates=62')
    print('support_maximal_equal_classes=18')
    print('class_size_histogram={1:16,21:1,25:1}')
    print('owner_class_count_histogram={1:577}')
    print('minimum_direct_residual_polar_rank_histogram={0:413,2:164}')
    print('previous_three_pair_mates_are_support_maximal=true')
    print('decision=ALL_TRANSFORM_MAXIMAL_CLASS_TOO_LARGE_FOR_ENUMERATION_25')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
