#!/usr/bin/env python3
"""Exact all-current C916 weighted counter using compiled higher-order clique bitsets.

This is a structurally independent execution fallback for the exact weighted target.  The
mathematics is unchanged: the complete 4,005-pair quotient model, complete 19 affine
support obstructions, exact conjunction of the five physical quaternary factors, and the
current 38 exact physical ternary factors are all enforced.

Instead of rescanning forbidden tuples during recursion, higher-order constraints assigned
to the same certified width-9 clique are conjoined once into a compact local relation.
Only variables actually mentioned by those assigned constraints are retained; chordal fill
variables are not introduced into the runtime factor.  Each allowed local row is indexed
by Python-integer bitsets for every variable/state.  Runtime GAC and relevance tests then
reduce to bitwise intersections.

The historical six-ternary + five-quad exact checkpoint remains a mandatory regression
gate before the all-current result may be admitted.  No approximation is used.
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
import verify_v26_q138_c916_e0_first_dyadic_all_order_affine_support_exact as A
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_4_physical_ternary_exact as F
import verify_v26_q138_c916_e0_first_dyadic_affine_plus_all_known_physical_exact as H
import verify_v26_q138_c916_e0_first_dyadic_all_current_physical_hypergraph_treewidth_exact as TOPO
import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_treewidth_exact as W
import verify_v26_q138_c916_e0_first_dyadic_current_physical_plus_affine_junction_compiler_exact as J

PAIRWISE_COUNTER = C.ExactCounter
FACTOR_DIR = Path(os.environ.get("C916_CURRENT_PHYSICAL_FACTOR_DIR", "authorities/current-physical-factors"))
EXPECTED_AFFINE_TOTAL = F.EXPECTED_AFFINE_TOTAL
EXPECTED_SIX_TERNARY_FIVE_QUAD_TOTAL = int(
    "90987190266267462495323685079227633113020903735137825407846207198697839001600000"
)
ACTIVE_FACTOR_LIMIT = len(TOPO.TERNARY_FACTORS)
MODEL_LABEL = "all_current"
PROFILE_ROWS = []
_MODEL_RELATION_CACHE = {}


class AnyExpected:
    def __eq__(self, other):
        return True


def load_factor_specs():
    rows = []
    for i, expected_scope in enumerate(TOPO.TERNARY_FACTORS):
        row = json.loads((FACTOR_DIR / f"factor_{i:02d}.json").read_text())
        assert int(row["inventory_index"]) == i
        scope = tuple(map(int, row["triple"]))
        assert scope == tuple(map(int, expected_scope))
        forbidden = frozenset(tuple(map(int, x)) for x in row["quotient_hole_tuples"])
        qsizes = tuple(map(int, row["quotient_alphabet_sizes"]))
        assert forbidden and len(forbidden) == int(row["quotient_holes"])
        rows.append(
            {
                "index": i,
                "scope": scope,
                "qsizes": qsizes,
                "forbidden": forbidden,
                "digest": str(row["quotient_hole_digest_sha256"]),
            }
        )
    assert len(rows) == 38
    return tuple(rows)


def compile_model_relations(limit):
    limit = int(limit)
    cached = _MODEL_RELATION_CACHE.get(limit)
    if cached is not None:
        return cached

    qsizes = J.quotient_sizes()
    cliques, fill_edges = J.elimination_cliques(W.all_scopes())
    assert len(fill_edges) == W.EXPECTED_FILL_EDGE_COUNT == 13
    assert max(map(len, cliques)) == W.EXPECTED_TREEWIDTH + 1 == 10

    grouped = defaultdict(list)
    factors = load_factor_specs()[:limit]
    for factor in factors:
        ci = J.assign_scope(factor["scope"], cliques)
        grouped[ci].append(("forbidden", factor["scope"], factor["forbidden"], f"physical_ternary:{factor['index']}"))

    quad_scope = tuple(map(int, H.FIVE_GIDS))
    quad_allowed = frozenset(tuple(map(int, row)) for row in H.ALLOWED)
    assert len(quad_allowed) == 832
    qci = J.assign_scope(quad_scope, cliques)
    grouped[qci].append(("allowed", quad_scope, quad_allowed, "physical_quads:compiled5"))

    affine = J.affine_scopes()
    assert len(affine) == A.EVENT_COUNT == 19
    for ai, scope in enumerate(affine):
        ci = J.assign_scope(scope, cliques)
        forbidden = frozenset((tuple(qsizes[v] - 1 for v in scope),))
        grouped[ci].append(("forbidden", scope, forbidden, f"affine:{ai}"))

    relations = []
    metadata = []
    expected_constraint_count = limit + 1 + 19
    assert sum(len(rows) for rows in grouped.values()) == expected_constraint_count

    for ci in sorted(grouped):
        raw = tuple(grouped[ci])
        used = {v for _kind, scope, _rel, _name in raw for v in scope}
        gids = tuple(v for v in cliques[ci] if v in used)
        assert used == set(gids)
        pos = {v: p for p, v in enumerate(gids)}
        capacity = math.prod(qsizes[v] for v in gids)
        allowed_rows = []
        for assignment in itertools.product(*(range(qsizes[v]) for v in gids)):
            ok = True
            for kind, scope, relation, _name in raw:
                projected = tuple(assignment[pos[v]] for v in scope)
                if kind == "forbidden":
                    if projected in relation:
                        ok = False
                        break
                else:
                    if projected not in relation:
                        ok = False
                        break
            if ok:
                allowed_rows.append(tuple(map(int, assignment)))
        allowed_rows = tuple(allowed_rows)
        assert allowed_rows, (ci, gids)
        relations.append(
            {
                "clique": ci,
                "gids": gids,
                "qsizes": tuple(qsizes[v] for v in gids),
                "allowed": allowed_rows,
                "capacity": capacity,
                "constraints": tuple(row[3] for row in raw),
            }
        )
        metadata.append(
            {
                "clique": ci,
                "gids": list(gids),
                "capacity": capacity,
                "allowed_rows": len(allowed_rows),
                "constraints": [row[3] for row in raw],
            }
        )

    out = (tuple(relations), tuple(metadata))
    _MODEL_RELATION_CACHE[limit] = out
    return out


def build_state_bitsets(allowed, qsizes):
    nrows = len(allowed)
    nbytes = (nrows + 7) // 8
    raw = [[bytearray(nbytes) for _ in range(qsize)] for qsize in qsizes]
    for rid, row in enumerate(allowed):
        byte_index = rid >> 3
        bit = 1 << (rid & 7)
        for p, state in enumerate(row):
            raw[p][int(state)][byte_index] |= bit
    indexed = tuple(
        tuple(int.from_bytes(buf, "little") for buf in per_state)
        for per_state in raw
    )
    all_rows = (1 << nrows) - 1
    for p, per_state in enumerate(indexed):
        union = 0
        for state_mask in per_state:
            union |= state_mask
        assert union == all_rows, (p, nrows)
    return indexed, all_rows


class CliqueBitsetConstraintCounter(PAIRWISE_COUNTER):
    def __init__(self, variables, var_states, var_weights, pairq):
        super().__init__(variables, var_states, var_weights, pairq)
        self.hyper_prunes = 0
        self.hyper_rounds = 0
        self.hyper_checks = 0
        self.relation_eval_hits = 0
        self.relation_eval_misses = 0
        self.memo_hits = 0
        self.max_context_variables = 0
        self.relation_eval_cache = {}

        loc = {}
        for vi, members in enumerate(self.variables):
            for ci, gid in enumerate(members):
                loc[int(gid)] = (vi, ci)
        assert len(loc) == 90

        compiled, metadata = compile_model_relations(ACTIVE_FACTOR_LIMIT)
        runtime = []
        by_var = defaultdict(list)
        for ri, relation in enumerate(compiled):
            vis = []
            for gid, qsize in zip(relation["gids"], relation["qsizes"]):
                vi, ci = loc[int(gid)]
                assert len(self.variables[vi]) == 1 and ci == 0, (gid, self.variables[vi])
                assert len(self.var_states[vi]) == int(qsize), (gid, len(self.var_states[vi]), qsize)
                vis.append(vi)
            assert len(vis) == len(set(vis))
            index, all_rows = build_state_bitsets(relation["allowed"], relation["qsizes"])
            row = {
                "name": f"clique:{relation['clique']}",
                "clique": relation["clique"],
                "gids": relation["gids"],
                "vis": tuple(vis),
                "active_mask": sum(1 << vi for vi in vis),
                "qsizes": relation["qsizes"],
                "row_index": index,
                "all_rows": all_rows,
                "allowed_rows": len(relation["allowed"]),
                "capacity": relation["capacity"],
                "constraints": relation["constraints"],
            }
            runtime.append(row)
            for vi in vis:
                by_var[vi].append(ri)

        self.relations = tuple(runtime)
        self.relations_by_var = {vi: tuple(rows) for vi, rows in by_var.items()}
        self.compiled_metadata = metadata
        assert sum(len(row["constraints"]) for row in self.relations) == ACTIVE_FACTOR_LIMIT + 20

    def _evaluate_relation(self, ri, domains):
        relation = self.relations[ri]
        vis = relation["vis"]
        projected = tuple(int(domains[vi]) for vi in vis)
        key = (ri, projected)
        cached = self.relation_eval_cache.get(key)
        if cached is not None:
            self.relation_eval_hits += 1
            return cached
        self.relation_eval_misses += 1

        viable = relation["all_rows"]
        for p, mask in enumerate(projected):
            accepted = 0
            scan = mask
            while scan:
                bit = scan & -scan
                scan ^= bit
                state = bit.bit_length() - 1
                accepted |= relation["row_index"][p][state]
            viable &= accepted
            if viable == 0:
                break

        supported = []
        if viable:
            for p, mask in enumerate(projected):
                kept = 0
                scan = mask
                while scan:
                    bit = scan & -scan
                    scan ^= bit
                    state = bit.bit_length() - 1
                    if viable & relation["row_index"][p][state]:
                        kept |= bit
                supported.append(kept)
        else:
            supported = [0] * len(projected)

        cartesian = 1
        for mask in projected:
            cartesian *= mask.bit_count()
        viable_count = viable.bit_count()
        assert viable_count <= cartesian
        binding = viable_count < cartesian
        result = (viable != 0, binding, tuple(supported), viable_count)
        self.relation_eval_cache[key] = result
        return result

    def _prune_hyper_relations(self, active, domains):
        dom = list(map(int, domains))
        changed = False
        for ri, relation in enumerate(self.relations):
            active_vis = relation["active_mask"] & active
            if not active_vis:
                continue
            viable, binding, supported, _count = self._evaluate_relation(ri, dom)
            if not viable:
                return None, True
            if not binding:
                continue
            for p, vi in enumerate(relation["vis"]):
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
            pruned, changed = self._prune_hyper_relations(active, paired)
            self.hyper_rounds += 1
            if pruned is None:
                return None
            if not changed and pruned == paired:
                return paired
            current = pruned

    def _relevant_neighbors(self, i, active, domains):
        out = PAIRWISE_COUNTER._relevant_neighbors(self, i, active, domains)
        for ri in self.relations_by_var.get(i, ()):
            relation = self.relations[ri]
            active_vis = relation["active_mask"] & active
            if not (active_vis & (1 << i)):
                continue
            if active_vis & (active_vis - 1) == 0:
                continue
            viable, binding, _supported, _count = self._evaluate_relation(ri, domains)
            assert viable
            if binding:
                out |= active_vis & ~(1 << i)
        return out

    def _memo_key(self, active, domains):
        context = int(active)
        for ri, relation in enumerate(self.relations):
            if not (relation["active_mask"] & active):
                continue
            viable, binding, _supported, _count = self._evaluate_relation(ri, domains)
            assert viable
            if binding:
                context |= relation["active_mask"]
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
        eval_hits_before = self.relation_eval_hits
        eval_misses_before = self.relation_eval_misses
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
            "relation_eval_hits_delta": self.relation_eval_hits - eval_hits_before,
            "relation_eval_misses_delta": self.relation_eval_misses - eval_misses_before,
            "max_context_variables": self.max_context_variables,
            "compiled_relation_count": len(self.relations),
        }
        PROFILE_ROWS.append(row)
        print("clique_bitset_weighted_profile", json.dumps(row, sort_keys=True), flush=True)
        return value, self.calls, len(self.memo)


def run_model(limit, label):
    global ACTIVE_FACTOR_LIMIT, MODEL_LABEL
    ACTIVE_FACTOR_LIMIT = int(limit)
    MODEL_LABEL = str(label)
    original_counter = C.ExactCounter
    original_expected = C.EXPECTED_EXACT_COUNT
    C.ExactCounter = CliqueBitsetConstraintCounter
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
    regression_relations, regression_meta = compile_model_relations(6)
    full_relations, full_meta = compile_model_relations(38)

    out = {
        "position": "C",
        "physical_shared_dimension": 149,
        "complete_higher_affine_conflicts": 19,
        "physical_ternary_factors": len(factors),
        "physical_ternary_forbidden_quotient_tuples": forbidden_tuple_count,
        "physical_quaternary_factors": 5,
        "physical_quaternary_compiled_relation_rows": len(H.ALLOWED),
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
        "regression_compiled_relations": len(regression_relations),
        "all_current_compiled_relations": len(full_relations),
        "regression_compiled_capacity": sum(row["capacity"] for row in regression_meta),
        "all_current_compiled_capacity": sum(row["capacity"] for row in full_meta),
        "regression_profile_rows": regression_profile_rows,
        "all_current_profile_rows": full_profile_rows,
        "decision": "C916_COMPLETE_AFFINE_SUPPORT_PLUS_ALL_CURRENT_EXACT_PHYSICAL_QUOTIENT_FACTORS_WEIGHTED_COUNT_CLIQUE_BITSET",
    }
    print("result", json.dumps(out, sort_keys=True), flush=True)
    print("PASS V26_Q138_C916_E0_FIRST_DYADIC_ALL_CURRENT_PHYSICAL_WEIGHTED_CLIQUE_BITSET_EXACT")
    print("theorem=the complete 4005-pair quotient model, complete 19-conflict affine-support theorem, five exact quaternary physical quotient factors, and all 38 current ternary physical quotient factors are conjoined in one exact weighted count using precompiled width-9 local relations and exact bitset GAC")
    print("boundary=this is exact for the current certified physical-factor inventory only; additional untested higher-order physical image constraints remain possible and no end-to-end work exponent is inferred")
    print("ALPHA_PASS=0")
    return out


if __name__ == "__main__":
    analyze()
