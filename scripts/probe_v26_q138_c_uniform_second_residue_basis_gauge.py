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
PRIMES = (65521, 65519)


def make_basis(seq):
    B = {}
    for v in seq:
        S.insert(B, v)
    assert len(B) == EXPECTED_DIM
    return list(B.values())


def projected_rows(basis, comp):
    rows = []
    for v in basis:
        w = R.fwht(v)
        rows.append([w[i] for i in comp])
    return rows


def mod_rank(rows, p):
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


def main():
    support = N.weight120_union(POS)
    assert len(support) == EXPECTED_SUPPORT
    comp = [i for i in range(2048) if i not in support]

    E = S.grouped_e0_basis(POS)
    H = S.half_basis(POS)
    canonical = S.union_basis(E, H)
    assert len(canonical) == EXPECTED_DIM

    base_rows = projected_rows(list(canonical.values()), comp)
    base_mod = tuple(mod_rank(base_rows, p) for p in PRIMES)
    base_exact = exact_rank(base_rows)
    assert base_exact == BASELINE_QR
    assert all(r <= base_exact for r in base_mod)
    print('baseline', 'mod_ranks', base_mod, 'exact_rank', base_exact, flush=True)

    records = []
    for name, order in variants(E, H):
        B = make_basis(order)
        rows = projected_rows(B, comp)
        mr = tuple(mod_rank(rows, p) for p in PRIMES)
        lower = max(mr)
        records.append((lower, name, mr, rows))
        print('variant', name, 'mod_ranks', mr, 'mod_lower_bound', lower, flush=True)

    candidates = sorted(rec for rec in records if rec[0] < BASELINE_QR)
    if not candidates:
        print('exact_candidate', 'NONE', 'reason=no_variant_has_modular_rank_below_baseline', flush=True)
        print('PASS V26_Q138_C_UNIFORM_SECOND_RESIDUE_BASIS_GAUGE_PROBE')
        print('scope=deterministic basis-order gauge search only; no improved uniform bound found')
        return

    best = None
    for lower, name, mr, rows in candidates:
        er = exact_rank(rows)
        print('exact_candidate', name, 'mod_ranks', mr, 'exact_rank', er, flush=True)
        assert er >= lower
        if best is None or er < best[0]:
            best = (er, name)
        if er < BASELINE_QR:
            print('UNIFORM_C_SECOND_LIFT_CANDIDATE', EXPECTED_SUPPORT + er,
                  'quotient_rank', er, 'baseline', EXPECTED_SUPPORT + BASELINE_QR,
                  'variant', name, flush=True)

    assert best is not None
    if best[0] >= BASELINE_QR:
        print('no_exact_improvement', 'best_candidate', best[1],
              'candidate_exact_rank', best[0], flush=True)

    print('PASS V26_Q138_C_UNIFORM_SECOND_RESIDUE_BASIS_GAUGE_PROBE')
    print('scope=deterministic GF2 basis-order gauge search on the admitted uniform C sign span')
    print('claim=any printed exact improvement is a valid alternative binary-lift upper bound; search is not optimal')


if __name__ == '__main__':
    main()
