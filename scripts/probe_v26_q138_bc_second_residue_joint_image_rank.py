#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import probe_v26_q138_bc_second_residue_fixed_predecessor_specialization as F


def rank_of(vs):
    return len(S.row_basis(vs))


def pack_joint(toggles, cross_families, syndrome_bits):
    out = []
    for j in range(len(F.RIGHT)):
        z = toggles[j]
        shift = syndrome_bits
        for cross in cross_families:
            z |= cross[j] << shift
            shift += len(F.LEFT)
        out.append(z)
    return out


def e0_joint_ranks(pos, pred):
    e0, _e1, _half = H.classify_patterns()
    groups = {}
    for k in range(4):
        for zs, cls in e0[k]:
            can = H.support_for(pos, zs, cls)
            if can is None or not F.fixed_possible(can, pred):
                continue
            _qbits, cross, _rank, _pr = F.specialized_phase_data(pos, zs, pred)
            if can not in groups:
                groups[can] = [0] * len(F.RIGHT)
            groups[can] = [a ^ b for a, b in zip(groups[can], cross)]

    expected = 243 if pos == 'B' else 244
    assert len(groups) == expected, (pos, len(groups))

    hist = Counter()
    excess_hist = Counter()
    max_joint = 0
    max_product_states = 0
    max_joint_states = 0
    correlated = 0

    for can, cross in groups.items():
        eqs, toggles, _rhs = F.support_desc(can, pred)
        sr = rank_of(toggles)
        cr = rank_of(cross)
        jr = rank_of(pack_joint(toggles, [cross], len(eqs)))
        assert max(sr, cr) <= jr <= min(len(F.RIGHT), sr + cr)
        excess = sr + cr - jr
        if excess:
            correlated += 1
        hist[(sr, cr, jr)] += 1
        excess_hist[excess] += 1
        max_joint = max(max_joint, jr)
        max_product_states = max(max_product_states, 1 << (sr + cr))
        max_joint_states = max(max_joint_states, 1 << jr)

    print(
        'position', pos,
        'e0_groups', len(groups),
        'support_cross_joint_rank_distribution', dict(sorted(hist.items())),
        'cartesian_excess_rank_distribution', dict(sorted(excess_hist.items())),
        'groups_with_strict_support_cross_correlation', correlated,
        'max_joint_rank', max_joint,
        'max_joint_states', max_joint_states,
        'max_independent_cartesian_states', max_product_states,
        flush=True,
    )
    return max_joint, correlated


def half_joint_rank(pos, pred):
    _e0, _e1, half = H.classify_patterns()
    assert len(half) == 4
    cans = []
    crosses = []
    for zs, cls in half:
        can = H.support_for(pos, zs, cls)
        assert can is not None and F.fixed_possible(can, pred)
        cans.append(can)
        _qbits, cross, rank, pr = F.specialized_phase_data(pos, zs, pred)
        assert rank == 128 and pr == 0
        crosses.append(cross)
    assert all(can == cans[0] for can in cans)

    eqs, toggles, _rhs = F.support_desc(cans[0], pred)
    sr = rank_of(toggles)
    crs = [rank_of(c) for c in crosses]
    phase_joint = rank_of(pack_joint([0] * len(F.RIGHT), crosses, len(eqs)))
    full_joint = rank_of(pack_joint(toggles, crosses, len(eqs)))
    assert max([sr, phase_joint] + crs) <= full_joint <= len(F.RIGHT)

    independent = sr + sum(crs)
    phase_independent = sum(crs)
    print(
        'position', pos,
        'half_support_rank', sr,
        'half_cross_ranks', crs,
        'half_phase_joint_rank', phase_joint,
        'half_full_joint_rank', full_joint,
        'half_phase_cartesian_excess', phase_independent - phase_joint,
        'half_full_cartesian_excess', independent - full_joint,
        'half_full_joint_states', 1 << full_joint,
        flush=True,
    )
    return full_joint


def main():
    for pos in 'BC':
        pred = F.WITNESS[pos]
        e0_max, correlated = e0_joint_ranks(pos, pred)
        half_max = half_joint_rank(pos, pred)
        print(
            'position', pos,
            'enumeration_guidance',
            'e0_joint_exact_enumeration_feasible' if e0_max <= 18 else 'e0_joint_rank_too_large_for_naive_per_group_enumeration',
            'half_joint_exact_enumeration_feasible' if half_max <= 18 else 'half_joint_rank_too_large_for_naive_enumeration',
            'strict_correlation_groups', correlated,
            flush=True,
        )

    print('PASS V26_Q138_BC_SECOND_RESIDUE_JOINT_IMAGE_RANK')
    print('scope=rank-only diagnostic for common right-beta support/phase images at the explicit max-overlap predecessors')
    print('no_second_lift_rank_or_uniform_claim')


if __name__ == '__main__':
    main()
