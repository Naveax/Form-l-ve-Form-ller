# V26 q138 C916 e0 complete first dyadic group residual

## Exact arithmetic identity

For every reachable C grouped-e0 support group with multiplicity `m` and restricted phase bits `q_i`, define

\[
R_g=\frac{\sum_i(-1)^{q_i}-(m\bmod 2)}{2}.
\]

The probe verifies this identity pointwise for every bit assignment for the only reachable multiplicities `m in {1,2,4}`.

For a singleton, `R_g=-q`. For even multiplicity, the exact pair identity from the first-dyadic pair certificate is used on a disjoint pairing.

## Exact result

The 250 C support groups have multiplicities `{1:103, 2:57, 4:90}`. Their complete first dyadic residual decomposes into:

- `103` singleton `-q` terms,
- `57` multiplicity-2 signed equality terms,
- `180` multiplicity-4 signed equality terms,
- total: `340` exact residual terms.

The group term-count histogram is `{1:160, 2:90}`.

### Singleton regime

All 103 singleton supports have free dimension 150. The restricted singleton phase polar-rank histogram is

`{142:74, 144:29}`.

Thus the singleton part remains a high-rank quadratic object on its common affine support.

### Pair regime

All 237 selected pair equality differences remain exactly as certified previously:

- polar-rank histogram `{2:237}`,
- affine nonconstant terms `0`,
- genuinely quadratic terms `237`,
- maximum polar rank `2`.

## Interpretation

The first dyadic residual is structurally two-regime rather than uniform:

`TWO_REGIME_FIRST_DYADIC_RESIDUAL`

The even-multiplicity contribution collapses to a very low-rank rank-2 equality layer, while singleton groups contribute high-rank phase bits. Consequently a useful carry representation should not force both regimes through one monolithic quadratic state.

The natural next step is fiber geometry relative to the existing 149-bit shared separator coordinates and the local left-variable fiber. For the pair regime, determine whether the rank-2 restricted polar form descends to the shared quotient, couples shared and local directions bilinearly, or contains local-local quadratic structure. For singleton terms, reuse the existing cut-local quadratic-evaluation machinery rather than pretending their rank is small.

## Scope

This certificate is an exact within-support integer decomposition. The support parameter coordinates include local left variables as well as the shared predecessor/right variables. Therefore the 340-term count and the polar ranks are not separator-state bit counts.

No separator width, complete grouped-e0 carry contraction, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work bound, alpha, ranking/search, or full-round theorem is claimed.

`ALPHA_PASS=0`
