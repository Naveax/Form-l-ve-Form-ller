#!/usr/bin/env python3
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sympy import GF, ZZ
from sympy.polys.matrices import DomainMatrix

import verify_v26_q138_predecessor_leaf_bc_second_residue_sign_span348_432 as S
import verify_v26_q138_predecessor_leaf_bc_second_residue_support_frequency_nesting as N
import verify_v26_q138_predecessor_leaf_bc_second_residue_rank812_972 as R

POS = 'C'
EXPECTED_DIM = 432
EXPECTED_SUPPORT = 788
BASELINE_QR = 184
P = 65521
PROJ_SEEDS = (0, 1, 2, 3)


def make_basis(seq):
    B = {}
    for v in seq:
        S.insert(B, v)
    assert len(B) == EXPECTED_DIM
    return list(B.values())


def full_projected_rows(basis, comp):
    rows = []
    for v in basis:
        w = R.fwht(v)
        rows.append([w[i] for i in comp])
    return rows


def mod_rank(rows, p=P):
    return DomainMatrix.from_list(rows, GF(p)).rank()


def exact_rank(rows):
    return DomainMatrix.from_list(rows, ZZ).rank()


def variants(E, H):
    ev = list(E.values())
    hv = list(H.values())
    raw = ev + hv
    yield 'E_then_H', raw
    yield 'H_then_E', hv + ev
    yield 'reverse_all', list(reversed(raw))
    yield 'weight_asc', sorted(raw, key=lambda x: (x.bit_count(), x.bit_length()))
    yield 'weight_desc', sorted(raw, key=lambda x: (-x.bit_count(), -x.bit_length()))
    yield 'pivot_asc', sorted(raw, key=lambda x: (x.bit_length(), x.bit_count()))
    yield 'pivot_desc', sorted(raw, key=lambda x: (-x.bit_length(), x.bit_count()))
    for seed in range(12):
        z = raw[:]
        random.Random(seed).shuffle(z)
        yield f'shuffle_{seed}', z


def projection_columns(ncols, seed):
    # A rank-184 minor certifies full projected rank >=184. Deterministic
    # shuffled column subsets provide cheap lower certificates. Failure of a
    # chosen minor says nothing, so unresolved gauges fall back to the full
    # modular matrix before any exact claim.
    idx = list(range(ncols))
    random.Random(138000 + seed).shuffle(idx)
    return sorted(idx[:BASELINE_QR])


def screen(rows):
    ncols = len(rows[0])
    for seed in PROJ_SEEDS:
        cols = projection_columns(ncols, seed)
        sub = [[row[j] for j in cols] for row in rows]
        r = mod_rank(sub)
        print('  projection', seed, 'columns', len(cols), 'rank_Fp', r, flush=True)
        if r >= BASELINE_QR:
            return r, f'projection_{seed}', None
    r = mod_rank(rows)
    print('  full_mod_rank_Fp', r, flush=True)
    return r, 'full', rows


def main():
    support = N.weight120_union(POS)
    assert len(support) == EXPECTED_SUPPORT
    comp = [i for i in range(2048) if i not in support]

    E = S.grouped_e0_basis(POS)
    H = S.half_basis(POS)
    canonical = S.union_basis(E, H)
    assert len(canonical) == EXPECTED_DIM

    base_rows = full_projected_rows(list(canonical.values()), comp)
    base_mod, how, fallback = screen(base_rows)
    assert base_mod >= BASELINE_QR
    print('baseline', 'rank_Fp_lower', base_mod, 'certificate', how,
          'admitted_exact_rank', BASELINE_QR, flush=True)

    improvements = []
    for name, order in variants(E, H):
        B = make_basis(order)
        rows = full_projected_rows(B, comp)
        lower, how, full_rows = screen(rows)
        print('variant', name, 'rank_Fp_lower', lower, 'certificate', how, flush=True)
        if lower >= BASELINE_QR:
            continue

        # A projected minor can only certify a lower bound. If it did not hit
        # 184, require the complete modular rank before considering exact ZZ.
        if full_rows is None:
            full_rows = rows
        full_mod = mod_rank(full_rows)
        print('variant', name, 'complete_rank_Fp', full_mod, flush=True)
        if full_mod >= BASELINE_QR:
            continue

        er = exact_rank(full_rows)
        assert er >= full_mod
        print('exact_candidate', name, 'rank_Fp', full_mod, 'exact_rank', er, flush=True)
        if er < BASELINE_QR:
            total = EXPECTED_SUPPORT + er
            improvements.append((total, er, name))
            print('UNIFORM_C_SECOND_LIFT_CANDIDATE', total,
                  'quotient_rank', er, 'baseline', EXPECTED_SUPPORT + BASELINE_QR,
                  'variant', name, flush=True)

    if improvements:
        print('best_uniform_candidate', min(improvements), flush=True)
    else:
        print('exact_candidate', 'NONE',
              'reason=every_tested_gauge_has_certified_modular_rank_at_least_baseline',
              flush=True)

    print('PASS V26_Q138_C_UNIFORM_SECOND_RESIDUE_BASIS_GAUGE_FAST')
    print('scope=deterministic basis-gauge search; rank-184 projected minors are rigorous lower certificates, unresolved cases use complete modular rank')
    print('claim=any exact r<184 is a valid alternative uniform lift; no-find is scoped to tested gauges only')


if __name__ == '__main__':
    main()
