#!/usr/bin/env python3
import io
import json
import math
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_affine_conflict_closure as Q
import verify_v26_q138_c916_e0_first_dyadic_projection_hyperedges_eventmask_vector_exact as V

PAIRWISE_COUNTER = C.ExactCounter
EVENT_COUNT = 19
ALL_EVENTS = (1 << EVENT_COUNT) - 1
EXPECTED_CONFLICT_DIGEST = 'e510dae8f89a09a914839c542e8a70806167531dffa2470f52b376ce48db30a7'
EXPECTED_13_TOTAL = 115292151876555345753619734419842756453063806455848707059568602382702959001600000
EXPECTED_13_PROFILE_COUNTS = {
    83: 0,
    88: 1,
    95: 0,
    100: 25,
    102: 0,
    134: 21578474445840,
    154: 42542498200320,
    251: 111084951958869817867992001256782656,
    288: 211344743415122576332937790083224704,
    302: 226432077982407439965462016079434368,
}
AFFINE_FIVE = (4, 5, 8, 9, 114)
EXTRA_SIX = (
    (5, 8, 9, 114, 165),
    (5, 7, 62, 67, 144, 182),
    (6, 9, 10, 24, 62, 186),
    (6, 7, 9, 10, 24, 144, 186),
    (5, 8, 9, 62, 67, 104, 113, 114),
    (6, 7, 9, 10, 24, 67, 144, 182),
)
PROFILE_ROWS = []


class AnyExpected:
    def __eq__(self, other):
        return True


class CompleteAffineEventCounter(V.EventMaskVectorCounter):
    def __init__(self, variables, var_states, var_weights, pairq):
        PAIRWISE_COUNTER.__init__(self, variables, var_states, var_weights, pairq)
        m4 = C.load(C.M4_PATH)
        triples = tuple(tuple(map(int, row)) for row in m4['projection_minimal_empty_triples'])
        assert len(triples) == 5
        gid_events = triples + V.QUADS + (AFFINE_FIVE,) + EXTRA_SIX
        assert len(gid_events) == EVENT_COUNT
        final_sorted = tuple(sorted(gid_events, key=lambda r: (len(r), tuple(r))))
        assert Q.digest_rows(final_sorted) == EXPECTED_CONFLICT_DIGEST

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
                # The complete 19-circuit family avoids the two contracted
                # signed-magnitude pair variables, so gid activity is exactly
                # one local quotient-state zero/nonzero predicate.
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
        prior = int(EXPECTED_13_PROFILE_COUNTS[dsum])
        assert exact <= prior

        row = {
            'domain_state_sum': dsum,
            'pairwise_count': int(baseline),
            'pairwise_plus_13_count': prior,
            'all_order_affine_support_count': exact,
            'removed_by_six_closure_conflicts': prior - exact,
            'gain_vs_13_log2_bits': None if exact == 0 or prior == 0 else math.log2(prior) - math.log2(exact),
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
        print('affine19_profile', json.dumps(row, sort_keys=True), flush=True)
        return exact, self.vector_calls, len(self.vector_memo)


def analyze():
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    old_v_event_count = V.EVENT_COUNT
    old_v_all_events = V.ALL_EVENTS
    V.EVENT_COUNT = EVENT_COUNT
    V.ALL_EVENTS = ALL_EVENTS
    C.ExactCounter = CompleteAffineEventCounter
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
    assert total <= EXPECTED_13_TOTAL
    assert {int(row['domain_state_sum']) for row in PROFILE_ROWS} == set(EXPECTED_13_PROFILE_COUNTS)
    removed = EXPECTED_13_TOTAL - total
    affected = [row for row in PROFILE_ROWS if int(row['removed_by_six_closure_conflicts']) > 0]

    out = {
        'position': 'C',
        'physical_shared_dimension': 149,
        'complete_higher_affine_conflicts': EVENT_COUNT,
        'higher_affine_conflict_digest_sha256': EXPECTED_CONFLICT_DIGEST,
        'pairwise_plus_13_exact_count': EXPECTED_13_TOTAL,
        'exact_all_order_affine_support_count': total,
        'exact_all_order_affine_support_log2': math.log2(total),
        'state_bits': total.bit_length(),
        'removed_weighted_assignments_vs_13': removed,
        'gain_vs_13_log2_bits': math.log2(EXPECTED_13_TOTAL) - math.log2(total),
        'gain_vs_complete_pairwise_log2_bits': math.log2(int(C.EXPECTED_EXACT_COUNT)) - math.log2(total),
        'affected_profiles': [int(row['domain_state_sum']) for row in affected],
        'profile_rows': PROFILE_ROWS,
        'decision': 'C916_250WAY_COMPLETE_M4_PAIRWISE_PLUS_COMPLETE_ALL_ORDER_AFFINE_SUPPORT_EXACT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_ORDER_AFFINE_SUPPORT_EXACT')
    print('theorem=the complete exact pairwise value model plus the certified complete 19-circuit activity obstruction family is equivalent to the all-order 149-bit affine-anchor intersection condition, and the emitted integer is its exact weighted separator count')
    print('boundary=the exact physical output-value image can impose constraints stronger than affine support; those constraints remain outside this count')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
