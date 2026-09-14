#!/usr/bin/env python3
import io, json, math, os, sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_m4_parent_correlation_scout as O

PHYS_N = 149
MASK = (1 << PHYS_N) - 1
TARGET_DOMAIN_SUMS = tuple(sorted({int(x) for x in os.environ.get('C916_AFFINE_SCOUT_DOMAIN_SUMS', '134,154').split(',') if x.strip()}))
MAX_CALLS = int(os.environ.get('C916_AFFINE_SCOUT_MAX_CALLS', '2000000'))
EXPECTED_CODIM = {6: 12, 7: 46, 8: 32}
EXPECTED_NORMAL_RANK = 92


def insert_rref(state, x):
    x = int(x)
    if not x:
        return state
    for r in state:
        p = (r & MASK).bit_length() - 1
        if p >= 0 and ((x >> p) & 1):
            x ^= r
    phys = x & MASK
    if not phys:
        return None if ((x >> PHYS_N) & 1) else state
    p = phys.bit_length() - 1
    out = [(r ^ x if ((r >> p) & 1) else r) for r in state]
    out.append(x)
    return tuple(sorted((r for r in out if r & MASK), reverse=True))


def inter(a, b, cache, stats):
    if a is None or b is None:
        return None
    if not a:
        return b
    if not b:
        return a
    key = (a, b) if a <= b else (b, a)
    if key in cache:
        stats['intersection_cache_hits'] += 1
        return cache[key]
    s = a
    for x in b:
        s = insert_rref(s, x)
        if s is None:
            break
    cache[key] = s
    stats['intersection_cache_misses'] += 1
    return s


def canonical(rows):
    s = ()
    for x in rows:
        s = insert_rref(s, x)
        if s is None:
            return None
    return s


def rebuild_anchors(gids):
    D, P = O.D, O.P
    e0, _e1, _half = P.C.P.U.H.classify_patterns()
    grouped = defaultdict(list)
    raw = 0
    for zc in range(4):
        for zs, cls in e0[zc]:
            can = P.C.P.U.H.support_for(O.POS, zs, cls)
            if can is None:
                continue
            raw += 1
            grouped[can].append((zs, cls))
    ordered = list(sorted(grouped.items(), key=lambda kv: kv[0]))
    assert raw == 577 and len(ordered) == 250
    anchors = {}
    codim = Counter()
    normals = []
    for gid in gids:
        can, sectors = ordered[int(gid)]
        assert len(sectors) == 4
        _prank, _local, anchor = D.projection_anchor(can)
        rows = tuple((int(m), int(rhs)) for m, rhs in anchor['physical_support_constraints'])
        codim[len(rows)] += 1
        normals.extend(m for m, _rhs in rows)
        aug = tuple(m | (rhs << PHYS_N) for m, rhs in rows)
        ca = canonical(aug)
        assert ca is not None
        anchors[int(gid)] = ca
    assert dict(sorted(codim.items())) == EXPECTED_CODIM
    assert P.R.gf2_rank(normals) == EXPECTED_NORMAL_RANK
    return anchors


class CallBudgetExceeded(RuntimeError):
    pass


SCOUT_ROWS = []


