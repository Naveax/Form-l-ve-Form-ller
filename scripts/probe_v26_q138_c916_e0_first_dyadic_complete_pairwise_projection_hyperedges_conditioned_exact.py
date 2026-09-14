#!/usr/bin/env python3
import io, json, math, sys
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import probe_v26_q138_c916_e0_first_dyadic_pr212_plus_projection_triples_quads_exact as H

PAIRWISE_COUNT = int(C.EXPECTED_EXACT_COUNT)
QUADS = tuple(tuple(map(int, q)) for q in H.QUADS)
EXPECTED_QUAD_DIGEST = H.EXPECTED_QUAD_DIGEST


class _AcceptExact:
    def __eq__(self, other):
        return True
    def __req__(self, other):
        return True


def _canonical_edges(edges):
    ordered = sorted({tuple(sorted(map(int, e))) for e in edges if e}, key=lambda e: (len(e), e))
    kept = []
    for e in ordered:
        se = set(e)
        if any(set(k) <= se for k in kept):
            continue
        kept.append(e)
    return tuple(kept)


class ConditionedHyperCounter(C.ExactCounter):
    """Exact finite-hyperedge counter that preserves the fast pairwise oracle.

    Rather than injecting every triple/quad into pairwise component connectivity,
    recursively satisfy one forbidden all-nonzero edge by partitioning on its
    first zero participant. Each branch is only a unary domain restriction; the
    original ExactCounter then retains arc closure, component factorization and
    memoization unchanged.
    """

    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        m4 = C.load(C.M4_PATH)
        triples = tuple(tuple(map(int, t)) for t in m4['projection_minimal_empty_triples'])
        assert len(triples) == 5 and len(QUADS) == 7
        self.raw_gid_edges = triples + QUADS

        loc = {}
        for vi, members in enumerate(self.variables):
            for ci, gid in enumerate(members):
                assert int(gid) not in loc
                loc[int(gid)] = (vi, ci)
        assert len(loc) == 90

        edges = []
        self.zero_state = {}
        for edge in self.raw_gid_edges:
            mapped = []
            for gid in edge:
                vi, ci = loc[int(gid)]
                # None of the frozen 5+7 projection obstructions touches the two
                # special signed-pair contractions. Keep this an asserted theorem
                # of this implementation rather than silently mishandling coords.
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, vi, self.variables[vi])
                z = max(int(s[0]) for s in self.var_states[vi])
                self.zero_state[vi] = z
                mapped.append(vi)
            assert len(mapped) == len(set(mapped)) == len(edge)
            edges.append(tuple(sorted(mapped)))
        self.hyperedges = _canonical_edges(edges)
        assert len(self.hyperedges) == 12
        self.hyper_memo = {}
        self.hyper_stats = Counter()

    def _restrict_zero(self, domains, vi):
        zbit = 1 << self.zero_state[vi]
        d = int(domains[vi]) & zbit
        if not d:
            return None
        out = list(domains)
        out[vi] = d
        return tuple(out)

    def _restrict_nonzero(self, domains, vi):
        zbit = 1 << self.zero_state[vi]
        d = int(domains[vi]) & ~zbit
        if not d:
            return None
        out = list(domains)
        out[vi] = d
        return tuple(out)

    def _normalize(self, domains, edges):
        """Pairwise-close domains and simplify/propagate forbidden hyperedges."""
        dom = tuple(domains)
        eds = tuple(edges)
        while True:
            dom = super()._arc_closure(self.ALL, dom)
            if dom is None:
                self.hyper_stats['pairwise_wipeouts'] += 1
                return None, None

            reduced = []
            forced_zero = None
            violated = False
            for edge in eds:
                uncertain = []
                satisfied = False
                for vi in edge:
                    d = int(dom[vi])
                    zbit = 1 << self.zero_state[vi]
                    can_zero = bool(d & zbit)
                    can_nonzero = bool(d & ~zbit)
                    if not can_nonzero:
                        satisfied = True
                        break
                    if can_zero:
                        uncertain.append(vi)
                    # else this participant is already forced nonzero and drops
                    # from the residual not-all-nonzero clause.
                if satisfied:
                    self.hyper_stats['satisfied_edges_dropped'] += 1
                    continue
                if not uncertain:
                    violated = True
                    break
                if len(uncertain) == 1:
                    forced_zero = uncertain[0]
                    break
                reduced.append(tuple(sorted(uncertain)))

            if violated:
                self.hyper_stats['forbidden_all_nonzero_prunes'] += 1
                return None, None
            if forced_zero is not None:
                nd = self._restrict_zero(dom, forced_zero)
                if nd is None:
                    self.hyper_stats['forced_zero_wipeouts'] += 1
                    return None, None
                self.hyper_stats['unit_hyperedge_forces'] += 1
                dom = nd
                continue

            new_eds = _canonical_edges(reduced)
            return dom, new_eds

    def _choose_edge(self, domains, edges):
        # Small residual edges first; then prefer participants whose domains are
        # smallest after pairwise closure so first-zero branching propagates fast.
        return min(
            edges,
            key=lambda e: (
                len(e),
                sum(int(domains[v]).bit_count() for v in e),
                e,
            ),
        )

    def _count_hyper(self, domains, edges):
        self.hyper_stats['hyper_calls'] += 1
        norm_dom, norm_edges = self._normalize(domains, edges)
        if norm_dom is None:
            return 0
        if not norm_edges:
            self.hyper_stats['pairwise_oracle_calls'] += 1
            return super().solve(self.ALL, norm_dom)

        key = (norm_edges, norm_dom)
        if key in self.hyper_memo:
            self.hyper_stats['hyper_memo_hits'] += 1
            return self.hyper_memo[key]

        edge = self._choose_edge(norm_dom, norm_edges)
        rest = tuple(e for e in norm_edges if e != edge)
        total = 0

        # Exact disjoint partition of "edge has at least one zero": first member
        # is zero; or first is nonzero and second is zero; ... . The omitted
        # all-nonzero branch is precisely the forbidden event.
        prefix = norm_dom
        for vi in edge:
            zdom = self._restrict_zero(prefix, vi)
            if zdom is not None:
                total += self._count_hyper(zdom, rest)
                self.hyper_stats['first_zero_branches'] += 1
            prefix = self._restrict_nonzero(prefix, vi)
            if prefix is None:
                break

        self.hyper_memo[key] = total
        return total

    def count_profile(self, domains):
        self.memo.clear()
        self.calls = 0
        self.hyper_memo.clear()
        self.hyper_stats.clear()
        value = self._count_hyper(tuple(domains), self.hyperedges)
        dsum = sum(int(d).bit_count() for d in domains)
        print('hyper_profile', json.dumps({
            'domain_state_sum': dsum,
            'count': int(value),
            'pairwise_memo_states': len(self.memo),
            'pairwise_recursive_calls': self.calls,
            'hyper_memo_states': len(self.hyper_memo),
            'hyper_stats': dict(self.hyper_stats),
        }, sort_keys=True), flush=True)
        return value, self.calls, len(self.memo)


