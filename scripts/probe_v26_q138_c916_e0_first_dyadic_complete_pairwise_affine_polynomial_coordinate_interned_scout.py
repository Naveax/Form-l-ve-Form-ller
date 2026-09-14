#!/usr/bin/env python3
import io, json, math, os, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_all_order_affine_scout as A
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_affine_polynomial_interned_scout as I

TARGET_DOMAIN_SUMS = tuple(sorted({int(x) for x in os.environ.get('C916_AFFINE_COORD_DOMAIN_SUMS', '134,154,251').split(',') if x.strip()}))
MAX_POLY_CALLS = int(os.environ.get('C916_AFFINE_COORD_MAX_CALLS', '2000000'))
MAX_POLY_STATES = int(os.environ.get('C916_AFFINE_COORD_MAX_POLY_STATES', '1800000'))
MAX_INTERNED_STATES = int(os.environ.get('C916_AFFINE_COORD_MAX_STATES', '2200000'))
EXPECTED_MEDIUM = {134: 21578474445840, 154: 42542498200320}
GLOBAL_NORMAL_RANK = 92
COORD_N = GLOBAL_NORMAL_RANK
COORD_MASK = (1 << COORD_N) - 1
EMPTY_ID = 0
BAD_ID = -1
SCOUT_ROWS = []


class CoordBudgetExceeded(RuntimeError):
    pass


def insert_coord(state, x):
    x = int(x)
    if not x:
        return state
    for row in state:
        p = (row & COORD_MASK).bit_length() - 1
        if p >= 0 and ((x >> p) & 1):
            x ^= row
    coeff = x & COORD_MASK
    if not coeff:
        return None if ((x >> COORD_N) & 1) else state
    p = coeff.bit_length() - 1
    out = [(row ^ x if ((row >> p) & 1) else row) for row in state]
    out.append(x)
    return tuple(sorted((row for row in out if row & COORD_MASK), reverse=True))


def canonical_coord(rows):
    state = ()
    for row in rows:
        state = insert_coord(state, row)
        if state is None:
            return None
    return state


