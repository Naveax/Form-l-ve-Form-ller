#!/usr/bin/env python3
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
MAX_ENUM_RANK = 20


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
    p0, null = sol[1], sol[2]
    assert F.fixed_possible(can, p0)

    eqs, toggles, rhsbits = F.support_desc(can, p0)
    syndrome_bits = len(eqs)
    syndrome_mask = (1 << syndrome_bits) - 1

    for zs, _cls in half:
        q, cross, rank, pr = F.specialized_phase_data(pos, zs, p0)
        assert rank == 128 and pr == 0
        qbase.append(q)
        crosses.append(cross)

    # Exact linear image seen by support syndrome plus four left phase
    # frequencies when both the half-active predecessor and the 21 right-beta
    # variables vary. Scalar phase bits are deliberately omitted and relaxed
    # to all 16 patterns only after this exact linear image is enumerated.
    generators = []

    for d in null:
        sd = pred_support_delta(can, d)
        freqs = [pred_left_freq(phases[i][2], d) for i in range(4)]
        generators.append(pack_state(sd, freqs, syndrome_bits))

    for j in range(len(F.RIGHT)):
        sd = toggles[j]
        freqs = [crosses[i][j] for i in range(4)]
        generators.append(pack_state(sd, freqs, syndrome_bits))

    image_basis = S.row_basis(generators)
    image_rank = len(image_basis)
    print(
        'position', pos,
        'half_predecessor_affine_nullity', len(null),
        'combined_pred_right_linear_state_rank', image_rank,
        'linear_state_count', 1 << image_rank,
        'scalar_relaxation_patterns_per_state', 16,
        flush=True,
    )

    if image_rank > MAX_ENUM_RANK:
        print(
            'position', pos,
            'uniform_relaxed_scalar_enumeration', 'SKIP',
            'reason=combined_linear_state_rank_exceeds_cap',
            'cap', MAX_ENUM_RANK,
            flush=True,
        )
        return None

    HB = {}
    support_cache = {}
    feasible_states = 0
    generated_pairs = 0

    # Enumerate the image subspace in Gray-code order. Every actual
    # predecessor/right pair maps into this image. For each linear state all
    # four scalar phase bits are allowed, a safe superset of the true
    # quadratic scalar image.
    state = 0
    prev_gray = 0
    for step in range(1 << image_rank):
        gray = step ^ (step >> 1)
        if step:
            changed = gray ^ prev_gray
            j = changed.bit_length() - 1
            state ^= image_basis[j]
        prev_gray = gray

        synd = rhsbits ^ (state & syndrome_mask)
        if synd not in support_cache:
            support_cache[synd] = F.left_support_mask(eqs, synd)
        sm = support_cache[synd]
        if sm == 0:
            continue
        feasible_states += 1

        freqs = unpack_freqs(state, syndrome_bits)
        base_qs = [qbase[i] ^ S.WALSH[freqs[i]] for i in range(4)]
        for scalarpat in range(16):
            qs = []
            for i, q in enumerate(base_qs):
                z = q
                if (scalarpat >> i) & 1:
                    z ^= S.ALL
                qs.append(z)
            vec = sm & E.half_correction(qs)
            S.insert(HB, vec)
            generated_pairs += 1

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
        'uniform_relaxed_scalar_feasible_linear_states', feasible_states,
        'uniform_relaxed_scalar_generated_state_pairs', generated_pairs,
        'uniform_relaxed_scalar_support_cache_size', len(support_cache),
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
    out = {}
    for pos in 'BC':
        out[pos] = analyze(pos)
    print('result', out)
    print('PASS V26_Q138_BC_HALF_UNIFORM_LINEAR_STATE_RELAXED_SCALAR')
    print('scope=uniform half-sector binary-lift upper span over all predecessors; scalar phase feasibility safely relaxed to all 16 patterns per exact linear image state')
    print('claim=any printed second-lift total is a valid uniform upper bound; SKIP means only the enumeration cap was exceeded')
    print('not_claimed=no optimality, complete-leaf, representation, arithmetic-work, alpha, ranking/search, or full-round claim')


if __name__ == '__main__':
    main()
