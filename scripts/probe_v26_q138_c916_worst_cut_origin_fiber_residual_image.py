#!/usr/bin/env python3
import json
import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_aggregate_signature_separator as A
import probe_v26_q138_c916_quadratic_function_space_separator as F
import probe_v26_q138_c916_quadratic_residual_separator as R
import probe_v26_q138_c916_aggregate_scalar_gauss_classes as G

DOMAIN_BITS = F.DOMAIN_BITS
PAIR_BITS = F.PAIR_BITS
QUAD_MASK = (1 << PAIR_BITS) - 1
LINEAR_MASK = (1 << DOMAIN_BITS) - 1
CONST_SHIFT = PAIR_BITS + DOMAIN_BITS
assert DOMAIN_BITS == 149


def nullspace_basis(rows, n):
    piv = {}
    for x in A.L.basis(rows):
        y = x
        while y:
            p = y.bit_length() - 1
            if p in piv:
                y ^= piv[p]
            else:
                piv[p] = y
                break
    free = [i for i in range(n) if i not in piv]
    out = []
    for f in free:
        x = 1 << f
        for p in sorted(piv):
            if (piv[p] & x).bit_count() & 1:
                x |= 1 << p
        assert all(((r & x).bit_count() & 1) == 0 for r in rows)
        out.append(x)
    assert len(out) == n - len(piv)
    return out


def quadratic_quotient_basis(J):
    piv = {}
    out = []
    for v0 in J:
        v = v0
        q = v & QUAD_MASK
        while q:
            p = q.bit_length() - 1
            if p in piv:
                pq, pv = piv[p]
                q ^= pq
                v ^= pv
            else:
                piv[p] = (q, v)
                out.append(v)
                break
    assert len(A.L.basis(v & QUAD_MASK for v in out)) == len(out)
    return out


def polar_apply(rows, x):
    z = 0
    y = x
    while y:
        b = y & -y
        i = b.bit_length() - 1
        z ^= rows[i]
        y ^= b
    return z


def restrict_poly(poly, kernel):
    m = len(kernel)
    pair = poly & QUAD_MASK
    lin = (poly >> PAIR_BITS) & LINEAR_MASK
    c = (poly >> CONST_SHIFT) & 1
    rows = G.rows_from_pair_mask(DOMAIN_BITS, pair)

    rrows = [0] * m
    for a, ka in enumerate(kernel):
        pa = polar_apply(rows, ka)
        for b in range(a + 1, m):
            if (pa & kernel[b]).bit_count() & 1:
                rrows[a] |= 1 << b
                rrows[b] |= 1 << a

    rlin = 0
    for a, ka in enumerate(kernel):
        if G.q_eval(rows, lin, c, ka) ^ c:
            rlin |= 1 << a
    return rrows, rlin, c


def inverse_walsh_counts(spectrum):
    a = list(spectrum)
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j] = x + y
                a[j + h] = x - y
        h *= 2
    for i, x in enumerate(a):
        assert x % n == 0
        a[i] = x // n
        assert a[i] >= 0
    return a


