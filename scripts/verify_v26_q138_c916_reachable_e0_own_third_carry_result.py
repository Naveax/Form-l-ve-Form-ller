#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_reachable_e0_own_third_carry as P

EXPECTED = {
    'position': 'C',
    'raw_e0_sectors': 577,
    'support_groups': 250,
    'correlated_groups': 111,
    'full_product_groups': 139,
    'reachable_e0_basis_dim': 388,
    'support_Walsh_dim': 788,
    'reachable_exact_ZZ_quotient': 128,
    'reachable_second_lift_total': 916,
    'max_group_joint_image_rank': 15,
    'support_syndrome_fibers_processed': 2304,
    'scalar_fibers_processed': 4608,
    'max_frequency_fiber_dimension': 11,
    'degree2_ANF_coefficients_inserted': 161336,
    'carry_evaluations': 174952,
    'unique_local_vectors_cached': 61841,
    'unique_coordinate_masks_cached': 61841,
    'reachable_e0_own_third_carry_GF2_span': 1164,
    'k9_repeated_target': 650,
    'target_met_by_e0_own_carry_span': False,
    'saturation': None,
}


def main():
    out = P.analyze()
    for key, expected in EXPECTED.items():
        actual = out[key]
        assert actual == expected, (key, actual, expected)

    assert out['reachable_e0_own_third_carry_GF2_span'] < 2048
    assert out['reachable_e0_own_third_carry_GF2_span'] > out['k9_repeated_target']

    print('PASS V26_Q138_C916_REACHABLE_E0_OWN_THIRD_CARRY_RESULT')
    print('C916_reachable_grouped_e0_own_third_carry_GF2_span<=1164')
    print('current_repeated_k9_target=650')
    print('verdict=SUBGENERIC_BUT_TARGET_NOT_MET')
    print('important=own-carry only; no cross-group/support/half carry and no complete C2')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
