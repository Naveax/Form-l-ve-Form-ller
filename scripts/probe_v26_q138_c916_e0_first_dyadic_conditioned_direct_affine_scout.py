#!/usr/bin/env python3
import io, json, math, os, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_all_order_affine_scout as A
import probe_v26_q138_c916_e0_first_dyadic_pr212_plus_projection_triples_quads_exact as H

PAIRWISE_COUNTER = C.ExactCounter
TARGET_DOMAIN_SUMS = tuple(sorted({int(x) for x in os.environ.get('C916_COND_DIRECT_AFFINE_DOMAIN_SUMS', '154,251').split(',') if x.strip()}))
QUADS = tuple(tuple(map(int, q)) for q in H.QUADS)
EXPECTED_REGRESSION = {154: 42542498200320}
EVENT_MASS_PRIORITY = (4, 3, 0, 1, 9, 10, 6, 5, 11, 8, 7, 2)
EVENT_PRIORITY_RANK = {event_index: rank for rank, event_index in enumerate(EVENT_MASS_PRIORITY)}
SCOUT_ROWS = []


def canonical_edges(edges):
    ordered = sorted({tuple(sorted(map(int, e))) for e in edges if e}, key=lambda e: (len(e), e))
    kept = []
    for edge in ordered:
        se = set(edge)
        if any(set(old) <= se for old in kept):
            continue
        kept.append(edge)
    return tuple(kept)


class ConditionedDirectAffineCounter(A.AffineScoutCounter):
    """Exact direct affine recursion after finite projection-clause conditioning.

    The 5 minimal-empty triples and 7 minimal-empty quadruples are exact necessary
    physical-image conditions. They are enforced by disjoint first-zero partitions.
    Each terminal branch then runs the already-merged exact global affine recursion.
    No branch is approximated; any direct-affine call-budget exhaustion is reported
    as incomplete and never converted into a count.
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

        self.zero_state = {}
        mapped = []
        for edge in gid_edges:
            row = []
            for gid in edge:
                vi, ci = loc[int(gid)]
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                self.zero_state[vi] = max(int(s[0]) for s in self.var_states[vi])
                row.append(vi)
            assert len(row) == len(set(row)) == len(edge)
            mapped.append(tuple(sorted(row)))
        self.raw_mapped_edges = tuple(mapped)
        self.hyperedges = canonical_edges(mapped)
        assert len(self.hyperedges) == 12
        self.hyper_memo = {}
        self.hyper_stats = Counter()
        self.terminal_stats = Counter()
        self.terminal_peak_affine_memo = 0
        self.terminal_peak_intersections = 0

    def _restrict_zero(self, domains, vi):
        bit = 1 << self.zero_state[vi]
        d = int(domains[vi]) & bit
        if not d:
            return None
        out = list(domains)
        out[vi] = d
        return tuple(out)

    def _restrict_nonzero(self, domains, vi):
        bit = 1 << self.zero_state[vi]
        d = int(domains[vi]) & ~bit
        if not d:
            return None
        out = list(domains)
        out[vi] = d
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
                    d = int(dom[vi])
                    zbit = 1 << self.zero_state[vi]
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

    def _event_priority(self, edge):
        target = set(edge)
        ranks = [EVENT_PRIORITY_RANK[i] for i, raw in enumerate(self.raw_mapped_edges) if target <= set(raw)]
        return min(ranks) if ranks else len(EVENT_MASS_PRIORITY)

    def _choose_edge(self, domains, edges):
        return min(edges, key=lambda e: (
            self._event_priority(e),
            len(e),
            sum(int(domains[v]).bit_count() for v in e),
            e,
        ))

    def _terminal_affine_count(self, domains):
        self.aff_cache.clear()
        self.aff_stats.clear()
        self.aff_memo.clear()
        self.aff_calls = 0
        value = self._solve_affine(self.ALL, tuple(domains), ())
        self.terminal_stats['terminal_branches'] += 1
        self.terminal_stats['affine_calls_sum'] += self.aff_calls
        self.terminal_stats['affine_memo_states_sum'] += len(self.aff_memo)
        self.terminal_stats['intersection_cache_entries_sum'] += len(self.aff_cache)
        self.terminal_peak_affine_memo = max(self.terminal_peak_affine_memo, len(self.aff_memo))
        self.terminal_peak_intersections = max(self.terminal_peak_intersections, len(self.aff_cache))
        return int(value)

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

        self.hyper_memo.clear()
        self.hyper_stats.clear()
        self.terminal_stats.clear()
        self.terminal_peak_affine_memo = 0
        self.terminal_peak_intersections = 0
        status = 'completed'
        exact = None
        try:
            if dsum in EXPECTED_REGRESSION:
                self.aff_cache.clear(); self.aff_stats.clear(); self.aff_memo.clear(); self.aff_calls = 0
                exact = int(self._solve_affine(self.ALL, tuple(domains), ()))
                self.terminal_stats['unconditioned_regression_calls'] = self.aff_calls
                self.terminal_stats['unconditioned_regression_memo_states'] = len(self.aff_memo)
            else:
                exact = int(self._count_conditioned(tuple(domains), self.hyperedges))
        except A.CallBudgetExceeded as exc:
            status = 'call_budget_exceeded'
            self.hyper_stats['budget_reason'] = str(exc)

        if exact is not None:
            assert 0 <= exact <= baseline
            if dsum in EXPECTED_REGRESSION:
                assert baseline == EXPECTED_REGRESSION[dsum]
                assert exact == baseline

        row = {
            'domain_state_sum': dsum,
            'status': status,
            'pairwise_count': int(baseline),
            'all_order_affine_count': exact,
            'gain_log2_bits': None if exact is None or exact == 0 else math.log2(baseline) - math.log2(exact),
            'hyper_memo_states': len(self.hyper_memo),
            'hyper_stats': dict(self.hyper_stats),
            'terminal_stats': dict(self.terminal_stats),
            'terminal_peak_affine_memo': self.terminal_peak_affine_memo,
            'terminal_peak_intersections': self.terminal_peak_intersections,
            'event_mass_priority': list(EVENT_MASS_PRIORITY),
        }
        SCOUT_ROWS.append(row)
        print('conditioned_direct_affine', json.dumps(row, sort_keys=True), flush=True)
        return baseline, baseline_calls, baseline_memo


def analyze():
    original = C.ExactCounter
    C.ExactCounter = ConditionedDirectAffineCounter
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
        'finite_projection_hyperedges_preconditioned': 12,
        'event_mass_priority': list(EVENT_MASS_PRIORITY),
        'event_mass_priority_authority_run': 34826179077,
        'target_domain_state_sums': list(TARGET_DOMAIN_SUMS),
        'max_direct_affine_calls_per_terminal': A.MAX_CALLS,
        'scout_rows': SCOUT_ROWS,
        'completed_profiles': sum(r['status'] == 'completed' for r in SCOUT_ROWS),
        'budget_exceeded_profiles': sum(r['status'] != 'completed' for r in SCOUT_ROWS),
        'decision': 'C916_COMPLETE_PAIRWISE_CONDITIONED_DIRECT_ALL_ORDER_AFFINE_SCOUT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_CONDITIONED_DIRECT_AFFINE_SCOUT')
    print('scope=exact all-order affine recursion on disjoint branches satisfying the five frozen minimal-empty triples and seven frozen minimal-empty quadruples; mass priority affects traversal only and call-budget exhaustion is incomplete')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
