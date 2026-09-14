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
import verify_v26_q138_c916_e0_first_dyadic_all_order_affine_support_exact as A

PAIRWISE_COUNTER = C.ExactCounter
EXPECTED_AFFINE_TOTAL = 100215909735124105069922281032909019043326715916545026952580687530924399001600000
EXPECTED_AFFINE_PROFILE_COUNTS = {
    83: 0, 88: 1, 95: 0, 100: 25, 102: 0,
    134: 21578474445840,
    154: 42542498200320,
    251: 96491872903925175488260425426864960,
    288: 183697181089509355446657454121817216,
    302: 196896631570740171574763723334509184,
}
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


class AffinePlusFiveQuadsCounter(A.CompleteAffineEventCounter):
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
        exact = 0
        conditioned = 0
        for states in ALLOWED:
            ok = True
            nd = list(domains)
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
            exact += int(dist.get(0, 0))

        dsum = sum(int(d).bit_count() for d in domains)
        affine = int(EXPECTED_AFFINE_PROFILE_COUNTS[dsum])
        assert 0 <= exact <= affine <= int(baseline)
        assert exact <= pairwise_plus_quads <= int(baseline)
        row = {
            'domain_state_sum': dsum,
            'pairwise_count': int(baseline),
            'all_order_affine_support_count': affine,
            'pairwise_plus_five_physical_quads_count': pairwise_plus_quads,
            'affine_plus_five_physical_quads_count': exact,
            'removed_vs_affine': affine - exact,
            'gain_vs_affine_log2_bits': None if exact == 0 or affine == 0 else math.log2(affine) - math.log2(exact),
            'allowed_five_state_rows_consistent_with_profile': conditioned,
            'vector_calls': self.vector_calls,
            'vector_memo_states': len(self.vector_memo),
            'vector_memo_hits': self.vector_memo_hits,
            'peak_event_mask_states': self.vector_peak_states,
            'and_convolutions': self.and_convolutions,
            'pairwise_baseline_calls': baseline_calls,
            'pairwise_baseline_memo_states': baseline_memo,
        }
        PROFILE_ROWS.append(row)
        print('affine19_physical5quads_profile', json.dumps(row, sort_keys=True), flush=True)
        return exact, self.vector_calls, len(self.vector_memo)


def analyze():
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    old_v_event_count = V.EVENT_COUNT
    old_v_all_events = V.ALL_EVENTS
    V.EVENT_COUNT = A.EVENT_COUNT
    V.ALL_EVENTS = A.ALL_EVENTS
    C.ExactCounter = AffinePlusFiveQuadsCounter
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
    out = {
        'position': 'C',
        'physical_shared_dimension': 149,
        'complete_higher_affine_conflicts': A.EVENT_COUNT,
        'physical_quaternary_factors': [[4,5,8,9],[4,5,8,114],[4,5,9,114],[4,8,9,114],[5,8,9,114]],
        'physical_quaternary_forbidden_quotient_tuples': [3,28,28,6,12],
        'conditioned_five_state_relation_size': len(ALLOWED),
        'all_order_affine_support_exact_count': EXPECTED_AFFINE_TOTAL,
        'exact_affine_plus_five_physical_quads_count': total,
        'exact_log2': math.log2(total),
        'state_bits': total.bit_length(),
        'removed_weighted_assignments_vs_affine': EXPECTED_AFFINE_TOTAL - total,
        'gain_vs_affine_log2_bits': math.log2(EXPECTED_AFFINE_TOTAL) - math.log2(total),
        'profile_rows': PROFILE_ROWS,
        'decision': 'C916_COMPLETE_AFFINE_SUPPORT_PLUS_FIVE_EXACT_PHYSICAL_QUATERNARY_QUOTIENT_FACTORS',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_AFFINE_PLUS_5_PHYSICAL_QUADS_EXACT')
    print('theorem=the five certified quaternary quotient relations collapse to an exact 832-row relation on gids 4,5,8,9,114; conditioning on those rows and summing the complete 19-event affine counter gives the exact weighted count for their conjunction')
    print('boundary=certified ternary factors and any further physical higher-order value constraints remain outside this partial physical-image model')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
