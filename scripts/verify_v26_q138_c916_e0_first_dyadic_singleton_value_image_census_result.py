#!/usr/bin/env python3
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_singleton_value_image_census as P


def main():
    with redirect_stdout(io.StringIO()):
        out = P.analyze()

    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['synthetic_singleton_regression_cases'] == 4096
    assert out['raw_e0_sectors'] == 577
    assert out['support_groups'] == 250
    assert out['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert out['singleton_groups'] == 103
    assert out['singleton_residual_identity'] == 'R=(sum_t(-1)^q-2^k)/2=-sum_t q'

    assert out['singleton_projection_rank_histogram'] == {141: 1, 142: 49, 143: 53}
    assert out['singleton_local_fiber_dimension_histogram'] == {7: 53, 8: 49, 9: 1}
    assert out['singleton_identically_zero_gauss_histogram'] == {'false': 103}
    assert out['singleton_gauss_support_control_rank_histogram'] == {1: 26, 2: 45, 3: 28, 4: 4}
    assert out['singleton_nonzero_gauss_log2_abs_histogram'] == {4: 26, 5: 72, 6: 5}

    assert out['singleton_residual_image_size_histogram'] == {4: 103}
    assert out['singleton_residual_state_bits_histogram'] == {2: 103}
    assert out['singleton_residual_nonzero_value_count_histogram'] == {3: 103}
    assert out['singleton_residual_minimum_nonzero_valuation_histogram'] == {3: 26, 4: 72, 5: 5}
    assert out['singleton_residual_normalized_alphabet_histogram'] == {
        '[-5, -4, -3, 0]': 31,
        '[-9, -8, -7, 0]': 72,
    }
    assert out['residual_image_size_by_local_fiber_dimension'] == {
        7: {4: 53},
        8: {4: 49},
        9: {4: 1},
    }
    assert out['residual_image_size_by_projection_rank'] == {
        141: {4: 1},
        142: {4: 49},
        143: {4: 53},
    }

    groups = out['groups']
    assert len(groups) == 103
    assert len({g['group_id'] for g in groups}) == 103
    domain = 1 << 149
    for g in groups:
        assert g['multiplicity'] == 1
        assert g['support_free_dimension'] == 150
        p = g['shared_projection_rank']
        k = g['local_fiber_dimension']
        assert p + k == 150
        assert p in (141, 142, 143)
        assert k in (7, 8, 9)
        assert g['projection_size'] == (1 << p)
        assert g['outside_projection_size'] == domain - (1 << p)
        assert g['local_fiber_size'] == (1 << k)
        assert g['baseline_residual_value'] == -(1 << (k - 1))
        assert g['identically_zero_gauss'] is False
        assert g['gauss_sign_moment'] == 0
        assert g['gauss_support_control_rank'] in (1, 2, 3, 4)
        assert g['gauss_log2_abs_nonzero'] in (4, 5, 6)
        assert g['image_size'] == 4
        assert g['state_bits'] == 2
        assert g['nonzero_value_count'] == 3
        values = [r['value'] for r in g['value_multiplicity']]
        multiplicities = [r['multiplicity'] for r in g['value_multiplicity']]
        assert len(values) == 4 and values == sorted(values)
        assert values[-1] == 0
        assert all(v < 0 for v in values[:-1])
        assert all(n > 0 for n in multiplicities)
        assert sum(multiplicities) == domain
        assert g['normalized_alphabet'] in (
            [-5, -4, -3, 0],
            [-9, -8, -7, 0],
        )

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SINGLETON_VALUE_IMAGE_CENSUS_RESULT')
    print('exact=103 singleton residual groups; every exact 149-bit-domain image has 4 values and needs 2 isolated state bits')
    print('projection_rank=141:1,142:49,143:53; local_fiber_dimension=7:53,8:49,9:1')
    print('gauss_control_rank=1:26,2:45,3:28,4:4; nonzero_gauss_log2_abs=4:26,5:72,6:5')
    print('minimum_nonzero_v2=3:26,4:72,5:5')
    print('normalized_alphabet=[-5,-4,-3,0]:31;[-9,-8,-7,0]:72')
    print('decision=SINGLETON_FIRST_DYADIC_EXACT_VALUE_IMAGE_CENSUS_COMPLETE')
    print('important=isolated 2-bit group labels do not imply a 2-bit or bounded-small joint representation across all 250 groups')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
