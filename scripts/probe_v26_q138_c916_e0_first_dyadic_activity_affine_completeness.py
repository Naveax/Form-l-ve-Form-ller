#!/usr/bin/env python3
import io
import json
import math
import os
import sys
from collections import Counter, deque
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_all_order_affine_scout as A
import probe_v26_q138_c916_e0_first_dyadic_pr212_plus_projection_triples_quads_exact as H

PAIRWISE_COUNTER = C.ExactCounter
TARGET_DOMAIN_SUMS = tuple(sorted({int(x) for x in os.environ.get('C916_ACTIVITY_AFFINE_DOMAIN_SUMS', '154,251').split(',') if x.strip()}))
MAX_ACTIVITY_CALLS = int(os.environ.get('C916_ACTIVITY_AFFINE_MAX_CALLS', '5000000'))
QUADS = tuple(tuple(map(int, q)) for q in H.QUADS)
SCOUT_ROWS = []


class ActivityBudgetExceeded(RuntimeError):
    pass


class ActivityAffineCompletenessCounter(PAIRWISE_COUNTER):
    """Search a safe activity-level superset for affine obstructions.

    Exact magnitude states are existentially projected to zero/nonzero activity
    classes, separately for every contracted variable. Pair relations are then
    existentially projected profile-by-profile through the original unary domains.
    This loses magnitude correlations and is therefore a *superset* of every exact
    finite-model assignment, never a subset.

    The five triples and seven quadruples are enforced exactly at activity level.
    We count all finite-valid projected activity patterns and all such patterns
    whose union of fixed gid projection anchors is affine-consistent. Equality of
    these two counts proves that every exact finite-model assignment is all-order
    affine-consistent, because the exact assignments map into this projected set.
    """

    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        self.gids = tuple(int(g) for members in self.variables for g in members)
        assert len(self.gids) == len(set(self.gids)) == 90
        self.anchors = A.rebuild_anchors(self.gids)

        self.zero_coords = []
        self.activity_signatures = []
        self.state_to_activity = []
        self.activity_aff = []
        self.activity_active_class_mask = []
        self.gid_loc = {}

        for vi, (members, states) in enumerate(zip(self.variables, self.var_states)):
            zero = tuple(max(int(s[ci]) for s in states) for ci in range(len(members)))
            self.zero_coords.append(zero)
            sigs = []
            state_sig = []
            for state in states:
                sig = tuple(int(int(state[ci]) != zero[ci]) for ci in range(len(members)))
                if sig not in sigs:
                    sigs.append(sig)
                state_sig.append(sig)
            sigs = tuple(sorted(sigs))
            sig_index = {sig: i for i, sig in enumerate(sigs)}
            state_map = tuple(sig_index[sig] for sig in state_sig)
            self.activity_signatures.append(sigs)
            self.state_to_activity.append(state_map)

            affs = []
            active_mask = 0
            for ai, sig in enumerate(sigs):
                rows = []
                for ci, gid in enumerate(members):
                    self.gid_loc[int(gid)] = (vi, ci)
                    if sig[ci]:
                        rows.extend(self.anchors[int(gid)])
                aff = A.canonical(rows)
                assert aff is not None, (vi, sig)
                affs.append(aff)
                if any(sig):
                    active_mask |= 1 << ai
            self.activity_aff.append(tuple(affs))
            self.activity_active_class_mask.append(active_mask)

            # Reassert that the all-order scout really depends only on activity,
            # not on which nonzero quotient magnitude was chosen.
            for si, state in enumerate(states):
                ai = state_map[si]
                rows = []
                for ci, gid in enumerate(members):
                    if int(state[ci]) != zero[ci]:
                        rows.extend(self.anchors[int(gid)])
                assert A.canonical(rows) == affs[ai]

        self.zero_coords = tuple(self.zero_coords)
        self.activity_signatures = tuple(self.activity_signatures)
        self.state_to_activity = tuple(self.state_to_activity)
        self.activity_aff = tuple(self.activity_aff)
        self.activity_active_class_mask = tuple(self.activity_active_class_mask)
        assert len(self.gid_loc) == 90

        m4 = C.load(C.M4_PATH)
        triples = tuple(tuple(map(int, row)) for row in m4['projection_minimal_empty_triples'])
        assert len(triples) == 5 and len(QUADS) == 7
        mapped = []
        for edge in triples + QUADS:
            row = []
            for gid in edge:
                vi, ci = self.gid_loc[int(gid)]
                # Frozen projection clauses avoid both two-gid contractions.
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                row.append(vi)
            assert len(row) == len(set(row)) == len(edge)
            mapped.append(tuple(sorted(row)))
        self.hyperedges = tuple(mapped)
        assert len(self.hyperedges) == 12
        self.hyper_incidence = [0] * self.N
        for ei, edge in enumerate(self.hyperedges):
            for vi in edge:
                self.hyper_incidence[vi] |= 1 << ei

        self.activity_relrows = None
        self.activity_adj = None
        self.finite_memo = {}
        self.affine_memo = {}
        self.finite_calls = 0
        self.affine_calls = 0
        self.inter_cache = {}
        self.aff_stats = Counter()
        self.activity_stats = Counter()

    def _project_profile(self, domains):
        actdom = []
        class_orig_masks = []
        for vi, domain in enumerate(domains):
            nclass = len(self.activity_signatures[vi])
            per_class = [0] * nclass
            out = 0
            mask = int(domain)
            while mask:
                bit = mask & -mask
                si = bit.bit_length() - 1
                mask ^= bit
                ai = self.state_to_activity[vi][si]
                per_class[ai] |= bit
                out |= 1 << ai
            assert out
            actdom.append(out)
            class_orig_masks.append(tuple(per_class))

        relrows = {}
        adj = [0] * self.N
        for i in range(self.N):
            for j in range(i + 1, self.N):
                ni = len(self.activity_signatures[i])
                nj = len(self.activity_signatures[j])
                orig = self.relrows.get((i, j))
                rows = []
                for ai in range(ni):
                    allowed_j = 0
                    simask = class_orig_masks[i][ai]
                    if simask:
                        if orig is None:
                            # Complete original relation. Unary/profile filtering
                            # is already encoded by class_orig_masks[j].
                            for aj in range(nj):
                                if class_orig_masks[j][aj]:
                                    allowed_j |= 1 << aj
                        else:
                            tmp = simask
                            original_j_mask = 0
                            while tmp:
                                bit = tmp & -tmp
                                si = bit.bit_length() - 1
                                tmp ^= bit
                                original_j_mask |= int(orig[si]) & int(domains[j])
                            for aj in range(nj):
                                if original_j_mask & class_orig_masks[j][aj]:
                                    allowed_j |= 1 << aj
                    rows.append(allowed_j)
                rows = tuple(rows)

                full_j = int(actdom[j])
                complete = True
                scan = int(actdom[i])
                while scan:
                    bit = scan & -scan
                    ai = bit.bit_length() - 1
                    scan ^= bit
                    if (rows[ai] & full_j) != full_j:
                        complete = False
                        break
                if complete:
                    continue

                relrows[(i, j)] = rows
                rev = []
                for aj in range(nj):
                    allowed_i = 0
                    for ai in range(ni):
                        if (rows[ai] >> aj) & 1:
                            allowed_i |= 1 << ai
                    rev.append(allowed_i)
                relrows[(j, i)] = tuple(rev)
                adj[i] |= 1 << j
                adj[j] |= 1 << i

        self.activity_relrows = relrows
        self.activity_adj = tuple(adj)
        return tuple(actdom)

    @staticmethod
    def _restrict_supported(di, rows, dj):
        out = 0
        mask = int(di)
        while mask:
            bit = mask & -mask
            ai = bit.bit_length() - 1
            mask ^= bit
            if int(rows[ai]) & int(dj):
                out |= bit
        return out

    def _pair_closure(self, domains):
        dom = list(domains)
        q = deque(range(self.N))
        inq = set(q)
        while q:
            i = q.popleft()
            inq.discard(i)
            di = int(dom[i])
            neighbors = int(self.activity_adj[i])
            while neighbors:
                bit = neighbors & -neighbors
                j = bit.bit_length() - 1
                neighbors ^= bit
                nd = self._restrict_supported(dom[j], self.activity_relrows[(j, i)], di)
                if nd != dom[j]:
                    if not nd:
                        self.activity_stats['pairwise_wipeouts'] += 1
                        return None
                    dom[j] = nd
                    self.activity_stats['pairwise_activity_reductions'] += 1
                    if j not in inq:
                        q.append(j)
                        inq.add(j)
        return tuple(dom)

    def _finite_closure(self, domains):
        dom = tuple(domains)
        while True:
            dom = self._pair_closure(dom)
            if dom is None:
                return None
            changed = False
            work = list(dom)
            for edge in self.hyperedges:
                uncertain = []
                satisfied = False
                for vi in edge:
                    d = int(work[vi])
                    active = d & int(self.activity_active_class_mask[vi])
                    inactive = d & ~int(self.activity_active_class_mask[vi])
                    if not active:
                        satisfied = True
                        break
                    if inactive:
                        uncertain.append(vi)
                if satisfied:
                    continue
                if not uncertain:
                    self.activity_stats['forbidden_all_active_prunes'] += 1
                    return None
                if len(uncertain) == 1:
                    vi = uncertain[0]
                    nd = int(work[vi]) & ~int(self.activity_active_class_mask[vi])
                    if not nd:
                        return None
                    if nd != work[vi]:
                        work[vi] = nd
                        self.activity_stats['unit_hyperedge_forces'] += 1
                        changed = True
            dom = tuple(work)
            if not changed:
                return dom

    def _affine_from_singletons(self, domains):
        aff = ()
        for vi, d in enumerate(domains):
            d = int(d)
            if d & (d - 1):
                continue
            ai = d.bit_length() - 1
            aff = A.inter(aff, self.activity_aff[vi][ai], self.inter_cache, self.aff_stats)
            if aff is None:
                return None
        return aff

    def _affine_closure(self, domains):
        dom = tuple(domains)
        while True:
            dom = self._finite_closure(dom)
            if dom is None:
                return None
            aff = self._affine_from_singletons(dom)
            if aff is None:
                self.activity_stats['forced_affine_wipeouts'] += 1
                return None
            changed = False
            work = list(dom)
            for vi, d in enumerate(dom):
                d = int(d)
                if not (d & (d - 1)):
                    continue
                keep = 0
                scan = d
                while scan:
                    bit = scan & -scan
                    ai = bit.bit_length() - 1
                    scan ^= bit
                    if A.inter(aff, self.activity_aff[vi][ai], self.inter_cache, self.aff_stats) is not None:
                        keep |= bit
                if not keep:
                    self.activity_stats['affine_domain_wipeouts'] += 1
                    return None
                if keep != d:
                    work[vi] = keep
                    self.activity_stats['affine_activity_reductions'] += d.bit_count() - keep.bit_count()
                    changed = True
            dom = tuple(work)
            if not changed:
                return dom

    def _branch_var(self, domains):
        best = None
        for vi, d in enumerate(domains):
            d = int(d)
            if not (d & (d - 1)):
                continue
            pairdeg = int(self.activity_adj[vi]).bit_count()
            hyperdeg = int(self.hyper_incidence[vi]).bit_count()
            score = (d.bit_count(), -hyperdeg, -pairdeg, vi)
            if best is None or score < best[0]:
                best = (score, vi)
        return None if best is None else best[1]

    def _count_finite(self, domains):
        self.finite_calls += 1
        if self.finite_calls > MAX_ACTIVITY_CALLS:
            raise ActivityBudgetExceeded(('finite', MAX_ACTIVITY_CALLS))
        dom = self._finite_closure(domains)
        if dom is None:
            return 0
        key = dom
        got = self.finite_memo.get(key)
        if got is not None:
            return got
        vi = self._branch_var(dom)
        if vi is None:
            self.finite_memo[key] = 1
            return 1
        total = 0
        scan = int(dom[vi])
        while scan:
            bit = scan & -scan
            scan ^= bit
            nd = list(dom)
            nd[vi] = bit
            total += self._count_finite(tuple(nd))
        self.finite_memo[key] = total
        return total

    def _count_affine(self, domains):
        self.affine_calls += 1
        if self.affine_calls > MAX_ACTIVITY_CALLS:
            raise ActivityBudgetExceeded(('affine', MAX_ACTIVITY_CALLS))
        dom = self._affine_closure(domains)
        if dom is None:
            return 0
        key = dom
        got = self.affine_memo.get(key)
        if got is not None:
            return got
        vi = self._branch_var(dom)
        if vi is None:
            # _affine_closure has already checked the union of every forced class.
            self.affine_memo[key] = 1
            return 1
        total = 0
        scan = int(dom[vi])
        while scan:
            bit = scan & -scan
            scan ^= bit
            nd = list(dom)
            nd[vi] = bit
            total += self._count_affine(tuple(nd))
        self.affine_memo[key] = total
        return total

    def count_profile(self, domains):
        baseline, baseline_calls, baseline_memo = PAIRWISE_COUNTER.count_profile(self, domains)
        dsum = sum(int(d).bit_count() for d in domains)
        if dsum not in TARGET_DOMAIN_SUMS:
            return baseline, baseline_calls, baseline_memo

        actdom = self._project_profile(tuple(domains))
        self.finite_memo.clear()
        self.affine_memo.clear()
        self.finite_calls = 0
        self.affine_calls = 0
        self.inter_cache.clear()
        self.aff_stats.clear()
        self.activity_stats.clear()
        status = 'completed'
        finite = None
        affine = None
        try:
            finite = self._count_finite(actdom)
            affine = self._count_affine(actdom)
        except ActivityBudgetExceeded as exc:
            status = 'budget_exceeded'
            self.activity_stats['budget_reason'] = repr(exc.args[0])

        if finite is not None and affine is not None:
            assert 0 <= affine <= finite
        row = {
            'domain_state_sum': dsum,
            'status': status,
            'pairwise_magnitude_count': int(baseline),
            'projected_activity_domain_state_sum': sum(int(d).bit_count() for d in actdom),
            'projected_partial_pair_relations': len(self.activity_relrows) // 2,
            'finite_valid_activity_patterns': None if finite is None else int(finite),
            'affine_valid_activity_patterns': None if affine is None else int(affine),
            'all_finite_activity_patterns_affine_consistent': None if finite is None or affine is None else bool(finite == affine),
            'finite_calls': self.finite_calls,
            'affine_calls': self.affine_calls,
            'finite_memo_states': len(self.finite_memo),
            'affine_memo_states': len(self.affine_memo),
            'intersection_cache_entries': len(self.inter_cache),
            'activity_stats': dict(self.activity_stats),
            'affine_stats': dict(self.aff_stats),
        }
        SCOUT_ROWS.append(row)
        print('activity_affine', json.dumps(row, sort_keys=True), flush=True)
        return baseline, baseline_calls, baseline_memo


