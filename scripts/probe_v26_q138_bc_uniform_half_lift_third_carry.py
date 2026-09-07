#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_bc_half_uniform_linear_state_relaxed_scalar as U


def coordinate_solver(B):
    items = list(B.values())
    piv = {}
    for i, v in enumerate(items):
        row = v
        coeff = 1 << i
        while row:
            p = row.bit_length() - 1
            if p not in piv:
                piv[p] = (row, coeff)
                break
            r, c = piv[p]
            row ^= r
            coeff ^= c
        assert row, ('dependent input basis vector', i)
    assert len(piv) == len(items)
    return items, piv


def coordinates(v, piv):
    row = v
    coeff = 0
    while row:
        p = row.bit_length() - 1
        if p not in piv:
            return None
        r, c = piv[p]
        row ^= r
        coeff ^= c
    return coeff


def xor_lift_carry(coeff, items, expected_vec):
    # If y = XOR_i a_i v_i and the explicit integer lift is
    # K = SUM_i a_i v_i, then (K-y)/2 mod2 is the parity of all pairwise
    # intersections v_i & v_j among active coefficients.
    acc = 0
    carry = 0
    c = coeff
    while c:
        bit = c & -c
        i = bit.bit_length() - 1
        v = items[i]
        carry ^= acc & v
        acc ^= v
        c ^= bit
    assert acc == expected_vec
    return carry


def pairwise_intersection_basis(items):
    H = {}
    tested = 0
    saturation_pair = None
    for i in range(len(items)):
        vi = items[i]
        for j in range(i + 1, len(items)):
            tested += 1
            S.insert(H, vi & items[j])
            if len(H) == 2048:
                saturation_pair = (i, j)
                return H, tested, saturation_pair
    return H, tested, saturation_pair


def state_from_coeff(image_basis, coeff):
    z = 0
    for j, b in enumerate(image_basis):
        if (coeff >> j) & 1:
            z ^= b
    return z


def support_projection_equations(image_basis, syndrome_bits):
    eq_masks = []
    for e in range(syndrome_bits):
        m = 0
        for j, b in enumerate(image_basis):
            if (b >> e) & 1:
                m |= 1 << j
        eq_masks.append(m)
    return eq_masks


def half_state_setup(pos):
    _e0, _e1, half = U.H.classify_patterns()
    assert len(half) == 4

    cans = []
    phases = []
    qbase = []
    crosses = []

    for zs, cls in half:
        assert cls == (128, 0, 0)
        can = U.H.support_for(pos, zs, cls)
        assert can is not None
        cans.append(can)
        c, lin, polar, rank, pr = U.X.full_corrected_phase(pos, U.D.carries(zs))
        assert rank == 128 and pr == 0
        phases.append((c, lin, polar))

    assert all(can == cans[0] for can in cans)
    can = cans[0]

    cond = U.G.predecessor_condition(can)
    sol = U.T.rref(cond, n=U.PRED_BITS)
    assert sol is not None
    p0, null = sol[1], sol[2]
    assert U.F.fixed_possible(can, p0)

    eqs, toggles, rhsbits = U.F.support_desc(can, p0)
    syndrome_bits = len(eqs)
    syndrome_mask = (1 << syndrome_bits) - 1

    for zs, _cls in half:
        q, cross, rank, pr = U.F.specialized_phase_data(pos, zs, p0)
        assert rank == 128 and pr == 0
        qbase.append(q)
        crosses.append(cross)

    generators = []
    for d in null:
        sd = U.pred_support_delta(can, d)
        freqs = [U.pred_left_freq(phases[i][2], d) for i in range(4)]
        generators.append(U.pack_state(sd, freqs, syndrome_bits))
    for j in range(len(U.F.RIGHT)):
        sd = toggles[j]
        freqs = [crosses[i][j] for i in range(4)]
        generators.append(U.pack_state(sd, freqs, syndrome_bits))

    image_basis = S.row_basis(generators)
    assert len(image_basis) == 18, (pos, len(image_basis))

    return {
        'eqs': eqs,
        'rhsbits': rhsbits,
        'syndrome_bits': syndrome_bits,
        'syndrome_mask': syndrome_mask,
        'qbase': qbase,
        'image_basis': image_basis,
        'nullity': len(null),
    }


