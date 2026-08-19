# V26 Q1.38 saturated-complement dyadic lift theorem

## Scope

This theorem is a general exact integer-lift lemma for predecessor-leaf matrices across the frozen 11|21 split. The row dimension is

`N = 2^11 = 2048`.

It does not use approximation and does not assume any special carry-sector geometry. It applies after **any** admitted integer dyadic lift of rational rank at most `d`.

The theorem changes the higher-residue search because an unresolved next residue need not be charged the generic2048 rank once the previous lift is subgeneric.

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

Choose an integral lift of a binary basis of `U`. Its columns are rationally independent because an odd minor survives from the binary basis. Thus `R1' mod2` has an integer lift `K1` of rational rank at most

`N-d`.

Therefore:

> If one dyadic layer admits rank at most `d`, the same layer can be chosen so that the **next** dyadic layer admits rank at most `N-d`.

No property of the following residue is required.

## Iteration

Apply the same argument to the `N-d` dimensional lift space. The subsequent layer can be bounded by `d`, then `N-d`, and so on.

Thus after any admitted rank-`d` lift one may continue with the exact alternating envelope

`d, N-d, d, N-d, ...`

unless a stronger direct theorem resets the envelope earlier.

The construction is coefficient-aware but uniform in rank. It is exact and constructive at the level of integer lift existence.

## Application to current A/B/C/D authority

Use the current exact-signed/direct theorem chain on main:

- A: `[1,41,564,1761,...]`, where the index3 direct signed aggregate has rank at most1761;
- B: `[36,812,...]`;
- C: `[84,972,...]`;
- D: `[1,20,173,838,1958,...]`.

Applying the complementary theorem at the latest admitted subgeneric layer gives safe infinite envelopes

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

`c2 <= 2048-972 = 1076`.

These are exact coefficient-aware integer-lift bounds. They do **not** claim that the natural/direct B/C third residues have those raw ranks; they claim that an alternative mod4 representative of the already-admitted K1 lift can always realize such next-layer rank.

## Dynamic convolution consequence

Using the safe envelopes above, exact four-leaf convolution gives

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

with margin

`10,279,828,547,840`.

But

`sum(k0..k9) = 20,832,211,913,648 > 2^44`.

So k9 remains the immediate prefix blocker, but the previous generic-higher-layer accounting is strictly superseded.

## Parametric B/C index2 gate

If future direct/aggregate theorems give

`rank(K_B,2)<=b2`, `rank(K_C,2)<=c2`,

then restart the complementary alternation at index2:

B `[36,812,b2,2048-b2,b2,2048-b2,...]`,

C `[84,972,c2,2048-c2,c2,2048-c2,...]`.

Keeping the admitted A/D sequences with their complementary tails, exact convolution through k9 simplifies to

`sum(k0..k9)`

`= 12,425,800,334,816`

`+ 3,537,036,576 b2`

`+ 2,841,485,712 c2`

`+ 734,769 b2 c2`.

For the equal-rank diagnostic `b2=c2=t`:

- `t=745` gives `17,585,614,603,601 < 2^44`;
- `t=746` gives `17,593,088,666,468 > 2^44`.

Thus the equal B/C index2 target for a k9 prefix pass changes from the old residue-by-residue value31 to the much less severe exact target745 once complementary higher lifts are counted correctly.

This is still only a k9 prefix criterion. It is **not** a complete-tail theorem and does not lower the current complete d=1 representation/factor-generation exponent by itself.

## Status discipline

Still not claimed:

- complete predecessor-leaf Schmidt rank below2048;
- complete four-leaf dyadic tail below2^44;
- lower `W_repr(1)` or `W_factor-gen`;
- arithmetic-work reduction;
- ranking/search gain, `alpha<1`, or full-round relevance.
