#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as Top
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import verify_v26_q138_predecessor_leaf_bc_second_residue_support_frequency_nesting as N
import verify_v26_q138_predecessor_leaf_bc_second_residue_rank812_972 as R

DOMAIN_BITS = len(S.RIGHT)
LEFT_BITS = len(S.LEFT)
assert DOMAIN_BITS == 149
assert LEFT_BITS == 11


def compress(mask, coords):
    z = 0
    for j, ext in enumerate(coords):
        if (mask >> ext) & 1:
            z |= 1 << j
    return z


def xor_columns(cols, r):
    z = 0
    x = r
    while x:
        b = x & -x
        z ^= cols[b.bit_length() - 1]
        x ^= b
    return z


def span_states(offset, basis):
    states = [offset]
    for b in basis:
        states += [x ^ b for x in states]
    return states


def support_affine_map(can):
    # Convert the affine full-support equations into left equations whose RHS
    # depends affinely on the 149 shared coordinates. Eliminate only on the
    # 11 left columns. Rows left over with zero left part are exact shared-only
    # reachability constraints; they must be enforced before a left support
    # coset exists.
    rows = []
    for row in can:
        rows.append([
            compress(row, S.LEFT),
            compress(row, S.RIGHT),
            (row >> 160) & 1,
        ])

    r = 0
    pivots = []
    for col in range(LEFT_BITS):
        p = next((k for k in range(r, len(rows)) if (rows[k][0] >> col) & 1), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        lm, rm, c = rows[r]
        for k in range(len(rows)):
            if k != r and ((rows[k][0] >> col) & 1):
                rows[k][0] ^= lm
                rows[k][1] ^= rm
                rows[k][2] ^= c
        pivots.append(col)
        r += 1

    pivot_rows = [tuple(x) for x in rows[:r]]
    pure_rows = [tuple(x) for x in rows[r:]]
    assert all(lm == 0 for lm, _rm, _c in pure_rows)
    assert r == len(S.left_basis(can))

    constraints = [(rm, c) for _lm, rm, c in pure_rows]
    sol = Top.rref(constraints, n=DOMAIN_BITS)
    assert sol is not None
    constraint_rank, r0, null_basis = sol
    return pivot_rows, constraint_rank, r0, tuple(null_basis)


def support_mask(pivot_rows, syndrome):
    z = S.ALL
    for i, (lm, _rm, _c) in enumerate(pivot_rows):
        w = S.WALSH[lm]
        z &= w if ((syndrome >> i) & 1) else (w ^ S.ALL)
        if z == 0:
            break
    return z


def joint_image(pivot_rows, cols, r0, null_basis):
    d = len(pivot_rows)

    def affine_out(r):
        y = 0
        for i, (_lm, rm, c) in enumerate(pivot_rows):
            if c ^ ((rm & r).bit_count() & 1):
                y |= 1 << i
        return y | (xor_columns(cols, r) << d)

    def linear_out(r):
        y = 0
        for i, (_lm, rm, _c) in enumerate(pivot_rows):
            if (rm & r).bit_count() & 1:
                y |= 1 << i
        return y | (xor_columns(cols, r) << d)

    offset = affine_out(r0)
    basis = S.row_basis(linear_out(h) for h in null_basis)
    return offset, basis


def canonical_local_insert(out, can, qbits, cols):
    cb = S.row_basis(cols)
    lb = S.left_basis(can)
    local = [qbits, S.ALL] + [S.WALSH[f] for f in cb]
    for smask in S.coset_masks(lb):
        for g in local:
            S.insert(out, smask & g)


def reachable_local_basis(can, qbits, cols):
    pivot_rows, constraint_rank, r0, null_basis = support_affine_map(can)
    support_rank = len(pivot_rows)
    freq_basis = S.row_basis(cols)
    freq_rank = len(freq_basis)
    product_rank = support_rank + freq_rank
    offset, image_basis = joint_image(pivot_rows, cols, r0, null_basis)
    image_rank = len(image_basis)
    assert image_rank <= product_rank

    out = {}
    if image_rank == product_rank:
        # The joint affine image has full dimension in support x frequency, so
        # it is the whole Cartesian product. In this case the canonical local
        # construction is already exact for the gauge-closed target and avoids
        # enumerating up to 2^21 states for singleton groups.
        canonical_local_insert(out, can, qbits, cols)
        mode = 'full_product'
        state_count = 1 << image_rank
    else:
        # Enumerate only genuinely correlated low-dimensional images. For each
        # reachable (support syndrome, frequency), include the phase truth
        # vector and the support mask itself. The latter closes under the
        # right-only scalar gauge: flipping the scalar complements the sign on
        # exactly that support mask.
        mode = 'correlated_image'
        states = span_states(offset, image_basis)
        state_count = len(states)
        smask_cache = {}
        smask_mask = (1 << support_rank) - 1
        for state in states:
            syndrome = state & smask_mask
            freq = state >> support_rank
            smask = smask_cache.get(syndrome)
            if smask is None:
                smask = support_mask(pivot_rows, syndrome)
                assert smask != 0
                smask_cache[syndrome] = smask
            phase = qbits ^ S.WALSH[freq]
            S.insert(out, smask)
            S.insert(out, smask & phase)

    return out, {
        'mode': mode,
        'support_rank': support_rank,
        'frequency_rank': freq_rank,
        'product_rank': product_rank,
        'joint_image_rank': image_rank,
        'rank_gap': product_rank - image_rank,
        'constraint_rank': constraint_rank,
        'state_count': state_count,
        'local_gauge_span_rank': len(out),
    }


def grouped_data(pos):
    e0, _e1, _half = H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = H.support_for(pos, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))

    expected_raw = 581 if pos == 'B' else 577
    expected_groups = 251 if pos == 'B' else 250
    expected_mult = Counter({1: 103, 2: 57, 4: 91 if pos == 'B' else 90})
    assert raw == expected_raw
    assert len(grouped) == expected_groups
    assert Counter(len(v) for v in grouped.values()) == expected_mult
    return raw, sorted(grouped.items(), key=lambda kv: kv[0])


