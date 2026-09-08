#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_pair_residual as P


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['raw_e0_sectors'] == 577
    assert out['support_groups'] == 250
    assert out['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert out['even_multiplicity_support_groups'] == 147
    assert out['first_dyadic_pair_residual_terms'] == 237
    assert out['multi_support_free_dimension_histogram'] == {150: 145, 151: 2}

    assert out['selected_difference_polar_rank_histogram'] == {2: 237}
    assert out['selected_affine_nonconstant_difference_pairs'] == 0
    assert out['selected_genuinely_quadratic_difference_pairs'] == 237
    assert out['max_selected_difference_polar_rank'] == 2

    assert out['multiplicity2_difference_polar_rank_histogram'] == {2: 57}
    assert out['multiplicity4_all_matching_candidate_polar_rank_histogram'] == {2: 360, 4: 180}
    assert out['multiplicity4_matching_choice_histogram'] == {0: 90}
    assert out['multiplicity4_selected_difference_polar_rank_histogram'] == {2: 180}
    assert out['multiplicity4_selected_max_difference_polar_rank_histogram'] == {2: 90}

    assert len(out['groups']) == 147
    for g in out['groups']:
        assert g['multiplicity'] in (2, 4)
        assert g['matching_index'] == 0
        assert g['selected_max_difference_polar_rank'] == 2
        assert len(g['selected_pairs']) == g['multiplicity'] // 2
        for pair in g['selected_pairs']:
            assert pair['difference_polar_rank'] == 2
            assert pair['difference_is_affine_nonconstant'] is False

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PAIR_RESIDUAL_RESULT')
    print('exact=237/237 selected pair equality conditions have restricted polar rank exactly 2')
    print('candidate_m4_polar_ranks=rank2:360,rank4:180; selected_matching0_groups=90')
    print('decision=RANK2_QUADRATIC_PAIR_EQUALITY_LAYER')
    print('important=this is exact restricted-support geometry, not yet a 149-bit separator-width certificate')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
