# V26 Q138 C916 e0 exact all-577 phase template cover

## Purpose

Freeze the exact minimum template counts over the complete support-maximal phase-template universe built from all **577 transformed C e0 sectors**.

The preceding geometry authority established 62 support-maximal transformed-sector templates in 18 uniquely owning maximal support classes with class-size histogram `{1:16,21:1,25:1}`. This pass removes the old 24-candidate enumeration cap and solves the complete set-cover problem exactly.

## Exact solver

For any non-empty residual child universe `U`, choose a deterministic uncovered pivot child. Every valid set cover of `U` must contain at least one candidate template covering that pivot. The recurrence therefore branches over every such candidate and solves the strictly smaller residual universe after removing that candidate's covered children.

Residual universes are memoized. Memoization merges only identical subproblems and does not remove any candidate branch. The returned solution is minimum-cardinality; equal-cardinality solutions are resolved by the lexicographically smallest sorted candidate-index tuple.

A synthetic regression includes an explicit 25-candidate class.

## Frozen input geometry

- physical shared dimension: **149**;
- transforms: **577**;
- support-maximal templates: **62**;
- maximal equal-support classes: **18**;
- class-size histogram: `{1:16,21:1,25:1}`;
- unique owner class for all 577 transforms;
- minimum direct residual polar-rank histogram: `{0:413,2:164}`.

## R=0

R=0 is **infeasible**.

The union of all rank-0 admissible templates covers only **413/577** transforms, leaving **164** uncovered. No choice of the 62 maximal templates can therefore provide a complete rank-0 residual cover.

## R=2 exact optimum

The exact global minimum is:

**39 templates**.

The two nontrivial support classes require:

- 25-root / 173-child class: minimum **10** templates;
- 21-root / 356-child class: minimum **13** templates.

The remaining 16 maximal support classes have one candidate root each and therefore force 16 additional templates.

Deterministic R=2 template set:

`[(2,0),(13,0),(15,1),(16,0),(17,0),(18,0),(19,0),(20,0),(21,1),(23,0),(25,0),(27,0),(46,1),(59,0),(61,0),(61,1),(61,3),(69,0),(71,1),(80,0),(83,0),(90,0),(107,0),(110,0),(117,0),(124,0),(132,0),(133,0),(139,0),(140,0),(158,0),(170,0),(180,0),(226,0),(227,0),(227,1),(232,0),(236,0),(238,0)]`.

Template-role histogram:

`{pair_anchor:20,pair_mate:7,singleton_anchor:12}`.

Under deterministic minimum-rank assignment to these selected templates, residual polar-rank histogram is:

`{0:361,2:216}`.

By role:

- pair anchors: `{0:135,2:102}`;
- pair mates: `{0:181,2:56}`;
- singleton anchors: `{0:45,2:58}`.

The memoized exact solver solved 272 residual states in total for the R=2 class problems and examined 717 branches.

## R=4 exact optimum

The exact global minimum is:

**22 templates**.

Both nontrivial maximal support classes require exactly **3** templates, plus the same 16 forced singleton support classes.

Deterministic R=4 template set:

`[(2,0),(13,0),(16,0),(18,0),(19,0),(23,0),(27,0),(61,0),(61,1),(61,3),(69,0),(117,0),(132,0),(133,0),(158,0),(180,0),(197,0),(227,0),(227,1),(232,0),(236,0),(238,0)]`.

Template-role histogram:

`{pair_anchor:13,pair_mate:3,singleton_anchor:6}`.

Deterministic assignment residual polar-rank histogram:

`{0:259,2:267,4:51}`.

By role:

- pair anchors: `{0:118,2:103,4:16}`;
- pair mates: `{0:106,2:112,4:19}`;
- singleton anchors: `{0:35,2:52,4:16}`.

The R=4 solver solved 161 residual states and examined 947 branches.

## Decision

`ALL_577_EXACT_MAXIMAL_TEMPLATE_COVER_R0_INFEASIBLE_R2_39_R4_22`.

These counts are exact set-cover minima in the complete 62-template universe, not heuristic template counts.

## Next exact gate

The next pass converts each chosen child-to-template residual quadratic into its **minimal linear evaluation signature** on the child physical support. For a quadratic residual with polar rank `2r`, the exact translation stabilizer construction gives a signature of rank `2r` or `2r+1`; hence R=2 residuals require at most 3 linear bits and R=4 residuals at most 5 before cross-sector/shared-basis deduplication.

Those signature rows must then be lifted into the 149-bit physical shared domain. The lift is accepted for separator measurement only when its gauge ambiguity is proved contained in the existing per-group radical-support separator basis. Separator cost is measured by actual GF(2) union rank and recursive cut intersections, not by multiplying template counts by per-residual bit bounds.

The common high-rank sign of the selected templates is still unresolved and is not treated as free.

## Scope

No residual-signature separator width is claimed here. No template common-sign cost, complete grouped-e0 separator theorem, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work, alpha, ranking/search, or full-round result is included.

`ALPHA_PASS=0`.
