#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_gauss_radical_augmented_separator as P


def main():
    # The augmented rows and the existing grouped-e0 basis must use exactly
    # the same 149-bit coordinate order, not merely the same coordinate set.
    assert P.SHARED_EXT == tuple(P.A.S.RIGHT)
    assert len(P.SHARED_EXT) == P.DOMAIN_BITS == 149

    out = P.analyze()
    assert out['position'] == 'C'
    assert out['support_groups'] == 250
    assert out['global_refined_rank'] == 149
    assert out['all_group_gauges_contained_in_existing_support_basis'] is True
    assert out['all_group_lifted_ranks_match_control_ranks'] is True

    assert out['radical_control_rank_histogram'] == {
        1: 29, 2: 46, 3: 68, 4: 20, 5: 48, 6: 39,
    }
    assert out['base_rank_histogram'] == {
        11: 24, 12: 107, 13: 15, 14: 1, 19: 4, 20: 14, 21: 85,
    }
    assert out['refined_rank_histogram'] == {
        12: 3, 13: 6, 14: 8, 15: 24, 16: 25,
        17: 38, 18: 40, 19: 7, 20: 14, 21: 85,
    }
    assert out['extra_rank_histogram'] == {
        0: 103, 1: 3, 2: 8, 3: 36, 4: 14, 5: 47, 6: 39,
    }
    assert out['max_extra_rank'] == 6
    assert out['groups_with_zero_extra_rank'] == 103
    assert out['gauge_dimension_histogram'] == {6: 78, 7: 137, 8: 35}

    assert out['base_recursive_width'] == 58
    assert out['base_recursive_depth'] == 11
    assert out['recursive_widths'] == {
        'base_multiplicity_then_rank': 67,
        'multiplicity_then_refined': 61,
        'radical_rank_ascending': 65,
        'refined_rank_ascending': 70,
        'refined_rank_descending': 82,
    }
    assert out['best_recursive_order'] == 'multiplicity_then_refined'
    assert out['best_recursive_width'] == 61
    assert out['best_recursive_depth'] == 11
    assert out['best_recursive_root_children'] == [
        {'size': 166, 'rank': 64, 'complement_rank': 125, 'lambda': 40},
        {'size': 84, 'rank': 125, 'complement_rank': 64, 'lambda': 40},
    ]
    assert out['best_balanced_cut'] == {
        'name': 'radical_rank_ascending_half',
        'left_groups': 125,
        'right_groups': 125,
        'left_rank': 52,
        'right_rank': 149,
        'lambda': 52,
    }

    print('PASS V26_Q138_C916_E0_GAUSS_RADICAL_AUGMENTED_SEPARATOR_RESULT')
    print('coordinate_order_matches_existing_separator=1')
    print('gauge_containment_all_250_groups=1')
    print('global_refined_rank=149')
    print('best_recursive_width=61')
    print('decision=GAUSS_RADICAL_SUPPORT_AUGMENTED_SEPARATOR_WIDTH61')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
