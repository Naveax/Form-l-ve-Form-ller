# V26 q138 Mask-to-U47 Prefix-119 Theorem

## Purpose

The physical q138 one-quarter-round line already proves that all 4096 mask-conditioned parent interface spaces lie in one exact 47-dimensional rational space `U47`. This note studies the **coefficient action inside that fixed space**, rather than only the per-mask ranks.

Code is only an exact calculator/falsifier. The mathematical object is the finite transfer tensor described below.

## 1. Physical control order

Use the twelve physical controls

`u1_3,u2_3,u1_4,u2_4,u1_5,u2_5,u1_6,u2_6,u1_7,u2_7,u2_8,u2_31`.

Group the first eight controls into four physical site symbols

- `s3=(u1_3,u2_3)`;
- `s4=(u1_4,u2_4)`;
- `s5=(u1_5,u2_5)`;
- `s6=(u1_6,u2_6)`,

each of dimension 4, and keep the final site-7 boundary symbol

`s7=(u1_7,u2_7,u2_8,u2_31)`

of dimension 16.

Let `a=1..48` index the exact common left-interface row-space basis and `r=1..47` index a fixed exact rational basis of `U47`. The exact coefficient tensor is

`T(s3,s4,s5,s6,s7;a,r)`.

No sigma cap, floating rank threshold or approximation is used.

## 2. Fixed U47 coordinate

A lexicographic sparse rational elimination of the canonical 64-dimensional six-interface coordinate gives one valid U47 pivot set

`[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,56,57,58,59,60,61,62,63]`.

This is only a coordinate choice. Any exact invertible basis change inside U47 leaves the ranks below unchanged.

## 3. Exact prefix ranks

Across the first physical sites, the exact successive flattening ranks are

- after `s3`: `4`;
- after `s3,s4`: `16`;
- after `s3,s4,s5`: `64`;
- after `s3,s4,s5,s6`: **`119`**.

Equivalently, in the underlying binary control order, the first seven cuts are full row-rank

`2,4,8,16,32,64,128`,

and the first nontrivial compression occurs after the eighth bit, where the rank is exactly `119 < 256`.

## 4. Why 119 appears

After site 6, the 256 physical prefix assignments generate an exact 140-dimensional reachable prefix-state space in the physical doubled transfer representation.

Propagate that 140-dimensional space through **all 16 exact physical site-7 closures** and then through the fixed common-left/U47 output map.

Exactly 21 independent reachable directions are annihilated by every one of those closures/output maps. Therefore the observable quotient has dimension

`140 - 21 = 119`.

The lower bound `>=119` was certified by a 119-dimensional nonzero modular minor with a prime that does not annihilate any dyadic denominator. The upper bound `<=119` was certified over the rationals by solving the remaining 21 prefix directions against 119 independent directions and verifying that each resulting exact kernel vector maps to zero through all 16 site-7 closures.

Thus 119 is an exact rational rank, not a numerical-SVD estimate.

## 5. Exact grouped representation

The coefficient family therefore admits the exact finite factorization

`(s3,s4,s5,s6) -> C119 -> (s7,a,r)`.

The final four mask controls need not be split further to obtain a valid exact generative representation: they may remain the 16-state physical site-7 closure core.

This is stronger and cleaner than storing 4096 unrelated coefficient matrices.

## 6. Sparse storage accounting

In the exact sparse U47 coordinate used for the calculation:

- the 256 prefix rows expanded over all 16 site-7 closures contain `1,105,936` nonzero rational entries;
- 119 exact basis rows contain `514,699` nonzero entries;
- the exact `256 x 119` coordinate factor contains `12,007` nonzero entries.

Hence the factorized representation uses

`526,706`

nonzero rational entries, a reduction factor

`1,105,936 / 526,706 ~= 2.09972`.

This is a coefficient-representation/storage result only. It is not yet an arithmetic-work theorem.

## 7. Left-mask coefficient falsifier

The six physical left controls are

`u1_8,u1_9,u1_10,u2_8,u2_9,u2_10`.

Although their **support selector** has exact rank 12, the full exact coefficient operators from the external left boundary into the common 48-dimensional interface basis have operator-family span

**`64`**

over the 64 mask assignments.

Successive binary mask cuts attain

`2,4,8,16,32,64`.

Therefore the rank-12 support selector must not be mistaken for a rank-12 coefficient generator. Support feasibility compresses; the exact coefficient family itself uses all 64 mask directions.

## 8. Composition implication

The exact next-layer representation must keep two distinct structures:

1. the rank-12 support selector for the nine-bit I9 feasibility pattern;
2. the coefficient transfer through the common U48/U47 spaces, including the exact 119-state observable prefix quotient on the right-transfer controls.

These objects share physical mask controls but are not interchangeable and must not be multiplied into a guessed `12*47`, `12*119` or other universal rank without an exact coupling theorem.

## 9. Scope correction for the next QR

`U47` is an **internal six-interface coefficient space inside the fixed-coefficient one-QR network**. It is not the full four-word, 128-bit Walsh-mask boundary between two ChaCha QR layers.

Therefore a second QR cannot be attached merely by treating U47 as the whole inter-round state. A valid two-layer contraction must expose/connect the actual intermediate word-mask legs, or prove an exact operator theorem that eliminates them.

This distinction is now part of the canonical continuation.

## 10. Claims not admitted

This theorem does not establish a sharp two-layer width `W2`, arithmetic-work reduction, `alpha<1`, ranking gain or full-round relevance. It supplies an exact coefficient-transfer compression and identifies the correct boundary object required before a genuine second-layer theorem.