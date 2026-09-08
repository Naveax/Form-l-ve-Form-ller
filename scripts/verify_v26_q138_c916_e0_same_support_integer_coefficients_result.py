#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_same_support_integer_coefficients as P


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['raw_e0_sectors'] == 577
    assert out['support_groups'] == 250
    assert out['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert out['support_free_dimension_histogram'] == {150: 248, 151: 2}
    assert out['phase_signature_bits_histogram'] == {11326: 248, 11477: 2}

    assert out['restricted_phase_classes_before_sign_combine'] == 577
    assert out['classes_per_group_histogram'] == {1: 103, 2: 57, 4: 90}
    assert out['nonzero_classes_per_group_histogram'] == {1: 103, 2: 57, 4: 90}

    assert out['coefficient_histogram'] == {-1: 295, 1: 282}
    assert out['absolute_coefficient_histogram'] == {1: 577}
    assert out['exact_opposite_zero_classes'] == 0
    assert out['exact_nonzero_integer_classes'] == 577
    assert out['odd_coefficient_classes'] == 577
    assert out['even_nonzero_coefficient_classes'] == 0
    assert out['zeroed_entire_support_groups'] == 0
    assert out['groups_with_restricted_phase_collision'] == 0
    assert out['groups_with_abs_coefficient_gt1'] == 0
    assert out['max_abs_coefficient'] == 1
    assert out['singleton_groups'] == 103

    assert len(out['groups']) == 250
    for g in out['groups']:
        assert g['restricted_nonconstant_phase_classes'] == g['multiplicity']
        assert g['nonzero_integer_classes'] == g['multiplicity']
        assert g['max_abs_coefficient'] == 1

    print('PASS V26_Q138_C916_E0_SAME_SUPPORT_INTEGER_COEFFICIENTS_RESULT')
    print('exact=577 reachable sectors remain 577 distinct restricted nonconstant phase classes')
    print('coefficients=-1:295,+1:282; zero=0; even_nonzero=0; abs_gt1=0; collisions=0')
    print('decision=NO_SAME_SUPPORT_CROSS_SECTOR_INTEGER_AGGREGATION')
    print('important=negative unit coefficients remain signed and their later 2-adic lift is not claimed resolved here')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