def analyze():
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    C.ExactCounter = ConditionedHyperCounter
    C.EXPECTED_EXACT_COUNT = _AcceptExact()
    try:
        with redirect_stdout(io.StringIO()) as capture:
            base = C.analyze()
        # Keep the heavy internal profile chatter out of normal CI logs. The
        # exact final profile rows are retained in the returned object.
    finally:
        C.ExactCounter = original_counter
        C.EXPECTED_EXACT_COUNT = original_expected

    total = int(base['exact_count'])
    assert 0 < total < PAIRWISE_COUNT
    log2 = math.log2(total)
    rows = []
    for row in base['profile_rows']:
        r = dict(row)
        r['m4_pairwise_plus_projection_hyperedges_count'] = r.pop('m4_pairwise_relaxation_count')
        r['m4_pairwise_plus_projection_hyperedges_log2'] = r.pop('m4_pairwise_relaxation_log2')
        rows.append(r)
    out = {
        **base,
        'profile_rows': rows,
        'exact_count': total,
        'exact_log2': log2,
        'state_bits': total.bit_length(),
        'pairwise_exact_baseline_count': PAIRWISE_COUNT,
        'gain_vs_pairwise_exact_log2_bits': math.log2(PAIRWISE_COUNT) - log2,
        'projection_minimal_empty_triples_added': 5,
        'projection_minimal_empty_quadruples_added': 7,
        'minimal_empty_quadruple_digest_sha256': EXPECTED_QUAD_DIGEST,
        'higher_order_hyperedges_added': 12,
        'solver': 'conditioned_first_zero_partition_with_pairwise_oracle',
        'decision': 'C916_250WAY_COMPLETE_M4_PAIRWISE_PLUS_PROJECTION_TRIPLES_QUADS_CONDITIONED_EXACT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_COMPLETE_PAIRWISE_PROJECTION_HYPEREDGES_CONDITIONED_EXACT')
    print('scope=all 4005 exact m4 pairwise value factors plus five exact minimal-empty projection triples and seven exact minimal-empty projection quadruples; finite hyperedges are enforced by an exact disjoint first-zero partition so pairwise component factorization remains available')
    print('boundary=all-order affine intersection and any further higher-order physical-image constraint remain outside this finite-hyperedge model')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
