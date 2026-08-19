# V26 Q1.38 saturated-complement dyadic lift theorem

## Scope

This theorem is a general exact integer-lift lemma for predecessor-leaf matrices across the frozen 11|21 split. The row dimension is

`N = 2^11 = 2048`.

It does not use approximation and does not assume special carry-sector geometry. It applies after **any** admitted integer dyadic lift of rational rank at most `d`.

The main consequence is methodological: finite dyadic prefix gates are not invariant under the allowed choice of integer lift representatives. A subgeneric layer can always be paired with a complementary layer, and the remaining binary obstruction can then be pushed to arbitrarily high dyadic depth without changing those two rank envelopes. Therefore complete-tail control, not a fixed k7/k8/k9 prefix pass, is the invariant target.

## Saturated lattice lemma

Let

`L <= Q^N`

be a rational subspace of dimension `d`, and let

`Lambda = L intersect Z^N`.

Then `Lambda` is a saturated rank-`d` lattice. Reduction modulo2 gives a binary code

`C = Lambda mod 2 <= F2^N`

of exact dimension `d`.

Indeed, the reduction kernel is exactly `2 Lambda`: if `v in Lambda` is coordinatewise even, then `v/2` is integral and still lies in the rational subspace `L`, hence `v/2 in Lambda`. Therefore

`Lambda / 2 Lambda ~= C`

and `dim_F2 C = rank_Z Lambda = d`.

This is why reducing a chosen rational basis modulo2 is the wrong operation: a Walsh basis may collapse mod2 even though the **saturated integer lattice** has the full dimension `d`.

## One-step complementary lift

Let `R` be an integer `N x M` residue matrix. Suppose there exists an integer lift `K` such that

`K = R (mod 2)`

and

`rank_Q K <= d`.

Choose a rational `d`-dimensional subspace `L` containing the columns of `K`; if the actual rank is smaller, extend its rational column space arbitrarily to dimension `d`.

Let `Lambda=L intersect Z^N`, let `C=Lambda mod2`, and choose any binary complement

`F2^N = C direct_sum U`,

`dim U = N-d`.

Write

`R1 = (R-K)/2`.

For every column `r` of `R1 mod2`, decompose uniquely

`r = c + u`, `c in C`, `u in U`.

By definition of `C`, choose an integral `z in Lambda` reducing to `c`. Put the corresponding columns into `Z` and replace

`K' = K + 2 Z`.

Then

- `K' = R (mod2)`;
- every column of `K'` remains in `L`, so `rank_Q K' <= d`;
- the new residual
  `R1'=(R-K')/2=R1-Z`
  has every binary column in `U`.

Choose integral lifts of a binary basis of `U`. They are rationally independent because an odd minor survives from the binary basis. Hence `R1' mod2` has an integer lift `K1` of rational rank at most

`N-d`.

Therefore:

> If one dyadic layer admits rank at most `d`, the same layer can be chosen so that the **next** dyadic layer admits rank at most `N-d`.

No property of the following residue is required.

## Alternating continuation

Apply the same argument to the `N-d` dimensional lift space. The subsequent layer can be bounded by `d`, then `N-d`, and so on.

Thus after any admitted rank-`d` lift one may continue with the exact alternating envelope

`d, N-d, d, N-d, ...`

unless a stronger direct theorem resets the envelope earlier.

This alternating envelope is a safe finite-layer accounting tool. It is **not** by itself a complete-tail compression theorem.

## Stronger finite-prefix deferral theorem

The complementary construction gives more than alternation.

After the first two layers, choose rational spaces `L0,L1` with saturated codes

`C0 = (L0 intersect Z^N) mod2`,

`C1 = (L1 intersect Z^N) mod2`

such that

`F2^N = C0 direct_sum C1`,

with dimensions `d` and `N-d`.

Suppose at some later dyadic depth `j>=2` the current integer residual is `Rj`. Because `C0+C1=F2^N`, each column of `Rj mod2` can be written

`c0+c1`, `c0 in C0`, `c1 in C1`.

Choose integral lifts `z0 in L0 intersect Z^N`, `z1 in L1 intersect Z^N`. Modify the two old lifts by

`K0 <- K0 + 2^j z0`,

`K1 <- K1 + 2^(j-1) z1`.

These changes:

- preserve the binary parity of `K0` and `K1` because `j>=2`;
- keep their columns in the same rational spaces, so their rank envelopes remain `d` and `N-d`;
- change the total represented matrix by exactly
  `2^j(z0+z1)`,
  so the depth-j residual becomes even.

Therefore one may set `Kj=0` and divide the remaining residual by2.

Repeating this argument proves:

> For every finite `T>=2`, one can choose integer representatives with
>
> `R = K0^(T) + 2 K1^(T) + 2^T RT`,
>
> `rank_Q K0^(T)<=d`, `rank_Q K1^(T)<=N-d`,
>
> and **all intermediate lifts `K2,...,K_(T-1)` equal to zero**.

This is an exact finite statement over integers. It does **not** assert that the process converges to a finite two-term integer decomposition as `T->infinity`; an odd-index lattice obstruction can persist indefinitely in 2-adic depth.

## Consequence: finite prefix gates are gauge-dependent

The deferral theorem means a statement such as

`sum(k0..k9) < 2^44`

is not an invariant achievement once lift representatives may be changed by higher even multiples. Complexity can be pushed beyond any chosen finite depth while the early rank envelopes remain fixed.

Therefore:

- a k7/k8/k9 prefix pass is a diagnostic only;
- thresholds such as “B/C index2 must be <=31” or the complementary diagnostic `<=745` are **not complete-tail necessities**;
- the invariant target is a complete finite exact decomposition/tail bound, a direct complete-leaf Schmidt theorem, or product-level cancellation that controls the whole factor rather than a chosen dyadic prefix.

There is also a simple rank-budget warning. The complementary pair itself costs

`d + (N-d) = N = 2048`.

Thus using only the generic complementary pair consumes the entire single-leaf Hilbert-rank budget. By separate-leaf rank subadditivity alone it cannot yield a strict `<2048` complete-leaf bound. Any actual compression must exploit stronger structure than the dimension-only complement construction.

## Application to current A/B/C/D authority

Use the current exact-signed/direct theorem chain on main:

- A: `[1,41,564,1761,...]`, where the index3 direct signed aggregate has rank at most1761;
- B: `[36,812,...]`;
- C: `[84,972,...]`;
- D: `[1,20,173,838,1958,...]`.

Applying the one-step complementary theorem at the latest admitted subgeneric layer gives safe alternating envelopes

A:

`[1,41,564,1761,287,1761,287,1761,...]`;

B:

`[36,812,1236,812,1236,812,...]`;

C:

`[84,972,1076,972,1076,972,...]`;

D:

`[1,20,173,838,1958,90,1958,90,...]`.

For B/C this immediately proves, without any direct third-residue theorem,

`b2 <= 2048-812 = 1236`,

`c2 <= 2048-972 = 1076`,

for a suitable alternative mod4 representative of the already-admitted K1 lift.

These are exact coefficient-aware integer-lift bounds. They do **not** claim that the natural/direct B/C third residues have those raw ranks.

## Prefix arithmetic diagnostic

Using the alternating envelopes above, exact four-leaf convolution gives

- k0 `3,024`;
- k1 `287,664`;
- k2 `11,935,392`;
- k3 `283,121,296`;
- k4 `4,263,338,416`;
- k5 `43,221,987,824`;
- k6 `305,905,291,312`;
- k7 `1,534,220,327,760`;
- k8 `5,424,451,203,888`;
- k9 `13,519,854,417,072`.

Hence

`sum(k0..k8) = 7,312,357,496,576 < 2^44`,

while

`sum(k0..k9) = 20,832,211,913,648 > 2^44`.

These numbers are useful consistency diagnostics but, by the finite-prefix deferral theorem, they are **not invariant search gates**.

## Parametric B/C diagnostic

If future direct/aggregate theorems give

`rank(K_B,2)<=b2`, `rank(K_C,2)<=c2`,

and one restarts the simple alternating accounting at index2, then the k0..k9 diagnostic is

`12,425,800,334,816`

`+ 3,537,036,576 b2`

`+ 2,841,485,712 c2`

`+ 734,769 b2 c2`.

For `b2=c2=t`, `t=745` lies below `2^44` and `t=746` lies above it. This replaces the old31 threshold **only as a gauge-dependent prefix diagnostic**. It is not a mathematical necessity for complete compression.

## New research implication

The correct next questions are no longer “how do we make k9 pass?” but:

1. can B/C complete predecessor-leaf matrices be shown to have exact Schmidt rank `<2048` for every predecessor input;
2. can the complete dyadic tail be represented with total rank-sum `<2048` for at least one leaf, rather than merely postponed;
3. can cross-leaf/product-level cancellation beat the product of separate leaf rank sums;
4. what odd-index lattice obstruction remains after complementary saturated lift spaces are combined, and can additional structural lift spaces remove it without restoring the full2048 rank budget.

## Status discipline

Still not claimed:

- complete predecessor-leaf Schmidt rank below2048;
- complete four-leaf dyadic tail below2^44;
- lower `W_repr(1)` or `W_factor-gen`;
- arithmetic-work reduction;
- ranking/search gain, `alpha<1`, or full-round relevance.
