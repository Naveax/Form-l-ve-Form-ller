#!/usr/bin/env python3
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_width61_local_signature_sufficiency as P


def main():
    with redirect_stdout(io.StringIO()):
        out = P.analyze()

    assert out['position'] == 'C'
    assert out['physical_shared_dimension'] == 149
    assert out['synthetic_factorization_and_translation_regression_cases'] == 68
    assert out['support_groups'] == 250
    assert out['support_multiplicity_histogram'] == {1: 103, 2: 57, 4: 90}
    assert out['physical_term_count'] == 680
    assert out['frozen_separator_best_order'] == 'multiplicity_then_refined'
    assert out['frozen_separator_width'] == 61
    assert out['frozen_separator_depth'] == 11
    assert out['refined_rank_histogram'] == {
        12: 3, 13: 6, 14: 8, 15: 24, 16: 25,
        17: 38, 18: 40, 19: 7, 20: 14, 21: 85,
    }
    assert out['refined_kernel_dimension_histogram'] == {
        128: 85, 129: 14, 130: 7, 131: 40, 132: 38,
        133: 25, 134: 24, 135: 8, 136: 6, 137: 3,
    }
    assert out['factorization_status_histogram'] == {'refuted': 250}
    assert out['factorization_status_by_multiplicity'] == {
        1: {'refuted': 103},
        2: {'refuted': 57},
        4: {'refuted': 90},
    }
    assert out['first_counterexample_mechanism_histogram'] == {
        'all_supports_preserved_phase_only': 250,
    }
    assert out['first_failure_kernel_basis_index_histogram'] == {0: 250}
    assert out['kernel_directions_checked_per_group_histogram'] == {1: 250}
    assert out['decision'] == (
        'ALL_250_GROUP_OUTPUTS_REFUTE_WIDTH61_REFINED_LOCAL_SIGNATURE_SUFFICIENCY'
    )

    groups = out['groups']
    assert len(groups) == 250
    for gid, rec in enumerate(groups):
        assert rec['group_id'] == gid
        assert rec['factorizes_through_refined_linear_signature'] is False
        assert rec['kernel_directions_checked'] == 1
        witness = rec['first_counterexample']
        assert witness is not None
        assert witness['kernel_basis_index'] == 0
        assert witness['mechanism'] == 'all_supports_preserved_phase_only'
        assert witness['difference_norm2'] > 0
        assert witness['translation_weight'] >= 1
        assert rec['kernel_dimension'] == 149 - rec['refined_rank']

    g0 = groups[0]
    assert g0['multiplicity'] == 2
    assert g0['refined_rank'] == 16
    assert g0['kernel_dimension'] == 133
    assert g0['first_counterexample'] == {
        'kernel_basis_index': 0,
        'translation_hex': '00000000000000000000000000000000000004',
        'translation_weight': 1,
        'mechanism': 'all_supports_preserved_phase_only',
        'norm2': 713623846352979940529142984724747568191373312,
        'translation_inner_product': 0,
        'difference_norm2': 1427247692705959881058285969449495136382746624,
    }

    g1 = groups[1]
    assert g1['multiplicity'] == 1
    assert g1['refined_rank'] == 21
    assert g1['kernel_dimension'] == 128
    assert g1['first_counterexample']['mechanism'] == 'all_supports_preserved_phase_only'
    assert g1['first_counterexample']['difference_norm2'] == 713623846352979940529142984724747568191373312

    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_WIDTH61_LOCAL_SIGNATURE_SUFFICIENCY_RESULT')
    print('factorization_status=refuted_250_of_250')
    print('first_failure_kernel_basis_index=0_for_all_250')
    print('mechanism=all_supports_preserved_phase_only_for_all_250')
    print('decision=ALL_250_GROUP_OUTPUTS_REFUTE_WIDTH61_REFINED_LOCAL_SIGNATURE_SUFFICIENCY')
    print('important=PR148 width61 remains valid for its original support/frequency/radical target; only unchanged promotion to exact nonlinear first-dyadic outputs is refuted')
    print('ALPHA_PASS=0')


if __name__ == '__main__':
    main()
