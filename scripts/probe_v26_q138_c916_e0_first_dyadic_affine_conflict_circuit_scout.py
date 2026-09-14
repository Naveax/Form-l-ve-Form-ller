#!/usr/bin/env python3
import hashlib, io, json, os, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_all_order_affine_scout as A
import probe_v26_q138_c916_e0_first_dyadic_complete_pairwise_affine_polynomial_interned_scout as I
import probe_v26_q138_c916_e0_first_dyadic_pr212_plus_projection_triples_quads_exact as H

PAIRWISE_COUNTER = C.ExactCounter
TARGET_DOMAIN_SUM = int(os.environ.get('C916_AFFINE_CIRCUIT_DOMAIN_SUM', '251'))
NOVEL_QUOTA = int(os.environ.get('C916_AFFINE_CIRCUIT_QUOTA', '32'))
MAX_RAW_BAD = int(os.environ.get('C916_AFFINE_CIRCUIT_MAX_RAW_BAD', '2000'))
SCOUT_ROWS = []


class CircuitQuotaReached(RuntimeError):
    pass


class AffineConflictCircuitScout(I.InternedAffinePolynomialCounter):
    """Mine exact minimal inconsistent anchor sets from affine-empty convolutions.

    Integer affine states are exactly the same canonical RREF objects as in the
    merged interned polynomial solver. One exact support witness is attached to
    each state. Whenever two witnessed affine states have empty intersection,
    their witness union is an exact inconsistent anchor set. Greedy deletions are
    then checked with the original 149-bit affine algebra until the set is
    inclusion-minimal. Every emitted circuit is independently recertified before
    output; the scout may stop after a quota without claiming a complete list.
    """

    def __init__(self, variables, var_states, var_weights, pairq):
        self.capture_enabled = False
        self.witness = {}
        self.raw_bad_seen = set()
        self.circuits = set()
        self.novel_circuits = set()
        self.circuit_stats = Counter()
        super().__init__(variables, var_states, var_weights, pairq)

        gids = tuple(int(g) for members in self.variables for g in members)
        assert len(gids) == len(set(gids)) == 90
        self.gids = tuple(sorted(gids))
        self.gid_to_bit = {gid: 1 << i for i, gid in enumerate(self.gids)}
        self.bit_to_gid = {1 << i: gid for i, gid in enumerate(self.gids)}
        self.anchors = A.rebuild_anchors(gids)

        # Attach one single-anchor witness to every anchor state already interned
        # by the parent initialization. If two gids share the same affine anchor,
        # keeping either one is sufficient to witness that exact affine state.
        for gid in self.gids:
            sid = self.state_to_id[self.anchors[gid]]
            self._set_witness(sid, self.gid_to_bit[gid])

        # Parent initialization may also have interned contracted variable-state
        # intersections. Seed them with their exact one/two-gid support witnesses.
        for vi, (members, states) in enumerate(zip(self.variables, self.var_states)):
            zero = tuple(max(int(s[ci]) for s in states) for ci in range(len(members)))
            for si, state in enumerate(states):
                mask = 0
                for ci, gid in enumerate(members):
                    if int(state[ci]) != zero[ci]:
                        mask |= self.gid_to_bit[int(gid)]
                sid = self.state_aff_id[vi][si]
                if sid != I.BAD_ID:
                    self._set_witness(sid, mask)

        m4 = C.load(C.M4_PATH)
        triples = tuple(tuple(sorted(map(int, t))) for t in m4['projection_minimal_empty_triples'])
        quads = tuple(tuple(sorted(map(int, q))) for q in H.QUADS)
        assert len(triples) == 5 and len(quads) == 7
        self.known_circuits = set(triples + quads)
        self.capture_enabled = True

    def _set_witness(self, sid, mask):
        if sid == I.BAD_ID:
            return
        mask = int(mask)
        old = self.witness.get(sid)
        if old is None or mask.bit_count() < old.bit_count() or (
            mask.bit_count() == old.bit_count() and mask < old
        ):
            self.witness[sid] = mask

    def _mask_gids(self, mask):
        out = []
        m = int(mask)
        while m:
            bit = m & -m
            m ^= bit
            out.append(self.bit_to_gid[bit])
        return tuple(sorted(out))

    def _inconsistent(self, mask):
        state = ()
        for gid in self._mask_gids(mask):
            for row in self.anchors[gid]:
                state = A.insert_rref(state, row)
                if state is None:
                    return True
        return False

    def _minimize_bad(self, mask):
        mask = int(mask)
        assert self._inconsistent(mask)
        changed = True
        while changed:
            changed = False
            m = mask
            while m:
                bit = m & -m
                m ^= bit
                cand = mask ^ bit
                if cand and self._inconsistent(cand):
                    mask = cand
                    changed = True
                    break
        gids = self._mask_gids(mask)
        assert self._inconsistent(mask)
        for gid in gids:
            assert not self._inconsistent(mask ^ self.gid_to_bit[gid]), (gids, gid)
        return gids

    def _capture_bad(self, wa, wb):
        raw = int(wa) | int(wb)
        if raw in self.raw_bad_seen:
            self.circuit_stats['raw_bad_duplicate'] += 1
            return
        if len(self.raw_bad_seen) >= MAX_RAW_BAD:
            self.circuit_stats['raw_bad_cap_skips'] += 1
            return
        self.raw_bad_seen.add(raw)
        self.circuit_stats['raw_bad_unique'] += 1
        circuit = self._minimize_bad(raw)
        if circuit in self.circuits:
            self.circuit_stats['minimal_duplicate'] += 1
            return
        self.circuits.add(circuit)
        self.circuit_stats[f'circuit_size_{len(circuit)}'] += 1
        if circuit not in self.known_circuits:
            self.novel_circuits.add(circuit)
            self.circuit_stats['novel_circuits'] += 1
            if len(self.novel_circuits) >= NOVEL_QUOTA:
                raise CircuitQuotaReached(NOVEL_QUOTA)
        else:
            self.circuit_stats['known_circuits_rediscovered'] += 1

    def _inter_id(self, a, b):
        rid = super()._inter_id(a, b)
        if not self.capture_enabled:
            return rid
        wa = self.witness.get(a)
        wb = self.witness.get(b)
        if wa is None or wb is None:
            self.circuit_stats['unwitnessed_intersections'] += 1
            return rid
        union = int(wa) | int(wb)
        if rid == I.BAD_ID:
            self.circuit_stats['witnessed_empty_intersections'] += 1
            self._capture_bad(wa, wb)
        else:
            self._set_witness(rid, union)
        return rid

    def _recertify(self):
        rows = []
        for circuit in sorted(self.circuits, key=lambda x: (len(x), x)):
            mask = 0
            for gid in circuit:
                mask |= self.gid_to_bit[gid]
            assert self._inconsistent(mask)
            deletions = []
            for gid in circuit:
                ok = not self._inconsistent(mask ^ self.gid_to_bit[gid])
                assert ok
                deletions.append({'removed_gid': gid, 'remaining_consistent': True})
            rows.append({
                'gids': list(circuit),
                'size': len(circuit),
                'known_projection_circuit': circuit in self.known_circuits,
                'all_single_deletions_consistent': True,
            })
        return rows

    def count_profile(self, domains):
        baseline, baseline_calls, baseline_memo = PAIRWISE_COUNTER.count_profile(self, domains)
        dsum = sum(int(d).bit_count() for d in domains)
        if dsum != TARGET_DOMAIN_SUM:
            return baseline, baseline_calls, baseline_memo

        self.inter_cache.clear()
        self.poly_memo.clear()
        self.poly_stats.clear()
        self.poly_calls = 0
        self.peak_poly_states = 0
        self.raw_bad_seen.clear()
        self.circuits.clear()
        self.novel_circuits.clear()
        self.circuit_stats.clear()
        status = 'completed_without_quota'
        try:
            self._solve_poly(self.ALL, tuple(domains))
        except CircuitQuotaReached:
            status = 'novel_quota_reached'
        except I.InternBudgetExceeded as exc:
            status = 'intern_budget_exceeded'
            self.circuit_stats['budget_reason'] = str(exc)

        circuits = self._recertify()
        payload = json.dumps(circuits, sort_keys=True, separators=(',', ':')).encode()
        row = {
            'domain_state_sum': dsum,
            'status': status,
            'pairwise_count': int(baseline),
            'novel_quota': NOVEL_QUOTA,
            'raw_bad_cap': MAX_RAW_BAD,
            'minimal_circuits_found': len(circuits),
            'novel_minimal_circuits_found': len(self.novel_circuits),
            'circuit_digest_sha256': hashlib.sha256(payload).hexdigest(),
            'circuits': circuits,
            'poly_calls': self.poly_calls,
            'poly_memo_states': len(self.poly_memo),
            'peak_poly_states': self.peak_poly_states,
            'interned_states': len(self.id_to_state),
            'intersection_cache_entries': len(self.inter_cache),
            'circuit_stats': dict(self.circuit_stats),
        }
        SCOUT_ROWS.append(row)
        print('affine_circuits', json.dumps(row, sort_keys=True), flush=True)
        return baseline, baseline_calls, baseline_memo


def analyze():
    original = C.ExactCounter
    C.ExactCounter = AffineConflictCircuitScout
    try:
        with redirect_stdout(io.StringIO()):
            baseline = C.analyze()
        assert int(baseline['exact_count']) == int(C.EXPECTED_EXACT_COUNT)
    finally:
        C.ExactCounter = original

    assert len(SCOUT_ROWS) == 1
    row = SCOUT_ROWS[0]
    assert row['minimal_circuits_found'] >= row['novel_minimal_circuits_found']
    out = {
        'position': 'C',
        'physical_shared_dimension': A.PHYS_N,
        'pairwise_exact_baseline_count': int(C.EXPECTED_EXACT_COUNT),
        'target_domain_state_sum': TARGET_DOMAIN_SUM,
        'scout': row,
        'complete_circuit_enumeration': False,
        'decision': 'C916_AFFINE_MINIMAL_CONFLICT_CIRCUIT_SCOUT_EXACT_WITNESSES',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_AFFINE_CONFLICT_CIRCUIT_SCOUT')
    print('scope=each emitted circuit is independently certified affine-inconsistent and inclusion-minimal; the list is a quota-limited discovery scout, not a complete circuit enumeration')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
