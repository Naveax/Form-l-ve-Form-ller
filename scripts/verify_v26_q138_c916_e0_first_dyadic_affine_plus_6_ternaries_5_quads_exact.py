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
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_4_physical_ternary_exact as F
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_all_known_physical_exact as H

PAIRWISE_COUNTER = C.ExactCounter
AFFINE_EVENT_COUNT = 19
EXTRA_TERNARY = (
    ((69, 82, 87), ((1, 1, 0), (2, 1, 0), (2, 1, 1))),
    ((130, 131, 132), ((0, 1, 1), (1, 0, 1))),
)
PHYSICAL_TERNARY = F.PHYSICAL_TERNARY + EXTRA_TERNARY
OLD_PHYSICAL_EVENT_COUNT = sum(len(rows) for _gids, rows in F.PHYSICAL_TERNARY)
PHYSICAL_EVENT_COUNT = sum(len(rows) for _gids, rows in PHYSICAL_TERNARY)
EVENT_COUNT = AFFINE_EVENT_COUNT + PHYSICAL_EVENT_COUNT
ALL_EVENTS = (1 << EVENT_COUNT) - 1
AFFINE_MASK = (1 << AFFINE_EVENT_COUNT) - 1
OLD_PHYSICAL_MASK = ((1 << (AFFINE_EVENT_COUNT + OLD_PHYSICAL_EVENT_COUNT)) - 1) ^ AFFINE_MASK
PHYSICAL_MASK = ALL_EVENTS ^ AFFINE_MASK
EXPECTED_AFFINE_TOTAL = F.EXPECTED_AFFINE_TOTAL
EXPECTED_AFFINE_PLUS_QUADS = {
    83: 0,
    88: 1,
    95: 0,
    100: 25,
    102: 0,
    134: 21578474445840,
    154: 42542498200320,
    251: 89907694729452706254683114802680640,
    288: 172756800789534020480516995048636032,
    302: 184499100445926283543514310179195520,
}
EXPECTED_FOUR_TERNARIES_PLUS_QUADS = {
    83: 0,
    88: 1,
    95: 0,
    100: 25,
    102: 0,
    134: 21578474445840,
    154: 42542498200320,
    251: 87639022052873245102889951271577152,
    288: 167100640692156092551072548681523584,
    302: 178525130634609700681252266313472640,
}
PROFILE_ROWS = []


class AnyExpected:
    def __eq__(self, other):
        return True


class SixTernaryFiveQuadCounter(F.AffinePlusFourPhysicalEventCounter):
    """Exact 36-event affine/ternary semiring, conditioned on the five-quad relation."""

    def __init__(self, variables, var_states, var_weights, pairq):
        PAIRWISE_COUNTER.__init__(self, variables, var_states, var_weights, pairq)
        m4 = C.load(C.M4_PATH)
        triples = tuple(tuple(map(int, row)) for row in m4['projection_minimal_empty_triples'])
        assert len(triples) == 5
        affine_events = triples + V.QUADS + (F.A.AFFINE_FIVE,) + F.A.EXTRA_SIX
        assert len(affine_events) == AFFINE_EVENT_COUNT
        assert F.A.Q.digest_rows(tuple(sorted(affine_events, key=lambda r: (len(r), tuple(r))))) == F.A.EXPECTED_CONFLICT_DIGEST

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
                vis.append(vi)
            assert len(set(vis)) == 3
            for raw_row in forbidden_rows:
                row = tuple(map(int, raw_row))
                assert len(row) == 3
                for pos, vi in enumerate(vis):
                    assert 0 <= row[pos] < len(self.var_states[vi]), (gids, row, vi, len(self.var_states[vi]))
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

        self.five_vars = []
        for gid in H.FIVE_GIDS:
            vi, ci = loc[int(gid)]
            assert len(self.variables[vi]) == 1 and ci == 0
            assert len(self.var_states[vi]) == 4
            self.five_vars.append(vi)
        assert len(set(self.five_vars)) == 5
        self.five_vars = tuple(self.five_vars)

    def count_profile(self, domains):
        baseline, baseline_calls, baseline_memo = PAIRWISE_COUNTER.count_profile(self, domains)
        self.vector_memo.clear()
        self.vector_calls = 0
        self.vector_peak_states = 0
        self.and_convolutions = 0
        self.vector_memo_hits = 0

        pairwise_plus_quads = 0
        affine_plus_quads = 0
        old_all_known = 0
        all_six = 0
        conditioned = 0
        for states in H.ALLOWED:
            nd = list(domains)
            ok = True
            for vi, si in zip(self.five_vars, states):
                bit = 1 << si
                if not (int(nd[vi]) & bit):
                    ok = False
                    break
                nd[vi] = bit
            if not ok:
                continue
            conditioned += 1
            dist = self.vector_solve(self.ALL, tuple(nd))
            pairwise_plus_quads += sum(int(weight) for weight in dist.values())
            affine_plus_quads += sum(
                int(weight) for mask, weight in dist.items()
                if (int(mask) & AFFINE_MASK) == 0
            )
            old_all_known += sum(
                int(weight) for mask, weight in dist.items()
                if (int(mask) & (AFFINE_MASK | OLD_PHYSICAL_MASK)) == 0
            )
            all_six += int(dist.get(0, 0))

        dsum = sum(int(d).bit_count() for d in domains)
        affine = int(F.EXPECTED_AFFINE_PROFILE_COUNTS[dsum])
        assert affine_plus_quads == EXPECTED_AFFINE_PLUS_QUADS[dsum], (dsum, affine_plus_quads)
        assert old_all_known == EXPECTED_FOUR_TERNARIES_PLUS_QUADS[dsum], (dsum, old_all_known)
        assert 0 <= all_six <= old_all_known <= affine_plus_quads <= affine <= int(baseline)
        assert all_six <= pairwise_plus_quads <= int(baseline)

        row = {
            'domain_state_sum': dsum,
            'pairwise_count': int(baseline),
            'all_order_affine_support_count': affine,
            'pairwise_plus_five_physical_quads_count': pairwise_plus_quads,
            'affine_plus_five_physical_quads_count': affine_plus_quads,
            'affine_plus_first_four_ternaries_plus_five_quads_count': old_all_known,
            'affine_plus_six_ternaries_plus_five_quads_count': all_six,
            'removed_vs_previous_four_ternary_checkpoint': old_all_known - all_six,
            'removed_vs_affine': affine - all_six,
            'gain_vs_affine_log2_bits': None if all_six == 0 or affine == 0 else math.log2(affine) - math.log2(all_six),
            'allowed_five_state_rows_consistent_with_profile': conditioned,
            'positive_event_masks_peak': self.vector_peak_states,
            'vector_calls': self.vector_calls,
            'vector_memo_states': len(self.vector_memo),
            'vector_memo_hits': self.vector_memo_hits,
            'and_convolutions': self.and_convolutions,
            'pairwise_baseline_calls': baseline_calls,
            'pairwise_baseline_memo_states': baseline_memo,
        }
        PROFILE_ROWS.append(row)
        print('six_ternary_five_quad_profile', json.dumps(row, sort_keys=True), flush=True)
        return all_six, self.vector_calls, len(self.vector_memo)


