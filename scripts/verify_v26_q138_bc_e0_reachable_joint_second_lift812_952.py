#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_reachable_joint_sign_span as P

EXPECTED = {
    'B': {
        'canonical_e0_rank_F2': 272,
        'reachable_joint_gauge_e0_rank_F2': 272,
        'canonical_e0_plus_half_rank_F2': 348,
        'reachable_e0_plus_half_rank_F2': 348,
        'support_Walsh_dim': 668,
        'old_exact_ZZ_quotient_rank': 144,
        'reachable_exact_ZZ_quotient_rank': 144,
        'old_second_lift_rank_bound': 812,
        'reachable_second_lift_rank_bound': 812,
        'correlated_groups': 91,
        'full_product_groups': 160,
        'max_joint_rank_gap': 2,
        'max_correlated_joint_image_rank': 14,
    },
    'C': {
        'canonical_e0_rank_F2': 388,
        'reachable_joint_gauge_e0_rank_F2': 388,
        'canonical_e0_plus_half_rank_F2': 432,
        'reachable_e0_plus_half_rank_F2': 432,
        'support_Walsh_dim': 788,
        'old_exact_ZZ_quotient_rank': 184,
        'reachable_exact_ZZ_quotient_rank': 164,
        'old_second_lift_rank_bound': 972,
        'reachable_second_lift_rank_bound': 952,
        'correlated_groups': 111,
        'full_product_groups': 139,
        'max_joint_rank_gap': 2,
        'max_correlated_joint_image_rank': 14,
    },
}


def main():
    out = {pos: P.analyze(pos) for pos in 'BC'}
    for pos in 'BC':
        for key, expected in EXPECTED[pos].items():
            actual = out[pos][key]
            assert actual == expected, (pos, key, actual, expected)

    # The new theorem is deliberately asymmetric. No GF(2) span-dimension
    # reduction is claimed for either position. The C improvement appears only
    # after exact integer Walsh-complement quotienting of the tighter reachable
    # generator family.
    assert out['B']['e0_rank_gain'] == 0
    assert out['B']['union_rank_gain'] == 0
    assert out['B']['quotient_rank_gain'] == 0
    assert out['B']['second_lift_rank_gain'] == 0

    assert out['C']['e0_rank_gain'] == 0
    assert out['C']['union_rank_gain'] == 0
    assert out['C']['quotient_rank_gain'] == 20
    assert out['C']['second_lift_rank_gain'] == 20

    print('PASS V26_Q138_BC_E0_REACHABLE_JOINT_SECOND_LIFT812_952')
    print('B_reachable_joint_second_integer_lift_rank_Q<=812')
    print('C_reachable_joint_second_integer_lift_rank_Q<=952')
    print('C_exact_ZZ_Walsh_complement_quotient_rank=164')
    print('C_previous_exact_ZZ_Walsh_complement_quotient_rank=184')
    print('important=no_GF2_e0_or_e0_plus_half_dimension_reduction; the C gain is exact ZZ quotient geometry')
    print('scope=admitted gauge-closed grouped-e0 sign span plus unchanged half span, quotient by admitted support-only Walsh space')
    print('not_included=complete B2/C2, W_repr, alpha, arithmetic-work, ranking/search, full-round')


if __name__ == '__main__':
    main()
