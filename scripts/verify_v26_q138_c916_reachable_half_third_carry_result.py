#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_reachable_half_third_carry as P

EXPECTED = {
    'mode': 'degree4_exact_relaxed_family',
    'reachable_pairwise_hull': 1848,
    'reachable_half_induced_third_carry_GF2_span': 636,
    'k9_repeated_target': 650,
    'target_met_by_half_only_carry_span': True,
    'second_lift_total': 916,
    'feasible_support_fibers': 8,
    'nonzero_support_fibers': 4,
    'scalar_fibers': 64,
    'max_fiber_dimension': 15,
    'max_subset_evaluations_per_scalar_fiber': 1941,
    'carry_evaluations': 124480,
    'ANF_coefficients_inserted': 124224,
    'unique_half_vectors_cached': 65809,
    'unique_coordinate_masks_cached': 65809,
}


def main():
    out = P.analyze()
    assert out == EXPECTED, (out, EXPECTED)
    assert out['reachable_half_induced_third_carry_GF2_span'] == 636
    assert out['reachable_half_induced_third_carry_GF2_span'] <= out['k9_repeated_target'] == 650
    print('PASS V26_Q138_C916_REACHABLE_HALF_THIRD_CARRY_RESULT')
    print('C916_reachable_relaxed_half_induced_third_carry_GF2_span<=636')
    print('current_repeated_k9_target=650')
    print('important=636 is half-induced carry only, not a complete C2 bound')
    print('not_included=reachable grouped-e0 own carry, support-only carry, cross-carries, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
