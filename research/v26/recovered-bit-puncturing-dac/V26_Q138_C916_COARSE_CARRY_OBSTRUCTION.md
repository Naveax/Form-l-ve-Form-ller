# V26 q=138 C916 coarse third-carry obstruction

## Status

Exact diagnostic certificate for the `C1 <= 916` reachable-joint gauge. This note freezes the failure of componentwise ambient third-carry envelopes. It does **not** give a complete `C2` bound.

## Inputs

The current second-lift authority is

- support-only Walsh frequency family: `|U120| = 788`;
- reachable grouped-e0 sign basis: GF(2) dimension `388`;
- reachable exact ZZ quotient contribution: `128`;
- admitted second-lift total: `C1 <= 788 + 128 = 916`.

Separately, the realized relaxed-half inherited third-carry certificate gives span `<=636`, below the repeated k9 target `650`. That result covers only the half-induced component.

## Exact coarse results

For C:

1. **Support-only integer-lift carry.**
   `U120 xor U120` saturates all `2048` left Walsh frequencies. The deterministic saturation witness is `(108, 162, 1885)`.

2. **Reachable sign ambient pairwise truth carry.**
   The pairwise intersection hull of the `388` reachable sign-basis truth tables has exact GF(2) dimension `1848`, after `75078` pairs. It does not itself saturate `2048`.

3. **Reachable sign Fourier union.**
   The union of Fourier supports of the reachable sign basis saturates all `2048` Walsh frequencies after the first `98` basis vectors.

4. **Support-times-sign cross envelope.**
   Shifting that reachable-sign Fourier union by the support frequency family is already full `2048` at support index `0`.

Therefore the natural componentwise ambient-envelope route has no subgeneric frequency gain:

`NO_COMPONENTWISE_AMBIENT_CARRY_GAIN`.

## Interpretation

Saturation here is an obstruction to proving a useful complete `C2` upper bound by separately bounding support-only carry, sign-only ambient carry, and support-times-sign cross products and then taking their ambient union.

It is **not** a lower bound on the true joint realized third-carry span. The second-lift support and sign corrections are correlated by the original sector/predecessor state, and the actual joint family may occupy a much smaller nonlinear subset than the Cartesian product of the ambient component families.

The next mathematically valid route is therefore to parameterize the **actual joint realized second-lift family** in the C916 reachable gauge and compute/interpolate its third carry directly. In particular, `916` is an integer rank certificate, not a claim that there are 916 freely independent Boolean coordinates whose pairwise products may be combined arbitrarily.

## Frozen values

- support frequency dimension: `788`
- support carry xor-sumset: `2048`
- reachable sign basis dimension: `388`
- reachable sign pairwise truth hull: `1848`
- reachable sign Fourier union: `2048`
- full sign spectrum after basis vector: `98`
- support-times-sign shift union: `2048`
- support-times-sign saturation support index: `0`

Exploratory clean PR run: `34219975611`, job `102040536493`.

## Scope

Not included:

- exact joint realized second-lift carry;
- complete `C2`;
- complete B2/C2 leaf theorem;
- `W_repr`;
- arithmetic work factor;
- alpha/ranking/search/full-round claim.

`ALPHA_PASS=0`.
