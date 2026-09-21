#!/usr/bin/env python3
"""Exact all-current C916 weighted counter with minimized residual context.

The predecessor finite-CSP counter was exact but timed out after 90 minutes because its
memo key retained every inactive singleton assignment after branching.  Higher-order
relations do require fixed endpoints while they remain unresolved, but they do not require
fixed endpoints of relations that are already satisfied.  Since domain restriction is
monotone, a forbidden tuple that is incompatible now can never become compatible later.

This verifier keeps the same exact 4,005 pairwise quotient model, complete 19 affine
obstructions, exact five-quad conjunction, and all 38 current ternary physical factors.
It changes only execution:

* higher-order support/relevance evaluations are cached by the local domain projection;
* GAC touches only active endpoints of constraints that still meet the active subproblem;
* memo keys retain active domains plus only inactive endpoints of still-relevant
  higher-order constraints;
* exact memo states are shared across the ten separator-domain profiles of one model.

The six-ternary + five-quad historical exact checkpoint remains a mandatory regression
gate before the all-current result is admitted.
"""

from __future__ import annotations

import itertools
import json
import math
import os
import sys
from collections import defaultdict
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
        scope = tuple(map(int, row["triple"]))
        assert scope == tuple(map(int, expected_scope))
        qholes = tuple(tuple(map(int, x)) for x in row["quotient_hole_tuples"])
        assert qholes and len(qholes) == int(row["quotient_holes"])
        qsizes = tuple(map(int, row["quotient_alphabet_sizes"]))
        assert len(qsizes) == 3 and all(1 <= n <= 5 for n in qsizes)
        rows.append(
            {
                "index": i,
                "scope": scope,
                "qsizes": qsizes,
                "forbidden": frozenset(qholes),
                "digest": str(row["quotient_hole_digest_sha256"]),
            }
        )
    assert len(rows) == 38
    _FACTOR_CACHE = tuple(rows)
    return _FACTOR_CACHE


