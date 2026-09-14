#!/usr/bin/env python3
import io, json, math, os, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_affine_polynomial_scout as P

# C.ExactCounter is temporarily monkey-patched in analyze(). Freeze the actual
# scalar pairwise base class now so helper calls cannot recurse back into this
# subclass after that patch.
PAIRWISE_COUNTER = C.ExactCounter

TARGET_DOMAIN_SUMS = tuple(sorted({int(x) for x in os.environ.get('C916_AFFINE_COND_DOMAIN_SUMS', '134,154,251').split(',') if x.strip()}))
QUADS = (
    (3,8,12,183), (3,113,183,185), (7,144,154,186),
    (10,24,154,186), (11,24,112,181), (11,24,112,182),
    (237,239,240,249),
)
EXPECTED_MEDIUM = {134: 21578474445840, 154: 42542498200320}
SCOUT_ROWS = []


def canonical_edges(edges):
    ordered = sorted({tuple(sorted(map(int, edge))) for edge in edges if edge}, key=lambda e: (len(e), e))
    kept = []
    for edge in ordered:
        se = set(edge)
        if any(set(old) <= se for old in kept):
            continue
        kept.append(edge)
    return tuple(kept)


class ConditionedAffinePolynomialCounter(P.AffinePolynomialCounter):
    """Exact all-order affine counter with finite projection clauses first.

    The 5+7 frozen empty projection sets are necessary consequences of the full
    affine-intersection theorem. Enforcing them first by a disjoint first-zero
    partition cannot remove a valid assignment; it only splits the exact search
    into smaller unary-conditioned branches before affine polynomial convolution.
    Each terminal branch is independent, so its exact affine count is scalar-summed
    and its potentially large polynomial can be discarded immediately.
    """

    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        m4 = C.load(C.M4_PATH)
        triples = tuple(tuple(map(int, t)) for t in m4['projection_minimal_empty_triples'])
        assert len(triples) == 5 and len(QUADS) == 7
        gid_edges = triples + QUADS
        loc = {}
        for vi, members in enumerate(self.variables):
            for ci, gid in enumerate(members):
                loc[int(gid)] = (vi, ci)
        assert len(loc) == 90
        zero = {}
        mapped = []
        for edge in gid_edges:
            row = []
            for gid in edge:
                vi, ci = loc[int(gid)]
                # The frozen 12 hyperedges avoid the two signed-pair contracted
                # variables. Keep this explicit; otherwise local zero predicates
                # would need a multi-coordinate clause representation.
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                zero[vi] = max(int(s[0]) for s in self.var_states[vi])
                row.append(vi)
            assert len(row) == len(set(row)) == len(edge)
            mapped.append(tuple(sorted(row)))
        self.zero_state = zero
        self.hyperedges = canonical_edges(mapped)
        assert len(self.hyperedges) == 12
        self.hyper_memo = {}
        self.hyper_stats = Counter()
        self.terminal_stats = Counter()
        self.terminal_peak_poly_states = 0

    def _restrict_zero(self, domains, vi):
        bit = 1 << self.zero_state[vi]
        d = int(domains[vi]) & bit
        if not d:
            return None
        out = list(domains); out[vi] = d
        return tuple(out)

    def _restrict_nonzero(self, domains, vi):
        bit = 1 << self.zero_state[vi]
        d = int(domains[vi]) & ~bit
        if not d:
            return None
        out = list(domains); out[vi] = d
        return tuple(out)

    def _normalize_hyper(self, domains, edges):
        dom = tuple(domains)
        eds = tuple(edges)
        while True:
            dom = PAIRWISE_COUNTER._arc_closure(self, self.ALL, dom)
            if dom is None:
                self.hyper_stats['pairwise_wipeouts'] += 1
                return None, None
            reduced = []
            forced = None
            for edge in eds:
                uncertain = []
                satisfied = False
                for vi in edge:
                    d = int(dom[vi]); zbit = 1 << self.zero_state[vi]
                    can_zero = bool(d & zbit)
                    can_nonzero = bool(d & ~zbit)
                    if not can_nonzero:
                        satisfied = True
                        break
                    if can_zero:
                        uncertain.append(vi)
                if satisfied:
                    self.hyper_stats['satisfied_edges_dropped'] += 1
                    continue
                if not uncertain:
                    self.hyper_stats['forbidden_all_nonzero_prunes'] += 1
                    return None, None
                if len(uncertain) == 1:
                    forced = uncertain[0]
                    break
                reduced.append(tuple(sorted(uncertain)))
            if forced is not None:
                dom = self._restrict_zero(dom, forced)
                if dom is None:
                    self.hyper_stats['forced_zero_wipeouts'] += 1
                    return None, None
                self.hyper_stats['unit_hyperedge_forces'] += 1
                continue
            return dom, canonical_edges(reduced)

    def _choose_edge(self, domains, edges):
        # Favor a short clause, then one whose variables already have the least
        # surviving pairwise freedom. This makes first-zero branches propagate.
        return min(edges, key=lambda e: (len(e), sum(int(domains[v]).bit_count() for v in e), e))

    def _terminal_affine_count(self, domains):
        # Branches are disjoint, so retaining polynomial maps across terminals is
        # unnecessary. Clearing profile-local caches bounds peak memory while
        # preserving exactness; immutable state_aff remains shared.
        self.aff_cache.clear()
        self.poly_memo.clear()
        self.poly_stats.clear()
        self.poly_calls = 0
        self.peak_poly_states = 0
        poly = self._solve_poly(self.ALL, tuple(domains))
        value = sum(int(w) for w in poly.values())
        self.terminal_stats['terminal_branches'] += 1
        self.terminal_stats['poly_calls_sum'] += self.poly_calls
        self.terminal_stats['poly_memo_states_sum'] += len(self.poly_memo)
        self.terminal_stats['intersection_cache_entries_sum'] += len(self.aff_cache)
        self.terminal_stats['affine_empty_prunes_sum'] += int(self.poly_stats.get('affine_empty_prunes', 0))
        self.terminal_peak_poly_states = max(self.terminal_peak_poly_states, self.peak_poly_states)
        return value

    def _count_conditioned(self, domains, edges):
        self.hyper_stats['hyper_calls'] += 1
        dom, eds = self._normalize_hyper(domains, edges)
        if dom is None:
            return 0
        if not eds:
            return self._terminal_affine_count(dom)
        key = (eds, dom)
        got = self.hyper_memo.get(key)
        if got is not None:
            self.hyper_stats['hyper_memo_hits'] += 1
            return got
        edge = self._choose_edge(dom, eds)
        rest = tuple(e for e in eds if e != edge)
        total = 0
        prefix = dom
        # Disjoint exact partition of the satisfying clause: first zero at vi.
        for vi in edge:
            zdom = self._restrict_zero(prefix, vi)
            if zdom is not None:
                total += self._count_conditioned(zdom, rest)
                self.hyper_stats['first_zero_branches'] += 1
            prefix = self._restrict_nonzero(prefix, vi)
            if prefix is None:
                break
        self.hyper_memo[key] = total
        return total

    def count_profile(self, domains):
        baseline, baseline_calls, baseline_memo = PAIRWISE_COUNTER.count_profile(self, domains)
        dsum = sum(int(d).bit_count() for d in domains)
        if dsum not in TARGET_DOMAIN_SUMS:
            return baseline, baseline_calls, baseline_memo
        self.hyper_memo.clear(); self.hyper_stats.clear(); self.terminal_stats.clear()
        self.terminal_peak_poly_states = 0
        status = 'completed'; exact = None
        try:
            exact = self._count_conditioned(tuple(domains), self.hyperedges)
        except P.PolyBudgetExceeded as exc:
            status = 'budget_exceeded'
            self.hyper_stats['budget_reason'] = str(exc)
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
            'hyper_memo_states': len(self.hyper_memo),
            'hyper_stats': dict(self.hyper_stats),
            'terminal_stats': dict(self.terminal_stats),
            'terminal_peak_poly_states': self.terminal_peak_poly_states,
        }
        SCOUT_ROWS.append(row)
        print('affine_conditioned', json.dumps(row, sort_keys=True), flush=True)
        return baseline, baseline_calls, baseline_memo


