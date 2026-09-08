#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_quadratic_function_space_separator as F
import probe_v26_q138_c916_evaluation_aware_recursive_tree_refined as E

PARENT_LO = 166
PARENT_HI = 250
OLD_SPLIT = 199
TARGET_BITS = 64


def summarize(st, lo, hi):
    return {
        'lo': lo,
        'hi': hi,
        'size': hi-lo,
        'safe_evaluation_bits': st['safe_evaluation_bits'],
        'generic_safe_evaluation_bits': st.get('generic_safe_evaluation_bits', st['safe_evaluation_bits']),
        'function_lambda': st['function_lambda'],
        'quadratic_residual_dim': st['quadratic_residual_dim'],
        'fiber_affine_residual': st['fiber_affine_residual'],
        'exact_override': st.get('exact_override', False),
        'digest': E.digest(frozenset()),
    }


def analyze():
    raw, groups = F.build_groups()
    assert raw == 577 and len(groups) == 250
    order = sorted(range(len(groups)), key=lambda i: (groups[i]['multiplicity'], groups[i]['function_rank'], i))
    oracle = E.EvaluationOracle(groups)

    parent_idx = frozenset(order[PARENT_LO:PARENT_HI])
    parent = dict(oracle.stats(parent_idx))
    parent_summary = {
        'lo': PARENT_LO,
        'hi': PARENT_HI,
        'size': PARENT_HI-PARENT_LO,
        'safe_evaluation_bits': parent['safe_evaluation_bits'],
        'generic_safe_evaluation_bits': parent.get('generic_safe_evaluation_bits', parent['safe_evaluation_bits']),
        'function_lambda': parent['function_lambda'],
        'quadratic_residual_dim': parent['quadratic_residual_dim'],
        'fiber_affine_residual': parent['fiber_affine_residual'],
        'exact_override': parent.get('exact_override', False),
        'digest': E.digest(parent_idx),
    }

    rows = []
    hist = Counter()
    for split in range(PARENT_LO+1, PARENT_HI):
        li = frozenset(order[PARENT_LO:split])
        ri = frozenset(order[split:PARENT_HI])
        ls = dict(oracle.stats(li))
        rs = dict(oracle.stats(ri))
        left = {
            'lo': PARENT_LO, 'hi': split, 'size': split-PARENT_LO,
            'safe_evaluation_bits': ls['safe_evaluation_bits'],
            'generic_safe_evaluation_bits': ls.get('generic_safe_evaluation_bits', ls['safe_evaluation_bits']),
            'function_lambda': ls['function_lambda'],
            'quadratic_residual_dim': ls['quadratic_residual_dim'],
            'fiber_affine_residual': ls['fiber_affine_residual'],
            'exact_override': ls.get('exact_override', False),
            'digest': E.digest(li),
        }
        right = {
            'lo': split, 'hi': PARENT_HI, 'size': PARENT_HI-split,
            'safe_evaluation_bits': rs['safe_evaluation_bits'],
            'generic_safe_evaluation_bits': rs.get('generic_safe_evaluation_bits', rs['safe_evaluation_bits']),
            'function_lambda': rs['function_lambda'],
            'quadratic_residual_dim': rs['quadratic_residual_dim'],
            'fiber_affine_residual': rs['fiber_affine_residual'],
            'exact_override': rs.get('exact_override', False),
            'digest': E.digest(ri),
        }
        m = max(left['safe_evaluation_bits'], right['safe_evaluation_bits'])
        hist[m] += 1
        rows.append({
            'split': split,
            'left': left,
            'right': right,
            'max_child_safe_bits': m,
            'sum_child_safe_bits': left['safe_evaluation_bits'] + right['safe_evaluation_bits'],
            'max_child_function_lambda': max(left['function_lambda'], right['function_lambda']),
        })

    rows.sort(key=lambda r: (
        r['max_child_safe_bits'],
        r['sum_child_safe_bits'],
        r['max_child_function_lambda'],
        abs((r['split']-PARENT_LO)-(PARENT_HI-r['split'])),
        r['split'],
    ))
    old = next(r for r in rows if r['split'] == OLD_SPLIT)
    feasible = [r for r in rows if r['max_child_safe_bits'] <= TARGET_BITS]
    strict = [r for r in rows if r['max_child_safe_bits'] < 65]
    best = rows[0]

    assert old['left']['exact_override'] is True
    assert old['left']['safe_evaluation_bits'] == 65
    assert old['left']['digest'] == '50a4b970f7f85916'
    assert len(rows) == 83

    out = {
        'position': 'C',
        'order': 'multiplicity_then_function',
        'parent': parent_summary,
        'splits_scanned': len(rows),
        'target_bits': TARGET_BITS,
        'max_child_safe_histogram': dict(sorted(hist.items())),
        'best_split': best,
        'old_split': old,
        'splits_with_max_child_safe_le_64': len(feasible),
        'splits_with_max_child_safe_lt_65': len(strict),
        'first_feasible_splits': feasible[:20],
        'top_splits': rows[:20],
        'oracle_cache_entries': len(oracle.cache),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_BOTTLENECK_PARENT_SPLIT_SCAN')
    print('scope=exact scan of all 83 contiguous splits of the baseline bottleneck parent [166,250)')
    print('decision=if any split has both children <=64, rebuild that local subtree under threshold64; otherwise local reordering is required')
    print('important=direct-child feasibility only; this does not yet certify the recursively rebuilt local subtree')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
