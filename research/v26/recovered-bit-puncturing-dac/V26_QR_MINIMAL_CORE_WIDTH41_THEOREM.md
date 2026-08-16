# V26 QR Minimal-Core Width-41 Theorem

## Purpose

This note closes the first exact global-contraction pass built from the minimal-rank local Walsh cores rather than prematurely fused bit-site tensors.

The previous exact values

- fused-site path cutwidth `44`,
- fused-site carving width `42`,

remain correct for their respective representations. They are not lower bounds for the fully refined exact tensor network.

The result here gives a strictly smaller **machine-verifiable exact global message-width upper bound** for one fixed-input/fixed-output 32-bit ChaCha quarter-round Walsh coefficient.

## 1. Fixed-IO reduced Walsh network

Use the exact fixed-IO reduction from `V26_EXACT_QR_PATHWIDTH_THEOREM.md`.

The four modular-addition bit factors have physical mask dependence

- `T4_i`: `u4_i`, `v4_i`, with `w4_i` fixed by the external masks;
- `T3_i`: `u3_i`, `v3_i`, `v4_{i+8}`, up to fixed XOR constants;
- `T2_i`: `v4_{i+8}`, `w2_i`, with the first addition-mask leg fixed and `w2_i = u4_i xor v3_{i+12} xor const_i`;
- `T1_i`: `v3_{i+12}`, `u3_i`, with the first addition-mask leg fixed, up to fixed XOR constants.

The `T2` relation is kept as an explicit local parity tensor rather than fused into a larger factor.

All fixed XOR constants are local basis flips and do not change the index dimensions or the rank statements below.

## 2. Exact local TT cores

`V26_MODADD_LOCAL_TT_RANK_THEOREM.md` gives the optimal full five-leg interior profile `[2,3,3,2]` with current sigma `s` in the center.

For the fixed-IO QR network, the exact orders used in the certificate are

- `T4`: `(t,s,v,u)`, profile `[2,3,2]` because `w` is fixed;
- `T3`: `(u,t,s,v,w)`, profile `[2,3,3,2]`;
- `T2`: `(t,w,v,s)`, profile `[2,3,2]` because `u` is fixed;
- `T1`: `(w,v,s,t)`, profile `[2,3,2]` because `u` is fixed.

At bit 0 the terminal sigma recurrence is summed and the ranks reduce to

- `T4/T2/T1`: `[2,2]`,
- `T3`: `[2,3,2]`.

At bit 31 the boundary condition `sigma_31=0` gives

- `T4/T2/T1`: `[1,1]`,
- `T3`: `[2,2,2]`.

These endpoint ranks were checked for both possible values of every fixed ordinary mask bit. The verifier recomputes the local ranks by exact rational Gaussian elimination.

## 3. Refined network size

Replacing the addition-bit tensors by these exact TT cores and keeping the local `T2` XOR parity factors explicit gives, for `n=32`,

- `568` tensor vertices;
- `686` nontrivial indices;
- `535` binary indices;
- `151` ternary indices;
- `622` degree-2 indices;
- `64` degree-3 indices.

No sigma cap, trail truncation, floating rank tolerance, or approximate SVD is used.

## 4. Boundary dimension

For a cluster `S` of tensor vertices, define its exact message dimension

`D(S) = product_{e crosses S | complement} dim(e)`.

Equivalently,

`log2 D(S) = (# crossing binary indices) + log2(3) * (# crossing ternary indices)`.

A binary contraction tree over the tensor vertices has message-width

`W = max_{non-root clusters S} log2 D(S)`.

This is a representation/intermediate-message size measure. Arithmetic work for combining child messages can be larger and is not identified with `2^W` here.

## 5. Exact width-41 certificate

A complete binary contraction tree with

- `568` leaves,
- `567` internal nodes,

has been materialized in

`V26_QR_MINIMAL_CORE_WIDTH41_CERTIFICATE.json`.

The complete tree was checked from leaves to root. Every leaf appears exactly once, every internal node is the disjoint union of its two children, and every boundary dimension is recomputed from the refined hypergraph.

The largest message occurs on a `340`-leaf cluster and crosses exactly

`41` binary indices

and no ternary index. Therefore

`D_max = 2^41 = 2,199,023,255,552`,

so

`W <= 41`.

The verifier is

`scripts/verify_v26_qr_minimal_core_width41.py`.

Expected output includes

`PASS V26_QR_MINIMAL_CORE_WIDTH41_CERTIFICATE`

and

`max_boundary_dimension=2^41`.

## 6. Improvement over fused representations

The exact structural comparison is now

- natural fused-site path: `W = 44`;
- optimal fused-site carving tree: `W = 42`;
- refined minimal-core explicit tree: `W <= 41`.

Thus the minimal-rank local-core representation gives a certified reduction of

- one full binary message bit relative to fused-site carving, i.e. a factor 2 in the largest dense message dimension;
- three bits relative to the natural fused-site path, i.e. a factor 8.

The key mechanism is not another ordering of the same fused graph. It is exact algebraic refinement of each local modular-addition tensor before global contraction.

## 7. What is and is not proved

Proved:

1. exact local TT ranks used in the refined QR network;
2. exact construction of the 568-vertex refined network;
3. a complete exact contraction tree with maximum message dimension `2^41`;
4. therefore a rigorous global upper bound `W <= 41` for this fixed-IO one-QR representation.

Not proved:

- `41` is optimal;
- width `40` is impossible;
- arithmetic work is `O(2^41)`;
- the same width holds when large external spectra are left open;
- a double-round or full-round network has comparable width;
- any cryptanalytic ranking gain or `alpha<1` follows.

## 8. Width-40 exploratory status

A separate, non-admitted search found several recursive cuts below 41, including clusters with boundaries `40` and `40 + log2(3) - 1 = 40.584962...` depending on the local ternary bond count.

However that search did not close a complete 568-leaf tree below 41: one large residual cluster remained unresolved within the finite solver budget.

Therefore **do not report `W <= 40`**. The only current complete machine-verified exact certificate is

`W <= 41`.

## 9. Next exact mathematical target

The next pass should not rerun the same fused-site search. It should attack the remaining one-bit gap by one of two genuinely distinct mechanisms:

1. continue exact global tree search on the minimal-core network, with width-40 feasibility as a frozen target;
2. derive algebraic/Schmidt rank compression of the width-41 separator message itself.

If width 40 cannot be certified efficiently, the second route is mathematically more important because even `2^40` remains impractical as a dense message.

Only after exact separator-rank structure is exhausted should certified epsilon-rank become the active approximation mechanism.

## 10. Claims not admitted

This theorem does not establish practical exact QR evaluation, full second-layer contraction, four-inverse-round exact energy, end-to-end ranking reduction, `alpha<1`, or full-round relevance.
