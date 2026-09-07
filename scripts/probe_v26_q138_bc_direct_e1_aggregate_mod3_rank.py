#!/usr/bin/env python3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_v26_q138_predecessor_leaf_top_carry_cancellation as T
import verify_v26_q138_predecessor_leaf_dyadic_descent92_121 as D
import verify_v26_q138_predecessor_leaf_ad_second_dyadic_rank310 as A
import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import probe_v26_q138_predecessor_leaf_bc_second_residue_high_correction_fourier as H
import probe_v26_q138_bc_direct_e1_exact_sector_cancellation as X

LEFT = sorted(A.S1)
RIGHT = list(A.R1)
LEXT = [128 + i for i in LEFT]
REXT = [128 + i for i in RIGHT]
ALL = (1 << (1 << len(LEFT))) - 1
NROW = 1 << len(LEFT)
MAX_COLUMNS = 4096
PRED_MASK = (1 << 128) - 1
EXT_MASK = (1 << 160) - 1
FULL_SECTOR_ZERO = {
    'B': ((1, 5),),
    'C': ((1, 1),),
}


def beta32_equations(can, pred):
    out = []
    for row in can:
        m = 0
        for i in range(32):
            if (row >> (128 + i)) & 1:
                m |= 1 << i
        rhs = ((row >> 160) & 1) ^ ((row & pred).bit_count() & 1)
        out.append((m, rhs))
    return out


def fixed_predecessor_possible(can, pred):
    return T.rref(beta32_equations(can, pred), n=32) is not None


def witness_predecessor(pos, e1):
    target = FULL_SECTOR_ZERO[pos]
    found = None
    for zs, cls in e1[len(target)]:
        if zs == target:
            found = (zs, cls)
            break
    assert found is not None, (pos, target)
    zs, cls = found
    can = H.support_for(pos, zs, cls)
    assert can is not None
    eq = [(row & EXT_MASK, (row >> 160) & 1) for row in can]
    sol = T.rref(eq, n=160)
    assert sol is not None
    pred = sol[1] & PRED_MASK
    assert fixed_predecessor_possible(can, pred)
    return pred, zs, cls


def support_desc(can, pred):
    eqs = []
    toggles = [0] * len(RIGHT)
    rhsbits = 0
    for e, row in enumerate(can):
        lm = rm = 0
        for q, ext in enumerate(LEXT):
            if (row >> ext) & 1:
                lm |= 1 << q
        for q, ext in enumerate(REXT):
            if (row >> ext) & 1:
                rm |= 1 << q
        rhs = ((row >> 160) & 1) ^ ((row & pred).bit_count() & 1)
        eqs.append(lm)
        if rhs:
            rhsbits |= 1 << e
        y = rm
        while y:
            b = y & -y
            j = b.bit_length() - 1
            toggles[j] ^= 1 << e
            y ^= b
    return [tuple(eqs), tuple(toggles), rhsbits]


def support_mask(desc):
    eqs, _toggles, rhsbits = desc
    out = ALL
    for e, lm in enumerate(eqs):
        val = (rhsbits >> e) & 1
        if lm == 0:
            if val:
                return 0
            continue
        w = S.WALSH[lm]
        out &= w if val else (w ^ ALL)
        if out == 0:
            return 0
    return out


def phase_desc(pos, zs, pred):
    c, lin, polar, _rank, _pr = X.full_corrected_phase(pos, D.carries(zs))

    # Specialize the complete 160-variable quadratic phase at the fixed
    # predecessor. Quadratic beta-beta coefficients are unchanged; each beta
    # linear coefficient gains B(pred,e), and the global constant becomes q(pred,0).
    const = X.q_eval(c, lin, polar, pred)

    lfreq = 0
    for q, ext in enumerate(LEXT):
        bit = ((lin >> ext) & 1) ^ ((polar[ext] & pred).bit_count() & 1)
        if bit:
            lfreq |= 1 << q
    base = S.WALSH[lfreq]
    for a in range(len(LEXT)):
        ea = LEXT[a]
        for b in range(a + 1, len(LEXT)):
            eb = LEXT[b]
            if (polar[ea] >> eb) & 1:
                base ^= S.WALSH[1 << a] & S.WALSH[1 << b]

    cross = []
    for er in REXT:
        f = 0
        for a, el in enumerate(LEXT):
            if (polar[er] >> el) & 1:
                f |= 1 << a
        cross.append(f)

    rlin = 0
    for j, er in enumerate(REXT):
        bit = ((lin >> er) & 1) ^ ((polar[er] & pred).bit_count() & 1)
        if bit:
            rlin |= 1 << j
    rpolar = []
    for j, er in enumerate(REXT):
        m = 0
        for k, ek in enumerate(REXT):
            if (polar[er] >> ek) & 1:
                m |= 1 << k
        assert not ((m >> j) & 1)
        rpolar.append(m)

    return [base, tuple(cross), rlin, tuple(rpolar), const & 1, 0]


def phase_flip(desc, j, old_y):
    _base, cross, rlin, rpolar, sign, freq = desc
    sign ^= ((rlin >> j) & 1) ^ ((rpolar[j] & old_y).bit_count() & 1)
    freq ^= cross[j]
    desc[4] = sign
    desc[5] = freq


def phase_bits(desc):
    base, _cross, _rlin, _rpolar, sign, freq = desc
    z = base ^ S.WALSH[freq]
    if sign:
        z ^= ALL
    return z


