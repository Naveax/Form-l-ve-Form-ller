#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H

PRED_BITS = 128
EXT_BITS = 160
RHS_BIT = 160
PRED_MASK = (1 << PRED_BITS) - 1
BETA_MASK = ((1 << 32) - 1) << PRED_BITS
MAX_ENUM_RANK = 18


def predecessor_condition(can):
    """Project an affine support in F2^160 onto predecessor128."""
    rows = list(can)
    r = 0
    for col in range(PRED_BITS, EXT_BITS):
        p = next((k for k in range(r, len(rows)) if (rows[k] >> col) & 1), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for k in range(len(rows)):
            if k != r and ((rows[k] >> col) & 1):
                rows[k] ^= rows[r]
        r += 1

    out = []
    for row in rows[r:]:
        assert (row & BETA_MASK) == 0
        pm = row & PRED_MASK
        rhs = (row >> RHS_BIT) & 1
        if pm == 0:
            assert rhs == 0
        else:
            out.append((pm, rhs))

    sol = T.rref(out, n=PRED_BITS)
    assert sol is not None
    particular, null = sol[1], sol[2]
    uniq = sorted(set(out))
    assert all((((pm & particular).bit_count() & 1) == rhs) for pm, rhs in uniq)
    for d in null[: min(8, len(null))]:
        assert all((((pm & d).bit_count() & 1) == 0) for pm, _ in uniq)
    return tuple(uniq)


def insert_linear_basis(B, x):
    y = x
    while y:
        p = y.bit_length() - 1
        if p not in B:
            B[p] = y
            return True
        y ^= B[p]
    return False


def build_linear_basis(masks):
    B = {}
    for x in masks:
        insert_linear_basis(B, x)
    pivots = sorted(B, reverse=True)
    vecs = [B[p] for p in pivots]
    index = {p: i for i, p in enumerate(pivots)}
    return B, vecs, index


def decompose(B, index, x):
    y = x
    c = 0
    while y:
        p = y.bit_length() - 1
        assert p in B, ("mask outside predecessor-form span", p)
        y ^= B[p]
        c ^= 1 << index[p]
    return c


def condition_in_signature_basis(cond, B, index):
    return tuple((decompose(B, index, pm), rhs) for pm, rhs in cond)


def active(cond, sig):
    return all((((c & sig).bit_count() & 1) == rhs) for c, rhs in cond)


def predecessor_from_signature(vecs, sig):
    eq = [(v, (sig >> i) & 1) for i, v in enumerate(vecs)]
    sol = T.rref(eq, n=PRED_BITS)
    assert sol is not None
    p = sol[1]
    assert all((((v & p).bit_count() & 1) == ((sig >> i) & 1))
               for i, v in enumerate(vecs))
    return p


def support_groups(pos):
    e0, _e1, half = H.classify_patterns()

    e0_groups = {}
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = H.support_for(pos, zs, cls)
            if can is None:
                continue
            raw += 1
            e0_groups[can] = e0_groups.get(can, 0) + 1

    expected_raw = 581 if pos == 'B' else 577
    expected_groups = 251 if pos == 'B' else 250
    assert raw == expected_raw
    assert len(e0_groups) == expected_groups

    half_cans = []
    for zs, cls in half:
        can = H.support_for(pos, zs, cls)
        assert can is not None
        half_cans.append(can)
    assert len(half_cans) == 4
    assert all(can == half_cans[0] for can in half_cans)

    return e0_groups, half_cans[0]


def beta32_equations(can, pred):
    out = []
    for row in can:
        m = 0
        for i in range(32):
            if (row >> (128 + i)) & 1:
                m |= 1 << i
        rhs = ((row >> RHS_BIT) & 1) ^ ((row & pred).bit_count() & 1)
        out.append((m, rhs))
    return out


def analyze(pos):
    e0_groups, half_can = support_groups(pos)
    group_conds = [predecessor_condition(can) for can in e0_groups]
    half_cond = predecessor_condition(half_can)

    masks = [pm for cond in group_conds for pm, _ in cond]
    masks.extend(pm for pm, _ in half_cond)
    B, vecs, index = build_linear_basis(masks)
    rank = len(vecs)

    cond_dims = Counter(len(c) for c in group_conds)
    distinct_conditions = len(set(group_conds))
    print(
        'position', pos,
        'e0_support_groups', len(group_conds),
        'distinct_predecessor_conditions', distinct_conditions,
        'predecessor_constraint_count_distribution', dict(sorted(cond_dims.items())),
        'half_predecessor_constraints', len(half_cond),
        'predecessor_condition_linear_rank', rank,
        flush=True,
    )

    if rank > MAX_ENUM_RANK:
        print(
            'position', pos,
            'exact_signature_enumeration', 'SKIP',
            'reason=predecessor_condition_linear_rank_exceeds_cap',
            'cap', MAX_ENUM_RANK,
            flush=True,
        )
        return

    gconds = [condition_in_signature_basis(c, B, index) for c in group_conds]
    hcond = condition_in_signature_basis(half_cond, B, index)

    distinct_patterns = set()
    min_active = len(gconds) + 1
    max_active = -1
    max_total = -1
    best_sig = None
    best_half = False
    all_e0 = False
    all_combined = False
    half_on = half_off = 0

    for sig in range(1 << rank):
        amask = 0
        n = 0
        for i, cond in enumerate(gconds):
            if active(cond, sig):
                amask |= 1 << i
                n += 1
        h = active(hcond, sig)
        pattern = amask | ((1 if h else 0) << len(gconds))
        distinct_patterns.add(pattern)
        min_active = min(min_active, n)
        max_active = max(max_active, n)
        total = n + (1 if h else 0)
        if total > max_total:
            max_total = total
            best_sig = sig
            best_half = h
        if n == len(gconds):
            all_e0 = True
            if h:
                all_combined = True
        if h:
            half_on += 1
        else:
            half_off += 1

    pred = predecessor_from_signature(vecs, best_sig)
    direct_e0 = sum(
        1 for can in e0_groups
        if T.rref(beta32_equations(can, pred), n=32) is not None
    )
    direct_half = T.rref(beta32_equations(half_can, pred), n=32) is not None

    assert direct_e0 == max_total - (1 if best_half else 0)
    assert direct_half == best_half

    print(
        'position', pos,
        'exact_signature_enumeration', 'PASS',
        'signatures', 1 << rank,
        'distinct_reachability_patterns', len(distinct_patterns),
        'e0_active_min', min_active,
        'e0_active_max', max_active,
        'half_active_signature_count', half_on,
        'half_inactive_signature_count', half_off,
        'max_e0_plus_half_support_groups', max_total,
        'all_e0_simultaneously_reachable', all_e0,
        'all_e0_plus_half_simultaneously_reachable', all_combined,
        'best_predecessor_hex', hex(pred),
        flush=True,
    )


def main():
    for pos in 'BC':
        analyze(pos)
    print('PASS V26_Q138_BC_SECOND_RESIDUE_REACHABLE_PREDECESSOR_GEOMETRY')
    print('scope=exact predecessor reachability geometry only; no new 812/972 rank claim')
    print('next=if signature rank is enumerable, specialize assembled correction columns per reachable class before Walsh quotient')


if __name__ == '__main__':
    main()
