#!/usr/bin/env python3
"""Exact C916 weighted count with authority-correct affine support semantics.

The current physical factor engine is retained, but affine-support scopes use the exact
activity obstruction semantics certified by the event-mask authorities: an affine scope
is forbidden only when every endpoint is in a nonzero quotient state. The local zero
state is the maximal quotient-state index. This is not the all-zero forbidden tuple.

Memoized weighted states remain isolated per separator-domain profile, and every active
variable plus every higher-order endpoint remains in the memo projection. Those choices
are conservative execution policy; they do not alter the mathematical relation layer.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _c916_all_current_weighted_context_engine as E


class AuthorityCorrectConstraintCounter(E.ContextMinimizedConstraintCounter):
    """Context-cached counter with exact affine activity-obstruction semantics."""

    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        hyper_context = 0
        for constraint in self.constraints:
            hyper_context |= int(constraint["active_mask"])
        self.hyper_context_mask = hyper_context
        self.hyper_context_variables = hyper_context.bit_count()

    def _evaluate_constraint(self, ci, domains):
        constraint = self.constraints[ci]
        if not str(constraint["name"]).startswith("affine:"):
            return super()._evaluate_constraint(ci, domains)

        vis = constraint["vis"]
        projected = tuple(int(domains[vi]) for vi in vis)
        key = (ci, projected)
        cached = self.constraint_eval_cache.get(key)
        if cached is not None:
            self.constraint_eval_hits += 1
            return cached
        self.constraint_eval_misses += 1

        # The certified event-mask theorem clears an affine conflict as soon as any
        # endpoint takes its zero quotient state. Therefore the forbidden relation is
        # the Cartesian product of NONZERO states, not the singleton all-zero tuple.
        # The base engine stores the zero-state tuple only as compact metadata here.
        zero_row = next(iter(constraint["forbidden"]))
        assert len(zero_row) == len(vis)
        nonzero_counts = []
        for p, domain in enumerate(projected):
            zero = int(zero_row[p])
            assert 0 <= zero < len(self.var_states[vis[p]])
            nonzero_counts.append((int(domain) & ~(1 << zero)).bit_count())

        compatible = math.prod(nonzero_counts)
        supported = []
        for p, domain in enumerate(projected):
            zero = int(zero_row[p])
            zero_bit = 1 << zero
            kept = int(domain) & zero_bit
            nonzero_domain = int(domain) & ~zero_bit
            if nonzero_domain:
                all_other = 1
                blocked_other = 1
                for q, other_domain in enumerate(projected):
                    if q == p:
                        continue
                    all_other *= int(other_domain).bit_count()
                    blocked_other *= nonzero_counts[q]
                # A nonzero candidate has support iff at least one completion contains
                # a zero state at another endpoint. If every completion is nonzero,
                # every completion belongs to the affine forbidden relation.
                if blocked_other < all_other:
                    kept |= nonzero_domain
            supported.append(kept)

        result = (int(compatible), tuple(supported))
        self.constraint_eval_cache[key] = result
        return result

    def _memo_key(self, active, domains):
        context = int(active) | self.hyper_context_mask
        self.max_context_variables = max(self.max_context_variables, context.bit_count())
        projected = tuple(int(domains[i]) for i in range(self.N) if (context >> i) & 1)
        return active, context, projected

    def count_profile(self, domains):
        # Profiles carry different unary boundary conditions. Keeping their weighted
        # memo tables separate is conservative and matches the historical exact count.
        self.memo.clear()
        return super().count_profile(domains)


def run_model(limit, label):
    original = E.ContextMinimizedConstraintCounter
    E.ContextMinimizedConstraintCounter = AuthorityCorrectConstraintCounter
    try:
        return E.run_model(limit, label)
    finally:
        E.ContextMinimizedConstraintCounter = original


def analyze():
    E.PROFILE_ROWS.clear()
    factors = E.load_factor_specs()
    assert len(factors) == len(E.TOPO.TERNARY_FACTORS) == 38
    assert tuple(f["scope"] for f in factors[:6]) == (
        (5, 181, 182),
        (11, 12, 24),
        (62, 67, 104),
        (111, 112, 113),
        (69, 82, 87),
        (130, 131, 132),
    )

    regression = run_model(6, "six_factor_regression")
    regression_total = int(regression["exact_count"])
    assert regression_total == E.EXPECTED_SIX_TERNARY_FIVE_QUAD_TOTAL, (
        regression_total,
        E.EXPECTED_SIX_TERNARY_FIVE_QUAD_TOTAL,
    )

    full = run_model(len(factors), "all_current")
    total = int(full["exact_count"])
    assert 0 <= total <= regression_total <= E.EXPECTED_AFFINE_TOTAL

    forbidden_tuple_count = sum(len(row["forbidden"]) for row in factors)
    full_profile_rows = [row for row in E.PROFILE_ROWS if row["model"] == "all_current"]
    regression_profile_rows = [row for row in E.PROFILE_ROWS if row["model"] == "six_factor_regression"]
    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "complete_higher_affine_conflicts": 19,
        "affine_constraint_semantics": "each certified affine-support scope forbids the all-nonzero activity relation; the maximal local quotient-state index is zero",
        "physical_ternary_factors": len(factors),
        "physical_ternary_forbidden_quotient_tuples": forbidden_tuple_count,
        "physical_quaternary_factors": 5,
        "physical_quaternary_compiled_relation_rows": len(E.H.ALLOWED),
        "physical_quaternary_compiled_forbidden_rows": 1024 - len(E.H.ALLOWED),
        "physical_factor_scope_digest_sha256": E.TOPO.EXPECTED_SCOPE_DIGEST,
        "six_factor_regression_expected": E.EXPECTED_SIX_TERNARY_FIVE_QUAD_TOTAL,
        "six_factor_regression_observed": regression_total,
        "all_order_affine_support_exact_count": E.EXPECTED_AFFINE_TOTAL,
        "exact_all_current_physical_weighted_count": total,
        "exact_log2": None if total == 0 else math.log2(total),
        "state_bits": total.bit_length(),
        "removed_weighted_assignments_vs_six_factor_checkpoint": regression_total - total,
        "removed_weighted_assignments_vs_affine": E.EXPECTED_AFFINE_TOTAL - total,
        "gain_vs_six_factor_checkpoint_log2_bits": None if total == 0 else math.log2(regression_total) - math.log2(total),
        "gain_vs_affine_log2_bits": None if total == 0 else math.log2(E.EXPECTED_AFFINE_TOTAL) - math.log2(total),
        "memo_context_policy": "active variables union all higher-order variables; memo reset per separator-domain profile",
        "regression_profile_rows": regression_profile_rows,
        "all_current_profile_rows": full_profile_rows,
        "decision": "C916_COMPLETE_AFFINE_SUPPORT_PLUS_ALL_CURRENT_EXACT_PHYSICAL_QUOTIENT_FACTORS_WEIGHTED_COUNT_AUTHORITY_CORRECT",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_CURRENT_PHYSICAL_WEIGHTED_CONTEXT_EXACT")
    print("theorem=the complete pairwise quotient model, complete 19-scope affine all-nonzero activity obstruction theorem, five exact quaternary physical quotient factors, and all 38 current ternary physical quotient factors are conjoined in one exact weighted count; the six-factor historical authority is an exact regression gate")
    print("boundary=this is exact for the current certified physical-factor inventory only; the pairwise layer still uses the repository's stated 1125 zero-cross activity-only relations, additional untested higher-order physical image constraints remain possible, and no end-to-end work exponent is inferred")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
