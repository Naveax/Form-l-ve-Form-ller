#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_gauss_radical_control as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['raw_e0_sectors'] == 577
    assert out['support_groups'] == 250
    assert out['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}

    assert out['sector_local_fiber_dimension_histogram'] == {7: 127, 8: 309, 9: 141}
    assert out['sector_local_fiber_polar_rank_histogram'] == {4: 209, 6: 329, 8: 39}
    assert out['sector_local_fiber_radical_dimension_histogram'] == {
        0: 3, 1: 88, 2: 172, 3: 180, 4: 134,
    }
    assert out['sector_shared_projection_radical_control_rank_histogram'] == {
        0: 3, 1: 88, 2: 172, 3: 180, 4: 134,
    }
    assert (
        out['sector_shared_projection_radical_control_rank_histogram']
        == out['sector_local_fiber_radical_dimension_histogram']
    )

    assert out['group_shared_projection_radical_control_rank_histogram'] == {
        1: 29, 2: 46, 3: 68, 4: 20, 5: 48, 6: 39,
    }
    assert out['group_radical_control_rank_by_multiplicity'] == {
        1: {1: 26, 2: 45, 3: 28, 4: 4},
        2: {1: 3, 2: 1, 3: 39, 4: 12, 5: 2},
        4: {3: 1, 4: 4, 5: 46, 6: 39},
    }
    assert out['sector_radical_control_rank_by_multiplicity'] == {
        1: {1: 26, 2: 45, 3: 28, 4: 4},
        2: {1: 14, 2: 72, 3: 16, 4: 12},
        4: {0: 3, 1: 48, 2: 55, 3: 136, 4: 118},
    }
    assert (
        out['sector_radical_control_rank_by_multiplicity']
        == out['sector_radical_dimension_by_multiplicity']
    )

    assert out['sectors_with_zero_shared_radical_control'] == 3
    assert out['sum_sector_radical_control_ranks'] == 1508
    assert out['max_sector_radical_control_rank'] == 4
    assert out['max_group_radical_control_rank'] == 6

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_GAUSS_RADICAL_CONTROL_RESULT')
    print('sector_radical_control_rank_equals_radical_dimension=1')
    print('max_sector_radical_control_rank=4')
    print('max_group_radical_control_rank=6')
    print('group_control_hist={1:29,2:46,3:68,4:20,5:48,6:39}')
    print('decision=GAUSS_RADICAL_CONTROL_MAX6_PER_SUPPORT_GROUP')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
