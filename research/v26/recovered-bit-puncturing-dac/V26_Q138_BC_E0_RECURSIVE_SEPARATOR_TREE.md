# V26 Q138 B/C grouped-e0 recursive separator tree

## Scope

This note continues the exact local linear-signature factorization established by PR #112. The shared domain is

\[
V=\mathrm{GF}(2)^{149},
\]

with 128 predecessor coordinates and 21 right-beta coordinates. For every grouped-e0 local factor `g`, PR #112 constructs an exact row space `R_g <= V*` containing the support-syndrome and sector left-frequency measurements seen by that factor.

For a factor subset `S`, define

\[
r(S)=\dim\operatorname{span}\{R_g:g\in S\}.
\]

Because the complete family has rank 149, the exact shared linear-information dimension across the cut is

\[
\lambda(S)=r(S)+r(\bar S)-149.
\]

This is the dimension of the row-space intersection of the two sides.

## Recursive certificate

The probe `scripts/probe_v26_q138_bc_e0_recursive_separator_tree.py` constructs deterministic binary trees from three factor orderings. At every recursive node it evaluates several balanced/asymmetric split candidates. The search rule is heuristic, but the resulting tree is reverified independently edge by edge: every cluster rank, complement rank, and lambda value is recomputed from the exact GF(2) row spaces.

Therefore each reported tree width

\[
W(T)=\max_{e\in T}\lambda(S_e)
\]

is an exact upper bound for that displayed tree. No optimal branchwidth statement is made.

## Clean run 34197401783

### Position B

- grouped factors: 251
- best displayed ordering: `local_rank_ascending`
- maximum depth: 11
- candidate widths:
  - `local_rank_ascending`: 80
  - `local_rank_descending`: 88
  - `multiplicity_then_rank`: 80
- certified displayed tree width:

\[
\boxed{W_B\le 80}
\]

The two root children have exact statistics:

- 167 groups: rank 73, complement rank 125, `lambda = 49`
- 84 groups: rank 125, complement rank 73, `lambda = 49`

Compared with the PR #112 sequential/path certificate `W_B <= 85`, this reduces the displayed linear separator upper bound by 5 dimensions.

### Position C

- grouped factors: 250
- best displayed ordering: `local_rank_descending`
- maximum depth: 11
- candidate widths:
  - `local_rank_ascending`: 83
  - `local_rank_descending`: 80
  - `multiplicity_then_rank`: 83
- certified displayed tree width:

\[
\boxed{W_C\le 80}
\]

The two root children have exact statistics:

- 83 groups: rank 127, complement rank 70, `lambda = 48`
- 167 groups: rank 70, complement rank 127, `lambda = 48`

Compared with the PR #112 sequential/path certificate `W_C <= 89`, this reduces the displayed linear separator upper bound by 9 dimensions.

## Interpretation

The global grouped-e0 linear signature remains injective on all 149 shared coordinates, but a monolithic `2^149` state is not required by the displayed local-factor contraction route. There exist exact recursive linear-signature trees whose largest shared separator has dimension 80 for both B and C.

This is a route certificate, not yet the complete grouped-e0 carry theorem. The next required test is whether the omitted scalar quadratic phase of each e0 sector factors through a modest refinement of these local linear signatures. The natural exact diagnostic is to compute, for each local factor, the maximal subgroup of `ker(R_g)` under which every sector scalar quadratic is invariant. Its annihilator is the minimal linear refinement of `R_g` sufficient to determine all those scalar phases.

## Frozen regression

`scripts/verify_v26_q138_bc_e0_recursive_separator_tree_result.py` recomputes the trees and asserts the clean-run values above. The frozen result is intentionally limited to the displayed deterministic trees.

## Not claimed

No claim is made here about:

- optimal branchwidth;
- quadratic scalar phase having width 80;
- grouped-e0 carry values;
- e0-half cross-carry;
- complete B2/C2;
- `W_repr`;
- `alpha < 1`;
- arithmetic-work reduction;
- ranking/search advantage;
- full-round compression.

`ALPHA_PASS=0` remains unchanged.
