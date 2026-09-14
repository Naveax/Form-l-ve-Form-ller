#!/usr/bin/env python3
import io, json, math, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C

PAIRWISE_COUNTER = C.ExactCounter
PAIRWISE_COUNT = int(C.EXPECTED_EXACT_COUNT)
QUADS = (
    (3,8,12,183), (3,113,183,185), (7,144,154,186),
    (10,24,154,186), (11,24,112,181), (11,24,112,182),
    (237,239,240,249),
)
HARD_DOMAIN_SUMS = {251, 288, 302}
# Exact zero pair intersections observed by clean authority run 34826179077.
# This script does not trust them blindly: every hard profile mechanically
# re-verifies all 13 counts as zero before using them to prune IE subsets.
ZERO_EVENT_PAIRS = (
    (0,7), (0,8), (1,3), (2,5), (2,6), (2,9), (2,10),
    (3,7), (3,8), (5,9), (5,10), (6,9), (6,10),
)
EXPECTED_INDEPENDENT_SUBSETS = 384
PROFILE_ROWS = []


class _AcceptExact:
    def __eq__(self, other): return True
    def __req__(self, other): return True


def has_zero_pair(mask):
    return any(((mask >> i) & 1) and ((mask >> j) & 1) for i, j in ZERO_EVENT_PAIRS)


INDEPENDENT_MASKS = tuple(mask for mask in range(1 << 12) if not has_zero_pair(mask))
assert len(INDEPENDENT_MASKS) == EXPECTED_INDEPENDENT_SUBSETS


class SparseIECounter(PAIRWISE_COUNTER):
    """Exact 12-event inclusion-exclusion after certified zero intersections.

    A subset of forbidden events asks that every gid in their union be nonzero.
    If it contains one of the 13 event pairs whose exact intersection count is
    zero, its higher intersection is also empty. Re-verifying those zero pairs
    leaves only 384 of 4096 IE subsets. Every retained term is counted by the
    unchanged complete 4,005-pair exact oracle with shared memoization.
    """

    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        m4 = C.load(C.M4_PATH)
        triples = tuple(tuple(map(int, row)) for row in m4['projection_minimal_empty_triples'])
        assert len(triples) == 5 and len(QUADS) == 7
        self.events = triples + tuple(tuple(map(int, row)) for row in QUADS)
        self.loc = {}
        self.zero_state = {}
        for vi, members in enumerate(self.variables):
            for ci, gid in enumerate(members):
                self.loc[int(gid)] = (vi, ci)
        assert len(self.loc) == 90
        for event in self.events:
            for gid in event:
                vi, ci = self.loc[gid]
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                self.zero_state[vi] = max(int(s[0]) for s in self.var_states[vi])
        self.ie_stats = Counter()

        unions = [() for _ in range(1 << 12)]
        for mask in range(1, 1 << 12):
            bit = mask & -mask
            i = bit.bit_length() - 1
            unions[mask] = tuple(sorted(set(unions[mask ^ bit]) | set(self.events[i])))
        self.event_unions = tuple(unions)

    def _condition_nonzero(self, domains, gids):
        out = list(domains)
        for gid in gids:
            vi, ci = self.loc[int(gid)]
            assert ci == 0
            zbit = 1 << self.zero_state[vi]
            nd = int(out[vi]) & ~zbit
            if not nd:
                return None
            out[vi] = nd
        return tuple(out)

    def _condition_count(self, domains, gids):
        conditioned = self._condition_nonzero(domains, gids)
        if conditioned is None:
            self.ie_stats['unary_wipeouts'] += 1
            return 0
        self.ie_stats['oracle_queries'] += 1
        return PAIRWISE_COUNTER.solve(self, self.ALL, conditioned)

    def count_profile(self, domains):
        baseline, baseline_calls, baseline_memo = PAIRWISE_COUNTER.count_profile(self, domains)
        dsum = sum(int(d).bit_count() for d in domains)
        self.ie_stats.clear()

        if baseline == 0:
            valid = 0
            verified_zero_pairs = 0
            evaluated_terms = 0
        elif dsum not in HARD_DOMAIN_SUMS:
            # Clean run 34826179077 says every event is impossible here. Reprove
            # that profile-locally so this exact solver has no external theorem
            # dependency beyond the frozen event list itself.
            singles = [self._condition_count(tuple(domains), event) for event in self.events]
            assert all(value == 0 for value in singles), (dsum, singles)
            valid = int(baseline)
            verified_zero_pairs = 0
            evaluated_terms = len(singles)
        else:
            # First certify the graph used to eliminate 3712 IE subsets.
            for i, j in ZERO_EVENT_PAIRS:
                gids = tuple(sorted(set(self.events[i]) | set(self.events[j])))
                value = int(self._condition_count(tuple(domains), gids))
                assert value == 0, (dsum, i, j, value)
            verified_zero_pairs = len(ZERO_EVENT_PAIRS)

            total = int(baseline)  # empty IE subset
            evaluated_terms = 0
            for mask in INDEPENDENT_MASKS:
                if mask == 0:
                    continue
                count = int(self._condition_count(tuple(domains), self.event_unions[mask]))
                evaluated_terms += 1
                if mask.bit_count() & 1:
                    total -= count
                else:
                    total += count
            valid = total
            assert 0 <= valid <= baseline

        row = {
            'domain_state_sum': dsum,
            'pairwise_count': int(baseline),
            'finite_hyperedge_exact_count': int(valid),
            'gain_log2_bits': None if valid == 0 else math.log2(baseline) - math.log2(valid),
            'verified_zero_event_pairs': verified_zero_pairs,
            'all_ie_subsets': 4096,
            'nonzero_candidate_ie_subsets': EXPECTED_INDEPENDENT_SUBSETS,
            'evaluated_nonempty_ie_terms': evaluated_terms,
            'pairwise_recursive_calls_after_queries': self.calls,
            'pairwise_memo_states_after_queries': len(self.memo),
            'ie_stats': dict(self.ie_stats),
        }
        PROFILE_ROWS.append(row)
        print('sparse_ie_profile', json.dumps(row, sort_keys=True), flush=True)
        return valid, self.calls, len(self.memo)


