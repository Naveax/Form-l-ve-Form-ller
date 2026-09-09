#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_template_residual_pareto as P

EXPECTED_R6_TEMPLATES = [
    [2, 0], [18, 0], [19, 0], [23, 0], [61, 0], [61, 1], [61, 3],
    [69, 0], [132, 0], [133, 0], [158, 0], [180, 0], [197, 0],
    [227, 0], [227, 1], [232, 0], [236, 0], [238, 0],
]
EXPECTED_R8_TEMPLATES = [
    [2, 0], [13, 0], [18, 0], [19, 0], [23, 0], [61, 0], [61, 1],
    [61, 3], [69, 0], [132, 0], [133, 0], [158, 0], [180, 0],
    [227, 0], [227, 1], [232, 0], [236, 0], [238, 0],
]


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['baseline_width'] == 61
    assert out['decision'] == 'ALL_577_TEMPLATE_RESIDUAL_PARETO_R6_T18_W104_R8_T18_W100'

    r6 = out['results'][6]
    assert r6['minimum_templates'] == 18
    assert r6['chosen_template_ids'] == EXPECTED_R6_TEMPLATES
    assert r6['class_minimum_template_histogram'] == {1: 18}
    assert r6['solver_stats_total'] == {
        'branches_examined': 638,
        'max_depth': 4,
        'memo_hits': 39,
        'states_solved': 54,
    }
    assert r6['assignment_residual_polar_rank_histogram'] == {0: 168, 2: 295, 4: 100, 6: 14}
    assert r6['minimal_signature_rank_histogram'] == {0: 18, 1: 150, 3: 295, 5: 100, 7: 14}
    assert r6['minimal_signature_rank_by_polar_rank'] == {
        0: {0: 18, 1: 150},
        2: {3: 295},
        4: {5: 100},
        6: {7: 14},
    }
    assert r6['scalar_cut_histogram'] == {0: 18, 1: 559}
    assert r6['total_signature_rows_before_group_union'] == 1633
    assert r6['gauge_failure_count'] == 0
    assert r6['all_lift_gauges_contained'] is True
    assert r6['first_gauge_failures'] == []
    assert r6['residual_signature_union_rank_histogram'] == {
        0: 3, 1: 20, 2: 3, 3: 40, 4: 18, 5: 48, 6: 15, 7: 28, 8: 69, 9: 1, 10: 5,
    }
    assert r6['extra_rank_histogram'] == {0: 3, 1: 20, 2: 17, 3: 54, 4: 75, 5: 54, 6: 19, 7: 7, 8: 1}
    assert r6['groups_with_zero_extra_rank'] == 3
    assert r6['max_extra_rank'] == 8
    assert r6['global_augmented_linear_rank'] == 149
    assert r6['recursive_widths'] == {
        'augmented_rank_ascending': 129,
        'augmented_rank_descending': 133,
        'extra_then_augmented': 104,
        'multiplicity_then_augmented': 104,
    }
    assert r6['best_recursive_order'] == 'multiplicity_then_augmented'
    assert r6['best_recursive_width'] == 104
    assert r6['best_recursive_depth'] == 9
    assert r6['best_recursive_root_children'] == [
        {'complement_rank': 149, 'lambda': 69, 'rank': 69, 'size': 100},
        {'complement_rank': 69, 'lambda': 69, 'rank': 149, 'size': 150},
    ]

    r8 = out['results'][8]
    assert r8['minimum_templates'] == 18
    assert r8['chosen_template_ids'] == EXPECTED_R8_TEMPLATES
    assert r8['class_minimum_template_histogram'] == {1: 18}
    assert r8['solver_stats_total'] == {
        'branches_examined': 62,
        'max_depth': 0,
        'memo_hits': 0,
        'states_solved': 18,
    }
    assert r8['assignment_residual_polar_rank_histogram'] == {0: 163, 2: 221, 4: 99, 6: 87, 8: 7}
    assert r8['minimal_signature_rank_histogram'] == {0: 18, 1: 145, 3: 221, 5: 99, 7: 87, 9: 7}
    assert r8['minimal_signature_rank_by_polar_rank'] == {
        0: {0: 18, 1: 145},
        2: {3: 221},
        4: {5: 99},
        6: {7: 87},
        8: {9: 7},
    }
    assert r8['scalar_cut_histogram'] == {0: 18, 1: 559}
    assert r8['total_signature_rows_before_group_union'] == 1975
    assert r8['gauge_failure_count'] == 0
    assert r8['all_lift_gauges_contained'] is True
    assert r8['first_gauge_failures'] == []
    assert r8['residual_signature_union_rank_histogram'] == {
        0: 3, 1: 13, 2: 3, 3: 33, 4: 19, 5: 49, 6: 18, 7: 33, 8: 7, 9: 66, 10: 1, 11: 5,
    }
    assert r8['extra_rank_histogram'] == {0: 3, 1: 13, 2: 17, 3: 48, 4: 10, 5: 119, 6: 12, 7: 25, 8: 2, 9: 1}
    assert r8['groups_with_zero_extra_rank'] == 3
    assert r8['max_extra_rank'] == 9
    assert r8['global_augmented_linear_rank'] == 149
    assert r8['recursive_widths'] == {
        'augmented_rank_ascending': 116,
        'augmented_rank_descending': 131,
        'extra_then_augmented': 124,
        'multiplicity_then_augmented': 100,
    }
    assert r8['best_recursive_order'] == 'multiplicity_then_augmented'
    assert r8['best_recursive_width'] == 100
    assert r8['best_recursive_depth'] == 10
    assert r8['best_recursive_root_children'] == [
        {'complement_rank': 149, 'lambda': 69, 'rank': 69, 'size': 100},
        {'complement_rank': 69, 'lambda': 69, 'rank': 149, 'size': 150},
    ]

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_TEMPLATE_RESIDUAL_PARETO_RESULT')
    print('decision=ALL_577_TEMPLATE_RESIDUAL_PARETO_R6_T18_W104_R8_T18_W100')
    print('important=both R6 and R8 reach one template per maximal support class, but individually determined residual-signature widths remain far above baseline 61')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
