#!/usr/bin/env python3
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import verify_v26_q138_predecessor_leaf_bc_second_residue_support_frequency_nesting as N
import verify_v26_q138_predecessor_leaf_bc_second_residue_rank812_972 as R
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import probe_v26_q138_bc_direct_e1_exact_sector_cancellation as X
import probe_v26_q138_bc_second_residue_fixed_predecessor_specialization as F
import probe_v26_q138_bc_second_residue_reachable_predecessor_geometry as G
import probe_v26_q138_bc_second_residue_half_exact_right21 as E

PRED_BITS = 128


def pred_support_delta(can, d):
    z = 0
    for e, row in enumerate(can):
        if (row & d).bit_count() & 1:
            z |= 1 << e
    return z


def pred_left_freq(polar, d):
    z = 0
    for a, el in enumerate(F.LEXT):
        if (polar[el] & d).bit_count() & 1:
            z |= 1 << a
    return z


def pack_state(syndrome, freqs, syndrome_bits):
    z = syndrome
    shift = syndrome_bits
    for f in freqs:
        z |= f << shift
        shift += len(F.LEFT)
    return z


def unpack_freqs(state, syndrome_bits):
    out = []
    shift = syndrome_bits
    mask = (1 << len(F.LEFT)) - 1
    for _ in range(4):
        out.append((state >> shift) & mask)
        shift += len(F.LEFT)
    return out


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


