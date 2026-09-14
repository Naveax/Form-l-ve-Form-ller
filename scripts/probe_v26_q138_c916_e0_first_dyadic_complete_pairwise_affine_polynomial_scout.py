#!/usr/bin/env python3
import io, json, math, os, sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_all_order_affine_scout as A

TARGET_DOMAIN_SUMS = tuple(sorted({int(x) for x in os.environ.get('C916_AFFINE_POLY_DOMAIN_SUMS', '134,154,251').split(',') if x.strip()}))
MAX_POLY_CALLS = int(os.environ.get('C916_AFFINE_POLY_MAX_CALLS', '2000000'))
MAX_POLY_STATES = int(os.environ.get('C916_AFFINE_POLY_MAX_STATES', '750000'))
EXPECTED_MEDIUM = {
    134: 21578474445840,
    154: 42542498200320,
}


class PolyBudgetExceeded(RuntimeError):
    pass


SCOUT_ROWS = []


class AffinePolynomialCounter(C.ExactCounter):
    """Return exact weight polynomials indexed by canonical affine RREF state.

    Pure pairwise components remain independently solvable. Instead of scalar
    multiplication, component results are convolved through exact affine-anchor
    intersection. Empty intersections are discarded. This preserves the fast
    pairwise decomposition while enforcing the global all-order affine condition.
    """

    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        gids = tuple(int(g) for members in self.variables for g in members)
        assert len(gids) == len(set(gids)) == 90
        anchors = A.rebuild_anchors(gids)

        state_aff = []
        for members, states in zip(self.variables, self.var_states):
            zero = tuple(max(int(s[ci]) for s in states) for ci in range(len(members)))
            row = []
            for state in states:
                aff = ()
                for ci, gid in enumerate(members):
                    if int(state[ci]) != zero[ci]:
                        aff = A.canonical(aff + anchors[int(gid)])
                        if aff is None:
                            break
                row.append(aff)
            state_aff.append(tuple(row))
        self.state_aff = tuple(state_aff)
        self.aff_cache = {}
        self.poly_memo = {}
        self.poly_calls = 0
        self.poly_stats = Counter()
        self.peak_poly_states = 0

    def _guard(self, poly=None):
        if self.poly_calls > MAX_POLY_CALLS:
            raise PolyBudgetExceeded(f'poly call budget {MAX_POLY_CALLS}')
        if poly is not None:
            n = len(poly)
            self.peak_poly_states = max(self.peak_poly_states, n)
            if n > MAX_POLY_STATES:
                raise PolyBudgetExceeded(f'poly state budget {MAX_POLY_STATES}')

    def _inter(self, a, b):
        return A.inter(a, b, self.aff_cache, self.poly_stats)

    def _add_into(self, dst, src):
        for aff, w in src.items():
            if w:
                dst[aff] += int(w)
        self._guard(dst)

    def _shift_scale(self, poly, aff, factor):
        if not poly or factor == 0 or aff is None:
            return {}
        if not aff:
            out = {a: int(w) * int(factor) for a, w in poly.items() if w}
            self._guard(out)
            return out
        out = defaultdict(int)
        for a, w in poly.items():
            na = self._inter(a, aff)
            if na is None:
                self.poly_stats['affine_empty_prunes'] += 1
            else:
                out[na] += int(w) * int(factor)
        ans = dict(out)
        self._guard(ans)
        return ans

    def _convolve(self, left, right):
        if not left or not right:
            return {}
        if len(left) > len(right):
            left, right = right, left
        if len(left) == 1 and () in left:
            return self._shift_scale(right, (), left[()])
        if len(right) == 1 and () in right:
            return self._shift_scale(left, (), right[()])
        self.poly_stats['component_convolutions'] += 1
        out = defaultdict(int)
        for a, aw in left.items():
            for b, bw in right.items():
                na = self._inter(a, b)
                if na is None:
                    self.poly_stats['affine_empty_prunes'] += 1
                else:
                    out[na] += int(aw) * int(bw)
            if len(out) > MAX_POLY_STATES:
                self._guard(out)
        ans = dict(out)
        self._guard(ans)
        return ans

    def _variable_poly(self, vi, domain):
        out = defaultdict(int)
        mask = int(domain)
        while mask:
            lsb = mask & -mask
            si = lsb.bit_length() - 1
            mask ^= lsb
            aff = self.state_aff[vi][si]
            if aff is not None:
                out[aff] += int(self.var_weights[vi][si])
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

        # Pairwise closure has already propagated fixed states to every active
        # neighbour, so singleton variables can be removed and represented as a
        # single affine shift/weight factor.
        singleton = 0
        factor = 1
        aff = ()
        scan = active
        while scan:
            lsb = scan & -scan
            vi = lsb.bit_length() - 1
            scan ^= lsb
            d = int(domains[vi])
            if d & (d - 1) == 0:
                si = d.bit_length() - 1
                singleton |= lsb
                factor *= int(self.var_weights[vi][si])
                aff = self._inter(aff, self.state_aff[vi][si])
                if aff is None:
                    self.poly_stats['singleton_affine_prunes'] += 1
                    self.poly_memo[key] = {}
                    return {}
        if singleton:
            rest = active ^ singleton
            if not rest:
                ans = {} if aff is None else {aff: factor}
            else:
                ans = self._shift_scale(self._solve_poly(rest, domains), aff, factor)
            self.poly_memo[key] = ans
            self._guard(ans)
            return ans

        # Preserve the original pairwise component decomposition. Isolated
        # variables are tiny affine polynomials; connected components recurse
        # independently and are joined only by exact affine convolution.
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
                if isinstance(piece, dict):
                    polys.append(piece)
                else:
                    polys.append(self._solve_poly(piece[1], domains))
            polys.sort(key=len)
            ans = {(): 1}
            for poly in polys:
                ans = self._convolve(ans, poly)
                if not ans:
                    break
            self.poly_memo[key] = ans
            self._guard(ans)
            return ans

        # One connected pairwise component remains. Branch exactly as the scalar
        # counter does; each child becomes singleton-normalized on entry.
        best = None
        scan = active
        while scan:
            x = scan & -scan
            vi = x.bit_length() - 1
            scan ^= x
            score = (int(domains[vi]).bit_count(), -self._relevant_neighbors(vi, active, domains).bit_count(), vi)
            if best is None or score < best[0]:
                best = (score, vi)
        vi = best[1]
        out = defaultdict(int)
        mask = int(domains[vi])
        while mask:
            x = mask & -mask
            mask ^= x
            nd = list(domains)
            nd[vi] = x
            self._add_into(out, self._solve_poly(active, tuple(nd)))
        ans = dict(out)
        self.poly_memo[key] = ans
        self._guard(ans)
        return ans

    def count_profile(self, domains):
        baseline_value, baseline_calls, baseline_memo = super().count_profile(domains)
        dsum = sum(int(d).bit_count() for d in domains)
        if dsum not in TARGET_DOMAIN_SUMS:
            return baseline_value, baseline_calls, baseline_memo

        self.aff_cache.clear()
        self.poly_memo.clear()
        self.poly_stats.clear()
        self.poly_calls = 0
        self.peak_poly_states = 0
        status = 'completed'
        exact = None
        final_states = None
        try:
            poly = self._solve_poly(self.ALL, tuple(domains))
            exact = sum(int(w) for w in poly.values())
            final_states = len(poly)
        except PolyBudgetExceeded as exc:
            status = 'budget_exceeded'
            self.poly_stats['budget_reason'] = str(exc)

        if exact is not None:
            assert 0 <= exact <= baseline_value
            if dsum in EXPECTED_MEDIUM:
                assert baseline_value == EXPECTED_MEDIUM[dsum]
                assert exact == baseline_value

        row = {
            'domain_state_sum': dsum,
            'status': status,
            'pairwise_count': int(baseline_value),
            'all_order_affine_count': None if exact is None else int(exact),
            'gain_log2_bits': None if exact is None or exact == 0 else math.log2(baseline_value) - math.log2(exact),
            'poly_calls': self.poly_calls,
            'poly_memo_states': len(self.poly_memo),
            'final_affine_states': final_states,
            'peak_poly_states': self.peak_poly_states,
            'intersection_cache_entries': len(self.aff_cache),
            'stats': dict(self.poly_stats),
        }
        SCOUT_ROWS.append(row)
        print('affine_poly', json.dumps(row, sort_keys=True), flush=True)
        return baseline_value, baseline_calls, baseline_memo


def analyze():
    original = C.ExactCounter
    C.ExactCounter = AffinePolynomialCounter
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
        'scout_rows': SCOUT_ROWS,
        'completed_profiles': sum(r['status'] == 'completed' for r in SCOUT_ROWS),
        'budget_exceeded_profiles': sum(r['status'] != 'completed' for r in SCOUT_ROWS),
        'decision': 'C916_COMPLETE_PAIRWISE_ALL_ORDER_AFFINE_POLYNOMIAL_SCOUT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_COMPLETE_PAIRWISE_AFFINE_POLYNOMIAL_SCOUT')
    print('scope=exact affine-state polynomial contraction over complete pairwise components; disconnected pairwise factors are convolved by canonical affine RREF intersection, and any configured budget exhaustion is reported as incomplete rather than as a count')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
