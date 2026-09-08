#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_complete_first_dyadic_group_residual as P


def main():
    out = P.analyze()

    assert out['position'] == 'C'
    assert out['raw_e0_sectors'] == 577
    assert out['support_groups'] == 250
    assert out['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert out['first_dyadic_group_residual_formula'] == '(sum_i (-1)^q_i - (m mod 2))/2'
    assert out['residual_terms_by_multiplicity'] == {1: 103, 2: 57, 4: 180}
    assert out['group_residual_term_count_histogram'] == {1: 160, 2: 90}
    assert out['total_first_dyadic_residual_terms'] == 340

    assert out['singleton_phase_polar_rank_histogram'] == {142: 74, 144: 29}
    assert out['singleton_support_free_dimension_histogram'] == {150: 103}

    assert out['pair_selected_difference_polar_rank_histogram'] == {2: 237}
    assert out['pair_max_selected_difference_polar_rank'] == 2
    assert out['pair_affine_nonconstant_difference_terms'] == 0
    assert out['pair_genuinely_quadratic_difference_terms'] == 237

    assert len(out['groups']) == 250
    singletons = [g for g in out['groups'] if g['multiplicity'] == 1]
    pairs2 = [g for g in out['groups'] if g['multiplicity'] == 2]
    groups4 = [g for g in out['groups'] if g['multiplicity'] == 4]
    assert (len(singletons), len(pairs2), len(groups4)) == (103, 57, 90)
    assert all(g['residual_terms'] == 1 for g in singletons + pairs2)
    assert all(g['residual_terms'] == 2 for g in groups4)
    assert all(g['singleton_phase_polar_rank'] in (142, 144) for g in singletons)
    assert all(g['selected_max_difference_polar_rank'] == 2 for g in pairs2 + groups4)

    print('PASS V26_Q138_C916_E0_COMPLETE_FIRST_DYADIC_GROUP_RESIDUAL_RESULT')
    print('exact=340 terms: singleton103 + multiplicity2-pair57 + multiplicity4-pair180')
    print('singleton_common_support_polar_rank=142:74,144:29; pair_difference_polar_rank=2:237')
    print('decision=TWO_REGIME_FIRST_DYADIC_RESIDUAL')
    print('important=exact arithmetic representation only; no separator-state width is claimed')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
