# V26 q138 C916 e0 first-dyadic template residual Pareto

## Purpose

Complete the exact template-count versus individually determined residual-signature trade-off after the frozen R2/R4 authority.

The complete transformed-sector universe has 577 transforms, 62 support-maximal template candidates and 18 unique maximal-support equality classes on the 149-bit physical shared domain. The width-61 Gauss radical-support separator remains the baseline.

This pass raises the allowed child-to-template residual polar-rank threshold to R=6 and R=8, solves the exact template set cover in every support class, converts every deterministic residual quadratic into its exact minimal linear evaluation signature, lifts those signatures gauge-aware into the 149-bit shared domain and remeasures recursive separator width.

Selected templates' common high-rank signs are not included and are not treated as free.

## Exact template minima

Both thresholds reach the structural lower bound of exactly one template per maximal support class:

- R=6: **18 templates**;
- R=8: **18 templates**.

Thus no solution can use fewer than 18 templates within the frozen maximal-support template model, because the 18 support classes are mutually distinct and each transform has a unique owner class.

For R=6, the deterministic assignment residual polar-rank histogram is

`{0:168, 2:295, 4:100, 6:14}`.

For R=8, it is

`{0:163, 2:221, 4:99, 6:87, 8:7}`.

## Exact minimal residual signatures

For every residual quadratic `r`, the translation stabilizer is

`K = rad(B_r) ∩ {h : r(h)=r(0)}`,

and its annihilator `K^perp` is the minimal linear evaluation signature determining the residual sign.

For R=6, the exact signature-rank histogram is

`{0:18, 1:150, 3:295, 5:100, 7:14}`.

For R=8, it is

`{0:18, 1:145, 3:221, 5:99, 7:87, 9:7}`.

The scalar-cut histogram is `{0:18,1:559}` at both thresholds. In particular, even after reducing to only 18 common templates, 559 of the 577 deterministic residuals retain a nontrivial scalar/affine cut in this individually determined signature representation.

## Gauge gate

Every child-coordinate signature row is lifted to the physical 149-bit shared domain. For both R=6 and R=8, every lift-gauge direction is contained in the corresponding pre-existing radical-support group basis.

Gauge failures: **0**.

Therefore the residual-only widths reported here are gauge-invariant for this representation.

## R=6 separator result

Raw minimal signature rows before per-group union: **1633**.

Per-group extra rank over the width-61 basis:

`{0:3, 1:20, 2:17, 3:54, 4:75, 5:54, 6:19, 7:7, 8:1}`.

Maximum extra rank is 8 and only 3/250 groups need no extra residual-signature state.

The exact recursive candidate widths are:

- `multiplicity_then_augmented`: **104**;
- `extra_then_augmented`: **104**;
- `augmented_rank_ascending`: 129;
- `augmented_rank_descending`: 133.

The deterministic tie-break selects `multiplicity_then_augmented`, with width **104** and depth 9.

## R=8 separator result

Raw minimal signature rows before per-group union: **1975**.

Per-group extra rank:

`{0:3, 1:13, 2:17, 3:48, 4:10, 5:119, 6:12, 7:25, 8:2, 9:1}`.

Maximum extra rank is 9 and again only 3/250 groups need no extra residual-signature state.

The exact recursive candidate widths are:

- `multiplicity_then_augmented`: **100**;
- `augmented_rank_ascending`: 116;
- `extra_then_augmented`: 124;
- `augmented_rank_descending`: 131.

Thus the best measured residual-only point in the R2/R4/R6/R8 family is

\[
\boxed{18\text{ templates},\quad W_{\mathrm{residual-only}}=100}
\]

at R=8.

Decision:

`ALL_577_TEMPLATE_RESIDUAL_PARETO_R6_T18_W104_R8_T18_W100`.

## Interpretation

Allowing larger residual quadratic rank successfully minimizes the number of common high-rank template phases: both R=6 and R=8 reach the unavoidable 18-template support-class floor.

However, the stronger representation that independently determines every child-to-template residual sign remains much more expensive than the width-61 radical-support baseline. R=8 improves the residual-only width from 104/107 to 100, but 100 is still not a compression target.

Therefore further progress should not come from adding more individually determined residual-signature bits. The next exact target should attack aggregation/common-phase structure directly, especially selected-template overlap/gluing and the exact first-dyadic grouped integer/Gauss function rather than each residual separately.

## Scope exclusions

Selected-template common high-rank sign cost is unresolved and excluded. No complete grouped-e0 separator theorem, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work improvement, alpha, ranking/search or full-round result is claimed.

`ALPHA_PASS=0`.
