#!/usr/bin/env python3
import hashlib
import io
import json
import math
import sys
from collections import defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C

PAIRWISE_COUNTER = C.ExactCounter
TRIPLES_EXPECTED = 5
QUADS = (
    (3, 8, 12, 183),
    (3, 113, 183, 185),
    (7, 144, 154, 186),
    (10, 24, 154, 186),
    (11, 24, 112, 181),
    (11, 24, 112, 182),
    (237, 239, 240, 249),
)
EVENT_COUNT = 12
ALL_EVENTS = (1 << EVENT_COUNT) - 1
EXPECTED_PAIRWISE_TOTAL = int(C.EXPECTED_EXACT_COUNT)
EXPECTED_FINITE_TOTAL = 119224931058957005800358130035798112729920532677074863008477782553762159001600000
EXPECTED_PROFILE_COUNTS = {
    83: 0,
    88: 1,
    95: 0,
    100: 25,
    102: 0,
    134: 21578474445840,
    154: 42542498200320,
    251: 114884695573259724175905211418508096,
    288: 218548782904222169092344242900939904,
    302: 234148899850520139999772901208978048,
}
BONFERRONI_LOWER = 2722414587159602541040697551354574968461239522793839001600000
BONFERRONI_UPPER = 441205873912093509972717475553434060732158565102084857212293988604025199001600000
PROFILE_ROWS = []


