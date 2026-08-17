# V26 q138 Left-I9 Support-216 Theorem

## Purpose

The exact physical q138 one-quarter-round line already proves that the certified 171-leaf bottleneck has parent Schmidt rank at most 27 across its `16|24` external partition. The earlier conditioned sub-40 certificate then exposed a new 230-leaf maximum created when the left rank factor was absorbed into the outside network.

This note identifies the exact structural reason that maximum is not intrinsic. The 64-leaf left child has only a bounded set of feasible assignments on the nine left-external bits consumed by the 229-leaf outside cluster.

The result is uniform over all 64 physical fixed-mask choices of the left child.

## 1. The relevant partition

The certified 16 left-external binary indices are split as follows.

The nine indices consumed by the 229-leaf outside cluster are

- `v4_8`;
- `v4_9`;
- `v4_10`;
- `sig4_18`;
- `sig3_10`;
- `v3_21`;
- `v3_22`;
- `aux_j2_i10_k2`;
- `sig1_10`.

Call this set `I9`.

The remaining seven left-external bits are

- `u4_16`;
- `u4_17`;
- `u4_18`;
- `v3_10`;
- `v3_20`;
- `v3_8`;
- `v3_9`.

The left child also has the six certified child-interface bits.

Thus the exact left map may be viewed as

`L_m(I9, O7, J6)`

for each physical left fixed-mask choice `m`.

## 2. Exact support upper envelope

For each of the 64 left fixed-mask choices, take the exact minimal-TT local Walsh factors used by the admitted left-rank-48 theorem. Replace each local factor value only by its nonzero indicator and existentially eliminate every index except `I9`.

This is a Boolean-semiring support projection. It is intentionally an **upper envelope** on the exact coefficient support: local signed cancellations may remove additional assignments, but an assignment absent from this Boolean projection is rigorously absent from the exact coefficient tensor.

Let `S_m` be the resulting feasible set of nine-bit assignments.

Across all 64 physical left fixed-mask cases,

`117 <= |S_m| <= 216`.

The exact size distribution is

- 117: 2 cases;
- 120: 2 cases;
- 144: 12 cases;
- 174: 4 cases;
- 177: 2 cases;
- 180: 6 cases;
- 216: 36 cases.

Therefore every physical left map satisfies

`rank_{I9 | (O7,J6)} L_m <= |S_m| <= 216`.

This bound is exact as a support-derived rank upper bound and uses no floating tolerance, trail cap or approximation.

## 3. Consequence for any parent Schmidt factorization

For a fixed physical mask, write the exact 171-leaf parent as

`M_m = L_m R_m`.

The physical rank-envelope theorem gives an exact factorization of the right action through some interface basis `B_m` with dimension `rho_m <= 27`, so one may choose the left parent factor as

`X_m = L_m B_m`.

Multiplication by `B_m` cannot create a nonzero `I9` assignment that was absent from `L_m`. Hence

`support_I9(X_m) subseteq S_m`

and therefore

`rank_{I9 | (O7,rho_m)} X_m <= 216`

for **every** physical fixed-mask instance, independently of the actual parent rank `rho_m` and independently of the mask-dependent Schmidt basis.

Thus the left parent factor admits an exact two-stage factorization

`I9 -- RL -- (O7,rho_m)`

with a uniform structural bond bound

`dim(RL) <= 216`.

Smaller support cases may use smaller bonds; 216 is the safe all-mask bound.

## 4. Support classes and common coordinate envelope

The 64 physical left-mask cases produce only 13 distinct feasible support sets `S_m`.

Their support sizes by distinct class are

`117,120,144,144,174,174,177,180,180,216,216,216,216`.

The union of all 13 support sets contains 384 of the 512 possible nine-bit assignments, while their intersection contains 96 assignments.

Therefore:

- a mask-conditioned coordinate selector needs at most 216 active states;
- a single mask-independent coordinate selector obtained from the union needs at most 384 states.

No strict subset of the six left fixed-mask control bits determines the exact support class for all 64 cases; all six are needed if one insists on exact support-set identity.

## 5. Exact mask/support selector rank

Define the `64 x 512` binary selector matrix

`C(m,i) = 1` iff `i in S_m`.

Its exact rational matrix rank is

`rank(C)=12`.

The same rank is obtained from the 13 distinct support rows. Thus the mask dependence of the support upper envelope itself has an exact 12-dimensional linear representation.

This gives a concrete exact bridge for later joint-mask composition: the impossible-state selector need not be represented as 64 unrelated tables.

## 6. Error statement

This support pruning is exact. Assignments excluded by the selector have coefficient exactly zero. Therefore the residual introduced by this pruning is

`epsilon = 0`.

The epsilon-rank/tail machinery is not needed for this reduction.

## 7. Machine verifier

Authority verifier:

`scripts/verify_v26_qr_q138_left_i9_support216.py`

It reconstructs the certified 64-leaf left child, enumerates all 64 physical fixed-mask choices, performs Boolean-semiring existential projection onto the nine named indices, checks the support-size distribution, the 13 distinct classes, union/intersection sizes, and the exact rational rank 12 of the `64 x 512` support-selector matrix.

## 8. Scope

This theorem is an exact structural result for the q138 fixed-output one-QR left child and the certified physical fixed-mask family. It does not by itself prove an arithmetic-work exponent reduction, a double-round/full-round result, ranking gain, `alpha<1`, or a minimal possible support/rank bound below 216.