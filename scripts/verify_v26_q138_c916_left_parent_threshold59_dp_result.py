#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_left_parent_threshold59_dp as P


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['order'] == 'multiplicity_then_function'
    assert out['target_bits'] == 59
    assert out['parent_exists_in_baseline_tree'] is True

    p = out['parent']
    assert (p['lo'], p['hi'], p['size']) == (0, 166, 166)
    assert p['safe_evaluation_bits'] == 40
    assert p['generic_safe_evaluation_bits'] == 40
    assert p['function_lambda'] == 44
    assert p['quadratic_residual_dim'] == 6
    assert p['fiber_affine_residual'] is True
    assert p['exact_override'] is False
    assert p['digest'] == '9e28f443b9a32e2e'

    assert out['direct_root_splits_le_59'] == 29
    assert out['threshold59_feasible'] is False
    assert out['witness'] is None
    assert out['witness_root_split'] is None
    assert out['witness_max_depth'] is None
    assert out['witness_edge_count'] == 0
    assert out['witness_max_safe_bits'] is None
    assert out['worst_witness_edges'] == []
    assert out['interval_costs_evaluated'] == 6270
    assert out['feasibility_states_cached'] == 291
    assert out['oracle_cache_entries'] == 6270

    print('PASS V26_Q138_C916_LEFT_PARENT_THRESHOLD59_DP_RESULT')
    print('exact=[0,166) parent costs 40 and has 29 direct splits with both children <=59')
    print('exact=no complete fixed-order contiguous binary tree exists with every non-root descendant <=59')
    print('decision=THRESHOLD59_FIXED_ORDER_CONTIGUOUS_NO_GO')
    print('next=compute exact minimax width on [0,166); current complete displayed tree supplies a width60 upper bound')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
