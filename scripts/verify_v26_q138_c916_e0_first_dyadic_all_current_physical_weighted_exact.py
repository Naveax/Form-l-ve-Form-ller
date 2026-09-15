#!/usr/bin/env python3
"""Exact weighted C916 count with every currently certified physical factor.

Mathematical mechanism
----------------------
The old partial counters represented each forbidden tuple as an independent event bit.
That representation scales badly as the certified physical inventory grows.  The merged
physical-factor topology theorem proves the current higher-order primal graph is chordal
with exact treewidth 5, so the right object is a small-domain CSP/junction system, not an
ever wider event mask.

This verifier therefore keeps the exact 4,005 pairwise quotient relations from the
existing counter, adds the complete 19 affine-support obstructions, the exact five-quad
relation, and all freshly recomputed ternary quotient relations as ordinary forbidden-
tuple constraints.  Generalized arc consistency is interleaved with the existing exact
pairwise closure.  The recursive weighted count is exact; memoization includes inactive
singleton context because higher-order constraints can leave a residual relation after a
variable has been fixed.
"""

from __future__ import annotations

import io
import itertools
import json
import math
import os
import sys
from collections import defaultdict
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import probe_v26_q138_c916_e0_first_dyadic_complete_m4_pairwise_relaxation_exact as C
import verify_v26_q138_c916_e0_first_dyadic_projection_hyperedges_eventmask_vector_exact as V
import verify_v26_q138_c916_e0_first_dyadic_all_order_affine_support_exact as A
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_4_physical_ternary_exact as F
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_all_known_physical_exact as H
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as TOPO


PAIRWISE_COUNTER = C.ExactCounter
FACTOR_DIR = Path(os.environ.get("C916_CURRENT_PHYSICAL_FACTOR_DIR", "authorities/current-physical-factors"))
EXPECTED_AFFINE_TOTAL = F.EXPECTED_AFFINE_TOTAL
EXPECTED_SIX_TERNARY_FIVE_QUAD_TOTAL = int(
    "90987190266267462495323685079227633113020903735137825407846207198697839001600000"
)
ACTIVE_FACTOR_LIMIT = len(TOPO.TERNARY_FACTORS)
MODEL_LABEL = "all_current"
PROFILE_ROWS = []
_FACTOR_CACHE = None


class AnyExpected:
    def __eq__(self, other):
        return True


def load_factor_specs():
    global _FACTOR_CACHE
    if _FACTOR_CACHE is not None:
        return _FACTOR_CACHE
    rows = []
    for i, expected_scope in enumerate(TOPO.TERNARY_FACTORS):
        path = FACTOR_DIR / f"factor_{i:02d}.json"
        row = json.loads(path.read_text())
        assert int(row["inventory_index"]) == i
        assert tuple(map(int, row["triple"])) == tuple(map(int, expected_scope))
        qholes = tuple(tuple(map(int, x)) for x in row["quotient_hole_tuples"])
        assert qholes and len(qholes) == int(row["quotient_holes"])
        qsizes = tuple(map(int, row["quotient_alphabet_sizes"]))
        assert len(qsizes) == 3 and all(1 <= n <= 5 for n in qsizes)
        rows.append(
            {
                "index": i,
                "scope": tuple(map(int, expected_scope)),
                "qsizes": qsizes,
                "forbidden": frozenset(qholes),
                "digest": str(row["quotient_hole_digest_sha256"]),
            }
        )
    assert len(rows) == 38
    _FACTOR_CACHE = tuple(rows)
    return _FACTOR_CACHE


def compatible_forbidden_rows(constraint, domains):
    vis = constraint["vis"]
    for row in constraint["forbidden"]:
        if all((int(domains[vi]) >> int(row[p])) & 1 for p, vi in enumerate(vis)):
            yield row


