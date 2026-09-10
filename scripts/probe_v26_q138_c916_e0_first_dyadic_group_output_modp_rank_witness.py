#!/usr/bin/env python3
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_group_output_pair_dependency as D

P = D.P
POS = D.POS
PHYS_N = D.PHYS_N
PRIMES = (65521, 1000003)
TARGET_RANK = 250
PROJECTION_BASIS_ROUNDS = 8
GAUSS_BASIS_ROUNDS = 4
PROJECTION_HASH_ROUNDS = 16
GAUSS_HASH_ROUNDS = 8

assert POS == 'C'
assert PHYS_N == 149


def is_prime(n):
    n = int(n)
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


class IncrementalModRank:
    def __init__(self, prime, width):
        self.prime = int(prime)
        self.width = int(width)
        self.pivots = {}
        self.selected_candidate_indices = []
        self.selected_raw_rows = []

    @property
    def rank(self):
        return len(self.pivots)

    def add(self, row, candidate_index):
        p = self.prime
        y = [int(v) % p for v in row]
        for col in sorted(self.pivots):
            factor = y[col]
            if not factor:
                continue
            pivot_row = self.pivots[col]
            for j in range(col, self.width):
                y[j] = (y[j] - factor * pivot_row[j]) % p

        pivot = next((j for j, v in enumerate(y) if v), None)
        if pivot is None:
            return False

        inv = pow(y[pivot], -1, p)
        for j in range(pivot, self.width):
            y[j] = (y[j] * inv) % p
        assert y[pivot] == 1
        self.pivots[pivot] = y
        self.selected_candidate_indices.append(int(candidate_index))
        self.selected_raw_rows.append(tuple(int(v) % p for v in row))
        assert len(self.selected_candidate_indices) == self.rank
        return True


def determinant_mod(matrix, prime):
    p = int(prime)
    a = [[int(v) % p for v in row] for row in matrix]
    n = len(a)
    assert n and all(len(row) == n for row in a)
    det = 1
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = (-det) % p
        pv = a[col][col]
        det = (det * pv) % p
        inv = pow(pv, -1, p)
        for j in range(col, n):
            a[col][j] = (a[col][j] * inv) % p
        for r in range(col + 1, n):
            factor = a[r][col]
            if not factor:
                continue
            for j in range(col, n):
                a[r][j] = (a[r][j] - factor * a[col][j]) % p
    return det % p


def synthetic_rank_regression():
    tested = 0
    rows = (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (1, 1, 0, 0),
        (0, 0, 2, 0),
        (3, 5, 7, 11),
        (2, 2, 0, 0),
    )
    for prime in PRIMES:
        assert is_prime(prime)
        tracker = IncrementalModRank(prime, 4)
        expected = (1, 2, 2, 3, 4, 4)
        for i, (row, rank) in enumerate(zip(rows, expected)):
            tracker.add(row, i)
            assert tracker.rank == rank
            tested += 1
        assert sorted(tracker.pivots) == [0, 1, 2, 3]
        assert determinant_mod(tracker.selected_raw_rows, prime) != 0
        tested += 1
    assert tested == 14
    return tested


