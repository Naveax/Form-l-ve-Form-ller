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


def flatten_rows(rows, width):
    z = 0
    for i, row in enumerate(rows):
        z |= int(row) << (i * width)
    return z


def unflatten_rows(z, nrows, width):
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


def label_of_x(rows, x):
    z = 0
    for i, row in enumerate(rows):
        if (row & x).bit_count() & 1:
            z |= 1 << i
    return z


def section_basis(affine_rows):
    piv = {}
    out = []
    for s in range(DOMAIN_BITS):
        lab = label_of_x(affine_rows, 1 << s)
        y = lab
        while y:
            p = y.bit_length() - 1
            if p not in piv:
                piv[p] = y
                out.append(1 << s)
                break
            y ^= piv[p]
    assert len(out) == len(affine_rows)
    assert A.L.rank(label_of_x(affine_rows, x) for x in out) == len(affine_rows)
    return out


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
    assert cert['width'] == 70

    oracles = {
        'function': R.BasisOracle(groups, 'function_basis'),
        'linear': R.BasisOracle(groups, 'linear_basis'),
    }
    linear_all = oracles['linear'].basis(all_indices)
    affine_basis = A.L.basis(linear_all + [R.CONST_BIT])

    idx = frozenset(order[55:110])
    comp = all_indices - idx
    J = R.intersection_basis(oracles['function'].basis(idx), oracles['function'].basis(comp))
    JA = R.intersection_basis(J, affine_basis)
    residual = O.quadratic_quotient_basis(J)
    assert len(J) == 64 and len(JA) == 52 and len(residual) == 12

    affine_rows = A.L.basis((v >> PAIR_BITS) & LINEAR_MASK for v in JA)
    assert len(affine_rows) == 52
    assert len(A.L.basis(JA + [R.CONST_BIT])) == len(JA) + 1
    kernel = O.nullspace_basis(affine_rows, DOMAIN_BITS)
    assert len(kernel) == 97

    restricted = [O.restrict_poly(v, kernel) for v in residual]
    affine_residual_indices = [
        i for i, (rrows, _lin, _c) in enumerate(restricted)
        if not any(rrows)
    ]
    quadratic_indices = [
        i for i, (rrows, _lin, _c) in enumerate(restricted)
        if any(rrows)
    ]
    assert len(affine_residual_indices) == 11
    assert len(quadratic_indices) == 1
    qidx = quadratic_indices[0]

    qrows, _qlin, _qc = restricted[qidx]
    polar_rank = A.L.rank(qrows)
    radical_dim = len(kernel) - polar_rank
    assert polar_rank == 88
    assert radical_dim == 9
    max_totally_isotropic_dim = radical_dim + polar_rank // 2
    assert max_totally_isotropic_dim == 53
    min_L_kernel_dim = len(kernel) - len(affine_residual_indices)
    assert min_L_kernel_dim == 86
    assert min_L_kernel_dim > max_totally_isotropic_dim

    origin_L = [restricted[i][1] for i in affine_residual_indices]
    origin_L_rank = A.L.rank(origin_L)
    assert origin_L_rank == 7

    full_polars = [
        O.G.rows_from_pair_mask(DOMAIN_BITS, residual[i] & QUAD_MASK)
        for i in affine_residual_indices
    ]
    section = section_basis(affine_rows)
    assert len(section) == 52

    effect_rows = []
    effect_matrices = []
    for x in section:
        rows = [
            P.functional_on_kernel(full_polars[j], x, kernel)
            for j in range(len(affine_residual_indices))
        ]
        effect_rows.extend(rows)
        effect_matrices.append(flatten_rows(rows, len(kernel)))

    common_row_rank = A.L.rank(origin_L + effect_rows)
    control_basis = A.L.basis(effect_matrices)
    control_rank = len(control_basis)

    assert control_rank <= 16, control_rank
    hist = Counter()
    image_size_sum = 0
    for mask in range(1 << control_rank):
        effect = xor_subset(control_basis, mask)
        erows = unflatten_rows(effect, len(origin_L), len(kernel))
        Lrows = [origin_L[i] ^ erows[i] for i in range(len(origin_L))]
        r = A.L.rank(Lrows)
        hist[r] += 1
        # The L-fiber kernel has dimension >=86, while any totally isotropic
        # subspace for the fixed rank-88 polar form has dimension <=53.
        # Hence q is nonconstant on every L fiber and doubles every L image.
        image_size_sum += 1 << (r + 1)

    labels_per_control_state = 1 << (len(affine_rows) - control_rank)
    exact_states = labels_per_control_state * image_size_sum
    max_L_rank = max(hist)
    max_residual_image_bits = max_L_rank + 1
    max_residual_image_size = 1 << max_residual_image_bits

    out = {
        'position': 'C',
        'edge': {'lo': 55, 'hi': 110, 'size': 55},
        'function_lambda': len(J),
        'shared_affine_linear_rank': len(affine_rows),
        'fiber_kernel_dim': len(kernel),
        'quadratic_residual_dim': len(residual),
        'affine_residual_coordinate_count': len(affine_residual_indices),
        'quadratic_residual_coordinate_count': 1,
        'fixed_restricted_quadratic_polar_rank': polar_rank,
        'fixed_restricted_quadratic_radical_dim': radical_dim,
        'max_totally_isotropic_dim': max_totally_isotropic_dim,
        'minimum_affine_residual_fiber_kernel_dim': min_L_kernel_dim,
        'origin_affine_residual_rank': origin_L_rank,
        'common_affine_residual_kernel_dual_row_span_rank': common_row_rank,
        'translation_affine_residual_matrix_control_rank': control_rank,
        'translation_control_states': 1 << control_rank,
        'affine_labels_per_control_state': labels_per_control_state,
        'control_state_affine_residual_rank_histogram': dict(sorted(hist.items())),
        'max_affine_residual_rank_all_fibers': max_L_rank,
        'max_residual_image_size_all_fibers': max_residual_image_size,
        'max_residual_image_bits_all_fibers': max_residual_image_bits,
        'exact_shared_evaluation_state_count': exact_states,
        'exact_shared_evaluation_state_ceiling_bits': ceil_log2(exact_states),
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_WIDTH64_QUADRATIC_EDGE_ALL_FIBER_IMAGE')
    print('scope=exact all-affine-fiber residual image-size geometry for the C916 fiber-quadratic edge [55,110)')
    print('method=split the 12 residual outputs into 11 affine-on-K coordinates plus one fixed rank-88 quadratic coordinate; enumerate the exact translation-matrix control image for the affine coordinates; the quadratic coordinate doubles every affine-coordinate fiber because its polar cannot vanish on an >=86-dimensional subspace')
    print('important=exact tuple count for this edge does not by itself change the already-certified full-tree width65, whose unique worst edge is [166,199)')
    print('not_included=tree reoptimization, aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