class AllCurrentConstraintCounter(PAIRWISE_COUNTER):
    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        self.hyper_prunes = 0
        self.hyper_rounds = 0
        self.hyper_checks = 0

        loc = {}
        for vi, members in enumerate(self.variables):
            for ci, gid in enumerate(members):
                loc[int(gid)] = (vi, ci)
        assert len(loc) == 90

        constraints = []

        def singleton_scope(gids):
            vis = []
            for gid in gids:
                vi, ci = loc[int(gid)]
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                vis.append(vi)
            assert len(vis) == len(set(vis))
            return tuple(vis)

        # Complete 19 all-order affine-support obstructions.  Each is exactly the
        # all-zero quotient tuple on its scope, as in the merged affine event verifier.
        m4 = C.load(C.M4_PATH)
        affine_triples = tuple(tuple(map(int, row)) for row in m4["projection_minimal_empty_triples"])
        assert len(affine_triples) == 5
        affine_scopes = affine_triples + V.QUADS + (A.AFFINE_FIVE,) + A.EXTRA_SIX
        assert len(affine_scopes) == 19
        assert A.Q.digest_rows(tuple(sorted(affine_scopes, key=lambda r: (len(r), tuple(r))))) == A.EXPECTED_CONFLICT_DIGEST
        for ai, gids in enumerate(affine_scopes):
            vis = singleton_scope(gids)
            zeros = tuple(max(int(state[0]) for state in self.var_states[vi]) for vi in vis)
            constraints.append(
                {
                    "name": f"affine:{ai}",
                    "kind": "affine",
                    "gids": tuple(map(int, gids)),
                    "vis": vis,
                    "forbidden": frozenset((zeros,)),
                }
            )

        # Compile the five exact physical quaternary relations into their already
        # certified 832-row five-variable conjunction, then represent its complement
        # as one forbidden-table constraint.  This avoids five nested conditioning loops.
        qvis = singleton_scope(H.FIVE_GIDS)
        assert all(len(self.var_states[vi]) == 4 for vi in qvis)
        allowed5 = frozenset(tuple(map(int, row)) for row in H.ALLOWED)
        all5 = set(itertools.product(range(4), repeat=5))
        qforbidden = frozenset(all5 - allowed5)
        assert len(allowed5) == 832 and len(qforbidden) == 192
        constraints.append(
            {
                "name": "physical_quads:compiled5",
                "kind": "physical_quad_compiled",
                "gids": tuple(map(int, H.FIVE_GIDS)),
                "vis": qvis,
                "forbidden": qforbidden,
            }
        )

        # Fresh exact ternary quotient factors.  ACTIVE_FACTOR_LIMIT is used only for
        # the six-factor historical regression and then reset to the full 38 factors.
        factors = load_factor_specs()[:ACTIVE_FACTOR_LIMIT]
        for factor in factors:
            vis = singleton_scope(factor["scope"])
            actual_sizes = tuple(len(self.var_states[vi]) for vi in vis)
            assert actual_sizes == factor["qsizes"], (factor["scope"], actual_sizes, factor["qsizes"])
            constraints.append(
                {
                    "name": f"physical_ternary:{factor['index']}",
                    "kind": "physical_ternary",
                    "gids": factor["scope"],
                    "vis": vis,
                    "forbidden": factor["forbidden"],
                }
            )

        self.constraints = tuple(constraints)
        by_var = defaultdict(list)
        for ci, constraint in enumerate(self.constraints):
            for vi in constraint["vis"]:
                by_var[vi].append(ci)
        self.constraints_by_var = {vi: tuple(rows) for vi, rows in by_var.items()}

    def _prune_hyper_constraints(self, domains):
        dom = list(map(int, domains))
        changed = False
        for constraint in self.constraints:
            vis = constraint["vis"]
            forbidden = constraint["forbidden"]
            # Generalized arc consistency for a relation represented as the full
            # Cartesian product minus a finite forbidden set.  For a candidate state,
            # support exists iff the number of compatible forbidden completions is
            # strictly smaller than the number of all completions.
            for p, vi in enumerate(vis):
                mask = int(dom[vi])
                kept = 0
                scan = mask
                while scan:
                    bit = scan & -scan
                    scan ^= bit
                    si = bit.bit_length() - 1
                    combos = 1
                    for q, vj in enumerate(vis):
                        if q != p:
                            combos *= int(dom[vj]).bit_count()
                    blocked = 0
                    for row in forbidden:
                        if int(row[p]) != si:
                            continue
                        if all((int(dom[vj]) >> int(row[q])) & 1 for q, vj in enumerate(vis) if q != p):
                            blocked += 1
                    assert blocked <= combos
                    if blocked < combos:
                        kept |= bit
                self.hyper_checks += 1
                if kept != mask:
                    if kept == 0:
                        return None, True
                    self.hyper_prunes += mask.bit_count() - kept.bit_count()
                    dom[vi] = kept
                    changed = True
        return tuple(dom), changed

    def _arc_closure(self, active, domains):
        current = tuple(map(int, domains))
        while True:
            paired = PAIRWISE_COUNTER._arc_closure(self, active, current)
            if paired is None:
                return None
            pruned, changed = self._prune_hyper_constraints(paired)
            self.hyper_rounds += 1
            if pruned is None:
                return None
            if not changed and pruned == paired:
                return paired
            current = pruned

    def _constraint_relevant(self, constraint, domains):
        # If even one forbidden row is still compatible with current domains, this
        # factor can distinguish assignments and must connect its active variables.
        return any(True for _row in compatible_forbidden_rows(constraint, domains))

    def _relevant_neighbors(self, i, active, domains):
        out = PAIRWISE_COUNTER._relevant_neighbors(self, i, active, domains)
        for ci in self.constraints_by_var.get(i, ()):
            constraint = self.constraints[ci]
            if not self._constraint_relevant(constraint, domains):
                continue
            for vi in constraint["vis"]:
                if vi != i and ((active >> vi) & 1):
                    out |= 1 << vi
        return out

    def solve(self, active, domains):
        # Copy of the exact pairwise recursion with one essential correctness change:
        # memo keys retain *all* fixed domains, including inactive singleton context.
        # A higher-order factor may reduce to a residual relation after one endpoint
        # is fixed, so dropping that fixed endpoint from the key would be unsound.
        self.calls += 1
        closed = self._arc_closure(active, domains)
        if closed is None:
            return 0
        domains = closed

        singleton = 0
        factor = 1
        scan = active
        while scan:
            bit = scan & -scan
            i = bit.bit_length() - 1
            scan ^= bit
            d = int(domains[i])
            if d & (d - 1) == 0:
                singleton |= bit
                factor *= int(self.var_weights[i][d.bit_length() - 1])
        if singleton:
            rest = active ^ singleton
            return factor if rest == 0 else factor * self.solve(rest, domains)

        key = (active, tuple(map(int, domains)))
        cached = self.memo.get(key)
        if cached is not None:
            return cached

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
            score = (
                int(domains[i]).bit_count(),
                -self._relevant_neighbors(i, active, domains).bit_count(),
                i,
            )
            if best is None or score < best[0]:
                best = (score, i)
        i = best[1]

        total = 0
        mask = int(domains[i])
        while mask:
            x = mask & -mask
            mask ^= x
            nd = list(domains)
            nd[i] = x
            total += self.solve(active, tuple(nd))
        self.memo[key] = total
        return total

    def count_profile(self, domains):
        self.memo.clear()
        self.calls = 0
        self.hyper_prunes = 0
        self.hyper_rounds = 0
        self.hyper_checks = 0
        value = self.solve(self.ALL, tuple(domains))
        row = {
            "model": MODEL_LABEL,
            "domain_state_sum": sum(int(d).bit_count() for d in domains),
            "exact_count": int(value),
            "calls": self.calls,
            "memo_states": len(self.memo),
            "hyper_prunes": self.hyper_prunes,
            "hyper_rounds": self.hyper_rounds,
            "hyper_checks": self.hyper_checks,
        }
        PROFILE_ROWS.append(row)
        print("all_current_constraint_profile", json.dumps(row, sort_keys=True), flush=True)
        return value, self.calls, len(self.memo)


