#!/usr/bin/env python3
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_local_group_separator as P

DOMAIN_BITS = P.DOMAIN_BITS


def build_groups(pos):
    e0, _e1, _half = P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = P.U.H.support_for(pos, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))

    expected_raw = 581 if pos == 'B' else 577
    expected_groups = 251 if pos == 'B' else 250
    assert raw == expected_raw
    assert len(grouped) == expected_groups

    groups = []
    for group_id, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        groups.append(P.local_group(pos, can, sectors, group_id))

    assert P.union_rank(groups, 'combined_basis') == DOMAIN_BITS
    return groups


class RankOracle:
    def __init__(self, groups):
        self.groups = groups
        self.all_indices = frozenset(range(len(groups)))
        self.rank_cache = {frozenset(): 0, self.all_indices: DOMAIN_BITS}
        self.lambda_cache = {frozenset(): 0, self.all_indices: 0}

    def rank(self, subset):
        key = frozenset(subset)
        if key not in self.rank_cache:
            self.rank_cache[key] = P.union_rank(
                self.groups, 'combined_basis', sorted(key)
            )
        return self.rank_cache[key]

    def stats(self, subset):
        key = frozenset(subset)
        comp = self.all_indices - key
        r = self.rank(key)
        cr = self.rank(comp)
        lam = r + cr - DOMAIN_BITS
        assert 0 <= lam <= DOMAIN_BITS
        self.lambda_cache[key] = lam
        return r, cr, lam


