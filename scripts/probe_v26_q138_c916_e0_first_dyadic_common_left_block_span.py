#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_same_support_integer_coefficients as C
import probe_v26_q138_c916_e0_first_dyadic_pair_residual as D

POS = 'C'
NEXT = 160
SHARED_EXT = tuple(range(128)) + tuple(C.P.U.F.REXT)
LOCAL_EXT = tuple(C.P.U.F.LEXT)
assert len(SHARED_EXT) == 149 and len(LOCAL_EXT) == 11
assert set(SHARED_EXT).isdisjoint(LOCAL_EXT)
assert set(SHARED_EXT) | set(LOCAL_EXT) == set(range(NEXT))
LOCAL_PAIR_BITS = 11 * 10 // 2
CROSS_BITS = 149 * 11


def xor_phase(a, b):
    assert len(a[2]) == len(b[2]) == NEXT
    return (
        a[0] ^ b[0],
        a[1] ^ b[1],
        tuple(x ^ y for x, y in zip(a[2], b[2])),
        None,
        None,
    )


def block_data(phase):
    c, lin, polar, _rank, _pr = phase
    assert len(polar) == NEXT

    local_lin = 0
    for j, ext in enumerate(LOCAL_EXT):
        if (lin >> ext) & 1:
            local_lin |= 1 << j

    local_quad = 0
    bit = 0
    for a in range(len(LOCAL_EXT)):
        ea = LOCAL_EXT[a]
        for b in range(a + 1, len(LOCAL_EXT)):
            eb = LOCAL_EXT[b]
            if (polar[ea] >> eb) & 1:
                local_quad |= 1 << bit
            bit += 1
    assert bit == LOCAL_PAIR_BITS

    cross = 0
    cross_rows = []
    for si, se in enumerate(SHARED_EXT):
        row = 0
        for lj, le in enumerate(LOCAL_EXT):
            if (polar[se] >> le) & 1:
                row |= 1 << lj
                cross |= 1 << (si * 11 + lj)
        cross_rows.append(row)
    assert cross >> CROSS_BITS == 0

    return {
        'constant': c & 1,
        'local_linear': local_lin,
        'local_quadratic': local_quad,
        'local_polynomial': local_quad | (local_lin << LOCAL_PAIR_BITS) | ((c & 1) << (LOCAL_PAIR_BITS + 11)),
        'cross_flat': cross,
        'cross_rank': D.gf2_rank(cross_rows),
        'cross_rows': tuple(cross_rows),
    }


def span_rank(values):
    return D.gf2_rank(values)


def joint_shared_control_rank(blocks):
    # For shared input x, each term receives an 11-bit local-frequency shift
    # M_t^T x. Concatenate those outputs over all terms and rank the resulting
    # 149 input-coordinate rows.
    rows = []
    for si in range(149):
        row = 0
        for t, b in enumerate(blocks):
            row |= b['cross_rows'][si] << (11 * t)
        rows.append(row)
    return span_rank(rows)


def summary(blocks):
    return {
        'terms': len(blocks),
        'local_quadratic_span_rank': span_rank(b['local_quadratic'] for b in blocks),
        'local_linear_span_rank': span_rank(b['local_linear'] for b in blocks),
        'local_polynomial_span_rank': span_rank(b['local_polynomial'] for b in blocks),
        'cross_matrix_coefficient_span_rank': span_rank(b['cross_flat'] for b in blocks),
        'joint_shared_to_local_frequency_control_rank': joint_shared_control_rank(blocks),
        'per_term_cross_rank_histogram': dict(sorted(Counter(b['cross_rank'] for b in blocks).items())),
    }


def analyze():
    pair_out = D.analyze()
    pair_groups = {g['group_id']: g for g in pair_out['groups']}
    assert len(pair_groups) == 147

    e0, _e1, _half = C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    for k in range(4):
        for zs, cls in e0[k]:
            can = C.P.U.H.support_for(POS, zs, cls)
            if can is not None:
                grouped[can].append((zs, cls))
    assert len(grouped) == 250

    singleton_anchor = []
    pair_anchor = []
    pair_difference = []
    anchor_all = []
    pair_by_mult_anchor = defaultdict(list)
    pair_by_mult_difference = defaultdict(list)

    for gid, (_can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        phases = [C.phase_tuple(zs) for zs, _cls in sectors]
        m = len(sectors)
        if m == 1:
            b = block_data(phases[0])
            singleton_anchor.append(b)
            anchor_all.append(b)
            continue

        pg = pair_groups[gid]
        assert pg['multiplicity'] == m
        for selected in pg['selected_pairs']:
            i, j = selected['pair']
            a = block_data(phases[i])
            d = block_data(xor_phase(phases[i], phases[j]))
            pair_anchor.append(a)
            pair_difference.append(d)
            anchor_all.append(a)
            pair_by_mult_anchor[m].append(a)
            pair_by_mult_difference[m].append(d)

    assert len(singleton_anchor) == 103
    assert len(pair_anchor) == len(pair_difference) == 237
    assert len(anchor_all) == 340

    out = {
        'position': POS,
        'shared_external_bits': len(SHARED_EXT),
        'local_left_external_bits': len(LOCAL_EXT),
        'local_quadratic_ambient_bits': LOCAL_PAIR_BITS,
        'shared_local_bilinear_ambient_bits': CROSS_BITS,
        'singleton_anchor': summary(singleton_anchor),
        'pair_anchor': summary(pair_anchor),
        'all_340_anchor_phases': summary(anchor_all),
        'pair_difference': summary(pair_difference),
        'pair_anchor_by_multiplicity': {
            int(m): summary(v) for m, v in sorted(pair_by_mult_anchor.items())
        },
        'pair_difference_by_multiplicity': {
            int(m): summary(v) for m, v in sorted(pair_by_mult_difference.items())
        },
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_COMMON_LEFT_BLOCK_SPAN')
    print('scope=exact block decomposition of a valid full 160-coordinate quadratic representative for all 340 first-dyadic anchor phases and 237 selected equality differences')
    print('important=measures common 11-left-variable quadratic and shared-to-left bilinear control spans; it is an exact representation diagnostic, not a minimal separator-state theorem because support constraints can create further gauge reductions')
    print('next=combine these common-coordinate controls with support/frequency factors and the signed equality arithmetic before cut-local message counting')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
