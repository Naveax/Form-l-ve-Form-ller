#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import probe_v26_q138_bc_direct_e1_exact_sector_cancellation as X
import probe_v26_q138_bc_second_residue_fixed_predecessor_specialization as F

NRIGHT = len(F.RIGHT)
assert NRIGHT == 21


def in_span(B, x):
    y = x
    while y:
        p = y.bit_length() - 1
        if p not in B:
            return False
        y ^= B[p]
    return True


def half_correction(qs):
    assert len(qs) == 4
    z = S.ALL
    for q in qs:
        z ^= q
    for i in range(4):
        for j in range(i + 1, 4):
            z ^= qs[i] & qs[j]
    return z


def right_model(pos, zs, pred):
    c, lin, polar, rank, pr = X.full_corrected_phase(pos, D.carries(zs))
    assert rank == 128 and pr == 0
    qbits, cross, rank2, pr2 = F.specialized_phase_data(pos, zs, pred)
    assert rank2 == rank and pr2 == pr

    lin_local = 0
    quad_rows = []
    for j, er in enumerate(F.REXT):
        a = ((lin >> er) & 1) ^ ((polar[er] & pred).bit_count() & 1)
        if a:
            lin_local |= 1 << j

        row = 0
        for k, ek in enumerate(F.REXT):
            if (polar[er] >> ek) & 1:
                row |= 1 << k
        assert ((row >> j) & 1) == 0
        quad_rows.append(row)

    def direct_delta(r):
        ext = pred
        for j, er in enumerate(F.REXT):
            if (r >> j) & 1:
                ext |= 1 << er
        return X.q_eval(c, lin, polar, ext) ^ X.q_eval(c, lin, polar, pred)

    def model_delta(r):
        z = (lin_local & r).bit_count() & 1
        for j in range(NRIGHT):
            if (r >> j) & 1:
                hi = r & ~((1 << (j + 1)) - 1)
                z ^= (quad_rows[j] & hi).bit_count() & 1
        return z

    tests = [0, 1, 2, 3, 5, 0x15555, 0x1AAAA, (1 << NRIGHT) - 1]
    for r in tests:
        r &= (1 << NRIGHT) - 1
        assert direct_delta(r) == model_delta(r), (pos, zs, r)

    return qbits, tuple(cross), lin_local, tuple(quad_rows)


def exact_half_basis(pos, pred):
    _e0, _e1, half = H.classify_patterns()
    assert len(half) == 4

    cans = []
    Q = []
    crosses = []
    linlocals = []
    qrows = []
    for zs, cls in half:
        assert cls == (128, 0, 0)
        can = H.support_for(pos, zs, cls)
        assert can is not None and F.fixed_possible(can, pred)
        cans.append(can)
        q, cross, linlocal, qr = right_model(pos, zs, pred)
        Q.append(q)
        crosses.append(cross)
        linlocals.append(linlocal)
        qrows.append(qr)

    assert all(can == cans[0] for can in cans)
    eqs, toggles, rhsbits = F.support_desc(cans[0], pred)
    syndrome_bits = len(eqs)
    syndrome_mask = (1 << syndrome_bits) - 1

    joint_gen = []
    for j in range(NRIGHT):
        z = toggles[j]
        shift = syndrome_bits
        for i in range(4):
            z |= crosses[i][j] << shift
            shift += len(F.LEFT)
        joint_gen.append(z)

    scalar_sets = {0: 1}
    gray = 0
    joint = 0
    scalar = 0
    for step in range(1, 1 << NRIGHT):
        j = (step & -step).bit_length() - 1
        d = 0
        for i in range(4):
            bit = ((linlocals[i] >> j) & 1) ^ ((qrows[i][j] & gray).bit_count() & 1)
            d |= bit << i
        scalar ^= d
        gray ^= 1 << j
        joint ^= joint_gen[j]
        scalar_sets[joint] = scalar_sets.get(joint, 0) | (1 << scalar)

    distinct_pairs = sum(mask.bit_count() for mask in scalar_sets.values())
    assert distinct_pairs <= (1 << NRIGHT)

    HB = {}
    feasible_linear_states = 0
    feasible_pairs = 0
    support_cache = {}

    for joint, scalarmask in scalar_sets.items():
        synd = rhsbits ^ (joint & syndrome_mask)
        if synd not in support_cache:
            support_cache[synd] = F.left_support_mask(eqs, synd)
        sm = support_cache[synd]
        if sm == 0:
            continue
        feasible_linear_states += 1

        freqs = []
        shift = syndrome_bits
        for _ in range(4):
            freqs.append((joint >> shift) & ((1 << len(F.LEFT)) - 1))
            shift += len(F.LEFT)

        m = scalarmask
        while m:
            b = m & -m
            scalarpat = b.bit_length() - 1
            m ^= b
            feasible_pairs += 1

            qs = []
            for i in range(4):
                q = Q[i] ^ S.WALSH[freqs[i]]
                if (scalarpat >> i) & 1:
                    q ^= S.ALL
                qs.append(q)

            vec = sm & half_correction(qs)
            S.insert(HB, vec)

    old = F.specialized_half_basis(pos, pred)
    expected_old = 212 if pos == 'B' else 280
    assert len(old) == expected_old, (pos, len(old))
    assert all(in_span(old, v) for v in HB.values())

    print(
        'position', pos,
        'right_assignments', 1 << NRIGHT,
        'distinct_joint_linear_states', len(scalar_sets),
        'distinct_joint_scalar_pairs', distinct_pairs,
        'feasible_joint_linear_states', feasible_linear_states,
        'feasible_joint_scalar_pairs', feasible_pairs,
        'support_syndrome_cache_size', len(support_cache),
        'exact_half_rank_F2', len(HB),
        'old_specialized_half_rank_F2<=', len(old),
        'half_rank_gain', len(old) - len(HB),
        flush=True,
    )
    return HB


def main():
    for pos in 'BC':
        exact_half_basis(pos, F.WITNESS[pos])

    print('PASS V26_Q138_BC_SECOND_RESIDUE_HALF_EXACT_RIGHT21')
    print('scope=exact half-sector second-bit correction at explicit max-overlap predecessor witnesses')
    print('exact=common support, four cross frequencies, and four right-only scalar phases tracked on all 2^21 right-beta assignments')
    print('not_uniform=no uniform B/C second-lift or representation claim')


if __name__ == '__main__':
    main()
