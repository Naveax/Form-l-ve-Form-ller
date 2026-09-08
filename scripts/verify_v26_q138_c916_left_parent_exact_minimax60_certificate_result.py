#!/usr/bin/env python3
import probe_v26_q138_c916_left_parent_exact_minimax60_certificate as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['order'] == 'multiplicity_then_function'
    assert out['parent_interval'] == [0, 166]
    assert out['local_leaves'] == 166
    assert out['lower_bound_from_threshold59_no_go'] == 60
    assert out['explicit_width60_witness'] is True
    assert out['witness_source'] == 'baseline_function_tree_subtree'
    assert out['witness_edge_count'] == 330
    assert out['witness_max_depth'] == 9
    assert out['witness_safe_width'] == 60
    assert out['exact_fixed_order_contiguous_minimax_width'] == 60
    assert out['threshold59_direct_root_splits'] == 29
    assert out['threshold59_intervals_evaluated'] == 6270
    assert out['oracle_cache_entries_for_upper_witness'] == 330
    assert out['witness_edge_width_histogram'] == {
        11: 8, 12: 38, 13: 21, 14: 4, 15: 9, 16: 7, 17: 10, 18: 3,
        19: 1, 20: 8, 21: 64, 22: 39, 23: 5, 24: 10, 25: 18, 26: 12,
        27: 13, 28: 2, 29: 6, 30: 7, 31: 8, 32: 4, 33: 4, 34: 2, 35: 2,
        36: 2, 37: 1, 38: 2, 39: 2, 40: 1, 41: 1, 42: 2, 44: 1, 45: 1,
        47: 1, 49: 2, 50: 2, 56: 1, 57: 3, 59: 1, 60: 2,
    }
    assert [(e['lo'], e['hi'], e['safe_evaluation_bits']) for e in out['worst_witness_edges'][:3]] == [
        (110, 166, 60),
        (55, 110, 60),
        (0, 110, 59),
    ]
    print('PASS V26_Q138_C916_LEFT_PARENT_EXACT_MINIMAX60_CERTIFICATE_RESULT')
    print('decision=EXACT_FIXED_ORDER_CONTIGUOUS_MINIMAX_WIDTH_60')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
