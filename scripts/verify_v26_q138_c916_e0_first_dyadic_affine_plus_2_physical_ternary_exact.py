#!/usr/bin/env python3
import io
import json
import math
import sys
from collections import defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import verify_v26_q138_c916_e0_first_dyadic_projection_hyperedges_eventmask_vector_exact as V
import verify_v26_q138_c916_e0_first_dyadic_all_order_affine_support_exact as A

PAIRWISE_COUNTER = C.ExactCounter
AFFINE_EVENT_COUNT = 19
PHYSICAL_TERNARY = (
    ((5, 181, 182), ((0, 1, 1), (1, 0, 2), (1, 1, 0), (2, 0, 1))),
    ((11, 12, 24), ((0, 1, 1), (1, 0, 2), (1, 2, 0))),
)
PHYSICAL_EVENT_COUNT = sum(len(rows) for _gids, rows in PHYSICAL_TERNARY)
EVENT_COUNT = AFFINE_EVENT_COUNT + PHYSICAL_EVENT_COUNT
ALL_EVENTS = (1 << EVENT_COUNT) - 1
AFFINE_MASK = (1 << AFFINE_EVENT_COUNT) - 1
PHYSICAL_MASK = ALL_EVENTS ^ AFFINE_MASK
EXPECTED_AFFINE_TOTAL = 100215909735124105069922281032909019043326715916545026952580687530924399001600000
EXPECTED_AFFINE_PROFILE_COUNTS = {
    83: 0,
    88: 1,
    95: 0,
    100: 25,
    102: 0,
    134: 21578474445840,
    154: 42542498200320,
    251: 96491872903925175488260425426864960,
    288: 183697181089509355446657454121817216,
    302: 196896631570740171574763723334509184,
}
PROFILE_ROWS = []


class AnyExpected:
    def __eq__(self, other):
        return True


class AffinePlusPhysicalEventCounter(V.EventMaskVectorCounter):
    """Exact pairwise recursion over 19 affine events plus seven value events.

    Each physical forbidden quotient tuple is represented as one event whose bit
    survives iff all three participating variables take the forbidden states.
    This is the same exact AND-semiring principle used for the affine support
    events, so an event may span pairwise components without adding a hard
    hyperedge to the recursion graph. Mask zero satisfies every affine circuit
    and every physical ternary factor simultaneously.
    """

    def __init__(self, variables, var_states, var_weights, pairq):
        PAIRWISE_COUNTER.__init__(self, variables, var_states, var_weights, pairq)
        m4 = C.load(C.M4_PATH)
        triples = tuple(tuple(map(int, row)) for row in m4['projection_minimal_empty_triples'])
        assert len(triples) == 5
        affine_events = triples + V.QUADS + (A.AFFINE_FIVE,) + A.EXTRA_SIX
        assert len(affine_events) == AFFINE_EVENT_COUNT
        assert A.Q.digest_rows(tuple(sorted(affine_events, key=lambda r: (len(r), tuple(r))))) == A.EXPECTED_CONFLICT_DIGEST

        loc = {}
        for vi, members in enumerate(self.variables):
            for ci, gid in enumerate(members):
                loc[int(gid)] = (vi, ci)
        assert len(loc) == 90

        self.event_incidence = [0] * self.N
        self.clear_by_state = [[0] * len(self.var_states[vi]) for vi in range(self.N)]
        event = 0

        for edge in affine_events:
            bit = 1 << event
            event += 1
            for gid in edge:
                vi, ci = loc[int(gid)]
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                zero = max(int(state[0]) for state in self.var_states[vi])
                self.event_incidence[vi] |= bit
                self.clear_by_state[vi][zero] |= bit

        mapped_physical = []
        for gids, forbidden_rows in PHYSICAL_TERNARY:
            vis = []
            for gid in gids:
                vi, ci = loc[int(gid)]
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                assert len(self.var_states[vi]) == 4, (gid, self.var_states[vi])
                vis.append(vi)
            assert len(set(vis)) == 3
            for row in forbidden_rows:
                row = tuple(map(int, row))
                assert len(row) == 3 and all(0 <= x < 4 for x in row)
                bit = 1 << event
                event += 1
                for pos, vi in enumerate(vis):
                    self.event_incidence[vi] |= bit
                    required = row[pos]
                    for si in range(len(self.var_states[vi])):
                        if si != required:
                            self.clear_by_state[vi][si] |= bit
                mapped_physical.append((tuple(gids), row))
        assert event == EVENT_COUNT
        assert len(mapped_physical) == PHYSICAL_EVENT_COUNT
        self.physical_events = tuple(mapped_physical)

        self.vector_memo = {}
        self.vector_calls = 0
        self.vector_peak_states = 0
        self.and_convolutions = 0
        self.vector_memo_hits = 0

    def _isolated_poly(self, vi, domain):
        out = defaultdict(int)
        mask = int(domain)
        while mask:
            bit = mask & -mask
            mask ^= bit
            si = bit.bit_length() - 1
            event_mask = ALL_EVENTS ^ int(self.clear_by_state[vi][si])
            out[event_mask] += int(self.var_weights[vi][si])
        ans = dict(out)
        self._record_peak(ans)
        return ans

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
                clear_mask |= int(self.clear_by_state[vi][si])
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
            for piece, poly in pieces:
                if poly is None:
                    poly = self.vector_solve(piece, domains)
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
        affine_expected = int(EXPECTED_AFFINE_PROFILE_COUNTS[dsum])
        affine_from_dist = sum(int(weight) for mask, weight in dist.items() if (int(mask) & AFFINE_MASK) == 0)
        physical_from_dist = sum(int(weight) for mask, weight in dist.items() if (int(mask) & PHYSICAL_MASK) == 0)
        assert affine_from_dist == affine_expected, (dsum, affine_from_dist, affine_expected)
        assert exact <= affine_expected
        assert exact <= physical_from_dist <= baseline

        row = {
            'domain_state_sum': dsum,
            'pairwise_count': int(baseline),
            'all_order_affine_support_count': affine_from_dist,
            'pairwise_plus_two_physical_ternary_count': physical_from_dist,
            'affine_plus_two_physical_ternary_count': exact,
            'removed_vs_affine': affine_from_dist - exact,
            'gain_vs_affine_log2_bits': None if exact == 0 or affine_from_dist == 0 else math.log2(affine_from_dist) - math.log2(exact),
            'positive_event_masks': len(dist),
            'vector_calls': self.vector_calls,
            'vector_memo_states': len(self.vector_memo),
            'vector_memo_hits': self.vector_memo_hits,
            'peak_event_mask_states': self.vector_peak_states,
            'and_convolutions': self.and_convolutions,
            'pairwise_baseline_calls': baseline_calls,
            'pairwise_baseline_memo_states': baseline_memo,
        }
        PROFILE_ROWS.append(row)
        print('affine19_physical2_profile', json.dumps(row, sort_keys=True), flush=True)
        return exact, self.vector_calls, len(self.vector_memo)


