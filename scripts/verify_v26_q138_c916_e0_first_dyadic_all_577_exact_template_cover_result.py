#!/usr/bin/env python3
import io
from contextlib import redirect_stdout

import probe_v26_q138_c916_e0_first_dyadic_all_577_exact_template_cover as P

EXPECTED_R2 = [
    (2, 0), (13, 0), (15, 1), (16, 0), (17, 0), (18, 0), (19, 0),
    (20, 0), (21, 1), (23, 0), (25, 0), (27, 0), (46, 1), (59, 0),
    (61, 0), (61, 1), (61, 3), (69, 0), (71, 1), (80, 0), (83, 0),
    (90, 0), (107, 0), (110, 0), (117, 0), (124, 0), (132, 0),
    (133, 0), (139, 0), (140, 0), (158, 0), (170, 0), (180, 0),
    (226, 0), (227, 0), (227, 1), (232, 0), (236, 0), (238, 0),
]
EXPECTED_R4 = [
    (2, 0), (13, 0), (16, 0), (18, 0), (19, 0), (23, 0), (27, 0),
    (61, 0), (61, 1), (61, 3), (69, 0), (117, 0), (132, 0),
    (133, 0), (158, 0), (180, 0), (197, 0), (227, 0), (227, 1),
    (232, 0), (236, 0), (238, 0),
]


def main():
    buf = io.StringIO()
    with redirect_stdout(buf):
        out = P.analyze()

    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['synthetic_solver_regression_cases'] == 4
    assert out['all_transforms'] == 577
    assert out['support_maximal_templates'] == 62
    assert out['support_maximal_equal_classes'] == 18
    assert out['support_maximal_equal_class_size_histogram'] == {1: 16, 21: 1, 25: 1}
    assert out['owner_class_count_histogram'] == {1: 577}
    assert out['minimum_direct_residual_rank_histogram'] == {0: 413, 2: 164}
    assert out['minimum_direct_residual_rank_by_role'] == {
        'pair_anchor': {0: 147, 2: 90},
        'pair_mate': {0: 188, 2: 49},
        'singleton_anchor': {0: 78, 2: 25},
    }

    r0 = out['threshold_results'][0]
    assert r0['feasible'] is False
    assert r0['covered_by_all_candidates'] == 413
    assert r0['uncovered_by_all_candidates'] == 164
    assert r0['minimum_templates'] is None

    r2 = out['threshold_results'][2]
    assert r2['feasible'] is True
    assert r2['minimum_templates'] == 39
    assert [tuple(x) for x in r2['chosen_template_ids']] == EXPECTED_R2
    assert r2['chosen_template_role_histogram'] == {
        'pair_anchor': 20, 'pair_mate': 7, 'singleton_anchor': 12,
    }
    assert r2['class_minimum_template_histogram'] == {1: 16, 10: 1, 13: 1}
    assert r2['assignment_residual_rank_histogram'] == {0: 361, 2: 216}
    assert r2['assignment_residual_rank_by_role'] == {
        'pair_anchor': {0: 135, 2: 102},
        'pair_mate': {0: 181, 2: 56},
        'singleton_anchor': {0: 45, 2: 58},
    }
    assert r2['solver_stats_total'] == {
        'branches_examined': 717,
        'max_depth': 27,
        'memo_hits': 370,
        'states_solved': 272,
    }
    assert r2['classes'][0]['minimum_templates'] == 10
    assert r2['classes'][1]['minimum_templates'] == 13

    r4 = out['threshold_results'][4]
    assert r4['feasible'] is True
    assert r4['minimum_templates'] == 22
    assert [tuple(x) for x in r4['chosen_template_ids']] == EXPECTED_R4
    assert r4['chosen_template_role_histogram'] == {
        'pair_anchor': 13, 'pair_mate': 3, 'singleton_anchor': 6,
    }
    assert r4['class_minimum_template_histogram'] == {1: 16, 3: 2}
    assert r4['assignment_residual_rank_histogram'] == {0: 259, 2: 267, 4: 51}
    assert r4['assignment_residual_rank_by_role'] == {
        'pair_anchor': {0: 118, 2: 103, 4: 16},
        'pair_mate': {0: 106, 2: 112, 4: 19},
        'singleton_anchor': {0: 35, 2: 52, 4: 16},
    }
    assert r4['solver_stats_total'] == {
        'branches_examined': 947,
        'max_depth': 11,
        'memo_hits': 437,
        'states_solved': 161,
    }
    assert r4['classes'][0]['minimum_templates'] == 3
    assert r4['classes'][1]['minimum_templates'] == 3

    assert out['decision'] == 'ALL_577_EXACT_MAXIMAL_TEMPLATE_COVER_R0_INFEASIBLE_R2_39_R4_22'

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_577_EXACT_TEMPLATE_COVER_RESULT')
    print('R0=infeasible_413_of_577')
    print('R2_minimum_templates=39')
    print('R2_assignment_residual_rank_histogram={0:361,2:216}')
    print('R4_minimum_templates=22')
    print('R4_assignment_residual_rank_histogram={0:259,2:267,4:51}')
    print('decision=ALL_577_EXACT_MAXIMAL_TEMPLATE_COVER_R0_INFEASIBLE_R2_39_R4_22')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