class CoordinateInternedCounter(I.InternedAffinePolynomialCounter):
    """Same exact polynomial solver in coordinates of the rank-92 normal span.

    Every physical projection normal lives in one frozen 92-dimensional GF(2)
    rowspace. Mapping normals injectively to coordinates in a global RREF basis
    is a linear isomorphism, so affine consistency/intersection is unchanged,
    while each augmented row shrinks from 150 bits to 93 bits.
    """

    def __init__(self, variables, var_states, var_weights, pairq):
        # Deliberately bypass parent's 149-bit affine setup while retaining all
        # scalar pairwise machinery and the parent's compact polynomial methods.
        C.ExactCounter.__init__(self, variables, var_states, var_weights, pairq)
        self.state_to_id = {(): EMPTY_ID}
        self.id_to_state = [()]
        self.inter_cache = {}
        self.poly_memo = {}
        self.poly_calls = 0
        self.poly_stats = Counter()
        self.peak_poly_states = 0
        self.peak_interned_states = 1

        gids = tuple(int(g) for members in self.variables for g in members)
        assert len(gids) == len(set(gids)) == 90
        raw_anchors = A.rebuild_anchors(gids)
        normals = []
        for state in raw_anchors.values():
            normals.extend(int(row) & A.MASK for row in state)
        global_basis = A.canonical(normals)
        assert global_basis is not None and len(global_basis) == GLOBAL_NORMAL_RANK
        self.global_basis = tuple(int(x) for x in global_basis)

        def encode_normal(normal):
            x = int(normal)
            coord = 0
            for i, row in enumerate(self.global_basis):
                p = row.bit_length() - 1
                if (x >> p) & 1:
                    x ^= row
                    coord |= 1 << i
            assert x == 0, x
            return coord

        coord_anchors = {}
        for gid, state in raw_anchors.items():
            rows = []
            for row in state:
                phys = int(row) & A.MASK
                rhs = (int(row) >> A.PHYS_N) & 1
                rows.append(encode_normal(phys) | (rhs << COORD_N))
            ca = canonical_coord(rows)
            assert ca is not None
            coord_anchors[int(gid)] = ca
        anchor_id = {gid: self._intern(state) for gid, state in coord_anchors.items()}

        state_rows = []
        for members, states in zip(self.variables, self.var_states):
            zero = tuple(max(int(s[ci]) for s in states) for ci in range(len(members)))
            out = []
            for state in states:
                sid = EMPTY_ID
                for ci, gid in enumerate(members):
                    if int(state[ci]) != zero[ci]:
                        sid = self._inter_id(sid, anchor_id[int(gid)])
                        if sid == BAD_ID:
                            break
                out.append(sid)
            state_rows.append(tuple(out))
        self.state_aff_id = tuple(state_rows)

    def _intern(self, state):
        if state is None:
            return BAD_ID
        sid = self.state_to_id.get(state)
        if sid is not None:
            return sid
        sid = len(self.id_to_state)
        if sid >= MAX_INTERNED_STATES:
            raise CoordBudgetExceeded(f'interned affine state budget {MAX_INTERNED_STATES}')
        self.state_to_id[state] = sid
        self.id_to_state.append(state)
        self.peak_interned_states = max(self.peak_interned_states, len(self.id_to_state))
        return sid

    def _inter_id(self, a, b):
        if a == BAD_ID or b == BAD_ID:
            return BAD_ID
        if a == EMPTY_ID:
            return b
        if b == EMPTY_ID:
            return a
        key = (a, b) if a < b else (b, a)
        got = self.inter_cache.get(key)
        if got is not None:
            self.poly_stats['intersection_cache_hits'] += 1
            return got
        state = self.id_to_state[a]
        for row in self.id_to_state[b]:
            state = insert_coord(state, row)
            if state is None:
                break
        rid = self._intern(state)
        self.inter_cache[key] = rid
        self.poly_stats['intersection_cache_misses'] += 1
        return rid

    def _guard(self, poly=None):
        if self.poly_calls > MAX_POLY_CALLS:
            raise CoordBudgetExceeded(f'poly call budget {MAX_POLY_CALLS}')
        if len(self.id_to_state) >= MAX_INTERNED_STATES:
            raise CoordBudgetExceeded(f'interned affine state budget {MAX_INTERNED_STATES}')
        if poly is not None:
            n = len(poly)
            self.peak_poly_states = max(self.peak_poly_states, n)
            if n > MAX_POLY_STATES:
                raise CoordBudgetExceeded(f'poly state budget {MAX_POLY_STATES}')

    def count_profile(self, domains):
        baseline, baseline_calls, baseline_memo = C.ExactCounter.count_profile(self, domains)
        dsum = sum(int(d).bit_count() for d in domains)
        if dsum not in TARGET_DOMAIN_SUMS:
            return baseline, baseline_calls, baseline_memo

        self.inter_cache.clear()
        self.poly_memo.clear()
        self.poly_stats.clear()
        self.poly_calls = 0
        self.peak_poly_states = 0
        start_interned = len(self.id_to_state)
        status = 'completed'
        exact = None
        final_states = None
        try:
            poly = self._solve_poly(self.ALL, tuple(domains))
            exact = sum(int(w) for w in poly.values())
            final_states = len(poly)
        except (CoordBudgetExceeded, I.InternBudgetExceeded) as exc:
            status = 'budget_exceeded'
            self.poly_stats['budget_reason'] = str(exc)

        if exact is not None:
            assert 0 <= exact <= baseline
            if dsum in EXPECTED_MEDIUM:
                assert baseline == EXPECTED_MEDIUM[dsum]
                assert exact == baseline

        rank_hist = Counter()
        for state in self.id_to_state:
            rank_hist[len(state)] += 1
        row = {
            'domain_state_sum': dsum,
            'status': status,
            'pairwise_count': int(baseline),
            'all_order_affine_count': None if exact is None else int(exact),
            'gain_log2_bits': None if exact is None or exact == 0 else math.log2(baseline) - math.log2(exact),
            'global_normal_rank': GLOBAL_NORMAL_RANK,
            'coordinate_augmented_bits': COORD_N + 1,
            'poly_calls': self.poly_calls,
            'poly_memo_states': len(self.poly_memo),
            'final_affine_states': final_states,
            'peak_poly_states': self.peak_poly_states,
            'interned_states_before_profile': start_interned,
            'interned_states_after_profile': len(self.id_to_state),
            'new_interned_states': len(self.id_to_state) - start_interned,
            'intersection_cache_entries': len(self.inter_cache),
            'interned_rank_histogram': dict(sorted(rank_hist.items())),
            'stats': dict(self.poly_stats),
        }
        SCOUT_ROWS.append(row)
        print('affine_coord', json.dumps(row, sort_keys=True), flush=True)
        return baseline, baseline_calls, baseline_memo


def analyze():
    original = C.ExactCounter
    C.ExactCounter = CoordinateInternedCounter
    try:
        with redirect_stdout(io.StringIO()):
            baseline = C.analyze()
        assert int(baseline['exact_count']) == int(C.EXPECTED_EXACT_COUNT)
    finally:
        C.ExactCounter = original
    got = {int(r['domain_state_sum']) for r in SCOUT_ROWS}
    assert got == set(TARGET_DOMAIN_SUMS), (got, TARGET_DOMAIN_SUMS)
    out = {
        'position': 'C',
        'physical_shared_dimension': A.PHYS_N,
        'global_projection_normal_rank': GLOBAL_NORMAL_RANK,
        'coordinate_augmented_bits': COORD_N + 1,
        'pairwise_exact_baseline_count': int(C.EXPECTED_EXACT_COUNT),
        'target_domain_state_sums': list(TARGET_DOMAIN_SUMS),
        'max_poly_calls': MAX_POLY_CALLS,
        'max_poly_states': MAX_POLY_STATES,
        'max_interned_states': MAX_INTERNED_STATES,
        'scout_rows': SCOUT_ROWS,
        'completed_profiles': sum(r['status'] == 'completed' for r in SCOUT_ROWS),
        'budget_exceeded_profiles': sum(r['status'] != 'completed' for r in SCOUT_ROWS),
        'decision': 'C916_COMPLETE_PAIRWISE_ALL_ORDER_AFFINE_POLYNOMIAL_COORDINATE_INTERNED_SCOUT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_COMPLETE_PAIRWISE_AFFINE_POLYNOMIAL_COORDINATE_INTERNED_SCOUT')
    print('scope=exact affine-state polynomial contraction after linear isomorphism from the 149-bit physical normal span to its frozen rank-92 coordinates; canonical RREF states are hash-consed by integer ID and configured budget exhaustion is incomplete, never a count')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
