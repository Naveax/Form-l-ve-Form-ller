#!/usr/bin/env python3
"""Exact C916 weighted count with profile-safe conservative higher-order context.

The engine caches local higher-order support evaluations, but memoized weighted states are
never shared across distinct separator-domain profiles.  Within one profile, every active
variable and every variable that participates in any higher-order constraint is retained in
the memo projection.  This is deliberately conservative: pairwise-only inactive variables
may be dropped after pairwise closure, while no residual higher-order endpoint can disappear
from the cache key.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _c916_all_current_weighted_context_engine as E


class ProfileSafeConstraintCounter(E.ContextMinimizedConstraintCounter):
    """Context-cached counter with separator-profile isolation and static hyper context."""

    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        hyper_context = 0
        for constraint in self.constraints:
            hyper_context |= int(constraint["active_mask"])
        self.hyper_context_mask = hyper_context
        self.hyper_context_variables = hyper_context.bit_count()

    def _memo_key(self, active, domains):
        context = int(active) | self.hyper_context_mask
        self.max_context_variables = max(self.max_context_variables, context.bit_count())
        projected = tuple(int(domains[i]) for i in range(self.N) if (context >> i) & 1)
        return active, context, projected

    def count_profile(self, domains):
        # Separator profiles have different unary-domain boundary conditions.  Reusing a
        # memo entry across profiles is unsound once inactive pairwise-only variables have
        # been projected out, even when the active/hyper projection happens to collide.
        self.memo.clear()
        return super().count_profile(domains)


def run_model(limit, label):
    original = E.ContextMinimizedConstraintCounter
    E.ContextMinimizedConstraintCounter = ProfileSafeConstraintCounter
    try:
        return E.run_model(limit, label)
    finally:
        E.ContextMinimizedConstraintCounter = original


def analyze():
    E.PROFILE_ROWS.clear()
    factors = E.load_factor_specs()
    assert len(factors) == len(E.TOPO.TERNARY_FACTORS) == 38

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
        "decision": "C916_COMPLETE_AFFINE_SUPPORT_PLUS_ALL_CURRENT_EXACT_PHYSICAL_QUOTIENT_FACTORS_WEIGHTED_COUNT_PROFILE_SAFE_CONTEXT",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_CURRENT_PHYSICAL_WEIGHTED_CONTEXT_EXACT")
    print("theorem=the complete 4005-pair quotient model, complete 19-conflict affine-support theorem, five exact quaternary physical quotient factors, and all 38 current ternary physical quotient factors are conjoined in one exact weighted count; memoization is isolated per separator profile and retains every higher-order endpoint")
    print("boundary=this is exact for the current certified physical-factor inventory only; additional untested higher-order physical image constraints remain possible and no end-to-end work exponent is inferred")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
