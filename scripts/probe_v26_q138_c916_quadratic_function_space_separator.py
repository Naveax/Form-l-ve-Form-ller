#!/usr/bin/env python3
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_aggregate_signature_separator as A
import probe_v26_q138_c916_hybrid_aggregate_scalar_separator as H

POS = 'C'
DOMAIN_BITS = H.DOMAIN_BITS
PAIR_BITS = H.PAIR_BITS
assert DOMAIN_BITS == 149


def linear_function(row):
    return int(row) << PAIR_BITS


def function_rank(vectors):
    return len(A.L.basis(vectors))


def union_rank(groups, key, indices=None):
    if indices is None:
        indices = range(len(groups))
    rows = []
    for i in indices:
        rows.extend(groups[i][key])
    return function_rank(rows)


def build_groups():
    raw, canonical = A.build_groups(POS)
    assert raw == 577 and len(canonical) == 250

    e0, _e1, _half = A.L.U.H.classify_patterns()
    grouped = defaultdict(list)
    for k in range(4):
        for zs, cls in e0[k]:
            can = A.L.U.H.support_for(POS, zs, cls)
            if can is not None:
                grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert len(ordered) == len(canonical)

    groups = []
    for gid, ((can, sectors), info) in enumerate(zip(ordered, canonical)):
        assert gid == info['group_id']
        assert len(sectors) == info['multiplicity']
        _rows, polar, poly = H.scalar_polynomial_vector(sectors)

        linear_basis = A.L.basis(info['combined_basis'])
        frows = [linear_function(r) for r in linear_basis]
        function_basis = A.L.basis(frows + [poly])
        scalar_basis = [poly] if poly else []
        polar_basis = [polar] if polar else []

        groups.append({
            'group_id': gid,
            'multiplicity': info['multiplicity'],
            'linear_rank': len(linear_basis),
            'function_rank': len(function_basis),
            'linear_basis': frows,
            'function_basis': function_basis,
            'scalar_basis': scalar_basis,
            'polar_basis': polar_basis,
        })

    assert union_rank(groups, 'linear_basis') == DOMAIN_BITS
    return raw, groups


class RankOracle:
    def __init__(self, groups, key):
        self.groups = groups
        self.key = key
        self.all_indices = frozenset(range(len(groups)))
        self.global_rank = union_rank(groups, key)
        self.rank_cache = {frozenset(): 0, self.all_indices: self.global_rank}

    def rank(self, subset):
        key = frozenset(subset)
        if key not in self.rank_cache:
            self.rank_cache[key] = union_rank(self.groups, self.key, sorted(key))
        return self.rank_cache[key]

    def stats(self, subset):
        key = frozenset(subset)
        comp = self.all_indices - key
        r = self.rank(key)
        cr = self.rank(comp)
        lam = r + cr - self.global_rank
        assert 0 <= lam <= min(r, cr)
        return r, cr, lam


