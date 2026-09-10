#!/usr/bin/env python3
import io
from contextlib import redirect_stdout
from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_group_output_minimal_linear_factorization_exact_overlap as P

EXPECTED_RANK_HIST = {142: 74, 143: 16, 144: 60, 145: 72, 146: 12, 147: 16}
EXPECTED_BY_MULT = {
    1: {142: 74, 144: 29},
    2: {143: 16, 144: 29, 145: 12},
    4: {144: 2, 145: 60, 146: 12, 147: 16},
}
EXPECTED_DELTA_HIST = {
    121: 60, 122: 10, 123: 29, 124: 4, 126: 2, 127: 34,
    128: 51, 129: 29, 130: 18, 131: 9, 132: 3, 133: 1,
}


def main():
    with redirect_stdout(io.StringIO()):
        out = P.analyze()

    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['support_groups'] == 250
    assert out['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert out['physical_term_count'] == 680
    assert out['synthetic_exact_fourier_transform_regression'] == {'terms': 28, 'frequencies': 896}
    assert out['base_unique_support_exact_groups'] == 140
    assert out['exact_overlap_closed_groups'] == 110
    assert out['exact_groups'] == 250
    assert out['unresolved_groups'] == 0
    assert out['lower_rank_histogram'] == EXPECTED_RANK_HIST
    assert out['upper_rank_histogram'] == EXPECTED_RANK_HIST
    assert out['exact_minimal_rank_histogram'] == EXPECTED_RANK_HIST
    assert out['exact_rank_by_multiplicity'] == EXPECTED_BY_MULT
    assert out['minimal_rank_minus_refined_rank_histogram'] == EXPECTED_DELTA_HIST
    assert out['closure_method_histogram'] == {
        'exact_overlap_walsh': 110,
        'unique_term_support': 140,
    }
    assert out['exact_overlap_totals'] == {
        'evaluations': 4245,
        'zero_evaluations': 2410,
        'nonzero_evaluations': 1835,
        'source_rank_increase': {
            'support_basis_single': 547,
            'support_hash': 1192,
            'support_origin': 96,
        },
    }
    assert out['decision'] == 'EXACT_MINIMAL_LINEAR_FACTORIZATION_RANKS_CLOSED_FOR_250_GROUPS'

    groups = out['groups']
    assert len(groups) == 250
    assert all(g['exact'] for g in groups)
    assert Counter(g['minimal_rank'] for g in groups) == Counter(EXPECTED_RANK_HIST)
    assert all(g['minimal_rank'] == g['lower_rank'] == g['upper_rank'] for g in groups)

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_GROUP_OUTPUT_MINIMAL_LINEAR_FACTORIZATION_RESULT')
    print('exact_groups=250 unresolved_groups=0')
    print('minimal_rank_histogram=' + str(EXPECTED_RANK_HIST))
    print('base_unique_support_exact_groups=140 exact_overlap_closed_groups=110')
    print('decision=EXACT_MINIMAL_LINEAR_FACTORIZATION_RANKS_CLOSED_FOR_250_GROUPS')
    print('theorem=each reported row space is the exact minimal GF2 linear factorization space of the corresponding exact integer-valued group residual function')
    print('important=local exact ranks 142..147 nearly saturate the 149-bit physical domain; this is not yet a global separator-width or nonlinear-compression theorem')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
