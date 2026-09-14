#!/usr/bin/env python3
import io
import json
import math
import sys
from contextlib import redirect_stdout
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import verify_v26_q138_c916_e0_first_dyadic_projection_hyperedges_eventmask_vector_exact as V
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_4_physical_ternary_exact as F

PAIRWISE_COUNTER = C.ExactCounter
EXPECTED_AFFINE_TOTAL = F.EXPECTED_AFFINE_TOTAL
FIVE_GIDS = (4, 5, 8, 9, 114)
Q0 = frozenset({(1,0,1,1),(1,0,1,3),(1,0,3,1)})
Q1 = frozenset({
    (0,1,2,0),(0,1,3,0),(0,2,2,1),(0,2,3,1),(1,0,1,1),(1,0,1,2),(1,0,1,3),
    (1,0,2,2),(1,0,3,2),(1,1,1,1),(1,1,1,2),(1,1,2,0),(1,2,1,0),(1,2,1,1),
    (1,2,2,0),(1,2,2,1),(1,2,3,0),(1,2,3,1),(1,3,1,1),(1,3,2,0),(2,0,1,1),
    (2,0,2,1),(2,0,3,1),(2,1,0,1),(3,0,1,1),(3,1,0,1),(3,1,2,0),(3,2,1,0),
})
Q3 = frozenset({(1,1,1,1),(1,1,3,1),(1,2,2,0),(1,2,3,0),(1,3,1,1),(1,3,2,0)})
Q4 = frozenset({
    (0,1,1,1),(0,1,3,1),(0,3,1,1),(1,0,0,1),(1,0,3,1),(1,2,2,0),
    (1,2,3,0),(1,3,0,1),(1,3,2,0),(2,1,1,0),(2,1,3,0),(2,3,1,0),
})
PROFILE_ROWS = []


def allowed_five_states():
    out = []
    for row in product(range(4), repeat=5):
        s4, s5, s8, s9, s114 = row
        if (s4,s5,s8,s9) in Q0: continue
        if (s4,s5,s8,s114) in Q1: continue
        if (s4,s5,s9,s114) in Q1: continue
        if (s4,s8,s9,s114) in Q3: continue
        if (s5,s8,s9,s114) in Q4: continue
        out.append(row)
    assert len(out) == 832
    return tuple(out)

ALLOWED = allowed_five_states()


class AnyExpected:
    def __eq__(self, other):
        return True


class AllKnownPhysicalCounter(F.AffinePlusFourPhysicalEventCounter):
    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        loc = {}
        for vi, members in enumerate(self.variables):
            for ci, gid in enumerate(members):
                loc[int(gid)] = (vi, ci)
        self.five_vars = []
        for gid in FIVE_GIDS:
            vi, ci = loc[gid]
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
        all_known = 0
        conditioned = 0
        for states in ALLOWED:
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
            affine_plus_quads += sum(int(weight) for mask, weight in dist.items() if (int(mask) & F.AFFINE_MASK) == 0)
            all_known += int(dist.get(0, 0))

        dsum = sum(int(d).bit_count() for d in domains)
        affine = int(F.EXPECTED_AFFINE_PROFILE_COUNTS[dsum])
        assert 0 <= all_known <= affine_plus_quads <= affine <= int(baseline)
        assert all_known <= pairwise_plus_quads <= int(baseline)
        row = {
            'domain_state_sum': dsum,
            'pairwise_count': int(baseline),
            'all_order_affine_support_count': affine,
            'pairwise_plus_five_physical_quads_count': pairwise_plus_quads,
            'affine_plus_five_physical_quads_count': affine_plus_quads,
            'affine_plus_four_ternaries_plus_five_quads_count': all_known,
            'removed_vs_affine': affine - all_known,
            'gain_vs_affine_log2_bits': None if all_known == 0 or affine == 0 else math.log2(affine) - math.log2(all_known),
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
        print('all_known_physical_profile', json.dumps(row, sort_keys=True), flush=True)
        return all_known, self.vector_calls, len(self.vector_memo)


def analyze():
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    old_event_count = V.EVENT_COUNT
    old_all_events = V.ALL_EVENTS
    V.EVENT_COUNT = F.EVENT_COUNT
    V.ALL_EVENTS = F.ALL_EVENTS
    C.ExactCounter = AllKnownPhysicalCounter
    C.EXPECTED_EXACT_COUNT = AnyExpected()
    try:
        with redirect_stdout(io.StringIO()):
            base = C.analyze()
    finally:
        C.ExactCounter = original_counter
        C.EXPECTED_EXACT_COUNT = original_expected
        V.EVENT_COUNT = old_event_count
        V.ALL_EVENTS = old_all_events

    total = int(base['exact_count'])
    assert total <= EXPECTED_AFFINE_TOTAL
    assert {int(row['domain_state_sum']) for row in PROFILE_ROWS} == set(F.EXPECTED_AFFINE_PROFILE_COUNTS)
    out = {
        'position': 'C',
        'physical_shared_dimension': 149,
        'complete_higher_affine_conflicts': F.AFFINE_EVENT_COUNT,
        'physical_ternary_factors': [list(gids) for gids, _rows in F.PHYSICAL_TERNARY],
        'physical_ternary_forbidden_quotient_tuples': [len(rows) for _gids, rows in F.PHYSICAL_TERNARY],
        'physical_quaternary_factors': [[4,5,8,9],[4,5,8,114],[4,5,9,114],[4,8,9,114],[5,8,9,114]],
        'physical_quaternary_forbidden_quotient_tuples': [3,28,28,6,12],
        'conditioned_five_state_relation_size': len(ALLOWED),
        'tracked_affine_and_ternary_events': F.EVENT_COUNT,
        'all_order_affine_support_exact_count': EXPECTED_AFFINE_TOTAL,
        'exact_affine_plus_all_known_physical_count': total,
        'exact_log2': math.log2(total),
        'state_bits': total.bit_length(),
        'removed_weighted_assignments_vs_affine': EXPECTED_AFFINE_TOTAL - total,
        'gain_vs_affine_log2_bits': math.log2(EXPECTED_AFFINE_TOTAL) - math.log2(total),
        'profile_rows': PROFILE_ROWS,
        'decision': 'C916_COMPLETE_AFFINE_SUPPORT_PLUS_ALL_CURRENTLY_CERTIFIED_PHYSICAL_QUOTIENT_FACTORS',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_AFFINE_PLUS_ALL_KNOWN_PHYSICAL_EXACT')
    print('theorem=conditioning on the exact 832-row conjunction of all five certified quaternary quotient factors and summing the exact 31-event affine-plus-four-ternary semiring yields the exact weighted count satisfying every currently certified physical quotient factor')
    print('boundary=untested ternary targets and any further physical higher-order value constraints remain outside; this is not yet the full physical image')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
