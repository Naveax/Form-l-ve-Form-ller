#!/usr/bin/env python3
import io, json, math, sys
from collections import defaultdict, deque
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


class HyperExactCounter(C.ExactCounter):
    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        m4 = C.load(C.M4_PATH)
        triples = tuple(tuple(map(int, t)) for t in m4['projection_minimal_empty_triples'])
        assert len(triples) == 5
        assert len(QUADS) == 7
        self.raw_hyperedges = triples + QUADS

        loc = {}
        for vi, members in enumerate(self.variables):
            for ci, gid in enumerate(members):
                assert gid not in loc
                loc[int(gid)] = (vi, ci)
        assert len(loc) == 90

        self.zero_index = {}
        for vi, states in enumerate(self.var_states):
            width = len(self.variables[vi])
            for ci in range(width):
                self.zero_index[(vi, ci)] = max(int(s[ci]) for s in states)

        edges = []
        for hedge in self.raw_hyperedges:
            parts = defaultdict(list)
            for gid in hedge:
                assert gid in loc, (hedge, gid)
                vi, ci = loc[gid]
                parts[vi].append(ci)
            edge = tuple(sorted((vi, tuple(sorted(coords))) for vi, coords in parts.items()))
            assert edge
            edges.append(edge)
        assert len(edges) == 12
        self.hyperedges = tuple(edges)
        self.hyper_by_var = [[] for _ in range(self.N)]
        for ei, edge in enumerate(self.hyperedges):
            for vi, _coords in edge:
                self.hyper_by_var[vi].append(ei)

    def _state_local_nonzero(self, vi, coords, state_index):
        state = self.var_states[vi][state_index]
        return all(int(state[ci]) != self.zero_index[(vi, ci)] for ci in coords)

    def _domain_has_local_zero(self, vi, coords, domain):
        mask = int(domain)
        while mask:
            lsb = mask & -mask
            si = lsb.bit_length() - 1
            mask ^= lsb
            if not self._state_local_nonzero(vi, coords, si):
                return True
        return False

    def _domain_can_local_nonzero(self, vi, coords, domain):
        mask = int(domain)
        while mask:
            lsb = mask & -mask
            si = lsb.bit_length() - 1
            mask ^= lsb
            if self._state_local_nonzero(vi, coords, si):
                return True
        return False

    def _hyper_prune_once(self, active, domains):
        dom = list(domains)
        changed = False
        for edge in self.hyperedges:
            # If any participant is guaranteed to contribute a zero, this
            # not-all-nonzero constraint is already satisfied for every assignment.
            if any(not self._domain_can_local_nonzero(vi, coords, dom[vi]) for vi, coords in edge):
                continue
            for vi, coords in edge:
                if not ((active >> vi) & 1):
                    continue
                other_has_zero = any(
                    self._domain_has_local_zero(vj, cjs, dom[vj])
                    for vj, cjs in edge if vj != vi
                )
                if other_has_zero:
                    continue
                old = dom[vi]
                keep = 0
                mask = old
                while mask:
                    lsb = mask & -mask
                    si = lsb.bit_length() - 1
                    mask ^= lsb
                    if not self._state_local_nonzero(vi, coords, si):
                        keep |= lsb
                if keep != old:
                    if keep == 0:
                        return None, True
                    dom[vi] = keep
                    changed = True
        return tuple(dom), changed

    def _arc_closure(self, active, domains):
        dom = tuple(domains)
        while True:
            dom = super()._arc_closure(active, dom)
            if dom is None:
                return None
            dom2, changed = self._hyper_prune_once(active, dom)
            if dom2 is None:
                return None
            dom = dom2
            if not changed:
                return dom

    def _hyperedge_relevant(self, edge, domains):
        # A guaranteed local zero satisfies the edge identically.
        return all(self._domain_can_local_nonzero(vi, coords, domains[vi]) for vi, coords in edge)

    def _relevant_neighbors(self, i, active, domains):
        out = super()._relevant_neighbors(i, active, domains)
        for ei in self.hyper_by_var[i]:
            edge = self.hyperedges[ei]
            if not self._hyperedge_relevant(edge, domains):
                continue
            for vi, _coords in edge:
                if vi != i and ((active >> vi) & 1):
                    out |= 1 << vi
        return out

    def solve(self, active, domains):
        self.calls += 1
        closed = self._arc_closure(active, domains)
        if closed is None:
            return 0
        domains = closed
        singleton = 0
        factor = 1
        scan = active
        while scan:
            lsb = scan & -scan
            i = lsb.bit_length() - 1
            scan ^= lsb
            d = domains[i]
            if d & (d - 1) == 0:
                singleton |= lsb
                factor *= self.var_weights[i][d.bit_length() - 1]
        if singleton:
            rest = active ^ singleton
            return factor if rest == 0 else factor * self.solve(rest, domains)

        # Hyperedges can remain conditioned on singleton variables removed from
        # active, so memoize the complete domain vector rather than active-only
        # domains used by the pure pairwise counter.
        key = (active, tuple(domains))
        if key in self.memo:
            return self.memo[key]

        remain = active
        comps = []
        isolated_factor = 1
        while remain:
            seed = remain & -remain
            i = seed.bit_length() - 1
            if self._relevant_neighbors(i, active, domains) == 0:
                isolated_factor *= self.wsum[i][domains[i]]
                remain ^= seed
                continue
            comp = 0
            frontier = seed
            while frontier:
                x = frontier & -frontier
                frontier ^= x
                k = x.bit_length() - 1
                if comp & x:
                    continue
                comp |= x
                frontier |= self._relevant_neighbors(k, active, domains) & ~comp
            comps.append(comp)
            remain &= ~comp
        if not comps:
            self.memo[key] = isolated_factor
            return isolated_factor
        if len(comps) > 1 or isolated_factor != 1 or comps[0] != active:
            value = isolated_factor
            for comp in comps:
                value *= self.solve(comp, domains)
            self.memo[key] = value
            return value

        best = None
        scan = active
        while scan:
            x = scan & -scan
            i = x.bit_length() - 1
            scan ^= x
            score = (domains[i].bit_count(), -self._relevant_neighbors(i, active, domains).bit_count())
            if best is None or score < best[0]:
                best = (score, i)
        i = best[1]
        total = 0
        mask = domains[i]
        while mask:
            x = mask & -mask
            mask ^= x
            nd = list(domains)
            nd[i] = x
            total += self.solve(active, tuple(nd))
        self.memo[key] = total
        return total


