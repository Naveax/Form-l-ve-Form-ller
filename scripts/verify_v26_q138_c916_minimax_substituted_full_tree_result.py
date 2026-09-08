#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_minimax_substituted_full_tree as P


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['support_groups'] == 250
    assert out['tree_edges_analyzed'] == 498
    assert out['baseline_function_tree_width'] == 70
    assert out['baseline_function_tree_depth'] == 10
    assert out['local_minimax_width'] == 55
    assert out['local_root_split'] == 167
    assert out['local_witness_edge_count'] == 166
    assert out['outside_safe_width'] == 60
    assert out['substituted_full_tree_safe_width'] == 60
    assert out['substituted_full_tree_function_width'] == 70
    assert out['substituted_full_tree_depth'] == 20
    assert out['oracle_cache_entries'] == 498

    expected_hist = {
        11: 9, 12: 62, 13: 79, 14: 9, 15: 22, 16: 22, 17: 14,
        18: 8, 19: 3, 20: 14, 21: 65, 22: 40, 23: 8, 24: 12,
        25: 20, 26: 12, 27: 13, 28: 2, 29: 8, 30: 7, 31: 11,
        32: 5, 33: 4, 34: 2, 35: 2, 36: 3, 37: 1, 38: 2, 39: 2,
        40: 4, 41: 2, 42: 3, 44: 2, 45: 1, 46: 1, 47: 2, 48: 2,
        49: 3, 50: 2, 51: 1, 52: 1, 53: 1, 54: 2, 55: 3, 56: 1,
        57: 3, 59: 1, 60: 2,
    }
    assert out['safe_evaluation_bit_histogram'] == expected_hist

    worst = out['worst_edges']
    assert len(worst) >= 3
    a, b, c = worst[:3]
    assert (a['lo'], a['hi'], a['safe_evaluation_bits']) == (110, 166, 60)
    assert a['exact_override'] is True
    assert a['function_lambda'] == 70
    assert a['generic_safe_evaluation_bits'] == 60
    assert a['quadratic_residual_dim'] == 13
    assert a['fiber_affine_residual'] is True

    assert (b['lo'], b['hi'], b['safe_evaluation_bits']) == (55, 110, 60)
    assert b['exact_override'] is True
    assert b['function_lambda'] == 64
    assert b['generic_safe_evaluation_bits'] == 64
    assert b['quadratic_residual_dim'] == 12
    assert b['fiber_affine_residual'] is False

    assert (c['lo'], c['hi'], c['safe_evaluation_bits']) == (0, 110, 59)
    assert c['exact_override'] is False
    assert c['function_lambda'] == 65

    assert sum(expected_hist.values()) == 498
    assert expected_hist[60] == 2
    assert expected_hist[55] == 3

    print('PASS V26_Q138_C916_MINIMAX_SUBSTITUTED_FULL_TREE_RESULT')
    print('exact=498-edge substituted C916 tree has safe evaluation width 60')
    print('bottlenecks=[110,166):60 and [55,110):60; former 65-bit [166,199) edge removed')
    print('local_minimax=55; full_tree_function_width=70; depth=20')
    print('decision=FREEZE_COMPLETE_DISPLAYED_TREE_WIDTH60')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
