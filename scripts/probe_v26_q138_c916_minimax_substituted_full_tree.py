#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_quadratic_function_space_separator as F
import probe_v26_q138_c916_evaluation_aware_recursive_tree_refined as E
import probe_v26_q138_c916_bottleneck_parent_minimax_interval_dp as M

TARGET_LO = 166
TARGET_HI = 250


def analyze():
    local = M.analyze()
    witness = local['witness']
    local_optimum = local['exact_minimax_safe_width']
    assert witness['lo'] == TARGET_LO and witness['hi'] == TARGET_HI

    raw, groups = F.build_groups()
    assert raw == 577 and len(groups) == 250
    n = len(groups)
    order = sorted(range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['function_rank'], i))

    foracle = F.RankOracle(groups, 'function_basis')
    baseline = F.build_tree(order, foracle)
    fcert = F.verify_tree(baseline, order, foracle)
    assert fcert['width'] == 70 and fcert['max_depth'] == 10

    oracle = E.EvaluationOracle(groups)
    edges = []
    seen = []
    replaced = 0
    max_depth = 0

    def add_edge(lo, hi, source, depth):
        nonlocal max_depth
        idx = frozenset(order[lo:hi])
        st = dict(oracle.stats(idx))
        row = {
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
            'source': source,
            'depth': depth,
        }
        edges.append(row)
        max_depth = max(max_depth, depth)
        return row

    def walk_witness(node, depth, root=False):
        lo, hi = node['lo'], node['hi']
        if not root:
            add_edge(lo, hi, 'minimax_witness', depth)
        split = node['split']
        if split is None:
            seen.append(lo)
            return
        walk_witness(node['left'], depth+1)
        walk_witness(node['right'], depth+1)

    def walk_baseline(node, depth, root=False):
        nonlocal replaced, max_depth
        lo, hi = node['lo'], node['hi']
        max_depth = max(max_depth, depth)
        if not root:
            add_edge(lo, hi, 'baseline', depth)
        if lo == TARGET_LO and hi == TARGET_HI:
            replaced += 1
            walk_witness(witness, depth, root=True)
            return
        if 'left' not in node:
            seen.append(lo)
            return
        walk_baseline(node['left'], depth+1)
        walk_baseline(node['right'], depth+1)

    walk_baseline(baseline, 0, root=True)
    assert replaced == 1
    assert sorted(seen) == list(range(n))
    assert len(edges) == 2*n - 2 == 498

    target_parent = [e for e in edges if e['lo'] == TARGET_LO and e['hi'] == TARGET_HI]
    assert len(target_parent) == 1
    assert target_parent[0]['safe_evaluation_bits'] == 40

    assert not any(e['lo'] == 166 and e['hi'] == 199 for e in edges)

    local_edges = [e for e in edges if e['source'] == 'minimax_witness']
    assert len(local_edges) == 2*(TARGET_HI-TARGET_LO)-2 == 166
    assert max(e['safe_evaluation_bits'] for e in local_edges) == local_optimum

    outside_edges = [e for e in edges if e['source'] == 'baseline']
    safe_width = max(e['safe_evaluation_bits'] for e in edges)
    outside_width = max(e['safe_evaluation_bits'] for e in outside_edges)
    function_width = max(e['function_lambda'] for e in edges)
    safe_hist = Counter(e['safe_evaluation_bits'] for e in edges)
    worst = sorted(
        edges,
        key=lambda e: (-e['safe_evaluation_bits'], -e['function_lambda'], -e['size'], e['lo']),
    )[:24]

    out = {
        'position': 'C',
        'support_groups': n,
        'tree_edges_analyzed': len(edges),
        'baseline_function_tree_width': fcert['width'],
        'baseline_function_tree_depth': fcert['max_depth'],
        'local_minimax_width': local_optimum,
        'local_root_split': local['root_split'],
        'local_witness_edge_count': len(local_edges),
        'outside_safe_width': outside_width,
        'substituted_full_tree_safe_width': safe_width,
        'substituted_full_tree_function_width': function_width,
        'substituted_full_tree_depth': max_depth,
        'safe_evaluation_bit_histogram': dict(sorted(safe_hist.items())),
        'worst_edges': worst,
        'oracle_cache_entries': len(oracle.cache),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_MINIMAX_SUBSTITUTED_FULL_TREE')
    print('scope=exact safe-evaluation remeasurement of all 498 non-root edges after substituting the exact fixed-order minimax witness for parent [166,250)')
    print('important=certifies this displayed substituted tree only; no unrestricted optimal branchwidth claim')
    print('not_included=aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
