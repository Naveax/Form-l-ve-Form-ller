# V26 Q1.38 predecessor-leaf A/D third-residue e1 correction: 362 / 171

## Scope

This theorem controls only the correction inherited from the e=1 sectors when descending from the admitted A/D second dyadic layer to the third dyadic residue across

`S1={0,1,2,3,4,5,12,13,14,15,16}`.

It does not yet bound the direct e=2 part of the third residue, so it is not by itself a complete A/D index-2 dyadic rank bound and not a complete leaf Schmidt-rank or arithmetic-work claim.

The admitted dependency is the uniform A/D second-residue activity theorem:

- A: at most181 of the271 affine e=1 supports are active for any fixed128-bit predecessor input;
- D: at most171 of the274 affine e=1 supports are active.

## Explicit second-lift sign choice

Let `M=2^92 L` and choose the admitted first lift `M0`, so

`M=M0+2M1`.

For an e=0 signed sector, after subtracting the first parity indicator its exact scalar contribution to `M1` is

`(s-1)/2`, `s in {+1,-1}`.

If `q=1` exactly when `s=-1`, then

`(s-1)/2=-q`.

The second-residue binary contribution is therefore `q mod2`. The previous second-layer rank argument may use `-q` rather than `+q` as its integer lift at exactly the same rank cost. With that choice the e=0 sector leaves zero contribution to the third residual.

For an e=1 signed sector the exact scalar contribution to `M1` is `s`. The natural second lift uses the support indicator `+1`, hence after division by2 its third-residue correction is again

`(s-1)/2=-q`.

Therefore, under this explicit same-rank second lift, all inherited sign correction in the third residue comes only from the e=1 sectors.

## Left support size of every e=1 sector

For each exact affine support, keep the11 S1 beta variables on the left and the21 complement beta variables on the right. The previously admitted second-residue theorem already proves zero intersection between the two beta column images, so after fixing the128 predecessor input the support factors into a left affine coset times a right affine coset whenever it is active.

Let `a` be the rank of the11 left-beta columns in the canonical external consistency system. Then the active left affine coset has at most

`2^(11-a)`

points. Any sign-correction matrix gated by that support has nonzero rows only on those left points, so its rational rank is at most `2^(11-a)` independently of the quadratic sign phase.

Exact sector distributions are:

A:

-266 sectors have `a=10`, hence at most2 nonzero left rows;
-5 sectors have `a=11`, hence at most1 nonzero left row.

D:

- all274 sectors have `a=11`, hence at most1 nonzero left row.

The type refinement is

A:178 weight91-full sectors with `a=10`,3 with `a=11`;88 weight92-nullity1 sectors with `a=10`,2 with `a=11`.

D:183 weight91-full and91 weight92-nullity1 sectors, all with `a=11`.

## Uniform correction bounds

For a fixed predecessor input, at most181 A e=1 sectors are active. Even charging the worst two left rows to every active sector gives

`rank_Q(K_A,2^corr) <= 2*181 =362`.

For D every active sector occupies at most one left row and at most171 sectors are active, so

`rank_Q(K_D,2^corr) <=171`.

Equivalently, the inherited e=1 negative-sign part of the third binary residue admits integer lifts of ranks at most362 and171.

These are conservative uniform bounds. A rank-weighted activity optimization could sharpen362 because five A sectors cost only one row, but no such sharpening is needed for this theorem.

## Third-residue decomposition

With the explicit sign convention above, for every fixed predecessor input the third residue decomposes as

`T_A,2 mod2 = E_A,2 + C_A,2`,

`T_D,2 mod2 = E_D,2 + C_D,2`,

where

- `E_2` is the direct e=2 support-indicator component;
- `C_2` is the inherited e=1 negative-sign correction;
- `rank_Q(lift(C_A,2))<=362`;
- `rank_Q(lift(C_D,2))<=171`.

The direct e=2 component remains the active blocker.
