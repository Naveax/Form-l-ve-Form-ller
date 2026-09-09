#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_same_support_integer_coefficients as C
import probe_v26_q138_c916_e0_complete_first_dyadic_fiber_geometry as G
import probe_v26_q138_c916_e0_first_dyadic_gauss_radical_control as R
import probe_v26_q138_c916_e0_first_dyadic_pair_residual as D

POS = 'C'


def q_eval(c, lin, rows, x):
    z = (c & 1) ^ ((lin & x).bit_count() & 1)
    y = x
    while y:
        b = y & -y
        i = b.bit_length() - 1
        hi = x & ~((1 << (i + 1)) - 1)
        z ^= ((rows[i] & hi).bit_count() & 1)
        y ^= b
    return z


def restrict_form(c, lin, rows, x0, basis):
    d = len(basis)
    c0 = q_eval(c, lin, rows, x0)
    out_lin = 0
    for i, b in enumerate(basis):
        if q_eval(c, lin, rows, x0 ^ b) ^ c0:
            out_lin |= 1 << i

    images = [G.polar_apply(rows, b) for b in basis]
    out_rows = [0] * d
    for i in range(d):
        for j in range(i + 1, d):
            if (images[i] & basis[j]).bit_count() & 1:
                out_rows[i] |= 1 << j
                out_rows[j] |= 1 << i
    return c0, out_lin, tuple(out_rows)


def complement_to_kernel(kernel, d):
    span = list(kernel)
    assert D.gf2_rank(span) == len(span)
    quotient = []
    for i in range(d):
        e = 1 << i
        if D.gf2_rank(span + [e]) > len(span):
            span.append(e)
            quotient.append(e)
    assert len(span) == d
    assert len(quotient) + len(kernel) == d
    return tuple(quotient)


def transform_signature(sig, d, basis):
    assert len(basis) == d
    c = sig & 1
    lin, rows = G.signature_form(sig, d)
    return restrict_form(c, lin, rows, 0, basis)


def local_polar_rank(rows, p, k):
    lmask = ((1 << k) - 1) << p
    local = []
    for i in range(p, p + k):
        local.append((rows[i] & lmask) >> p)
    out = D.gf2_rank(local)
    assert out % 2 == 0
    return out


def partial_gauss_eliminate(c0, lin0, rows0, p, k):
    n = p + k
    assert len(rows0) == n
    rows = [int(r) for r in rows0]
    lin = int(lin0)
    c = int(c0) & 1
    active_local = set(range(p, n))
    pairs = 0

    while True:
        found = None
        local_mask = sum(1 << i for i in active_local)
        for i in sorted(active_local):
            nbr = rows[i] & local_mask & ~(1 << i)
            if nbr:
                bj = nbr & -nbr
                found = (i, bj.bit_length() - 1)
                break
        if found is None:
            break

        i, j = found
        rem_mask = ((1 << n) - 1) & ~(1 << i) & ~(1 << j)
        avec = rows[i] & rem_mask
        bvec = rows[j] & rem_mask
        a0 = (lin >> i) & 1
        b0 = (lin >> j) & 1

        # Exact hyperbolic-pair identity:
        # sum_{xi,xj} (-1)^(xi*xj + a*xi + b*xj) = 2*(-1)^(a*b).
        if a0 & b0:
            c ^= 1
        newlin = lin & rem_mask
        if a0:
            newlin ^= bvec
        if b0:
            newlin ^= avec
        newlin ^= avec & bvec
        lin = newlin

        for t in range(n):
            if t in (i, j):
                continue
            row = rows[t] & rem_mask
            if (avec >> t) & 1:
                row ^= bvec
            if (bvec >> t) & 1:
                row ^= avec
            row &= ~(1 << t)
            rows[t] = row

        rows[i] = 0
        rows[j] = 0
        active_local.remove(i)
        active_local.remove(j)
        pairs += 1

    local_mask = sum(1 << i for i in active_local)
    assert all((rows[i] & local_mask) == 0 for i in active_local)

    smask = (1 << p) - 1
    constraints = [
        (rows[i] & smask, (lin >> i) & 1)
        for i in sorted(active_local)
    ]
    sol = C.P.U.T.rref(constraints, n=p)
    assert sol is not None
    control_rank, support_x0, support_basis = sol
    support_basis = tuple(support_basis)

    shared_rows = tuple(rows[i] & smask for i in range(p))
    shared_lin = lin & smask
    sc, slin, srows = restrict_form(
        c, shared_lin, shared_rows, support_x0, support_basis
    )
    sign_polar_rank = D.gf2_rank(srows)
    assert sign_polar_rank % 2 == 0

    return {
        'hyperbolic_pairs': pairs,
        'radical_dimension': len(active_local),
        'support_control_rank': control_rank,
        'support_control_rows': tuple(m for m, _rhs in constraints),
        'support_control_rhs': tuple(rhs for _m, rhs in constraints),
        'support_x0': support_x0,
        'support_basis': support_basis,
        'support_free_dimension': len(support_basis),
        'log2_abs_nonzero_gauss': pairs + len(active_local),
        'shared_survivor_constant': c,
        'shared_survivor_linear': shared_lin,
        'shared_survivor_rows': shared_rows,
        'normalized_sign_constant': sc,
        'normalized_sign_linear': slin,
        'normalized_sign_rows': srows,
        'normalized_sign_polar_rank': sign_polar_rank,
        'normalized_sign_is_affine': sign_polar_rank == 0,
        'normalized_sign_is_constant': sign_polar_rank == 0 and slin == 0,
    }


