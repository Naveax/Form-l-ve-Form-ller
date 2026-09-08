#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_reachable_joint_sign_span as P
import probe_v26_q138_bc_half_uniform_linear_state_relaxed_scalar as L

S = L.S
N = L.N
R = L.R


def relaxed_half_basis(pos):
    _e0, _e1, half = L.H.classify_patterns()
    assert len(half) == 4

    cans = []
    phases = []
    qbase = []
    crosses = []
    for zs, cls in half:
        assert cls == (128, 0, 0)
        can = L.H.support_for(pos, zs, cls)
        assert can is not None
        cans.append(can)
        c, lin, polar, rank, pr = L.X.full_corrected_phase(pos, L.D.carries(zs))
        assert rank == 128 and pr == 0
        phases.append((c, lin, polar))

    assert all(can == cans[0] for can in cans)
    can = cans[0]

    cond = L.G.predecessor_condition(can)
    sol = L.T.rref(cond, n=L.PRED_BITS)
    assert sol is not None
    p0, null = sol[1], sol[2]
    assert L.F.fixed_possible(can, p0)

    eqs, toggles, rhsbits = L.F.support_desc(can, p0)
    syndrome_bits = len(eqs)
    syndrome_mask = (1 << syndrome_bits) - 1

    for zs, _cls in half:
        q, cross, rank, pr = L.F.specialized_phase_data(pos, zs, p0)
        assert rank == 128 and pr == 0
        qbase.append(q)
        crosses.append(cross)

    generators = []
    for d in null:
        sd = L.pred_support_delta(can, d)
        freqs = [L.pred_left_freq(phases[i][2], d) for i in range(4)]
        generators.append(L.pack_state(sd, freqs, syndrome_bits))

    for j in range(len(L.F.RIGHT)):
        sd = toggles[j]
        freqs = [crosses[i][j] for i in range(4)]
        generators.append(L.pack_state(sd, freqs, syndrome_bits))

    image_basis = S.row_basis(generators)
    image_rank = len(image_basis)
    assert image_rank <= L.MAX_ENUM_RANK, (pos, image_rank, L.MAX_ENUM_RANK)

    HB = {}
    support_cache = {}
    feasible_states = 0
    generated_pairs = 0

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
            support_cache[synd] = L.F.left_support_mask(eqs, synd)
        sm = support_cache[synd]
        if sm == 0:
            continue
        feasible_states += 1

        freqs = L.unpack_freqs(state, syndrome_bits)
        base_qs = [qbase[i] ^ S.WALSH[freqs[i]] for i in range(4)]
        for scalarpat in range(16):
            qs = []
            for i, q in enumerate(base_qs):
                z = q
                if (scalarpat >> i) & 1:
                    z ^= S.ALL
                qs.append(z)
            vec = sm & L.E.half_correction(qs)
            S.insert(HB, vec)
            generated_pairs += 1

    old_half = S.half_basis(pos)
    assert all(L.E.in_span(old_half, v) for v in HB.values())
    return HB, {
        'half_linear_image_rank': image_rank,
        'half_feasible_linear_states': feasible_states,
        'half_generated_state_pairs': generated_pairs,
        'half_relaxed_rank_F2': len(HB),
    }


def reachable_e0_basis(pos):
    raw, groups = P.grouped_data(pos)
    reachable = {}
    correlated = 0
    full_product = 0
    for can, sectors in groups:
        qbits, cols = P.aggregate_phase(pos, sectors)
        local, st = P.reachable_local_basis(can, qbits, cols)
        correlated += st['mode'] == 'correlated_image'
        full_product += st['mode'] == 'full_product'
        for v in local.values():
            S.insert(reachable, v)

    canonical = S.grouped_e0_basis(pos)
    assert len(reachable) == len(canonical)
    assert len(S.union_basis(canonical, reachable)) == len(canonical)
    return reachable, canonical, {
        'raw_e0_sectors': raw,
        'support_groups': len(groups),
        'reachable_e0_rank_F2': len(reachable),
        'correlated_groups': correlated,
        'full_product_groups': full_product,
    }


