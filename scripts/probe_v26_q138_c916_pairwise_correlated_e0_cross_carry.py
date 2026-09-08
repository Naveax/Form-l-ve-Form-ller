#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_reachable_joint_sign_span as P
import probe_v26_q138_bc_uniform_half_lift_third_carry as H
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S

POS = 'C'
DOMAIN_BITS = 149
FREQ_BITS = 11
FULL = 2048
K9_REPEATED_TARGET = 650


def support_description(can):
    rows = []
    for row in can:
        rows.append([
            P.compress(row, S.LEFT),
            P.compress(row, S.RIGHT),
            (row >> 160) & 1,
        ])

    r = 0
    for col in range(len(S.LEFT)):
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
        r += 1

    piv = [tuple(x) for x in rows[:r]]
    pure = [tuple(x) for x in rows[r:]]
    assert all(lm == 0 for lm, _rm, _c in pure)

    old_piv, old_rank, old_r0, old_null = P.support_affine_map(can)
    assert piv == old_piv
    pure_eq = [(rm, c) for _lm, rm, c in pure]
    sol = P.Top.rref(pure_eq, n=DOMAIN_BITS)
    assert sol is not None
    assert sol[0] == old_rank and sol[1] == old_r0 and tuple(sol[2]) == old_null
    return piv, tuple(pure_eq)


def fixed_support_equations(rec, sigma):
    eq = list(rec['pure_eq'])
    for i, (_lm, rm, c) in enumerate(rec['pivot_rows']):
        eq.append((rm, c ^ ((sigma >> i) & 1)))
    return eq


def build_records_and_basis():
    raw, groups = P.grouped_data(POS)
    assert raw == 577 and len(groups) == 250

    global_basis = {}
    records = []
    correlated = 0
    full_product = 0

    for gid, (can, sectors) in enumerate(groups):
        qbits, cols = P.aggregate_phase(POS, sectors)
        local, st = P.reachable_local_basis(can, qbits, cols)
        for v in local.values():
            S.insert(global_basis, v)
        correlated += st['mode'] == 'correlated_image'
        full_product += st['mode'] == 'full_product'
        piv, pure = support_description(can)
        assert len(piv) == st['support_rank']
        records.append({
            'group_id': gid,
            'qbits': qbits,
            'cols': tuple(cols),
            'pivot_rows': piv,
            'pure_eq': pure,
            'support_rank': len(piv),
            'joint_image_rank': st['joint_image_rank'],
            'mode': st['mode'],
        })

    assert correlated == 111 and full_product == 139
    assert len(global_basis) == 388
    items, piv = H.coordinate_solver(global_basis)

    support = P.N.weight120_union(POS)
    assert len(support) == 788
    qr, comp = P.R.quotient_rank(global_basis, support)
    assert qr == 128 and comp == 1260 and len(support) + qr == 916
    return records, items, piv


