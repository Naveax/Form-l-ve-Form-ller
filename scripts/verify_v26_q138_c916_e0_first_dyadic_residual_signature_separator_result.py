#!/usr/bin/env python3
import io
from contextlib import redirect_stdout

import probe_v26_q138_c916_e0_first_dyadic_residual_signature_separator as P


EXPECTED_R2_TEMPLATES = 39
EXPECTED_R4_TEMPLATES = 22


def main():
    buf = io.StringIO()
    with redirect_stdout(buf):
        out = P.analyze()

    assert out['synthetic_quadratic_signature_regression_cases'] == 2198
    assert out['baseline_radical_support_recursive_width'] == 61
    assert out['decision'] == 'RESIDUAL_SIGNATURE_AUGMENTATION_GAUGE_VALID_R2_WIDTH104_R4_WIDTH107'

    r2 = out['results'][2]
    assert r2['templates'] == EXPECTED_R2_TEMPLATES
    assert r2['assignment_residual_polar_rank_histogram'] == {0: 361, 2: 216}
    assert r2['minimal_signature_rank_histogram'] == {0: 39, 1: 322, 3: 216}
    assert r2['minimal_signature_rank_by_polar_rank'] == {
        0: {0: 39, 1: 322},
        2: {3: 216},
    }
    assert r2['scalar_cut_histogram'] == {0: 39, 1: 538}
    assert r2['total_signature_rows_before_group_union'] == 970
    assert r2['all_lift_gauges_contained_in_existing_radical_support_group_basis']
    assert r2['gauge_failure_count'] == 0
    assert r2['extra_rank_over_width61_group_basis_histogram'] == {
        0: 13, 1: 40, 2: 21, 3: 65, 4: 20, 5: 30, 6: 59, 7: 2,
    }
    assert r2['groups_with_zero_extra_rank'] == 13
    assert r2['max_extra_rank'] == 7
    assert r2['global_augmented_linear_rank'] == 149
    assert r2['recursive_widths'] == {
        'augmented_rank_ascending': 127,
        'augmented_rank_descending': 126,
        'extra_then_augmented': 111,
        'multiplicity_then_augmented': 104,
    }
    assert r2['best_recursive_order'] == 'multiplicity_then_augmented'
    assert r2['best_recursive_width'] == 104

    r4 = out['results'][4]
    assert r4['templates'] == EXPECTED_R4_TEMPLATES
    assert r4['assignment_residual_polar_rank_histogram'] == {0: 259, 2: 267, 4: 51}
    assert r4['minimal_signature_rank_histogram'] == {0: 22, 1: 237, 3: 267, 5: 51}
    assert r4['minimal_signature_rank_by_polar_rank'] == {
        0: {0: 22, 1: 237},
        2: {3: 267},
        4: {5: 51},
    }
    assert r4['scalar_cut_histogram'] == {0: 22, 1: 555}
    assert r4['total_signature_rows_before_group_union'] == 1293
    assert r4['all_lift_gauges_contained_in_existing_radical_support_group_basis']
    assert r4['gauge_failure_count'] == 0
    assert r4['extra_rank_over_width61_group_basis_histogram'] == {
        0: 7, 1: 31, 2: 17, 3: 58, 4: 20, 5: 36, 6: 68,
        7: 6, 8: 6, 12: 1,
    }
    assert r4['groups_with_zero_extra_rank'] == 7
    assert r4['max_extra_rank'] == 12
    assert r4['global_augmented_linear_rank'] == 149
    assert r4['recursive_widths'] == {
        'augmented_rank_ascending': 123,
        'augmented_rank_descending': 119,
        'extra_then_augmented': 118,
        'multiplicity_then_augmented': 107,
    }
    assert r4['best_recursive_order'] == 'multiplicity_then_augmented'
    assert r4['best_recursive_width'] == 107

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_RESIDUAL_SIGNATURE_SEPARATOR_RESULT')
    print('decision=RESIDUAL_SIGNATURE_AUGMENTATION_GAUGE_VALID_R2_WIDTH104_R4_WIDTH107')
    print('scope=frozen clean-checkout verification of exact minimal residual evaluation signatures, gauge containment, and residual-only recursive separator widths')
    print('important=template common high-rank sign cost remains excluded; widths 104/107 are residual-correction measurements, not complete grouped-e0 separator widths')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
