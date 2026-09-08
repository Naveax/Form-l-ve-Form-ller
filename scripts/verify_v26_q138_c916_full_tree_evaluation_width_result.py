#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_full_tree_evaluation_width as P
import probe_v26_q138_c916_width65_edge_exact_fiber_count as W


def main():
    base = P.analyze()
    assert base['position'] == 'C'
    assert base['support_groups'] == 250
    assert base['tree_edges_analyzed'] == 498
    assert base['function_space_tree_width'] == 70
    assert base['function_space_tree_depth'] == 10
    assert base['residual_zero_edges'] == 175
    assert base['fiber_affine_residual_edges'] == 372
    assert base['fiber_quadratic_residual_edges'] == 126
    assert base['safe_full_tree_evaluation_width_upper_bound'] == 65
    assert base['safe_evaluation_bit_histogram'][65] == 1
    assert max(k for k, v in base['safe_evaluation_bit_histogram'].items() if k != 65 and v) == 64

    old = base['unique_former_width70_edge']
    assert (old['lo'], old['hi'], old['size']) == (110, 166, 56)
    assert old['function_lambda'] == 70
    assert old['shared_affine_linear_rank'] == 56
    assert old['quadratic_residual_dim'] == 13
    assert old['common_kernel_dual_row_span_rank'] == 4
    assert old['translation_matrix_control_rank'] == 4
    assert old['safe_evaluation_bits'] == 60

    got = W.analyze()
    assert got['position'] == 'C'
    assert got['edge'] == {'lo': 166, 'hi': 199, 'size': 33}
    assert got['function_lambda'] == 68
    assert got['shared_affine_function_dim'] == 63
    assert got['varying_affine_label_rank'] == 62
    assert got['fiber_kernel_dim'] == 87
    assert got['quadratic_residual_dim'] == 5
    assert got['common_kernel_dual_row_span_rank'] == 3
    assert got['translation_matrix_control_rank'] == 3
    assert got['translation_matrix_control_states'] == 8
    assert got['fiber_labels_per_control_state'] == 1 << 59
    assert got['control_state_residual_rank_histogram'] == {1: 1, 2: 2, 3: 5}
    assert got['exact_shared_evaluation_state_count'] == 28823037615171174400
    assert got['exact_shared_evaluation_state_ceiling_bits'] == 65
    assert got['max_other_edge_safe_bits'] == 64
    assert got['refined_safe_full_tree_evaluation_width_upper_bound'] == 65

    print('PASS V26_Q138_C916_FULL_TREE_EVALUATION_WIDTH_RESULT')
    print('C_function_space_width=70')
    print('C_safe_full_tree_evaluation_width_upper_bound=65')
    print('former_width70_edge_safe_bits=60')
    print('unique_width65_edge_exact_states=28823037615171174400')
    print('unique_width65_edge_exact_ceiling_bits=65')
    print('all_other_edges_safe_bits<=64')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
