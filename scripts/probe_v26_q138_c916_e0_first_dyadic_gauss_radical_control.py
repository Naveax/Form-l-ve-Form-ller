#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_same_support_integer_coefficients as C
import probe_v26_q138_c916_e0_complete_first_dyadic_fiber_geometry as G
import probe_v26_q138_c916_e0_first_dyadic_pair_residual as D

POS = 'C'


def nullspace_basis(rows, n):
    # n <= 9 for the local support fibers here. Exhaustive enumeration keeps
    # the diagnostic transparent and independent of a basis convention.
    vals = []
    for x in range(1 << n):
        z = 0
        y = x
        while y:
            b = y & -y
            z ^= rows[b.bit_length() - 1]
            y ^= b
        if z == 0:
            vals.append(x)
    basis = C.P.U.S.row_basis(vals)
    assert len(vals) == 1 << len(basis)
    return tuple(basis)


def combine(vectors, coeff):
    z = 0
    y = coeff
    while y:
        b = y & -y
        z ^= vectors[b.bit_length() - 1]
        y ^= b
    return z


def restrict_polar_to_kernel(rows, kernel):
    out = []
    for x in kernel:
        px = G.polar_apply(rows, x)
        row = 0
        for j, y in enumerate(kernel):
            if (px & y).bit_count() & 1:
                row |= 1 << j
        out.append(row)
    return tuple(out)


def sector_radical_controls(sig, d, kernel):
    _linear, rows = G.signature_form(sig, d)
    krows = restrict_polar_to_kernel(rows, kernel)
    local_rank = D.gf2_rank(krows)
    assert local_rank % 2 == 0
    radical = nullspace_basis(krows, len(kernel))
    assert len(radical) == len(kernel) - local_rank

    controls = []
    for z in radical:
        r = combine(kernel, z)
        f = G.polar_apply(rows, r)
        # r is radical only after restriction to the local fiber. Therefore
        # B(r,.) must annihilate the projection kernel and descends exactly to
        # a linear functional on the shared support projection T/K.
        assert all(((f & k).bit_count() & 1) == 0 for k in kernel)
        if f:
            controls.append(f)
    controls = tuple(C.P.U.S.row_basis(controls))
    assert len(controls) <= len(radical)
    return {
        'local_fiber_polar_rank': local_rank,
        'local_fiber_radical_dimension': len(radical),
        'shared_projection_radical_control_rank': len(controls),
        'control_basis_pullback': controls,
    }


def analyze():
    e0, _e1, _half = C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = C.P.U.H.support_for(POS, zs, cls)
            if can is not None:
                raw += 1
                grouped[can].append((zs, cls))
    assert raw == 577 and len(grouped) == 250

    mult_hist = Counter()
    sector_fiber_dim = Counter()
    sector_polar_rank = Counter()
    sector_radical_dim = Counter()
    sector_control_rank = Counter()
    group_union_control_rank = Counter()
    by_mult_sector_polar = defaultdict(Counter)
    by_mult_sector_radical = defaultdict(Counter)
    by_mult_sector_control = defaultdict(Counter)
    by_mult_group_union = defaultdict(Counter)
    compact = []

    total_sector_controls = 0
    sectors_with_zero_control = 0

    for gid, (can, sectors) in enumerate(sorted(grouped.items(), key=lambda kv: kv[0])):
        m = len(sectors)
        mult_hist[m] += 1
        _srank, x0, support_basis = C.X.support_param(can)
        d = len(support_basis)
        projection_rank, kernel = G.local_fiber_coeff_basis(support_basis)
        kdim = len(kernel)
        assert projection_rank + kdim == d

        group_controls = []
        sector_records = []
        for zs, _cls in sectors:
            sig, sd, _nbits = C.X.restricted_phase_signature(
                C.phase_tuple(zs), x0, support_basis
            )
            assert sd == d
            rec = sector_radical_controls(sig, d, kernel)
            rank = rec['local_fiber_polar_rank']
            rdim = rec['local_fiber_radical_dimension']
            crank = rec['shared_projection_radical_control_rank']

            sector_fiber_dim[kdim] += 1
            sector_polar_rank[rank] += 1
            sector_radical_dim[rdim] += 1
            sector_control_rank[crank] += 1
            by_mult_sector_polar[m][rank] += 1
            by_mult_sector_radical[m][rdim] += 1
            by_mult_sector_control[m][crank] += 1
            total_sector_controls += crank
            sectors_with_zero_control += int(crank == 0)
            group_controls.extend(rec['control_basis_pullback'])
            sector_records.append({
                'local_fiber_polar_rank': rank,
                'local_fiber_radical_dimension': rdim,
                'shared_projection_radical_control_rank': crank,
            })

        union_basis = C.P.U.S.row_basis(group_controls)
        urank = len(union_basis)
        group_union_control_rank[urank] += 1
        by_mult_group_union[m][urank] += 1
        compact.append({
            'group_id': gid,
            'multiplicity': m,
            'support_free_dimension': d,
            'shared_projection_rank': projection_rank,
            'local_fiber_dimension': kdim,
            'group_shared_projection_radical_control_rank': urank,
            'sectors': sector_records,
        })

    assert dict(sorted(mult_hist.items())) == {1: 103, 2: 57, 4: 90}
    assert sum(sector_polar_rank.values()) == 577

    out = {
        'position': POS,
        'raw_e0_sectors': raw,
        'support_groups': len(grouped),
        'support_multiplicity_histogram': dict(sorted(mult_hist.items())),
        'sector_local_fiber_dimension_histogram': dict(sorted(sector_fiber_dim.items())),
        'sector_local_fiber_polar_rank_histogram': dict(sorted(sector_polar_rank.items())),
        'sector_local_fiber_radical_dimension_histogram': dict(sorted(sector_radical_dim.items())),
        'sector_shared_projection_radical_control_rank_histogram': dict(sorted(sector_control_rank.items())),
        'group_shared_projection_radical_control_rank_histogram': dict(sorted(group_union_control_rank.items())),
        'sector_polar_rank_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_sector_polar.items())
        },
        'sector_radical_dimension_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_sector_radical.items())
        },
        'sector_radical_control_rank_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_sector_control.items())
        },
        'group_radical_control_rank_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(by_mult_group_union.items())
        },
        'sectors_with_zero_shared_radical_control': sectors_with_zero_control,
        'sum_sector_radical_control_ranks': total_sector_controls,
        'max_sector_radical_control_rank': max(sector_control_rank),
        'max_group_radical_control_rank': max(group_union_control_rank),
        'groups': compact,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_GAUSS_RADICAL_CONTROL')
    print('scope=exact support-parameter diagnostic for all 577 C e0 sector characters: restrict each quadratic polar form to the common-support local fiber, take its radical, and measure the descended shared-projection linear controls B(r,.) that move the local Gauss cancellation/support coset')
    print('important=these controls are basis-independent pullbacks on T/K; this is not yet a separator-width theorem and does not charge Gauss transform phase/amplitude or signed integer carry arithmetic')
    print('next=if radical controls are small, construct compatible 149-bit shared representatives modulo support-projection gauge and combine them with the existing support/frequency skeleton cut by cut')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
