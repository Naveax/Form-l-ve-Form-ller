# V26 Q138 C916 e0 all-transform maximal phase template cover

## Purpose

Freeze the support-maximal phase-template geometry obtained after rebuilding the template universe from all **577 transformed C e0 sectors** rather than only the 340 first-dyadic term anchors.

The preceding full-sector coverage gate proved that the anchor-only maximal-template universe misses three pair-mate supports. This pass therefore allows every transformed sector, including pair mates, to become a template candidate.

## Exact universe

- physical shared dimension: **149**;
- transformed sectors: **577**;
- roles: **237 pair anchors + 237 pair mates + 103 singleton anchors**.

## Complete support-maximal template geometry

The all-transform universe contains **62 support-maximal transformed-sector templates**.

Role histogram:

`{pair_anchor:26, pair_mate:10, singleton_anchor:26}`.

Support-dimension histogram:

`{140:7, 142:55}`.

These 62 templates form **18 maximal equal-support classes** with class-size histogram:

`{1:16, 21:1, 25:1}`.

The two nontrivial classes contain 25 and 21 distinct phase candidates on the same two large support classes. The remaining 16 support classes have one maximal transformed-sector template each.

## Full ownership

Every one of the 577 transformed sectors is contained in exactly one maximal support class:

`owner_class_count_histogram={1:577}`.

There are no transforms with zero owners and no transforms with multiple maximal support-class owners. Therefore the eventual template set-cover optimum decomposes exactly by these 18 support classes.

## Previously uncovered pair mates

The three pair mates missed by the anchor-only template universe are now themselves support-maximal transformed-sector templates:

- `(61,1)`, support dimension 140;
- `(61,3)`, support dimension 140;
- `(227,1)`, support dimension 140.

They belong to deterministic singleton maximal support classes in the all-transform ordering. Thus the physical-support coverage obstruction from the anchor-only universe is fully explained rather than patched by an ad hoc exception.

## Direct residual-rank geometry

For every transformed sector, minimize the direct whole-support sign-difference polar rank over every template in its unique containing maximal support class.

The exact histogram is:

`{0:413, 2:164}`.

By role:

- pair anchors: `{0:147, 2:90}`;
- pair mates: `{0:188, 2:49}`;
- singleton anchors: `{0:78, 2:25}`.

Therefore **all 577 transformed sectors admit a direct full-support residual of polar rank at most 2** once the complete all-transform maximal-template universe is used.

## Why the exact minimum template count is not frozen here

The previous exact set-cover solver enumerates all candidate subsets in a maximal equal-support class and was intentionally guarded at 24 candidate roots. The complete all-transform geometry has one class with **25** candidates.

Accordingly this pass does not silently raise the guard or label a heuristic result as exact. It stops with:

`ALL_TRANSFORM_MAXIMAL_CLASS_TOO_LARGE_FOR_ENUMERATION_25`.

The next pass must use an exact pruned branch-and-bound set-cover solver with valid lower bounds and deterministic optimality certificates for the 25-root class, while retaining the exact class decomposition proved here.

## Consequence

The previous 52-template anchor universe is obsolete as a complete full-sector template universe. The complete geometry is now 62 maximal transformed-sector templates in 18 uniquely owning support classes.

The promising fact is stronger than before: full-sector support coverage is complete and every sector has an R<=2 direct residual candidate. The unresolved quantity is the **minimum number of templates** required at R=0, R=2 and R=4.

Only after that exact optimization is frozen should residual evaluation signatures be lifted into the existing 149-bit radical-support separator. The common high-rank sign of selected templates remains a separate unresolved cost and is not treated as free.

## Scope

No complete template-count optimum is claimed in this note. No separator-width attachment, template common-sign cost, complete grouped-e0 separator theorem, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work, alpha, ranking/search, or full-round result is included.

`ALPHA_PASS=0`.