def analyze():
    records, items, coord_piv = build_records_and_basis()

    coord_cache = {0: 0}
    truth_cache = {0: 0}
    polar_cache = {}
    cross_span = {}

    def coord(vec):
        z = coord_cache.get(vec)
        if z is None:
            z = H.coordinates(vec, coord_piv)
            assert z is not None, 'local reachable vector escaped global C916 e0 basis'
            coord_cache[vec] = z
        return z

    def truth(coeff):
        z = truth_cache.get(coeff)
        if z is not None:
            return z
        x = coeff
        v = 0
        while x:
            b = x & -x
            v ^= items[b.bit_length() - 1]
            x ^= b
        truth_cache[coeff] = v
        return v

    def polar(a, b):
        if a > b:
            a, b = b, a
        key = (a, b)
        z = polar_cache.get(key)
        if z is None:
            # Polarization of Q(a)=xor_{i<j} a_i a_j (v_i & v_j):
            # B(a,b) = truth(a)&truth(b) xor truth(a&b).
            z = (truth(a) & truth(b)) ^ truth(a & b)
            polar_cache[key] = z
        return z

    pair_order = sorted(
        range(len(records)),
        key=lambda i: (-records[i]['joint_image_rank'], -records[i]['support_rank'], i),
    )

    group_pairs_started = 0
    group_pairs_completed = 0
    support_pair_fibers = 0
    scalar_fibers = 0
    frequency_image_generators_mapped = 0
    max_joint_frequency_image_rank = 0
    anf_coefficients_inserted = 0
    saturation = None

    def add(v):
        nonlocal anf_coefficients_inserted
        S.insert(cross_span, v)
        anf_coefficients_inserted += 1
        return len(cross_span) == FULL

    for oi in range(len(pair_order)):
        gi = pair_order[oi]
        A = records[gi]
        for oj in range(oi + 1, len(pair_order)):
            gj = pair_order[oj]
            B = records[gj]
            group_pairs_started += 1

            for sa in range(1 << A['support_rank']):
                sma = P.support_mask(A['pivot_rows'], sa)
                assert sma != 0
                eq_a = fixed_support_equations(A, sa)
                for sb in range(1 << B['support_rank']):
                    smb = P.support_mask(B['pivot_rows'], sb)
                    assert smb != 0
                    eq = eq_a + fixed_support_equations(B, sb)
                    sol = P.Top.rref(eq, n=DOMAIN_BITS)
                    if sol is None:
                        continue
                    support_pair_fibers += 1
                    r0, null = sol[1], sol[2]

                    f0a = P.xor_columns(A['cols'], r0)
                    f0b = P.xor_columns(B['cols'], r0)
                    joint_dirs = S.row_basis(
                        P.xor_columns(A['cols'], d)
                        | (P.xor_columns(B['cols'], d) << FREQ_BITS)
                        for d in null
                    )
                    k = len(joint_dirs)
                    max_joint_frequency_image_rank = max(max_joint_frequency_image_rank, k)
                    frequency_image_generators_mapped += len(null)

                    va0 = sma & (A['qbits'] ^ S.WALSH[f0a])
                    vb0 = smb & (B['qbits'] ^ S.WALSH[f0b])
                    a0 = coord(va0)
                    b0 = coord(vb0)
                    atoggle = coord(sma)
                    btoggle = coord(smb)

                    ad = []
                    bd = []
                    for d in joint_dirs:
                        dfa = d & ((1 << FREQ_BITS) - 1)
                        dfb = d >> FREQ_BITS
                        ad.append(coord(sma & S.WALSH[dfa]))
                        bd.append(coord(smb & S.WALSH[dfb]))

                    # Quadratic ANF coefficients do not depend on the two
                    # scalar-gauge constants, so insert them once per fiber.
                    for x in range(k):
                        for y in range(x + 1, k):
                            q = polar(ad[x], bd[y]) ^ polar(ad[y], bd[x])
                            if add(q):
                                saturation = {
                                    'group_pair': [A['group_id'], B['group_id']],
                                    'support_syndromes': [sa, sb],
                                    'scalar_pattern': None,
                                    'coefficient': 'quadratic',
                                    'rank': FULL,
                                }
                                break
                        if saturation is not None:
                            break
                    if saturation is not None:
                        break

                    for scalar_a in (0, 1):
                        aa0 = a0 ^ (atoggle if scalar_a else 0)
                        for scalar_b in (0, 1):
                            scalar_fibers += 1
                            bb0 = b0 ^ (btoggle if scalar_b else 0)
                            if add(polar(aa0, bb0)):
                                saturation = {
                                    'group_pair': [A['group_id'], B['group_id']],
                                    'support_syndromes': [sa, sb],
                                    'scalar_pattern': [scalar_a, scalar_b],
                                    'coefficient': 'constant',
                                    'rank': FULL,
                                }
                                break
                            for x in range(k):
                                lin = (
                                    polar(ad[x], bb0)
                                    ^ polar(aa0, bd[x])
                                    ^ polar(ad[x], bd[x])
                                )
                                if add(lin):
                                    saturation = {
                                        'group_pair': [A['group_id'], B['group_id']],
                                        'support_syndromes': [sa, sb],
                                        'scalar_pattern': [scalar_a, scalar_b],
                                        'coefficient': ['linear', x],
                                        'rank': FULL,
                                    }
                                    break
                            if saturation is not None:
                                break
                        if saturation is not None:
                            break
                    if saturation is not None:
                        break
                if saturation is not None:
                    break
            if saturation is not None:
                break
            group_pairs_completed += 1
        if saturation is not None:
            break

    out = {
        'position': POS,
        'reachable_e0_basis_dim': len(items),
        'reachable_second_lift_total': 916,
        'group_count': len(records),
        'group_pairs_total': len(records) * (len(records) - 1) // 2,
        'group_pairs_started': group_pairs_started,
        'group_pairs_completed_before_stop': group_pairs_completed,
        'support_pair_fibers_processed': support_pair_fibers,
        'scalar_fibers_processed': scalar_fibers,
        'max_joint_frequency_image_rank': max_joint_frequency_image_rank,
        'frequency_image_generators_mapped': frequency_image_generators_mapped,
        'degree2_ANF_coefficients_inserted': anf_coefficients_inserted,
        'pairwise_correlated_e0_cross_carry_GF2_span': len(cross_span),
        'saturation': saturation,
        'coordinate_cache_size': len(coord_cache),
        'truth_cache_size': len(truth_cache),
        'polar_cache_size': len(polar_cache),
        'k9_repeated_target': K9_REPEATED_TARGET,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_PAIRWISE_CORRELATED_E0_CROSS_CARRY')
    print('scope=pairwise cross-group polar carry in the 388-vector reachable C916 e0 basis, preserving exact shared-state reachability for each group pair and exact degree<=2 fixed-support interpolation; local scalar gauge is relaxed over both constants')
    print('important=this is an envelope for pairwise cross terms, not the exact all-250-group aggregate carry and not a lower bound on complete C2')
    print('not_included=support/e1 component, support-e0 cross, half cross, exact all-group scalar correlation, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


def main():
    analyze()


if __name__ == '__main__':
    main()