def analyze(pos):
    HB, hstats = relaxed_half_basis(pos)
    reachable, canonical, estats = reachable_e0_basis(pos)

    old_union = S.union_basis(canonical, HB)
    reachable_union = S.union_basis(reachable, HB)

    # The old relaxed-half probe established that HB adds no GF(2) direction
    # to the canonical grouped-e0 span. Since the reachable e0 span is exactly
    # the same GF(2) subspace, the reachable union must have the same dimension.
    assert len(old_union) == len(canonical)
    assert len(reachable_union) == len(reachable)

    support = N.weight120_union(pos)
    expected_support = 668 if pos == 'B' else 788
    assert len(support) == expected_support

    old_qr, old_comp = R.quotient_rank(old_union, support)
    reachable_qr, reachable_comp = R.quotient_rank(reachable_union, support)
    assert old_comp == reachable_comp

    old_total = len(support) + old_qr
    reachable_total = len(support) + reachable_qr
    expected_old_total = 748 if pos == 'B' else 936
    assert old_total == expected_old_total, (pos, old_total, expected_old_total)

    out = {
        'position': pos,
        **hstats,
        **estats,
        'canonical_e0_plus_relaxed_half_rank_F2': len(old_union),
        'reachable_e0_plus_relaxed_half_rank_F2': len(reachable_union),
        'support_Walsh_dim': len(support),
        'Walsh_complement_coordinates': reachable_comp,
        'canonical_relaxed_exact_ZZ_quotient_rank': old_qr,
        'reachable_relaxed_exact_ZZ_quotient_rank': reachable_qr,
        'canonical_relaxed_second_lift_rank_bound': old_total,
        'reachable_relaxed_second_lift_rank_bound': reachable_total,
        'reachable_vs_canonical_relaxed_gain': old_total - reachable_total,
    }
    print(json.dumps(out, sort_keys=True), flush=True)
    return out


def main():
    out = {pos: analyze(pos) for pos in 'BC'}
    print('result_summary', json.dumps({
        pos: {
            'half_linear_image_rank': out[pos]['half_linear_image_rank'],
            'half_relaxed_rank_F2': out[pos]['half_relaxed_rank_F2'],
            'reachable_e0_rank_F2': out[pos]['reachable_e0_rank_F2'],
            'reachable_e0_plus_relaxed_half_rank_F2': out[pos]['reachable_e0_plus_relaxed_half_rank_F2'],
            'canonical_relaxed_exact_ZZ_quotient_rank': out[pos]['canonical_relaxed_exact_ZZ_quotient_rank'],
            'reachable_relaxed_exact_ZZ_quotient_rank': out[pos]['reachable_relaxed_exact_ZZ_quotient_rank'],
            'canonical_relaxed_second_lift_rank_bound': out[pos]['canonical_relaxed_second_lift_rank_bound'],
            'reachable_relaxed_second_lift_rank_bound': out[pos]['reachable_relaxed_second_lift_rank_bound'],
            'reachable_vs_canonical_relaxed_gain': out[pos]['reachable_vs_canonical_relaxed_gain'],
        }
        for pos in 'BC'
    }, sort_keys=True), flush=True)
    print('PASS PROBE V26_Q138_BC_E0_REACHABLE_HALF_RELAXED_ZZ')
    print('scope=reachable-joint grouped-e0 gauge span union exact linear-image half span with scalar phase safely relaxed to all 16 patterns per feasible state')
    print('important=GF2 span equality is checked separately; the reported comparison is recomputed in the exact ZZ Walsh-complement quotient')
    print('not_claimed=no monotonicity assumption between alternate GF2 bases, no complete B2/C2, W_repr, alpha, arithmetic-work, ranking/search, or full-round claim')


if __name__ == '__main__':
    main()
