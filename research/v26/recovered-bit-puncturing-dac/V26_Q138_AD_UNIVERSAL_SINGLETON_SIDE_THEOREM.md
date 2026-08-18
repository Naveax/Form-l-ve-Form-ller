# V26 Q1.38 A/D universal singleton-side theorem

## Statement

Fix the predecessor128 input and the frozen output split

`S1={0,1,2,3,4,5,12,13,14,15,16}`,

`R1={0,...,31}\S1`.

For **every** A/D carry-zero pattern on the93 variable j1..j3 carry sites, whenever the corresponding coefficient sector is externally reachable:

- position A is supported on exactly one `R1` (right21) beta assignment;
- position D is supported on exactly one `S1` (left11) beta assignment.

Consequently every individual A/D signed carry sector, at every dyadic valuation, has rational matrix rank at most1 across the frozen11|21 split.

This is a sectorwise theorem. It does not by itself bound the rank of the sum over many sectors; that requires singleton-map collision/template geometry.

## Internal-rank prerequisite

The all-one j1..j3 A/D homogeneous internal system has rank127 and a one-dimensional kernel N. The only special carry sites are

`(1,0)` and `(3,0)`.

Every nonspecial one-zero constraint preserves rank127, so every newly added homogeneous equality row annihilates N. Hence an arbitrary all-nonspecial zero set still has rank127 with the same kernel N. Either special one-zero constraint already gives rank128, and adding more rows cannot reduce rank.

Therefore every carry pattern is in exactly one of two regimes:

1. no special zero: internal affine fiber has direction N;
2. at least one special zero: internal solution is unique whenever externally consistent.

## Why A always has a unique right21 beta assignment

At j3, for every interior bit `i=1,...,30`, the carry equations always contain

`u_i + v_i + w_i = constant`,

independently of whether the local carry is0 or1.

For output position A,

`w_i = beta_i + V4_{i+8}`.

Hence every `beta_i`, `1<=i<=30`, is an affine function of the internal variables and fixed predecessor/carry data. At bit31 the always-present equality `u_31=w_31` likewise determines `beta_31`.

The only beta bit not covered by these equations is potentially `beta_0`. But `0 in S1`, so every bit in the selected right side `R1` is determined by the internal solution.

In the rank128 regime the internal solution is unique, so the right21 beta assignment is unique immediately.

In the rank127 regime, all-nonspecial carry patterns share the same internal kernel direction N. Exact evaluation of the beta formulas on N gives zero for every `i in R1`:

- for `1<=i<=30`, `N(U3_i)+N(V3_i)+N(V4_{i+8})=0`;
- for `i=31`, `N(U3_31)+N(V4_7)=0`.

Thus moving along the two-point internal fiber changes no right21 beta bit. Therefore A has a unique right21 assignment in every reachable carry sector.

## Why D always has a unique left11 beta assignment

For output position D,

`w_i = V4_{i+8} + beta_{i+8}`

at j3.

For every `k in S1`, put `i=k-8 mod32`. The resulting indices are

`{24,25,26,27,28,29,4,5,6,7,8}`,

all lying in the interior range1..30. Therefore the always-present j3 three-variable equation determines every selected `beta_k`, `k in S1`, from the internal variables and fixed data.

Again the rank128 regime is immediate. In the rank127 regime, exact evaluation on the common kernel direction N gives

`N(U3_i)+N(V3_i)+N(V4_{i+8})=0`

for all these eleven indices. Hence the left11 assignment is invariant across the internal two-point fiber.

The potentially exceptional output bit is `beta_8`, corresponding to j3 bit0; but `8 notin S1`, so it lies on the unselected right side and is irrelevant to the left11 singleton claim.

## Rank consequence

After fixing the predecessor input, an A sector has nonzero matrix entries in at most one right column; a D sector has nonzero entries in at most one left row. This remains true after summing the one- or two-point internal fiber with its exact signs.

Therefore every individual signed A/D carry sector has rational rank at most1 across S1|R1.

## Higher-residue meaning

This theorem upgrades the observed e1/e2 singleton phenomenon to **all** A/D carry patterns. The remaining higher-residue problem is no longer sector rank. It is global map complexity: how many affine singleton templates are needed to cover the simultaneously relevant sectors, or ultimately all carry patterns.

In particular, if all raw valuation-e sectors admit a global affine singleton-template cover of size R, their exact signed aggregate has rank at most R and can be used as an exact integer dyadic lift with no inherited correction from that valuation family.

No complete-leaf rank, complete dyadic-tail, representation, arithmetic-work, alpha or full-round claim is made here.
