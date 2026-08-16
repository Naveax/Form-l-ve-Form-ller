# V26 q138 Hard-Cap QR Error Example

## Purpose

This note gives a finite, exact calculator example of the error algebra developed in the mathematics-first track. It composes the **published hard per-addition sigma cap** through one inverse ChaCha quarter-round starting from the local q138-style mask.

This example is deliberately separated from the recovered project `max_sigma_weight` implementation. It is not a canonical project cap2/cap3 measurement and not a NO-GO for the historical method. Its purpose is to validate the local residual-Gram / telescoping framework on a concrete source-conditioned orbit.

## 1. Model

Use the standard ChaCha quarter-round and reverse it from output masks

`(A,B,C,D)=(0,2^10,0,0)`.

XOR and rotations are transported exactly in Walsh space.

At each reverse modular addition, use the exact published modular-addition Walsh coefficients but retain only terms with

`wt(sigma)<=K`

for that addition independently.

All kept coefficients are merged exactly by their resulting four-word masks.

Before every modular addition, the exact local omitted l2 defect is computed from the side-mask residual Gram theorem, context by context:

`eta_j^2 = sum_z c_z^T G_K^res c_z`.

Thus omitted trails are not materialized.

## 2. K=2 exact sequence

Starting from unit norm:

### Reverse addition 1: `C += D`

- local residual squared: `1/4`;
- local residual norm: `1/2`;
- kept support after merge: `6`;
- kept squared norm: `3/4`.

### Reverse addition 2: `A += B`

- local residual squared: `7/32`;
- local residual norm: `sqrt(14)/8`;
- kept support after merge: `40`;
- kept squared norm: `17/32`.

### Reverse addition 3: `C += D`

- local residual squared: `17/32`;
- kept support after merge: `0`;
- kept squared norm: `0`.

The hard cap annihilates the entire approximate state at this step.

The final fourth addition therefore receives zero and changes nothing.

Since the full exact inverse QR Walsh operator is orthogonal and the input vector has norm one, the exact full QR output has norm one. The K=2 hard-cap QR output is zero, so the actual final QR approximation error is exactly

`1` in l2 norm.

## 3. K=3 exact sequence

### Reverse addition 1: `C += D`

For the first local mask `w=2^3`, K=3 already includes the entire one-addition Walsh column.

- local residual squared: `0`;
- kept support: `22`;
- kept squared norm: `1`.

### Reverse addition 2: `A += B`

- local residual squared: `23/128`;
- local residual norm: `sqrt(46)/16`;
- kept support: `480`;
- kept squared norm: `105/128`.

### Reverse addition 3: `C += D`

- local residual squared: `769/1024`;
- local residual norm: `sqrt(769)/32`;
- kept support: `416`;
- kept squared norm: `25/512`.

### Reverse addition 4: `A += B`

- local residual squared: `25/512`;
- kept support: `0`;
- kept squared norm: `0`.

Again the final hard-cap QR approximation is identically zero, while the full exact inverse QR output has norm one. The actual full QR l2 approximation error is therefore exactly `1`.

## 4. Concrete coherent-interference identity at K=3, addition 3

This step gives a useful warning against treating energy loss as residual energy.

Before addition 3, the approximate state has squared norm

`105/128 = 840/1024`.

After the kept hard-cap operation, the squared norm is

`25/512 = 50/1024`.

The naive energy decrease is therefore

`790/1024`.

But the exact residual-Gram calculation gives omitted residual squared norm

`769/1024`,

which is different.

Writing

`U y = A_K y + R_K y`,

orthogonality of the full local gate gives

`||Uy||^2 = ||A_K y||^2 + ||R_K y||^2 + 2 <A_K y,R_K y>`.

Substituting the exact values:

`840/1024 = 50/1024 + 769/1024 + 21/1024`.

Hence

`<A_K y,R_K y> = 21/2048`.

The kept and omitted contributions are not orthogonal after coherent endpoint merging. This explicitly demonstrates why

`input energy - kept energy`

is not generally equal to approximation-error energy in a composed trail hull.

## 5. Telescoping upper bounds are safe but can be loose

For K=2, summing the local defect norms gives the safe bound

`1/2 + sqrt(7/32) + sqrt(17/32) > 1`.

For K=3, the analogous sum

`sqrt(23/128) + sqrt(769/1024) + sqrt(25/512)`

also exceeds one.

The true final error is exactly one because the approximation collapses to zero.

Thus simple norm telescoping is a robust upper bound but can be loose. The factorized residual Gram is valuable because it makes each **local** defect exact; further global sharpness would require propagating cross-step error correlations rather than only their norms.

## 6. Mathematical lesson

The q138 path combines:

1. strong local low-sigma concentration at individual additions;
2. rotation-induced carry-tail amplification;
3. coherent interference between kept and omitted pieces;
4. changing source-conditioned mask families after each gate.

Therefore a successful controlled approximation cannot be justified by a fixed statement such as

`K=4 keeps over 80% local energy`.

The relevant object is the evolving source-conditioned state and its gate-by-gate residual Gram.

## 7. Implication for adaptive error allocation

The example motivates a local adaptive cap `K_j` or even mask/context-dependent budget rather than the same hard cap everywhere.

The first K=3 addition is already exact, so spending a larger cap there buys nothing. The later additions are much harder and should receive more of the representation budget if the goal is a fixed global error tolerance.

This is exactly the optimization structure derived in `V26_ERROR_REPRESENTATION_EXPONENT.md`.

A frozen controlled-approximation protocol could therefore allocate error/cost unevenly across the four additions while preserving a preregistered total tolerance.

## 8. Validation status

The kept hard-cap state propagation and residual-Gram values were evaluated with exact dyadic rational arithmetic. The underlying modular-addition coefficient recurrence and the shifted residual-Gram DP were separately exhaustively checked on small word sizes.

Again, these calculations validate the mathematical hard-per-addition model only. They are not measurements of the missing recovered implementation.

## 9. Claims not admitted

This example does not establish that the historical project cap behaves this way, does not close the recovered D&C route, and does not establish full-round compression, ranking gain, alpha<1, or cryptanalytic improvement.