def rows_from_pair_mask(n, pair_mask):
    rows = [0] * n
    bit = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (pair_mask >> bit) & 1:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
            bit += 1
    return tuple(rows)


def partial_gauss_regression_split(p, k):
    n = p + k
    assert n == 4
    pair_bits = n * (n - 1) // 2
    tested = 0
    for pm in range(1 << pair_bits):
        rows = rows_from_pair_mask(n, pm)
        for lin in range(1 << n):
            for c in (0, 1):
                got = partial_gauss_eliminate(c, lin, rows, p, k)
                constraints = list(zip(
                    got['support_control_rows'],
                    got['support_control_rhs'],
                ))
                for s in range(1 << p):
                    brute = 0
                    for local in range(1 << k):
                        x = s | (local << p)
                        brute += -1 if q_eval(c, lin, rows, x) else 1

                    feasible = all(
                        ((m & s).bit_count() & 1) == rhs
                        for m, rhs in constraints
                    )
                    if feasible:
                        sign = q_eval(
                            got['shared_survivor_constant'],
                            got['shared_survivor_linear'],
                            got['shared_survivor_rows'],
                            s,
                        )
                        predicted = (-1 if sign else 1) * (
                            1 << got['log2_abs_nonzero_gauss']
                        )
                    else:
                        predicted = 0
                    assert predicted == brute, (
                        p, k, pm, lin, c, s, got, brute, predicted
                    )
                tested += 1
    return tested


