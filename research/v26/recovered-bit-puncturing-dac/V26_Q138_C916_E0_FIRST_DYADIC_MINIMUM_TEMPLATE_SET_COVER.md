# V26 Q138 C916 e0 first-dyadic minimum template set cover

## Purpose

Freeze the exact minimum number of actual support-maximal transformed phase templates required to cover the 340 frozen first-dyadic term anchors when direct whole-support residual polar rank is bounded by `R=0`, `R=2`, or `R=4`.

This optimization comes after the constructive maximal-support template cover. It does not invent ambient quadratic extensions and does not use overlap-path corrections: a template is admissible for a child only when the template physical support contains the entire child physical support.

## Reproduced geometry

The probe independently reconstructs:

- 340 first-dyadic term anchors;
- 149 physical shared bits;
- 52 support-maximal anchor templates;
- 15 maximal-support equality classes;
- class-size histogram `{1:13, 18:1, 21:1}`;
- containing-maximal candidate-count histogram `{1:24, 18:201, 21:115}`;
- minimum direct residual polar-rank histogram `{0:222, 2:118}`.

Every child belongs to exactly one containing maximal-support equality class. Therefore the global template-count problem decomposes exactly into 15 independent class problems.

## Exact optimizer

Each class has at most 21 candidate roots. For a fixed residual threshold, each candidate is represented by a bit mask over the children it covers. Candidate subsets are enumerated in increasing cardinality and deterministic lexicographic order.

The first covering subset is therefore minimum. Every smaller subset has been exhaustively rejected. This is an exact finite proof, not a greedy or heuristic set-cover result.

## R=0

`R=0` is infeasible.

Even the union of every rank-0 admissible candidate covers only 222 of 340 anchors. Exactly 118 anchors have no rank-0 containing maximal template.

Thus no number of the existing support-maximal templates can give a complete rank-0 cover.

## R=2

The exact global minimum is **33 templates**.

The 13 singleton maximal-support classes each force one template. The two nontrivial classes have exact minima:

- 21 candidate roots / 115 children: minimum **9** templates;
- 18 candidate roots / 201 children: minimum **11** templates.

The 21-root class exhausts 401,929 smaller subsets before finding its first optimum. The 18-root class exhausts 199,139 smaller subsets. Global exhausted subsets below the optimum: **601,068**.

Deterministic R=2 template IDs:

`[(2,0),(13,0),(16,0),(17,0),(18,0),(19,0),(20,0),(23,0),(26,0),(27,0),(28,0),(59,0),(61,0),(69,0),(71,0),(80,0),(83,0),(107,0),(110,0),(121,0),(124,0),(132,0),(133,0),(139,0),(140,0),(158,0),(180,0),(196,0),(226,0),(227,0),(232,0),(236,0),(238,0)]`.

## R=4

The exact global minimum is **19 templates**.

Again 13 singleton classes are forced. Each nontrivial maximal-support class needs exactly **3** templates:

- 21 candidate roots / 115 children: minimum 3;
- 18 candidate roots / 201 children: minimum 3.

The global number of subsets exhausted below the optimum is **402**.

Deterministic R=4 template IDs:

`[(2,0),(13,0),(16,0),(18,0),(19,0),(23,0),(27,0),(61,0),(69,0),(117,0),(132,0),(133,0),(158,0),(180,0),(197,0),(227,0),(232,0),(236,0),(238,0)]`.

## Decision

`MINIMUM_MAXIMAL_SUPPORT_TEMPLATE_COVER_R2_33_R4_19_R0_INFEASIBLE`

## Interpretation

The constructive rank-2 cover from the preceding authority can be reduced from 52 independently chosen roots to an exact minimum of 33 actual templates. Allowing residual polar rank 4 reduces the exact minimum further to 19.

This is a template-count result, not yet a separator-width result. A smaller template count can trade against a more expensive residual signature, and the common high-rank template sign itself is not treated as free.

Before attaching correction signatures to the existing 149-bit radical-support separator, the selected template sets must also be checked against the 237 frozen pair mates on their full physical supports. Pair-mate low-rank differences measured only on overlap do not by themselves justify mate-only regions.

## Scope

No template common-sign cost, no full pair-mate coverage theorem, no complete grouped-e0 separator, no support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work, alpha, ranking/search, or full-round claim is made.

`ALPHA_PASS=0`.