def analyze():
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    old_v_event_count = V.EVENT_COUNT
    old_v_all_events = V.ALL_EVENTS
    old_f_event_count = F.EVENT_COUNT
    old_f_all_events = F.ALL_EVENTS
    old_f_phys_count = F.PHYSICAL_EVENT_COUNT
    old_f_phys_mask = F.PHYSICAL_MASK

    V.EVENT_COUNT = EVENT_COUNT
    V.ALL_EVENTS = ALL_EVENTS
    F.EVENT_COUNT = EVENT_COUNT
    F.ALL_EVENTS = ALL_EVENTS
    F.PHYSICAL_EVENT_COUNT = PHYSICAL_EVENT_COUNT
    F.PHYSICAL_MASK = PHYSICAL_MASK
    C.ExactCounter = SixTernaryFiveQuadCounter
    C.EXPECTED_EXACT_COUNT = AnyExpected()
    try:
        with redirect_stdout(io.StringIO()):
            base = C.analyze()
    finally:
        C.ExactCounter = original_counter
        C.EXPECTED_EXACT_COUNT = original_expected
        V.EVENT_COUNT = old_v_event_count
        V.ALL_EVENTS = old_v_all_events
        F.EVENT_COUNT = old_f_event_count
        F.ALL_EVENTS = old_f_all_events
        F.PHYSICAL_EVENT_COUNT = old_f_phys_count
        F.PHYSICAL_MASK = old_f_phys_mask

    total = int(base['exact_count'])
    previous_total = 90987190266267462495475398124505539992830544680017055400806207198697839001600000
    assert total <= previous_total <= EXPECTED_AFFINE_TOTAL
    assert {int(row['domain_state_sum']) for row in PROFILE_ROWS} == set(F.EXPECTED_AFFINE_PROFILE_COUNTS)
    affected_new = [row for row in PROFILE_ROWS if int(row['removed_vs_previous_four_ternary_checkpoint']) > 0]
    out = {
        'position': 'C',
        'physical_shared_dimension': 149,
        'complete_higher_affine_conflicts': AFFINE_EVENT_COUNT,
        'physical_ternary_factors': [list(gids) for gids, _rows in PHYSICAL_TERNARY],
        'physical_ternary_forbidden_quotient_tuples': [len(rows) for _gids, rows in PHYSICAL_TERNARY],
        'physical_quaternary_factors': [[4,5,8,9],[4,5,8,114],[4,5,9,114],[4,8,9,114],[5,8,9,114]],
        'physical_quaternary_forbidden_quotient_tuples': [3,28,28,6,12],
        'conditioned_five_state_relation_size': len(H.ALLOWED),
        'tracked_affine_and_ternary_events': EVENT_COUNT,
        'previous_four_ternary_five_quad_exact_count': previous_total,
        'all_order_affine_support_exact_count': EXPECTED_AFFINE_TOTAL,
        'exact_affine_plus_six_ternaries_plus_five_quads_count': total,
        'exact_log2': math.log2(total),
        'state_bits': total.bit_length(),
        'removed_weighted_assignments_vs_previous_checkpoint': previous_total - total,
        'removed_weighted_assignments_vs_affine': EXPECTED_AFFINE_TOTAL - total,
        'gain_vs_affine_log2_bits': math.log2(EXPECTED_AFFINE_TOTAL) - math.log2(total),
        'newly_affected_profiles': [int(row['domain_state_sum']) for row in affected_new],
        'profile_rows': PROFILE_ROWS,
        'decision': 'C916_COMPLETE_AFFINE_SUPPORT_PLUS_SIX_EXACT_TERNARY_AND_FIVE_EXACT_QUATERNARY_PHYSICAL_QUOTIENT_FACTORS',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_AFFINE_PLUS_6_TERNARIES_5_QUADS_EXACT')
    print('theorem=the five certified quaternary quotient factors are conditioned exactly while one 36-event AND semiring tracks all 19 affine conflicts and all 17 forbidden tuples from the six certified ternary physical quotient factors, including the five-state endpoint of gid 82')
    print('boundary=untested ternary targets and any further physical higher-order value constraints remain outside; this is not yet the full physical image')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
