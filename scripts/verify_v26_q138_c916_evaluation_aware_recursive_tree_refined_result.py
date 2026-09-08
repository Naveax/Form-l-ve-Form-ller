#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_evaluation_aware_recursive_tree_refined as P


def main():
    got = P.analyze()
    assert got['position'] == 'C'
    assert got['support_groups'] == 250
    assert got['baseline_safe_evaluation_width'] == 65
    assert got['baseline_function_width'] == 70
    assert got['candidate_safe_widths'] == {
        'function_descending': 77,
        'function_then_multiplicity': 72,
        'linear_descending': 77,
        'linear_then_multiplicity': 72,
        'multiplicity_then_function': 65,
        'multiplicity_then_linear': 65,
    }
    assert got['candidate_function_widths'] == {
        'function_descending': 84,
        'function_then_multiplicity': 79,
        'linear_descending': 84,
        'linear_then_multiplicity': 79,
        'multiplicity_then_function': 70,
        'multiplicity_then_linear': 70,
    }
    assert got['best_order'] == 'multiplicity_then_function'
    assert got['best_safe_evaluation_width'] == 65
    assert got['best_function_width'] == 70
    assert got['best_depth'] == 11
    assert got['best_exact_override_edges'] == 3
    assert got['exact_override_meta'] == [
        {'name': 'former_width70', 'lo': 110, 'hi': 166, 'bits': 60, 'digest': 'ddddf643ea96032a'},
        {'name': 'width64_quadratic', 'lo': 55, 'hi': 110, 'bits': 60, 'digest': 'c72f29e8fe2266ec'},
        {'name': 'exact_width65', 'lo': 166, 'hi': 199, 'bits': 65, 'digest': '50a4b970f7f85916'},
    ]
    worst = got['best_worst_edges'][0]
    assert worst['digest'] == '50a4b970f7f85916'
    assert worst['lo'] == 166 and worst['hi'] == 199 and worst['size'] == 33
    assert worst['exact_override'] is True
    assert worst['function_lambda'] == 68
    assert worst['generic_safe_evaluation_bits'] == 65
    assert worst['safe_evaluation_bits'] == 65
    assert worst['quadratic_residual_dim'] == 5
    assert worst['fiber_affine_residual'] is True
    print('PASS V26_Q138_C916_EVALUATION_AWARE_RECURSIVE_TREE_REFINED_RESULT')
    print('verdict=NO_REFINED_EVALUATION_AWARE_TREE_GAIN')
    print('candidate_safe_widths=65,65,72,72,77,77')
    print('persistent_bottleneck=[166,199) digest=50a4b970f7f85916 safe_bits=65')
    print('next=scan every split of the bottleneck parent and perform local tree surgery instead of adding more global orders')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
