#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_reachable_half_relaxed_zz as P

EXPECTED = {
    'B': {
        'half_linear_image_rank': 18,
        'half_feasible_linear_states': 131072,
        'half_generated_state_pairs': 2097152,
        'half_relaxed_rank_F2': 144,
        'raw_e0_sectors': 581,
        'support_groups': 251,
        'reachable_e0_rank_F2': 272,
        'correlated_groups': 91,
        'full_product_groups': 160,
        'canonical_e0_plus_relaxed_half_rank_F2': 272,
        'reachable_e0_plus_relaxed_half_rank_F2': 272,
        'support_Walsh_dim': 668,
        'Walsh_complement_coordinates': 1380,
        'canonical_relaxed_exact_ZZ_quotient_rank': 80,
        'reachable_relaxed_exact_ZZ_quotient_rank': 92,
        'canonical_relaxed_second_lift_rank_bound': 748,
        'reachable_relaxed_second_lift_rank_bound': 760,
        'reachable_vs_canonical_relaxed_gain': -12,
    },
    'C': {
        'half_linear_image_rank': 18,
        'half_feasible_linear_states': 131072,
        'half_generated_state_pairs': 2097152,
        'half_relaxed_rank_F2': 144,
        'raw_e0_sectors': 577,
        'support_groups': 250,
        'reachable_e0_rank_F2': 388,
        'correlated_groups': 111,
        'full_product_groups': 139,
        'canonical_e0_plus_relaxed_half_rank_F2': 388,
        'reachable_e0_plus_relaxed_half_rank_F2': 388,
        'support_Walsh_dim': 788,
        'Walsh_complement_coordinates': 1260,
        'canonical_relaxed_exact_ZZ_quotient_rank': 148,
        'reachable_relaxed_exact_ZZ_quotient_rank': 128,
        'canonical_relaxed_second_lift_rank_bound': 936,
        'reachable_relaxed_second_lift_rank_bound': 916,
        'reachable_vs_canonical_relaxed_gain': 20,
    },
}


def main():
    out = {pos: P.analyze(pos) for pos in 'BC'}
    for pos in 'BC':
        for key, expected in EXPECTED[pos].items():
            actual = out[pos][key]
            assert actual == expected, (pos, key, actual, expected)

    # The GF(2) dimensions are unchanged.  The exact ZZ Walsh-complement
    # quotient reacts asymmetrically to the reachable generator basis, so the
    # certified positionwise envelope deliberately selects different admitted
    # constructions for B and C.
    assert out['B']['reachable_relaxed_exact_ZZ_quotient_rank'] - out['B']['canonical_relaxed_exact_ZZ_quotient_rank'] == 12
    assert out['C']['canonical_relaxed_exact_ZZ_quotient_rank'] - out['C']['reachable_relaxed_exact_ZZ_quotient_rank'] == 20

    best = {
        pos: min(
            out[pos]['canonical_relaxed_second_lift_rank_bound'],
            out[pos]['reachable_relaxed_second_lift_rank_bound'],
        )
        for pos in 'BC'
    }
    assert best == {'B': 748, 'C': 916}

    print('PASS V26_Q138_BC_E0_REACHABLE_HALF_RELAXED_ZZ748_916')
    print('B_second_integer_lift_rank_Q<=748 via canonical grouped-e0 + exact-linear-image relaxed-half span')
    print('C_second_integer_lift_rank_Q<=916 via reachable-joint grouped-e0 + exact-linear-image relaxed-half span')
    print('B_exact_ZZ_quotients canonical=80 reachable=92; choose canonical')
    print('C_exact_ZZ_quotients canonical=148 reachable=128; choose reachable')
    print('important=same GF2 dimensions do not imply the same displayed ZZ Walsh-complement quotient rank; no monotonicity claim is used')
    print('scope=second dyadic integer-lift sign-span upper bounds with half scalar phase safely relaxed to all 16 patterns per exact linear image state')
    print('not_included=complete B2/C2, W_repr, alpha, arithmetic-work, ranking/search, full-round')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
