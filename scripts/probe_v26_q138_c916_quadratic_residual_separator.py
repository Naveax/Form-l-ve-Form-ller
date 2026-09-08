#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_aggregate_signature_separator as A
import probe_v26_q138_c916_quadratic_function_space_separator as F

POS = 'C'
DOMAIN_BITS = F.DOMAIN_BITS
PAIR_BITS = F.PAIR_BITS
QUAD_MASK = (1 << PAIR_BITS) - 1
CONST_BIT = 1 << (PAIR_BITS + DOMAIN_BITS)


def xor_selected(items, mask):
    z = 0
    x = mask
    while x:
        b = x & -x
        z ^= items[b.bit_length() - 1]
        x ^= b
    return z


def intersection_basis(a_rows, b_rows):
    A0 = A.L.basis(a_rows)
    B0 = A.L.basis(b_rows)
    na = len(A0)
    rows = A0 + B0
    piv = {}
    out = {}

    for idx, v in enumerate(rows):
        row = v
        tag = 1 << idx
        while row:
            p = row.bit_length() - 1
            if p not in piv:
                piv[p] = (row, tag)
                break
            pr, pt = piv[p]
            row ^= pr
            tag ^= pt
        if row == 0:
            am = tag & ((1 << na) - 1)
            bm = tag >> na
            assert am and bm
            xa = xor_selected(A0, am)
            xb = xor_selected(B0, bm)
            assert xa == xb and xa != 0
            A.L.insert(out, xa)

    expected = len(A0) + len(B0) - len(A.L.basis(rows))
    assert len(out) == expected, (len(out), expected)
    return list(out.values())


class BasisOracle:
    def __init__(self, groups, key):
        self.groups = groups
        self.key = key
        self.all_indices = frozenset(range(len(groups)))
        self.cache = {frozenset(): []}

    def basis(self, subset):
        key = frozenset(subset)
        if key not in self.cache:
            rows = []
            for i in sorted(key):
                rows.extend(self.groups[i][self.key])
            self.cache[key] = A.L.basis(rows)
        return self.cache[key]

    def rank(self, subset):
        return len(self.basis(subset))


def analyze_edge(indices, all_indices, oracles, affine_basis):
    comp = all_indices - indices
    FL = oracles['function'].basis(indices)
    FR = oracles['function'].basis(comp)
    J = intersection_basis(FL, FR)
    lambda_f = len(J)

    JA = intersection_basis(J, affine_basis)
    shared_affine = len(JA)
    quad_projection = A.L.basis(v & QUAD_MASK for v in J)
    quadratic_residual = len(quad_projection)
    assert quadratic_residual == lambda_f - shared_affine

    LL = oracles['linear'].basis(indices)
    LR = oracles['linear'].basis(comp)
    direct_linear = len(intersection_basis(LL, LR))

    def lam(key, global_rank):
        r = oracles[key].rank(indices)
        cr = oracles[key].rank(comp)
        return r + cr - global_rank

    scalar_lambda = lam('scalar', oracles['scalar'].rank(all_indices))
    polar_lambda = lam('polar', oracles['polar'].rank(all_indices))

    return {
        'size': len(indices),
        'complement_size': len(comp),
        'function_lambda': lambda_f,
        'shared_affine_dim': shared_affine,
        'direct_linear_lambda': direct_linear,
        'affine_from_scalar_combinations': shared_affine - direct_linear,
        'quadratic_residual_dim': quadratic_residual,
        'scalar_lambda': scalar_lambda,
        'polar_lambda': polar_lambda,
    }


