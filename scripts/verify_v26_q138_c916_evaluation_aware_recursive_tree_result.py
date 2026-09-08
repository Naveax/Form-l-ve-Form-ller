#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_evaluation_aware_recursive_tree as P


def main():
    got = P.analyze()
    assert got['position'] == 'C'
    assert got['support_groups'] == 250
    assert got['baseline_function_tree_width'] == 70
    assert got['baseline_safe_evaluation_width'] == 65
    assert got['candidate_safe_widths'] == {
        'multiplicity_then_function': 65,
        'multiplicity_then_linear': 65,
    }
    assert got['candidate_function_widths'] == {
        'multiplicity_then_function': 70,
        'multiplicity_then_linear': 70,
    }
    assert got['best_order'] == 'multiplicity_then_function'
    assert got['best_safe_evaluation_width'] == 65
    assert got['best_function_width'] == 70
    assert got['best_depth'] == 10
    assert got['best_fiber_quadratic_edges'] == 126
    worst = got['best_worst_edges'][0]
    assert worst == {
        'lo': 166,
        'hi': 199,
        'size': 33,
        'safe_evaluation_bits': 65,
        'function_lambda': 68,
        'quadratic_residual_dim': 5,
        'fiber_affine_residual': True,
    }
    print('PASS V26_Q138_C916_EVALUATION_AWARE_RECURSIVE_TREE_RESULT')
    print('verdict=NO_GENERIC_EVALUATION_AWARE_TREE_GAIN')
    print('baseline_safe_width=65 candidate_safe_widths=65,65')
    print('persistent_bottleneck=[166,199) safe_bits=65 function_lambda=68')
    print('next=expand deterministic orders/splits and inject subset-stable exact edge refinements from merged certificates')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
