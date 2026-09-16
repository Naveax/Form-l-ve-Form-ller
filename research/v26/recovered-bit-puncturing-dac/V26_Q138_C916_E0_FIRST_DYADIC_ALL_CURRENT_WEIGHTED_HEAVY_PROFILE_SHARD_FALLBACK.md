# V26 Q138 C916 E0 first-dyadic all-current weighted heavy-profile shard fallback

Status: prepared execution theorem; **not yet an admitted numerical authority**.

`ALPHA_PASS=0`.

## Purpose

The monolithic authority-correct all-current weighted counter reproduced the historical six-factor regression exactly, then exceeded its runner budget in the first large separator-domain profile. The profile-matrix execution removes cross-profile serialization. If one of the large profiles still exceeds a single-run budget, the fallback in

`scripts/verify_v26_q138_c916_e0_first_dyadic_all_current_weighted_heavy_profile_shards_exact.py`

splits that one profile into independent exact subproblems without changing the mathematical model.

The intended targets are the large separator-domain profiles with domain-state sums `251`, `288`, and `302`.

## Frozen model boundary

Every shard uses the same authority-correct model as the all-current weighted counter:

- the exact complete `4005` pairwise quotient value relations;
- all `19` complete affine-support obstructions with **all-nonzero forbidden** semantics;
- the exact `832`-row conjunction of the five certified physical quaternary factors;
- all `38` current exact physical ternary quotient factors;
- the exact quotient-state multiplicity weights;
- the same four-parent separator unary domains and base separator mass.

No factor is omitted or relaxed by sharding.

## Exact partition theorem

Let `D=(D_0,...,D_{N-1})` be the arc-closed quotient-state domains for one separator profile under the complete current model. Choose any variable `i` with more than one surviving local state and write

`D_i = {s_1,...,s_k}`.

For every `s_j`, form `D^(j)` by replacing `D_i` with the singleton `{s_j}` and rerunning the exact pairwise-plus-hyperedge arc closure.

The solution sets satisfy

`Sol(D) = disjoint_union_j Sol(D^(j))`.

Reason: every assignment in `Sol(D)` chooses exactly one state of `D_i`; singleton restriction therefore places it in exactly one branch. Arc closure removes only states with no compatible completion, so it cannot remove a valid assignment. Branches whose closure is empty contribute exactly zero. Distinct singleton choices are disjoint.

Repeating this argument to any fixed split depth yields a finite set of pairwise-disjoint leaf domains whose exact weighted counts sum to the unsplit profile count.

This theorem does **not** depend on choosing the same branch variable as the recursive solver. The fallback uses a deterministic domain-width/relevant-neighbor heuristic only for execution balance; the partition remains exact for any deterministic multi-state choice.

## Multiplicity weights

A shard fixes quotient states, not raw physical representatives. The existing exact counter applies the frozen `var_weights` multiplicities when singleton variables are eliminated. Therefore a leaf count is already the exact quotient-multiplicity-weighted count for that restricted domain.

For a separator profile with base mass `M`, a shard returning exact profile count `c_j` contributes

`M * c_j`

to the global weighted count. Because `M` is constant across shards of the same separator-domain profile,

`sum_j M*c_j = M * sum_j c_j`.

## Manifest integrity

The fallback emits a deterministic manifest containing, for every leaf:

- shard index;
- ordered sequence of `(variable_index, quotient_state_index)` branch choices;
- closed-domain state-sum diagnostic;
- SHA-256 digest of the complete closed domain-mask vector.

Every shard recomputes the same manifest from the same authorities and records its manifest digest, path, and domain digest. Aggregation rejects missing, duplicate, reordered, or mismatched shards before summing exact integers.

## Admission rule

This fallback should remain workflow-free while the current profile-matrix run can finish the large profiles directly. It becomes the execution path only after a concrete large-profile timeout or runner-budget failure is observed on the current exact head.

A numerical heavy-profile result is admissible only after:

1. one frozen manifest is cleanly reproduced;
2. every manifest leaf completes exactly;
3. aggregation verifies the complete shard index set and all path/domain digests;
4. the summed profile result is folded into the ten-profile matrix;
5. the historical six-factor weighted checkpoint remains an exact regression gate.

No shard count, manifest size, or execution speed is an end-to-end cryptanalytic work exponent.