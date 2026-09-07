#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import verify_v26_q138_predecessor_leaf_bc_second_residue_support_frequency_nesting as N
import verify_v26_q138_predecessor_leaf_bc_second_residue_rank812_972 as R
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import probe_v26_q138_bc_direct_e1_exact_sector_cancellation as X
import probe_v26_q138_bc_second_residue_reachable_predecessor_geometry as G

LEFT = sorted(A.S1)
RIGHT = list(A.R1)
LEXT = [128 + i for i in LEFT]
REXT = [128 + i for i in RIGHT]
WITNESS = {
    'B': 0x18180000bfffffff80080800bffffffd,
    'C': 0x180000bfffffff80000800bfffffff,
}


def fixed_possible(can, pred):
    return T.rref(G.beta32_equations(can, pred), n=32) is not None


def specialized_phase_data(pos, zs, pred):
    c, lin, polar, rank, pr = X.full_corrected_phase(pos, D.carries(zs))
    const = X.q_eval(c, lin, polar, pred)

    lfreq = 0
    for a, ext in enumerate(LEXT):
        bit = ((lin >> ext) & 1) ^ ((polar[ext] & pred).bit_count() & 1)
        if bit:
            lfreq |= 1 << a

    qbits = S.WALSH[lfreq]
    if const:
        qbits ^= S.ALL

    for a in range(len(LEXT)):
        ea = LEXT[a]
        for b in range(a + 1, len(LEXT)):
            eb = LEXT[b]
            if (polar[ea] >> eb) & 1:
                qbits ^= S.WALSH[1 << a] & S.WALSH[1 << b]

    cross = []
    for er in REXT:
        f = 0
        for a, el in enumerate(LEXT):
            if (polar[er] >> el) & 1:
                f |= 1 << a
        cross.append(f)

    assert len(cross) == 21
    return qbits, cross, rank, pr


def support_desc(can, pred):
    eqs = []
    toggles = [0] * len(RIGHT)
    rhsbits = 0
    for e, row in enumerate(can):
        lm = 0
        for a, ext in enumerate(LEXT):
            if (row >> ext) & 1:
                lm |= 1 << a
        eqs.append(lm)

        rhs = ((row >> 160) & 1) ^ ((row & pred).bit_count() & 1)
        if rhs:
            rhsbits |= 1 << e

        for j, ext in enumerate(REXT):
            if (row >> ext) & 1:
                toggles[j] ^= 1 << e
    return tuple(eqs), tuple(toggles), rhsbits


def left_support_mask(eqs, syndrome):
    out = S.ALL
    for e, lm in enumerate(eqs):
        val = (syndrome >> e) & 1
        if lm == 0:
            if val:
                return 0
            continue
        w = S.WALSH[lm]
        out &= w if val else (w ^ S.ALL)
        if out == 0:
            return 0
    return out


def fixed_support_masks(can, pred):
    eqs, toggles, rhsbits = support_desc(can, pred)
    basis = S.row_basis(toggles)
    out = set()
    for bits in range(1 << len(basis)):
        syndrome = rhsbits
        for i, v in enumerate(basis):
            if (bits >> i) & 1:
                syndrome ^= v
        m = left_support_mask(eqs, syndrome)
        if m:
            out.add(m)

    if fixed_possible(can, pred):
        assert out
    return out, len(basis)


def specialized_e0_basis(pos, pred):
    e0, _e1, _half = H.classify_patterns()
    groups = {}
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = H.support_for(pos, zs, cls)
            if can is None or not fixed_possible(can, pred):
                continue
            raw += 1
            qbits, cross, _rank, _pr = specialized_phase_data(pos, zs, pred)
            if can not in groups:
                groups[can] = [0, [0] * len(RIGHT), 0]
            g = groups[can]
            g[0] ^= qbits
            g[1] = [a ^ b for a, b in zip(g[1], cross)]
            g[2] += 1

    expected_raw = 555 if pos == 'B' else 557
    expected_groups = 243 if pos == 'B' else 244
    assert raw == expected_raw, (pos, raw)
    assert len(groups) == expected_groups, (pos, len(groups))

    out = {}
    cross_hist = Counter()
    support_image_hist = Counter()
    syndrome_rank_hist = Counter()

    for can, (qbits, cross, _n) in groups.items():
        cb = S.row_basis(cross)
        cross_hist[len(cb)] += 1
        masks, srank = fixed_support_masks(can, pred)
        support_image_hist[len(masks)] += 1
        syndrome_rank_hist[srank] += 1

        local = [qbits, S.ALL] + [S.WALSH[f] for f in cb]
        for support_mask in masks:
            for g in local:
                S.insert(out, support_mask & g)

    print(
        'position', pos,
        'fixed_predecessor_e0_raw', raw,
        'fixed_predecessor_e0_support_groups', len(groups),
        'fixed_predecessor_cross_rank_distribution', dict(sorted(cross_hist.items())),
        'fixed_support_syndrome_rank_distribution', dict(sorted(syndrome_rank_hist.items())),
        'fixed_support_mask_count_distribution', dict(sorted(support_image_hist.items())),
        'specialized_e0_rank_F2<=', len(out),
        flush=True,
    )
    return out


