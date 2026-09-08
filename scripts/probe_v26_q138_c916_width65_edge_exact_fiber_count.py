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
import probe_v26_q138_c916_full_tree_evaluation_width as P

DOMAIN_BITS = F.DOMAIN_BITS
PAIR_BITS = F.PAIR_BITS
LINEAR_MASK = (1 << DOMAIN_BITS) - 1
QUAD_MASK = (1 << PAIR_BITS) - 1
assert DOMAIN_BITS == 149


def unflatten_matrix(z, nrows, width):
    mask = (1 << width) - 1
    return [(z >> (i * width)) & mask for i in range(nrows)]


def xor_subset(items, mask):
    z = 0
    x = mask
    while x:
        b = x & -x
        z ^= items[b.bit_length() - 1]
        x ^= b
    return z


def ceil_log2(n):
    assert n > 0
    return (n - 1).bit_length()


def analyze():
    base = P.analyze()
    assert base['safe_full_tree_evaluation_width_upper_bound'] == 65
    safe_hist = base['safe_evaluation_bit_histogram']
    assert safe_hist[65] == 1
    other_max = max(k for k, count in safe_hist.items() if k != 65 and count)
    assert other_max == 64

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
    assert cert['width'] == 70

    oracles = {
        'function': R.BasisOracle(groups, 'function_basis'),
        'linear': R.BasisOracle(groups, 'linear_basis'),
    }
    linear_all = oracles['linear'].basis(all_indices)
    affine_basis = A.L.basis(linear_all + [R.CONST_BIT])

    lo, hi = 166, 199
    idx = frozenset(order[lo:hi])
    comp = all_indices - idx
    J = R.intersection_basis(oracles['function'].basis(idx), oracles['function'].basis(comp))
    JA = R.intersection_basis(J, affine_basis)
    residual = O.quadratic_quotient_basis(J)
    assert len(J) == 68
    assert len(JA) == 63
    assert len(residual) == 5

    affine_rows = A.L.basis((v >> PAIR_BITS) & LINEAR_MASK for v in JA)
    affine_rank = len(affine_rows)
    assert affine_rank == 62
    assert len(A.L.basis(JA + [R.CONST_BIT])) == len(JA)
    kernel = O.nullspace_basis(affine_rows, DOMAIN_BITS)
    assert len(kernel) == 87

    restricted = [O.restrict_poly(v, kernel) for v in residual]
    assert all(all(row == 0 for row in rrows) for rrows, _lin, _c in restricted)
    origin_rows = [lin for _rrows, lin, _c in restricted]
    full_polars = [
        O.G.rows_from_pair_mask(DOMAIN_BITS, v & QUAD_MASK)
        for v in residual
    ]

    effect_rows = []
    effect_matrices = []
    for s in range(DOMAIN_BITS):
        x = 1 << s
        rows = [
            P.functional_on_kernel(full_polars[i], x, kernel)
            for i in range(len(residual))
        ]
        effect_rows.extend(rows)
        effect_matrices.append(P.flatten_matrix(rows, len(kernel)))

    for k in kernel:
        for i in range(len(residual)):
            assert P.functional_on_kernel(full_polars[i], k, kernel) == 0

    common_rank = A.L.rank(origin_rows + effect_rows)
    control_basis = A.L.basis(effect_matrices)
    control_rank = len(control_basis)
    assert common_rank == 3
    assert control_rank == 3

    hist = Counter()
    image_size_sum = 0
    for mask in range(1 << control_rank):
        flat = xor_subset(control_basis, mask)
        erows = unflatten_matrix(flat, len(residual), len(kernel))
        rows = [origin_rows[i] ^ erows[i] for i in range(len(residual))]
        r = A.L.rank(rows)
        hist[r] += 1
        image_size_sum += 1 << r

    labels_per_control = 1 << (affine_rank - control_rank)
    exact_states = labels_per_control * image_size_sum
    exact_ceiling = ceil_log2(exact_states)
    refined_full_tree = max(other_max, exact_ceiling)

    out = {
        'position': 'C',
        'edge': {'lo': lo, 'hi': hi, 'size': hi-lo},
        'function_lambda': len(J),
        'shared_affine_function_dim': len(JA),
        'varying_affine_label_rank': affine_rank,
        'fiber_kernel_dim': len(kernel),
        'quadratic_residual_dim': len(residual),
        'common_kernel_dual_row_span_rank': common_rank,
        'translation_matrix_control_rank': control_rank,
        'translation_matrix_control_states': 1 << control_rank,
        'fiber_labels_per_control_state': labels_per_control,
        'control_state_residual_rank_histogram': dict(sorted(hist.items())),
        'exact_shared_evaluation_state_count': exact_states,
        'exact_shared_evaluation_state_ceiling_bits': exact_ceiling,
        'previous_safe_full_tree_width': base['safe_full_tree_evaluation_width_upper_bound'],
        'max_other_edge_safe_bits': other_max,
        'refined_safe_full_tree_evaluation_width_upper_bound': refined_full_tree,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_WIDTH65_EDGE_EXACT_FIBER_COUNT')
    print('scope=exact all-fiber evaluation tuple count for the unique edge attaining the 65-bit safe full-tree bound')
    print('method=enumerate the exact 3-dimensional translation-matrix image; each of its 8 states represents 2^59 affine labels')
    print('important=combine this exact edge ceiling with the independently certified <=64 upper bound on every other edge')
    print('not_included=exact images on fiber-quadratic edges, aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
