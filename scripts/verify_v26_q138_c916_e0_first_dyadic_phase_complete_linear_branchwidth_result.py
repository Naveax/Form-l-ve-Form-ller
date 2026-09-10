#!/usr/bin/env python3
import io
from contextlib import redirect_stdout
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_phase_complete_linear_branchwidth as P

PAIR_HIST = {142: 5, 143: 194, 144: 2359, 145: 7774, 146: 6117, 147: 11195, 148: 3110, 149: 371}
KERNEL_DIM_HIST = {2: 16, 3: 12, 4: 72, 5: 60, 6: 16, 7: 74}
COVERAGE_HIST = {1: 2016, 2: 720, 3: 216, 4: 80, 5: 112, 6: 112, 7: 40, 8: 40, 9: 84, 10: 40, 11: 20, 12: 32, 13: 5, 14: 20, 15: 4, 16: 5, 18: 1, 19: 1, 26: 1, 27: 1, 29: 1, 30: 1, 58: 8, 60: 8, 66: 8, 69: 1, 74: 1, 76: 1, 79: 1, 80: 9, 82: 2, 84: 2, 85: 4, 88: 2, 100: 1, 181: 1, 182: 1, 195: 1, 199: 1, 200: 1, 216: 1, 217: 1}


def main():
    with redirect_stdout(io.StringIO()):
        out = P.analyze()
    assert out['physical_shared_dimension'] == 149
    assert out['support_groups'] == 250
    assert out['global_minimal_union_rank'] == 149
    assert out['minimal_rank_histogram'] == {142: 74, 143: 16, 144: 60, 145: 72, 146: 12, 147: 16}
    assert out['kernel_dimension_histogram'] == KERNEL_DIM_HIST
    assert out['pair_count'] == 31125
    assert out['pair_union_rank_histogram'] == PAIR_HIST
    assert out['nonfull_pair_count'] == 30754
    assert out['max_pair_kernel_intersection_dimension'] == 7
    assert out['unique_nonzero_kernel_directions'] == 3607
    assert out['kernel_direction_coverage_histogram'] == COVERAGE_HIST
    assert out['max_nonzero_kernel_direction_coverage'] == 217
    assert out['max_coverage_direction_count'] == 1
    assert out['max_coverage_direction_digest'] == '4a6fb6925a8f5418ab88'
    assert len(out['max_coverage_example_groups']) == 217
    assert out['max_nonfull_group_subset_size'] == 217
    assert out['all_subsets_of_size_at_least'] == 218
    assert out['all_such_subsets_span_full_149'] is True
    assert out['balanced_edge_min_side_for_250_leaf_subcubic_tree'] == 84
    assert out['phase_complete_linear_branchwidth_exact'] is False
    assert out['phase_complete_linear_branchwidth'] is None
    assert out['decision'] == 'PHASE_COMPLETE_LINEAR_BRANCHWIDTH_DUAL_COVERAGE_INCONCLUSIVE'
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHASE_COMPLETE_LINEAR_BRANCHWIDTH_RESULT')
    print('pair_union_rank_histogram=' + str(PAIR_HIST))
    print('max_nonfull_group_subset_size=217 saturation_threshold=218')
    print('max_coverage_direction_digest=4a6fb6925a8f5418ab88')
    print('branchwidth_status=inconclusive_from_balanced-edge bound; exact phase-complete linear branchwidth remains in [147,149]')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
