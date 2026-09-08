#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_width64_quadratic_edge_origin_image as O
import probe_v26_q138_c916_width64_quadratic_edge_all_fiber_image as A


def main():
    origin = O.analyze()
    assert origin['position'] == 'C'
    assert origin['edge'] == {'lo': 55, 'hi': 110, 'size': 55}
    assert origin['function_lambda'] == 64
    assert origin['shared_affine_function_dim'] == 52
    assert origin['shared_affine_linear_rank'] == 52
    assert origin['constant_in_shared_affine_space'] is False
    assert origin['origin_fiber_kernel_dim'] == 97
    assert origin['quadratic_residual_dim'] == 12
    assert origin['restricted_nonzero_polar_basis_count'] == 1
    assert origin['restricted_polar_space_rank'] == 1
    assert origin['characters_evaluated'] == 4096
    assert origin['zero_gauss_characters'] == 4080
    assert origin['nonzero_gauss_characters'] == 16
    assert origin['restricted_polar_rank_histogram'] == {0: 2048, 88: 2048}
    assert origin['nonzero_gauss_log2_abs_histogram'] == {97: 16}
    assert origin['origin_fiber_residual_image_size'] == 256
    assert origin['origin_fiber_residual_image_ceiling_bits'] == 8
    assert origin['origin_fiber_missing_outputs'] == 3840
    assert origin['origin_fiber_distinct_preimage_counts'] == 1
    assert origin['origin_fiber_min_nonzero_preimages'] == 1 << 89
    assert origin['origin_fiber_max_preimages'] == 1 << 89

    got = A.analyze()
    assert got['position'] == 'C'
    assert got['edge'] == {'lo': 55, 'hi': 110, 'size': 55}
    assert got['function_lambda'] == 64
    assert got['shared_affine_linear_rank'] == 52
    assert got['fiber_kernel_dim'] == 97
    assert got['quadratic_residual_dim'] == 12
    assert got['affine_residual_coordinate_count'] == 11
    assert got['quadratic_residual_coordinate_count'] == 1
    assert got['fixed_restricted_quadratic_polar_rank'] == 88
    assert got['fixed_restricted_quadratic_radical_dim'] == 9
    assert got['max_totally_isotropic_dim'] == 53
    assert got['minimum_affine_residual_fiber_kernel_dim'] == 86
    assert got['origin_affine_residual_rank'] == 7
    assert got['common_affine_residual_kernel_dual_row_span_rank'] == 7
    assert got['translation_affine_residual_matrix_control_rank'] == 3
    assert got['translation_control_states'] == 8
    assert got['affine_labels_per_control_state'] == 1 << 49
    assert got['control_state_affine_residual_rank_histogram'] == {5: 1, 6: 2, 7: 5}
    assert got['max_affine_residual_rank_all_fibers'] == 7
    assert got['max_residual_image_size_all_fibers'] == 256
    assert got['max_residual_image_bits_all_fibers'] == 8
    assert got['exact_shared_evaluation_state_count'] == 900719925474099200
    assert got['exact_shared_evaluation_state_ceiling_bits'] == 60

    print('PASS V26_Q138_C916_WIDTH64_QUADRATIC_EDGE_ALL_FIBER_IMAGE_RESULT')
    print('edge=[55,110)')
    print('origin_residual_image=256')
    print('all_fiber_max_residual_image=256')
    print('translation_control_rank=3')
    print('exact_shared_evaluation_states=900719925474099200')
    print('exact_shared_evaluation_ceiling_bits=60')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