def analyze():
    raw, groups = F.build_groups()
    assert raw == 577 and len(groups) == 250
    n = len(groups)
    all_indices = frozenset(range(n))

    order = sorted(
        range(n),
        key=lambda i: (groups[i]['multiplicity'], groups[i]['function_rank'], i),
    )
    foracle = F.RankOracle(groups, 'function_basis')
    tree = F.build_tree(order, foracle)
    cert = F.verify_tree(tree, order, foracle)
    assert cert['width'] == 70 and cert['max_depth'] == 10

    oracles = {
        'function': BasisOracle(groups, 'function_basis'),
        'linear': BasisOracle(groups, 'linear_basis'),
        'scalar': BasisOracle(groups, 'scalar_basis'),
        'polar': BasisOracle(groups, 'polar_basis'),
    }
    linear_all = oracles['linear'].basis(all_indices)
    assert len(linear_all) == DOMAIN_BITS
    affine_basis = A.L.basis(linear_all + [CONST_BIT])
    assert len(affine_basis) == DOMAIN_BITS + 1

    edge_stats = []

    def walk(node):
        lo, hi = node['lo'], node['hi']
        if not (lo == 0 and hi == n):
            idx = frozenset(order[lo:hi])
            st = analyze_edge(idx, all_indices, oracles, affine_basis)
            st.update({'lo': lo, 'hi': hi, 'lambda_from_tree': node['lambda']})
            assert st['function_lambda'] == node['lambda']
            edge_stats.append(st)
        if 'left' in node:
            walk(node['left'])
            walk(node['right'])

    walk(tree)
    assert len(edge_stats) == 2*n - 2

    max_quad = max(st['quadratic_residual_dim'] for st in edge_stats)
    max_affine_extra = max(st['affine_from_scalar_combinations'] for st in edge_stats)
    max_function = max(st['function_lambda'] for st in edge_stats)
    max_direct_linear = max(st['direct_linear_lambda'] for st in edge_stats)
    assert max_function == 70

    worst_function = sorted(
        edge_stats,
        key=lambda st: (
            -st['function_lambda'],
            -st['quadratic_residual_dim'],
            -st['size'],
            st['lo'],
        ),
    )[:12]
    worst_quadratic = sorted(
        edge_stats,
        key=lambda st: (
            -st['quadratic_residual_dim'],
            -st['function_lambda'],
            -st['size'],
            st['lo'],
        ),
    )[:12]

    root_children = []
    for child in (tree['left'], tree['right']):
        idx = frozenset(order[child['lo']:child['hi']])
        st = analyze_edge(idx, all_indices, oracles, affine_basis)
        st.update({'lo': child['lo'], 'hi': child['hi']})
        root_children.append(st)

    # Exact 125/125 cut in the same multiplicity/function order, even though it
    # is not necessarily an edge of the recursively chosen tree.
    half_idx = frozenset(order[:n//2])
    balanced = analyze_edge(half_idx, all_indices, oracles, affine_basis)

    quad_hist = {}
    for st in edge_stats:
        q = st['quadratic_residual_dim']
        quad_hist[q] = quad_hist.get(q, 0) + 1

    out = {
        'position': POS,
        'support_groups': n,
        'best_combined_function_tree_width': cert['width'],
        'best_combined_function_tree_depth': cert['max_depth'],
        'tree_edges_analyzed': len(edge_stats),
        'max_function_lambda': max_function,
        'max_direct_linear_lambda_on_function_tree': max_direct_linear,
        'max_quadratic_residual_dim': max_quad,
        'max_affine_from_scalar_combinations': max_affine_extra,
        'quadratic_residual_histogram': dict(sorted(quad_hist.items())),
        'root_children': root_children,
        'balanced_cut': balanced,
        'worst_function_edges': worst_function,
        'worst_quadratic_edges': worst_quadratic,
        'function_global_rank': oracles['function'].rank(all_indices),
        'linear_global_rank': oracles['linear'].rank(all_indices),
        'scalar_global_rank': oracles['scalar'].rank(all_indices),
        'polar_global_rank': oracles['polar'].rank(all_indices),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_QUADRATIC_RESIDUAL_SEPARATOR')
    print('scope=exact edge-by-edge decomposition of the best C quadratic function-space tree intersection into affine shared functions and genuinely quadratic residual functions')
    print('important=quadratic residual dimension is exact in degree<=2 function space; it is not yet an exact realizable nonlinear message-count theorem')
    print('next=if max quadratic residual is small, compute exact or bounded evaluation-image sizes conditioned on the ordinary linear separator coordinates using quadratic Gauss-sum machinery')
    print('not_included=aggregate e0 carry, exact nonlinear message count, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


def main():
    analyze()


if __name__ == '__main__':
    main()