def aggregate_phase(pos, sectors):
    qbits = 0
    cols = [0] * DOMAIN_BITS
    for zs, _cls in sectors:
        q, c, _rank, _meta = S.corrected_phase_data(pos, D.carries(zs))
        qbits ^= q
        cols = [a ^ b for a, b in zip(cols, c)]
    return qbits, tuple(cols)


def analyze(pos):
    raw, groups = grouped_data(pos)
    reachable = {}
    stats = []
    multiplicity_mode = Counter()
    gap_hist = Counter()
    image_rank_hist = Counter()
    constraint_rank_hist = Counter()
    local_rank_hist = Counter()
    total_enumerated_states = 0

    for group_id, (can, sectors) in enumerate(groups):
        qbits, cols = aggregate_phase(pos, sectors)
        local, st = reachable_local_basis(can, qbits, cols)
        st['group_id'] = group_id
        st['multiplicity'] = len(sectors)
        stats.append(st)
        multiplicity_mode[(len(sectors), st['mode'])] += 1
        gap_hist[st['rank_gap']] += 1
        image_rank_hist[st['joint_image_rank']] += 1
        constraint_rank_hist[st['constraint_rank']] += 1
        local_rank_hist[st['local_gauge_span_rank']] += 1
        if st['mode'] == 'correlated_image':
            total_enumerated_states += st['state_count']
        for v in local.values():
            S.insert(reachable, v)

    canonical = S.grouped_e0_basis(pos)
    old_e0 = 272 if pos == 'B' else 388
    assert len(canonical) == old_e0
    assert len(reachable) <= len(canonical)

    # Prove the tightened reachable-joint gauge span is a subspace of the
    # previously admitted Cartesian grouped-e0 span, not a different target.
    cover = S.union_basis(canonical, reachable)
    assert len(cover) == len(canonical)

    half = S.half_basis(pos)
    old_union = S.union_basis(canonical, half)
    new_union = S.union_basis(reachable, half)
    expected_old_union = 348 if pos == 'B' else 432
    assert len(old_union) == expected_old_union
    assert len(new_union) <= len(old_union)

    support = N.weight120_union(pos)
    expected_support = 668 if pos == 'B' else 788
    assert len(support) == expected_support
    new_qr, comp = R.quotient_rank(new_union, support)
    old_qr = 144 if pos == 'B' else 184
    assert new_qr <= old_qr
    new_total = len(support) + new_qr
    old_total = 812 if pos == 'B' else 972
    assert new_total <= old_total

    out = {
        'position': pos,
        'raw_e0_sectors': raw,
        'support_groups': len(groups),
        'canonical_e0_rank_F2': len(canonical),
        'reachable_joint_gauge_e0_rank_F2': len(reachable),
        'e0_rank_gain': len(canonical) - len(reachable),
        'canonical_e0_plus_half_rank_F2': len(old_union),
        'reachable_e0_plus_half_rank_F2': len(new_union),
        'union_rank_gain': len(old_union) - len(new_union),
        'support_Walsh_dim': len(support),
        'Walsh_complement_coordinates': comp,
        'old_exact_ZZ_quotient_rank': old_qr,
        'reachable_exact_ZZ_quotient_rank': new_qr,
        'quotient_rank_gain': old_qr - new_qr,
        'old_second_lift_rank_bound': old_total,
        'reachable_second_lift_rank_bound': new_total,
        'second_lift_rank_gain': old_total - new_total,
        'multiplicity_mode_histogram': {
            f'{m}:{mode}': n for (m, mode), n in sorted(multiplicity_mode.items())
        },
        'joint_rank_gap_histogram': dict(sorted(gap_hist.items())),
        'joint_image_rank_histogram': dict(sorted(image_rank_hist.items())),
        'shared_constraint_rank_histogram': dict(sorted(constraint_rank_hist.items())),
        'local_gauge_span_rank_histogram': dict(sorted(local_rank_hist.items())),
        'correlated_groups': sum(st['mode'] == 'correlated_image' for st in stats),
        'full_product_groups': sum(st['mode'] == 'full_product' for st in stats),
        'total_enumerated_correlated_joint_states': total_enumerated_states,
        'max_joint_rank_gap': max(st['rank_gap'] for st in stats),
        'max_correlated_joint_image_rank': max(
            (st['joint_image_rank'] for st in stats if st['mode'] == 'correlated_image'),
            default=0,
        ),
    }
    print(json.dumps(out, sort_keys=True), flush=True)
    return out


