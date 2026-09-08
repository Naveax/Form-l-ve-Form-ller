#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_hybrid_aggregate_scalar_separator as P

EXPECTED = {
    'position': 'C',
    'raw_e0_sectors': 577,
    'support_groups': 250,
    'singleton_groups': 103,
    'multi_sector_groups': 147,
    'singleton_polar_rank_histogram': {136: 6, 138: 50, 140: 41, 142: 6},
    'multi_sector_polar_rank_histogram': {2: 8, 4: 53, 6: 71, 8: 11, 10: 3, 12: 1},
    'polar_rank_split_exact': True,
    'baseline_unrefined_recursive_width': 58,
    'hybrid_linear_global_rank': 149,
    'hybrid_linear_best_recursive_width': 83,
    'hybrid_linear_best_recursive_depth': 11,
    'singleton_polar_span_rank': 94,
    'singleton_polar_affine_difference_rank': 93,
    'singleton_full_quadratic_polynomial_span_rank': 100,
    'singleton_full_quadratic_polynomial_affine_difference_rank': 99,
    'multi_sector_polar_span_rank': 88,
    'multi_sector_full_quadratic_polynomial_span_rank': 102,
}

EXPECTED_RECURSIVE = {
    'hybrid_rank_ascending': 111,
    'hybrid_rank_descending': 91,
    'multiplicity_then_hybrid': 83,
}
EXPECTED_PATH = {
    'hybrid_rank_ascending': 120,
    'hybrid_rank_descending': 104,
    'multiplicity_then_hybrid': 94,
}


def main():
    out = P.analyze()
    for key, expected in EXPECTED.items():
        actual = out[key]
        assert actual == expected, (key, actual, expected)
    assert out['hybrid_linear_recursive_widths'] == EXPECTED_RECURSIVE
    assert out['hybrid_linear_path_widths'] == EXPECTED_PATH
    assert out['hybrid_linear_best_recursive_order'] == 'multiplicity_then_hybrid'
    assert out['hybrid_linear_best_balanced_cut'] == {
        'left_groups': 125,
        'right_groups': 125,
        'left_rank': 61,
        'right_rank': 149,
        'lambda': 61,
        'name': 'multiplicity_then_hybrid_half',
    }
    assert out['hybrid_linear_best_recursive_root_children'] == [
        {'size': 166, 'rank': 71, 'complement_rank': 123, 'lambda': 45},
        {'size': 84, 'rank': 123, 'complement_rank': 71, 'lambda': 45},
    ]

    print('PASS V26_Q138_C916_HYBRID_AGGREGATE_SCALAR_SEPARATOR_RESULT')
    print('singleton_high_polar_groups=103')
    print('multi_sector_low_polar_groups=147')
    print('hybrid_linear_recursive_width=83')
    print('full_linear_refinement_recursive_width=147')
    print('singleton_full_quadratic_polynomial_span_rank=100')
    print('verdict=HYBRID_LINEAR_SKELETON_SURVIVES_BUT_SINGLETON_QUADRATICS_NEAR_INDEPENDENT')
    print('important=width83 excludes nonlinear singleton label cost; no complete separator/carry bound')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
