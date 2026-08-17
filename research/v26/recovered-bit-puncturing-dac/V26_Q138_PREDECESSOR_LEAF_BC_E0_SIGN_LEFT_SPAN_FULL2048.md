# V26 Q1.38 predecessor-leaf B/C e0 sign-left span full2048

## Scope

In the B/C second dyadic residue, after the support-only part is confined to the clean668/788 Walsh bases, the e0 carry sectors also produce sign-negative correction functions.

This note asks whether those corrections can be compressed uniformly by showing that their **left sign-factor family** spans a proper subspace of the2048-dimensional S1 row space.

The answer is no. This is a method-scope closure only: it does not prove that the fully assembled e0 correction matrix has rank2048 for every predecessor input.

## Left sign-factor family

For each affine-consistent e0 sector:

1. eliminate the internal variables exactly;
2. impose the radical derivative equations selecting the nonzero Gauss support;
3. write the remaining sign phase on the frozen 11|21 split as a left Boolean phase plus right-dependent linear frequency shifts;
4. multiply by the affine-support left characters.

Up to an overall nonzero scalar sign, this produces a finite family of2048-entry left sign vectors.

Deterministic enumeration gives at least2048 distinct factors in both output positions.

## Exact rational full-span certificate

Take the first deterministic2048 distinct sign vectors and form the `2048 x 2048` matrix whose entries are `+1/-1`.

Reduce the matrix modulo the odd prime

`p=65521`.

Exact modular Gaussian elimination gives

- B: rank2048/2048;
- C: rank2048/2048.

A matrix with nonzero determinant modulo p has an integer determinant not divisible by p, hence a nonzero determinant over Q. Therefore the same2048 sign vectors are linearly independent over Q.

Thus

`dim_Q span{e0 left sign factors}=2048`

for both B and C.

## Consequence

Any B/C second-residue proof that tries to bound the e0 sign correction solely by placing **all possible left sign factors** in one fixed proper subspace of the S1 row space cannot beat the generic2048 cap.

This does not exclude:

- cancellation between different e0 sectors after right coefficients are assembled;
- predecessor-input-dependent restrictions on which sign factors occur together;
- cancellation with the support-only or half-sector correction;
- a different first dyadic lift;
- four-leaf product-level cancellation.

So this is a precise closure of the simple left-factor-span shortcut, not a lower bound on the true second-residue rank.