def analyze():
    original = C.ExactCounter
    C.ExactCounter = ConditionedAffinePolynomialCounter
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
        'physical_shared_dimension': 149,
        'pairwise_exact_baseline_count': int(C.EXPECTED_EXACT_COUNT),
        'finite_projection_hyperedges_preconditioned': 12,
        'target_domain_state_sums': list(TARGET_DOMAIN_SUMS),
        'parent_poly_max_calls': P.MAX_POLY_CALLS,
        'parent_poly_max_states': P.MAX_POLY_STATES,
        'scout_rows': SCOUT_ROWS,
        'completed_profiles': sum(r['status'] == 'completed' for r in SCOUT_ROWS),
        'budget_exceeded_profiles': sum(r['status'] != 'completed' for r in SCOUT_ROWS),
        'decision': 'C916_COMPLETE_PAIRWISE_ALL_ORDER_AFFINE_POLYNOMIAL_CONDITIONED_HYPEREDGES_SCOUT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_AFFINE_POLYNOMIAL_CONDITIONED_HYPEREDGES_SCOUT')
    print('scope=exact all-order affine count after disjoint exact conditioning by the five frozen minimal-empty triples and seven frozen minimal-empty quadruples; terminal pairwise components are contracted as exact affine-state polynomials and branch polynomials are discarded after scalar exact summation')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
