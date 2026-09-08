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


def known_exact_overrides(groups):
    n = len(groups)
    base = sorted(range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['function_rank'], i))
    all_idx = frozenset(range(n))
    specs = [
        ('former_width70', 110, 166, 60),
        ('width64_quadratic', 55, 110, 60),
        ('exact_width65', 166, 199, 65),
    ]
    out = {}
    meta = []
    for name, lo, hi, bits in specs:
        key = frozenset(base[lo:hi])
        comp = all_idx - key
        out[key] = bits
        out[comp] = bits
        meta.append({'name': name, 'lo': lo, 'hi': hi, 'bits': bits, 'digest': digest(key)})
    return out, meta


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
        self.exact_overrides, self.override_meta = known_exact_overrides(groups)
        self.cache = {}

    def stats(self, subset):
        key = frozenset(subset)
        if not key or key == self.all_indices:
            return {
                'safe_evaluation_bits': 0,
                'function_lambda': 0,
                'fiber_affine_residual': True,
                'quadratic_residual_dim': 0,
                'exact_override': False,
            }
        if key not in self.cache:
            st = dict(P.analyze_edge(key, self.all_indices, self.oracles, self.affine_basis))
            st['generic_safe_evaluation_bits'] = st['safe_evaluation_bits']
            st['exact_override'] = key in self.exact_overrides
            if st['exact_override']:
                exact = self.exact_overrides[key]
                assert exact <= st['safe_evaluation_bits']
                st['safe_evaluation_bits'] = exact
            self.cache[key] = st
        return self.cache[key]


def candidate_splits(lo, hi):
    n = hi - lo
    assert n >= 2
    if n <= 6:
        return list(range(lo + 1, hi))
    offsets = {n//4, n//3, (2*n)//5, n//2, (3*n)//5, (2*n)//3, (3*n)//4}
    return sorted(lo + x for x in offsets if 0 < x < n)


def build_tree(order, oracle, lo=0, hi=None):
    if hi is None:
        hi = len(order)
    idx = frozenset(order[lo:hi])
    st = oracle.stats(idx)
    node = {
        'lo': lo,
        'hi': hi,
        'size': hi-lo,
        'safe_evaluation_bits': st['safe_evaluation_bits'],
        'function_lambda': st['function_lambda'],
        'digest': digest(idx),
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
    seen = []
    depths = []
    edges = []

    def walk(node, depth):
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
                'digest': digest(idx),
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
    assert len(edges) == 2*len(order)-2
    worst = sorted(edges, key=lambda e: (-e['safe_evaluation_bits'], -e['function_lambda'], -e['size'], e['lo']))[:20]
    return {
        'safe_width': max(safe),
        'function_width': max(func),
        'max_depth': max(depths),
        'exact_override_edges': sum(e['exact_override'] for e in edges),
        'fiber_quadratic_edges': sum(not e['fiber_affine_residual'] for e in edges),
        'worst_edges': worst,
    }


def analyze():
    raw, groups = F.build_groups()
    assert raw == 577 and len(groups) == 250
    n = len(groups)
    orders = {
        'multiplicity_then_function': sorted(range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['function_rank'], i)),
        'multiplicity_then_linear': sorted(range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['linear_rank'], i)),
        'function_then_multiplicity': sorted(range(n), key=lambda i: (groups[i]['function_rank'], groups[i]['multiplicity'], i)),
        'linear_then_multiplicity': sorted(range(n), key=lambda i: (groups[i]['linear_rank'], groups[i]['multiplicity'], i)),
        'function_descending': sorted(range(n), key=lambda i: (-groups[i]['function_rank'], groups[i]['multiplicity'], i)),
        'linear_descending': sorted(range(n), key=lambda i: (-groups[i]['linear_rank'], groups[i]['multiplicity'], i)),
    }

    oracle = EvaluationOracle(groups)
    candidates = {}
    for name, order in orders.items():
        tree = build_tree(order, oracle)
        cert = verify_tree(tree, order, oracle)
        candidates[name] = cert
        print('candidate', name, json.dumps(cert, sort_keys=True), flush=True)

    best_name, best = min(candidates.items(), key=lambda kv: (kv[1]['safe_width'], kv[1]['function_width'], kv[1]['max_depth'], kv[0]))
    out = {
        'position': 'C',
        'support_groups': n,
        'baseline_safe_evaluation_width': 65,
        'baseline_function_width': 70,
        'exact_override_meta': oracle.override_meta,
        'candidate_safe_widths': {k: v['safe_width'] for k, v in candidates.items()},
        'candidate_function_widths': {k: v['function_width'] for k, v in candidates.items()},
        'best_order': best_name,
        'best_safe_evaluation_width': best['safe_width'],
        'best_function_width': best['function_width'],
        'best_depth': best['max_depth'],
        'best_exact_override_edges': best['exact_override_edges'],
        'best_worst_edges': best['worst_edges'],
        'oracle_cache_entries': len(oracle.cache),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_EVALUATION_AWARE_RECURSIVE_TREE_REFINED')
    print('scope=expanded deterministic heuristic tree search using safe evaluation edge costs plus subset-stable exact edge refinements from merged certificates')
    print('important=each displayed tree is an exact certificate for its displayed safe upper bound; no optimal branchwidth claim')
    print('decision=freeze any candidate below 65; otherwise move to local tree surgery around exact bottleneck cuts rather than blindly adding more global orders')
    print('not_included=aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
