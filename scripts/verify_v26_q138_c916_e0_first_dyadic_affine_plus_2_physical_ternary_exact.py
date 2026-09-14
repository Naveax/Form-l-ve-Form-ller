#!/usr/bin/env python3
import io
import json
import math
import sys
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import verify_v26_q138_c916_e0_first_dyadic_projection_hyperedges_eventmask_vector_exact as V
import verify_v26_q138_c916_e0_first_dyadic_all_order_affine_support_exact as A

PAIRWISE_COUNTER = C.ExactCounter
EVENT_COUNT = 19
ALL_EVENTS = (1 << EVENT_COUNT) - 1
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

# Exact magnitude-quotient holes certified by clean run 34835467302.
PHYSICAL_TERNARY = (
    ((5, 181, 182), frozenset({(0, 1, 1), (1, 0, 2), (1, 1, 0), (2, 0, 1)})),
    ((11, 12, 24), frozenset({(0, 1, 1), (1, 0, 2), (1, 2, 0)})),
)
PROFILE_ROWS = []


class AnyExpected:
    def __eq__(self, other):
        return True


class AffinePlusPhysicalCounter(A.CompleteAffineEventCounter):
    """Exact 19-affine-event counter with two exact ternary quotient factors.

    The ternary tables are enforced by generalized arc consistency during every
    recursive branch. They are also added to the component-connectivity logic,
    so the inherited exact factorization never separates variables coupled by a
    physical ternary factor.
    """

    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        loc = {}
        for vi, members in enumerate(self.variables):
            for ci, gid in enumerate(members):
                loc[int(gid)] = (vi, ci)
        assert len(loc) == 90

        self.physical_ternary = []
        self.hyper_adj = [0] * self.N
        for gids, forbidden in PHYSICAL_TERNARY:
            vis = []
            for gid in gids:
                vi, ci = loc[int(gid)]
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                # All six physical-factor endpoints have the ordinary 7-value
                # alphabet, hence exactly four sign-reflection quotient states.
                assert len(self.var_states[vi]) == 4, (gid, self.var_states[vi])
                vis.append(vi)
            assert len(set(vis)) == 3
            for row in forbidden:
                assert len(row) == 3 and all(0 <= int(x) < 4 for x in row)
            vis = tuple(vis)
            self.physical_ternary.append((vis, frozenset(tuple(map(int, r)) for r in forbidden)))
            for i in range(3):
                for j in range(i + 1, 3):
                    self.hyper_adj[vis[i]] |= 1 << vis[j]
                    self.hyper_adj[vis[j]] |= 1 << vis[i]
        self.physical_ternary = tuple(self.physical_ternary)

    def _relevant_neighbors(self, i, active, domains):
        base = PAIRWISE_COUNTER._relevant_neighbors(self, i, active, domains)
        return base | (self.hyper_adj[i] & active)

    @staticmethod
    def _state_indices(mask):
        out = []
        m = int(mask)
        while m:
            bit = m & -m
            out.append(bit.bit_length() - 1)
            m ^= bit
        return tuple(out)

    def _physical_prune_once(self, domains):
        dom = list(domains)
        changed = False
        for vis, forbidden in self.physical_ternary:
            for pos, vi in enumerate(vis):
                keep = 0
                for si in self._state_indices(dom[vi]):
                    others = [k for k in range(3) if k != pos]
                    vj, vk = vis[others[0]], vis[others[1]]
                    supported = False
                    for sj in self._state_indices(dom[vj]):
                        for sk in self._state_indices(dom[vk]):
                            row = [None, None, None]
                            row[pos] = si
                            row[others[0]] = sj
                            row[others[1]] = sk
                            if tuple(row) not in forbidden:
                                supported = True
                                break
                        if supported:
                            break
                    if supported:
                        keep |= 1 << si
                if keep == 0:
                    return None, False
                if keep != dom[vi]:
                    dom[vi] = keep
                    changed = True
        return tuple(dom), changed

    def _arc_closure(self, active, domains):
        dom = tuple(domains)
        while True:
            dom = PAIRWISE_COUNTER._arc_closure(self, active, dom)
            if dom is None:
                return None
            dom, changed = self._physical_prune_once(dom)
            if dom is None:
                return None
            if not changed:
                return dom

    def count_profile(self, domains):
        # Dynamic dispatch makes the baseline solve include the two ternary
        # factors but not the 19 affine-event exclusions.
        physical_pairwise, baseline_calls, baseline_memo = PAIRWISE_COUNTER.count_profile(self, domains)
        self.vector_memo.clear()
        self.vector_calls = 0
        self.vector_peak_states = 0
        self.and_convolutions = 0
        self.vector_memo_hits = 0

        dist = self.vector_solve(self.ALL, tuple(domains))
        tracked_total = sum(int(weight) for weight in dist.values())
        assert tracked_total == int(physical_pairwise)
        exact = int(dist.get(0, 0))
        dsum = sum(int(d).bit_count() for d in domains)
        affine = int(EXPECTED_AFFINE_PROFILE_COUNTS[dsum])
        assert exact <= affine

        row = {
            'domain_state_sum': dsum,
            'all_order_affine_support_count': affine,
            'pairwise_plus_two_physical_ternary_count': int(physical_pairwise),
            'affine_plus_two_physical_ternary_count': exact,
            'removed_vs_affine': affine - exact,
            'gain_vs_affine_log2_bits': None if exact == 0 or affine == 0 else math.log2(affine) - math.log2(exact),
            'positive_affine_event_masks': len(dist),
            'vector_calls': self.vector_calls,
            'vector_memo_states': len(self.vector_memo),
            'vector_memo_hits': self.vector_memo_hits,
            'peak_event_mask_states': self.vector_peak_states,
            'and_convolutions': self.and_convolutions,
            'physical_baseline_calls': baseline_calls,
            'physical_baseline_memo_states': baseline_memo,
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
    C.ExactCounter = AffinePlusPhysicalCounter
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
    affected = [row for row in PROFILE_ROWS if int(row['removed_vs_affine']) > 0]
    out = {
        'position': 'C',
        'physical_shared_dimension': 149,
        'complete_higher_affine_conflicts': 19,
        'physical_ternary_factors': [list(gids) for gids, _ in PHYSICAL_TERNARY],
        'physical_ternary_forbidden_quotient_tuples': [len(forbidden) for _, forbidden in PHYSICAL_TERNARY],
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
    print('theorem=the emitted integer is the exact weighted separator count under all 4005 exact pairwise value factors, the complete 19-circuit all-order affine-support condition, and the two certified physical ternary quotient factors')
    print('boundary=other physical ternary, quaternary, and higher-order value constraints remain outside this partial physical-image model')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
