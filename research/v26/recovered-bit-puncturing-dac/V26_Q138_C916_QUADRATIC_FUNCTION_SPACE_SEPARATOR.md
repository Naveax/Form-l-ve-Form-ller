# V26 q=138 C916 quadratic function-space separator

## Status

Exact GF(2) function-space intersection certificate for the C same-support aggregate grouped-e0 dependence when the right-only scalar is retained as a quadratic polynomial instead of being forced into a linear refinement of the original 149 shared-state bits.

This is a structural separator diagnostic, not yet an exact nonlinear contraction-state or carry theorem.

## Function-space model

For each grouped-e0 factor `g`, define `F_g` as the GF(2) span of:

1. its exact aggregate support/frequency linear signature coordinates; and
2. its exact aggregate right-only scalar Boolean quadratic polynomial, represented in the degree-`<=2` ANF coordinate space on the 149 shared predecessor/right variables.

The ambient degree-two coordinate count is

`1 + 149 + C(149,2) = 11176`.

For a factor subset `S`, let `F_S` be the span of the local function coordinates in that subset. The exact function-space intersection dimension across a cut is

`lambda_F(S) = dim(F_S) + dim(F_Sbar) - dim(F_all)`.

Every reported `lambda_F` is therefore an exact GF(2) subspace-intersection dimension for the displayed function family.

Important caveat: evaluations of nonlinear functions on a common 149-bit input can satisfy compatibility constraints that are not captured by function-space dimension alone. Thus `2^lambda_F` is not promoted here as an exact dynamic-programming state count.

## Exact global ranks

For C:

- aggregate linear-signature global rank: `149`;
- aggregate scalar-polynomial global rank: `199`;
- aggregate scalar polar-form global rank: `171`;
- combined linear-plus-scalar function global rank: `321`.

## Exact separator trees

### Linear signature only

Best displayed width: **`58`**.

This reproduces the existing same-support aggregate separator geometry.

### Scalar polynomial only

Best displayed width: **`6`** using `multiplicity_then_function`.

The scalar family has large global rank `199`, but very little shared function-space intersection across the displayed recursive decomposition.

### Scalar polar form only

Best displayed width: **`12`** using `function_rank_ascending`.

### Combined linear signature plus scalar polynomial

Best displayed exact function-space width: **`70`** using `multiplicity_then_function`, depth `10`.

Candidate widths:

- function-rank ascending: `79`;
- function-rank descending: `90`;
- multiplicity-then-function: `70`;
- multiplicity-then-linear: `70`.

Root children:

- 166 groups: rank `206`, complement rank `159`, `lambda_F=44`;
- 84 groups: rank `159`, complement rank `206`, `lambda_F=44`.

At the 125/125 balanced cut under the best function order:

- combined function ranks `169 | 224`, `lambda_F=72`;
- scalar-only ranks `122 | 83`, scalar intersection `lambda=6`;
- linear-only ranks `56 | 148`, linear intersection `lambda=55`.

## Comparison

The key separator widths now line up as:

- unrefined aggregate linear signature: `58`;
- combined quadratic function space: **`70`**;
- hybrid linear skeleton from PR #125: `83`;
- full aggregate-scalar linear refinement from PR #124: `147`.

Therefore the near-monolithic width `147` is not intrinsic to the aggregate scalar family. It is largely a cost of demanding that every quadratic scalar become a function of extra **linear shared-state coordinates**. Keeping the scalar as a quadratic function preserves much smaller cut overlap.

Verdict:

`QUADRATIC_FUNCTION_SPACE_PRESERVES_SMALL_SEPARATOR_OVERHEAD`.

## Next exact diagnostic

The next step is to inspect every edge of the best combined tree and decompose its shared function-space intersection into:

- functions already lying in the global linear-signature subspace; and
- a genuinely quadratic residual quotient.

If the nonlinear residual stays small, the interface can be represented as ordinary linear separator coordinates plus a small number of quadratic function evaluations, after which exact realizability/image counting can be attacked with polynomial-time quadratic Gauss-sum primitives rather than enumerating `2^149` shared states.

## Authority

Exploratory clean run: `34225778615`, job `102059429159`.

## Scope

Not included:

- exact nonlinear message count;
- all-group aggregate grouped-e0 carry;
- support/e1 carry;
- half/e0 cross carry;
- complete `C2`;
- complete leaf theorem;
- `W_repr`;
- arithmetic-work factor;
- alpha/ranking/search/full-round claim.

`ALPHA_PASS=0`.