class EventMaskVectorCounter(PAIRWISE_COUNTER):
    """Exact pairwise CSP counter over the semiring of 12-bit event masks.

    For an assignment to an active variable set, a bit remains set iff no
    participant of that forbidden projection event has been assigned zero.
    Thus on the full variable set a bit is set exactly when that event is
    violated (all of its participants are nonzero). The coefficient at mask 0
    is therefore the exact count satisfying all twelve not-all-nonzero clauses.

    Disjoint pairwise components combine by bitwise AND because an event is
    globally all-nonzero iff it is locally all-nonzero in every component.
    This preserves the original pairwise component factorization without
    inserting hyperedges into the connectivity graph.
    """

    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        m4 = C.load(C.M4_PATH)
        triples = tuple(tuple(map(int, row)) for row in m4['projection_minimal_empty_triples'])
        assert len(triples) == TRIPLES_EXPECTED
        gid_events = triples + QUADS
        assert len(gid_events) == EVENT_COUNT

        loc = {}
        for vi, members in enumerate(self.variables):
            for ci, gid in enumerate(members):
                loc[int(gid)] = (vi, ci)
        assert len(loc) == 90

        self.event_incidence = [0] * self.N
        self.zero_state = {}
        mapped = []
        for ei, edge in enumerate(gid_events):
            row = []
            for gid in edge:
                vi, ci = loc[int(gid)]
                # The frozen 5+7 projection obstructions avoid both contracted
                # signed-pair variables, so one local zero state is sufficient.
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                z = max(int(state[0]) for state in self.var_states[vi])
                self.zero_state[vi] = z
                self.event_incidence[vi] |= 1 << ei
                row.append(vi)
            assert len(row) == len(set(row)) == len(edge)
            mapped.append(tuple(sorted(row)))
        self.events = tuple(mapped)

        self.vector_memo = {}
        self.vector_calls = 0
        self.vector_peak_states = 0
        self.and_convolutions = 0
        self.vector_memo_hits = 0

    def _record_peak(self, poly):
        self.vector_peak_states = max(self.vector_peak_states, len(poly))
        assert len(poly) <= (1 << EVENT_COUNT)

    def _add_poly(self, left, right):
        if not left:
            out = dict(right)
            self._record_peak(out)
            return out
        out = dict(left)
        for mask, weight in right.items():
            out[mask] = out.get(mask, 0) + int(weight)
        self._record_peak(out)
        return out

    def _and_convolve(self, left, right):
        if not left or not right:
            return {}
        if len(left) > len(right):
            left, right = right, left
        self.and_convolutions += 1
        out = defaultdict(int)
        for lm, lw in left.items():
            for rm, rw in right.items():
                out[int(lm) & int(rm)] += int(lw) * int(rw)
        ans = dict(out)
        self._record_peak(ans)
        return ans

    def _shift_clear(self, poly, clear_mask, factor):
        if not poly or factor == 0:
            return {}
        if clear_mask == 0:
            ans = {mask: int(weight) * int(factor) for mask, weight in poly.items()}
            self._record_peak(ans)
            return ans
        keep = ALL_EVENTS ^ int(clear_mask)
        out = defaultdict(int)
        for mask, weight in poly.items():
            out[int(mask) & keep] += int(weight) * int(factor)
        ans = dict(out)
        self._record_peak(ans)
        return ans

    def _isolated_poly(self, vi, domain):
        incidence = int(self.event_incidence[vi])
        if incidence == 0:
            return {ALL_EVENTS: int(self.wsum[vi][domain])}
        z = int(self.zero_state[vi])
        zbit = 1 << z
        zero_weight = int(self.var_weights[vi][z]) if domain & zbit else 0
        nonzero_weight = int(self.wsum[vi][int(domain) & ~zbit])
        out = {}
        if nonzero_weight:
            out[ALL_EVENTS] = nonzero_weight
        if zero_weight:
            mask = ALL_EVENTS ^ incidence
            out[mask] = out.get(mask, 0) + zero_weight
        self._record_peak(out)
        return out

    def vector_solve(self, active, domains):
        self.vector_calls += 1
        closed = self._arc_closure(active, domains)
        if closed is None:
            return {}
        domains = closed

        singleton = 0
        factor = 1
        clear_mask = 0
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
                if self.event_incidence[vi] and si == self.zero_state[vi]:
                    clear_mask |= int(self.event_incidence[vi])
        if singleton:
            rest = active ^ singleton
            if rest == 0:
                return {ALL_EVENTS ^ clear_mask: factor}
            return self._shift_clear(self.vector_solve(rest, domains), clear_mask, factor)

        key = (active, tuple(domains[i] for i in range(self.N) if (active >> i) & 1))
        cached = self.vector_memo.get(key)
        if cached is not None:
            self.vector_memo_hits += 1
            return cached

        remain = active
        pieces = []
        while remain:
            seed = remain & -remain
            vi = seed.bit_length() - 1
            if self._relevant_neighbors(vi, active, domains) == 0:
                pieces.append((seed, self._isolated_poly(vi, domains[vi])))
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

        if len(pieces) > 1 or pieces[0][0] != active:
            solved = []
            for mask, poly in pieces:
                if poly is None:
                    poly = self.vector_solve(mask, domains)
                solved.append(poly)
            solved.sort(key=len)
            ans = {ALL_EVENTS: 1}
            for poly in solved:
                ans = self._and_convolve(ans, poly)
                if not ans:
                    break
            self.vector_memo[key] = ans
            return ans

        best = None
        scan = active
        while scan:
            bit = scan & -scan
            vi = bit.bit_length() - 1
            scan ^= bit
            score = (
                int(domains[vi]).bit_count(),
                -self._relevant_neighbors(vi, active, domains).bit_count(),
                -int(self.event_incidence[vi]).bit_count(),
                vi,
            )
            if best is None or score < best[0]:
                best = (score, vi)
        vi = best[1]

        ans = {}
        mask = int(domains[vi])
        while mask:
            bit = mask & -mask
            mask ^= bit
            nd = list(domains)
            nd[vi] = bit
            ans = self._add_poly(ans, self.vector_solve(active, tuple(nd)))
        self.vector_memo[key] = ans
        return ans

    def count_profile(self, domains):
        baseline, baseline_calls, baseline_memo = PAIRWISE_COUNTER.count_profile(self, domains)
        self.vector_memo.clear()
        self.vector_calls = 0
        self.vector_peak_states = 0
        self.and_convolutions = 0
        self.vector_memo_hits = 0

        dist = self.vector_solve(self.ALL, tuple(domains))
        tracked_total = sum(int(weight) for weight in dist.values())
        assert tracked_total == int(baseline)
        exact = int(dist.get(0, 0))
        dsum = sum(int(d).bit_count() for d in domains)
        assert exact == EXPECTED_PROFILE_COUNTS[dsum], (dsum, exact, EXPECTED_PROFILE_COUNTS[dsum])

        digest_payload = ';'.join(f'{mask}:{dist[mask]}' for mask in sorted(dist))
        row = {
            'domain_state_sum': dsum,
            'pairwise_count': int(baseline),
            'finite_hyperedge_exact_count': exact,
            'gain_log2_bits': None if exact == 0 or baseline == 0 else math.log2(baseline) - math.log2(exact),
            'positive_event_masks': len(dist),
            'event_mask_distribution_sha256': hashlib.sha256(digest_payload.encode()).hexdigest(),
            'vector_calls': self.vector_calls,
            'vector_memo_states': len(self.vector_memo),
            'vector_memo_hits': self.vector_memo_hits,
            'peak_event_mask_states': self.vector_peak_states,
            'and_convolutions': self.and_convolutions,
            'pairwise_baseline_calls': baseline_calls,
            'pairwise_baseline_memo_states': baseline_memo,
        }
        PROFILE_ROWS.append(row)
        print('eventmask_profile', json.dumps(row, sort_keys=True), flush=True)
        return exact, self.vector_calls, len(self.vector_memo)


