#!/usr/bin/env python3
import io
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_even_group_value_image_census as C

EXPECTED_SUPPORT_MULTIPLICITY = {1: 103, 2: 57, 4: 90}
EXPECTED_IMAGE_SIZE_HIST = {3: 6, 5: 51, 7: 88, 9: 2}
EXPECTED_STATE_BITS_HIST = {2: 6, 3: 139, 4: 2}
EXPECTED_NONZERO_VALUE_COUNT_HIST = {2: 6, 4: 51, 6: 88, 8: 2}
EXPECTED_MIN_V2_HIST = {3: 21, 4: 123, 5: 3}
EXPECTED_NORMALIZED_ALPHABET_HIST = {
    '[-1, 0, 1]': 6,
    '[-2, -1, 0, 1, 2]': 37,
    '[-3, -1, 0, 1, 3]': 14,
    '[-3, -2, -1, 0, 1, 2, 3]': 12,
    '[-4, -3, -2, -1, 0, 1, 2, 3, 4]': 2,
    '[-5, -3, -1, 0, 1, 3, 5]': 76,
}
EXPECTED_IMAGE_BY_MULTIPLICITY = {
    2: {3: 6, 5: 51},
    4: {7: 88, 9: 2},
}
EXPECTED_STATE_BY_MULTIPLICITY = {
    2: {2: 6, 3: 51},
    4: {3: 88, 4: 2},
}
EXPECTED_NONZERO_BY_MULTIPLICITY = {
    2: {2: 6, 4: 51},
    4: {6: 88, 8: 2},
}
EXPECTED_MIN_V2_BY_MULTIPLICITY = {
    2: {3: 6, 4: 48, 5: 3},
    4: {3: 15, 4: 75},
}
EXPECTED_MEMBERSHIP_BY_MULTIPLICITY = {
    2: {2: 4, 3: 18, 4: 35},
    4: {3: 1, 5: 12, 7: 75, 8: 1, 10: 1},
}
EXPECTED_MEMBERSHIP_CELL_HIST = {2: 4, 3: 19, 4: 35, 5: 12, 7: 75, 8: 1, 10: 1}
EXPECTED_CHARACTER_MOMENT_HIST = {7: 4, 8: 18, 9: 35, 38: 1, 48: 12, 56: 75, 63: 1, 66: 1}


