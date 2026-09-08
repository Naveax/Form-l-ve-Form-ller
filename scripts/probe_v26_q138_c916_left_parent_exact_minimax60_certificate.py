#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_left_parent_threshold59_dp as T
import probe_v26_q138_c916_quadratic_function_space_separator as F
import probe_v26_q138_c916_evaluation_aware_recursive_tree_refined as E

LO = 0
HI = 166


def find_interval(node, lo, hi):
    if node['lo'] == lo and node['hi'] == hi:
        return node
    if 'left' not in node:
        return None
    return find_interval(node['left'], lo, hi) or find_interval(node['right'], lo, hi)


def analyze():
    lower = T.analyze()
    assert lower['threshold59_feasible'] is False
    assert lower['target_bits'] == 59
    assert lower['parent_exists_in_baseline_tree'] is True

    raw, groups = F.build_groups()
    assert raw == 577 and len(groups) == 250
    order = sorted(
        range(len(groups)),
        key=lambda i: (groups[i]['multiplicity'], groups[i]['function_rank'], i),
    )

    foracle = F.RankOracle(groups, 'function_basis')
    baseline = F.build_tree(order, foracle)
    target = find_interval(baseline, LO, HI)
    assert target is not None

    oracle = E.EvaluationOracle(groups)
    edges = []
    leaves = []
    max_depth = 0

    def walk(node, depth, root=False):
        nonlocal max_depth
        max_depth = max(max_depth, depth)
        lo, hi = node['lo'], node['hi']
        if not root:
            idx = frozenset(order[lo:hi])
            st = dict(oracle.stats(idx))
            edges.append({
                'lo': lo,
                'hi': hi,
                'size': hi-lo,
                'safe_evaluation_bits': st['safe_evaluation_bits'],
                'generic_safe_evaluation_bits': st.get('generic_safe_evaluation_bits', st['safe_evaluation_bits']),
                'function_lambda': st['function_lambda'],
                'quadratic_residual_dim': st['quadratic_residual_dim'],
                'fiber_affine_residual': st['fiber_affine_residual'],
                'exact_override': st.get('exact_override', False),
                'digest': E.digest(idx),
            })
        if 'left' not in node:
            leaves.append(lo)
            return
        walk(node['left'], depth+1)
        walk(node['right'], depth+1)

    walk(target, 0, root=True)
    assert leaves == list(range(LO, HI))
    assert len(edges) == 2*(HI-LO)-2 == 330

    upper = max(e['safe_evaluation_bits'] for e in edges)
    assert upper == 60
    width_hist = Counter(e['safe_evaluation_bits'] for e in edges)
    worst = sorted(
        edges,
        key=lambda e: (-e['safe_evaluation_bits'], -e['function_lambda'], -e['size'], e['lo']),
    )[:24]

    # Exact sandwich: threshold 59 is impossible for the full fixed-order
    # contiguous-tree class, while this explicit baseline subtree has width 60.
    exact_optimum = upper
    assert exact_optimum == lower['target_bits'] + 1

    out = {
        'position': 'C',
        'order': 'multiplicity_then_function',
        'parent_interval': [LO, HI],
        'local_leaves': HI-LO,
        'lower_bound_from_threshold59_no_go': 60,
        'explicit_width60_witness': True,
        'witness_source': 'baseline_function_tree_subtree',
        'witness_edge_count': len(edges),
        'witness_max_depth': max_depth,
        'witness_safe_width': upper,
        'witness_edge_width_histogram': dict(sorted(width_hist.items())),
        'worst_witness_edges': worst,
        'exact_fixed_order_contiguous_minimax_width': exact_optimum,
        'threshold59_direct_root_splits': lower['direct_root_splits_le_59'],
        'threshold59_intervals_evaluated': lower['interval_costs_evaluated'],
        'oracle_cache_entries_for_upper_witness': len(oracle.cache),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_LEFT_PARENT_EXACT_MINIMAX60_CERTIFICATE')
    print('lower=threshold59 exhaustive fixed-order contiguous DP has no complete witness')
    print('upper=explicit baseline [0,166) subtree has every descendant edge <=60')
    print('exact=fixed-order contiguous minimax width on [0,166) is 60')
    print('important=this is not unrestricted branchwidth')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