class AffineScoutCounter(C.ExactCounter):
    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        gids = tuple(g for members in variables for g in members)
        assert len(gids) == 90 and len(set(gids)) == 90
        anchors = rebuild_anchors(gids)
        self.state_aff = []
        for vi, (members, states) in enumerate(zip(self.variables, self.var_states)):
            zero = tuple(max(int(s[ci]) for s in states) for ci in range(len(members)))
            row = []
            for state in states:
                a = ()
                for ci, gid in enumerate(members):
                    if int(state[ci]) != zero[ci]:
                        a = canonical(a + anchors[int(gid)])
                        if a is None:
                            break
                row.append(a)
            self.state_aff.append(tuple(row))
        self.state_aff = tuple(self.state_aff)
        self.aff_cache = {}
        self.aff_stats = Counter()
        self.aff_memo = {}
        self.aff_calls = 0

    def _affine_filter(self, active, domains, aff):
        dom = tuple(domains)
        while True:
            dom = super()._arc_closure(active, dom)
            if dom is None:
                return None
            changed = False
            work = list(dom)
            scan = active
            while scan:
                lsb = scan & -scan
                vi = lsb.bit_length() - 1
                scan ^= lsb
                old = work[vi]
                keep = 0
                mask = old
                while mask:
                    x = mask & -mask
                    si = x.bit_length() - 1
                    mask ^= x
                    if inter(aff, self.state_aff[vi][si], self.aff_cache, self.aff_stats) is not None:
                        keep |= x
                if keep == 0:
                    self.aff_stats['affine_domain_wipeouts'] += 1
                    return None
                if keep != old:
                    work[vi] = keep
                    changed = True
                    self.aff_stats['affine_domain_reductions'] += old.bit_count() - keep.bit_count()
            dom = tuple(work)
            if not changed:
                return dom

    def _solve_affine(self, active, domains, aff):
        self.aff_calls += 1
        if self.aff_calls > MAX_CALLS:
            raise CallBudgetExceeded(MAX_CALLS)
        closed = self._affine_filter(active, domains, aff)
        if closed is None:
            return 0
        domains = closed

        factor = 1
        # Eliminate singleton variables one at a time. Pairwise arc closure has
        # already propagated their exact relation to every active neighbour.
        while active:
            singleton = None
            scan = active
            while scan:
                lsb = scan & -scan
                vi = lsb.bit_length() - 1
                scan ^= lsb
                d = domains[vi]
                if d & (d - 1) == 0:
                    singleton = vi
                    break
            if singleton is None:
                break
            vi = singleton
            d = domains[vi]
            si = d.bit_length() - 1
            na = inter(aff, self.state_aff[vi][si], self.aff_cache, self.aff_stats)
            if na is None:
                self.aff_stats['singleton_affine_prunes'] += 1
                return 0
            factor *= self.var_weights[vi][si]
            active ^= 1 << vi
            aff = na
            if not active:
                return factor
            closed = self._affine_filter(active, domains, aff)
            if closed is None:
                return 0
            domains = closed

        key = (active, tuple(domains[i] for i in range(self.N) if (active >> i) & 1), aff)
        if key in self.aff_memo:
            self.aff_stats['memo_hits'] += 1
            return factor * self.aff_memo[key]

        # Do not multiply disconnected pairwise components: the affine state is
        # a genuine global higher-order coupling. Instead use pairwise relevance
        # only as a branching heuristic, preserving exactness.
        best = None
        scan = active
        while scan:
            x = scan & -scan
            vi = x.bit_length() - 1
            scan ^= x
            rel = self._relevant_neighbors(vi, active, domains).bit_count()
            aff_classes = len({self.state_aff[vi][si] for si in range(len(self.var_states[vi])) if (domains[vi] >> si) & 1})
            score = (domains[vi].bit_count(), -rel, -aff_classes, vi)
            if best is None or score < best[0]:
                best = (score, vi)
        vi = best[1]
        subtotal = 0
        mask = domains[vi]
        while mask:
            x = mask & -mask
            mask ^= x
            nd = list(domains)
            nd[vi] = x
            subtotal += self._solve_affine(active, tuple(nd), aff)
        self.aff_memo[key] = subtotal
        return factor * subtotal

    def count_profile(self, domains):
        baseline_value, baseline_calls, baseline_memo = super().count_profile(domains)
        dsum = sum(d.bit_count() for d in domains)
        if dsum not in TARGET_DOMAIN_SUMS:
            return baseline_value, baseline_calls, baseline_memo

        self.aff_cache.clear()
        self.aff_stats.clear()
        self.aff_memo.clear()
        self.aff_calls = 0
        status = 'completed'
        value = None
        try:
            value = self._solve_affine(self.ALL, tuple(domains), ())
        except CallBudgetExceeded:
            status = 'call_budget_exceeded'
        row = {
            'domain_state_sum': dsum,
            'status': status,
            'pairwise_count': int(baseline_value),
            'all_order_affine_count': None if value is None else int(value),
            'gain_log2_bits': None if not value or not baseline_value else math.log2(baseline_value) - math.log2(value),
            'affine_calls': self.aff_calls,
            'affine_memo_states': len(self.aff_memo),
            'intersection_cache_entries': len(self.aff_cache),
            'stats': dict(self.aff_stats),
        }
        SCOUT_ROWS.append(row)
        print('affine_scout', json.dumps(row, sort_keys=True), flush=True)
        return baseline_value, baseline_calls, baseline_memo


def analyze():
    original = C.ExactCounter
    C.ExactCounter = AffineScoutCounter
    try:
        with redirect_stdout(io.StringIO()) as buf:
            baseline = C.analyze()
        # Preserve only the scout rows from the otherwise noisy baseline run.
        assert int(baseline['exact_count']) == int(C.EXPECTED_EXACT_COUNT)
    finally:
        C.ExactCounter = original

    got = {int(r['domain_state_sum']) for r in SCOUT_ROWS}
    assert got == set(TARGET_DOMAIN_SUMS), (got, TARGET_DOMAIN_SUMS)
    out = {
        'position': 'C',
        'physical_shared_dimension': PHYS_N,
        'pairwise_exact_baseline_count': int(C.EXPECTED_EXACT_COUNT),
        'target_domain_state_sums': list(TARGET_DOMAIN_SUMS),
        'max_calls_per_profile': MAX_CALLS,
        'scout_rows': SCOUT_ROWS,
        'completed_profiles': sum(r['status'] == 'completed' for r in SCOUT_ROWS),
        'budget_exceeded_profiles': sum(r['status'] != 'completed' for r in SCOUT_ROWS),
        'decision': 'C916_COMPLETE_PAIRWISE_ALL_ORDER_AFFINE_TRACTABILITY_SCOUT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_COMPLETE_PAIRWISE_ALL_ORDER_AFFINE_SCOUT')
    print('scope=exact all-order affine intersection scout on selected complete-pairwise separator profiles; no approximation is admitted and any call-budget exhaustion is reported as incomplete, never as a count')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
