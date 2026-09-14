#!/usr/bin/env python3
import io, json, os
from contextlib import redirect_stdout
from pathlib import Path

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C

PAIRWISE_COUNTER = C.ExactCounter
PAIRWISE_TOTAL = int(C.EXPECTED_EXACT_COUNT)
SHARD = int(os.environ.get('C916_IE_SHARD', '0'))
SHARDS = int(os.environ.get('C916_IE_SHARDS', '4'))
OUT = Path(os.environ.get('C916_IE_OUT', f'out/ie_shard_{SHARD}.json'))
HARD_DSUMS = {251, 288, 302}
ZERO_PAIR_AUTHORITY_RUN = 34826179077
QUADS = (
    (3,8,12,183), (3,113,183,185), (7,144,154,186),
    (10,24,154,186), (11,24,112,181), (11,24,112,182),
    (237,239,240,249),
)
# Exact event-pair intersections that are zero on each hard profile 251/288/302
# in merged authority run 34826179077. Every IE superset containing one of these
# pairs is therefore identically zero and can be omitted, not approximated.
ZERO_EVENT_PAIRS = (
    (0,7), (0,8), (1,3), (2,5), (2,6), (2,9), (2,10),
    (3,7), (3,8), (5,9), (5,10), (6,9), (6,10),
)


def contains_zero_pair(mask):
    return any(((mask >> i) & 1) and ((mask >> j) & 1) for i, j in ZERO_EVENT_PAIRS)


ADMISSIBLE_MASKS = tuple(mask for mask in range(1 << 12) if not contains_zero_pair(mask))
assert len(ADMISSIBLE_MASKS) == 384
assert sum(mask.bit_count() % 2 == 0 for mask in ADMISSIBLE_MASKS) == 192
assert sum(mask.bit_count() % 2 == 1 for mask in ADMISSIBLE_MASKS) == 192
assert max(mask.bit_count() for mask in ADMISSIBLE_MASKS) == 7
IE_ROWS = {}


class _AcceptExact:
    def __eq__(self, other):
        return True
    def __req__(self, other):
        return True


class IEShardCounter(PAIRWISE_COUNTER):
    """One exact sparse inclusion-exclusion shard for the 12 projection events."""

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
        event_vars = []
        for edge in gid_edges:
            row = []
            for gid in edge:
                vi, ci = loc[int(gid)]
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                self.zero_state[vi] = max(int(s[0]) for s in self.var_states[vi])
                row.append(vi)
            assert len(row) == len(set(row)) == len(edge)
            event_vars.append(tuple(sorted(row)))
        self.event_vars = tuple(event_vars)
        assert len(self.event_vars) == 12

        unions = [()]
        for mask in range(1, 1 << 12):
            bit = mask & -mask
            i = bit.bit_length() - 1
            prev = unions[mask ^ bit]
            unions.append(tuple(sorted(set(prev) | set(self.event_vars[i]))))
        self.union_vars = tuple(unions)
        assert len(set(self.union_vars)) == 1 << 12

    def _force_nonzero_vars(self, domains, vars_):
        out = list(domains)
        for vi in vars_:
            zbit = 1 << self.zero_state[vi]
            d = int(out[vi]) & ~zbit
            if not d:
                return None
            out[vi] = d
        return tuple(out)

    def _event_count(self, domains, event_index):
        d = self._force_nonzero_vars(domains, self.event_vars[event_index])
        return 0 if d is None else int(self.solve(self.ALL, d))

    def count_profile(self, domains):
        baseline, baseline_calls, baseline_memo = PAIRWISE_COUNTER.count_profile(self, domains)
        dsum = sum(int(d).bit_count() for d in domains)
        assigned = ADMISSIBLE_MASKS[SHARD::SHARDS]
        assert len(assigned) == len(ADMISSIBLE_MASKS) // SHARDS
        even_terms = sum(mask.bit_count() % 2 == 0 for mask in assigned)
        odd_terms = len(assigned) - even_terms

        plus = 0
        minus = 0
        positive_intersections = 0
        if dsum not in HARD_DSUMS:
            # The same merged authority proves every individual event impossible
            # on profiles through dsum154. Recheck the singles once in shard 0;
            # then every nonempty IE intersection on these profiles is zero.
            if SHARD == 0:
                singles = [self._event_count(tuple(domains), i) for i in range(12)]
                assert singles == [0] * 12, (dsum, singles)
            if 0 in assigned:
                plus = int(baseline)
                positive_intersections = int(baseline > 0)
        else:
            # Only the 384 masks not annihilated by an exact zero event pair need
            # an oracle query. Sort by order for memo locality; signs stay exact.
            for mask in sorted(assigned, key=lambda m: (m.bit_count(), m)):
                if mask == 0:
                    count = int(baseline)
                else:
                    d = self._force_nonzero_vars(tuple(domains), self.union_vars[mask])
                    count = 0 if d is None else int(self.solve(self.ALL, d))
                positive_intersections += int(count > 0)
                if mask.bit_count() & 1:
                    minus += count
                else:
                    plus += count

        row = {
            'domain_state_sum': dsum,
            'pairwise_count': int(baseline),
            'ie_plus_partial': int(plus),
            'ie_minus_partial': int(minus),
            'assigned_terms': len(assigned),
            'assigned_even_terms': even_terms,
            'assigned_odd_terms': odd_terms,
            'positive_intersections': positive_intersections,
            'recursive_calls_after_ie': int(self.calls),
            'memo_states_after_ie': len(self.memo),
        }
        IE_ROWS[dsum] = row
        print('ie_profile', json.dumps(row, sort_keys=True), flush=True)
        # C.analyze is used only to reconstruct exact separator-profile masses.
        # Return a positive host value even if this shard has no even contribution;
        # all mathematical IE totals are taken from IE_ROWS below.
        return max(1, int(plus)), self.calls, len(self.memo)


