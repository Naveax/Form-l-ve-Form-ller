#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import verify_v26_q138_predecessor_leaf_bc_second_residue_support_frequency_nesting as N
import verify_v26_q138_predecessor_leaf_bc_second_residue_rank812_972 as R
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import probe_v26_q138_bc_second_residue_fixed_predecessor_specialization as F


def span_states(basis):
    states = [0]
    for v in basis:
        states += [x ^ v for x in states]
    return states


def joint_e0_basis(pos, pred):
    e0, _e1, _half = H.classify_patterns()
    groups = {}
    raw = 0

    for k in range(4):
        for zs, cls in e0[k]:
            can = H.support_for(pos, zs, cls)
            if can is None or not F.fixed_possible(can, pred):
                continue
            raw += 1
            qbits, cross, _rank, _pr = F.specialized_phase_data(pos, zs, pred)
            if can not in groups:
                groups[can] = [0, [0] * len(F.RIGHT), 0]
            g = groups[can]
            g[0] ^= qbits
            g[1] = [a ^ b for a, b in zip(g[1], cross)]
            g[2] += 1

    expected_raw = 555 if pos == 'B' else 557
    expected_groups = 243 if pos == 'B' else 244
    assert raw == expected_raw, (pos, raw)
    assert len(groups) == expected_groups, (pos, len(groups))

    out = {}
    joint_rank_hist = Counter()
    image_state_hist = Counter()
    feasible_state_hist = Counter()
    distinct_pair_hist = Counter()
    max_joint = 0
    total_image_states = 0
    total_feasible_states = 0

    for can, (qbits, cross, _n) in groups.items():
        eqs, toggles, rhsbits = F.support_desc(can, pred)
        syndrome_bits = len(eqs)
        packed = [
            toggles[j] | (cross[j] << syndrome_bits)
            for j in range(len(F.RIGHT))
        ]
        jb = S.row_basis(packed)
        jr = len(jb)
        assert jr <= 18, (pos, jr)
        max_joint = max(max_joint, jr)
        joint_rank_hist[jr] += 1

        states = span_states(jb)
        assert len(states) == 1 << jr
        image_state_hist[len(states)] += 1
        total_image_states += len(states)

        seen_pairs = set()
        feasible = 0
        smask = (1 << syndrome_bits) - 1

        for z in states:
            syndrome = rhsbits ^ (z & smask)
            freq = z >> syndrome_bits
            assert 0 <= freq < (1 << len(F.LEFT))
            pair = (syndrome, freq)
            assert pair not in seen_pairs
            seen_pairs.add(pair)

            support_mask = F.left_support_mask(eqs, syndrome)
            if support_mask == 0:
                continue
            feasible += 1

            # Exact left phase for this common right-beta image, except for
            # the right-only scalar phase. Relax that scalar independently:
            # span{m&(q^W_f), m} contains either possible actual vector
            # m&(q^W_f^c*ALL), c in F2.
            phase = qbits ^ S.WALSH[freq]
            S.insert(out, support_mask & phase)
            S.insert(out, support_mask)

        feasible_state_hist[feasible] += 1
        distinct_pair_hist[len(seen_pairs)] += 1
        total_feasible_states += feasible

    print(
        'position', pos,
        'fixed_e0_raw', raw,
        'fixed_e0_groups', len(groups),
        'joint_rank_distribution', dict(sorted(joint_rank_hist.items())),
        'max_joint_rank', max_joint,
        'total_joint_image_states', total_image_states,
        'total_feasible_joint_states', total_feasible_states,
        'joint_image_state_count_distribution', dict(sorted(image_state_hist.items())),
        'feasible_joint_state_count_distribution', dict(sorted(feasible_state_hist.items())),
        'distinct_joint_pair_count_distribution', dict(sorted(distinct_pair_hist.items())),
        'joint_e0_rightscalar_relaxed_rank_F2<=', len(out),
        flush=True,
    )
    return out


def main():
    old_specialized = {'B': (272, 332, 141, 809), 'C': (388, 432, 198, 986)}
    uniform = {'B': 812, 'C': 972}

    for pos in 'BC':
        pred = F.WITNESS[pos]
        E = joint_e0_basis(pos, pred)

        # Keep the already-validated fixed-predecessor half-sector span.
        # This probe tightens only e0 support/cross coupling.
        HH = F.specialized_half_basis(pos, pred)
        U = S.union_basis(E, HH)

        support = N.weight120_union(pos)
        expected_support = 668 if pos == 'B' else 788
        assert len(support) == expected_support

        qr, comp = R.quotient_rank(U, support)
        total = len(support) + qr
        old_e0, old_sign, old_qr, old_total = old_specialized[pos]

        print(
            'position', pos,
            'witness_predecessor_hex', hex(pred),
            'joint_e0_rank_F2<=', len(E),
            'old_independent_specialized_e0_rank_F2<=', old_e0,
            'e0_basis_gain', old_e0 - len(E),
            'joint_e0_plus_old_half_sign_basis_dim', len(U),
            'old_specialized_sign_basis_dim', old_sign,
            'sign_basis_gain', old_sign - len(U),
            'Walsh_complement_coordinates', comp,
            'joint_exact_ZZ_quotient_rank', qr,
            'old_specialized_exact_ZZ_quotient_rank', old_qr,
            'quotient_gain', old_qr - qr,
            'joint_second_lift_rank<=', total,
            'old_specialized_second_lift_rank<=', old_total,
            'witness_gain', old_total - total,
            'current_uniform_bound', uniform[pos],
            flush=True,
        )

    print('PASS V26_Q138_BC_SECOND_RESIDUE_E0_JOINT_ENUMERATION')
    print('scope=explicit max-overlap predecessor witnesses; not a uniform second-lift theorem')
    print('exact=e0 common right-beta support-syndrome/cross-frequency image enumeration')
    print('relaxation=e0 right-only scalar phase independent; half uses prior specialized span; U120 remains global')


if __name__ == '__main__':
    main()