def analyze():
    original = C.ExactCounter
    C.ExactCounter = ActivityAffineCompletenessCounter
    try:
        with redirect_stdout(io.StringIO()):
            baseline = C.analyze()
        assert int(baseline['exact_count']) == int(C.EXPECTED_EXACT_COUNT)
    finally:
        C.ExactCounter = original

    got = {int(row['domain_state_sum']) for row in SCOUT_ROWS}
    assert got == set(TARGET_DOMAIN_SUMS), (got, TARGET_DOMAIN_SUMS)
    proved = [
        int(row['domain_state_sum'])
        for row in SCOUT_ROWS
        if row['status'] == 'completed' and row['all_finite_activity_patterns_affine_consistent']
    ]
    counterexamples = [
        int(row['domain_state_sum'])
        for row in SCOUT_ROWS
        if row['status'] == 'completed' and row['all_finite_activity_patterns_affine_consistent'] is False
    ]
    out = {
        'position': 'C',
        'physical_shared_dimension': A.PHYS_N,
        'global_projection_normal_rank': A.EXPECTED_NORMAL_RANK,
        'pairwise_exact_baseline_count': int(C.EXPECTED_EXACT_COUNT),
        'activity_projection_is_safe_superset': True,
        'projection_hyperedges_enforced': 12,
        'target_domain_state_sums': list(TARGET_DOMAIN_SUMS),
        'max_activity_calls_per_counter': MAX_ACTIVITY_CALLS,
        'scout_rows': SCOUT_ROWS,
        'profiles_proved_finite_implies_affine': proved,
        'profiles_with_projected_activity_affine_gap': counterexamples,
        'decision': 'C916_FINITE_MODEL_TO_ALL_ORDER_AFFINE_ACTIVITY_SUPERSET_SCOUT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_ACTIVITY_AFFINE_COMPLETENESS_SCOUT')
    print('scope=existential zero/nonzero projection of the exact magnitude CSP is a safe superset; equality between finite-valid and affine-valid projected activity pattern counts proves finite-model assignments are all-order affine-consistent for that separator profile')
    print('boundary=this theorem concerns all-order affine consistency only; any stronger higher-order physical-image condition remains separate')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
