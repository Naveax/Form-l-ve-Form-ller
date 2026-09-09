# V26 Q138 C916 e0 first-dyadic residual-signature separator

## Purpose

Freeze the exact separator cost of the **child-to-template residual signs** induced by the complete 577-transform phase-template authorities. This pass deliberately excludes the selected templates' common high-rank signs.

## Frozen inputs

- physical shared dimension: **149**;
- grouped e0 support groups: **250**;
- frozen Gauss radical-support baseline recursive width: **61**;
- exact R=2 phase-template optimum: **39 templates** with residual polar-rank histogram `{0:361,2:216}`;
- exact R=4 phase-template optimum: **22 templates** with residual polar-rank histogram `{0:259,2:267,4:51}`.

## Minimal residual evaluation signature

For a Boolean quadratic residual `r`, let `B_r` be its polar form. Its exact translation stabilizer is

`K = rad(B_r) ∩ { h : r(h)=r(0) }`.

The annihilator `K^perp` is the minimal linear signature that determines the residual value. The construction is exhaustively verified on all **2,198** Boolean quadratic forms of dimensions 0 through 4.

The result exposes an important distinction: low polar rank does not imply zero linear state cost. A polar-rank-0 residual can still be affine nonconstant and require one signature bit.

## Gauge result

Every child-coordinate signature row is lifted to the ambient 149-bit physical shared domain. For **both** deterministic template optima, every lift-gauge direction is contained in the corresponding pre-existing width-61 Gauss radical-support group basis.

Gauge failures: **0**.

Therefore the reported residual-only recursive widths are gauge-invariant with respect to the chosen ambient representatives.

## R=2 / 39-template residual state

Minimal signature-rank histogram:

`{0:39,1:322,3:216}`.

By polar rank:

- polar rank 0: `{signature 0:39, signature 1:322}`;
- polar rank 2: `{signature 3:216}`.

Every nonzero polar-rank-2 residual needs the extra scalar cut, hence exactly 3 signature bits in this deterministic assignment.

Raw signature rows before per-group union: **970**.

Extra rank over the frozen width-61 group basis:

`{0:13,1:40,2:21,3:65,4:20,5:30,6:59,7:2}`.

Maximum per-group extra rank: **7**. Only **13/250** groups require zero additional residual-signature rank.

Deterministic recursive widths:

- `multiplicity_then_augmented`: **104**;
- `extra_then_augmented`: **111**;
- `augmented_rank_descending`: **126**;
- `augmented_rank_ascending`: **127**.

Best measured residual-only width: **104**.

## R=4 / 22-template residual state

Minimal signature-rank histogram:

`{0:22,1:237,3:267,5:51}`.

By polar rank:

- polar rank 0: `{signature 0:22, signature 1:237}`;
- polar rank 2: `{signature 3:267}`;
- polar rank 4: `{signature 5:51}`.

Raw signature rows before per-group union: **1,293**.

Extra rank over the width-61 basis:

`{0:7,1:31,2:17,3:58,4:20,5:36,6:68,7:6,8:6,12:1}`.

Maximum per-group extra rank: **12**. Only **7/250** groups require zero extra residual-signature rank.

Deterministic recursive widths:

- `multiplicity_then_augmented`: **107**;
- `extra_then_augmented`: **118**;
- `augmented_rank_descending`: **119**;
- `augmented_rank_ascending`: **123**.

Best measured residual-only width: **107**.

## Consequence

The low-rank phase-template cover is mathematically real, but converting every deterministic residual sign into an individually determined minimal linear signature is **not** a separator compression relative to the width-61 radical-support baseline. It expands the measured recursive width to 104 for R=2 and 107 for R=4.

This does not refute phase factoring itself. It refutes the stronger representation that determines every selected child-to-template residual sign independently through a linear signature.

Decision: `RESIDUAL_SIGNATURE_AUGMENTATION_GAUGE_VALID_R2_WIDTH104_R4_WIDTH107`.

## Next target

The next pass must attack the unresolved **common template sign** and aggregation structure rather than adding more individually determined residual bits. Two useful exact gates are:

1. selected-template overlap compatibility / common-phase gluing;
2. R=6/R=8 template-count versus residual-state Pareto measurements, including the one-template-per-maximal-support-class regime.

## Scope

No selected-template common-sign cost is included. No complete grouped-e0 separator theorem, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work, alpha, ranking/search, or full-round claim is made.

`ALPHA_PASS=0`.
