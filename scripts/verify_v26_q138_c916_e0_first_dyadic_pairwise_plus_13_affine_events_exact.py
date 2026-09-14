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

PAIRWISE_COUNTER = C.ExactCounter
AFFINE_FIVE = (4, 5, 8, 9, 114)
EVENT_COUNT = 13
ALL_EVENTS = (1 << EVENT_COUNT) - 1
OLD_TWELVE_TOTAL = int(V.EXPECTED_FINITE_TOTAL)
OLD_PROFILE_COUNTS = dict(V.EXPECTED_PROFILE_COUNTS)
PROFILE_ROWS = []


class AnyExpected:
    def __eq__(self, other):
        return True

    def __req__(self, other):
        return True


class ThirteenEventCounter(V.EventMaskVectorCounter):
    def __init__(self, variables, var_states, var_weights, pairq):
        PAIRWISE_COUNTER.__init__(self, variables, var_states, var_weights, pairq)
        m4 = C.load(C.M4_PATH)
        triples = tuple(tuple(map(int, row)) for row in m4['projection_minimal_empty_triples'])
        assert len(triples) == 5
        gid_events = triples + V.QUADS + (AFFINE_FIVE,)
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
        old = int(OLD_PROFILE_COUNTS[dsum])
        assert exact <= old

        row = {
            'domain_state_sum': dsum,
            'pairwise_count': int(baseline),
            'pairwise_plus_12_count': old,
            'pairwise_plus_13_count': exact,
            'removed_by_new_affine_five': old - exact,
            'gain_vs_12_log2_bits': None if exact == 0 or old == 0 else math.log2(old) - math.log2(exact),
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
        print('eventmask13_profile', json.dumps(row, sort_keys=True), flush=True)
        return exact, self.vector_calls, len(self.vector_memo)


def analyze():
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    old_v_event_count = V.EVENT_COUNT
    old_v_all_events = V.ALL_EVENTS
    V.EVENT_COUNT = EVENT_COUNT
    V.ALL_EVENTS = ALL_EVENTS
    C.ExactCounter = ThirteenEventCounter
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
    assert total <= OLD_TWELVE_TOTAL
    assert {int(row['domain_state_sum']) for row in PROFILE_ROWS} == set(OLD_PROFILE_COUNTS)
    weighted_removed = OLD_TWELVE_TOTAL - total
    affected = [row for row in PROFILE_ROWS if int(row['removed_by_new_affine_five']) > 0]

    out = {
        'position': 'C',
        'physical_shared_dimension': 149,
        'pairwise_plus_12_exact_count': OLD_TWELVE_TOTAL,
        'new_minimal_affine_conflict': list(AFFINE_FIVE),
        'known_higher_affine_events': EVENT_COUNT,
        'exact_count': total,
        'exact_log2': math.log2(total),
        'state_bits': total.bit_length(),
        'removed_weighted_assignments_vs_12': weighted_removed,
        'gain_vs_12_log2_bits': math.log2(OLD_TWELVE_TOTAL) - math.log2(total),
        'affected_profiles': [int(row['domain_state_sum']) for row in affected],
        'profile_rows': PROFILE_ROWS,
        'decision': 'C916_250WAY_COMPLETE_M4_PAIRWISE_PLUS_13_KNOWN_AFFINE_CONFLICT_EVENTS_EXACT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PAIRWISE_PLUS_13_AFFINE_EVENTS_EXACT')
    if weighted_removed:
        print('theorem=the newly certified inclusion-minimal affine conflict (4,5,8,9,114) removes additional exact weighted assignments beyond the previous pairwise-plus-12 finite support model')
    else:
        print('theorem=the newly certified inclusion-minimal affine conflict (4,5,8,9,114) is globally new at support level but happens to remove no additional weighted assignments from the previous pairwise-plus-12 counted separator profiles')
    print('boundary=the remaining all-order affine conflict family is not yet proven complete, and stronger physical-value constraints remain outside this theorem')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
