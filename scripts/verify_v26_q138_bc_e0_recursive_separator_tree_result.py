#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_recursive_separator_tree as P

EXPECTED = {
    'B': {
        'groups': 251,
        'best_order': 'local_rank_ascending',
        'best_width': 80,
        'best_depth': 11,
        'candidate_widths': {
            'local_rank_ascending': 80,
            'local_rank_descending': 88,
            'multiplicity_then_rank': 80,
        },
        'root_children': [
            {'size': 167, 'rank': 73, 'complement_rank': 125, 'lambda': 49},
            {'size': 84, 'rank': 125, 'complement_rank': 73, 'lambda': 49},
        ],
    },
    'C': {
        'groups': 250,
        'best_order': 'local_rank_descending',
        'best_width': 80,
        'best_depth': 11,
        'candidate_widths': {
            'local_rank_ascending': 83,
            'local_rank_descending': 80,
            'multiplicity_then_rank': 83,
        },
        'root_children': [
            {'size': 83, 'rank': 127, 'complement_rank': 70, 'lambda': 48},
            {'size': 167, 'rank': 70, 'complement_rank': 127, 'lambda': 48},
        ],
    },
}


def compact(out):
    return {
        'groups': out['groups'],
        'best_order': out['best_order'],
        'best_width': out['best_width'],
        'best_depth': out['best_depth'],
        'candidate_widths': {
            name: data['certificate']['width']
            for name, data in out['candidates'].items()
        },
        'root_children': out['best_root_children'],
    }


def main():
    observed = {}
    for pos in 'BC':
        out = P.analyze(pos)
        got = compact(out)
        exp = EXPECTED[pos]
        assert got == exp, (pos, got, exp)
        observed[pos] = got

    print('frozen_result', json.dumps(observed, sort_keys=True))
    print('PASS V26_Q138_BC_E0_RECURSIVE_SEPARATOR_TREE_RESULT')
    print('scope=frozen exact recursive linear-signature contraction-tree certificates from clean run 34197401783')
    print('claim=B and C each admit a displayed exact tree with maximum separator lambda 80; no optimal branchwidth claim')
    print('not_included=quadratic scalar phase, grouped-e0 carry values, e0-half cross-carry, complete B2/C2, W_repr, alpha, arithmetic-work, ranking/search, full-round')


if __name__ == '__main__':
    main()