def candidate_splits(lo, hi):
    n = hi - lo
    assert n >= 2
    if n <= 4:
        return [lo + n // 2]

    # Keep the tree reasonably balanced while still allowing the exact rank
    # oracle to exploit asymmetric separators. These are search candidates;
    # the final tree is independently reverified edge by edge.
    offsets = {
        n // 3,
        (2 * n) // 5,
        n // 2,
        (3 * n) // 5,
        (2 * n) // 3,
    }
    return sorted(lo + x for x in offsets if 0 < x < n)


def cluster_digest(indices):
    payload = ','.join(str(i) for i in sorted(indices)).encode()
    return hashlib.sha256(payload).hexdigest()[:16]


def build_tree(groups, order, oracle, lo=0, hi=None, depth=0):
    if hi is None:
        hi = len(order)
    indices = frozenset(order[lo:hi])
    r, cr, lam = oracle.stats(indices)
    node = {
        'lo': lo,
        'hi': hi,
        'size': hi - lo,
        'rank': r,
        'complement_rank': cr,
        'lambda': lam,
        'cluster_digest': cluster_digest(indices),
    }
    if hi - lo == 1:
        node['leaf_group'] = order[lo]
        return node

    choices = []
    for split in candidate_splits(lo, hi):
        left = frozenset(order[lo:split])
        right = frozenset(order[split:hi])
        _lr, _lcr, llam = oracle.stats(left)
        _rr, _rcr, rlam = oracle.stats(right)
        # Immediate separator objective, then total child lambda, then balance.
        choices.append(
            (
                max(llam, rlam),
                llam + rlam,
                abs((split - lo) - (hi - split)),
                split,
                llam,
                rlam,
            )
        )
    choices.sort()
    _, _, _, split, left_lam, right_lam = choices[0]
    node['split'] = split
    node['search_child_lambdas'] = [left_lam, right_lam]
    node['left'] = build_tree(groups, order, oracle, lo, split, depth + 1)
    node['right'] = build_tree(groups, order, oracle, split, hi, depth + 1)
    return node


def verify_tree(tree, order, oracle):
    seen = []
    widths = []
    depths = []
    internal = 0

    def walk(node, depth):
        nonlocal internal
        lo, hi = node['lo'], node['hi']
        assert node['size'] == hi - lo
        indices = frozenset(order[lo:hi])
        r, cr, lam = oracle.stats(indices)
        assert node['rank'] == r
        assert node['complement_rank'] == cr
        assert node['lambda'] == lam
        assert node['cluster_digest'] == cluster_digest(indices)
        if not (lo == 0 and hi == len(order)):
            widths.append(lam)
        depths.append(depth)

        if hi - lo == 1:
            assert node['leaf_group'] == order[lo]
            seen.append(node['leaf_group'])
            return

        internal += 1
        split = node['split']
        assert lo < split < hi
        assert node['left']['lo'] == lo and node['left']['hi'] == split
        assert node['right']['lo'] == split and node['right']['hi'] == hi
        walk(node['left'], depth + 1)
        walk(node['right'], depth + 1)

    walk(tree, 0)
    assert sorted(seen) == list(range(len(order)))
    assert len(seen) == len(set(seen)) == len(order)
    assert internal == len(order) - 1
    return {
        'width': max(widths) if widths else 0,
        'max_depth': max(depths),
        'leaves': len(seen),
        'internal_nodes': internal,
    }


def worst_nodes(tree, limit=12):
    nodes = []

    def walk(node):
        if node['size'] != 1 and not (node['lo'] == 0 and node['hi'] - node['lo'] == node.get('root_size', -1)):
            pass
        nodes.append(
            {
                'lo': node['lo'],
                'hi': node['hi'],
                'size': node['size'],
                'rank': node['rank'],
                'complement_rank': node['complement_rank'],
                'lambda': node['lambda'],
                'cluster_digest': node['cluster_digest'],
            }
        )
        if 'left' in node:
            walk(node['left'])
            walk(node['right'])

    walk(tree)
    # Root has lambda 0 and cannot contaminate the top of this ranking.
    nodes.sort(key=lambda x: (-x['lambda'], -x['size'], x['lo'], x['hi']))
    return nodes[:limit]


def analyze(pos):
    groups = build_groups(pos)
    n = len(groups)
    orderings = {
        'local_rank_ascending': sorted(
            range(n), key=lambda i: (groups[i]['combined_rank'], groups[i]['multiplicity'], i)
        ),
        'local_rank_descending': sorted(
            range(n), key=lambda i: (-groups[i]['combined_rank'], groups[i]['multiplicity'], i)
        ),
        'multiplicity_then_rank': sorted(
            range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['combined_rank'], i)
        ),
    }

    candidates = {}
    for name, order in orderings.items():
        oracle = RankOracle(groups)
        tree = build_tree(groups, order, oracle)
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
            'worst_nodes': worst_nodes(tree),
            'rank_oracle_cache_entries': len(oracle.rank_cache),
        }

    best_name, best = min(
        candidates.items(),
        key=lambda kv: (
            kv[1]['certificate']['width'],
            kv[1]['certificate']['max_depth'],
            kv[0],
        ),
    )
    out = {
        'position': pos,
        'groups': n,
        'domain_bits': DOMAIN_BITS,
        'candidates': candidates,
        'best_order': best_name,
        'best_width': best['certificate']['width'],
        'best_depth': best['certificate']['max_depth'],
        'best_root_children': best['root_children'],
        'best_worst_nodes': best['worst_nodes'],
    }
    print(json.dumps(out, sort_keys=True), flush=True)
    return out


def main():
    out = {pos: analyze(pos) for pos in 'BC'}
    print('result_summary', json.dumps({
        pos: {
            'best_order': out[pos]['best_order'],
            'best_width': out[pos]['best_width'],
            'best_depth': out[pos]['best_depth'],
            'best_root_children': out[pos]['best_root_children'],
            'candidate_widths': {
                name: data['certificate']['width']
                for name, data in out[pos]['candidates'].items()
            },
        }
        for pos in 'BC'
    }, sort_keys=True))
    print('PASS V26_Q138_BC_E0_RECURSIVE_SEPARATOR_TREE')
    print('scope=deterministic exact GF2 recursive contraction-tree certificates for the PR112 local linear signature family')
    print('claim=every internal cluster edge is independently re-ranked against its global complement; reported tree widths are exact upper bounds for the displayed trees, not optimal branchwidth claims')
    print('not_included=quadratic scalar phase, grouped-e0 carry values, e0-half cross-carry, complete B2/C2, W_repr, alpha, arithmetic-work, ranking/search, full-round')


if __name__ == '__main__':
    main()
