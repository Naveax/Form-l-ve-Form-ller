#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_bc_e0_aggregate_signature_separator as A
import probe_v26_q138_c916_aggregate_e0_scalar_separator as G

POS = 'C'
DOMAIN_BITS = 149


def rows_from_pair_mask(n, pair_mask):
    rows = [0] * n
    k = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (pair_mask >> k) & 1:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
            k += 1
    return rows


def q_eval(rows, lin, c, x):
    z = c ^ ((lin & x).bit_count() & 1)
    y = x
    while y:
        b = y & -y
        i = b.bit_length() - 1
        z ^= ((rows[i] & x & ~((1 << (i + 1)) - 1)).bit_count() & 1)
        y ^= b
    return z


def quadratic_gauss_sum(rows0, lin0, c0, n):
    """Exact sum_x (-1)^q(x) for a Boolean quadratic q over F2^n.

    Repeatedly eliminate one hyperbolic pair x_i x_j using

      sum_{x_i,x_j} (-1)^(x_i x_j + a x_i + b x_j) = 2 (-1)^(a b).

    The affine forms a,b may depend on the remaining variables; their product
    is folded back into the remaining quadratic/linear/constant coefficients.
    No 2^n state enumeration is used.
    """
    rows = [int(r) for r in rows0]
    lin = int(lin0)
    c = int(c0) & 1
    active = (1 << n) - 1
    pairs = 0

    while True:
        i = None
        j = None
        x = active
        while x:
            bi = x & -x
            ii = bi.bit_length() - 1
            nbr = rows[ii] & active & ~bi
            if nbr:
                i = ii
                bj = nbr & -nbr
                j = bj.bit_length() - 1
                break
            x ^= bi
        if i is None:
            break

        rem = active & ~(1 << i) & ~(1 << j)
        avec = rows[i] & rem
        bvec = rows[j] & rem
        a0 = (lin >> i) & 1
        b0 = (lin >> j) & 1

        # Fold the affine product a(z)b(z) into q(z).
        if a0 & b0:
            c ^= 1
        newlin = lin & rem
        if a0:
            newlin ^= bvec
        if b0:
            newlin ^= avec
        newlin ^= avec & bvec  # Boolean diagonal z_k^2 = z_k.
        lin = newlin

        y = rem
        while y:
            bk = y & -y
            k = bk.bit_length() - 1
            r = rows[k] & rem
            if (avec >> k) & 1:
                r ^= bvec
            if (bvec >> k) & 1:
                r ^= avec
            r &= ~(1 << k)
            rows[k] = r
            y ^= bk
        rows[i] = 0
        rows[j] = 0
        active = rem
        pairs += 1

    residual_dim = active.bit_count()
    residual_linear = lin & active
    polar_rank = 2 * pairs
    assert polar_rank + residual_dim == n

    if residual_linear:
        return {
            'sum': 0,
            'sign': 0,
            'log2_abs': None,
            'polar_rank': polar_rank,
            'radical_dim': residual_dim,
            'radical_linear_obstruction': True,
        }

    log2_abs = pairs + residual_dim
    total = (-1 if c else 1) * (1 << log2_abs)
    return {
        'sum': total,
        'sign': -1 if c else 1,
        'log2_abs': log2_abs,
        'polar_rank': polar_rank,
        'radical_dim': residual_dim,
        'radical_linear_obstruction': False,
    }


def exhaustive_small_regression():
    tested = 0
    for n in range(1, 5):
        pair_bits = n * (n - 1) // 2
        for pm in range(1 << pair_bits):
            rows = rows_from_pair_mask(n, pm)
            expected_rank = A.L.rank(rows)
            for lin in range(1 << n):
                for c in (0, 1):
                    got = quadratic_gauss_sum(rows, lin, c, n)
                    brute = 0
                    for x in range(1 << n):
                        brute += -1 if q_eval(rows, lin, c, x) else 1
                    assert got['sum'] == brute, (n, pm, lin, c, got, brute)
                    assert got['polar_rank'] == expected_rank
                    tested += 1
    return tested