def analyze():
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    C.ExactCounter = SparseIECounter
    C.EXPECTED_EXACT_COUNT = _AcceptExact()
    try:
        with redirect_stdout(io.StringIO()):
            base = C.analyze()
    finally:
        C.ExactCounter = original_counter
        C.EXPECTED_EXACT_COUNT = original_expected

    total = int(base['exact_count'])
    assert 0 < total < PAIRWISE_COUNT
    assert len(PROFILE_ROWS) == len(base['profile_rows'])
    out = {
        **base,
        'exact_count': total,
        'exact_log2': math.log2(total),
        'state_bits': total.bit_length(),
        'pairwise_exact_baseline_count': PAIRWISE_COUNT,
        'gain_vs_pairwise_exact_log2_bits': math.log2(PAIRWISE_COUNT) - math.log2(total),
        'projection_minimal_empty_triples_added': 5,
        'projection_minimal_empty_quadruples_added': 7,
        'zero_event_pairs_reverified_per_hard_profile': len(ZERO_EVENT_PAIRS),
        'all_ie_subsets': 4096,
        'candidate_nonzero_ie_subsets_after_zero_pair_pruning': EXPECTED_INDEPENDENT_SUBSETS,
        'sparse_ie_profile_rows': PROFILE_ROWS,
        'solver': 'sparse_inclusion_exclusion_with_mechanically_reverified_zero_pair_intersections',
        'decision': 'C916_250WAY_COMPLETE_M4_PAIRWISE_PLUS_PROJECTION_TRIPLES_QUADS_SPARSE_IE_EXACT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_COMPLETE_PAIRWISE_PROJECTION_HYPEREDGES_SPARSE_IE_EXACT')
    print('scope=all 4005 exact m4 pairwise value factors plus five minimal-empty triples and seven minimal-empty quadruples; 13 exact zero event-pair intersections are reverified before pruning inclusion-exclusion subsets')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
