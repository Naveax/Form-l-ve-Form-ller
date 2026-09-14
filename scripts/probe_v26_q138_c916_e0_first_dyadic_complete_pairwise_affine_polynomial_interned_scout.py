#!/usr/bin/env python3
import io, json, math, os, sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_all_order_affine_scout as A

TARGET_DOMAIN_SUMS = tuple(sorted({int(x) for x in os.environ.get('C916_AFFINE_INTERN_DOMAIN_SUMS', '134,154,251').split(',') if x.strip()}))
MAX_POLY_CALLS = int(os.environ.get('C916_AFFINE_INTERN_MAX_CALLS', '2000000'))
MAX_POLY_STATES = int(os.environ.get('C916_AFFINE_INTERN_MAX_POLY_STATES', '1500000'))
MAX_INTERNED_STATES = int(os.environ.get('C916_AFFINE_INTERN_MAX_STATES', '1800000'))
EXPECTED_MEDIUM = {134: 21578474445840, 154: 42542498200320}
EMPTY_ID = 0
BAD_ID = -1
SCOUT_ROWS = []


class InternBudgetExceeded(RuntimeError):
    pass


class InternedAffinePolynomialCounter(C.ExactCounter):
    """Exact affine-polynomial counter with hash-consed RREF states.

    Polynomial keys and intersection-cache keys are compact integer state IDs.
    Each canonical affine RREF tuple is stored exactly once. This changes only
    representation; pairwise closure, component decomposition and affine
    intersection semantics are identical to the merged polynomial scout.
    """

    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
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
        anchors = A.rebuild_anchors(gids)
        anchor_id = {gid: self._intern(state) for gid, state in anchors.items()}

        rows = []
        for members, states in zip(self.variables, self.var_states):
            zero = tuple(max(int(s[ci]) for s in states) for ci in range(len(members)))
            out = []
            for state in states:
                aid = EMPTY_ID
                for ci, gid in enumerate(members):
                    if int(state[ci]) != zero[ci]:
                        aid = self._inter_id(aid, anchor_id[int(gid)])
                        if aid == BAD_ID:
                            break
                out.append(aid)
            rows.append(tuple(out))
        self.state_aff_id = tuple(rows)

    def _intern(self, state):
        if state is None:
            return BAD_ID
        sid = self.state_to_id.get(state)
        if sid is not None:
            return sid
        sid = len(self.id_to_state)
        if sid >= MAX_INTERNED_STATES:
            raise InternBudgetExceeded(f'interned affine state budget {MAX_INTERNED_STATES}')
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
        s = self.id_to_state[a]
        for row in self.id_to_state[b]:
            s = A.insert_rref(s, row)
            if s is None:
                break
        rid = self._intern(s)
        self.inter_cache[key] = rid
        self.poly_stats['intersection_cache_misses'] += 1
        return rid

    def _guard(self, poly=None):
        if self.poly_calls > MAX_POLY_CALLS:
            raise InternBudgetExceeded(f'poly call budget {MAX_POLY_CALLS}')
        if len(self.id_to_state) >= MAX_INTERNED_STATES:
            raise InternBudgetExceeded(f'interned affine state budget {MAX_INTERNED_STATES}')
        if poly is not None:
            n = len(poly)
            self.peak_poly_states = max(self.peak_poly_states, n)
            if n > MAX_POLY_STATES:
                raise InternBudgetExceeded(f'poly state budget {MAX_POLY_STATES}')

    def _add_into(self, dst, src):
        for sid, weight in src.items():
            if weight:
                dst[sid] += int(weight)
        self._guard(dst)

    def _shift_scale(self, poly, shift_id, factor):
        if not poly or factor == 0 or shift_id == BAD_ID:
            return {}
        if shift_id == EMPTY_ID:
            out = {sid: int(w) * int(factor) for sid, w in poly.items() if w}
            self._guard(out)
            return out
        out = defaultdict(int)
        for sid, weight in poly.items():
            rid = self._inter_id(sid, shift_id)
            if rid == BAD_ID:
                self.poly_stats['affine_empty_prunes'] += 1
            else:
                out[rid] += int(weight) * int(factor)
        ans = dict(out)
        self._guard(ans)
        return ans

    def _convolve(self, left, right):
        if not left or not right:
            return {}
        if len(left) > len(right):
            left, right = right, left
        if len(left) == 1 and EMPTY_ID in left:
            return self._shift_scale(right, EMPTY_ID, left[EMPTY_ID])
        if len(right) == 1 and EMPTY_ID in right:
            return self._shift_scale(left, EMPTY_ID, right[EMPTY_ID])
        self.poly_stats['component_convolutions'] += 1
        out = defaultdict(int)
        for aid, aw in left.items():
            for bid, bw in right.items():
                rid = self._inter_id(aid, bid)
                if rid == BAD_ID:
                    self.poly_stats['affine_empty_prunes'] += 1
                else:
                    out[rid] += int(aw) * int(bw)
            if len(out) > MAX_POLY_STATES:
                self._guard(out)
        ans = dict(out)
        self._guard(ans)
        return ans

    def _variable_poly(self, vi, domain):
        out = defaultdict(int)
        mask = int(domain)
        while mask:
            bit = mask & -mask
            si = bit.bit_length() - 1
            mask ^= bit
            sid = self.state_aff_id[vi][si]
            if sid != BAD_ID:
                out[sid] += int(self.var_weights[vi][si])
        ans = dict(out)
        self._guard(ans)
        return ans

    def _solve_poly(self, active, domains):
        self.poly_calls += 1
        self._guard()
        closed = super()._arc_closure(active, domains)
        if closed is None:
            self.poly_stats['pairwise_wipeouts'] += 1
            return {}
        domains = closed
        key = (active, tuple(domains[i] for i in range(self.N) if (active >> i) & 1))
        cached = self.poly_memo.get(key)
        if cached is not None:
            self.poly_stats['poly_memo_hits'] += 1
            return cached

        singleton = 0
        factor = 1
        shift = EMPTY_ID
        scan = active
        while scan:
            bit = scan & -scan
            vi = bit.bit_length() - 1
            scan ^= bit
            d = int(domains[vi])
            if d & (d - 1) == 0:
                si = d.bit_length() - 1
                singleton |= bit
                factor *= int(self.var_weights[vi][si])
                shift = self._inter_id(shift, self.state_aff_id[vi][si])
                if shift == BAD_ID:
                    self.poly_stats['singleton_affine_prunes'] += 1
                    self.poly_memo[key] = {}
                    return {}
        if singleton:
            rest = active ^ singleton
            ans = ({shift: factor} if rest == 0 else self._shift_scale(self._solve_poly(rest, domains), shift, factor))
            self.poly_memo[key] = ans
            self._guard(ans)
            return ans

        remain = active
        pieces = []
        while remain:
            seed = remain & -remain
            vi = seed.bit_length() - 1
            if self._relevant_neighbors(vi, active, domains) == 0:
                pieces.append(self._variable_poly(vi, domains[vi]))
                remain ^= seed
                continue
            comp = 0
            frontier = seed
            while frontier:
                x = frontier & -frontier
                frontier ^= x
                k = x.bit_length() - 1
                if comp & x:
                    continue
                comp |= x
                frontier |= self._relevant_neighbors(k, active, domains) & ~comp
            pieces.append(('component', comp))
            remain &= ~comp

        split = len(pieces) > 1 or (pieces and isinstance(pieces[0], dict))
        if split:
            polys = []
            for piece in pieces:
                polys.append(piece if isinstance(piece, dict) else self._solve_poly(piece[1], domains))
            polys.sort(key=len)
            ans = {EMPTY_ID: 1}
            for poly in polys:
                ans = self._convolve(ans, poly)
                if not ans:
                    break
            self.poly_memo[key] = ans
            self._guard(ans)
            return ans

        best = None
        scan = active
        while scan:
            bit = scan & -scan
            vi = bit.bit_length() - 1
            scan ^= bit
            score = (int(domains[vi]).bit_count(), -self._relevant_neighbors(vi, active, domains).bit_count(), vi)
            if best is None or score < best[0]:
                best = (score, vi)
        vi = best[1]
        out = defaultdict(int)
        mask = int(domains[vi])
        while mask:
            bit = mask & -mask
            mask ^= bit
            nd = list(domains)
            nd[vi] = bit
            self._add_into(out, self._solve_poly(active, tuple(nd)))
        ans = dict(out)
        self.poly_memo[key] = ans
        self._guard(ans)
        return ans

    def count_profile(self, domains):
        baseline, baseline_calls, baseline_memo = super().count_profile(domains)
        dsum = sum(int(d).bit_count() for d in domains)
        if dsum not in TARGET_DOMAIN_SUMS:
            return baseline, baseline_calls, baseline_memo

        # Keep anchor/state IDs, but discard profile-specific intersections and
        # polynomial memo. Hash-consed states discovered by a previous target
        # profile are safe to reuse because IDs name canonical RREF tuples.
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
        except InternBudgetExceeded as exc:
            status = 'budget_exceeded'
            self.poly_stats['budget_reason'] = str(exc)

        if exact is not None:
            assert 0 <= exact <= baseline
            if dsum in EXPECTED_MEDIUM:
                assert baseline == EXPECTED_MEDIUM[dsum]
                assert exact == baseline

        row = {
            'domain_state_sum': dsum,
            'status': status,
            'pairwise_count': int(baseline),
            'all_order_affine_count': None if exact is None else int(exact),
            'gain_log2_bits': None if exact is None or exact == 0 else math.log2(baseline) - math.log2(exact),
            'poly_calls': self.poly_calls,
            'poly_memo_states': len(self.poly_memo),
            'final_affine_states': final_states,
            'peak_poly_states': self.peak_poly_states,
            'interned_states_before_profile': start_interned,
            'interned_states_after_profile': len(self.id_to_state),
            'new_interned_states': len(self.id_to_state) - start_interned,
            'intersection_cache_entries': len(self.inter_cache),
            'stats': dict(self.poly_stats),
        }
        SCOUT_ROWS.append(row)
        print('affine_intern', json.dumps(row, sort_keys=True), flush=True)
        return baseline, baseline_calls, baseline_memo


def analyze():
    original = C.ExactCounter
    C.ExactCounter = InternedAffinePolynomialCounter
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
        'pairwise_exact_baseline_count': int(C.EXPECTED_EXACT_COUNT),
        'target_domain_state_sums': list(TARGET_DOMAIN_SUMS),
        'max_poly_calls': MAX_POLY_CALLS,
        'max_poly_states': MAX_POLY_STATES,
        'max_interned_states': MAX_INTERNED_STATES,
        'scout_rows': SCOUT_ROWS,
        'completed_profiles': sum(r['status'] == 'completed' for r in SCOUT_ROWS),
        'budget_exceeded_profiles': sum(r['status'] != 'completed' for r in SCOUT_ROWS),
        'decision': 'C916_COMPLETE_PAIRWISE_ALL_ORDER_AFFINE_POLYNOMIAL_INTERNED_SCOUT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_COMPLETE_PAIRWISE_AFFINE_POLYNOMIAL_INTERNED_SCOUT')
    print('scope=exact affine-state polynomial contraction with hash-consed canonical RREF states and integer-ID intersection cache; configured budget exhaustion is incomplete, never a count')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
