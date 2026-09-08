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
assert DOMAIN_BITS == 149


def flatten_rows(rows, width):
    z = 0
    for i, row in enumerate(rows):
        z |= int(row) << (i * width)
    return z


def ceil_log2(n):
    assert n > 0
    return (n - 1).bit_length()


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

    target = None
    def walk(node):
        nonlocal target
        if (node['lo'], node['hi']) == (55, 110):
            assert target is None
            target = node
        if 'left' in node:
            walk(node['left'])
            walk(node['right'])
    walk(tree)
    assert target is not None
    assert target['lambda'] == 64 and target['size'] == 55

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

    assert len(J) == 64
    assert len(JA) == 52
    assert len(residual) == 12

    affine_rows = A.L.basis((v >> PAIR_BITS) & LINEAR_MASK for v in JA)
    affine_rank = len(affine_rows)
    constant_in_shared = len(A.L.basis(JA + [R.CONST_BIT])) == len(JA)
    assert affine_rank == 52
    assert not constant_in_shared

    kernel = O.nullspace_basis(affine_rows, DOMAIN_BITS)
    assert len(kernel) == 97

    restricted = [O.restrict_poly(v, kernel) for v in residual]
    restricted_nonzero_polar_basis = sum(
        any(row != 0 for row in rrows)
        for rrows, _lin, _c in restricted
    )
    polar_vectors = [
        flatten_rows(rrows, len(kernel))
        for rrows, _lin, _c in restricted
        if any(row != 0 for row in rrows)
    ]
    restricted_polar_space_rank = A.L.rank(polar_vectors)
    assert restricted_nonzero_polar_basis == 1
    assert restricted_polar_space_rank == 1

    qdim = len(restricted)
    total_chars = 1 << qdim
    spectrum = [0] * total_chars
    polar_rank_hist = Counter()
    nonzero_log_hist = Counter()
    zero_chars = 0

    cur_rows = [0] * len(kernel)
    cur_lin = 0
    cur_c = 0
    prev_gray = 0
    for i in range(total_chars):
        gray = i ^ (i >> 1)
        if i:
            d = gray ^ prev_gray
            bit = (d & -d).bit_length() - 1
            br, bl, bc = restricted[bit]
            for j in range(len(kernel)):
                cur_rows[j] ^= br[j]
            cur_lin ^= bl
            cur_c ^= bc
        got = O.G.quadratic_gauss_sum(cur_rows, cur_lin, cur_c, len(kernel))
        spectrum[gray] = got['sum']
        polar_rank_hist[got['polar_rank']] += 1
        if got['sum'] == 0:
            zero_chars += 1
        else:
            nonzero_log_hist[got['log2_abs']] += 1
        prev_gray = gray

    assert spectrum[0] == 1 << len(kernel)
    counts = O.inverse_walsh_counts(spectrum)
    assert sum(counts) == 1 << len(kernel)
    image = [i for i, c in enumerate(counts) if c]
    missing = [i for i, c in enumerate(counts) if not c]
    nz = [counts[i] for i in image]

    out = {
        'position': 'C',
        'edge': {'lo': 55, 'hi': 110, 'size': 55},
        'function_lambda': len(J),
        'shared_affine_function_dim': len(JA),
        'shared_affine_linear_rank': affine_rank,
        'constant_in_shared_affine_space': constant_in_shared,
        'origin_fiber_kernel_dim': len(kernel),
        'quadratic_residual_dim': qdim,
        'restricted_nonzero_polar_basis_count': restricted_nonzero_polar_basis,
        'restricted_polar_space_rank': restricted_polar_space_rank,
        'characters_evaluated': total_chars,
        'zero_gauss_characters': zero_chars,
        'nonzero_gauss_characters': total_chars - zero_chars,
        'restricted_polar_rank_histogram': dict(sorted(polar_rank_hist.items())),
        'nonzero_gauss_log2_abs_histogram': dict(sorted(nonzero_log_hist.items())),
        'origin_fiber_residual_image_size': len(image),
        'origin_fiber_residual_image_ceiling_bits': ceil_log2(len(image)),
        'origin_fiber_missing_outputs': len(missing),
        'origin_fiber_distinct_preimage_counts': len(set(nz)),
        'origin_fiber_min_nonzero_preimages': min(nz),
        'origin_fiber_max_preimages': max(nz),
        'first_missing_output_masks': missing[:16],
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_WIDTH64_QUADRATIC_EDGE_ORIGIN_IMAGE')
    print('scope=exact residual evaluation image on the x=0 shared-affine fiber of the 64-bit fiber-quadratic edge [55,110)')
    print('method=restrict 12 residual degree<=2 functions to the 97-dimensional affine kernel; evaluate all 4096 Fourier characters with exact quadratic Gauss elimination; invert the Walsh spectrum exactly')
    print('important=this is one affine fiber only; do not promote it to an all-fiber or full-tree width theorem without a separate translation/fiber argument')
    print('not_included=all-fiber image, aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