def analyze(pos):
    _e0, _e1, half = H.classify_patterns()
    assert len(half) == 4

    cans = []
    phases = []
    qbase = []
    crosses = []
    for zs, cls in half:
        assert cls == (128, 0, 0)
        can = H.support_for(pos, zs, cls)
        assert can is not None
        cans.append(can)
        c, lin, polar, rank, pr = X.full_corrected_phase(pos, D.carries(zs))
        assert rank == 128 and pr == 0
        phases.append((c, lin, polar))

    assert all(can == cans[0] for can in cans)
    can = cans[0]

    cond = G.predecessor_condition(can)
    sol = T.rref(cond, n=PRED_BITS)
    assert sol is not None
    p0, pred_null = sol[1], sol[2]
    assert F.fixed_possible(can, p0)

    eqs, toggles, rhsbits = F.support_desc(can, p0)
    syndrome_bits = len(eqs)
    syndrome_mask = (1 << syndrome_bits) - 1

    for zs, _cls in half:
        q, cross, rank, pr = F.specialized_phase_data(pos, zs, p0)
        assert rank == 128 and pr == 0
        qbase.append(q)
        crosses.append(cross)

    generators = []
    for d in pred_null:
        sd = pred_support_delta(can, d)
        freqs = [pred_left_freq(phases[i][2], d) for i in range(4)]
        generators.append(pack_state(sd, freqs, syndrome_bits))

    for j in range(len(F.RIGHT)):
        sd = toggles[j]
        freqs = [crosses[i][j] for i in range(4)]
        generators.append(pack_state(sd, freqs, syndrome_bits))

    image_basis = S.row_basis(generators)
    image_rank = len(image_basis)
    support_image_basis = S.row_basis([b & syndrome_mask for b in image_basis])
    support_image_rank = len(support_image_basis)
    support_eq_masks = support_projection_equations(image_basis, syndrome_bits)

    print(
        'position', pos,
        'half_predecessor_affine_nullity', len(pred_null),
        'combined_pred_right_linear_state_rank', image_rank,
        'support_projection_rank', support_image_rank,
        'support_projection_state_count', 1 << support_image_rank,
        flush=True,
    )

    HB = {}
    feasible_support_fibers = 0
    nonzero_support_fibers = 0
    max_fiber_dim = 0
    coefficient_vectors_attempted = 0
    rng = random.Random(0xB if pos == 'B' else 0xC)

    for sigma in range(1 << syndrome_bits):
        eq = [(support_eq_masks[e], (sigma >> e) & 1)
              for e in range(syndrome_bits)]
        fib = T.rref(eq, n=image_rank)
        if fib is None:
            continue
        feasible_support_fibers += 1
        coeff0, coeff_null = fib[1], fib[2]
        max_fiber_dim = max(max_fiber_dim, len(coeff_null))

        state0 = state_from_coeff(image_basis, coeff0)
        dirs = [state_from_coeff(image_basis, d) for d in coeff_null]
        assert (state0 & syndrome_mask) == sigma
        assert all((d & syndrome_mask) == 0 for d in dirs)

        synd = rhsbits ^ sigma
        sm = F.left_support_mask(eqs, synd)
        if sm == 0:
            continue
        nonzero_support_fibers += 1

        def eval_state(state, scalarpat):
            freqs = unpack_freqs(state, syndrome_bits)
            qs = []
            for i in range(4):
                q = qbase[i] ^ S.WALSH[freqs[i]]
                if (scalarpat >> i) & 1:
                    q ^= S.ALL
                qs.append(q)
            return sm & E.half_correction(qs)

        for scalarpat in range(16):
            local = {}
            c0 = eval_state(state0, scalarpat)
            S.insert(local, c0)
            S.insert(HB, c0)
            coefficient_vectors_attempted += 1

            singles = []
            for d in dirs:
                v = eval_state(state0 ^ d, scalarpat)
                singles.append(v)
                a = v ^ c0
                S.insert(local, a)
                S.insert(HB, a)
                coefficient_vectors_attempted += 1

            for a in range(len(dirs)):
                for b in range(a + 1, len(dirs)):
                    vab = eval_state(state0 ^ dirs[a] ^ dirs[b], scalarpat)
                    qcoef = vab ^ singles[a] ^ singles[b] ^ c0
                    S.insert(local, qcoef)
                    S.insert(HB, qcoef)
                    coefficient_vectors_attempted += 1

            # Deterministic checks of the degree-two interpolation. Every
            # sampled exact fiber value must lie in the coefficient span.
            tests = min(8, 1 << min(len(dirs), 8))
            for _ in range(tests):
                state = state0
                for j, d in enumerate(dirs):
                    if rng.getrandbits(1):
                        state ^= d
                v = eval_state(state, scalarpat)
                assert E.in_span(local, v), (pos, sigma, scalarpat)

    assert feasible_support_fibers == (1 << support_image_rank)

    old_half = S.half_basis(pos)
    assert all(E.in_span(old_half, v) for v in HB.values())

    e0 = S.grouped_e0_basis(pos)
    U = S.union_basis(e0, HB)
    support = N.weight120_union(pos)
    expected_support = 668 if pos == 'B' else 788
    assert len(support) == expected_support
    qr, comp = R.quotient_rank(U, support)
    total = len(support) + qr

    baseline_half = 252 if pos == 'B' else 280
    baseline_total = 812 if pos == 'B' else 972
    print(
        'position', pos,
        'feasible_support_fibers', feasible_support_fibers,
        'nonzero_support_fibers', nonzero_support_fibers,
        'max_linear_fiber_dimension', max_fiber_dim,
        'quadratic_coefficient_vectors_attempted', coefficient_vectors_attempted,
        'uniform_relaxed_scalar_half_rank_F2<=', len(HB),
        'baseline_uniform_half_rank_F2<=', baseline_half,
        'combined_uniform_sign_basis_dim<=', len(U),
        'uniform_exact_ZZ_quotient_rank<=', qr,
        'uniform_second_lift_rank<=', total,
        'baseline_uniform_second_lift_rank<=', baseline_total,
        'uniform_second_lift_gain>=', baseline_total - total,
        'Walsh_complement_coordinates', comp,
        flush=True,
    )
    assert total <= baseline_total
    return total


def main():
    result = {pos: analyze(pos) for pos in 'BC'}
    print('result', result)
    print('PASS V26_Q138_BC_HALF_UNIFORM_FIBER_QUADRATIC_SPAN')
    print('scope=uniform half-sector binary-lift upper span over all predecessors using exact support fibers and degree-two interpolation; scalar feasibility safely relaxed to all 16 patterns')
    print('claim=printed second-lift totals are valid uniform upper bounds, not optimality claims')
    print('not_claimed=no complete-leaf, representation, arithmetic-work, alpha, ranking/search, or full-round claim')


if __name__ == '__main__':
    main()