def specialized_half_basis(pos, pred):
    _e0, _e1, half = H.classify_patterns()
    assert len(half) == 4

    cans = []
    Q = []
    AS = []
    cross_ranks = []
    for zs, cls in half:
        assert cls == (128, 0, 0)
        can = H.support_for(pos, zs, cls)
        assert can is not None and fixed_possible(can, pred)
        cans.append(can)

        qbits, cross, rank, pr = specialized_phase_data(pos, zs, pred)
        assert rank == 128 and pr == 0
        cb = S.row_basis(cross)
        cross_ranks.append(len(cb))
        Q.append(qbits)
        AS.append(S.row_basis([S.ALL] + [S.WALSH[f] for f in cb]))

    assert all(can == cans[0] for can in cans)
    core_gens = [S.ALL]
    for i in range(4):
        core_gens.append(Q[i])
        core_gens.extend(AS[i])
    for i in range(4):
        for j in range(i + 1, 4):
            core_gens.append(Q[i] & Q[j])
            core_gens.extend(a & Q[j] for a in AS[i])
            core_gens.extend(Q[i] & b for b in AS[j])
            core_gens.extend(a & b for a in AS[i] for b in AS[j])

    core = S.row_basis(core_gens)
    masks, srank = fixed_support_masks(cans[0], pred)
    HB = {}
    for support_mask in masks:
        for g in core:
            S.insert(HB, support_mask & g)

    print(
        'position', pos,
        'fixed_half_cross_ranks', cross_ranks,
        'fixed_half_core_span', len(core),
        'fixed_half_support_syndrome_rank', srank,
        'fixed_half_support_masks', len(masks),
        'specialized_half_rank_F2<=', len(HB),
        flush=True,
    )
    return HB


def main():
    baseline = {'B': (348, 144, 812), 'C': (432, 184, 972)}
    for pos in 'BC':
        pred = WITNESS[pos]
        E = specialized_e0_basis(pos, pred)
        HH = specialized_half_basis(pos, pred)
        U = S.union_basis(E, HH)

        support = N.weight120_union(pos)
        expected_support = 668 if pos == 'B' else 788
        assert len(support) == expected_support

        qr, comp = R.quotient_rank(U, support)
        total = len(support) + qr
        old_sign, old_qr, old_total = baseline[pos]

        print(
            'position', pos,
            'witness_predecessor_hex', hex(pred),
            'specialized_sign_GF2_basis_dim', len(U),
            'baseline_sign_GF2_basis_dim', old_sign,
            'Walsh_complement_coordinates', comp,
            'specialized_exact_ZZ_quotient_rank', qr,
            'baseline_exact_ZZ_quotient_rank', old_qr,
            'specialized_second_lift_rank<=', total,
            'baseline_second_lift_rank<=', old_total,
            'sign_basis_gain', old_sign - len(U),
            'quotient_gain', old_qr - qr,
            'second_lift_gain', old_total - total,
            flush=True,
        )

    print('PASS V26_Q138_BC_SECOND_RESIDUE_FIXED_PREDECESSOR_SPECIALIZATION')
    print('scope=explicit max-overlap predecessor witnesses; diagnostic, not a uniform second-lift theorem')
    print('exact=predecessor phase specialization and reachable left-support syndrome images')
    print('relaxation=support/cross-frequency coupling and right-only phase signs remain span-relaxed; support-only U120 remains global')


if __name__ == '__main__':
    main()