def main():
    out = {pos: analyze(pos) for pos in 'BC'}
    summary = {
        pos: {
            'canonical_e0_rank_F2': out[pos]['canonical_e0_rank_F2'],
            'reachable_joint_gauge_e0_rank_F2': out[pos]['reachable_joint_gauge_e0_rank_F2'],
            'e0_rank_gain': out[pos]['e0_rank_gain'],
            'canonical_e0_plus_half_rank_F2': out[pos]['canonical_e0_plus_half_rank_F2'],
            'reachable_e0_plus_half_rank_F2': out[pos]['reachable_e0_plus_half_rank_F2'],
            'union_rank_gain': out[pos]['union_rank_gain'],
            'old_exact_ZZ_quotient_rank': out[pos]['old_exact_ZZ_quotient_rank'],
            'reachable_exact_ZZ_quotient_rank': out[pos]['reachable_exact_ZZ_quotient_rank'],
            'quotient_rank_gain': out[pos]['quotient_rank_gain'],
            'old_second_lift_rank_bound': out[pos]['old_second_lift_rank_bound'],
            'reachable_second_lift_rank_bound': out[pos]['reachable_second_lift_rank_bound'],
            'second_lift_rank_gain': out[pos]['second_lift_rank_gain'],
            'correlated_groups': out[pos]['correlated_groups'],
            'full_product_groups': out[pos]['full_product_groups'],
            'total_enumerated_correlated_joint_states': out[pos]['total_enumerated_correlated_joint_states'],
            'max_joint_rank_gap': out[pos]['max_joint_rank_gap'],
            'max_correlated_joint_image_rank': out[pos]['max_correlated_joint_image_rank'],
        }
        for pos in 'BC'
    }
    print('result_summary', json.dumps(summary, sort_keys=True), flush=True)
    print('PASS PROBE V26_Q138_BC_E0_REACHABLE_JOINT_SIGN_SPAN')
    print('scope=gauge-closed grouped-e0 sign span using only jointly reachable affine-support-syndrome and XOR-aggregate-frequency states')
    print('containment=the reachable-joint span is exactly checked to lie inside the canonical Cartesian grouped-e0 span')
    print('scalar_gauge=for each reachable joint state the support mask generator closes under the omitted right-only scalar sign flip')
    print('downstream=reports exact GF2 e0/e0+half ranks and exact ZZ Walsh-quotient rank against the admitted support-only space')
    print('not_included=exact integer coefficients beyond the admitted gauge-closed sign-span target, complete B2/C2, W_repr, alpha, arithmetic-work, ranking/search, full-round')


if __name__ == '__main__':
    main()
