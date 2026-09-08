#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_bottleneck_parent_minimax_interval_dp as P

EXPECTED_HIST = {
    11: 1,
    12: 24,
    13: 58,
    14: 5,
    15: 13,
    16: 15,
    17: 4,
    18: 5,
    19: 2,
    20: 6,
    21: 1,
    22: 1,
    23: 3,
    24: 2,
    25: 2,
    29: 2,
    31: 3,
    32: 1,
    36: 1,
    40: 1,
    41: 1,
    42: 1,
    44: 1,
    46: 1,
    47: 1,
    48: 2,
    49: 1,
    51: 1,
    52: 1,
    53: 1,
    54: 2,
    55: 3,
}

EXPECTED_WORST = [
    (173, 243, 70, 55, 59, 6, '666736852e0e2036'),
    (173, 241, 68, 55, 59, 6, '9883979cefaaef27'),
    (173, 201, 28, 55, 57, 4, 'f1ab5bee99739b49'),
]


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['order'] == 'multiplicity_then_function'
    assert out['local_leaves'] == 84
    assert out['exact_minimax_safe_width'] == 55
    assert out['root_split'] == 167
    assert out['root_child_subtree_widths'] == [12, 55]
    assert out['witness_edge_count'] == 166
    assert out['witness_max_depth'] == 19
    assert out['witness_edge_width_histogram'] == EXPECTED_HIST
    assert out['intervals_evaluated'] == 3570
    assert out['dp_states'] == 3569
    assert out['split_comparisons'] == 98770
    assert out['oracle_cache_entries'] == 3570

    parent = out['parent']
    assert parent['lo'] == 166 and parent['hi'] == 250 and parent['size'] == 84
    assert parent['safe_evaluation_bits'] == 40
    assert parent['generic_safe_evaluation_bits'] == 40
    assert parent['function_lambda'] == 44
    assert parent['quadratic_residual_dim'] == 6
    assert parent['fiber_affine_residual'] is True
    assert parent['exact_override'] is False
    assert parent['digest'] == 'eba0751e307b560c'

    worst = out['worst_witness_edges']
    assert len([e for e in worst if e['safe_evaluation_bits'] == 55]) == 3
    for e, expected in zip(worst[:3], EXPECTED_WORST):
        got = (
            e['lo'], e['hi'], e['size'], e['safe_evaluation_bits'],
            e['function_lambda'], e['quadratic_residual_dim'], e['digest'],
        )
        assert got == expected
    assert all(e['safe_evaluation_bits'] <= 55 for e in worst)

    print('PASS V26_Q138_C916_BOTTLENECK_PARENT_MINIMAX_INTERVAL_DP_RESULT')
    print('exact_fixed_order_contiguous_optimum=55')
    print('improvement_vs_threshold_witness=4')
    print('improvement_vs_former_width65_edge=10')
    print('scope=fixed multiplicity-then-function order, all contiguous binary trees inside parent [166,250), retained parent edge excluded')
    print('not_claimed=unrestricted branchwidth or complete carry theorem')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
