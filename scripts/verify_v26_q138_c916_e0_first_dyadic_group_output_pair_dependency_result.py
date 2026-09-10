#!/usr/bin/env python3
import io
from contextlib import redirect_stdout

import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as P


def main():
    buf = io.StringIO()
    with redirect_stdout(buf):
        out = P.analyze()

    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['synthetic_inner_product_regression_cases'] == 36
    assert out['raw_e0_sectors'] == 577
    assert out['support_groups'] == 250
    assert out['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert out['physical_term_count'] == 680
    assert out['singleton_baseline_term_count'] == 103

    assert out['all_unordered_group_pairs'] == 31125
    assert out['scale_signature_class_count'] == 19
    assert out['scale_signature_class_size_histogram'] == {
        1: 6, 2: 2, 4: 2, 6: 1, 8: 1, 11: 1,
        14: 1, 26: 1, 27: 1, 36: 1, 45: 1, 59: 1,
    }
    assert out['scale_compatible_candidate_pairs'] == 4210
    assert out['distribution_filter_rejected_pairs'] == 26915
    assert out['exact_distribution_equal_candidate_pairs'] == 4210
    assert out['exact_distribution_negated_candidate_pairs'] == 2538

    assert out['zero_inner_scale_compatible_candidate_pairs'] == 2536
    assert out['nonproportional_scale_compatible_candidate_pairs'] == 4210
    assert out['exact_scalar_proportional_pairs'] == 0
    assert out['exact_equal_function_pairs'] == 0
    assert out['exact_negated_function_pairs'] == 0
    assert out['exact_other_scaled_function_pairs'] == 0
    assert out['proportional_ratio_histogram'] == {}
    assert out['proportional_pair_multiplicity_histogram'] == {}
    assert out['proportional_projection_support_relation_histogram'] == {}
    assert out['proportional_pairs'] == []

    assert out['proportional_dependency_component_sizes_descending'] == [1] * 250
    assert out['proportional_dependency_component_size_histogram'] == {1: 250}
    assert out['term_inner_product_cache_entries'] == 40516
    assert out['norm_crosscheck_failures'] == []
    assert out['decision'] == 'NO_PAIRWISE_EXACT_SCALAR_DEPENDENCY_ACROSS_250_GROUP_OUTPUTS'

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_GROUP_OUTPUT_PAIR_DEPENDENCY_RESULT')
    print('all_group_pairs=31125 scale_compatible=4210 filtered=26915')
    print('same_exact_distribution_pairs=4210 zero_inner_pairs=2536')
    print('exact_scalar_proportional_pairs=0')
    print('dependency_components=250 singleton components')
    print('decision=NO_PAIRWISE_EXACT_SCALAR_DEPENDENCY_ACROSS_250_GROUP_OUTPUTS')
    print('important=this excludes pairwise scalar reuse only; higher-order linear and nonlinear joint dependencies remain unresolved')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
