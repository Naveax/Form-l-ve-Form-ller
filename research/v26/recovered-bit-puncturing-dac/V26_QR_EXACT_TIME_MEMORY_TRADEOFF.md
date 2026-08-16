# V26 QR Exact Time-Memory Tradeoff

## Purpose

The exact reduced fixed-IO QR site graph has topological carving width 42 and path cutwidth 44. Dense contraction at those widths is impractical. However the cyclic long-range bonds can be conditioned to open the ring into a finite-memory chain.

This gives an exact time-memory tradeoff: memory can be reduced far below `2^42` without approximation, at the cost of repeating the chain calculation over boundary assignments.

## 1. Reduced site network

Use the exact n-site network from the pathwidth/carving-width notes:

- four binary sigma chains between adjacent bit sites;
- one binary `v4` edge family of cyclic offset 8;
- one binary `v3` edge family of cyclic offset 12.

For standard n=32, cut the cycle between sites 31 and 0.

The long-range edge families that wrap across this cut contain:

- 8 `v4` bonds;
- 12 `v3` bonds.

So there are exactly 20 binary wrap variables.

The sigma chains are not cyclic because the modular-addition Walsh recurrence has a fixed top boundary `sigma_{n-1}=0`; they require no wrap guess.

## 2. Open-chain state after conditioning wrap bonds

Fix an assignment to the 20 wrap variables.

The remaining network is an open finite-range chain. Scanning sites from low to high index requires remembering only:

- the 8 delayed `v4` bits whose second endpoints lie eight sites ahead;
- the 12 delayed `v3` bits whose second endpoints lie twelve sites ahead;
- the four current sigma/carry bits, one per addition chain.

Thus the exact dynamic state has at most

`8 + 12 + 4 = 24`

binary coordinates.

The state table therefore has at most

`2^24 = 16,777,216`

entries.

At eight bytes per dense scalar this is 128 MiB, before implementation overhead and exact-arithmetic expansion.

This is an exact memory bound for the conditioned chain; no trail or rank approximation is used.

## 3. Sparse local transition

At one site, the incoming state determines:

- the currently due delayed `v4` and `v3` bits;
- the four incoming sigma bits.

The outgoing state introduces:

- one new future `v4` bit;
- one new future `v3` bit;
- four outgoing sigma bits.

So at most six new binary choices label a naive local transition. The exact local site tensor is sparse because the modular-addition compatibility conditions kill many assignments, but a conservative bound is at most `2^6=64` outgoing configurations per current state.

Hence one conditioned-chain sweep has a straightforward sparse-DP work upper bound of order

`O(64 * n * 2^24)`.

This is a structural upper bound, not an optimized implementation count.

## 4. Closing the cyclic boundary

The full cyclic network is the sum over all 20 wrap assignments.

Running the 24-state-bit DP separately for every wrap assignment gives an exact algorithm with:

- memory `O(2^24)` dense scalar slots;
- outer boundary enumeration `2^20`;
- conservative work `O(n * 2^(24+20+6)) = O(n * 2^50)` under the naive 64-transition bound.

The exact constant can be smaller because the local site tensor is sparse and because repeated boundary calculations can share work. The important theorem is the existence of an exact low-memory formulation.

## 5. Continuous batching tradeoff

Instead of conditioning all 20 wrap bits externally, keep b of them symbolic inside the DP and enumerate only the remaining `20-b`.

Then, schematically:

- state-memory exponent becomes `24+b`;
- number of external batches becomes `2^(20-b)`.

The product of batch count and state-space size remains `2^44` before local-transition factors:

`2^(20-b) * 2^(24+b) = 2^44`.

Thus b parameterizes an exact memory/batching continuum from

- low memory: `b=0`, state dimension `2^24`, `2^20` batches;
- high memory: `b=20`, state dimension `2^44`, one fully symbolic batch.

This is the tensor-network analogue of conditioning a cutset in graphical-model inference.

## 6. Relation to the topology certificates

There is no contradiction with carving width 42 or path cutwidth 44.

Those widths measure the largest simultaneous bond frontier when all boundary variables are kept symbolic in an ordinary contraction tree/path.

Conditioning converts some symbolic bond dimensions into explicit outer enumeration. It lowers memory by paying time.

So the topology certificates bound dense symbolic contraction, while the present theorem exposes an exact time-memory tradeoff outside that model.

## 7. Why this matters for FDS

FDS distinguishes representation, memory and compute.

For this fixed-IO exact QR coefficient we now have:

1. local generative representation: bond-2 modular-addition MPOs, O(n) factors;
2. topology-only dense contraction: optimal tree frontier 42 binary bonds;
3. exact conditioned dynamic programming: only 24 binary dynamic-state bits, but with 20 wrap bits moved into outer enumeration.

Therefore a representation can be exact and memory-manageable while still having prohibitive total work. That is precisely why memory reduction must never be reported as an attack/work reduction by itself.

## 8. New optimization target

The remaining problem is to reduce the **product of boundary enumeration and dynamic state work**, not merely memory.

Possible genuinely new mechanisms include:

- meet-in-the-middle over the 20 wrap variables;
- low-rank factorization of the boundary-to-boundary transfer operator;
- symmetry/parity block decomposition of wrap assignments;
- exact reuse of transfer subproblems across boundary conditions;
- certified epsilon-rank truncation of the transfer operator.

If none of these reduce total work, the exact conditioned algorithm remains only a memory tradeoff.

## 9. Claims not admitted

This theorem does not claim practical exact QR computation. The `2^24` memory state is accompanied by very large boundary/time work, and exact dyadic/rational arithmetic can increase storage beyond eight bytes per entry.

It does not establish double-round/full-round contraction, ranking gain, alpha<1, or cryptanalytic improvement.