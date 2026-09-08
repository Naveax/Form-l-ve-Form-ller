#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_aggregate_signature_separator as A
import probe_v26_q138_c916_quadratic_function_space_separator as F
import probe_v26_q138_c916_quadratic_residual_separator as R
import probe_v26_q138_c916_full_tree_evaluation_width as P

DOMAIN_BITS = F.DOMAIN_BITS
assert DOMAIN_BITS == 149


def digest(indices):
    payload = ','.join(str(i) for i in sorted(indices)).encode()
    return hashlib.sha256(payload).hexdigest()[:16]


class EvaluationOracle:
    def __init__(self, groups):
        self.groups = groups
        self.all_indices = frozenset(range(len(groups)))
        self.oracles = {
            'function': R.BasisOracle(groups, 'function_basis'),
            'linear': R.BasisOracle(groups, 'linear_basis'),
        }
        linear_all = self.oracles['linear'].basis(self.all_indices)
        assert len(linear_all) == DOMAIN_BITS
        self.affine_basis = A.L.basis(linear_all + [R.CONST_BIT])
        self.cache = {}

    def stats(self, subset):
        key = frozenset(subset)
        if not key or key == self.all_indices:
            return {
                'safe_evaluation_bits': 0,
                'function_lambda': 0,
                'fiber_affine_residual': True,
                'quadratic_residual_dim': 0,
            }
        if key not in self.cache:
            self.cache[key] = P.analyze_edge(
                key,
                self.all_indices,
                self.oracles,
                self.affine_basis,
            )
        return self.cache[key]


def candidate_splits(lo, hi):
    return F.candidate_splits(lo, hi)


def build_tree(order, oracle, lo=0, hi=None):
    if hi is None:
        hi = len(order)
    indices = frozenset(order[lo:hi])
    st = oracle.stats(indices)
    node = {
        'lo': lo,
        'hi': hi,
        'size': hi-lo,
        'safe_evaluation_bits': st['safe_evaluation_bits'],
        'function_lambda': st['function_lambda'],
        'digest': digest(indices),
    }
    if hi-lo == 1:
        node['leaf_group'] = order[lo]
        return node

    choices = []
    for split in candidate_splits(lo, hi):
        left = frozenset(order[lo:split])
        right = frozenset(order[split:hi])
        ls = oracle.stats(left)
        rs = oracle.stats(right)
        choices.append((
            max(ls['safe_evaluation_bits'], rs['safe_evaluation_bits']),
            ls['safe_evaluation_bits'] + rs['safe_evaluation_bits'],
            max(ls['function_lambda'], rs['function_lambda']),
            ls['function_lambda'] + rs['function_lambda'],
            abs((split-lo)-(hi-split)),
            split,
        ))
    choices.sort()
    split = choices[0][-1]
    node['split'] = split
    node['left'] = build_tree(order, oracle, lo, split)
    node['right'] = build_tree(order, oracle, split, hi)
    return node


def verify_tree(tree, order, oracle):
    safe = []
    func = []
    fiber_quad = 0
    seen = []
    depths = []
    edge_stats = []

    def walk(node, depth):
        nonlocal fiber_quad
        lo, hi = node['lo'], node['hi']
        idx = frozenset(order[lo:hi])
        st = oracle.stats(idx)
        assert node['digest'] == digest(idx)
        assert node['safe_evaluation_bits'] == st['safe_evaluation_bits']
        assert node['function_lambda'] == st['function_lambda']
        depths.append(depth)
        if not (lo == 0 and hi == len(order)):
            safe.append(st['safe_evaluation_bits'])
            func.append(st['function_lambda'])
            fiber_quad += int(not st['fiber_affine_residual'])
            edge_stats.append({
                'lo': lo,
                'hi': hi,
                'size': hi-lo,
                'safe_evaluation_bits': st['safe_evaluation_bits'],
                'function_lambda': st['function_lambda'],
                'quadratic_residual_dim': st['quadratic_residual_dim'],
                'fiber_affine_residual': st['fiber_affine_residual'],
            })
        if hi-lo == 1:
            assert node['leaf_group'] == order[lo]
            seen.append(node['leaf_group'])
            return
        split = node['split']
        assert lo < split < hi
        walk(node['left'], depth+1)
        walk(node['right'], depth+1)

    walk(tree, 0)
    assert sorted(seen) == list(range(len(order)))
    assert len(edge_stats) == 2*len(order)-2
    worst = sorted(
        edge_stats,
        key=lambda x: (-x['safe_evaluation_bits'], -x['function_lambda'], -x['size'], x['lo']),
    )[:16]
    return {
        'safe_width': max(safe),
        'function_width_on_evaluation_tree': max(func),
        'max_depth': max(depths),
        'fiber_quadratic_edges': fiber_quad,
        'worst_edges': worst,
        'oracle_cache_entries': len(oracle.cache),
    }


def analyze():
    raw, groups = F.build_groups()
    assert raw == 577 and len(groups) == 250
    n = len(groups)

    orders = {
        'multiplicity_then_function': sorted(
            range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['function_rank'], i)
        ),
        'multiplicity_then_linear': sorted(
            range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['linear_rank'], i)
        ),
    }

    candidates = {}
    for name, order in orders.items():
        oracle = EvaluationOracle(groups)
        tree = build_tree(order, oracle)
        cert = verify_tree(tree, order, oracle)
        candidates[name] = cert
        print('candidate', name, json.dumps(cert, sort_keys=True), flush=True)

    best_name, best = min(
        candidates.items(),
        key=lambda kv: (kv[1]['safe_width'], kv[1]['function_width_on_evaluation_tree'], kv[1]['max_depth'], kv[0]),
    )
    out = {
        'position': 'C',
        'support_groups': n,
        'baseline_function_tree_width': 70,
        'baseline_safe_evaluation_width': 65,
        'candidate_safe_widths': {k: v['safe_width'] for k, v in candidates.items()},
        'candidate_function_widths': {k: v['function_width_on_evaluation_tree'] for k, v in candidates.items()},
        'best_order': best_name,
        'best_safe_evaluation_width': best['safe_width'],
        'best_function_width': best['function_width_on_evaluation_tree'],
        'best_depth': best['max_depth'],
        'best_fiber_quadratic_edges': best['fiber_quadratic_edges'],
        'best_worst_edges': best['worst_edges'],
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_EVALUATION_AWARE_RECURSIVE_TREE')
    print('scope=heuristic exact certificate for displayed recursive trees whose split choices minimize the currently certified safe evaluation-state edge cost rather than function-space lambda')
    print('important=the displayed tree widths are safe exact upper bounds under the same edge evaluator as the merged width65 certificate; no optimal branchwidth claim')
    print('decision=if any candidate beats 65, freeze that contraction tree; otherwise expand ordering/split search without changing the edge semantics')
    print('not_included=aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
