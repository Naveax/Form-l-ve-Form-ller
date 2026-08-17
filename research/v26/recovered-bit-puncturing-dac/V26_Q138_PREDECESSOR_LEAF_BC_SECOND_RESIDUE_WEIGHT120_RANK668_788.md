# V26 Q1.38 predecessor-leaf B/C second-residue weight120 component

## Scope

Use the explicit first dyadic lifts

`M_B=2^121 L_B = K_B +2R_B`,

`M_C=2^121 L_C = K_C +2R_C`,

with `rank_Q(K_B)<=36`, `rank_Q(K_C)<=84`.

This theorem isolates one exact component of `R_B mod2` and `R_C mod2`: the contribution from carry weight120, i.e. four zero carry sites among the124 B/C carry bits.

It is not yet a complete B/C second-residue rank bound because weight121..124 correction terms from subtracting K remain.

## Why only unique-solution sectors survive at weight120

A carry sector of weight w contributes to M with dyadic factor `2^(121-w)` times its signed internal Gauss sum S.

At weight120 this factor is2. After dividing `M-K` by2, the weight120 contribution to `R mod2` is simply `S mod2`.

Therefore a weight120 sector contributes iff S is odd. For a quadratic Gauss sum over the internal affine fiber, odd S requires a zero-dimensional fiber: internal rank128, nullity0. Then S is `+1` or `-1`, and modulo2 its sign disappears.

Thus the weight120 second-residue component is exactly the XOR of affine support indicators of all affine-consistent rank128 four-zero sectors.

## Exact sector census

There are

`C(124,4)=9,381,251`

four-zero patterns.

The homogeneous B/C internal system is common to positions B and C. Exact rank scan gives

`29,041`

internal-rank128 patterns.

After full external affine consistency:

- B: `29,021` consistent unique-solution sectors;
- C: `28,549` consistent unique-solution sectors.

## Walsh frequency union

For an affine support indicator across the frozen S1|complement split, its rational row space is contained in the span of the left Walsh characters appearing in the projection of the affine dual row space to S1.

Take the union of these homogeneous left frequency sets over every affine-consistent rank128 weight120 sector.

Exact full scan gives

- B: `668` distinct S1 Walsh frequencies;
- C: `788` distinct S1 Walsh frequencies.

Hence the ordinary integer sum of all consistent support indicators has rational matrix rank at most668 for B and788 for C. Its reduction modulo2 is exactly the weight120 component of the second residue.

Therefore there exist integer lifts U_B,U_C of the weight120 second-residue component with

`rank_Q(U_B)<=668`,

`rank_Q(U_C)<=788`.

Both are below the generic single-leaf rank cap2048 and below the approximate k6 target968 for B/C if A/D next residues remain generic.

## Remaining second-residue work

The complete `R_B mod2`, `R_C mod2` also contains correction terms coming from carry weights121..124 after the explicit first lift K is subtracted and divided by2.

To obtain complete B/C second-residue bounds near or below968, the combined additional correction rank should stay roughly below

- B:300;
- C:180,

relative to the current weight120 envelopes668/788. These are search targets, not proved correction bounds.