def add_signed_mod3(one, two, positive, negative):
    used = positive | negative
    zero = (~(one | two)) & ALL
    n1 = (one & ~used) | (zero & positive) | (two & negative)
    n2 = (two & ~used) | (one & positive) | (zero & negative)
    return n1 & ALL, n2 & ALL


def add_mod3(a1, a2, b1, b2):
    a0 = (~(a1 | a2)) & ALL
    b0 = (~(b1 | b2)) & ALL
    r1 = (a0 & b1) | (a1 & b0) | (a2 & b2)
    r2 = (a0 & b2) | (a1 & b1) | (a2 & b0)
    return r1 & ALL, r2 & ALL


def insert_mod3(basis, one, two):
    while one | two:
        p = (one | two).bit_length() - 1
        cur = basis[p]
        if cur is None:
            if (two >> p) & 1:
                one, two = two, one
            basis[p] = (one, two)
            return True
        b1, b2 = cur
        if (one >> p) & 1:
            one, two = add_mod3(one, two, b2, b1)
        else:
            one, two = add_mod3(one, two, b1, b2)
    return False


def prepare(pos):
    _e0, e1, _half = H.classify_patterns()
    pred, witness_zs, witness_cls = witness_predecessor(pos, e1)
    support_groups = {}
    phases = []
    raw = fixed_unreachable = 0
    byk = Counter()
    witness_active = False
    for k in range(4):
        for zs, cls in e1[k]:
            can = H.support_for(pos, zs, cls)
            if can is None:
                continue
            raw += 1
            if not fixed_predecessor_possible(can, pred):
                fixed_unreachable += 1
                continue
            byk[k] += 1
            if zs == witness_zs and cls == witness_cls:
                witness_active = True
            gi = support_groups.get(can)
            if gi is None:
                gi = len(support_groups)
                support_groups[can] = gi
            pd = phase_desc(pos, zs, pred)
            phases.append((gi, pd))

    assert witness_active
    groups = [None] * len(support_groups)
    for can, gi in support_groups.items():
        groups[gi] = [support_desc(can, pred), []]
    for gi, pd in phases:
        groups[gi][1].append(pd)

    score = [0] * len(RIGHT)
    for desc, _arr in groups:
        for j, t in enumerate(desc[1]):
            if t:
                score[j] += 1
    for _gi, pd in phases:
        for j, f in enumerate(pd[1]):
            if f:
                score[j] += 2
    order = sorted(range(len(RIGHT)), key=lambda j: (-score[j], j))
    print('position', pos,
          'predecessor_witness_hex', hex(pred),
          'witness_sector', (witness_zs, witness_cls),
          'reachable_global_e1', raw,
          'fixed_predecessor_unreachable', fixed_unreachable,
          'active_fixed_predecessor', len(phases),
          'support_groups', len(groups),
          'active_by_zero_count', dict(sorted(byk.items())), flush=True)
    print('position', pos, 'right_bit_order', [RIGHT[j] for j in order],
          'right_bit_scores', [score[j] for j in order], flush=True)
    return pred, groups, phases, order


def aggregate_column(groups):
    one = two = 0
    for sdesc, arr in groups:
        sm = support_mask(sdesc)
        if not sm:
            continue
        for pd in arr:
            q = phase_bits(pd)
            neg = sm & q
            pos = sm & (q ^ ALL)
            one, two = add_signed_mod3(one, two, pos, neg)
    return one, two


def run_position(pos):
    pred, groups, phases, order = prepare(pos)
    basis = [None] * NROW
    rank = 0
    y = 0
    prev_gray = 0
    milestones = {64, 128, 256, 512, 768, 1024, 1280, 1536, 1792,
                  2048, 2304, 2560, 3072, 3584, 4096}

    for i in range(MAX_COLUMNS):
        if i:
            gray = i ^ (i >> 1)
            delta = gray ^ prev_gray
            src = delta.bit_length() - 1
            j = order[src]
            old_y = y
            y ^= 1 << j
            for sdesc, _arr in groups:
                sdesc[2] ^= sdesc[1][j]
            for _gi, pd in phases:
                phase_flip(pd, j, old_y)
            prev_gray = gray

        one, two = aggregate_column(groups)
        if insert_mod3(basis, one, two):
            rank += 1
            if rank == NROW:
                print('position', pos, 'FULL_RANK_F3', rank,
                      'columns_examined', i + 1,
                      'predecessor_witness_hex', hex(pred),
                      'last_right_beta', y, flush=True)
                return rank, i + 1
        if (i + 1) in milestones:
            print('position', pos, 'columns_examined', i + 1, 'rank_F3', rank, flush=True)

    print('position', pos, 'rank_F3_lower_bound', rank,
          'columns_examined', MAX_COLUMNS, 'full_rank_not_reached', True, flush=True)
    return rank, MAX_COLUMNS


def main():
    results = {}
    for pos in 'CB':
        results[pos] = run_position(pos)
    print('results', results)
    if all(r == NROW for r, _n in results.values()):
        print('PASS PROBE V26_Q138_BC_DIRECT_E1_AGGREGATE_MOD3_FULL_RANK')
        print('theorem=at deterministic reachable predecessor witnesses, complete direct-e1 integer aggregates have rank_F3=2048 for both B and C, hence exact rank_Q=2048')
        print('consequence=no uniform subgeneric rational-rank bound exists for the complete direct-e1 aggregate itself')
    else:
        print('PASS PROBE V26_Q138_BC_DIRECT_E1_AGGREGATE_MOD3_LOWER_BOUND')
        print('scope=deterministic exact GF(3) lower bound on sampled-column submatrices at reachable predecessor witnesses; non-full result is not an upper bound')


if __name__ == '__main__':
    main()
