#!/usr/bin/env python3
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as D
import probe_v26_q138_c916_e0_first_dyadic_group_output_modp_rank_witness as W
import probe_v26_q138_c916_e0_first_dyadic_width61_local_signature_sufficiency as Q

POS = 'C'
PHYS_N = 149
HASH_ROUNDS_PER_TERM = 256
assert D.PHYS_N == W.PHYS_N == Q.PHYS_N == PHYS_N


def parity(x):
    return int(x).bit_count() & 1


def canonical_basis(rows, n=PHYS_N):
    work = sorted({int(x) for x in rows if int(x)}, reverse=True)
    out = []
    r = 0
    for col in range(n - 1, -1, -1):
        pivot = next((i for i in range(r, len(work)) if (work[i] >> col) & 1), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        pv = work[r]
        for i in range(len(work)):
            if i != r and ((work[i] >> col) & 1):
                work[i] ^= pv
        out.append(work[r])
        r += 1
        if r == len(work):
            break
    return tuple(out)


def space_digest(rows):
    rows = canonical_basis(rows)
    payload = b''.join(int(x).to_bytes(19, 'big') for x in rows)
    return hashlib.sha256(payload).hexdigest()


def homogeneous_kernel(rows, n):
    rows = tuple(canonical_basis(rows, n=n))
    sol = Q.B.C.P.U.T.rref([(row, 0) for row in rows], n=n)
    assert sol is not None
    rank, x0, kernel = sol
    assert x0 == 0
    assert rank == len(rows)
    assert rank + len(kernel) == n
    return tuple(int(x) for x in kernel)


def term_fourier_support(term, n=PHYS_N):
    anchor = term['anchor']
    support_basis = tuple(int(x) for x in anchor['physical_support_basis'])
    d = len(support_basis)
    c = int(anchor['normalized_sign_constant'])
    lin = int(anchor['normalized_sign_linear'])
    rows = tuple(int(x) for x in anchor['normalized_sign_rows'])
    assert len(rows) == d

    polar_rank = D.P.R.gf2_rank(rows)
    radical = homogeneous_kernel(rows, d)
    assert len(radical) == d - polar_rank

    equations = []
    for r in radical:
        mask = D.P.xor_combine(r, support_basis)
        assert mask != 0
        rhs = D.P.L.q_eval(c, lin, rows, r) ^ c
        equations.append((mask, rhs))

    sol = Q.B.C.P.U.T.rref(equations, n=n)
    assert sol is not None
    rank, x0, basis = sol
    basis = tuple(int(x) for x in basis)
    assert rank == len(radical)
    assert len(basis) == n - rank
    assert len(canonical_basis(basis, n=n)) == len(basis)

    constraints = tuple((int(mask), int(rhs)) for mask, rhs in equations)
    for mask, rhs in constraints:
        assert parity(mask & x0) == rhs
        assert all(parity(mask & b) == 0 for b in basis)

    hull = canonical_basis(([x0] if x0 else []) + list(basis), n=n)
    return {
        'term_id': int(term['term_id']),
        'kind': term['kind'],
        'coefficient': int(term['coefficient']),
        'support_rank': rank,
        'support_dimension': len(basis),
        'support_x0': int(x0),
        'support_basis': basis,
        'support_constraints': constraints,
        'linear_hull_basis': hull,
        'linear_hull_rank': len(hull),
        'polar_rank': polar_rank,
        'radical_dimension': len(radical),
    }


def in_fourier_support(rec, omega):
    return all(
        parity(int(mask) & int(omega)) == int(rhs)
        for mask, rhs in rec['support_constraints']
    )


def brute_term_walsh(term, omega, n):
    return sum(
        D.eval_term(term, x) * (-1 if parity(int(omega) & x) else 1)
        for x in range(1 << n)
    )


def make_custom_anchor(constraints, n, c, lin_seed, pair_seed):
    sol = Q.B.C.P.U.T.rref(constraints, n=n)
    assert sol is not None
    _rank, x0, basis = sol
    basis = tuple(int(x) for x in basis)
    d = len(basis)
    lin = int(lin_seed) & ((1 << d) - 1 if d else 0)
    rows = [0] * d
    for i in range(d):
        for j in range(i + 1, d):
            if ((pair_seed >> ((i * d + j) % 13)) & 1):
                rows[i] |= 1 << j
                rows[j] |= 1 << i
    return {
        'physical_support_x0': int(x0),
        'physical_support_basis': basis,
        'physical_support_constraints': tuple((int(a), int(b)) for a, b in constraints),
        'normalized_sign_constant': int(c) & 1,
        'normalized_sign_linear': lin,
        'normalized_sign_rows': tuple(rows),
        '_coordinate_solver': D.P.coordinate_solver(basis),
    }


def synthetic_regression():
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
    tested_terms = 0
    tested_frequencies = 0
    tid = 0
    for si, constraints in enumerate(systems):
        for vi, (c, lin, pair_seed) in enumerate(variants):
            anchor = make_custom_anchor(constraints, n, c, lin, pair_seed ^ (si << 3) ^ vi)
            term = {
                'term_id': tid,
                'group_id': 0,
                'kind': 'synthetic',
                'coefficient': (-3 if (tid & 1) else 5),
                'anchor': anchor,
                'ambient_dimension': n,
            }
            tid += 1
            rec = term_fourier_support(term, n=n)
            for omega in range(1 << n):
                brute = brute_term_walsh(term, omega, n)
                predicted = in_fourier_support(rec, omega)
                assert (brute != 0) == predicted, (
                    constraints, c, lin, pair_seed, omega, brute, rec
                )
                tested_frequencies += 1
            tested_terms += 1
    assert tested_terms == len(systems) * len(variants) == 28
    assert tested_frequencies == tested_terms * (1 << n) == 896
    return {
        'terms': tested_terms,
        'frequencies': tested_frequencies,
    }


def hashed_affine_point(gid, local_term_index, rec, round_index):
    basis = rec['support_basis']
    d = len(basis)
    seed = (
        f'c916-minlin:{gid}:{local_term_index}:{round_index}:{rec["term_id"]}'
    ).encode()
    raw = hashlib.shake_256(seed).digest((d + 7) // 8 or 1)
    coeff = int.from_bytes(raw, 'little')
    if d:
        coeff &= (1 << d) - 1
    else:
        coeff = 0
    return rec['support_x0'] ^ D.P.xor_combine(coeff, basis)


def candidate_stream(gid, supports):
    for ti, rec in enumerate(supports):
        yield 'support_origin', ti, rec['support_x0']
    for ti, rec in enumerate(supports):
        x0 = rec['support_x0']
        for bi, b in enumerate(rec['support_basis']):
            yield 'support_basis_single', ti, x0 ^ b
    for round_index in range(HASH_ROUNDS_PER_TERM):
        for ti, rec in enumerate(supports):
            yield 'support_hash', ti, hashed_affine_point(gid, ti, rec, round_index)


def certified_lower_space(gid, supports, upper_basis):
    target_rank = len(upper_basis)
    lower_basis = ()
    seen = set()
    unique_points = []
    source_seen = Counter()
    source_unique = Counter()
    source_rank_increase = Counter()
    owner_hist = Counter()
    candidates = 0
    duplicates = 0

    for source, _source_term, omega in candidate_stream(gid, supports):
        source_seen[source] += 1
        if omega in seen:
            duplicates += 1
            continue
        seen.add(omega)
        candidates += 1
        owners = [i for i, rec in enumerate(supports) if in_fourier_support(rec, omega)]
        owner_hist[len(owners)] += 1
        if len(owners) != 1:
            continue
        source_unique[source] += 1
        new_basis = canonical_basis(list(lower_basis) + [omega])
        if len(new_basis) > len(lower_basis):
            source_rank_increase[source] += 1
            unique_points.append({
                'frequency': int(omega),
                'owner_term_index': owners[0],
                'source': source,
            })
            lower_basis = new_basis
            if len(lower_basis) == target_rank:
                break

    return {
        'lower_basis': tuple(lower_basis),
        'lower_rank': len(lower_basis),
        'target_rank': target_rank,
        'candidate_unique_points': tuple(unique_points),
        'candidates_evaluated': candidates,
        'duplicates_skipped': duplicates,
        'source_seen': dict(sorted(source_seen.items())),
        'source_unique_support': dict(sorted(source_unique.items())),
        'source_rank_increase': dict(sorted(source_rank_increase.items())),
        'owner_count_histogram': dict(sorted(owner_hist.items())),
    }


def build_minimal_spaces():
    physical_groups, physical_terms, mult_hist = W.build_physical_groups()
    assert len(physical_groups) == 250
    assert len(physical_terms) == 680
    assert mult_hist == {1: 103, 2: 57, 4: 90}

    refined_groups, _order, _tree, cert = Q.build_refined_groups()
    assert cert['width'] == 61 and cert['max_depth'] == 11
    assert len(refined_groups) == len(physical_groups)

    records = []
    for gid, (group, refined) in enumerate(zip(physical_groups, refined_groups)):
        assert group['group_id'] == refined['group_id'] == gid
        assert group['multiplicity'] == refined['multiplicity']
        supports = tuple(term_fourier_support(term) for term in group['terms'])
        upper_basis = canonical_basis(
            row
            for rec in supports
            for row in rec['linear_hull_basis']
        )
        lower = certified_lower_space(gid, supports, upper_basis)
        lower_basis = lower.pop('lower_basis')
        lower_rank = len(lower_basis)
        upper_rank = len(upper_basis)
        assert lower_rank <= upper_rank <= PHYS_N
        exact = lower_rank == upper_rank
        if exact:
            assert canonical_basis(lower_basis) == canonical_basis(
                list(lower_basis) + list(upper_basis)
            )
        records.append({
            'group_id': gid,
            'multiplicity': group['multiplicity'],
            'physical_term_count': len(group['terms']),
            'refined_rank': refined['refined_rank'],
            'lower_rank': lower_rank,
            'upper_rank': upper_rank,
            'exact': exact,
            'minimal_basis': tuple(lower_basis) if exact else None,
            'upper_basis': tuple(upper_basis),
            'minimal_space_digest': space_digest(lower_basis) if exact else None,
            'upper_space_digest': space_digest(upper_basis),
            'term_supports': supports,
            **lower,
        })
    return records, mult_hist


def analyze():
    regression = synthetic_regression()
    records, mult_hist = build_minimal_spaces()

    lower_hist = Counter(r['lower_rank'] for r in records)
    upper_hist = Counter(r['upper_rank'] for r in records)
    exact_records = [r for r in records if r['exact']]
    exact_hist = Counter(r['lower_rank'] for r in exact_records)
    exact_by_mult = defaultdict(Counter)
    lower_by_mult = defaultdict(Counter)
    upper_by_mult = defaultdict(Counter)
    delta_lower_refined = Counter()
    delta_upper_refined = Counter()
    term_radical_hist = Counter()
    term_fourier_dim_hist = Counter()
    term_hull_rank_hist = Counter()
    total_candidates = 0
    total_duplicates = 0
    source_seen = Counter()
    source_unique = Counter()
    source_rank = Counter()

    for rec in records:
        m = rec['multiplicity']
        lower_by_mult[m][rec['lower_rank']] += 1
        upper_by_mult[m][rec['upper_rank']] += 1
        if rec['exact']:
            exact_by_mult[m][rec['lower_rank']] += 1
        delta_lower_refined[rec['lower_rank'] - rec['refined_rank']] += 1
        delta_upper_refined[rec['upper_rank'] - rec['refined_rank']] += 1
        total_candidates += rec['candidates_evaluated']
        total_duplicates += rec['duplicates_skipped']
        source_seen.update(rec['source_seen'])
        source_unique.update(rec['source_unique_support'])
        source_rank.update(rec['source_rank_increase'])
        for term in rec['term_supports']:
            term_radical_hist[term['radical_dimension']] += 1
            term_fourier_dim_hist[term['support_dimension']] += 1
            term_hull_rank_hist[term['linear_hull_rank']] += 1

    closed = len(exact_records)
    if closed == 250:
        decision = 'EXACT_MINIMAL_LINEAR_FACTORIZATION_RANKS_CLOSED_FOR_250_GROUPS'
    else:
        decision = f'MINIMAL_LINEAR_FACTORIZATION_BOUNDS_UNRESOLVED_{250 - closed}'

    compact = []
    for rec in records:
        compact.append({
            'group_id': rec['group_id'],
            'multiplicity': rec['multiplicity'],
            'physical_term_count': rec['physical_term_count'],
            'refined_rank': rec['refined_rank'],
            'lower_rank': rec['lower_rank'],
            'upper_rank': rec['upper_rank'],
            'exact': rec['exact'],
            'minimal_space_digest': rec['minimal_space_digest'],
            'upper_space_digest': rec['upper_space_digest'],
            'candidates_evaluated': rec['candidates_evaluated'],
            'duplicates_skipped': rec['duplicates_skipped'],
            'source_rank_increase': rec['source_rank_increase'],
            'certified_basis_witness_count': len(rec['candidate_unique_points']),
        })

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'synthetic_walsh_support_regression': regression,
        'support_groups': 250,
        'support_multiplicity_histogram': mult_hist,
        'physical_term_count': 680,
        'hash_rounds_per_term': HASH_ROUNDS_PER_TERM,
        'term_radical_dimension_histogram': dict(sorted(term_radical_hist.items())),
        'term_fourier_support_dimension_histogram': dict(sorted(term_fourier_dim_hist.items())),
        'term_fourier_linear_hull_rank_histogram': dict(sorted(term_hull_rank_hist.items())),
        'lower_rank_histogram': dict(sorted(lower_hist.items())),
        'upper_rank_histogram': dict(sorted(upper_hist.items())),
        'exact_minimal_rank_histogram': dict(sorted(exact_hist.items())),
        'exact_groups': closed,
        'unresolved_groups': 250 - closed,
        'lower_rank_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(lower_by_mult.items())
        },
        'upper_rank_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(upper_by_mult.items())
        },
        'exact_rank_by_multiplicity': {
            int(m): dict(sorted(h.items())) for m, h in sorted(exact_by_mult.items())
        },
        'lower_rank_minus_refined_rank_histogram': dict(sorted(delta_lower_refined.items())),
        'upper_rank_minus_refined_rank_histogram': dict(sorted(delta_upper_refined.items())),
        'candidate_totals': {
            'evaluated': total_candidates,
            'duplicates_skipped': total_duplicates,
            'source_seen': dict(sorted(source_seen.items())),
            'source_unique_support': dict(sorted(source_unique.items())),
            'source_rank_increase': dict(sorted(source_rank.items())),
        },
        'groups': compact,
        'decision': decision,
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_GROUP_OUTPUT_MINIMAL_LINEAR_FACTORIZATION')
    print('scope=exact Walsh-support upper bounds and certified nonzero unique-term Walsh-frequency lower bounds for minimal linear factorization of all 250 exact C916 e0 first-dyadic group residual functions')
    print('theorem=for f on GF2^149, the minimal linear factorization row space is the span of nonzero Walsh frequencies; equality of certified lower span and exact term-support upper span closes the exact minimal rank')
    print('important=unique-term support membership makes each lower-bound frequency an exact nonzero group Walsh coefficient; deterministic sampling affects discovery only, not validity')
    print('not_included=nonlinear compression, exact phase-complete separator width, exact all-250 joint image, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
