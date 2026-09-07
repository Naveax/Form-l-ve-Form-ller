#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from z3 import And, Bool, BoolVal, If, IntVal, Optimize, Sum, Xor, is_true, sat

import probe_v26_q138_bc_second_residue_reachable_predecessor_geometry as G
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import verify_v26_q138_predecessor_leaf_bc_second_residue_support_frequency_nesting as N
import verify_v26_q138_predecessor_leaf_bc_second_residue_rank812_972 as R
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H


def z3_parity(xs, mask):
    bits = [xs[i] for i in range(len(xs)) if (mask >> i) & 1]
    if not bits:
        return BoolVal(False)
    if len(bits) == 1:
        return bits[0]
    return Xor(*bits)


def z3_condition(xs, cond):
    terms = []
    for c, rhs in cond:
        terms.append(z3_parity(xs, c) == BoolVal(bool(rhs)))
    return And(*terms) if terms else BoolVal(True)


def solve_max_overlap(pos):
    e0_groups, half_can = G.support_groups(pos)
    group_conds0 = {can: G.predecessor_condition(can) for can in e0_groups}
    half_cond0 = G.predecessor_condition(half_can)

    masks = [pm for cond in group_conds0.values() for pm, _ in cond]
    masks.extend(pm for pm, _ in half_cond0)
    B, vecs, index = G.build_linear_basis(masks)
    rank = len(vecs)
    expected = 77 if pos == 'B' else 75
    assert rank == expected

    group_conds = {
        can: G.condition_in_signature_basis(cond, B, index)
        for can, cond in group_conds0.items()
    }
    half_cond = G.condition_in_signature_basis(half_cond0, B, index)

    classes = Counter(group_conds.values())
    xs = [Bool(f'x{i}') for i in range(rank)]
    score_terms = []
    for cond, weight in classes.items():
        score_terms.append(IntVal(weight) * If(z3_condition(xs, cond), 1, 0))
    score_terms.append(If(z3_condition(xs, half_cond), 1, 0))
    score = Sum(score_terms)

    opt = Optimize()
    opt.set(priority='lex')
    handle = opt.maximize(score)
    assert opt.check() == sat
    model = opt.model()
    lower = handle.lower()
    upper = handle.upper()
    sig = 0
    for i, x in enumerate(xs):
        if is_true(model.eval(x, model_completion=True)):
            sig |= 1 << i

    active_cans = {
        can for can, cond in group_conds.items()
        if G.active(cond, sig)
    }
    half_active = G.active(half_cond, sig)
    value = len(active_cans) + (1 if half_active else 0)
    assert int(str(lower)) == value, (pos, lower, value)
    assert int(str(upper)) == value, (pos, upper, value)

    pred = G.predecessor_from_signature(vecs, sig)
    direct_cans = {
        can for can in e0_groups
        if G.T.rref(G.beta32_equations(can, pred), n=32) is not None
    }
    direct_half = G.T.rref(G.beta32_equations(half_can, pred), n=32) is not None
    assert direct_cans == active_cans
    assert direct_half == half_active

    print(
        'position', pos,
        'predecessor_condition_rank', rank,
        'distinct_condition_classes', len(classes),
        'z3_optimum_lower', lower,
        'z3_optimum_upper', upper,
        'max_reachable_e0_groups', len(active_cans),
        'half_active_at_optimum', half_active,
        'max_reachable_e0_plus_half_groups', value,
        'witness_predecessor_hex', hex(pred),
        flush=True,
    )
    return pred, active_cans, half_active


def filtered_e0_basis(pos, active_cans):
    e0, _e1, _half = H.classify_patterns()
    groups = {}
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = H.support_for(pos, zs, cls)
            if can is None or can not in active_cans:
                continue
            raw += 1
            qbits, cols, _rank, _meta = S.corrected_phase_data(pos, D.carries(zs))
            if can not in groups:
                groups[can] = [0, [0] * len(cols), 0]
            g = groups[can]
            g[0] ^= qbits
            g[1] = [a ^ b for a, b in zip(g[1], cols)]
            g[2] += 1

    assert set(groups) == active_cans
    out = {}
    for can, (qbits, cols, _n) in groups.items():
        cb = S.row_basis(cols)
        lb = S.left_basis(can)
        local = [qbits, S.ALL] + [S.WALSH[f] for f in cb]
        for support_mask in S.coset_masks(lb):
            for g in local:
                S.insert(out, support_mask & g)

    print(
        'position', pos,
        'reachable_e0_raw_patterns', raw,
        'reachable_e0_support_groups', len(groups),
        'filtered_uniform_e0_rank_F2<=', len(out),
        flush=True,
    )
    return out


def filtered_quotient(pos, active_cans, half_active):
    E = filtered_e0_basis(pos, active_cans)
    if half_active:
        HB = S.half_basis(pos)
        U = S.union_basis(E, HB)
    else:
        U = S.union_basis(E)

    support = N.weight120_union(pos)
    expected_support = 668 if pos == 'B' else 788
    assert len(support) == expected_support
    qr, comp = R.quotient_rank(U, support)
    total = len(support) + qr
    print(
        'position', pos,
        'filtered_uniform_sign_GF2_basis_dim', len(U),
        'Walsh_complement_coordinates', comp,
        'filtered_exact_ZZ_quotient_rank', qr,
        'filtered_second_lift_rank<=', total,
        flush=True,
    )
    return len(U), qr, total


def main():
    for pos in 'BC':
        _pred, active_cans, half_active = solve_max_overlap(pos)
        filtered_quotient(pos, active_cans, half_active)

    print('PASS V26_Q138_BC_SECOND_RESIDUE_REACHABLE_PREDECESSOR_MAXOVERLAP')
    print('scope=solver-guided diagnostic at a max-support-overlap predecessor; not a uniform rank theorem')
    print('note=filtered phase basis remains predecessor-uniform, so further exact specialization can only reduce this witness bound')


if __name__ == '__main__':
    main()
