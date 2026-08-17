# V26 q138 Joint-Mask Composition Bridge with Common Interface Span 47

## Purpose

The exact q138 one-QR line now has two complementary all-mask structures:

1. the `64 x 512` left support selector has exact rational rank 12;
2. the union of all 4096 mask-conditioned parent Schmidt/interface spaces has exact dimension 47 inside the canonical 64-dimensional six-bit interface coordinate.

Together these results remove two obstacles to composing the one-QR representation into a later QR/layer:

- support feasibility no longer requires 64 unrelated lookup tables;
- parent coefficient spaces no longer require mask-specific ambient coordinate systems.

This note records the exact composition bridge. It is not yet a complete second-layer contraction theorem.

## 1. Fixed universal parent-interface space

For every physical fixed mask `m`, let `S_m` denote the exact parent Schmidt/interface row space in the canonical six-bit interface coordinate.

The physical rank theorem proves

`dim S_m <= 27`

for each mask and

`dim Span_m(S_m) = 47`.

Therefore there exists one fixed 47-dimensional rational subspace

`U47 subset Q^64`

such that

`S_m subseteq U47`

for all 4096 physical masks.

This does **not** mean a single 27-dimensional basis works for every mask. It means every mask-conditioned active space can be represented in one common 47-dimensional ambient basis.

## 2. Linear composition consequence

Let `T` be any subsequent exact linear operator acting on the canonical six-bit interface coordinate or on a tensor product containing that coordinate.

Because every parent interface vector lies in `U47`, the action of `T` on the parent family is determined by its restriction to `U47`.

Thus a later exact Walsh/QR layer need not first expand each mask-conditioned parent representation back to a 64-dimensional ambient interface and then choose a new basis. One may freeze one rational basis of `U47` and propagate that basis through the next linear operator.

This is the exact algebraic condition needed to begin next-layer composition without basis switching.

## 3. Support dependence

The separate left-I9 support selector

`C(m,i)`

has exact rank 12 and an explicit 12-state factorization with reconstruction coefficients in `{-1,0,1}`.

Hence the zero/nonzero feasibility dependence on the six left mask controls can be carried by a finite exact selector sector rather than by 64 unrelated support tables.

The two structures serve different roles:

- `U47` carries coefficient/interface directions;
- the rank-12 selector carries exact support feasibility.

Do not conflate them into a claimed universal rank `12*47` coefficient bond without further algebra. The coefficient dependence of the mask inside `U47` is a separate tensor that still requires analysis.

## 4. Exact joint representation now available

A mathematically valid next-layer starting representation is therefore:

- keep the six physical mask controls as explicit binary variables;
- express parent interface coefficients in one fixed 47-dimensional rational basis of `U47`;
- attach the exact rank-12 support selector wherever the `I9` feasibility condition is needed;
- apply the next exact QR/Walsh operator directly to the fixed `U47` basis directions.

No approximation is used and no mask-conditioned basis switching remains.

## 5. New sharp blocker

The unresolved object is no longer the common span. It is the **coefficient transfer tensor** in the fixed common basis.

Concretely, after choosing a basis `e_1,...,e_47` of `U47`, determine how the physical mask variables generate the active coefficient combinations in those 47 directions.

The next targets are:

1. exact tensor rank / TT rank of the mask-to-`U47` coefficient map;
2. block or sector decomposition under the five-site transfer algebra;
3. compatibility of those sectors with the rank-12 support selector;
4. growth of the composed separator after applying one more QR layer.

This is strictly smaller and better posed than the previous problem of comparing 4096 independent rank-27 bases.

## 6. Relation to error

All results in this bridge are exact:

- common parent span 47: exact rational span;
- support selector rank 12: exact rational factorization;
- support pruning residual: `epsilon=0`.

Therefore epsilon-rank approximation remains inactive.

## 7. Falsified stronger hypothesis

The hypothesis that all masks share one universal rank-27 parent basis is false at the level of the common-span dimension: the exact union span is 47, not `<=27`.

Thus any exact next-layer construction that uses one fixed ambient parent basis must allow at least 47 directions in this canonical interface representation.

This is a useful scoped NO-GO: it blocks the naive “just reuse one rank-27 basis for all masks” route without blocking structured mask-conditioned sectors inside `U47`.

## 8. Authority

Common-span verification is integrated into

`scripts/verify_v26_qr_q138_physical_rank_envelope27.py`.

Support-selector authority:

- `V26_QR_Q138_LEFT_I9_SUPPORT216_THEOREM.md`;
- `V26_QR_Q138_SUPPORT_SELECTOR_RANK12_COMPOSITION_BRIDGE.md`;
- `scripts/verify_v26_qr_q138_left_i9_support216.py`.

## 9. Scope

This note opens an exact next-layer representation but does not yet prove a complete second-layer contraction, a round-depth width law, arithmetic-work reduction, ranking gain, `alpha<1`, or full-round relevance.