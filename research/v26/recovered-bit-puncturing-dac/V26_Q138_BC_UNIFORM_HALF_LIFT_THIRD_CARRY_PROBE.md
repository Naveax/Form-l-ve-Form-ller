# V26 Q1.38 B/C uniform half-lift third-carry probe

## Scope

PR104 proves that the uniform relaxed half-correction span is contained in the already admitted grouped-e0 GF(2) span:

- B grouped-e0 basis dimension 272;
- C grouped-e0 basis dimension 388.

This probe chooses those fixed grouped-e0 bases as an explicit parity-lift gauge for the half correction and measures the induced third-bit carry of that gauge.

It covers the **half correction only**. It does not include the grouped-e0 correction's own lift carry, the support-only lift carry, or cross-carries among those components. Therefore it cannot by itself prove a complete B2/C2 bound.

## Explicit parity lift

For each half-correction truth vector `y` in the PR104 uniform relaxed state family, solve exactly over GF(2)

`y = XOR_i a_i v_i`,

where `v_i` are the fixed grouped-e0 basis vectors.

Choose the integer lift

`K(y) = SUM_i a_i v_i`.

This is congruent to `y mod2` by construction.

Pointwise, if `n` active basis terms equal one, then

`(K-y)/2 mod2 = floor(n/2) mod2 = C(n,2) mod2`.

Hence the induced carry truth vector is exactly

`carry(y) = XOR_{i<j, a_i=a_j=1} (v_i AND v_j)`.

The verifier evaluates this efficiently by accumulating the XOR of previously active basis vectors, so each active term contributes one big-integer `AND` rather than an explicit quadratic loop.

## Uniform state family

The state reduction is copied from the admitted PR104 construction:

- predecessor restricted to the exact half-active affine space;
- predecessor-null and right21 variables combined;
- exact linear image rank 18;
- 2^18 linear states;
- 131072 support-feasible states;
- all 16 scalar phase patterns safely allowed for each feasible state.

Thus the full relaxed family has 2,097,152 state/scalar pairs. The true half states are a subset of this family.

If the verifier completes the full relaxed enumeration without saturation, the reported GF(2) carry-span dimension is a valid **uniform upper span** for the true half-only induced carry of this explicit lift gauge.

If the relaxed carry span reaches2048 early, that gives NO-GAIN only for this relaxed global-left-span route. It does **not** prove that the true unrelaxed carry has rank2048.

## Claim discipline

Not included:

- grouped-e0 own lift carry;
- support-only lift carry;
- cross-carry between support/e0/half lifts;
- complete B2/C2;
- complete leaf Schmidt rank;
- `W_repr`;
- arithmetic-work, alpha, ranking/search, or full-round claims.

The purpose is to decide whether the new 748/936 uniform half construction carries exploitable structure into the next dyadic bit before spending effort on the much harder complete third-residue assembly.
