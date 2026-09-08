#!/usr/bin/env python3
import json
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_quadratic_function_space_separator as F
import probe_v26_q138_c916_evaluation_aware_recursive_tree_refined as E

LO = 0
HI = 166
TARGET = 59


def find_interval(node, lo, hi):
    if node['lo'] == lo and node['hi'] == hi:
        return node
    if 'left' not in node:
        return None
    return find_interval(node['left'], lo, hi) or find_interval(node['right'], lo, hi)


def analyze():
    raw, groups = F.build_groups()
    assert raw == 577 and len(groups) == 250
    order = sorted(range(len(groups)), key=lambda i: (groups[i]['multiplicity'], groups[i]['function_rank'], i))

    foracle = F.RankOracle(groups, 'function_basis')
    baseline = F.build_tree(order, foracle)
    target_node = find_interval(baseline, LO, HI)
    assert target_node is not None, 'expected [0,166) baseline parent is absent'

    oracle = E.EvaluationOracle(groups)
    cost_cache = {}

    def stats(lo, hi):
        key = (lo, hi)
        if key not in cost_cache:
            idx = frozenset(order[lo:hi])
            st = dict(oracle.stats(idx))
            cost_cache[key] = {
                'lo': lo, 'hi': hi, 'size': hi-lo,
                'safe_evaluation_bits': st['safe_evaluation_bits'],
                'generic_safe_evaluation_bits': st.get('generic_safe_evaluation_bits', st['safe_evaluation_bits']),
                'function_lambda': st['function_lambda'],
                'quadratic_residual_dim': st['quadratic_residual_dim'],
                'fiber_affine_residual': st['fiber_affine_residual'],
                'exact_override': st.get('exact_override', False),
                'digest': E.digest(idx),
            }
        return cost_cache[key]

    parent = stats(LO, HI)

    @lru_cache(None)
    def feasible(lo, hi):
        st = stats(lo, hi)
        if st['safe_evaluation_bits'] > TARGET:
            return None
        if hi-lo == 1:
            return {'lo': lo, 'hi': hi, 'split': None}

        choices = []
        for split in range(lo+1, hi):
            ls = stats(lo, split)
            rs = stats(split, hi)
            if max(ls['safe_evaluation_bits'], rs['safe_evaluation_bits']) <= TARGET:
                choices.append((
                    max(ls['safe_evaluation_bits'], rs['safe_evaluation_bits']),
                    ls['safe_evaluation_bits'] + rs['safe_evaluation_bits'],
                    max(ls['function_lambda'], rs['function_lambda']),
                    abs((split-lo)-(hi-split)),
                    split,
                ))
        choices.sort()
        for *_key, split in choices:
            left = feasible(lo, split)
            if left is None:
                continue
            right = feasible(split, hi)
            if right is None:
                continue
            return {'lo': lo, 'hi': hi, 'split': split, 'left': left, 'right': right}
        return None

    root_choices = []
    for split in range(LO+1, HI):
        ls = stats(LO, split)
        rs = stats(split, HI)
        if max(ls['safe_evaluation_bits'], rs['safe_evaluation_bits']) <= TARGET:
            root_choices.append((
                max(ls['safe_evaluation_bits'], rs['safe_evaluation_bits']),
                ls['safe_evaluation_bits'] + rs['safe_evaluation_bits'],
                max(ls['function_lambda'], rs['function_lambda']),
                abs((split-LO)-(HI-split)), split,
            ))
    root_choices.sort()

    witness = None
    if parent['safe_evaluation_bits'] <= TARGET:
        for *_key, split in root_choices:
            left = feasible(LO, split)
            if left is None:
                continue
            right = feasible(split, HI)
            if right is None:
                continue
            witness = {'lo': LO, 'hi': HI, 'split': split, 'left': left, 'right': right}
            break

    edges = []
    max_depth = 0
    if witness is not None:
        def walk(node, depth, root=False):
            nonlocal max_depth
            max_depth = max(max_depth, depth)
            if not root:
                edges.append(stats(node['lo'], node['hi']))
            if node['split'] is not None:
                walk(node['left'], depth+1)
                walk(node['right'], depth+1)
        walk(witness, 0, root=True)
        assert len(edges) == 2*(HI-LO)-2
        assert max(e['safe_evaluation_bits'] for e in edges) <= TARGET

    out = {
        'position': 'C',
        'order': 'multiplicity_then_function',
        'parent': parent,
        'parent_exists_in_baseline_tree': True,
        'target_bits': TARGET,
        'direct_root_splits_le_59': len(root_choices),
        'threshold59_feasible': witness is not None,
        'witness': witness,
        'witness_root_split': witness['split'] if witness else None,
        'witness_max_depth': max_depth if witness else None,
        'witness_edge_count': len(edges),
        'witness_max_safe_bits': max((e['safe_evaluation_bits'] for e in edges), default=None),
        'worst_witness_edges': sorted(edges, key=lambda e: (-e['safe_evaluation_bits'], -e['function_lambda'], -e['size'], e['lo']))[:24],
        'interval_costs_evaluated': len(cost_cache),
        'feasibility_states_cached': feasible.cache_info().currsize,
        'oracle_cache_entries': len(oracle.cache),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_LEFT_PARENT_THRESHOLD59_DP')
    print('scope=exact fixed-order contiguous interval threshold59 feasibility search inside the baseline parent [0,166), retaining the parent edge itself')
    print('decision=if feasible, replace [0,166) descendants to remove both current 60-bit child bottlenecks; if infeasible, fixed-order contiguous surgery cannot certify full-tree width59')
    print('important=no unrestricted branchwidth claim')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
