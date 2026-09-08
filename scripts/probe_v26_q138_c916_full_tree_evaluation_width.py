#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_aggregate_signature_separator as A
import probe_v26_q138_c916_quadratic_function_space_separator as F
import probe_v26_q138_c916_quadratic_residual_separator as R
import probe_v26_q138_c916_worst_cut_origin_fiber_residual_image as O

DOMAIN_BITS = F.DOMAIN_BITS
PAIR_BITS = F.PAIR_BITS
LINEAR_MASK = (1 << DOMAIN_BITS) - 1
QUAD_MASK = (1 << PAIR_BITS) - 1
assert DOMAIN_BITS == 149


def flatten_matrix(rows, width):
    z = 0
    for i, row in enumerate(rows):
        assert row >> width == 0
        z |= row << (i * width)
    return z


def functional_on_kernel(polar_rows, x, kernel):
    p = O.polar_apply(polar_rows, x)
    row = 0
    for j, k in enumerate(kernel):
        if (p & k).bit_count() & 1:
            row |= 1 << j
    return row


def analyze_edge(indices, all_indices, oracles, affine_basis):
    comp = all_indices - indices
    J = R.intersection_basis(
        oracles['function'].basis(indices),
        oracles['function'].basis(comp),
    )
    JA = R.intersection_basis(J, affine_basis)
    residual = O.quadratic_quotient_basis(J)
    assert len(residual) == len(J) - len(JA)

    affine_rows = A.L.basis((v >> PAIR_BITS) & LINEAR_MASK for v in JA)
    affine_rank = len(affine_rows)
    constant_in_shared = len(A.L.basis(JA + [R.CONST_BIT])) == len(JA)
    assert len(JA) - affine_rank in (0, 1)
    assert constant_in_shared == (len(JA) - affine_rank == 1)

    rdim = len(residual)
    naive_evaluation_bits = affine_rank + rdim
    kernel = O.nullspace_basis(affine_rows, DOMAIN_BITS)
    assert len(kernel) == DOMAIN_BITS - affine_rank

    st = {
        'function_lambda': len(J),
        'shared_affine_dim': len(JA),
        'shared_affine_linear_rank': affine_rank,
        'constant_in_shared_affine_space': constant_in_shared,
        'fiber_kernel_dim': len(kernel),
        'quadratic_residual_dim': rdim,
        'naive_evaluation_bits': naive_evaluation_bits,
        'fiber_affine_residual': True,
        'restricted_polar_nonzero_basis_count': 0,
        'common_kernel_dual_row_span_rank': 0,
        'translation_matrix_control_rank': 0,
        'residual_rank_upper_bound': 0,
        'safe_evaluation_bits': affine_rank,
        'improvement_vs_naive_bits': rdim,
    }

    if rdim == 0:
        return st

    restricted = [O.restrict_poly(v, kernel) for v in residual]
    nonzero_polar = sum(any(row != 0 for row in rrows) for rrows, _lin, _c in restricted)
    st['restricted_polar_nonzero_basis_count'] = nonzero_polar

    if nonzero_polar:
        # The residual map remains genuinely quadratic on this affine kernel.
        # Keep the safe r-bit residual envelope for now; later probes target
        # only the edges that dominate after the fiber-affine improvements.
        st['fiber_affine_residual'] = False
        st['common_kernel_dual_row_span_rank'] = None
        st['translation_matrix_control_rank'] = None
        st['residual_rank_upper_bound'] = rdim
        st['safe_evaluation_bits'] = naive_evaluation_bits
        st['improvement_vs_naive_bits'] = 0
        return st

    origin_rows = [lin for _rrows, lin, _c in restricted]
    full_polars = [
        O.G.rows_from_pair_mask(DOMAIN_BITS, v & QUAD_MASK)
        for v in residual
    ]

    effect_rows = []
    effect_matrices = []
    kdim = len(kernel)
    for s in range(DOMAIN_BITS):
        x = 1 << s
        rows = [
            functional_on_kernel(full_polars[i], x, kernel)
            for i in range(rdim)
        ]
        effect_rows.extend(rows)
        effect_matrices.append(flatten_matrix(rows, kdim))

    # Because every residual polar vanishes on K x K, translation by a
    # kernel vector must leave the residual linear map on K unchanged.
    for k in kernel:
        for i in range(rdim):
            assert functional_on_kernel(full_polars[i], k, kernel) == 0

    common_rank = A.L.rank(origin_rows + effect_rows)
    control_rank = A.L.rank(effect_matrices)
    residual_rank_upper = min(rdim, common_rank)
    safe_bits = affine_rank + residual_rank_upper

    st['common_kernel_dual_row_span_rank'] = common_rank
    st['translation_matrix_control_rank'] = control_rank
    st['residual_rank_upper_bound'] = residual_rank_upper
    st['safe_evaluation_bits'] = safe_bits
    st['improvement_vs_naive_bits'] = naive_evaluation_bits - safe_bits
    return st


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
        'function': R.BasisOracle(groups, 'function_basis'),
        'linear': R.BasisOracle(groups, 'linear_basis'),
    }
    linear_all = oracles['linear'].basis(all_indices)
    assert len(linear_all) == DOMAIN_BITS
    affine_basis = A.L.basis(linear_all + [R.CONST_BIT])

    stats = []

    def walk(node):
        lo, hi = node['lo'], node['hi']
        if not (lo == 0 and hi == n):
            idx = frozenset(order[lo:hi])
            st = analyze_edge(idx, all_indices, oracles, affine_basis)
            st.update({
                'lo': lo,
                'hi': hi,
                'size': hi - lo,
                'lambda_from_tree': node['lambda'],
            })
            assert st['function_lambda'] == node['lambda']
            stats.append(st)
        if 'left' in node:
            walk(node['left'])
            walk(node['right'])

    walk(tree)
    assert len(stats) == 2 * n - 2 == 498

    max_function = max(s['function_lambda'] for s in stats)
    max_naive = max(s['naive_evaluation_bits'] for s in stats)
    max_safe = max(s['safe_evaluation_bits'] for s in stats)
    max_improvement = max(s['improvement_vs_naive_bits'] for s in stats)
    assert max_function == 70

    residual_zero_edges = sum(s['quadratic_residual_dim'] == 0 for s in stats)
    fiber_affine_edges = sum(s['fiber_affine_residual'] for s in stats)
    fiber_quadratic_edges = len(stats) - fiber_affine_edges

    safe_hist = Counter(s['safe_evaluation_bits'] for s in stats)
    naive_hist = Counter(s['naive_evaluation_bits'] for s in stats)
    residual_hist = Counter(s['quadratic_residual_dim'] for s in stats)

    worst_safe = sorted(
        stats,
        key=lambda s: (
            -s['safe_evaluation_bits'],
            -s['naive_evaluation_bits'],
            -s['quadratic_residual_dim'],
            -s['size'],
            s['lo'],
        ),
    )[:20]

    worst_naive = sorted(
        stats,
        key=lambda s: (
            -s['naive_evaluation_bits'],
            -s['function_lambda'],
            -s['size'],
            s['lo'],
        ),
    )[:12]

    improved_edges = sorted(
        (s for s in stats if s['improvement_vs_naive_bits'] > 0),
        key=lambda s: (
            -s['improvement_vs_naive_bits'],
            -s['naive_evaluation_bits'],
            s['lo'],
        ),
    )[:20]

    target = [s for s in stats if s['lo'] == 110 and s['hi'] == 166]
    assert len(target) == 1
    target = target[0]
    assert target['function_lambda'] == 70
    assert target['shared_affine_linear_rank'] == 56
    assert target['quadratic_residual_dim'] == 13
    assert target['fiber_affine_residual'] is True
    assert target['common_kernel_dual_row_span_rank'] == 4
    assert target['translation_matrix_control_rank'] == 4
    assert target['safe_evaluation_bits'] == 60

    out = {
        'position': 'C',
        'support_groups': n,
        'tree_edges_analyzed': len(stats),
        'function_space_tree_width': cert['width'],
        'function_space_tree_depth': cert['max_depth'],
        'max_function_lambda': max_function,
        'max_naive_evaluation_bits': max_naive,
        'safe_full_tree_evaluation_width_upper_bound': max_safe,
        'max_edge_improvement_bits': max_improvement,
        'residual_zero_edges': residual_zero_edges,
        'fiber_affine_residual_edges': fiber_affine_edges,
        'fiber_quadratic_residual_edges': fiber_quadratic_edges,
        'naive_evaluation_bit_histogram': dict(sorted(naive_hist.items())),
        'safe_evaluation_bit_histogram': dict(sorted(safe_hist.items())),
        'quadratic_residual_dim_histogram': dict(sorted(residual_hist.items())),
        'unique_former_width70_edge': target,
        'worst_safe_edges': worst_safe,
        'worst_naive_edges': worst_naive,
        'largest_improvement_edges': improved_edges,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_FULL_TREE_EVALUATION_WIDTH')
    print('scope=safe edge-by-edge realizable-evaluation-state bit upper bound on all 498 non-root edges of the merged C916 function-space tree')
    print('method=fiber-affine residual edges use exact common K* translation-row span; fiber-quadratic residual edges retain the conservative residual-dimension envelope')
    print('important=this is a safe full-tree evaluation-width upper bound, not necessarily exact on edges whose residual remains quadratic on the affine kernel')
    print('next=target only the edges that attain the new safe width, using exact cut-restricted quadratic image methods where necessary')
    print('not_included=aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
