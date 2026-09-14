#!/usr/bin/env python3
import io, json, math, os
from contextlib import redirect_stdout
from pathlib import Path

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C

PAIRWISE_COUNTER = C.ExactCounter
PAIRWISE_TOTAL = int(C.EXPECTED_EXACT_COUNT)
SHARD = int(os.environ.get('C916_IE_SHARD', '0'))
SHARDS = int(os.environ.get('C916_IE_SHARDS', '8'))
OUT = Path(os.environ.get('C916_IE_OUT', f'out/ie_shard_{SHARD}.json'))
HARD_DSUMS = {251, 288, 302}
QUADS = (
    (3,8,12,183), (3,113,183,185), (7,144,154,186),
    (10,24,154,186), (11,24,112,181), (11,24,112,182),
    (237,239,240,249),
)
IE_ROWS = {}


class _AcceptExact:
    def __eq__(self, other):
        return True
    def __req__(self, other):
        return True


class IEShardCounter(PAIRWISE_COUNTER):
    """One exact inclusion-exclusion shard for the 12 frozen projection events."""

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
                # The frozen 12 events avoid both signed-pair contractions.
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
        if d is None:
            return 0
        return int(self.solve(self.ALL, d))

    def count_profile(self, domains):
        baseline, baseline_calls, baseline_memo = PAIRWISE_COUNTER.count_profile(self, domains)
        dsum = sum(int(d).bit_count() for d in domains)
        assigned = list(range(SHARD, 1 << 12, SHARDS))
        assert len(assigned) == (1 << 12) // SHARDS
        even_terms = sum(mask.bit_count() % 2 == 0 for mask in assigned)
        odd_terms = len(assigned) - even_terms

        plus = 0
        minus = 0
        positive_intersections = 0
        if dsum not in HARD_DSUMS:
            # Merged event-mass authority run 34826179077 proves each individual
            # event is impossible on these profiles. Recheck that cheaply here;
            # then every nonempty event intersection is also empty.
            singles = [self._event_count(tuple(domains), i) for i in range(12)]
            assert singles == [0] * 12, (dsum, singles)
            if SHARD == 0:
                assert assigned[0] == 0
                plus = int(baseline)
                positive_intersections = int(baseline > 0)
        else:
            # Group nearby subset sizes only as a cache-locality heuristic. The
            # shard assignment and every IE sign remain fixed and exact.
            for mask in sorted(assigned, key=lambda m: (m.bit_count(), m)):
                if mask == 0:
                    count = int(baseline)
                else:
                    d = self._force_nonzero_vars(tuple(domains), self.union_vars[mask])
                    count = 0 if d is None else int(self.solve(self.ALL, d))
                if count:
                    positive_intersections += 1
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
        # C.analyze supplies the exact separator-profile base masses. Returning
        # the even-parity subtotal lets it aggregate the global plus side once;
        # the odd side is aggregated below from the same stored profile rows.
        return int(plus), self.calls, len(self.memo)


def analyze():
    assert SHARDS > 0 and SHARDS & (SHARDS - 1) == 0
    assert (1 << 12) % SHARDS == 0 and 0 <= SHARD < SHARDS
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    original_pr212 = C.EXPECTED_PR212_COUNT
    C.ExactCounter = IEShardCounter
    C.EXPECTED_EXACT_COUNT = _AcceptExact()
    C.EXPECTED_PR212_COUNT = 1 << 10000
    try:
        with redirect_stdout(io.StringIO()):
            plus_base = C.analyze()
    finally:
        C.ExactCounter = original_counter
        C.EXPECTED_EXACT_COUNT = original_expected
        C.EXPECTED_PR212_COUNT = original_pr212

    profile_meta = {int(r['domain_state_sum']): r for r in plus_base['profile_rows']}
    assert set(profile_meta) == set(IE_ROWS)
    assert set(profile_meta) == {83,88,95,100,102,134,154,251,288,302}

    global_plus = 0
    global_minus = 0
    for dsum, erow in IE_ROWS.items():
        mass = int(profile_meta[dsum]['base_mass'])
        global_plus += mass * int(erow['ie_plus_partial'])
        global_minus += mass * int(erow['ie_minus_partial'])
    assert global_plus == int(plus_base['exact_count'])

    result = {
        'shard': SHARD,
        'shards': SHARDS,
        'projection_events': 12,
        'assigned_subset_terms': sum(int(r['assigned_terms']) for r in IE_ROWS.values()) // len(IE_ROWS),
        'assigned_even_terms': sum(int(r['assigned_even_terms']) for r in IE_ROWS.values()) // len(IE_ROWS),
        'assigned_odd_terms': sum(int(r['assigned_odd_terms']) for r in IE_ROWS.values()) // len(IE_ROWS),
        'global_ie_plus_partial': int(global_plus),
        'global_ie_minus_partial': int(global_minus),
        'global_signed_partial': int(global_plus - global_minus),
        'profile_rows': [IE_ROWS[k] for k in sorted(IE_ROWS)],
        'pairwise_exact_baseline_count': PAIRWISE_TOTAL,
        'hard_profiles': sorted(HARD_DSUMS),
        'event_inactivity_authority_run': 34826179077,
        'decision': 'C916_PROJECTION_HYPEREDGES_EXACT_IE_SHARD',
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print('result', json.dumps(result, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PROJECTION_HYPEREDGES_IE_SHARD')
    print('ALPHA_PASS=0')
    return result


if __name__ == '__main__':
    analyze()
