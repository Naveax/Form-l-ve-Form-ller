#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_local_gauss_transform_quotient_geometry as P


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['small_split_quadratic_forms_exhaustively_checked'] == 4096
    assert out['small_split_identically_zero_transforms'] == {
        '2_shared_2_local': 336,
        '1_shared_3_local': 644,
    }

    assert out['raw_e0_sectors'] == 577
    assert out['support_groups'] == 250
    assert out['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert out['shared_projection_rank_histogram'] == {
        141: 133, 142: 317, 143: 127,
    }
    assert out['local_fiber_dimension_histogram'] == {
        7: 127, 8: 309, 9: 141,
    }
    assert out['local_fiber_polar_rank_histogram'] == {
        4: 209, 6: 329, 8: 39,
    }
    assert out['local_fiber_radical_dimension_histogram'] == {
        0: 3, 1: 88, 2: 172, 3: 180, 4: 134,
    }
    assert out['support_control_rank_histogram'] == {
        0: 3, 1: 88, 2: 172, 3: 180, 4: 134,
    }

    assert out['identically_zero_gauss_sectors'] == 0
    assert out['nonzero_gauss_sectors'] == 577
    assert out['identically_zero_gauss_by_multiplicity'] == {}
    assert out['nonzero_gauss_log2_abs_histogram'] == {
        4: 55, 5: 283, 6: 239,
    }
    assert out['support_free_dimension_after_radical_constraints_histogram'] == {
        138: 233, 139: 6, 140: 281, 141: 2, 142: 55,
    }

    assert out['normalized_sign_polar_rank_histogram'] == {
        130: 162, 132: 275, 134: 125, 136: 15,
    }
    assert out['normalized_sign_affine_sectors'] == 0
    assert out['normalized_sign_constant_sectors'] == 0
    assert out['max_normalized_sign_polar_rank'] == 136
    assert out['normalized_sign_polar_rank_by_multiplicity'] == {
        1: {130: 4, 132: 53, 134: 38, 136: 8},
        2: {130: 7, 132: 59, 134: 43, 136: 5},
        4: {130: 151, 132: 163, 134: 44, 136: 2},
    }
    assert out['nonzero_gauss_log2_abs_by_multiplicity'] == {
        1: {4: 26, 5: 72, 6: 5},
        2: {4: 12, 5: 88, 6: 14},
        4: {4: 17, 5: 123, 6: 220},
    }

    assert len(out['groups']) == 250
    assert sum(
        len(g['sectors']) for g in out['groups']
    ) == 577
    assert all(
        not sector['identically_zero']
        for group in out['groups']
        for sector in group['sectors']
    )

    print('PASS V26_Q138_C916_E0_LOCAL_GAUSS_TRANSFORM_QUOTIENT_GEOMETRY_RESULT')
    print('small_quadratic_regression_forms=4096')
    print('actual_nonzero_gauss_sectors=577')
    print('normalized_sign_polar_rank_min=130')
    print('normalized_sign_polar_rank_max=136')
    print('decision=LOCAL_GAUSS_QUOTIENT_SIGN_POLAR_RANK130_136')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
