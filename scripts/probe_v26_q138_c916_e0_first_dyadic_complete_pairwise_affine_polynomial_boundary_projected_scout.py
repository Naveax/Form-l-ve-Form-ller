#!/usr/bin/env python3
import io, json, math, os, sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_all_order_affine_scout as A
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_affine_polynomial_scout as P

PAIRWISE_COUNTER = C.ExactCounter
TARGET_DOMAIN_SUMS = tuple(sorted({int(x) for x in os.environ.get('C916_AFFINE_BOUNDARY_DOMAIN_SUMS', '134,154,251').split(',') if x.strip()}))
EXPECTED_MEDIUM = {134: 21578474445840, 154: 42542498200320}
SCOUT_ROWS = []


def normal_insert(state, x):
    x = int(x)
    if not x:
        return state
    for row in state:
        p = row.bit_length() - 1
        if (x >> p) & 1:
            x ^= row
    if not x:
        return state
    p = x.bit_length() - 1
    out = [(row ^ x if ((row >> p) & 1) else row) for row in state]
    out.append(x)
    return tuple(sorted(out, reverse=True))


def normal_canonical(rows):
    state = ()
    for row in rows:
        state = normal_insert(state, int(row))
    return state


def reduce_normal(x, basis):
    x = int(x)
    for row in basis:
        p = row.bit_length() - 1
        if (x >> p) & 1:
            x ^= row
    return x


class BoundaryProjectedCounter(P.AffinePolynomialCounter):
    """Exact component polynomial with future-boundary affine projection."""

    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        var_normals = []
        all_normals = []
        for states in self.state_aff:
            rows = []
            for aff in states:
                if aff is None:
                    continue
                for aug in aff:
                    normal = int(aug) & A.MASK
                    if normal:
                        rows.append(normal)
                        all_normals.append(normal)
            var_normals.append(normal_canonical(rows))
        self.var_normal_span = tuple(var_normals)
        self.global_normal_span = normal_canonical(all_normals)
        assert len(self.global_normal_span) == A.EXPECTED_NORMAL_RANK == 92
        self.boundary_cache = {}
        self.project_cache = {}
        self.boundary_stats = Counter()
        self.boundary_rank_hist = Counter()

    def _boundary_basis(self, active):
        active = int(active)
        got = self.boundary_cache.get(active)
        if got is not None:
            self.boundary_stats['boundary_cache_hits'] += 1
            return got
        rows = []
        scan = self.ALL ^ active
        while scan:
            bit = scan & -scan
            vi = bit.bit_length() - 1
            scan ^= bit
            rows.extend(self.var_normal_span[vi])
        basis = normal_canonical(rows)
        self.boundary_cache[active] = basis
        self.boundary_rank_hist[len(basis)] += 1
        self.boundary_stats['boundary_cache_misses'] += 1
        return basis

    def _project_state(self, active, state):
        if state is None:
            return None
        if not state:
            return ()
        key = (int(active), state)
        got = self.project_cache.get(key)
        if got is not None:
            self.boundary_stats['projection_cache_hits'] += 1
            return got
        boundary = self._boundary_basis(active)
        if not boundary:
            out = ()
        elif len(boundary) == len(self.global_normal_span):
            out = state
        else:
            quotient_basis = {}
            kernel_combos = []
            for i, aug in enumerate(state):
                residual = reduce_normal(int(aug) & A.MASK, boundary)
                combo = 1 << i
                while residual:
                    pivot = residual.bit_length() - 1
                    prior = quotient_basis.get(pivot)
                    if prior is None:
                        quotient_basis[pivot] = (residual, combo)
                        break
                    residual ^= prior[0]
                    combo ^= prior[1]
                if residual == 0:
                    kernel_combos.append(combo)
            out = ()
            for combo in kernel_combos:
                aug = 0
                mask = combo
                while mask:
                    bit = mask & -mask
                    j = bit.bit_length() - 1
                    mask ^= bit
                    aug ^= int(state[j])
                assert reduce_normal(aug & A.MASK, boundary) == 0
                nxt = A.insert_rref(out, aug)
                assert nxt is not None
                out = nxt
        self.project_cache[key] = out
        self.boundary_stats['projection_cache_misses'] += 1
        self.boundary_stats['projected_rank_before_sum'] += len(state)
        self.boundary_stats['projected_rank_after_sum'] += len(out)
        return out

    def _project_poly(self, active, poly):
        if not poly:
            return {}
        out = defaultdict(int)
        for state, weight in poly.items():
            out[self._project_state(active, state)] += int(weight)
        ans = dict(out)
        self.boundary_stats['poly_states_before_projection'] += len(poly)
        self.boundary_stats['poly_states_after_projection'] += len(ans)
        self.boundary_stats['poly_states_merged'] += len(poly) - len(ans)
        self._guard(ans)
        return ans

    def _shift_scale_boundary(self, poly, aff, factor, target_active):
        if not poly or factor == 0 or aff is None:
            return {}
        out = defaultdict(int)
        for state, weight in poly.items():
            merged = self._inter(state, aff)
            if merged is None:
                self.poly_stats['affine_empty_prunes'] += 1
                continue
            out[self._project_state(target_active, merged)] += int(weight) * int(factor)
        ans = dict(out)
        self._guard(ans)
        return ans

    def _convolve_boundary(self, left, right, target_active):
        if not left or not right:
            return {}
        if len(left) > len(right):
            left, right = right, left
        self.poly_stats['component_convolutions'] += 1
        out = defaultdict(int)
        for a, aw in left.items():
            for b, bw in right.items():
                merged = self._inter(a, b)
                if merged is None:
                    self.poly_stats['affine_empty_prunes'] += 1
                    continue
                out[self._project_state(target_active, merged)] += int(aw) * int(bw)
            if len(out) > P.MAX_POLY_STATES:
                self._guard(out)
        ans = dict(out)
        self._guard(ans)
        return ans

    def _variable_boundary_poly(self, vi, domain):
        return self._project_poly(1 << vi, self._variable_poly(vi, domain))

    def _solve_poly(self, active, domains):
        self.poly_calls += 1
        self._guard()
        closed = PAIRWISE_COUNTER._arc_closure(self, active, domains)
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
        aff = ()
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
                aff = self._inter(aff, self.state_aff[vi][si])
                if aff is None:
                    self.poly_stats['singleton_affine_prunes'] += 1
                    self.poly_memo[key] = {}
                    return {}
        if singleton:
            rest = active ^ singleton
            if not rest:
                ans = self._project_poly(active, {aff: factor})
            else:
                ans = self._shift_scale_boundary(self._solve_poly(rest, domains), aff, factor, active)
            self.poly_memo[key] = ans
            return ans

        remain = active
        pieces = []
        while remain:
            seed = remain & -remain
            vi = seed.bit_length() - 1
            if self._relevant_neighbors(vi, active, domains) == 0:
                pieces.append((seed, self._variable_boundary_poly(vi, domains[vi])))
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
            pieces.append((comp, None))
            remain &= ~comp

        if len(pieces) > 1 or (pieces and pieces[0][0] != active):
            solved = []
            for mask, poly in pieces:
                if poly is None:
                    poly = self._solve_poly(mask, domains)
                solved.append((mask, poly))
            solved.sort(key=lambda item: len(item[1]))
            combined_active = 0
            ans = {(): 1}
            for mask, poly in solved:
                combined_active |= mask
                ans = self._convolve_boundary(ans, poly, combined_active)
                if not ans:
                    break
            assert combined_active == active
            self.poly_memo[key] = ans
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
            for state, weight in self._solve_poly(active, tuple(nd)).items():
                out[state] += int(weight)
            self._guard(out)
        ans = dict(out)
        self.poly_memo[key] = ans
        return ans

    def count_profile(self, domains):
        baseline, baseline_calls, baseline_memo = PAIRWISE_COUNTER.count_profile(self, domains)
        dsum = sum(int(d).bit_count() for d in domains)
        if dsum not in TARGET_DOMAIN_SUMS:
            return baseline, baseline_calls, baseline_memo
        self.aff_cache.clear()
        self.poly_memo.clear()
        self.poly_stats.clear()
        self.boundary_cache.clear()
        self.project_cache.clear()
        self.boundary_stats.clear()
        self.boundary_rank_hist.clear()
        self.poly_calls = 0
        self.peak_poly_states = 0
        status = 'completed'
        exact = None
        final_states = None
        try:
            poly = self._solve_poly(self.ALL, tuple(domains))
            exact = sum(int(weight) for weight in poly.values())
            final_states = len(poly)
        except P.PolyBudgetExceeded as exc:
            status = 'budget_exceeded'
            self.poly_stats['budget_reason'] = str(exc)
        if exact is not None:
            assert 0 <= exact <= baseline
            if dsum in EXPECTED_MEDIUM:
                assert baseline == EXPECTED_MEDIUM[dsum]
                assert exact == baseline
            assert final_states <= 1
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
            'intersection_cache_entries': len(self.aff_cache),
            'boundary_cache_entries': len(self.boundary_cache),
            'projection_cache_entries': len(self.project_cache),
            'boundary_rank_histogram': dict(sorted(self.boundary_rank_hist.items())),
            'boundary_stats': dict(self.boundary_stats),
            'stats': dict(self.poly_stats),
        }
        SCOUT_ROWS.append(row)
        print('affine_boundary', json.dumps(row, sort_keys=True), flush=True)
        return baseline, baseline_calls, baseline_memo


