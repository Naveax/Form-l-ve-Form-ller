#!/usr/bin/env python3
import probe_v26_q138_c916_e0_first_dyadic_signed_pair_anchor_geometry as P


def main():
    out = P.analyze()
    assert out['position'] == 'C'
    assert out['signed_pair_terms'] == 237
    assert out['multi_support_groups'] == 147
    assert out['anchor_polar_rank_histogram'] == {142: 163, 144: 74}
    assert out['anchor_polar_rank_by_multiplicity'] == {
        2: {142: 33, 144: 24},
        4: {142: 130, 144: 50},
    }
    assert out['anchor_polar_rank_by_pair_slot'] == {
        '2:0': {142: 33, 144: 24},
        '4:0': {142: 65, 144: 25},
        '4:1': {142: 65, 144: 25},
    }
    assert out['anchor_local_to_all_polar_rank_histogram'] == {7: 37, 8: 130, 9: 70}
    assert out['anchor_local_local_polar_rank_histogram'] == {4: 60, 6: 138, 8: 39}
    assert out['anchor_local_linear_rank_histogram'] == {1: 237}
    assert out['anchor_fiber_category_histogram'] == {'local_quadratic': 237}
    assert out['anchor_fiber_category_by_multiplicity'] == {
        2: {'local_quadratic': 57},
        4: {'local_quadratic': 180},
    }
    assert out['difference_fiber_category_histogram'] == {
        'local_quadratic': 132,
        'shared_local_bilinear': 105,
    }
    assert out['anchor_difference_joint_category_histogram'] == {
        'local_quadratic|local_quadratic': 132,
        'local_quadratic|shared_local_bilinear': 105,
    }
    assert out['anchors_descending_to_shared_quotient'] == 0
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_SIGNED_PAIR_ANCHOR_GEOMETRY_RESULT')
    print('decision=SIGNED_PAIR_ANCHOR_IS_ALWAYS_LOCAL_QUADRATIC')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