def analyze():
    raw, groups = F.build_groups()
    assert raw == 577 and len(groups) == 250
    n = len(groups)
    all_indices = frozenset(range(n))
    order = sorted(range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['function_rank'], i))

    foracle = F.RankOracle(groups, 'function_basis')
    tree = F.build_tree(order, foracle)
    cert = F.verify_tree(tree, order, foracle)
    assert cert['width'] == 70 and cert['max_depth'] == 10

    oracles = {
        'function': R.BasisOracle(groups, 'function_basis'),
        'linear': R.BasisOracle(groups, 'linear_basis'),
    }
    linear_all = oracles['linear'].basis(all_indices)
    affine_basis = A.L.basis(linear_all + [R.CONST_BIT])

    target = None
    def walk(node):
        nonlocal target
        lo, hi = node['lo'], node['hi']
        if not (lo == 0 and hi == n) and node['lambda'] == 70:
            assert target is None
            target = node
        if 'left' in node:
            walk(node['left'])
            walk(node['right'])
    walk(tree)
    assert target is not None
    assert (target['lo'], target['hi'], target['size']) == (110, 166, 56)

    idx = frozenset(order[target['lo']:target['hi']])
    comp = all_indices - idx
    J = R.intersection_basis(oracles['function'].basis(idx), oracles['function'].basis(comp))
    JA = R.intersection_basis(J, affine_basis)
    residual = quadratic_quotient_basis(J)
    assert len(J) == 70
    assert len(JA) == 57
    assert len(residual) == 13

    affine_linear_rows = A.L.basis((v >> PAIR_BITS) & LINEAR_MASK for v in JA)
    affine_linear_rank = len(affine_linear_rows)
    constant_in_shared = len(A.L.basis(JA + [R.CONST_BIT])) == len(JA)
    assert len(JA) - affine_linear_rank in (0, 1)
    assert constant_in_shared == (len(JA) - affine_linear_rank == 1)

    kernel = nullspace_basis(affine_linear_rows, DOMAIN_BITS)
    kernel_dim = len(kernel)
    assert kernel_dim == DOMAIN_BITS - affine_linear_rank

    restricted = [restrict_poly(v, kernel) for v in residual]
    qdim = len(restricted)
    total_chars = 1 << qdim
    spectrum = [0] * total_chars
    polar_rank_hist = Counter()
    nonzero_log_hist = Counter()
    zero_chars = 0

    cur_rows = [0] * kernel_dim
    cur_lin = 0
    cur_c = 0
    prev_gray = 0
    for i in range(total_chars):
        gray = i ^ (i >> 1)
        if i:
            d = gray ^ prev_gray
            bit = (d & -d).bit_length() - 1
            br, bl, bc = restricted[bit]
            for j in range(kernel_dim):
                cur_rows[j] ^= br[j]
            cur_lin ^= bl
            cur_c ^= bc
        got = G.quadratic_gauss_sum(cur_rows, cur_lin, cur_c, kernel_dim)
        spectrum[gray] = got['sum']
        polar_rank_hist[got['polar_rank']] += 1
        if got['sum'] == 0:
            zero_chars += 1
        else:
            nonzero_log_hist[got['log2_abs']] += 1
        prev_gray = gray

    assert spectrum[0] == 1 << kernel_dim
    counts = inverse_walsh_counts(spectrum)
    assert sum(counts) == 1 << kernel_dim
    image = [i for i, c in enumerate(counts) if c]
    missing = [i for i, c in enumerate(counts) if not c]
    nz = [counts[i] for i in image]

    out = {
        'position': 'C',
        'edge': {'lo': 110, 'hi': 166, 'size': 56},
        'function_lambda': len(J),
        'shared_affine_function_dim': len(JA),
        'shared_affine_linear_rank': affine_linear_rank,
        'constant_in_shared_affine_space': constant_in_shared,
        'origin_fiber_kernel_dim': kernel_dim,
        'quadratic_residual_dim': qdim,
        'characters_evaluated': total_chars,
        'zero_gauss_characters': zero_chars,
        'nonzero_gauss_characters': total_chars - zero_chars,
        'restricted_polar_rank_histogram': dict(sorted(polar_rank_hist.items())),
        'nonzero_gauss_log2_abs_histogram': dict(sorted(nonzero_log_hist.items())),
        'origin_fiber_residual_image_size': len(image),
        'origin_fiber_missing_outputs': len(missing),
        'origin_fiber_distinct_preimage_counts': len(set(nz)),
        'origin_fiber_min_nonzero_preimages': min(nz),
        'origin_fiber_max_preimages': max(nz),
        'first_missing_output_masks': missing[:16],
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_WORST_CUT_ORIGIN_FIBER_RESIDUAL_IMAGE')
    print('scope=exact residual evaluation image on the affine-separator fiber containing x=0 for the unique width-70 edge')
    print('method=restrict 13 residual quadratics to the affine kernel; evaluate all 8192 Fourier characters by exact quadratic Gauss elimination; invert Walsh spectrum exactly')
    print('important=this is one affine fiber, not yet a uniform all-fiber nonlinear message-count theorem')
    print('not_included=all affine fibers, aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
