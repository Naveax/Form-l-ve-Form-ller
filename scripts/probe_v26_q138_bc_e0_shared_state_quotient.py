#!/usr/bin/env python3
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_bc_half_uniform_linear_state_relaxed_scalar as U

PRED_BITS = 128
RIGHT_BITS = len(U.F.RIGHT)
DOMAIN_BITS = PRED_BITS + RIGHT_BITS


def rank(rows):
    return len(S.row_basis(rows))


def component_ranks(pred_rows, right_rows):
    pred_rank = rank(pred_rows)
    right_rank = rank(right_rows)
    joint_rank = rank(pred_rows + right_rows)
    return {
        'pred_rank': pred_rank,
        'right_rank': right_rank,
        'joint_rank': joint_rank,
        'right_quotient_over_pred': joint_rank - pred_rank,
        'pred_quotient_over_right': joint_rank - right_rank,
        'domain_kernel_dim': DOMAIN_BITS - joint_rank,
    }


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

    support_pred = [0] * PRED_BITS
    support_right = [0] * RIGHT_BITS
    freq_pred = [0] * PRED_BITS
    freq_right = [0] * RIGHT_BITS

    support_offset = 0
    freq_offset = 0
    multiplicity_hist = defaultdict(int)
    syndrome_hist = defaultdict(int)
    checkpoints = []

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

        for i in range(PRED_BITS):
            d = 1 << i
            support_pred[i] |= U.pred_support_delta(can, d) << support_offset

            local_freq = 0
            shift = 0
            for polar in phases:
                local_freq |= U.pred_left_freq(polar, d) << shift
                shift += len(U.F.LEFT)
            freq_pred[i] |= local_freq << freq_offset

        for j in range(RIGHT_BITS):
            support_right[j] |= toggles[j] << support_offset

            local_freq = 0
            shift = 0
            for cross in crosses:
                local_freq |= cross[j] << shift
                shift += len(U.F.LEFT)
            freq_right[j] |= local_freq << freq_offset

        support_offset += syndrome_bits
        freq_offset += len(sectors) * len(U.F.LEFT)

        if (gi + 1) % 25 == 0 or gi + 1 == len(groups):
            sr = rank(support_pred + support_right)
            fr = rank(freq_pred + freq_right)
            combined_pred = [
                support_pred[i] | (freq_pred[i] << support_offset)
                for i in range(PRED_BITS)
            ]
            combined_right = [
                support_right[j] | (freq_right[j] << support_offset)
                for j in range(RIGHT_BITS)
            ]
            jr = rank(combined_pred + combined_right)
            checkpoints.append(
                {
                    'groups': gi + 1,
                    'support_bits': support_offset,
                    'frequency_bits': freq_offset,
                    'support_rank': sr,
                    'frequency_rank': fr,
                    'joint_rank': jr,
                }
            )

    support_stats = component_ranks(support_pred, support_right)
    freq_stats = component_ranks(freq_pred, freq_right)

    combined_pred = [
        support_pred[i] | (freq_pred[i] << support_offset)
        for i in range(PRED_BITS)
    ]
    combined_right = [
        support_right[j] | (freq_right[j] << support_offset)
        for j in range(RIGHT_BITS)
    ]
    combined_stats = component_ranks(combined_pred, combined_right)

    # Regression against PR110: the complete shared linear signature map is
    # injective on the 128 predecessor + 21 right-beta coordinates.
    assert combined_stats['joint_rank'] == DOMAIN_BITS, (pos, combined_stats)
    assert combined_stats['domain_kernel_dim'] == 0

    # Exact conditional dimensions.  For linear maps A=support and B=frequency,
    # rank(A,B)-rank(A) = rank(B restricted to ker A).  This is the number of
    # frequency degrees of freedom that remain after the support signature is
    # fixed; the symmetric expression has the analogous meaning.
    freq_given_support = DOMAIN_BITS - support_stats['joint_rank']
    support_given_freq = DOMAIN_BITS - freq_stats['joint_rank']
    shared_measurement_redundancy = (
        support_stats['joint_rank']
        + freq_stats['joint_rank']
        - combined_stats['joint_rank']
    )

    out = {
        'position': pos,
        'raw_e0_sectors': raw,
        'support_groups': len(groups),
        'support_signature_bits': support_offset,
        'frequency_signature_bits': freq_offset,
        'group_multiplicity_histogram': dict(sorted(multiplicity_hist.items())),
        'support_syndrome_bits_histogram': dict(sorted(syndrome_hist.items())),
        'support_component': support_stats,
        'frequency_component': freq_stats,
        'combined_component': combined_stats,
        'frequency_residual_dim_given_support': freq_given_support,
        'support_residual_dim_given_frequency': support_given_freq,
        'shared_measurement_redundancy_dim': shared_measurement_redundancy,
        'checkpoints': checkpoints,
    }
    print(json.dumps(out, sort_keys=True), flush=True)
    return out


def main():
    out = {pos: analyze(pos) for pos in 'BC'}
    print('result', json.dumps(out, sort_keys=True))
    print('PASS V26_Q138_BC_E0_SHARED_STATE_QUOTIENT')
    print(
        'scope=exact GF2 quotient diagnostic splitting the PR110 shared e0 linear state into support-syndrome and left-frequency channels'
    )
    print(
        'not_included=quadratic scalar phases, grouped-e0 carry evaluation, e0-half cross-carry, complete B2/C2, W_repr, alpha, arithmetic-work, ranking/search, full-round'
    )


if __name__ == '__main__':
    main()
