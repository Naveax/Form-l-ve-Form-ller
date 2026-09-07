# V26 Q138 leaf S1 internal-sliced binary path probe

## Status

Diagnostic NO-GO for the tested pure internal-slicing/binary-path route. This file does **not** admit a numerical leaf contraction, a leaf-rank bound, a lower `W_repr(1)`, arithmetic-work improvement, `ALPHA_PASS=1`, or full-round relevance.

Clean authority run `34112973361` completed successfully on PR #91 and tested position C with `b_open in {0,2,7}` through 24 exact internal binary slices. Every tested acceptance Pareto set was empty:

`case_pareto C 0 {}`

`case_pareto C 2 {}`

`case_pareto C 7 {}`

Thus no tested pairwise path simultaneously met the explicit `2^28`, `2^30`, or `2^32` element ceilings with the recorded exact output-block/internal-slice work accounting.

## Motivation

Clean authority run `34109391867` for the preceding row/column-block path probe showed that explicit opt_einsum memory ceilings can fit the S1 leaf network, but the selected memory-capped paths use high multi-operand arity and have astronomical estimated total work. Memory feasibility is therefore not an execution theorem.

The existing numerical leaf-minor executor already requires pairwise contraction (`len(step)==2`) and reduces modulo251 after each step. The missing execution-design question was whether exact **internal binary index slicing** could bring a pairwise path under a practical intermediate-size ceiling without making the total number of slice assignments prohibitive.

## Probe

`scripts/probe_v26_q138_leaf_s1_internal_sliced_binary_path.py` reuses the admitted factor network and S1 cut topology.

Initial target is position C, because the preceding memory-capped Pareto scan gave the lowest path-only work there. It tests representative open-column block sizes `b_open in {0,2,7}`.

For each case the probe:

1. computes an uncapped greedy opt_einsum path and requires every path step to have arity at most2;
2. symbolically replays the existing pairwise tensordot semantics and identifies a peak-intermediate frontier;
3. considers only degree-two **internal** frontier labels, excluding logical output names and their normalized output legs;
4. fixes one selected internal binary label for topology planning, then re-plans the binary path;
5. records the exact work multiplier `2^k` needed to recover the unsliced contraction by summing all assignments of `k` sliced internal bits;
6. multiplies path cost by both internal-slice assignments and the exact number of fixed-column output blocks;
7. reports the least estimated total work found under `2^28`, `2^30`, and `2^32` element ceilings.

The fixed planning value is zero only because tensor values do not change path shapes. A later numerical executor must sum both values of every sliced internal bit; the probe accounts for that through the `2^k` multiplier.

## Clean result

Authority run: `34112973361`.

All recorded contraction paths satisfy `max_step_arity=2`, so the failure is not caused by hidden high-arity opt_einsum steps.

Representative observations:

- `C, b_open=0`: after 24 selected internal slices, the searched paths still have no accepted memory/work point; observed peaks remain far above `2^32` elements.
- `C, b_open=2`: the lowest observed peak in the recorded search is `2^41` elements (for example at 22 internal slices), still a factor512 above the loosest `2^32` ceiling. The corresponding exact total-work estimate is about `6.20e26` path-cost units after output blocks and all slice assignments are included.
- `C, b_open=7`: despite much larger output blocks and aggressive internal slicing, the searched paths likewise produce no accepted point through 24 slices.

The probe therefore closes the specific route “greedy pairwise contraction + exact degree-two internal slicing + output-column blocking” under the tested C configurations and stated element ceilings. Internal slicing substantially changes the work/peak tradeoff compared with the earlier high-arity memory-capped plans, but it does not make the exact numerical leaf-minor execution practical here.

## Acceptance semantics

A successful CI run means only that the binary internal-slicing search completed and produced its recorded path/work table. The empty Pareto sets are a path-design NO-GO, not a leaf-rank theorem.

A useful later execution candidate would still need all of:

- `max_step_arity=2`;
- a controlled peak intermediate;
- total work including output blocks and all internal slice assignments small enough for an exact modular execution attempt.

Only after such a candidate exists should a numerical modulo251 contraction be implemented. That executor must reduce after every pairwise operation and explicitly check integer accumulation safety or chunk the contracted dimension.

## Consequence / next direction

Do not continue by merely increasing the number of greedy internal slices on the same planning strategy. The next useful complete-leaf route must change the contraction structure itself, for example by exploiting algebraic factor elimination, separator/message reuse, variable elimination with cached boundary states, or a product-level rank/cancellation theorem before numerical materialization.

No numerical leaf-rank claim follows from this diagnostic.
