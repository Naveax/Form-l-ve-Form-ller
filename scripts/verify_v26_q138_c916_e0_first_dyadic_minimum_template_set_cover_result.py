#!/usr/bin/env python3
import io
from contextlib import redirect_stdout

import probe_v26_q138_c916_e0_first_dyadic_minimum_template_set_cover as P

EXPECTED_R2 = [
    [2, 0], [13, 0], [16, 0], [17, 0], [18, 0], [19, 0], [20, 0],
    [23, 0], [26, 0], [27, 0], [28, 0], [59, 0], [61, 0], [69, 0],
    [71, 0], [80, 0], [83, 0], [107, 0], [110, 0], [121, 0], [124, 0],
    [132, 0], [133, 0], [139, 0], [140, 0], [158, 0], [180, 0], [196, 0],
    [226, 0], [227, 0], [232, 0], [236, 0], [238, 0],
]
EXPECTED_R4 = [
    [2, 0], [13, 0], [16, 0], [18, 0], [19, 0], [23, 0], [27, 0],
    [61, 0], [69, 0], [117, 0], [132, 0], [133, 0], [158, 0], [180, 0],
    [197, 0], [227, 0], [232, 0], [236, 0], [238, 0],
]


def main():
    with redirect_stdout(io.StringIO()):
        out = P.analyze()

    assert out['first_dyadic_term_anchors'] == 340
    assert out['physical_shared_dimension'] == 149
    assert out['maximal_support_anchors'] == 52
    assert out['maximal_support_equal_classes'] == 15
    assert out['maximal_support_equal_class_size_histogram'] == {1: 13, 18: 1, 21: 1}
    assert out['containing_maximal_candidate_count_histogram'] == {1: 24, 18: 201, 21: 115}
    assert out['direct_containing_template_residual_rank_histogram'] == {
        0: 459, 2: 2027, 4: 2027, 6: 1354, 8: 190,
    }
    assert out['minimum_direct_residual_polar_rank_histogram'] == {0: 222, 2: 118}

    r0 = out['threshold_results'][0]
    assert not r0['feasible']
    assert r0['covered_by_all_candidates'] == 222
    assert r0['uncovered_anchors'] == 118

    r2 = out['threshold_results'][2]
    assert r2['feasible']
    assert r2['minimum_templates'] == 33
    assert r2['chosen_template_anchor_ids'] == EXPECTED_R2
    assert r2['class_minimum_template_histogram'] == {1: 13, 9: 1, 11: 1}
    assert r2['exhausted_subsets_below_optimum'] == 601068
    assert r2['covered_by_all_candidates'] == 340

    r4 = out['threshold_results'][4]
    assert r4['feasible']
    assert r4['minimum_templates'] == 19
    assert r4['chosen_template_anchor_ids'] == EXPECTED_R4
    assert r4['class_minimum_template_histogram'] == {1: 13, 3: 2}
    assert r4['exhausted_subsets_below_optimum'] == 402
    assert r4['covered_by_all_candidates'] == 340

    assert out['minimum_templates_r2'] == 33
    assert out['minimum_templates_r4'] == 19
    assert out['decision'] == 'MINIMUM_MAXIMAL_SUPPORT_TEMPLATE_COVER_R2_33_R4_19_R0_INFEASIBLE'

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_MINIMUM_TEMPLATE_SET_COVER_RESULT')
    print('anchors=340')
    print('r0_feasible=0 r0_covered=222 r0_uncovered=118')
    print('r2_minimum_templates=33 r2_exhausted_below_optimum=601068')
    print('r4_minimum_templates=19 r4_exhausted_below_optimum=402')
    print('decision=MINIMUM_MAXIMAL_SUPPORT_TEMPLATE_COVER_R2_33_R4_19_R0_INFEASIBLE')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