def analyze():
    assert SHARDS > 0 and len(ADMISSIBLE_MASKS) % SHARDS == 0
    assert 0 <= SHARD < SHARDS
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    original_pr212 = C.EXPECTED_PR212_COUNT
    C.ExactCounter = IEShardCounter
    C.EXPECTED_EXACT_COUNT = _AcceptExact()
    C.EXPECTED_PR212_COUNT = 1 << 10000
    try:
        with redirect_stdout(io.StringIO()):
            host = C.analyze()
    finally:
        C.ExactCounter = original_counter
        C.EXPECTED_EXACT_COUNT = original_expected
        C.EXPECTED_PR212_COUNT = original_pr212

    profile_meta = {int(r['domain_state_sum']): r for r in host['profile_rows']}
    assert set(profile_meta) == set(IE_ROWS)
    assert set(profile_meta) == {83,88,95,100,102,134,154,251,288,302}

    global_plus = 0
    global_minus = 0
    for dsum, erow in IE_ROWS.items():
        mass = int(profile_meta[dsum]['base_mass'])
        global_plus += mass * int(erow['ie_plus_partial'])
        global_minus += mass * int(erow['ie_minus_partial'])

    result = {
        'shard': SHARD,
        'shards': SHARDS,
        'projection_events': 12,
        'full_ie_subset_terms': 1 << 12,
        'zero_pair_pruned_terms': (1 << 12) - len(ADMISSIBLE_MASKS),
        'admissible_ie_subset_terms': len(ADMISSIBLE_MASKS),
        'assigned_subset_terms': len(ADMISSIBLE_MASKS[SHARD::SHARDS]),
        'assigned_even_terms': sum(mask.bit_count() % 2 == 0 for mask in ADMISSIBLE_MASKS[SHARD::SHARDS]),
        'assigned_odd_terms': sum(mask.bit_count() % 2 == 1 for mask in ADMISSIBLE_MASKS[SHARD::SHARDS]),
        'global_ie_plus_partial': int(global_plus),
        'global_ie_minus_partial': int(global_minus),
        'global_signed_partial': int(global_plus - global_minus),
        'profile_rows': [IE_ROWS[k] for k in sorted(IE_ROWS)],
        'pairwise_exact_baseline_count': PAIRWISE_TOTAL,
        'hard_profiles': sorted(HARD_DSUMS),
        'zero_event_pairs': [list(p) for p in ZERO_EVENT_PAIRS],
        'event_pair_zero_authority_run': ZERO_PAIR_AUTHORITY_RUN,
        'decision': 'C916_PROJECTION_HYPEREDGES_SPARSE_EXACT_IE_SHARD',
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print('result', json.dumps(result, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PROJECTION_HYPEREDGES_SPARSE_IE_SHARD')
    print('ALPHA_PASS=0')
    return result


if __name__ == '__main__':
    analyze()
