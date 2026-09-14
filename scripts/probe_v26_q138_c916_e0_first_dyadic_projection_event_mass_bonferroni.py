#!/usr/bin/env python3
import io, json, math, os, sys
from collections import defaultdict
from contextlib import redirect_stdout
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_pr212_plus_projection_triples_quads_exact as H

PAIRWISE_TOTAL = int(C.EXPECTED_EXACT_COUNT)
PAIR_TARGETS = tuple(sorted({int(x) for x in os.environ.get('C916_EVENT_PAIR_DOMAIN_SUMS', '251,288,302').split(',') if x.strip()}))
EVENT_ROWS = {}


class EventMassCounter(C.ExactCounter):
    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        m4 = C.load(C.M4_PATH)
        triples = tuple(tuple(map(int, t)) for t in m4['projection_minimal_empty_triples'])
        quads = tuple(tuple(map(int, q)) for q in H.QUADS)
        assert len(triples) == 5 and len(quads) == 7
        self.gid_edges = triples + quads

        self.loc = {}
        self.zero = {}
        for vi, members in enumerate(self.variables):
            for ci, gid in enumerate(members):
                self.loc[int(gid)] = (vi, ci)
        assert len(self.loc) == 90
        for edge in self.gid_edges:
            for gid in edge:
                vi, ci = self.loc[int(gid)]
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                self.zero[vi] = max(int(s[0]) for s in self.var_states[vi])

    def _condition_nonzero(self, domains, gids):
        out = list(domains)
        for gid in sorted(set(map(int, gids))):
            vi, ci = self.loc[gid]
            assert ci == 0
            zbit = 1 << self.zero[vi]
            nd = int(out[vi]) & ~zbit
            if not nd:
                return None
            out[vi] = nd
        return tuple(out)

    def _condition_count(self, domains, gids):
        d = self._condition_nonzero(domains, gids)
        if d is None:
            return 0
        return super().solve(self.ALL, d)

    def count_profile(self, domains):
        baseline, base_calls, base_memo = super().count_profile(domains)
        dsum = sum(int(d).bit_count() for d in domains)
        if baseline == 0:
            EVENT_ROWS[dsum] = {
                'domain_state_sum': dsum,
                'pairwise_count': 0,
                'single_event_counts': [0] * 12,
                'single_sum': 0,
                'pair_intersection_sum': 0,
                'valid_lower_bonferroni': 0,
                'valid_upper_bonferroni': 0,
                'pair_order_evaluated': dsum in PAIR_TARGETS,
            }
            return baseline, base_calls, base_memo

        # Reuse the scalar pairwise memo populated by the baseline count and by
        # every subsequent conditioned query. All keys include the conditioned
        # active domains, so sharing is exact and materially cheaper than 78
        # independent cold solves per hard profile.
        single = []
        for edge in self.gid_edges:
            single.append(int(self._condition_count(tuple(domains), edge)))
        s1 = sum(single)

        s2 = 0
        pair_rows = []
        if dsum in PAIR_TARGETS:
            for i, j in combinations(range(len(self.gid_edges)), 2):
                union = tuple(sorted(set(self.gid_edges[i]) | set(self.gid_edges[j])))
                c = int(self._condition_count(tuple(domains), union))
                s2 += c
                pair_rows.append({'left_event': i, 'right_event': j, 'intersection_count': c})

        # Bonferroni inequalities for U = union of the 12 forbidden events:
        #   S1-S2 <= |U| <= S1.
        # Therefore N-S1 <= valid <= N-S1+S2. Clamp to [0,N].
        valid_lower = max(0, int(baseline) - s1)
        valid_upper = min(int(baseline), int(baseline) - s1 + s2) if dsum in PAIR_TARGETS else int(baseline)
        row = {
            'domain_state_sum': dsum,
            'pairwise_count': int(baseline),
            'single_event_counts': single,
            'single_sum': s1,
            'pair_intersection_sum': s2,
            'pair_order_evaluated': dsum in PAIR_TARGETS,
            'valid_lower_bonferroni': valid_lower,
            'valid_upper_bonferroni': valid_upper,
            'single_event_forbidden_fraction_sum': (s1 / baseline) if baseline else None,
            'pairwise_memo_states_after_queries': len(self.memo),
            'pairwise_recursive_calls_after_queries': self.calls,
            'pair_intersections': pair_rows,
        }
        EVENT_ROWS[dsum] = row
        print('event_mass', json.dumps({k: v for k, v in row.items() if k != 'pair_intersections'}, sort_keys=True), flush=True)
        return baseline, base_calls, base_memo


def analyze():
    original = C.ExactCounter
    C.ExactCounter = EventMassCounter
    try:
        with redirect_stdout(io.StringIO()):
            base = C.analyze()
        assert int(base['exact_count']) == PAIRWISE_TOTAL
    finally:
        C.ExactCounter = original

    by_dsum = {int(r['domain_state_sum']): r for r in base['profile_rows']}
    assert set(EVENT_ROWS) == set(by_dsum)

    global_lower = 0
    global_upper = 0
    global_pairwise = 0
    activation = []
    for dsum, prow in sorted(by_dsum.items()):
        mass = int(prow['base_mass'])
        erow = EVENT_ROWS[dsum]
        n = int(erow['pairwise_count'])
        global_pairwise += mass * n
        global_lower += mass * int(erow['valid_lower_bonferroni'])
        global_upper += mass * int(erow['valid_upper_bonferroni'])
        active_events = [i for i, c in enumerate(erow['single_event_counts']) if int(c) > 0]
        activation.append({'domain_state_sum': dsum, 'active_events': active_events, 'active_event_count': len(active_events)})

    assert global_pairwise == PAIRWISE_TOTAL
    assert 0 <= global_lower <= global_upper <= global_pairwise
    out = {
        'position': 'C',
        'physical_shared_dimension': 149,
        'pairwise_exact_baseline_count': PAIRWISE_TOTAL,
        'projection_events': 12,
        'projection_minimal_empty_triples': 5,
        'projection_minimal_empty_quadruples': 7,
        'pair_intersection_profiles': list(PAIR_TARGETS),
        'event_activation_by_profile': activation,
        'global_valid_lower_bonferroni': global_lower,
        'global_valid_upper_bonferroni': global_upper,
        'global_valid_lower_log2': math.log2(global_lower) if global_lower else None,
        'global_valid_upper_log2': math.log2(global_upper) if global_upper else None,
        'guaranteed_gain_lower_bound_log2_bits': math.log2(PAIRWISE_TOTAL) - math.log2(global_upper) if global_upper else None,
        'possible_gain_upper_bound_log2_bits': math.log2(PAIRWISE_TOTAL) - math.log2(global_lower) if global_lower else None,
        'profile_event_rows': [EVENT_ROWS[k] for k in sorted(EVENT_ROWS)],
        'decision': 'C916_COMPLETE_PAIRWISE_PROJECTION_EVENT_MASS_BONFERRONI_EXACT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_PROJECTION_EVENT_MASS_BONFERRONI')
    print('scope=exact complete-pairwise conditional masses for each of the five minimal-empty triples and seven minimal-empty quadruples, plus all pair intersections on the 251/288/302 hard profiles; reported global interval follows the first two Bonferroni inequalities and is rigorous')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
