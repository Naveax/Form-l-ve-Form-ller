#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_complete_first_dyadic_fiber_geometry as P


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['support_groups'] == 250
    assert out['total_first_dyadic_terms'] == 340
    assert out['singleton_terms'] == 103
    assert out['pair_terms'] == 237

    assert out['shared_projection_rank_histogram_by_multiplicity'] == {
        1: {141: 1, 142: 49, 143: 53},
        2: {141: 2, 142: 42, 143: 13},
        4: {141: 32, 142: 46, 143: 12},
    }
    assert out['local_fiber_dimension_histogram_by_multiplicity'] == {
        1: {7: 53, 8: 49, 9: 1},
        2: {7: 13, 8: 42, 9: 2},
        4: {7: 12, 8: 44, 9: 34},
    }

    assert out['singleton_polar_rank_histogram'] == {142: 74, 144: 29}
    assert out['singleton_local_to_all_polar_rank_histogram'] == {7: 53, 8: 49, 9: 1}
    assert out['singleton_local_local_polar_rank_histogram'] == {4: 31, 6: 72}
    assert out['singleton_local_linear_rank_histogram'] == {1: 103}
    assert out['singleton_fiber_category_histogram'] == {'local_quadratic': 103}
    assert out['singleton_descends_to_shared_quotient'] == 0

    assert out['pair_local_to_all_polar_rank_histogram'] == {1: 105, 2: 132}
    assert out['pair_local_local_polar_rank_histogram'] == {0: 105, 2: 132}
    assert out['pair_local_linear_rank_histogram'] == {0: 6, 1: 231}
    assert out['pair_fiber_category_histogram'] == {
        'local_quadratic': 132,
        'shared_local_bilinear': 105,
    }
    assert out['pair_fiber_category_by_multiplicity'] == {
        2: {'local_quadratic': 42, 'shared_local_bilinear': 15},
        4: {'local_quadratic': 90, 'shared_local_bilinear': 90},
    }
    assert out['pair_descends_to_shared_quotient'] == 0

    print('PASS V26_Q138_C916_E0_COMPLETE_FIRST_DYADIC_FIBER_GEOMETRY_RESULT')
    print('exact=all 103 singleton terms are local-quadratic on the support fiber')
    print('exact=237 pair terms split as local-quadratic132 + shared-local-bilinear105')
    print('exact=no singleton or selected pair term descends to the 149-bit shared quotient')
    print('decision=FIRST_DYADIC_CARRY_IS_FIBER_COUPLED')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
