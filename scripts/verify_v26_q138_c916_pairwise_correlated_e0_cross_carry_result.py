#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_pairwise_correlated_e0_cross_carry as P

EXPECTED = {
    'position': 'C',
    'reachable_e0_basis_dim': 388,
    'reachable_second_lift_total': 916,
    'group_count': 250,
    'group_pairs_total': 31125,
    'group_pairs_started': 31125,
    'group_pairs_completed_before_stop': 31125,
    'support_pair_fibers_processed': 610335,
    'scalar_fibers_processed': 2441340,
    'max_joint_frequency_image_rank': 15,
    'frequency_image_generators_mapped': 83744693,
    'degree2_ANF_coefficients_inserted': 65447487,
    'pairwise_correlated_e0_cross_carry_GF2_span': 1848,
    'saturation': None,
    'coordinate_cache_size': 25008,
    'truth_cache_size': 1039920,
    'polar_cache_size': 8589161,
    'k9_repeated_target': 650,
}


def main():
    out = P.analyze()
    for key, expected in EXPECTED.items():
        actual = out[key]
        assert actual == expected, (key, actual, expected)

    # The exact shared-state pairwise envelope equals the historical ambient
    # reachable-basis pairwise truth hull. Pairwise correlation therefore buys
    # no dimension reduction, but this remains an upper-envelope statement,
    # not a lower bound on the true all-group realized carry or complete C2.
    assert out['pairwise_correlated_e0_cross_carry_GF2_span'] == 1848
    assert out['group_pairs_completed_before_stop'] == out['group_pairs_total']
    assert out['saturation'] is None

    print('PASS V26_Q138_C916_PAIRWISE_CORRELATED_E0_CROSS_CARRY_RESULT')
    print('pairwise_correlated_e0_cross_carry_GF2_span=1848')
    print('ambient_reachable_basis_pairwise_truth_hull=1848')
    print('verdict=NO_PAIRWISE_CORRELATED_CROSS_GAIN')
    print('important=upper-envelope diagnostic only; not a lower bound on exact all-group realized carry or complete C2')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
