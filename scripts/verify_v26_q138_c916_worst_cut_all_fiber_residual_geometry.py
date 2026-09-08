#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_worst_cut_all_fiber_residual_upper_bound as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['edge'] == {'lo': 110, 'hi': 166, 'size': 56}
    assert out['function_lambda'] == 70
    assert out['shared_affine_function_dim'] == 57
    assert out['varying_affine_label_rank'] == 56
    assert out['fiber_kernel_dim'] == 93
    assert out['quadratic_residual_dim'] == 13
    assert out['origin_fiber_residual_rank'] == 4
    assert out['origin_fiber_image_size'] == 16
    assert out['translation_effect_vectors'] == 1937
    assert out['common_kernel_dual_row_span_rank'] == 4
    assert out['translation_matrix_control_rank'] == 4
    assert out['translation_matrix_control_states'] == 16
    assert out['fiber_labels_per_control_state'] == 1 << 52
    assert out['control_state_residual_rank_histogram'] == {1: 1, 2: 2, 3: 7, 4: 6}
    assert out['all_affine_fiber_residual_rank_histogram'] == {
        1: 1 << 52,
        2: 2 << 52,
        3: 7 << 52,
        4: 6 << 52,
    }
    assert out['all_fiber_residual_rank_upper_bound'] == 4
    assert out['all_fiber_residual_image_upper_bound'] == 16
    assert out['max_fiber_residual_rank_exact'] == 4
    assert out['max_fiber_residual_image_exact'] == 16
    assert out['shared_evaluation_state_upper_bits'] == 60
    assert out['shared_evaluation_state_upper_bound'] == 1 << 60
    assert out['exact_shared_evaluation_state_count'] == 729583139634020352
    assert out['exact_shared_evaluation_state_ceiling_bits'] == 60
    print('PASS V26_Q138_C916_WORST_CUT_ALL_FIBER_RESIDUAL_GEOMETRY_RESULT')
    print('exact_control_hist={1:1,2:2,3:7,4:6}')
    print('exact_shared_evaluation_states=729583139634020352')
    print('worst_fiber_residual_rank=4')
    print('ceiling_bits=60')
    print('scope=unique width-70 edge only; not a full-tree evaluation-width theorem')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