def analyze():
    original = C.ExactCounter
    C.ExactCounter = BoundaryProjectedCounter
    try:
        with redirect_stdout(io.StringIO()):
            baseline = C.analyze()
        assert int(baseline['exact_count']) == int(C.EXPECTED_EXACT_COUNT)
    finally:
        C.ExactCounter = original
    got = {int(row['domain_state_sum']) for row in SCOUT_ROWS}
    assert got == set(TARGET_DOMAIN_SUMS), (got, TARGET_DOMAIN_SUMS)
    out = {
        'position': 'C',
        'physical_shared_dimension': A.PHYS_N,
        'global_projection_normal_rank': A.EXPECTED_NORMAL_RANK,
        'pairwise_exact_baseline_count': int(C.EXPECTED_EXACT_COUNT),
        'target_domain_state_sums': list(TARGET_DOMAIN_SUMS),
        'max_poly_calls': P.MAX_POLY_CALLS,
        'max_poly_states': P.MAX_POLY_STATES,
        'scout_rows': SCOUT_ROWS,
        'completed_profiles': sum(row['status'] == 'completed' for row in SCOUT_ROWS),
        'budget_exceeded_profiles': sum(row['status'] != 'completed' for row in SCOUT_ROWS),
        'decision': 'C916_COMPLETE_PAIRWISE_ALL_ORDER_AFFINE_POLYNOMIAL_BOUNDARY_PROJECTED_SCOUT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_COMPLETE_PAIRWISE_AFFINE_POLYNOMIAL_BOUNDARY_PROJECTED_SCOUT')
    print('scope=exact component affine-state polynomials projected before memoization to the conservative span of all possible normals outside each active subproblem; projection preserves exactly the affine information any future continuation can observe')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