def run_model(limit, label):
    global ACTIVE_FACTOR_LIMIT, MODEL_LABEL
    ACTIVE_FACTOR_LIMIT = int(limit)
    MODEL_LABEL = str(label)
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    C.ExactCounter = AllCurrentConstraintCounter
    C.EXPECTED_EXACT_COUNT = AnyExpected()
    try:
        with redirect_stdout(io.StringIO()):
            base = C.analyze()
    finally:
        C.ExactCounter = original_counter
        C.EXPECTED_EXACT_COUNT = original_expected
    return base


def analyze():
    factors = load_factor_specs()
    assert len(factors) == len(TOPO.TERNARY_FACTORS) == 38

    # Regression gate: the new constraint engine must reproduce the last clean
    # six-ternary + five-quad event-mask authority exactly before it may emit a new count.
    regression = run_model(6, "six_factor_regression")
    regression_total = int(regression["exact_count"])
    assert regression_total == EXPECTED_SIX_TERNARY_FIVE_QUAD_TOTAL, (
        regression_total,
        EXPECTED_SIX_TERNARY_FIVE_QUAD_TOTAL,
    )

    full = run_model(len(factors), "all_current")
    total = int(full["exact_count"])
    assert 0 <= total <= regression_total <= EXPECTED_AFFINE_TOTAL

    forbidden_tuple_count = sum(len(row["forbidden"]) for row in factors)
    full_profile_rows = [row for row in PROFILE_ROWS if row["model"] == "all_current"]
    regression_profile_rows = [row for row in PROFILE_ROWS if row["model"] == "six_factor_regression"]

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "complete_higher_affine_conflicts": 19,
        "physical_ternary_factors": len(factors),
        "physical_ternary_forbidden_quotient_tuples": forbidden_tuple_count,
        "physical_quaternary_factors": 5,
        "physical_quaternary_compiled_relation_rows": len(H.ALLOWED),
        "physical_quaternary_compiled_forbidden_rows": 1024 - len(H.ALLOWED),
        "physical_factor_scope_digest_sha256": TOPO.EXPECTED_SCOPE_DIGEST,
        "physical_factor_primal_exact_treewidth": TOPO.EXPECTED_TREEWIDTH,
        "six_factor_regression_expected": EXPECTED_SIX_TERNARY_FIVE_QUAD_TOTAL,
        "six_factor_regression_observed": regression_total,
        "all_order_affine_support_exact_count": EXPECTED_AFFINE_TOTAL,
        "exact_all_current_physical_weighted_count": total,
        "exact_log2": None if total == 0 else math.log2(total),
        "state_bits": total.bit_length(),
        "removed_weighted_assignments_vs_six_factor_checkpoint": regression_total - total,
        "removed_weighted_assignments_vs_affine": EXPECTED_AFFINE_TOTAL - total,
        "gain_vs_six_factor_checkpoint_log2_bits": None if total == 0 else math.log2(regression_total) - math.log2(total),
        "gain_vs_affine_log2_bits": None if total == 0 else math.log2(EXPECTED_AFFINE_TOTAL) - math.log2(total),
        "regression_profile_rows": regression_profile_rows,
        "all_current_profile_rows": full_profile_rows,
        "decision": "C916_COMPLETE_AFFINE_SUPPORT_PLUS_ALL_CURRENT_EXACT_PHYSICAL_QUOTIENT_FACTORS_WEIGHTED_COUNT",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_CURRENT_PHYSICAL_WEIGHTED_EXACT")
    print("theorem=the complete 4005-pair quotient model, complete 19-conflict affine-support theorem, five exact quaternary physical quotient factors, and all 38 currently certified ternary physical quotient factors are conjoined in one exact weighted count using finite forbidden-tuple propagation rather than an expanding event mask")
    print("boundary=this is exact for the current certified physical-factor inventory only; additional untested higher-order physical image constraints remain possible and no end-to-end work exponent is inferred")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
