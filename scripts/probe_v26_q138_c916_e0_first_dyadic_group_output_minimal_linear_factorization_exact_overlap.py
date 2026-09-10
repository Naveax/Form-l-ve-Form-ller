#!/usr/bin/env python3
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_group_output_minimal_linear_factorization as B

D = B.D
W = B.W
PHYS_N = B.PHYS_N
EXTENDED_HASH_ROUNDS_PER_TERM = 1024


def build_frequency_transform(term, manual_support, n=PHYS_N):
    anchor = term['anchor']
    sbasis = tuple(int(x) for x in anchor['physical_support_basis'])
    d = len(sbasis)
    c = int(anchor['normalized_sign_constant'])
    qlin = int(anchor['normalized_sign_linear'])
    qrows = tuple(int(x) for x in anchor['normalized_sign_rows'])
    assert len(qrows) == d

    total = n + d
    rows = [0] * total

    # Local quadratic q(z).
    for i in range(d):
        hi = qrows[i] & ~((1 << (i + 1)) - 1)
        while hi:
            bit = hi & -hi
            j = bit.bit_length() - 1
            a = n + i
            b = n + j
            rows[a] |= 1 << b
            rows[b] |= 1 << a
            hi ^= bit

    # Cross term omega . B z.
    for i, vec in enumerate(sbasis):
        local = n + i
        y = vec
        while y:
            bit = y & -y
            shared = bit.bit_length() - 1
            assert shared < n
            rows[shared] |= 1 << local
            rows[local] |= 1 << shared
            y ^= bit

    # omega . x0 is shared-linear; qlin is local-linear.
    lin = int(anchor['physical_support_x0']) | (qlin << n)
    got = D.P.L.partial_gauss_eliminate(c, lin, tuple(rows), n, d)
    assert not got['identically_zero']
    assert got['support_free_dimension'] is not None
    assert got['log2_abs_nonzero_gauss'] is not None

    expected_exp = d - (manual_support['polar_rank'] // 2)
    assert got['log2_abs_nonzero_gauss'] == expected_exp
    assert got['support_control_rank'] == manual_support['support_rank']
    assert got['support_free_dimension'] == manual_support['support_dimension']

    fx0 = int(got['support_x0'])
    fbasis = tuple(int(x) for x in got['support_basis'])
    fconstraints = D.P.affine_constraints_from_param(fx0, fbasis, n)

    # Independent cross-check: symbolic elimination support must equal the
    # radical-consistency support derived by the first pass. Same dimension
    # plus containment proves affine-space equality.
    for mask, rhs in manual_support['support_constraints']:
        assert B.parity(mask & fx0) == rhs
        assert all(B.parity(mask & v) == 0 for v in fbasis)

    fanchor = {
        'physical_support_x0': fx0,
        'physical_support_basis': fbasis,
        'physical_support_constraints': fconstraints,
        'normalized_sign_constant': int(got['normalized_sign_constant']),
        'normalized_sign_linear': int(got['normalized_sign_linear']),
        'normalized_sign_rows': tuple(int(x) for x in got['normalized_sign_rows']),
        '_coordinate_solver': D.P.coordinate_solver(fbasis),
    }
    return {
        'anchor': fanchor,
        'amplitude': int(term['coefficient']) << got['log2_abs_nonzero_gauss'],
        'log2_gauss_amplitude': got['log2_abs_nonzero_gauss'],
        'support_dimension': len(fbasis),
        'support_rank': got['support_control_rank'],
    }


def eval_frequency_transform(transform, omega):
    sign = D.P.eval_anchor_sign(transform['anchor'], int(omega))
    if sign is None:
        return 0
    amp = int(transform['amplitude'])
    return -amp if sign else amp


def exact_group_walsh(transforms, omega):
    return sum(eval_frequency_transform(t, omega) for t in transforms)


def synthetic_exact_transform_regression():
    n = 5
    systems = (
        (),
        ((1, 0),),
        ((1, 1),),
        ((3, 0),),
        ((3, 1),),
        ((1, 1), (6, 0)),
        ((5, 1), (10, 0)),
    )
    variants = (
        (0, 0b00000, 0x000),
        (1, 0b10101, 0x155),
        (0, 0b11110, 0x0D3),
        (1, 0b00111, 0x1A7),
    )
    tid = 0
    frequencies = 0
    for si, constraints in enumerate(systems):
        for vi, (c, lin, pair_seed) in enumerate(variants):
            anchor = B.make_custom_anchor(
                constraints, n, c, lin, pair_seed ^ (si << 3) ^ vi
            )
            term = {
                'term_id': tid,
                'group_id': 0,
                'kind': 'synthetic',
                'coefficient': (-3 if tid & 1 else 5),
                'anchor': anchor,
                'ambient_dimension': n,
            }
            tid += 1
            manual = B.term_fourier_support(term, n=n)
            transform = build_frequency_transform(term, manual, n=n)
            for omega in range(1 << n):
                got = eval_frequency_transform(transform, omega)
                brute = B.brute_term_walsh(term, omega, n)
                assert got == brute, (
                    constraints, c, lin, pair_seed, omega, got, brute
                )
                frequencies += 1
    assert tid == 28 and frequencies == 896
    return {'terms': tid, 'frequencies': frequencies}


def independent_of(lower, row):
    y = int(row)
    while y:
        p = y.bit_length() - 1
        old = lower.pivots.get(p)
        if old is None:
            return True
        y ^= old
    return False


def extended_candidate_stream(gid, supports):
    yield from B.candidate_stream(gid, supports)
    for round_index in range(
        B.HASH_ROUNDS_PER_TERM, EXTENDED_HASH_ROUNDS_PER_TERM
    ):
        for ti, rec in enumerate(supports):
            yield 'extended_support_hash', ti, B.hashed_affine_point(
                gid, ti, rec, round_index
            )


def exact_overlap_close_group(gid, group, rec):
    supports = rec['term_supports']
    transforms = tuple(
        build_frequency_transform(term, support)
        for term, support in zip(group['terms'], supports)
    )
    lower = B.IncrementalBasis()
    for witness in rec['candidate_unique_points']:
        assert lower.add(witness['frequency'])
    assert lower.rank == rec['lower_rank']

    target = rec['upper_rank']
    seen = set()
    exact_evaluations = 0
    nonzero_evaluations = 0
    zero_evaluations = 0
    source_evaluated = Counter()
    source_rank = Counter()
    rank_witnesses = []

    for source, _ti, omega in extended_candidate_stream(gid, supports):
        if lower.rank == target:
            break
        if omega in seen:
            continue
        seen.add(omega)
        if not independent_of(lower, omega):
            continue
        source_evaluated[source] += 1
        exact_evaluations += 1
        value = exact_group_walsh(transforms, omega)
        if value == 0:
            zero_evaluations += 1
            continue
        nonzero_evaluations += 1
        assert lower.add(omega)
        source_rank[source] += 1
        rank_witnesses.append({
            'frequency': int(omega),
            'source': source,
            'walsh_value': int(value),
        })

    lower_basis = lower.canonical()
    assert len(lower_basis) == lower.rank
    upper_basis = rec['upper_basis']
    union_rank = len(B.canonical_basis(list(lower_basis) + list(upper_basis)))
    assert union_rank == target
    return {
        'group_id': gid,
        'lower_basis': lower_basis,
        'lower_rank': lower.rank,
        'upper_rank': target,
        'exact': lower.rank == target,
        'minimal_space_digest': B.space_digest(lower_basis)
            if lower.rank == target else None,
        'exact_evaluations': exact_evaluations,
        'nonzero_evaluations': nonzero_evaluations,
        'zero_evaluations': zero_evaluations,
        'source_evaluated': dict(sorted(source_evaluated.items())),
        'source_rank_increase': dict(sorted(source_rank.items())),
        'exact_rank_witnesses': tuple(rank_witnesses),
        'transform_support_crosscheck_terms': len(transforms),
    }


def build_closed_spaces():
    base_records, mult_hist = B.build_minimal_spaces()
    physical_groups, physical_terms, mult2 = W.build_physical_groups()
    assert mult2 == mult_hist == {1: 103, 2: 57, 4: 90}
    assert len(physical_terms) == 680

    records = []
    for gid, (base, group) in enumerate(zip(base_records, physical_groups)):
        assert base['group_id'] == group['group_id'] == gid
        if base['exact']:
            minimal_basis = tuple(base['minimal_basis'])
            assert len(minimal_basis) == base['lower_rank'] == base['upper_rank']
            records.append({
                **base,
                'minimal_basis': minimal_basis,
                'closure_method': 'unique_term_support',
                'exact_overlap_evaluations': 0,
                'exact_overlap_zero_evaluations': 0,
                'exact_overlap_nonzero_evaluations': 0,
                'exact_overlap_source_rank_increase': {},
            })
            continue

        closure = exact_overlap_close_group(gid, group, base)
        records.append({
            **base,
            'lower_rank': closure['lower_rank'],
            'exact': closure['exact'],
            'minimal_basis': closure['lower_basis'] if closure['exact'] else None,
            'minimal_space_digest': closure['minimal_space_digest'],
            'closure_method': 'exact_overlap_walsh' if closure['exact'] else 'unresolved',
            'exact_overlap_evaluations': closure['exact_evaluations'],
            'exact_overlap_zero_evaluations': closure['zero_evaluations'],
            'exact_overlap_nonzero_evaluations': closure['nonzero_evaluations'],
            'exact_overlap_source_rank_increase': closure['source_rank_increase'],
            'exact_overlap_rank_witnesses': closure['exact_rank_witnesses'],
            'transform_support_crosscheck_terms': closure['transform_support_crosscheck_terms'],
        })
    return records, mult_hist


def analyze():
    regression = synthetic_exact_transform_regression()
    records, mult_hist = build_closed_spaces()

    exact = [r for r in records if r['exact']]
    exact_hist = Counter(r['lower_rank'] for r in exact)
    exact_by_mult = defaultdict(Counter)
    method_hist = Counter(r['closure_method'] for r in records)
    delta_hist = Counter()
    upper_hist = Counter(r['upper_rank'] for r in records)
    lower_hist = Counter(r['lower_rank'] for r in records)
    overlap_evals = 0
    overlap_zero = 0
    overlap_nonzero = 0
    overlap_source_rank = Counter()

    for rec in records:
        if rec['exact']:
            exact_by_mult[rec['multiplicity']][rec['lower_rank']] += 1
            delta_hist[rec['lower_rank'] - rec['refined_rank']] += 1
        overlap_evals += rec.get('exact_overlap_evaluations', 0)
        overlap_zero += rec.get('exact_overlap_zero_evaluations', 0)
        overlap_nonzero += rec.get('exact_overlap_nonzero_evaluations', 0)
        overlap_source_rank.update(rec.get('exact_overlap_source_rank_increase', {}))

    closed = len(exact)
    decision = (
        'EXACT_MINIMAL_LINEAR_FACTORIZATION_RANKS_CLOSED_FOR_250_GROUPS'
        if closed == 250
        else f'MINIMAL_LINEAR_FACTORIZATION_EXACT_OVERLAP_UNRESOLVED_{250 - closed}'
    )

    compact = [{
        'group_id': r['group_id'],
        'multiplicity': r['multiplicity'],
        'refined_rank': r['refined_rank'],
        'minimal_rank': r['lower_rank'] if r['exact'] else None,
        'lower_rank': r['lower_rank'],
        'upper_rank': r['upper_rank'],
        'exact': r['exact'],
        'closure_method': r['closure_method'],
        'minimal_space_digest': r['minimal_space_digest'],
        'exact_overlap_evaluations': r.get('exact_overlap_evaluations', 0),
        'exact_overlap_zero_evaluations': r.get('exact_overlap_zero_evaluations', 0),
        'exact_overlap_nonzero_evaluations': r.get('exact_overlap_nonzero_evaluations', 0),
        'exact_overlap_source_rank_increase': r.get(
            'exact_overlap_source_rank_increase', {}
        ),
    } for r in records]

    out = {
        'position': 'C',
        'physical_shared_dimension': PHYS_N,
        'synthetic_exact_fourier_transform_regression': regression,
        'support_groups': 250,
        'support_multiplicity_histogram': mult_hist,
        'physical_term_count': 680,
        'base_unique_support_exact_groups': sum(
            r['closure_method'] == 'unique_term_support' for r in records
        ),
        'exact_overlap_closed_groups': sum(
            r['closure_method'] == 'exact_overlap_walsh' for r in records
        ),
        'exact_groups': closed,
        'unresolved_groups': 250 - closed,
        'lower_rank_histogram': dict(sorted(lower_hist.items())),
        'upper_rank_histogram': dict(sorted(upper_hist.items())),
        'exact_minimal_rank_histogram': dict(sorted(exact_hist.items())),
        'exact_rank_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(exact_by_mult.items())
        },
        'minimal_rank_minus_refined_rank_histogram': dict(sorted(delta_hist.items())),
        'closure_method_histogram': dict(sorted(method_hist.items())),
        'exact_overlap_totals': {
            'evaluations': overlap_evals,
            'zero_evaluations': overlap_zero,
            'nonzero_evaluations': overlap_nonzero,
            'source_rank_increase': dict(sorted(overlap_source_rank.items())),
        },
        'extended_hash_rounds_per_term': EXTENDED_HASH_ROUNDS_PER_TERM,
        'groups': compact,
        'decision': decision,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_GROUP_OUTPUT_MINIMAL_LINEAR_FACTORIZATION_EXACT_OVERLAP')
    print('scope=exact closure of minimal linear factorization spaces using symbolic per-term Walsh transforms and exact overlap cancellation on top of the unique-support certificates')
    print('theorem=when lower rank equals the exact union-of-term-Walsh-support upper rank, the reported row space is the exact minimal linear factorization space of that group output')
    print('crosscheck=every symbolic per-term Walsh support is independently required to equal the radical-consistency affine support from the first pass; synthetic exact Walsh values are brute-force checked')
    print('not_included=nonlinear compression, phase-complete separator width, exact all-250 joint image, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
