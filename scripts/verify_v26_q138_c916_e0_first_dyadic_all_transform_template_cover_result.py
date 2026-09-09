#!/usr/bin/env python3
import io
from contextlib import redirect_stdout

import probe_v26_q138_c916_e0_first_dyadic_all_transform_template_cover as P


def main():
    with redirect_stdout(io.StringIO()):
        out = P.analyze()

    assert out['physical_shared_dimension'] == 149
    assert out['all_transforms'] == 577
    assert out['anchor_transforms'] == 340
    assert out['pair_mates'] == 237
    assert out['role_histogram'] == {
        'pair_anchor': 237,
        'pair_mate': 237,
        'singleton_anchor': 103,
    }
    assert out['maximal_anchor_templates'] == 52
    assert out['maximal_anchor_support_classes'] == 15
    assert out['maximal_anchor_support_class_size_histogram'] == {1: 13, 18: 1, 21: 1}
    assert out['owner_class_count_histogram'] == {0: 3, 1: 574}
    assert out['transforms_without_containing_anchor_template_support'] == 3
    assert out['transforms_with_multiple_maximal_support_classes'] == 0
    assert out['first_uncovered_support_ids'] == [[61, 1], [61, 3], [227, 1]]

    r2 = out['selected_anchor_optimum_template_results'][2]
    assert r2['selected_templates'] == 33
    assert r2['full_support_covered'] == 574
    assert r2['no_containing_template'] == 3
    assert r2['no_containing_template_by_role'] == {'pair_mate': 3}
    assert r2['over_nominal_threshold'] == 6
    assert r2['over_nominal_threshold_by_role'] == {'pair_mate': 6}
    assert r2['max_minimum_residual_rank'] == 4
    assert r2['minimum_residual_rank_histogram'] == {0: 355, 2: 213, 4: 6}

    r4 = out['selected_anchor_optimum_template_results'][4]
    assert r4['selected_templates'] == 19
    assert r4['full_support_covered'] == 574
    assert r4['no_containing_template'] == 3
    assert r4['no_containing_template_by_role'] == {'pair_mate': 3}
    assert r4['over_nominal_threshold'] == 0
    assert r4['max_minimum_residual_rank'] == 4
    assert r4['minimum_residual_rank_histogram'] == {0: 256, 2: 267, 4: 51}

    assert out['optimized_all_transform_template_cover'] == {}
    assert out['decision'] == 'ANCHOR_MAXIMAL_TEMPLATE_SUPPORT_DOES_NOT_COVER_ALL_577_TRANSFORMS'

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_TRANSFORM_TEMPLATE_COVER_RESULT')
    print('all_transforms=577 anchors=340 pair_mates=237')
    print('anchor_template_support_covered=574 uncovered=3')
    print('uncovered_ids=[(61,1),(61,3),(227,1)]')
    print('r2_selected=33 r2_support_covered=574 r2_rank4_exceptions=6')
    print('r4_selected=19 r4_support_covered=574 r4_over_threshold=0')
    print('decision=ANCHOR_MAXIMAL_TEMPLATE_SUPPORT_DOES_NOT_COVER_ALL_577_TRANSFORMS')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