def analyze():
    regression_forms = (
        partial_gauss_regression_split(2, 2)
        + partial_gauss_regression_split(1, 3)
    )
    assert regression_forms == 4096

    e0, _e1, _half = C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for zc in range(4):
        for zs, cls in e0[zc]:
            can = C.P.U.H.support_for(POS, zs, cls)
            if can is not None:
                raw += 1
                grouped[can].append((zs, cls))
    assert raw == 577 and len(grouped) == 250

    mult_hist = Counter()
    projection_hist = Counter()
    local_dim_hist = Counter()
    local_polar_hist = Counter()
    radical_hist = Counter()
    control_hist = Counter()
    amplitude_hist = Counter()
    sign_rank_hist = Counter()
    sign_free_dim_hist = Counter()
    sign_affine = 0
    sign_constant = 0

    by_mult_sign_rank = defaultdict(Counter)
    by_mult_amplitude = defaultdict(Counter)
    compact = []

    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        m = len(sectors)
        mult_hist[m] += 1
        _srank, x0, support_basis = C.X.support_param(can)
        d = len(support_basis)
        projection_rank, kernel = G.local_fiber_coeff_basis(support_basis)
        k = len(kernel)
        quotient = complement_to_kernel(kernel, d)
        assert len(quotient) == projection_rank
        adapted = quotient + tuple(kernel)
        assert D.gf2_rank(adapted) == d

        sector_records = []
        for zs, _cls in sectors:
            sig, sd, _nbits = C.X.restricted_phase_signature(
                C.phase_tuple(zs), x0, support_basis
            )
            assert sd == d
            tc, tlin, trows = transform_signature(sig, d, adapted)
            lrank = local_polar_rank(trows, projection_rank, k)
            got = partial_gauss_eliminate(
                tc, tlin, trows, projection_rank, k
            )
            assert 2 * got['hyperbolic_pairs'] == lrank
            assert got['radical_dimension'] == k - lrank

            old = R.sector_radical_controls(sig, d, kernel)
            assert got['radical_dimension'] == old['local_fiber_radical_dimension']
            assert got['support_control_rank'] == old['shared_projection_radical_control_rank']
            assert got['support_control_rank'] == got['radical_dimension']

            projection_hist[projection_rank] += 1
            local_dim_hist[k] += 1
            local_polar_hist[lrank] += 1
            radical_hist[got['radical_dimension']] += 1
            control_hist[got['support_control_rank']] += 1
            amplitude_hist[got['log2_abs_nonzero_gauss']] += 1
            sign_rank_hist[got['normalized_sign_polar_rank']] += 1
            sign_free_dim_hist[got['support_free_dimension']] += 1
            sign_affine += int(got['normalized_sign_is_affine'])
            sign_constant += int(got['normalized_sign_is_constant'])
            by_mult_sign_rank[m][got['normalized_sign_polar_rank']] += 1
            by_mult_amplitude[m][got['log2_abs_nonzero_gauss']] += 1

            sector_records.append({
                'local_fiber_dimension': k,
                'local_polar_rank': lrank,
                'radical_dimension': got['radical_dimension'],
                'support_control_rank': got['support_control_rank'],
                'support_free_dimension_after_radical_constraints': got['support_free_dimension'],
                'log2_abs_nonzero_gauss': got['log2_abs_nonzero_gauss'],
                'normalized_sign_polar_rank': got['normalized_sign_polar_rank'],
                'normalized_sign_is_affine': got['normalized_sign_is_affine'],
                'normalized_sign_is_constant': got['normalized_sign_is_constant'],
            })

        compact.append({
            'group_id': gid,
            'multiplicity': m,
            'support_free_dimension': d,
            'shared_projection_rank': projection_rank,
            'local_fiber_dimension': k,
            'sectors': sector_records,
        })

    assert dict(sorted(mult_hist.items())) == {1: 103, 2: 57, 4: 90}
    assert sum(sign_rank_hist.values()) == 577
    assert dict(sorted(control_hist.items())) == {
        0: 3, 1: 88, 2: 172, 3: 180, 4: 134,
    }

    out = {
        'position': POS,
        'small_split_quadratic_forms_exhaustively_checked': regression_forms,
        'raw_e0_sectors': raw,
        'support_groups': len(grouped),
        'support_multiplicity_histogram': dict(sorted(mult_hist.items())),
        'shared_projection_rank_histogram': dict(sorted(projection_hist.items())),
        'local_fiber_dimension_histogram': dict(sorted(local_dim_hist.items())),
        'local_fiber_polar_rank_histogram': dict(sorted(local_polar_hist.items())),
        'local_fiber_radical_dimension_histogram': dict(sorted(radical_hist.items())),
        'support_control_rank_histogram': dict(sorted(control_hist.items())),
        'nonzero_gauss_log2_abs_histogram': dict(sorted(amplitude_hist.items())),
        'support_free_dimension_after_radical_constraints_histogram': dict(sorted(sign_free_dim_hist.items())),
        'normalized_sign_polar_rank_histogram': dict(sorted(sign_rank_hist.items())),
        'normalized_sign_affine_sectors': sign_affine,
        'normalized_sign_constant_sectors': sign_constant,
        'max_normalized_sign_polar_rank': max(sign_rank_hist),
        'normalized_sign_polar_rank_by_multiplicity': {
            int(m): dict(sorted(h.items()))
            for m, h in sorted(by_mult_sign_rank.items())
        },
        'nonzero_gauss_log2_abs_by_multiplicity': {
            int(m): dict(sorted(h.items()))
            for m, h in sorted(by_mult_amplitude.items())
        },
        'groups': compact,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_LOCAL_GAUSS_TRANSFORM_QUOTIENT_GEOMETRY')
    print('scope=exact symbolic elimination of the 7-9 dimensional local support fiber for every one of the 577 C grouped-e0 sector characters, followed by exact restriction of the nonzero normalized Gauss sign to the radical-compatible shared support quotient')
    print('important=the reported normalized-sign polar rank is measured on each sector support quotient after radical constraints, so no arbitrary ambient 149-bit quadratic lift or quadratic gauge is used')
    print('next=combine the exact per-sector transforms according to the frozen singleton/pair first-dyadic arithmetic and measure pairwise support/amplitude/sign compatibility before separator-state assembly')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
