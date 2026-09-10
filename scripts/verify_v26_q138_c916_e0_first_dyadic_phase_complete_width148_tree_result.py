#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_phase_complete_width148_tree as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['support_groups'] == 250
    assert out['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert out['minimal_rank_histogram'] == {142: 74, 143: 16, 144: 60, 145: 72, 146: 12, 147: 16}
    assert out['dominant_direction_digest'] == '4a6fb6925a8f5418ab88'
    assert out['dominant_direction_coverage'] == 217
    assert out['exception_count'] == 33
    assert out['exception_cover_size'] == 2
    assert out['exception_cover_direction_digests'] == ['0913d6a8787377491d4d', 'd249413823c65dd43a21']
    assert out['exception_partition_sizes'] == [21, 12]
    assert out['lower_bound_witness_group'] == 5
    assert out['lower_bound_witness_group_rank'] == 147
    assert out['lower_bound_witness_complement_rank'] == 149
    assert out['lower_bound_lambda'] == 147
    cert = out['certified_tree']
    assert cert is not None
    assert cert['nodes'] == 499
    assert cert['edges_checked'] == 498
    assert cert['width'] == 148
    assert cert['bad_edges_over_148'] == []
    assert cert['edge_lambda_histogram'] == {142: 74, 143: 17, 144: 81, 145: 124, 146: 78, 147: 79, 148: 45}
    assert out['phase_complete_linear_branchwidth_lower_bound'] == 147
    assert out['phase_complete_linear_branchwidth_upper_bound'] == 148
    assert out['decision'] == 'PHASE_COMPLETE_LINEAR_BRANCHWIDTH_IN_147_148_WITH_WIDTH148_CERTIFICATE'
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHASE_COMPLETE_WIDTH148_TREE_RESULT')
    print('certified_width=148 lower_bound=147 edges_checked=498')
    print('exception_cover=2 partitions=21+12 dominant_coverage=217')
    print('decision=PHASE_COMPLETE_LINEAR_BRANCHWIDTH_IN_147_148_WITH_WIDTH148_CERTIFICATE')
    print('important=linear-factorization branchwidth only; nonlinear compression remains open')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
