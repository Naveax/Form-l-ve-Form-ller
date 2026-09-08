#!/usr/bin/env python3
import json
import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_aggregate_signature_separator as A
import probe_v26_q138_c916_quadratic_function_space_separator as F
import probe_v26_q138_c916_quadratic_residual_separator as R
import probe_v26_q138_c916_aggregate_scalar_gauss_classes as G
import probe_v26_q138_c916_worst_cut_origin_fiber_residual_image as O

DOMAIN_BITS = F.DOMAIN_BITS
PAIR_BITS = F.PAIR_BITS
QUAD_MASK = (1 << PAIR_BITS) - 1
LINEAR_MASK = (1 << DOMAIN_BITS) - 1
assert DOMAIN_BITS == 149


def context():
    raw, groups = F.build_groups()
    assert raw == 577 and len(groups) == 250
    n = len(groups)
    all_indices = frozenset(range(n))
    order = sorted(range(n), key=lambda i: (groups[i]['multiplicity'], groups[i]['function_rank'], i))
    foracle = F.RankOracle(groups, 'function_basis')
    tree = F.build_tree(order, foracle)
    cert = F.verify_tree(tree, order, foracle)
    assert cert['width'] == 70 and cert['max_depth'] == 10

    target = None
    def walk(node):
        nonlocal target
        if not (node['lo'] == 0 and node['hi'] == n) and node['lambda'] == 70:
            assert target is None
            target = node
        if 'left' in node:
            walk(node['left'])
            walk(node['right'])
    walk(tree)
    assert target is not None
    assert (target['lo'], target['hi'], target['size']) == (110, 166, 56)

    oracles = {
        'function': R.BasisOracle(groups, 'function_basis'),
        'linear': R.BasisOracle(groups, 'linear_basis'),
    }
    idx = frozenset(order[110:166])
    comp = all_indices - idx
    J = R.intersection_basis(oracles['function'].basis(idx), oracles['function'].basis(comp))
    linear_all = oracles['linear'].basis(all_indices)
    affine_basis = A.L.basis(linear_all + [R.CONST_BIT])
    JA = R.intersection_basis(J, affine_basis)
    residual = O.quadratic_quotient_basis(J)
    assert len(J) == 70 and len(JA) == 57 and len(residual) == 13

    affine_rows = A.L.basis((v >> PAIR_BITS) & LINEAR_MASK for v in JA)
    assert len(affine_rows) == 56
    assert len(A.L.basis(JA + [R.CONST_BIT])) == len(JA)
    kernel = O.nullspace_basis(affine_rows, DOMAIN_BITS)
    assert len(kernel) == 93

    origin_rows = []
    full_polars = []
    for v in residual:
        rrows, rlin, _c = O.restrict_poly(v, kernel)
        assert all(r == 0 for r in rrows)
        origin_rows.append(rlin)
        pair = v & QUAD_MASK
        full_polars.append(G.rows_from_pair_mask(DOMAIN_BITS, pair))
    assert A.L.rank(origin_rows) == 4
    return kernel, origin_rows, full_polars


def functional_on_kernel(polar_rows, x0, kernel):
    p = O.polar_apply(polar_rows, x0)
    row = 0
    for j, k in enumerate(kernel):
        if (p & k).bit_count() & 1:
            row |= 1 << j
    return row


def analyze():
    kernel, origin_rows, full_polars = context()
    assert len(origin_rows) == 13

    # Translation by x0 changes only the linear part on K because every
    # residual polar restricts to zero on K x K. Precompute one coordinate
    # translation effect for each original shared variable.
    effects = []
    for s in range(DOMAIN_BITS):
        x = 1 << s
        effects.append([
            functional_on_kernel(full_polars[i], x, kernel)
            for i in range(13)
        ])

    def rank_for_mask(mask):
        rows = list(origin_rows)
        x = mask
        while x:
            b = x & -x
            s = b.bit_length() - 1
            es = effects[s]
            for i in range(13):
                rows[i] ^= es[i]
            x ^= b
        return A.L.rank(rows)

    hist = Counter()
    tested = 0
    best_rank = rank_for_mask(0)
    best_mask = 0
    best_source = 'origin'
    hist[best_rank] += 1
    tested += 1
    assert best_rank == 4

    # Deterministic low-weight search first gives a compact human-auditable
    # witness if possible.
    for s in range(DOMAIN_BITS):
        m = 1 << s
        r = rank_for_mask(m)
        hist[r] += 1
        tested += 1
        if r > best_rank:
            best_rank, best_mask, best_source = r, m, f'unit:{s}'
        if best_rank == 13:
            break

    if best_rank < 13:
        stop = False
        for s in range(DOMAIN_BITS):
            for t in range(s + 1, DOMAIN_BITS):
                m = (1 << s) | (1 << t)
                r = rank_for_mask(m)
                hist[r] += 1
                tested += 1
                if r > best_rank:
                    best_rank, best_mask, best_source = r, m, f'pair:{s},{t}'
                if best_rank == 13:
                    stop = True
                    break
            if stop:
                break

    if best_rank < 13:
        rng = random.Random(0xC916129)
        for j in range(20000):
            m = rng.getrandbits(DOMAIN_BITS)
            r = rank_for_mask(m)
            hist[r] += 1
            tested += 1
            if r > best_rank:
                best_rank, best_mask, best_source = r, m, f'prng:{j}'
            if best_rank == 13:
                break

    # Rank is constant on an affine fiber: translating the representative by
    # k0 in K does not change B_i(x0,k), because B_i|_{K x K}=0.
    for k in kernel[:8]:
        assert rank_for_mask(best_mask ^ k) == best_rank

    out = {
        'position': 'C',
        'edge': {'lo': 110, 'hi': 166, 'size': 56},
        'shared_affine_function_dim': 57,
        'shared_affine_linear_rank': 56,
        'fiber_kernel_dim': 93,
        'quadratic_residual_dim': 13,
        'restricted_polar_rank': 0,
        'origin_fiber_residual_rank': 4,
        'origin_fiber_image_size': 16,
        'origin_fiber_uniform_preimages': 1 << 89,
        'candidates_tested': tested,
        'observed_rank_histogram': dict(sorted(hist.items())),
        'max_fiber_residual_rank_witnessed': best_rank,
        'witness_mask_hex': hex(best_mask),
        'witness_hamming_weight': best_mask.bit_count(),
        'witness_source': best_source,
        'witness_image_size': 1 << best_rank,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_WORST_CUT_FIBER_RESIDUAL_RANK_WITNESS')
    print('scope=exact affine-linear residual rank on explicit affine-fiber representatives for the unique width-70 edge')
    print('important=if rank13 is witnessed, global maximum fiber residual rank is exactly13; this does not describe the rank distribution over all 2^56 fibers')
    print('not_included=all-fiber rank distribution, aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