def affine_hash_point(anchor, tag):
    basis = tuple(int(x) for x in anchor['physical_support_basis'])
    d = len(basis)
    assert d > 0
    raw = hashlib.shake_256(tag.encode('utf-8')).digest((d + 7) // 8)
    coeff = int.from_bytes(raw, 'little') & ((1 << d) - 1)
    if coeff == 0:
        coeff = 1
    return int(anchor['physical_support_x0']) ^ P.xor_combine(coeff, basis)


def synthetic_affine_point_regression():
    anchors = (
        P.make_synthetic_anchor((), 5, 'quadratic'),
        P.make_synthetic_anchor(((1, 0),), 5, 'linear'),
        P.make_synthetic_anchor(((2, 1),), 5, 'one'),
        P.make_synthetic_anchor(((1, 1), (4, 0)), 5, 'quadratic'),
    )
    tested = 0
    for i, anchor in enumerate(anchors):
        point = affine_hash_point(anchor, f'synthetic:{i}')
        assert 0 <= point < (1 << 5)
        assert P.eval_anchor_sign(anchor, point) is not None
        tested += 1
    assert tested == 4
    return tested


def build_physical_groups():
    e0, _e1, _half = P.C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for k in range(4):
        for zs, cls in e0[k]:
            can = P.C.P.U.H.support_for(POS, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert raw == 577 and len(ordered) == 250

    groups = []
    terms = []
    next_term_id = 0
    for gid, (can, sectors) in enumerate(ordered):
        group, next_term_id = D.build_group_terms(
            gid, can, sectors, next_term_id
        )
        groups.append(group)
        terms.extend(group['terms'])

    assert len(groups) == 250
    assert next_term_id == len(terms) == 680
    assert sum(t['kind'] == 'gauss_sector' for t in terms) == 577
    assert sum(t['kind'] == 'singleton_projection_baseline' for t in terms) == 103
    mult_hist = Counter(g['multiplicity'] for g in groups)
    assert dict(sorted(mult_hist.items())) == {1: 103, 2: 57, 4: 90}
    return groups, tuple(terms), dict(sorted(mult_hist.items()))


def evaluate_all_groups(terms, physical):
    row = [0] * 250
    for term in terms:
        q = P.eval_anchor_sign(term['anchor'], physical)
        if q is None:
            continue
        value = int(term['coefficient'])
        if q:
            value = -value
        row[int(term['group_id'])] += value
    return tuple(row)


def candidate_stages(groups, terms):
    yield (
        'projection_origins',
        (
            (
                'projection_origin',
                f'projection_origin:{g["group_id"]}',
                int(g['projection_anchor']['physical_support_x0']),
            )
            for g in groups
        ),
    )

    gauss_terms = tuple(t for t in terms if t['kind'] == 'gauss_sector')
    yield (
        'gauss_support_origins',
        (
            (
                'gauss_support_origin',
                f'gauss_support_origin:{t["group_id"]}:{t["term_id"]}',
                int(t['anchor']['physical_support_x0']),
            )
            for t in gauss_terms
        ),
    )

    def projection_basis_candidates():
        for basis_index in range(PROJECTION_BASIS_ROUNDS):
            for g in groups:
                basis = g['projection_anchor']['physical_support_basis']
                if basis_index >= len(basis):
                    continue
                yield (
                    'projection_basis_single',
                    f'projection_basis_single:{basis_index}:{g["group_id"]}',
                    int(g['projection_anchor']['physical_support_x0'])
                    ^ int(basis[basis_index]),
                )

    yield ('projection_basis_single', projection_basis_candidates())

    def gauss_basis_candidates():
        for basis_index in range(GAUSS_BASIS_ROUNDS):
            for t in gauss_terms:
                basis = t['anchor']['physical_support_basis']
                if basis_index >= len(basis):
                    continue
                yield (
                    'gauss_basis_single',
                    f'gauss_basis_single:{basis_index}:{t["group_id"]}:{t["term_id"]}',
                    int(t['anchor']['physical_support_x0'])
                    ^ int(basis[basis_index]),
                )

    yield ('gauss_basis_single', gauss_basis_candidates())

    def projection_hash_candidates():
        for round_index in range(PROJECTION_HASH_ROUNDS):
            for g in groups:
                yield (
                    'projection_hash',
                    f'projection_hash:{round_index}:{g["group_id"]}',
                    affine_hash_point(
                        g['projection_anchor'],
                        f'projection:{round_index}:{g["group_id"]}',
                    ),
                )

    yield ('projection_hash', projection_hash_candidates())

    def gauss_hash_candidates():
        for round_index in range(GAUSS_HASH_ROUNDS):
            for t in gauss_terms:
                yield (
                    'gauss_hash',
                    f'gauss_hash:{round_index}:{t["group_id"]}:{t["term_id"]}',
                    affine_hash_point(
                        t['anchor'],
                        f'gauss:{round_index}:{t["group_id"]}:{t["term_id"]}',
                    ),
                )

    yield ('gauss_hash', gauss_hash_candidates())


def witness_digest(records, rows, prime):
    h = hashlib.sha256()
    h.update(f'prime={prime}\n'.encode('ascii'))
    for rec, row in zip(records, rows):
        h.update(f'{rec["candidate_index"]}:{rec["source"]}:{rec["point_hex"]}\n'.encode('ascii'))
        for v in row:
            h.update(int(v).to_bytes(4, 'little', signed=False))
    return h.hexdigest()


def analyze():
    rank_regression = synthetic_rank_regression()
    affine_regression = synthetic_affine_point_regression()
    groups, terms, mult_hist = build_physical_groups()

    trackers = {
        prime: IncrementalModRank(prime, TARGET_RANK)
        for prime in PRIMES
    }
    seen = set()
    candidate_records = []
    duplicate_candidates = 0
    zero_rows = 0
    rank_checkpoints = []
    winning_prime = None

    for stage_name, candidates in candidate_stages(groups, terms):
        stage_total = 0
        stage_unique = 0
        stage_independent = Counter()
        for source_kind, source, physical in candidates:
            stage_total += 1
            physical = int(physical)
            assert 0 <= physical < (1 << PHYS_N)
            if physical in seen:
                duplicate_candidates += 1
                continue
            seen.add(physical)
            stage_unique += 1

            row = evaluate_all_groups(terms, physical)
            if not any(row):
                zero_rows += 1

            candidate_index = len(candidate_records)
            record = {
                'candidate_index': candidate_index,
                'stage': stage_name,
                'source_kind': source_kind,
                'source': source,
                'point_hex': format(physical, '038x'),
                'row_nonzero_entries': sum(v != 0 for v in row),
            }
            candidate_records.append(record)

            for prime, tracker in trackers.items():
                if tracker.rank == TARGET_RANK:
                    continue
                if tracker.add(row, candidate_index):
                    stage_independent[prime] += 1

            winners = sorted(
                prime for prime, tracker in trackers.items()
                if tracker.rank == TARGET_RANK
            )
            if winners:
                winning_prime = winners[0]
                break

        rank_checkpoints.append({
            'stage': stage_name,
            'stage_candidates_seen': stage_total,
            'stage_unique_candidates_evaluated': stage_unique,
            'stage_rank_increases_by_prime': {
                str(p): stage_independent[p] for p in PRIMES
            },
            'rank_by_prime': {
                str(p): trackers[p].rank for p in PRIMES
            },
            'cumulative_unique_candidates_evaluated': len(candidate_records),
        })
        if winning_prime is not None:
            break

    final_rank_by_prime = {
        str(p): trackers[p].rank for p in PRIMES
    }

    if winning_prime is None:
        decision = 'INCONCLUSIVE_MODP_PHYSICAL_EVALUATION_SAMPLE_WITNESS'
        witness = None
    else:
        tracker = trackers[winning_prime]
        assert tracker.rank == TARGET_RANK
        assert len(tracker.selected_candidate_indices) == TARGET_RANK
        assert sorted(tracker.pivots) == list(range(TARGET_RANK))
        selected_records = [
            candidate_records[i]
            for i in tracker.selected_candidate_indices
        ]
        det = determinant_mod(tracker.selected_raw_rows, winning_prime)
        assert det != 0
        source_hist = Counter(rec['source_kind'] for rec in selected_records)
        witness = {
            'prime': winning_prime,
            'rank': TARGET_RANK,
            'determinant_mod_prime': det,
            'selected_rows': TARGET_RANK,
            'selected_source_histogram': dict(sorted(source_hist.items())),
            'witness_sha256': witness_digest(
                selected_records,
                tracker.selected_raw_rows,
                winning_prime,
            ),
            'selected_candidate_indices': tracker.selected_candidate_indices,
            'selected_points_hex': [
                rec['point_hex'] for rec in selected_records
            ],
            'selected_sources': [
                rec['source'] for rec in selected_records
            ],
        }
        decision = 'MODP_FULL_RANK250_PHYSICAL_EVALUATION_WITNESS'

    out = {
        'position': POS,
        'physical_shared_dimension': PHYS_N,
        'primes': list(PRIMES),
        'synthetic_rank_regression_cases': rank_regression,
        'synthetic_affine_point_regression_cases': affine_regression,
        'raw_e0_sectors': 577,
        'support_groups': 250,
        'support_multiplicity_histogram': mult_hist,
        'physical_term_count': len(terms),
        'gauss_sector_term_count': 577,
        'singleton_baseline_term_count': 103,
        'candidate_generation': {
            'projection_basis_rounds': PROJECTION_BASIS_ROUNDS,
            'gauss_basis_rounds': GAUSS_BASIS_ROUNDS,
            'projection_hash_rounds': PROJECTION_HASH_ROUNDS,
            'gauss_hash_rounds': GAUSS_HASH_ROUNDS,
        },
        'unique_candidates_evaluated': len(candidate_records),
        'duplicate_candidates_skipped': duplicate_candidates,
        'zero_evaluation_rows': zero_rows,
        'rank_checkpoints': rank_checkpoints,
        'final_rank_by_prime': final_rank_by_prime,
        'witness': witness,
        'decision': decision,
    }

    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_GROUP_OUTPUT_MODP_RANK_WITNESS')
    print('scope=deterministic physical evaluation witness for linear independence of the 250 exact integer-valued C916 e0 first-dyadic group residual functions')
    print('proof=rank250 modulo any reported odd prime gives a 250x250 evaluation minor with determinant nonzero modulo that prime; therefore the integer determinant is nonzero and the 250 functions are linearly independent over Q')
    print('sampling=deterministic projection/support origins, basis toggles, and SHAKE256-derived affine points; failure to reach rank250 is reported only as inconclusive')
    print('important=this is a linear-independence theorem only when decision=MODP_FULL_RANK250_PHYSICAL_EVALUATION_WITNESS; it is not a nonlinear joint-image or separator-width theorem')
    print('not_included=complete all-250 joint image, support/e1 carry, half cross, complete C2, W_repr, arithmetic-work, alpha, ranking/search, full-round')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
