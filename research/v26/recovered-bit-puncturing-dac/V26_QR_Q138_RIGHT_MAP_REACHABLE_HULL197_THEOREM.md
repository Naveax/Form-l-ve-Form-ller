# V26 q138 Right-Map Reachable-Hull-197 Theorem

## Purpose

`V26_QR_Q138_RIGHT_MAP_TRANSFER_CHAIN_THEOREM.md` reduces the 107-leaf q138 right-map Gram calculation to a five-site transfer chain. Between neighboring interior sites, the doubled Gram state has 10 binary bits and therefore a formal ambient dimension of 1024.

This note determines the exact subspace of that 1024-dimensional state that is reachable from the site-3 boundary under arbitrary choices of the eight interior fixed-mask control types.

The main result is an exact common invariant reachable hull of dimension

`197`.

Thus the correct exact Gram transfer representation needs at most 197 states on the reachable family, not 1024 anonymous dense states.

## 1. Interior transfer family

For an ordinary interior site let

`tau=(u1,u2,p) in {0,1}^3`,

where `u1` and `u2` are the fixed T1/T2 mask bits and `p` is the local affine parity constant.

Contract the doubled exact site tensor, summing the parent-external local variables between the two Gram copies and leaving open the five-bit carry/sigma state on the left and right in both copies.

This gives an exact rational operator

`K_tau : Q^1024 -> Q^1024`.

Sites 4, 5 and 6 give the same eight operators after the canonical translation of bit labels. This identity was checked entry-for-entry with exact rational arithmetic.

## 2. Ambient operator ranks

In lexicographic tau order

`000,001,010,011,100,101,110,111`,

the exact rational ranks of the full 1024-dimensional operators are

`1016, 575, 384, 397, 454, 537, 431, 315`.

In particular `K_000` is almost full rank in the ambient doubled state.

Therefore the useful compression is **not** a generic low-rank factorization of each local transfer operator considered in isolation.

## 3. Site-3 boundary space

Site 3 contains one of the six child-interface bits, `aux_j4_i11_k0`. In the doubled Gram network it therefore has four interface-pair sectors.

For every one of the eight site-3 control types, those four boundary-to-hidden-state vectors are independent.

Taking the span over

- all eight site-3 control types; and
- all four interface-pair sectors

gives an exact initial hidden-state space of dimension

`28`.

Call this space `H_0`.

## 4. Exact-length image dimensions

If only products of exactly d interior transfer operators are considered, the successive span dimensions are

- before an interior transfer: `28`;
- after one site: `135`;
- after two sites: `166`;
- after three sites: `166`.

The two 166-dimensional spaces at depths two and three are **not the same subspace**. Their union has dimension 193.

Therefore equal dimensions at adjacent depths must not be misread as invariance.

## 5. Monotone reachable hull

Define the cumulative hull recursively by

`U_0 = H_0`

and

`U_{d+1} = span(U_d union { v K_tau : v in U_d, tau in {0,1}^3 }).`

Exact rational Gaussian elimination gives

`dim U_0 = 28`

`dim U_1 = 150`

`dim U_2 = 193`

`dim U_3 = 197`

`dim U_4 = 197`.

At the final step no new independent vector is generated. Hence

`U = U_3`

is invariant under all eight `K_tau`, and

`dim U = 197`.

This proves an exact reachable-state quotient

`1024 -> 197`

for every interior control sequence generated after the site-3 boundary family.

The state reduction factor is

`1024/197 ~= 5.198`.

## 6. Transfer ranks on the invariant hull

Restrict each exact operator to the invariant 197-dimensional reachable hull.

Again in tau order

`000,001,010,011,100,101,110,111`,

the exact image dimensions are

`194, 126, 89, 94, 112, 122, 100, 80`.

Thus even the nearly full ambient `K_000` has rank only 194 on the only subspace that matters for the complete reachable control family.

These are the appropriate local state dimensions for a quotient-transfer implementation or further sector analysis.

## 7. Gram-copy exchange symmetry

Let `S` exchange the two five-bit Gram-copy states:

`S |a,b> = |b,a>`.

Every doubled transfer operator commutes with this exchange, because the two Gram copies contain identical local tensors and share the same summed parent-external variables.

The reachable hull is closed under `S` and decomposes exactly into the two eigensectors

`U = U_+ direct_sum U_-`,

with

- symmetric sector `dim U_+ = 138`;
- antisymmetric sector `dim U_- = 59`.

Hence

`197 = 138 + 59`.

This supplies a canonical block basis for the next transfer/rank calculation rather than an arbitrary 197-coordinate quotient.

## 8. Mathematical interpretation

The hierarchy is now:

- formal doubled hidden state: `1024`;
- site-3 reachable boundary span: `28`;
- common invariant hull under arbitrary interior controls: `197`;
- canonical copy-swap blocks: `138 + 59`.

The almost-full ambient rank of `K_000` and the much smaller reachable hull explain why inspecting local matrices alone was misleading. The compression is **boundary-conditioned reachability**, not generic local low rank.

This is exactly the source-conditioned mechanism sought by FDS: the full operator may be large, while the subspace reachable from the actual source/boundary family is much smaller and is closed under all subsequent local dynamics.

## 9. Machine verifier

The exact verifier is

`scripts/verify_v26_qr_q138_right_map_reachable_hull197.py`.

It reconstructs the certified width-40 q138 network and the 107-leaf right child, builds all eight exact doubled interior transfers, checks the site-4/site-5/site-6 translation identity, recomputes the ambient ranks, builds the site-3 boundary span, closes the cumulative reachable hull, and verifies the copy-exchange sector dimensions.

Expected output ends with

`PASS V26_QR_Q138_RIGHT_MAP_REACHABLE_HULL197`

and reports

- ambient ranks `1016,575,384,397,454,537,431,315`;
- cumulative hull dimensions `28,150,193,197,197`;
- restricted ranks `194,126,89,94,112,122,100,80`;
- copy-swap sectors `138/59`.

No floating tolerance, trail cap, SVD approximation or historical V25 runtime is involved.

## 10. Next exact target

The next distinct step is to **materialize the quotient transfer algebra on U**, not to return to 1024-state contractions.

In particular:

1. choose an exact rational basis adapted to `U_+ direct_sum U_-`;
2. express the eight `K_tau|_U` as exact block matrices of sizes at most 138 and 59;
3. construct the site-3 and site-7 boundary maps in the same quotient basis;
4. derive the exact right-map and parent-rank envelope over all five-site control sequences by finite-state dynamic programming in the quotient;
5. identify which quotient sectors are actually reachable under the q138 source-conditioned mask family;
6. only then reinsert conditioned rank factors globally and seek a new complete width/work certificate.

## 11. Claims not admitted

This theorem does not by itself prove `W<=39`, does not give a universal right-map rank, and does not establish practical exact QR evaluation, arithmetic-work reduction, double-round/full-round contraction, ranking gain or `alpha<1`.

It proves an exact source/boundary-conditioned reduction of the doubled Gram transfer state from 1024 formal states to a 197-dimensional invariant reachable hull.
