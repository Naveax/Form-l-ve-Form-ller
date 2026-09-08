#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_quadratic_scalar_refinement as P

EXPECTED = {
    'B': {
        'refined_local_rank_histogram': {144: 2, 145: 46, 146: 79, 147: 67, 148: 35, 149: 22},
        'extra_rank_histogram': {119: 1, 121: 11, 122: 27, 123: 34, 124: 91, 125: 80, 126: 7},
        'groups_already_scalar_determined': 0,
        'groups_refined_to_full_149': 22,
        'max_refined_rank': 149,
        'max_extra_rank': 126,
        'best_balanced_lambda': 147,
        'path_widths': {
            'original_rank_ascending': 149,
            'refined_rank_ascending': 149,
            'refined_rank_descending': 149,
            'multiplicity_then_refined': 149,
        },
    },
    'C': {
        'refined_local_rank_histogram': {145: 43, 146: 102, 147: 52, 148: 45, 149: 8},
        'extra_rank_histogram': {120: 1, 121: 10, 122: 37, 123: 64, 124: 52, 125: 70, 126: 14, 127: 2},
        'groups_already_scalar_determined': 0,
        'groups_refined_to_full_149': 8,
        'max_refined_rank': 149,
        'max_extra_rank': 127,
        'best_balanced_lambda': 147,
        'path_widths': {
            'original_rank_ascending': 149,
            'refined_rank_ascending': 149,
            'refined_rank_descending': 149,
            'multiplicity_then_refined': 149,
        },
    },
}


def compact(out):
    return {
        'refined_local_rank_histogram': out['refined_local_rank_histogram'],
        'extra_rank_histogram': out['extra_rank_histogram'],
        'groups_already_scalar_determined': out['groups_already_scalar_determined'],
        'groups_refined_to_full_149': out['groups_refined_to_full_149'],
        'max_refined_rank': out['max_refined_rank'],
        'max_extra_rank': out['max_extra_rank'],
        'best_balanced_lambda': out['best_deterministic_balanced_cut']['lambda'],
        'path_widths': {
            name: profile['max_lambda']
            for name, profile in out['order_profiles'].items()
        },
    }


def main():
    observed = {}
    for pos in 'BC':
        out = P.analyze(pos)
        got = compact(out)
        exp = EXPECTED[pos]
        assert got == exp, (pos, got, exp)
        assert out['phase_internal_pr_histogram'] == ({0: 566, 2: 15} if pos == 'B' else {0: 562, 2: 15})
        observed[pos] = got

    print('frozen_result', json.dumps(observed, sort_keys=True))
    print('PASS V26_Q138_BC_E0_QUADRATIC_SCALAR_REFINEMENT_RESULT')
    print('scope=frozen clean-run 34197928053 sectorwise minimal linear scalar-refinement diagnostic')
    print('decision=NO_SECTORWISE_LINEAR_SCALAR_SEPARATOR_GAIN')
    print('claim=sectorwise scalar determination raises local ranks to 144..149 for B and 145..149 for C; displayed balanced lambda is 147 and every tested path width is 149')
    print('not_closed=aggregate same-support cross-sector cancellation remains open and is the next route')


if __name__ == '__main__':
    main()