def candidate_splits(lo, hi):
    n = hi - lo
    assert n >= 2
    if n <= 4:
        return [lo + n // 2]
    offsets = {n // 3, (2*n)//5, n//2, (3*n)//5, (2*n)//3}
    return sorted(lo + x for x in offsets if 0 < x < n)


def digest(indices):
    payload = ','.join(str(i) for i in sorted(indices)).encode()
    return hashlib.sha256(payload).hexdigest()[:16]


def build_tree(order, oracle, lo=0, hi=None):
    if hi is None:
        hi = len(order)
    indices = frozenset(order[lo:hi])
    r, cr, lam = oracle.stats(indices)
    node = {
        'lo': lo,
        'hi': hi,
        'size': hi-lo,
        'rank': r,
        'complement_rank': cr,
        'lambda': lam,
        'digest': digest(indices),
    }
    if hi-lo == 1:
        node['leaf_group'] = order[lo]
        return node

    choices = []
    for split in candidate_splits(lo, hi):
        left = frozenset(order[lo:split])
        right = frozenset(order[split:hi])
        _lr, _lcr, llam = oracle.stats(left)
        _rr, _rcr, rlam = oracle.stats(right)
        choices.append((
            max(llam, rlam),
            llam + rlam,
            abs((split-lo)-(hi-split)),
            split,
            llam,
            rlam,
        ))
    choices.sort()
    _, _, _, split, llam, rlam = choices[0]
    node['split'] = split
    node['search_child_lambdas'] = [llam, rlam]
    node['left'] = build_tree(order, oracle, lo, split)
    node['right'] = build_tree(order, oracle, split, hi)
    return node


def verify_tree(tree, order, oracle):
    seen = []
    widths = []
    depths = []
    internal = 0

    def walk(node, depth):
        nonlocal internal
        lo, hi = node['lo'], node['hi']
        idx = frozenset(order[lo:hi])
        r, cr, lam = oracle.stats(idx)
        assert (node['rank'], node['complement_rank'], node['lambda']) == (r, cr, lam)
        assert node['digest'] == digest(idx)
        if not (lo == 0 and hi == len(order)):
            widths.append(lam)
        depths.append(depth)
        if hi-lo == 1:
            assert node['leaf_group'] == order[lo]
            seen.append(node['leaf_group'])
            return
        internal += 1
        split = node['split']
        assert node['left']['lo'] == lo and node['left']['hi'] == split
        assert node['right']['lo'] == split and node['right']['hi'] == hi
        walk(node['left'], depth+1)
        walk(node['right'], depth+1)

    walk(tree, 0)
    assert sorted(seen) == list(range(len(order)))
    assert internal == len(order)-1
    return {
        'width': max(widths) if widths else 0,
        'max_depth': max(depths),
        'leaves': len(seen),
        'internal_nodes': internal,
    }


def tree_summary(groups, key, orders):
    candidates = {}
    for name, order in orders.items():
        oracle = RankOracle(groups, key)
        tree = build_tree(order, oracle)
        cert = verify_tree(tree, order, oracle)
        candidates[name] = {
            'certificate': cert,
            'root_children': [
                {
                    'size': tree['left']['size'],
                    'rank': tree['left']['rank'],
                    'complement_rank': tree['left']['complement_rank'],
                    'lambda': tree['left']['lambda'],
                },
                {
                    'size': tree['right']['size'],
                    'rank': tree['right']['rank'],
                    'complement_rank': tree['right']['complement_rank'],
                    'lambda': tree['right']['lambda'],
                },
            ],
            'rank_cache_entries': len(oracle.rank_cache),
        }
    best_name, best = min(
        candidates.items(),
        key=lambda kv: (
            kv[1]['certificate']['width'],
            kv[1]['certificate']['max_depth'],
            kv[0],
        ),
    )
    return {
        'global_rank': RankOracle(groups, key).global_rank,
        'candidate_widths': {
            name: data['certificate']['width'] for name, data in candidates.items()
        },
        'best_order': best_name,
        'best_width': best['certificate']['width'],
        'best_depth': best['certificate']['max_depth'],
        'best_root_children': best['root_children'],
    }


def balanced_cut(groups, key, order):
    oracle = RankOracle(groups, key)
    n = len(order)
    left = frozenset(order[:n//2])
    r, cr, lam = oracle.stats(left)
    return {
        'left_groups': len(left),
        'right_groups': n-len(left),
        'left_rank': r,
        'right_rank': cr,
        'lambda': lam,
    }


def analyze():
    raw, groups = build_groups()
    n = len(groups)

    orders = {
        'function_rank_ascending': sorted(
            range(n), key=lambda i: (groups[i]['function_rank'], groups[i]['multiplicity'], i)
        ),
        'function_rank_descending': sorted(
            range(n), key=lambda i: (-groups[i]['function_rank'], groups[i]['multiplicity'], i)
        ),
        'multiplicity_then_function': sorted(
            range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['function_rank'], i)
        ),
        'multiplicity_then_linear': sorted(
            range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['linear_rank'], i)
        ),
    }

    linear = tree_summary(groups, 'linear_basis', orders)
    scalar = tree_summary(groups, 'scalar_basis', orders)
    polar = tree_summary(groups, 'polar_basis', orders)
    function = tree_summary(groups, 'function_basis', orders)

    best_order = orders[function['best_order']]
    out = {
        'position': POS,
        'raw_e0_sectors': raw,
        'support_groups': n,
        'degree2_ambient_coordinates': 1 + DOMAIN_BITS + PAIR_BITS,
        'linear_global_rank': linear['global_rank'],
        'scalar_polynomial_global_rank': scalar['global_rank'],
        'polar_global_rank': polar['global_rank'],
        'combined_function_global_rank': function['global_rank'],
        'linear_tree': linear,
        'scalar_tree': scalar,
        'polar_tree': polar,
        'combined_function_tree': function,
        'combined_function_best_balanced_cut': balanced_cut(
            groups, 'function_basis', best_order
        ),
        'scalar_best_balanced_cut_under_function_order': balanced_cut(
            groups, 'scalar_basis', best_order
        ),
        'linear_best_balanced_cut_under_function_order': balanced_cut(
            groups, 'linear_basis', best_order
        ),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_QUADRATIC_FUNCTION_SPACE_SEPARATOR')
    print('scope=exact GF2 function-span intersection diagnostic over degree<=2 ANF coordinates for each C aggregate grouped-e0 linear signature plus its aggregate right-only scalar polynomial')
    print('important=lambda_F is exact for the displayed function spaces, but is not by itself an exact contraction-state theorem because evaluation tuples can obey nonlinear compatibility constraints')
    print('decision=compare combined function-space width with linear-refinement width147 and hybrid-linear width83; use the result to choose cut-local nonlinear representation')
    print('not_included=aggregate e0 carry, exact nonlinear message count, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


def main():
    analyze()


if __name__ == '__main__':
    main()