def relaxed_half_basis(st):
    """Reconstruct the PR104 relaxed half span by degree-two fiber interpolation.

    On a fixed support-syndrome fiber and scalar pattern the four left phase
    frequencies depend linearly on the fiber coordinates and half_correction is
    degree at most two in those sign bits. Values at zero, first differences,
    and mixed second differences therefore span every value on that fiber.
    """
    image_basis = st['image_basis']
    syndrome_bits = st['syndrome_bits']
    syndrome_mask = st['syndrome_mask']
    eq_masks = support_projection_equations(image_basis, syndrome_bits)

    HB = {}
    feasible_fibers = 0
    nonzero_fibers = 0
    coefficient_vectors = 0
    max_fiber_dim = 0

    for sigma in range(1 << syndrome_bits):
        eq = [(eq_masks[e], (sigma >> e) & 1) for e in range(syndrome_bits)]
        fib = U.T.rref(eq, n=len(image_basis))
        if fib is None:
            continue
        feasible_fibers += 1
        coeff0, coeff_null = fib[1], fib[2]
        max_fiber_dim = max(max_fiber_dim, len(coeff_null))

        state0 = state_from_coeff(image_basis, coeff0)
        dirs = [state_from_coeff(image_basis, d) for d in coeff_null]
        assert (state0 & syndrome_mask) == sigma
        assert all((d & syndrome_mask) == 0 for d in dirs)

        synd = st['rhsbits'] ^ sigma
        sm = U.F.left_support_mask(st['eqs'], synd)
        if sm == 0:
            continue
        nonzero_fibers += 1

        def eval_state(state, scalarpat):
            freqs = U.unpack_freqs(state, syndrome_bits)
            qs = []
            for i in range(4):
                q = st['qbase'][i] ^ S.WALSH[freqs[i]]
                if (scalarpat >> i) & 1:
                    q ^= S.ALL
                qs.append(q)
            return sm & U.E.half_correction(qs)

        for scalarpat in range(16):
            local = {}
            c0 = eval_state(state0, scalarpat)
            S.insert(local, c0)
            S.insert(HB, c0)
            coefficient_vectors += 1

            singles = []
            for d in dirs:
                v = eval_state(state0 ^ d, scalarpat)
                singles.append(v)
                a = v ^ c0
                S.insert(local, a)
                S.insert(HB, a)
                coefficient_vectors += 1

            for a in range(len(dirs)):
                for b in range(a + 1, len(dirs)):
                    vab = eval_state(state0 ^ dirs[a] ^ dirs[b], scalarpat)
                    qcoef = vab ^ singles[a] ^ singles[b] ^ c0
                    S.insert(local, qcoef)
                    S.insert(HB, qcoef)
                    coefficient_vectors += 1

            # Small deterministic interpolation regression on the first three
            # fiber directions. This catches accidental degree/order mistakes.
            tdim = min(3, len(dirs))
            for mask in range(1 << tdim):
                state = state0
                for j in range(tdim):
                    if (mask >> j) & 1:
                        state ^= dirs[j]
                assert U.E.in_span(local, eval_state(state, scalarpat))

    assert len(HB) == 144, len(HB)
    return HB, {
        'feasible_support_fibers': feasible_fibers,
        'nonzero_support_fibers': nonzero_fibers,
        'max_linear_fiber_dimension': max_fiber_dim,
        'quadratic_coefficient_vectors_attempted': coefficient_vectors,
    }


