# V26 q138 Right-Map Rank-Conditioning Falsifier

## Purpose

After the exact rank-48 theorem for the 64-leaf side of the certified width-40 bottleneck, the next tempting step is to assign one fixed rank to the opposite 107-leaf map and therefore to the 171-leaf parent message.

That shortcut is false.

The 107-leaf map's exact interface rank changes with the fixed input-mask bits of the fixed-IO coefficient. Therefore any second-stage compression beyond the uniform left-child rank 48 must be treated as **input/source conditioned** unless a separate uniform envelope is proved.

## 1. Geometry

The certified 171-leaf bottleneck splits as

`64 | 107`

through six binary interface variables. The right map is

`R : 2^6 -> 2^24`.

Topology gives only

`rank(R) <= 64`.

For a fixed set of ordinary input-mask bits, its exact rank can be computed without materializing the `64 x 2^24` matrix by the exact Gram contraction

`G_R(z,z') = sum_x R(z,x) R(z',x)`.

Because the coefficients are real dyadic rationals,

`rank(R) = rank(G_R)`.

The doubled tensor network has only the two six-bit interface copies open, so the final Gram matrix is `64 x 64` and can be evaluated exactly with rational arithmetic.

## 2. Exact counterexamples to a universal rank

Several exact fixed-mask instances were evaluated.

### Zero-gauge instance

With the relevant fixed T1/T2 mask bits and affine parity constants set to zero,

`rank(L_64)=48`,

`rank(R)=34`.

Using the 64-dimensional interface Gram space, the exact 171-parent rank is

`rank(L_64 R)=23`.

### All-one representative

For an all-one representative of the corresponding fixed-u families,

`rank(L_64)=48`,

`rank(R)=19`,

and the exact parent rank is

`8`.

### Higher-rank exact representative

For the exact fixed-u pattern

- left T1 bits `(0,1,0)`;
- left T2 bits `(0,0,0)`;
- left parity gauge zero;
- right T1 bits `(0,1,1,0,1)`;
- right T2 bits `(1,1,0,0,1,0,0)` in the local order used by the finite calculation;
- right parity gauge zero;

with the shared T2 bit-8 value consistent across the two children,

`rank(L_64)=48`,

`rank(R)=37`,

and

`rank(L_64 R)=26`.

All three calculations use exact rational local Walsh tensors and exact rational rank elimination; no floating tolerance or historical cap code is involved.

## 3. Consequence

The statements

`rank(R)=34`

or

`rank(parent)=23`

are **not** q138-wide invariants. They are fixed-mask instances.

What *is* currently uniform and admitted is the left-child theorem

`rank(L_64)=48`

for all 64 combinations of its six relevant fixed-u bits, up to affine internal index relabelings.

Therefore the next mathematical object is not one more unconditional scalar rank. It is a rank function / rank envelope

`rho(m) = rank R_m`

or directly

`rho_parent(m) = rank(L_m R_m)`

on the fixed-input mask family `m` that is actually relevant to the q138 coefficient family / source-conditioned contraction.

## 4. Why this is useful for FDS

This dependence is not merely an annoyance. FDS is explicitly source conditioned.

If the source/reachable mask family occupies low-rank sectors disproportionately, an adaptive separator representation can be substantially smaller than a worst-case uniform representation.

Conversely, a compression claim based only on one convenient zero-gauge rank would be invalid.

The correct program is therefore:

1. identify which fixed input-mask combinations are genuinely reachable/relevant for the q138 source-conditioned path;
2. classify `rank(R)` or parent rank on that family;
3. derive a uniform envelope on the relevant family, or a finite sector decomposition with one rank per class;
4. only then reinsert the conditioned rank factors globally and certify the resulting work/message bounds.

## 5. Scope

This note is a falsifier of **mask-independent right-map rank**, not a negative result for algebraic compression.

It does not prove the worst-case right rank, the worst-case parent rank, or a complete `W<=39` tree. It also does not depend on the missing historical V25 runtime bytes.

No practical exact QR evaluation, arithmetic-work reduction, double-round/full-round result, ranking gain, or `alpha<1` is claimed.