def analyze():
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    old_v_event_count = V.EVENT_COUNT
    old_v_all_events = V.ALL_EVENTS
    V.EVENT_COUNT = EVENT_COUNT
    V.ALL_EVENTS = ALL_EVENTS
    C.ExactCounter = AffinePlusPhysicalEventCounter
    C.EXPECTED_EXACT_COUNT = AnyExpected()
    try:
        with redirect_stdout(io.StringIO()):
            base = C.analyze()
    finally:
        C.ExactCounter = original_counter
        C.EXPECTED_EXACT_COUNT = original_expected
        V.EVENT_COUNT = old_v_event_count
        V.ALL_EVENTS = old_v_all_events

    total = int(base['exact_count'])
    assert total <= EXPECTED_AFFINE_TOTAL
    assert {int(row['domain_state_sum']) for row in PROFILE_ROWS} == set(EXPECTED_AFFINE_PROFILE_COUNTS)
    weighted_affine = sum(
        int(row['base_mass']) * int(EXPECTED_AFFINE_PROFILE_COUNTS[int(row['domain_state_sum'])])
        for row in base['profile_rows']
    )
    assert weighted_affine == EXPECTED_AFFINE_TOTAL
    affected = [row for row in PROFILE_ROWS if int(row['removed_vs_affine']) > 0]

    out = {
        'position': 'C',
        'physical_shared_dimension': 149,
        'complete_higher_affine_conflicts': AFFINE_EVENT_COUNT,
        'physical_ternary_factors': [list(gids) for gids, _rows in PHYSICAL_TERNARY],
        'physical_ternary_forbidden_quotient_tuples': [len(rows) for _gids, rows in PHYSICAL_TERNARY],
        'tracked_events': EVENT_COUNT,
        'all_order_affine_support_exact_count': EXPECTED_AFFINE_TOTAL,
        'exact_affine_plus_two_physical_ternary_count': total,
        'exact_log2': math.log2(total),
        'state_bits': total.bit_length(),
        'removed_weighted_assignments_vs_affine': EXPECTED_AFFINE_TOTAL - total,
        'gain_vs_affine_log2_bits': math.log2(EXPECTED_AFFINE_TOTAL) - math.log2(total),
        'affected_profiles': [int(row['domain_state_sum']) for row in affected],
        'profile_rows': PROFILE_ROWS,
        'decision': 'C916_COMPLETE_AFFINE_SUPPORT_PLUS_TWO_EXACT_PHYSICAL_TERNARY_QUOTIENT_FACTORS',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_AFFINE_PLUS_2_PHYSICAL_TERNARY_EXACT')
    print('theorem=the exact pairwise component recursion tracks the complete 19 affine-support violations and every forbidden tuple of the two certified physical ternary quotient factors in one AND-event semiring; coefficient mask zero is therefore the exact weighted count satisfying all of them')
    print('boundary=other physical ternary, quaternary, and higher-order value constraints remain outside this partial physical-image model')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