def verify():
    with redirect_stdout(io.StringIO()):
        got = C.analyze()

    assert got['position'] == 'C'
    assert got['physical_shared_dimension'] == 149
    assert got['synthetic_group_regression_cases'] == 650
    assert got['synthetic_group_regression_by_transform_count'] == {2: 25, 4: 625}
    assert got['raw_e0_sectors'] == 577
    assert got['support_groups'] == 250
    assert got['support_multiplicity_histogram'] == EXPECTED_SUPPORT_MULTIPLICITY
    assert got['singleton_groups_deferred'] == 103
    assert got['even_multiplicity_groups'] == 147
    assert got['multiplicity2_pair_census_crosschecks'] == 57
    assert got['multiplicity4_pairing_partition_checks'] == 90

    assert got['even_group_value_image_size_histogram'] == EXPECTED_IMAGE_SIZE_HIST
    assert got['even_group_value_state_bits_histogram'] == EXPECTED_STATE_BITS_HIST
    assert got['even_group_nonzero_value_count_histogram'] == EXPECTED_NONZERO_VALUE_COUNT_HIST
    assert got['even_group_minimum_nonzero_valuation_histogram'] == EXPECTED_MIN_V2_HIST
    assert got['even_group_normalized_alphabet_histogram'] == EXPECTED_NORMALIZED_ALPHABET_HIST
    assert got['even_group_alphabet_sign_symmetry_histogram'] == {'true': 147}
    assert got['even_group_multiplicity_sign_symmetry_histogram'] == {'true': 147}

    assert got['realized_exact_membership_cell_histogram'] == EXPECTED_MEMBERSHIP_CELL_HIST
    assert got['cached_character_moment_count_histogram'] == EXPECTED_CHARACTER_MOMENT_HIST
    assert got['image_size_by_group_multiplicity'] == EXPECTED_IMAGE_BY_MULTIPLICITY
    assert got['state_bits_by_group_multiplicity'] == EXPECTED_STATE_BY_MULTIPLICITY
    assert got['nonzero_value_count_by_group_multiplicity'] == EXPECTED_NONZERO_BY_MULTIPLICITY
    assert got['minimum_nonzero_valuation_by_group_multiplicity'] == EXPECTED_MIN_V2_BY_MULTIPLICITY
    assert got['membership_cells_by_group_multiplicity'] == EXPECTED_MEMBERSHIP_BY_MULTIPLICITY
    assert got['maximum_even_group_image_size'] == 9
    assert got['maximum_even_group_state_bits'] == 4
    assert got['decision'] == 'EVEN_MULTIPLICITY_GROUP_EXACT_NONLINEAR_VALUE_IMAGE_CENSUS_COMPLETE'

    groups = got['groups']
    assert len(groups) == 147
    assert len({g['group_id'] for g in groups}) == 147
    assert Counter(g['multiplicity'] for g in groups) == Counter({2: 57, 4: 90})

    domain = 1 << 149
    for g in groups:
        m = g['multiplicity']
        assert m in (2, 4)
        assert g['transform_count'] == m
        counts = {r['value']: r['multiplicity'] for r in g['value_multiplicity']}
        assert sum(counts.values()) == domain
        assert len(counts) == g['image_size']
        assert 0 in counts
        assert g['state_bits'] == (g['image_size'] - 1).bit_length()
        assert g['nonzero_value_count'] == g['image_size'] - 1
        assert g['alphabet_sign_symmetric'] is True
        assert g['multiplicity_sign_symmetric'] is True
        assert all(-v in counts for v in counts)
        assert all(counts[v] == counts[-v] for v in counts)

        nonzero = [v for v in counts if v]
        assert nonzero
        min_v2 = min(C.P.v2_nonzero(v) for v in nonzero)
        assert min_v2 == g['minimum_nonzero_valuation']
        normalized = sorted(v >> min_v2 for v in counts)
        assert normalized == g['normalized_alphabet']

        selected = [tuple(pair) for pair in g['selected_pairs']]
        assert sorted(i for pair in selected for i in pair) == list(range(m))
        if m == 2:
            assert selected == [(0, 1)]
            assert g['image_size'] in (3, 5)
            assert g['state_bits'] in (2, 3)
        else:
            assert len(selected) == 2
            assert g['image_size'] in (7, 9)
            assert g['state_bits'] in (3, 4)

    print('PASS VERIFY_V26_Q138_C916_E0_FIRST_DYADIC_EVEN_GROUP_VALUE_IMAGE_CENSUS_RESULT')
    print('decision=EVEN_MULTIPLICITY_GROUP_EXACT_NONLINEAR_VALUE_IMAGE_CENSUS_COMPLETE')
    print('support_multiplicity_histogram={1:103,2:57,4:90}')
    print('singleton_groups_deferred=103')
    print('even_group_image_size_histogram={3:6,5:51,7:88,9:2}')
    print('even_group_state_bits_histogram={2:6,3:139,4:2}')
    print('even_group_minimum_nonzero_valuation_histogram={3:21,4:123,5:3}')
    print('multiplicity2_pair_census_crosschecks=57')
    print('multiplicity4_pairing_partition_checks=90')
    print('synthetic_group_regression_cases=650')
    print('maximum_even_group_image_size=9')
    print('maximum_even_group_state_bits=4')
    print('important=group-local exact nonlinear state is not a joint separator width across the 147 groups')
    print('next=define and measure the 103 singleton signed-unit 2-adic lift before any all-250-group joint state analysis')
    print('ALPHA_PASS=0')
    return got


if __name__ == '__main__':
    verify()
