#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_phase_complete_width147_three_plane_cover as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['support_groups'] == 250
    assert out['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert out['minimal_rank_histogram'] == {142: 74, 143: 16, 144: 60, 145: 72, 146: 12, 147: 16}
    assert out['rank147_groups'] == [5, 8, 24, 62, 113, 154, 155, 156, 158, 179, 182, 186, 234, 239, 241, 244]
    assert out['forced_rank147_plane_count'] == 5
    assert out['forced_rank147_plane_digests'] == [
        '35078c9c78e4ea8a77dd',
        '648c2d0942437f963696',
        '3d38bd58df28dcc428a3',
        '3fddb3d36da3e8c82c5f',
        '6cd96f38e42b56e8ff91',
    ]
    assert out['forced_rank147_plane_coverages'] == [191, 10, 7, 73, 8]
    assert out['three_plane_cover_exists'] is False
    assert out['minimum_common_2d_cover_size_at_most_3'] is None
    assert out['certified_tree'] is None
    assert out['lower_bound_witness_group'] == 5
    assert out['lower_bound_witness_group_rank'] == 147
    assert out['lower_bound_witness_complement_rank'] == 149
    assert out['lower_bound_lambda'] == 147
    assert out['phase_complete_linear_branchwidth_lower_bound'] == 147
    assert out['phase_complete_linear_branchwidth_upper_bound'] == 148
    assert out['decision'] == 'THREE_COMMON_2D_KERNEL_COVER_IMPOSSIBLE_WIDTH147_OPEN'
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PHASE_COMPLETE_WIDTH147_THREE_PLANE_COVER_RESULT')
    print('forced_rank147_plane_count=5')
    print('forced_plane_coverages=191,10,7,73,8')
    print('three_plane_cover_exists=false')
    print('decision=THREE_COMMON_2D_KERNEL_COVER_IMPOSSIBLE_WIDTH147_OPEN')
    print('important=this closes only the <=3 common-2D-kernel cover construction, not width147 in general')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
