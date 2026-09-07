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
        'can': can,
        'eqs': eqs,
        'rhsbits': rhsbits,
        'syndrome_bits': syndrome_bits,
        'syndrome_mask': syndrome_mask,
        'qbase': qbase,
        'image_basis': image_basis,
        'nullity': len(null),
    }


def analyze(pos):
    st = half_state_setup(pos)

    # PR104 proves the relaxed uniform half span is contained in this fixed
    # grouped-e0 GF(2) span. Use the grouped-e0 basis itself as an explicit
    # parity-lift gauge for every half correction column.
    e0 = S.grouped_e0_basis(pos)
    expected_e0_dim = 272 if pos == 'B' else 388
    assert len(e0) == expected_e0_dim
    items, piv = coordinate_solver(e0)

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
                assert coeff is not None, (pos, 'half vector escaped grouped-e0 span')
                coord_cache[vec] = coeff

            unique_coeff.add(coeff)
            carry = carry_cache.get(coeff)
            if carry is None:
                carry = xor_lift_carry(coeff, items, vec)
                carry_cache[coeff] = carry
            else:
                # A GF(2) basis has unique coordinates, so equal coordinate
                # masks reconstruct the same truth vector. This assertion
                # protects the cache from silently hiding a solver bug.
                recon = 0
                c = coeff
                while c:
                    bit = c & -c
                    recon ^= items[bit.bit_length() - 1]
                    c ^= bit
                assert recon == vec

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
        'explicit_e0_basis_dim', len(items),
        'unique_half_vectors_cached', len(coord_cache),
        'unique_e0_coordinate_masks', len(unique_coeff),
        'unique_carry_vectors_cached', len(carry_cache),
        'half_lift_induced_third_carry_GF2_span_dim<=', len(carry_basis),
        'saturation_at', saturation_at,
        flush=True,
    )

    if saturation_at is None:
        # Full relaxed state enumeration completed. Since all true scalar states
        # are a subset of the 16-way relaxation, this is a uniform upper span
        # for the half-only induced carry of this explicit parity-lift gauge.
        assert feasible_states == 131072
        assert generated_pairs == 2_097_152
        return ('upper', len(carry_basis))

    # Early saturation is already a NO-GAIN certificate only for this relaxed
    # global-left-span route. The true scalar-feasible family is smaller, so
    # relaxed saturation is not a lower bound on the true carry rank.
    return ('relaxed_saturated', 2048)


def main():
    out = {pos: analyze(pos) for pos in 'BC'}
    print('result', out)
    print('PASS V26_Q138_BC_UNIFORM_HALF_LIFT_THIRD_CARRY')
    print('scope=induced third-bit carry of the explicit grouped-e0-basis integer lift for the PR104 relaxed half correction only')
    print('not_included=grouped-e0 own lift carry, support-only lift carry, cross-carries between components, complete B2/C2, complete leaf, W_repr, alpha, arithmetic-work, ranking/search, full-round')


if __name__ == '__main__':
    main()
