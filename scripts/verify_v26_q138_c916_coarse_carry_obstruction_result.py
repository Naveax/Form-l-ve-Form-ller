#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_coarse_carry_obstruction as P

EXPECTED_SPECTRUM_GROWTH = [
    (1, 40), (2, 40), (3, 48), (4, 48), (5, 48), (6, 48),
    (7, 48), (8, 48), (32, 48), (64, 1132), (96, 1132), (98, 2048),
]


def main():
    r = P.analyze()
    assert r['position'] == 'C'
    assert r['support_frequency_dim'] == 788
    assert r['support_carry_xor_sumset_size'] == 2048
    assert r['support_carry_sumset_saturated'] is True
    assert tuple(r['support_carry_saturation_witness']) == (108, 162, 1885)
    assert r['reachable_sign_basis_dim'] == 388
    assert r['reachable_sign_pairwise_truth_hull_dim'] == 1848
    assert r['reachable_sign_pairwise_pairs_tested'] == 75078
    assert r['reachable_sign_pairwise_saturation_pair'] is None
    assert r['reachable_sign_fourier_union_size'] == 2048
    assert r['reachable_sign_fourier_union_full_after_basis_vectors'] == 98
    assert r['support_times_sign_shift_union_size'] == 2048
    assert r['support_times_sign_shift_union_saturated'] is True
    assert r['support_times_sign_shift_union_full_after_support_index'] == 0
    assert r['spectrum_growth_samples'] == EXPECTED_SPECTRUM_GROWTH
    print('PASS V26_Q138_C916_COARSE_CARRY_OBSTRUCTION_RESULT')
    print('support_only_carry_sumset=2048')
    print('reachable_sign_pairwise_truth_hull=1848')
    print('reachable_sign_fourier_union=2048')
    print('support_times_sign_shift_union=2048')
    print('verdict=NO_COMPONENTWISE_AMBIENT_CARRY_GAIN')
    print('important=not a lower bound on exact joint realized C2')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