def aggregate_scalar_coefficients(sectors):
    rows, delta, phases = G.aggregate_scalar_phase(POS, sectors)
    lin = 0
    for i in range(DOMAIN_BITS):
        if delta(1 << i):
            lin |= 1 << i
    c = 0
    for ph in phases:
        c ^= ph['c']
    return rows, lin, c


def analyze():
    small_tests = exhaustive_small_regression()
    raw, canonical = A.build_groups(POS)
    assert raw == 577 and len(canonical) == 250

    e0, _e1, _half = A.L.U.H.classify_patterns()
    grouped = defaultdict(list)
    for k in range(4):
        for zs, cls in e0[k]:
            can = A.L.U.H.support_for(POS, zs, cls)
            if can is not None:
                grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert len(ordered) == len(canonical)

    by_mult = {1: Counter(), 2: Counter(), 4: Counter()}
    rank_hist = Counter()
    zero_hist = Counter()
    nonzero_sign_hist = Counter()
    nonzero_log_hist = Counter()
    nonzero = 0
    zero = 0

    for gid, ((_can, sectors), info) in enumerate(zip(ordered, canonical)):
        assert gid == info['group_id']
        mult = info['multiplicity']
        assert len(sectors) == mult
        rows, lin, c = aggregate_scalar_coefficients(sectors)
        got = quadratic_gauss_sum(rows, lin, c, DOMAIN_BITS)
        exact_rank = A.L.rank(rows)
        assert got['polar_rank'] == exact_rank
        rank_hist[exact_rank] += 1
        key = (
            got['polar_rank'],
            got['radical_dim'],
            got['sign'],
            got['log2_abs'],
        )
        by_mult[mult][key] += 1
        if got['sum'] == 0:
            zero += 1
            zero_hist[(mult, exact_rank)] += 1
            assert got['radical_linear_obstruction']
        else:
            nonzero += 1
            nonzero_sign_hist[(mult, got['sign'])] += 1
            nonzero_log_hist[(mult, got['log2_abs'])] += 1
            assert not got['radical_linear_obstruction']
            assert got['log2_abs'] == DOMAIN_BITS - exact_rank // 2

    assert zero + nonzero == 250
    out = {
        'position': POS,
        'small_quadratic_forms_exhaustively_checked': small_tests,
        'groups': 250,
        'polar_rank_histogram': {str(k): v for k, v in sorted(rank_hist.items())},
        'gauss_zero_groups': zero,
        'gauss_nonzero_groups': nonzero,
        'zero_histogram_by_multiplicity_and_rank': {
            f'{m}:{r}': v for (m, r), v in sorted(zero_hist.items())
        },
        'nonzero_sign_histogram_by_multiplicity': {
            f'{m}:{s}': v for (m, s), v in sorted(nonzero_sign_hist.items())
        },
        'nonzero_log2_abs_histogram_by_multiplicity': {
            f'{m}:{e}': v for (m, e), v in sorted(nonzero_log_hist.items())
        },
        'class_histograms_by_multiplicity': {
            str(m): {
                f'rank{r}_rad{d}_sign{s}_log{e}': v
                for (r, d, s, e), v in sorted(C.items(), key=lambda kv: str(kv[0]))
            }
            for m, C in by_mult.items()
        },
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_AGGREGATE_SCALAR_GAUSS_CLASSES')
    print('method=polynomial-time exact hyperbolic-pair elimination; exhaustive regression over every Boolean quadratic in n<=4')
    print('scope=global Gauss-sum class of each individual C same-support aggregate right-only scalar over the 149 shared variables')
    print('important=individual scalar Gauss classes are a reusable nonlinear primitive, not an aggregate carry or separator-state theorem')
    print('not_included=cut-restricted Gauss sums, aggregate e0 carry, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


def main():
    analyze()


if __name__ == '__main__':
    main()
