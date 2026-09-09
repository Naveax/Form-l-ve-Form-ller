#!/usr/bin/env python3
import io
from contextlib import redirect_stdout
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_pair_value_image_census as C

EXPECTED_RELATION_HIST = {
    'disjoint': 28,
    'equal': 6,
    'left_subset_right': 4,
    'overlap_incomparable': 112,
    'right_subset_left': 87,
}
EXPECTED_AMPLITUDE_DELTA_HIST = {0: 132, 1: 105}
EXPECTED_DIFFERENCE_TYPE_HIST = {
    'affine_nonconstant': 201,
    'constant': 2,
    'quadratic_nonconstant': 6,
}
EXPECTED_DIFFERENCE_RANK_HIST = {0: 203, 2: 6}

EXPECTED_IMAGE_SIZE_HIST = {3: 20, 5: 217}
EXPECTED_STATE_BITS_HIST = {2: 20, 3: 217}
EXPECTED_NONZERO_VALUE_COUNT_HIST = {2: 20, 4: 217}
EXPECTED_MIN_V2_HIST = {3: 21, 4: 139, 5: 77}
EXPECTED_NORMALIZED_ALPHABET_HIST = {
    '[-1, 0, 1]': 20,
    '[-2, -1, 0, 1, 2]': 126,
    '[-3, -1, 0, 1, 3]': 91,
}
EXPECTED_IMAGE_BY_MULTIPLICITY = {
    2: {3: 6, 5: 51},
    4: {3: 14, 5: 166},
}
EXPECTED_STATE_BY_MULTIPLICITY = {
    2: {2: 6, 3: 51},
    4: {2: 14, 3: 166},
}
EXPECTED_IMAGE_BY_RELATION = {
    'disjoint': {3: 14, 5: 14},
    'equal': {3: 6},
    'left_subset_right': {5: 4},
    'overlap_incomparable': {5: 112},
    'right_subset_left': {5: 87},
}
EXPECTED_IMAGE_BY_DELTA = {
    0: {3: 20, 5: 112},
    1: {5: 105},
}


def verify():
    with redirect_stdout(io.StringIO()):
        got = C.analyze()

    assert got['position'] == 'C'
    assert got['physical_shared_dimension'] == 149
    assert got['synthetic_census_regression_cases'] == 2304
    assert got['raw_e0_sectors'] == 577
    assert got['support_groups'] == 250
    assert got['group_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert got['even_multiplicity_support_groups'] == 147
    assert got['frozen_transformed_pairs'] == 237

    assert got['reproduced_support_relation_histogram'] == EXPECTED_RELATION_HIST
    assert got['reproduced_amplitude_delta_histogram'] == EXPECTED_AMPLITUDE_DELTA_HIST
    assert got['reproduced_sign_difference_type_histogram'] == EXPECTED_DIFFERENCE_TYPE_HIST
    assert got['reproduced_sign_difference_polar_rank_histogram'] == EXPECTED_DIFFERENCE_RANK_HIST

    assert got['pair_value_image_size_histogram'] == EXPECTED_IMAGE_SIZE_HIST
    assert got['pair_value_state_bits_histogram'] == EXPECTED_STATE_BITS_HIST
    assert got['pair_nonzero_value_count_histogram'] == EXPECTED_NONZERO_VALUE_COUNT_HIST
    assert got['pair_minimum_nonzero_valuation_histogram'] == EXPECTED_MIN_V2_HIST
    assert got['pair_normalized_alphabet_histogram'] == EXPECTED_NORMALIZED_ALPHABET_HIST
    assert got['pair_alphabet_sign_symmetry_histogram'] == {'true': 237}
    assert got['pair_multiplicity_sign_symmetry_histogram'] == {'true': 237}

    assert got['image_size_by_group_multiplicity'] == EXPECTED_IMAGE_BY_MULTIPLICITY
    assert got['state_bits_by_group_multiplicity'] == EXPECTED_STATE_BY_MULTIPLICITY
    assert got['image_size_by_support_relation'] == EXPECTED_IMAGE_BY_RELATION
    assert got['image_size_by_amplitude_delta'] == EXPECTED_IMAGE_BY_DELTA
    assert got['maximum_pair_image_size'] == 5
    assert got['maximum_pair_state_bits'] == 3
    assert got['decision'] == 'FROZEN_PAIR_EXACT_NONLINEAR_VALUE_IMAGE_CENSUS_COMPLETE'

    pairs = [p for g in got['groups'] for p in g['pairs']]
    assert len(got['groups']) == 147
    assert len(pairs) == 237
    domain = 1 << 149
    for p in pairs:
        counts = {r['value']: r['multiplicity'] for r in p['value_multiplicity']}
        assert sum(counts.values()) == domain
        assert len(counts) == p['image_size']
        assert p['image_size'] in (3, 5)
        assert p['state_bits'] == (p['image_size'] - 1).bit_length()
        assert p['state_bits'] in (2, 3)
        assert p['nonzero_value_count'] == p['image_size'] - 1
        assert 0 in counts
        assert p['alphabet_sign_symmetric'] is True
        assert p['multiplicity_sign_symmetric'] is True
        assert all(-v in counts for v in counts)
        assert all(counts[v] == counts[-v] for v in counts)

    print('PASS VERIFY_V26_Q138_C916_E0_FIRST_DYADIC_PAIR_VALUE_IMAGE_CENSUS_RESULT')
    print('decision=FROZEN_PAIR_EXACT_NONLINEAR_VALUE_IMAGE_CENSUS_COMPLETE')
    print('pair_image_size_histogram={3:20,5:217}')
    print('pair_state_bits_histogram={2:20,3:217}')
    print('pair_normalized_alphabets=20*[-1,0,1]+126*[-2,-1,0,1,2]+91*[-3,-1,0,1,3]')
    print('maximum_pair_image_size=5')
    print('maximum_pair_state_bits=3')
    print('important=pair-local exact nonlinear state is not a global separator width')
    print('ALPHA_PASS=0')
    return got


if __name__ == '__main__':
    verify()
