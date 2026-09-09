#!/usr/bin/env python3
import probe_v26_q138_c916_e0_first_dyadic_common_left_block_span as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['shared_external_bits'] == 149
    assert out['local_left_external_bits'] == 11
    assert out['local_quadratic_ambient_bits'] == 55
    assert out['shared_local_bilinear_ambient_bits'] == 1639

    assert out['singleton_anchor'] == {
        'terms': 103,
        'local_quadratic_span_rank': 7,
        'local_linear_span_rank': 9,
        'local_polynomial_span_rank': 16,
        'cross_matrix_coefficient_span_rank': 86,
        'joint_shared_to_local_frequency_control_rank': 45,
        'per_term_cross_rank_histogram': {10: 7, 11: 96},
    }
    assert out['pair_anchor'] == {
        'terms': 237,
        'local_quadratic_span_rank': 11,
        'local_linear_span_rank': 11,
        'local_polynomial_span_rank': 23,
        'cross_matrix_coefficient_span_rank': 169,
        'joint_shared_to_local_frequency_control_rank': 144,
        'per_term_cross_rank_histogram': {10: 1, 11: 236},
    }
    assert out['all_340_anchor_phases'] == {
        'terms': 340,
        'local_quadratic_span_rank': 11,
        'local_linear_span_rank': 11,
        'local_polynomial_span_rank': 23,
        'cross_matrix_coefficient_span_rank': 237,
        'joint_shared_to_local_frequency_control_rank': 145,
        'per_term_cross_rank_histogram': {10: 8, 11: 332},
    }
    assert out['pair_difference'] == {
        'terms': 237,
        'local_quadratic_span_rank': 9,
        'local_linear_span_rank': 11,
        'local_polynomial_span_rank': 21,
        'cross_matrix_coefficient_span_rank': 98,
        'joint_shared_to_local_frequency_control_rank': 87,
        'per_term_cross_rank_histogram': {1: 46, 2: 88, 3: 73, 4: 24, 5: 6},
    }
    assert out['pair_anchor_by_multiplicity'] == {
        2: {
            'terms': 57,
            'local_quadratic_span_rank': 9,
            'local_linear_span_rank': 10,
            'local_polynomial_span_rank': 19,
            'cross_matrix_coefficient_span_rank': 54,
            'joint_shared_to_local_frequency_control_rank': 53,
            'per_term_cross_rank_histogram': {10: 1, 11: 56},
        },
        4: {
            'terms': 180,
            'local_quadratic_span_rank': 10,
            'local_linear_span_rank': 11,
            'local_polynomial_span_rank': 22,
            'cross_matrix_coefficient_span_rank': 117,
            'joint_shared_to_local_frequency_control_rank': 118,
            'per_term_cross_rank_histogram': {11: 180},
        },
    }
    assert out['pair_difference_by_multiplicity'] == {
        2: {
            'terms': 57,
            'local_quadratic_span_rank': 6,
            'local_linear_span_rank': 7,
            'local_polynomial_span_rank': 14,
            'cross_matrix_coefficient_span_rank': 50,
            'joint_shared_to_local_frequency_control_rank': 40,
            'per_term_cross_rank_histogram': {1: 6, 2: 11, 3: 26, 4: 8, 5: 6},
        },
        4: {
            'terms': 180,
            'local_quadratic_span_rank': 6,
            'local_linear_span_rank': 11,
            'local_polynomial_span_rank': 18,
            'cross_matrix_coefficient_span_rank': 52,
            'joint_shared_to_local_frequency_control_rank': 58,
            'per_term_cross_rank_histogram': {1: 40, 2: 77, 3: 47, 4: 16},
        },
    }
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_COMMON_LEFT_BLOCK_SPAN_RESULT')
    print('decision=COMMON_LEFT_QUADRATIC_SPAN_11_SHARED_CONTROL_145')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