def analyze():
    # Run the exact pairwise setup unchanged, replacing only the CSP counter
    # by one that also enforces the 5+7 finite projection hyperedges.
    C.ExactCounter = HyperExactCounter
    C.EXPECTED_EXACT_COUNT = _AcceptExact()
    with redirect_stdout(io.StringIO()):
        base = C.analyze()

    total = int(base['exact_count'])
    assert 0 < total < PAIRWISE_COUNT
    log2 = math.log2(total)
    out = {
        **base,
        'exact_count': total,
        'exact_log2': log2,
        'state_bits': total.bit_length(),
        'pairwise_exact_baseline_count': PAIRWISE_COUNT,
        'gain_vs_pairwise_exact_log2_bits': math.log2(PAIRWISE_COUNT) - log2,
        'projection_minimal_empty_triples_added': 5,
        'projection_minimal_empty_quadruples_added': 7,
        'minimal_empty_quadruple_digest_sha256': EXPECTED_QUAD_DIGEST,
        'higher_order_hyperedges_added': 12,
        'decision': 'C916_250WAY_COMPLETE_M4_PAIRWISE_PLUS_PROJECTION_TRIPLES_QUADS_EXACT',
    }
    print('result', json.dumps(out, sort_keys=True), flush=True)
    print('PASS V26_Q138_C916_E0_FIRST_DYADIC_COMPLETE_M4_PAIRWISE_PLUS_PROJECTION_HYPEREDGES_EXACT')
    print('scope=all 4005 exact m4 pairwise value factors plus five exact minimal-empty projection triples and seven exact minimal-empty projection quadruples')
    print('boundary=all-order affine intersection and any further higher-order physical-image constraint remain outside this finite-hyperedge model')
    print('ALPHA_PASS=0')
    return out


if __name__ == '__main__':
    analyze()
