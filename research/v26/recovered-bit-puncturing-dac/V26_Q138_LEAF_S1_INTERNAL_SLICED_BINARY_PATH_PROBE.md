# V26 Q138 leaf S1 internal-sliced binary path probe

## Status

Diagnostic only. This file does **not** admit a numerical leaf contraction, a leaf-rank bound, a lower `W_repr(1)`, arithmetic-work improvement, `ALPHA_PASS=1`, or full-round relevance.

## Motivation

Clean authority run `34109391867` for the preceding row/column-block path probe showed that explicit opt_einsum memory ceilings can fit the S1 leaf network, but the selected memory-capped paths use high multi-operand arity and have astronomical estimated total work. Memory feasibility is therefore not an execution theorem.

The existing numerical leaf-minor executor already requires pairwise contraction (`len(step)==2`) and reduces modulo251 after each step. The missing execution-design question is whether exact **internal binary index slicing** can bring a pairwise path under a practical intermediate-size ceiling without making the total number of slice assignments prohibitive.

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

## Acceptance semantics

A successful CI run means only that the binary internal-slicing search completed and produced its recorded path/work table. Even a memory-feasible result is not yet a rank theorem.

A useful next-stage execution candidate must have all of:

- `max_step_arity=2`;
- a controlled peak intermediate;
- total work including output blocks and all internal slice assignments small enough for an exact modular execution attempt.

Only after such a candidate exists should a numerical modulo251 contraction be implemented. That executor must reduce after every pairwise operation and explicitly check integer accumulation safety or chunk the contracted dimension.