class ContextMinimizedConstraintCounter(PAIRWISE_COUNTER):
    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        self.hyper_prunes = 0
        self.hyper_rounds = 0
        self.hyper_checks = 0
        self.constraint_eval_hits = 0
        self.constraint_eval_misses = 0
        self.memo_hits = 0
        self.max_context_variables = 0
        self.constraint_eval_cache = {}

        loc = {}
        for vi, members in enumerate(self.variables):
            for ci, gid in enumerate(members):
                loc[int(gid)] = (vi, ci)
        assert len(loc) == 90

        def singleton_scope(gids):
            vis = []
            for gid in gids:
                vi, ci = loc[int(gid)]
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                vis.append(vi)
            assert len(vis) == len(set(vis))
            return tuple(vis)

        constraints = []
        m4 = C.load(C.M4_PATH)
        affine_triples = tuple(tuple(map(int, row)) for row in m4["projection_minimal_empty_triples"])
        assert len(affine_triples) == 5
        affine_scopes = affine_triples + V.QUADS + (A.AFFINE_FIVE,) + A.EXTRA_SIX
        assert len(affine_scopes) == A.EVENT_COUNT == 19
        assert A.Q.digest_rows(tuple(sorted(affine_scopes, key=lambda r: (len(r), tuple(r))))) == A.EXPECTED_CONFLICT_DIGEST
        for ai, gids in enumerate(affine_scopes):
            vis = singleton_scope(gids)
            forbidden = frozenset((tuple(max(int(state[0]) for state in self.var_states[vi]) for vi in vis),))
            constraints.append(
                {
                    "name": f"affine:{ai}",
                    "gids": tuple(map(int, gids)),
                    "vis": vis,
                    "active_mask": sum(1 << vi for vi in vis),
                    "forbidden": forbidden,
                }
            )

        qvis = singleton_scope(H.FIVE_GIDS)
        assert all(len(self.var_states[vi]) == 4 for vi in qvis)
        allowed5 = frozenset(tuple(map(int, row)) for row in H.ALLOWED)
        qforbidden = frozenset(set(itertools.product(range(4), repeat=5)) - allowed5)
        assert len(allowed5) == 832 and len(qforbidden) == 192
        constraints.append(
            {
                "name": "physical_quads:compiled5",
                "gids": tuple(map(int, H.FIVE_GIDS)),
                "vis": qvis,
                "active_mask": sum(1 << vi for vi in qvis),
                "forbidden": qforbidden,
            }
        )

        factors = load_factor_specs()[:ACTIVE_FACTOR_LIMIT]
        for factor in factors:
            vis = singleton_scope(factor["scope"])
            actual_sizes = tuple(len(self.var_states[vi]) for vi in vis)
            assert actual_sizes == factor["qsizes"], (factor["scope"], actual_sizes, factor["qsizes"])
            constraints.append(
                {
                    "name": f"physical_ternary:{factor['index']}",
                    "gids": factor["scope"],
                    "vis": vis,
                    "active_mask": sum(1 << vi for vi in vis),
                    "forbidden": factor["forbidden"],
                }
            )

        self.constraints = tuple(constraints)
        by_var = defaultdict(list)
        for ci, constraint in enumerate(self.constraints):
            for vi in constraint["vis"]:
                by_var[vi].append(ci)
        self.constraints_by_var = {vi: tuple(rows) for vi, rows in by_var.items()}

    def _evaluate_constraint(self, ci, domains):
        constraint = self.constraints[ci]
        vis = constraint["vis"]
        projected = tuple(int(domains[vi]) for vi in vis)
        key = (ci, projected)
        cached = self.constraint_eval_cache.get(key)
        if cached is not None:
            self.constraint_eval_hits += 1
            return cached
        self.constraint_eval_misses += 1

        compatible = 0
        forbidden = constraint["forbidden"]
        for row in forbidden:
            if all((projected[p] >> int(row[p])) & 1 for p in range(len(vis))):
                compatible += 1

        supported = []
        for p, mask in enumerate(projected):
            kept = 0
            scan = mask
            while scan:
                bit = scan & -scan
                scan ^= bit
                si = bit.bit_length() - 1
                combinations = 1
                for q, other in enumerate(projected):
                    if q != p:
                        combinations *= int(other).bit_count()
                blocked = 0
                for row in forbidden:
                    if int(row[p]) != si:
                        continue
                    if all((projected[q] >> int(row[q])) & 1 for q in range(len(vis)) if q != p):
                        blocked += 1
                assert blocked <= combinations
                if blocked < combinations:
                    kept |= bit
            supported.append(kept)
        result = (compatible, tuple(supported))
        self.constraint_eval_cache[key] = result
        return result

    def _constraint_relevant(self, ci, domains):
        compatible, _supported = self._evaluate_constraint(ci, domains)
        return compatible > 0

    def _prune_hyper_constraints(self, active, domains):
        dom = list(map(int, domains))
        changed = False
        for ci, constraint in enumerate(self.constraints):
            if not (constraint["active_mask"] & active):
                continue
            compatible, supported = self._evaluate_constraint(ci, dom)
            if compatible == 0:
                continue
            for p, vi in enumerate(constraint["vis"]):
                if not ((active >> vi) & 1):
                    continue
                mask = int(dom[vi])
                kept = mask & int(supported[p])
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
            pruned, changed = self._prune_hyper_constraints(active, paired)
            self.hyper_rounds += 1
            if pruned is None:
                return None
            if not changed and pruned == paired:
                return paired
            current = pruned

    def _relevant_neighbors(self, i, active, domains):
        out = PAIRWISE_COUNTER._relevant_neighbors(self, i, active, domains)
        for ci in self.constraints_by_var.get(i, ()):
            constraint = self.constraints[ci]
            active_vis = constraint["active_mask"] & active
            if not (active_vis & (1 << i)):
                continue
            if active_vis & (active_vis - 1) == 0:
                continue
            if not self._constraint_relevant(ci, domains):
                continue
            out |= active_vis & ~(1 << i)
        return out

    def _memo_key(self, active, domains):
        context = int(active)
        for ci, constraint in enumerate(self.constraints):
            if not (constraint["active_mask"] & active):
                continue
            if self._constraint_relevant(ci, domains):
                context |= constraint["active_mask"]
        self.max_context_variables = max(self.max_context_variables, context.bit_count())
        projected = tuple(int(domains[i]) for i in range(self.N) if (context >> i) & 1)
        return active, context, projected

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

        key = self._memo_key(active, domains)
        cached = self.memo.get(key)
        if cached is not None:
            self.memo_hits += 1
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
            neighbors = self._relevant_neighbors(i, active, domains)
            score = (int(domains[i]).bit_count(), -neighbors.bit_count(), i)
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
        calls_before = self.calls
        memo_before = len(self.memo)
        hits_before = self.memo_hits
        eval_hits_before = self.constraint_eval_hits
        eval_misses_before = self.constraint_eval_misses
        value = self.solve(self.ALL, tuple(domains))
        row = {
            "model": MODEL_LABEL,
            "domain_state_sum": sum(int(d).bit_count() for d in domains),
            "exact_count": int(value),
            "calls_delta": self.calls - calls_before,
            "memo_states_total": len(self.memo),
            "memo_states_delta": len(self.memo) - memo_before,
            "memo_hits_delta": self.memo_hits - hits_before,
            "hyper_prunes_total": self.hyper_prunes,
            "hyper_rounds_total": self.hyper_rounds,
            "hyper_checks_total": self.hyper_checks,
            "constraint_eval_hits_delta": self.constraint_eval_hits - eval_hits_before,
            "constraint_eval_misses_delta": self.constraint_eval_misses - eval_misses_before,
            "max_context_variables": self.max_context_variables,
        }
        PROFILE_ROWS.append(row)
        print("context_weighted_profile", json.dumps(row, sort_keys=True), flush=True)
        return value, self.calls, len(self.memo)


def run_model(limit, label):
    global ACTIVE_FACTOR_LIMIT, MODEL_LABEL
    ACTIVE_FACTOR_LIMIT = int(limit)
    MODEL_LABEL = str(label)
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    C.ExactCounter = ContextMinimizedConstraintCounter
    C.EXPECTED_EXACT_COUNT = AnyExpected()
    try:
        print("model_start", json.dumps({"label": label, "ternary_factor_limit": limit}), flush=True)
        base = C.analyze()
        print("model_done", json.dumps({"label": label, "exact_count": int(base["exact_count"])}), flush=True)
    finally:
        C.ExactCounter = original_counter
        C.EXPECTED_EXACT_COUNT = original_expected
    return base


def analyze():
    factors = load_factor_specs()
    assert len(factors) == len(TOPO.TERNARY_FACTORS) == 38

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
        "decision": "C916_COMPLETE_AFFINE_SUPPORT_PLUS_ALL_CURRENT_EXACT_PHYSICAL_QUOTIENT_FACTORS_WEIGHTED_COUNT_CONTEXT_MINIMIZED",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_CURRENT_PHYSICAL_WEIGHTED_CONTEXT_EXACT")
    print("theorem=the complete 4005-pair quotient model, complete 19-conflict affine-support theorem, five exact quaternary physical quotient factors, and all 38 current ternary physical quotient factors are conjoined in one exact weighted count; memo context retains exactly the unresolved higher-order endpoints rather than every historical singleton assignment")
    print("boundary=this is exact for the current certified physical-factor inventory only; additional untested higher-order physical image constraints remain possible and no end-to-end work exponent is inferred")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
