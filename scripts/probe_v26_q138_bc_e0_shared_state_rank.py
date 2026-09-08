#!/usr/bin/env python3
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_bc_half_uniform_linear_state_relaxed_scalar as U

PRED_BITS = 128
RIGHT_BITS = len(U.F.RIGHT)


def pack_group_support_and_freqs(syndrome, freqs, syndrome_bits):
    z = syndrome
    shift = syndrome_bits
    for f in freqs:
        z |= f << shift
        shift += len(U.F.LEFT)
    return z


def analyze(pos):
    e0, _e1, _half = U.H.classify_patterns()
    groups = defaultdict(list)
    raw = 0

    for k in range(4):
        for zs, cls in e0[k]:
            can = U.H.support_for(pos, zs, cls)
            if can is None:
                continue
            raw += 1
            groups[can].append((zs, cls))

    expected_raw = 581 if pos == 'B' else 577
    expected_groups = 251 if pos == 'B' else 250
    assert raw == expected_raw, (pos, raw)
    assert len(groups) == expected_groups, (pos, len(groups))

    pred_generators = [0] * PRED_BITS
    right_generators = [0] * RIGHT_BITS
    total_signature_bits = 0
    checkpoint = []
    multiplicity_hist = defaultdict(int)
    syndrome_hist = defaultdict(int)

    for gi, (can, sectors) in enumerate(sorted(groups.items(), key=lambda kv: kv[0])):
        multiplicity_hist[len(sectors)] += 1

        cond = U.G.predecessor_condition(can)
        sol = U.T.rref(cond, n=PRED_BITS)
        assert sol is not None
        p0 = sol[1]
        assert U.F.fixed_possible(can, p0)

        eqs, toggles, _rhsbits = U.F.support_desc(can, p0)
        syndrome_bits = len(eqs)
        syndrome_hist[syndrome_bits] += 1
        assert len(toggles) == RIGHT_BITS

        phases = []
        crosses = []
        for zs, _cls in sectors:
            _c, _lin, polar, _rank, _pr = U.X.full_corrected_phase(
                pos, U.D.carries(zs)
            )
            phases.append(polar)

            _q, cross, _rank2, _pr2 = U.F.specialized_phase_data(pos, zs, p0)
            assert len(cross) == RIGHT_BITS
            crosses.append(cross)

        group_width = syndrome_bits + len(sectors) * len(U.F.LEFT)

        for i in range(PRED_BITS):
            d = 1 << i
            sd = U.pred_support_delta(can, d)
            freqs = [U.pred_left_freq(polar, d) for polar in phases]
            local = pack_group_support_and_freqs(sd, freqs, syndrome_bits)
            pred_generators[i] |= local << total_signature_bits

        for j in range(RIGHT_BITS):
            freqs = [cross[j] for cross in crosses]
            local = pack_group_support_and_freqs(toggles[j], freqs, syndrome_bits)
            right_generators[j] |= local << total_signature_bits

        total_signature_bits += group_width

        if (gi + 1) % 25 == 0 or gi + 1 == len(groups):
            rp = len(S.row_basis(pred_generators))
            rr = len(S.row_basis(right_generators))
            rj = len(S.row_basis(pred_generators + right_generators))
            checkpoint.append((gi + 1, total_signature_bits, rp, rr, rj))

    pred_rank = len(S.row_basis(pred_generators))
    right_rank = len(S.row_basis(right_generators))
    joint_rank = len(S.row_basis(pred_generators + right_generators))

    # The full shared linear state is driven by at most 128 predecessor bits
    # plus the 21 right-beta coordinates. Scalar phase bits are deliberately
    # omitted here; they are quadratic data and are not part of this linear
    # feasibility diagnostic.
    assert joint_rank <= PRED_BITS + RIGHT_BITS

    print(
        'position', pos,
        'raw_e0_sectors', raw,
        'support_groups', len(groups),
        'group_multiplicity_histogram', dict(sorted(multiplicity_hist.items())),
        'support_syndrome_bits_histogram', dict(sorted(syndrome_hist.items())),
        'packed_shared_signature_bits', total_signature_bits,
        'predecessor_generator_rank', pred_rank,
        'right_generator_rank', right_rank,
        'joint_pred_right_shared_linear_state_rank', joint_rank,
        'joint_state_count_if_enumerated', 1 << joint_rank,
        'rank_checkpoints', checkpoint,
        flush=True,
    )

    return {
        'groups': len(groups),
        'packed_bits': total_signature_bits,
        'pred_rank': pred_rank,
        'right_rank': right_rank,
        'joint_rank': joint_rank,
    }


def main():
    out = {pos: analyze(pos) for pos in 'BC'}
    print('result', out)
    print('PASS V26_Q138_BC_E0_SHARED_STATE_RANK')
    print('scope=rank-only diagnostic for the single shared predecessor/right linear state seen simultaneously by every grouped-e0 support syndrome and every sector left-frequency map')
    print('not_included=quadratic scalar phases, e0 carry evaluation, e0-half cross-carry, complete B2/C2, W_repr, alpha, arithmetic-work, ranking/search, full-round')


if __name__ == '__main__':
    main()
