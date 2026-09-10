#!/usr/bin/env python3
import io
from contextlib import redirect_stdout

import probe_v26_q138_c916_e0_first_dyadic_group_output_modp_rank_witness as P

EXPECTED_CHECKPOINTS = [
    {
        'stage': 'projection_origins',
        'stage_candidates_seen': 250,
        'stage_unique_candidates_evaluated': 127,
        'stage_rank_increases_by_prime': {'65521': 78, '1000003': 78},
        'rank_by_prime': {'65521': 78, '1000003': 78},
        'cumulative_unique_candidates_evaluated': 127,
    },
    {
        'stage': 'gauss_support_origins',
        'stage_candidates_seen': 577,
        'stage_unique_candidates_evaluated': 376,
        'stage_rank_increases_by_prime': {'65521': 166, '1000003': 166},
        'rank_by_prime': {'65521': 244, '1000003': 244},
        'cumulative_unique_candidates_evaluated': 503,
    },
    {
        'stage': 'projection_basis_single',
        'stage_candidates_seen': 2000,
        'stage_unique_candidates_evaluated': 851,
        'stage_rank_increases_by_prime': {'65521': 4, '1000003': 4},
        'rank_by_prime': {'65521': 248, '1000003': 248},
        'cumulative_unique_candidates_evaluated': 1354,
    },
    {
        'stage': 'gauss_basis_single',
        'stage_candidates_seen': 201,
        'stage_unique_candidates_evaluated': 114,
        'stage_rank_increases_by_prime': {'65521': 2, '1000003': 2},
        'rank_by_prime': {'65521': 250, '1000003': 250},
        'cumulative_unique_candidates_evaluated': 1468,
    },
]

EXPECTED_WITNESS_SHA256 = '154b789ef5b116ebae864169d9be793d4e03e1d35a1804b06f871d6b067e21fd'


def main():
    buf = io.StringIO()
    with redirect_stdout(buf):
        out = P.analyze()

    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['primes'] == [65521, 1000003]
    assert out['synthetic_rank_regression_cases'] == 14
    assert out['synthetic_affine_point_regression_cases'] == 4
    assert out['raw_e0_sectors'] == 577
    assert out['support_groups'] == 250
    assert out['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert out['physical_term_count'] == 680
    assert out['gauss_sector_term_count'] == 577
    assert out['singleton_baseline_term_count'] == 103

    assert out['unique_candidates_evaluated'] == 1468
    assert out['duplicate_candidates_skipped'] == 1560
    assert out['zero_evaluation_rows'] == 32
    assert out['rank_checkpoints'] == EXPECTED_CHECKPOINTS
    assert out['final_rank_by_prime'] == {'65521': 250, '1000003': 250}
    assert out['decision'] == 'MODP_FULL_RANK250_PHYSICAL_EVALUATION_WITNESS'

    witness = out['witness']
    assert witness is not None
    assert witness['prime'] == 65521
    assert witness['rank'] == 250
    assert witness['determinant_mod_prime'] == 27993
    assert witness['selected_rows'] == 250
    assert witness['selected_source_histogram'] == {
        'gauss_basis_single': 2,
        'gauss_support_origin': 166,
        'projection_basis_single': 4,
        'projection_origin': 78,
    }
    assert witness['witness_sha256'] == EXPECTED_WITNESS_SHA256
    assert len(witness['selected_candidate_indices']) == 250
    assert len(witness['selected_points_hex']) == 250
    assert len(set(witness['selected_points_hex'])) == 250
    assert len(witness['selected_sources']) == 250

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_GROUP_OUTPUT_MODP_RANK_WITNESS_RESULT')
    print('rank_mod_65521=250 rank_mod_1000003=250')
    print('witness_prime=65521 determinant_mod_prime=27993 selected_rows=250')
    print(f'witness_sha256={EXPECTED_WITNESS_SHA256}')
    print('decision=MODP_FULL_RANK250_PHYSICAL_EVALUATION_WITNESS')
    print('theorem=the 250 exact integer-valued C916 e0 first-dyadic group residual functions are linearly independent over Q')
    print('important=this does not imply a 250-bit nonlinear joint state or a complete separator-width theorem')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
