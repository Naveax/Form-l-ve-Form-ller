#!/usr/bin/env python3
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_bc_half_uniform_linear_state_relaxed_scalar as U
import probe_v26_q138_bc_uniform_half_lift_third_carry as H

MAX_DEGREE = 4


def subset_masks_upto(n, degree):
    out = [0]
    for k in range(1, degree + 1):
        for comb in itertools.combinations(range(n), k):
            m = 0
            for j in comb:
                m |= 1 << j
            out.append(m)
    return out


def state_with_mask(state0, dirs, mask):
    state = state0
    c = mask
    while c:
        bit = c & -c
        state ^= dirs[bit.bit_length() - 1]
        c ^= bit
    return state


def proper_subsets(mask):
    sub = (mask - 1) & mask
    while True:
        yield sub
        if sub == 0:
            break
        sub = (sub - 1) & mask


def analyze(pos):
    st = H.half_state_setup(pos)

    # Reconstruct PR104's relaxed half span independently of the carry step and
    # reverify that the entire half family lies in the canonical grouped-e0
    # GF(2) space.
    halfB, hstats = H.relaxed_half_basis(st)
    assert len(halfB) == 144

    e0 = S.grouped_e0_basis(pos)
    expected_e0_dim = 272 if pos == 'B' else 388
    expected_support = 668 if pos == 'B' else 788
    expected_qr = 80 if pos == 'B' else 148
    expected_total = 748 if pos == 'B' else 936
    assert len(e0) == expected_e0_dim

    e0_items, e0_piv = H.coordinate_solver(e0)
    assert all(H.coordinates(v, e0_piv) is not None for v in halfB.values())

    # Canonical PR104 integer-gauge regression.  Because PR104 inserts grouped
    # e0 before the new half span and the latter is contained in e0, its union
    # basis is exactly this grouped-e0 pivot basis.
    support = U.N.weight120_union(pos)
    assert len(support) == expected_support
    qr, comp = U.R.quotient_rank(e0, support)
    assert qr == expected_qr, (pos, qr, expected_qr)
    assert len(support) + qr == expected_total

    # Cheap all-coordinate-mask upper hull for the actual canonical basis.
    pair_hull, pair_tests, pair_sat = H.pairwise_intersection_basis(e0_items)
    print(
        'position', pos,
        **hstats,
        'canonical_grouped_e0_basis_dim', len(e0_items),
        'canonical_exact_ZZ_quotient', qr,
        'canonical_second_lift_total', expected_total,
        'canonical_Walsh_complement_coordinates', comp,
        'canonical_pairwise_intersections_tested', pair_tests,
        'canonical_pairwise_intersection_hull_GF2_dim<=', len(pair_hull),
        'canonical_pairwise_hull_saturation_pair', pair_sat,
        flush=True,
    )

    if len(pair_hull) < 2048:
        return ('canonical_pairwise_hull_upper', len(pair_hull), expected_total)

    # On one support-syndrome fiber and fixed scalar pattern, half correction
    # y(t) is degree <=2 in the fiber coordinates. Coordinates in a fixed GF(2)
    # basis are linear in y, hence each coordinate bit has degree <=2. The
    # parity-lift carry is quadratic in those coordinate bits, so carry(t) has
    # degree <=4. Therefore its ANF coefficients through degree4 span every
    # carry value on the fiber.
    image_basis = st['image_basis']
    syndrome_bits = st['syndrome_bits']
    syndrome_mask = st['syndrome_mask']
    eq_masks = H.support_projection_equations(image_basis, syndrome_bits)

    carry_span = {}
    coord_cache = {0: 0}
    carry_cache = {0: 0}
    feasible_fibers = 0
    nonzero_fibers = 0
    scalar_fibers = 0
    carry_evaluations = 0
    anf_coefficients = 0
    max_fiber_dim = 0
    max_subset_evaluations = 0

    def eval_carry(state, scalarpat, sm):
        nonlocal carry_evaluations
        freqs = U.unpack_freqs(state, syndrome_bits)
        qs = []
        for i in range(4):
            q = st['qbase'][i] ^ S.WALSH[freqs[i]]
            if (scalarpat >> i) & 1:
                q ^= S.ALL
            qs.append(q)
        vec = sm & U.E.half_correction(qs)
        carry_evaluations += 1

        coeff = coord_cache.get(vec)
        if coeff is None:
            coeff = H.coordinates(vec, e0_piv)
            assert coeff is not None, (pos, 'half vector escaped canonical grouped-e0 basis')
            coord_cache[vec] = coeff
        carry = carry_cache.get(coeff)
        if carry is None:
            carry = H.xor_lift_carry(coeff, e0_items, vec)
            carry_cache[coeff] = carry
        return carry

    for sigma in range(1 << syndrome_bits):
        eq = [(eq_masks[e], (sigma >> e) & 1) for e in range(syndrome_bits)]
        fib = U.T.rref(eq, n=len(image_basis))
        if fib is None:
            continue
        feasible_fibers += 1
        coeff0, coeff_null = fib[1], fib[2]
        max_fiber_dim = max(max_fiber_dim, len(coeff_null))

        state0 = H.state_from_coeff(image_basis, coeff0)
        dirs = [H.state_from_coeff(image_basis, d) for d in coeff_null]
        assert (state0 & syndrome_mask) == sigma
        assert all((d & syndrome_mask) == 0 for d in dirs)

        synd = st['rhsbits'] ^ sigma
        sm = U.F.left_support_mask(st['eqs'], synd)
        if sm == 0:
            continue
        nonzero_fibers += 1

        masks = subset_masks_upto(len(dirs), MAX_DEGREE)
        max_subset_evaluations = max(max_subset_evaluations, len(masks))

        for scalarpat in range(16):
            scalar_fibers += 1
            anf = {}
            for mask in masks:
                state = state_with_mask(state0, dirs, mask)
                a = eval_carry(state, scalarpat, sm)
                if mask:
                    for sub in proper_subsets(mask):
                        a ^= anf[sub]
                anf[mask] = a
                S.insert(carry_span, a)
                anf_coefficients += 1

            # Deterministic degree<=4 regressions away from the interpolation
            # sample set.  These checks fail if the coordinate/carry degree
            # argument or affine-fiber origin handling is wrong.
            probes = []
            full = (1 << len(dirs)) - 1
            probes.append(full)
            if len(dirs) >= 5:
                probes.append((1 << 5) - 1)
            if len(dirs) >= 7:
                probes.append(sum(1 << j for j in range(0, len(dirs), 2)))
                probes.append(sum(1 << j for j in range(1, len(dirs), 2)))
            for mask in dict.fromkeys(probes):
                predicted = 0
                for mon, coef in anf.items():
                    if mon & ~mask == 0:
                        predicted ^= coef
                actual = eval_carry(state_with_mask(state0, dirs, mask), scalarpat, sm)
                assert predicted == actual, (pos, sigma, scalarpat, mask)

    print(
        'position', pos,
        'canonical_degree4_feasible_support_fibers', feasible_fibers,
        'canonical_degree4_nonzero_support_fibers', nonzero_fibers,
        'canonical_degree4_scalar_fibers', scalar_fibers,
        'canonical_degree4_max_fiber_dimension', max_fiber_dim,
        'canonical_degree4_max_subset_evaluations_per_scalar_fiber', max_subset_evaluations,
        'canonical_degree4_carry_evaluations', carry_evaluations,
        'canonical_degree4_ANF_coefficients_inserted', anf_coefficients,
        'canonical_degree4_unique_half_vectors_cached', len(coord_cache),
        'canonical_degree4_unique_coordinate_masks_cached', len(carry_cache),
        'canonical_half_induced_third_carry_GF2_span_dim<=', len(carry_span),
        flush=True,
    )

    return ('canonical_degree4_upper', len(carry_span), expected_total)


def main():
    out = {pos: analyze(pos) for pos in 'BC'}
    print('result', out)
    print('PASS V26_Q138_BC_CANONICAL_E0_HALF_THIRD_CARRY_DEGREE4')
    print('scope=uniform relaxed half-only inherited third carry under the exact canonical PR104 grouped-e0 integer basis; pairwise hull first, then exact degree<=4 fiber interpolation if needed')
    print('not_included=grouped-e0 family own carry, support-only lift carry, cross-carries, complete B2/C2, complete leaf, W_repr, alpha, arithmetic-work, ranking/search, full-round')


if __name__ == '__main__':
    main()