def analyze(pos):
    st = half_state_setup(pos)

    # Reconstruct the exact PR104 relaxed half span cheaply and prove that its
    # 144-dimensional basis lies inside the grouped-e0 space. This makes the
    # half basis itself a valid integer-lift gauge without enlarging PR104's
    # admitted ambient sign left-factor space.
    halfB, hstats = relaxed_half_basis(st)
    e0 = S.grouped_e0_basis(pos)
    expected_e0_dim = 272 if pos == 'B' else 388
    assert len(e0) == expected_e0_dim
    _e0_items, e0_piv = coordinate_solver(e0)
    assert all(coordinates(v, e0_piv) is not None for v in halfB.values())

    items, piv = coordinate_solver(halfB)
    assert len(items) == 144
    print(
        'position', pos,
        **hstats,
        'relaxed_half_basis_dim', len(items),
        'ambient_grouped_e0_dim', len(e0),
        'relaxed_half_basis_subset_grouped_e0', True,
        flush=True,
    )

    pair_hull, pair_tests, pair_sat = pairwise_intersection_basis(items)
    print(
        'position', pos,
        'explicit_half_lift_basis_dim', len(items),
        'pairwise_intersections_tested', pair_tests,
        'pairwise_intersection_hull_GF2_dim<=', len(pair_hull),
        'pairwise_hull_saturation_pair', pair_sat,
        flush=True,
    )

    if len(pair_hull) < 2048:
        return ('pairwise_hull_upper', len(pair_hull))

    carry_basis = {}
    support_cache = {}
    coord_cache = {0: 0}
    carry_cache = {0: 0}
    unique_coeff = set()
    feasible_states = 0
    generated_pairs = 0
    saturation_at = None

    state = 0
    prev_gray = 0
    image_basis = st['image_basis']
    for step in range(1 << len(image_basis)):
        gray = step ^ (step >> 1)
        if step:
            changed = gray ^ prev_gray
            j = changed.bit_length() - 1
            state ^= image_basis[j]
        prev_gray = gray

        synd = st['rhsbits'] ^ (state & st['syndrome_mask'])
        if synd not in support_cache:
            support_cache[synd] = U.F.left_support_mask(st['eqs'], synd)
        sm = support_cache[synd]
        if sm == 0:
            continue
        feasible_states += 1

        freqs = U.unpack_freqs(state, st['syndrome_bits'])
        base_qs = [st['qbase'][i] ^ S.WALSH[freqs[i]] for i in range(4)]
        for scalarpat in range(16):
            qs = []
            for i, q in enumerate(base_qs):
                z = q
                if (scalarpat >> i) & 1:
                    z ^= S.ALL
                qs.append(z)
            vec = sm & U.E.half_correction(qs)
            generated_pairs += 1

            coeff = coord_cache.get(vec)
            if coeff is None:
                coeff = coordinates(vec, piv)
                assert coeff is not None, (pos, 'half vector escaped reconstructed half span')
                coord_cache[vec] = coeff

            unique_coeff.add(coeff)
            carry = carry_cache.get(coeff)
            if carry is None:
                carry = xor_lift_carry(coeff, items, vec)
                carry_cache[coeff] = carry
            S.insert(carry_basis, carry)

            if len(carry_basis) == 2048:
                saturation_at = generated_pairs
                break
        if saturation_at is not None:
            break

    print(
        'position', pos,
        'half_predecessor_affine_nullity', st['nullity'],
        'linear_state_rank', len(image_basis),
        'feasible_linear_states_scanned', feasible_states,
        'generated_state_pairs_scanned', generated_pairs,
        'support_cache_size', len(support_cache),
        'unique_half_vectors_cached', len(coord_cache),
        'unique_half_basis_coordinate_masks', len(unique_coeff),
        'unique_carry_vectors_cached', len(carry_cache),
        'half_lift_induced_third_carry_GF2_span_dim<=', len(carry_basis),
        'saturation_at', saturation_at,
        flush=True,
    )

    if saturation_at is None:
        assert feasible_states == 131072
        assert generated_pairs == 2_097_152
        return ('upper', len(carry_basis))

    return ('relaxed_saturated', 2048)


def main():
    out = {pos: analyze(pos) for pos in 'BC'}
    print('result', out)
    print('PASS V26_Q138_BC_UNIFORM_HALF_LIFT_THIRD_CARRY')
    print('scope=induced third-bit carry of an explicit 144-vector relaxed-half-basis integer lift; basis containment in grouped-e0 is reverified by degree-two fiber interpolation; pairwise-intersection hull checked before full state enumeration')
    print('not_included=grouped-e0 own lift carry, support-only lift carry, cross-carries between components, complete B2/C2, complete leaf, W_repr, alpha, arithmetic-work, ranking/search, full-round')


if __name__ == '__main__':
    main()