def analyze():
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    C.ExactCounter = EventMaskVectorCounter
    C.EXPECTED_EXACT_COUNT = EXPECTED_FINITE_TOTAL
    try:
        with redirect_stdout(io.StringIO()):
            base = C.analyze()
    finally:
        C.ExactCounter = original_counter
        C.EXPECTED_EXACT_COUNT = original_expected

    assert int(base['exact_count']) == EXPECTED_FINITE_TOTAL
    assert {int(row['domain_state_sum']) for row in PROFILE_ROWS} == set(EXPECTED_PROFILE_COUNTS)
    assert BONFERRONI_LOWER <= EXPECTED_FINITE_TOTAL <= BONFERRONI_UPPER
    hard = {int(row['domain_state_sum']): row for row in PROFILE_ROWS if int(row['domain_state_sum']) in (251, 288, 302)}
    assert {int(row['positive_event_masks']) for row in hard.values()} == {384}

    log2 = math.log2(EXPECTED_FINITE_TOTAL)
    out = {
        'position': 'C',
        'physical_shared_dimension': 149,
        'pairwise_exact_baseline_count': EXPECTED_PAIRWISE_TOTAL,
        'projection_minimal_empty_triples': 5,
        'projection_minimal_empty_quadruples': 7,
        'projection_events': EVENT_COUNT,
        'exact_count': EXPECTED_FINITE_TOTAL,
        'exact_log2': log2,
        'state_bits': EXPECTED_FINITE_TOTAL.bit_length(),
        'gain_vs_pairwise_exact_log2_bits': math.log2(EXPECTED_PAIRWISE_TOTAL) - log2,
        'bonferroni_lower_authority': BONFERRONI_LOWER,
        'bonferroni_upper_authority': BONFERRONI_UPPER,
        'bonferroni_authority_run': 34826179077,
        'profile_rows': PROFILE_ROWS,
        'decision': 'C916_250WAY_COMPLETE_M4_PAIRWISE_PLUS_12_PROJECTION_HYPEREDGES_EVENTMASK_VECTOR_EXACT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PROJECTION_HYPEREDGES_EVENTMASK_VECTOR_EXACT')
    print('theorem=the original exact pairwise component recursion lifts to a finite 12-bit event-mask semiring; disjoint components combine by bitwise AND, so coefficient mask 0 is exactly the assignments satisfying all five projection triples and seven projection quadruples')
    print('boundary=all-order affine intersection and any further higher-order physical-image constraint remain outside this finite-hyperedge model')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
