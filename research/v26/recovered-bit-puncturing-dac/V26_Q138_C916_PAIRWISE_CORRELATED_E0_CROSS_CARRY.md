# V26 q=138 C916 pairwise-correlated grouped-e0 cross carry

## Status

Exact pairwise-correlated cross-carry envelope for the current `C1 <= 916` reachable grouped-e0 gauge.

This is **not** the exact all-250-group aggregate carry and is not a complete `C2` theorem.

## Setup

The current C916 reachable grouped-e0 authority has:

- 250 same-support grouped-e0 factors;
- reachable grouped-e0 GF(2) basis dimension `388`;
- support-only Walsh dimension `788`;
- exact ZZ Walsh-complement quotient `128`;
- admitted second-lift total `788 + 128 = 916`.

For each pair of distinct groups, the probe preserves both factors on the same 149-bit predecessor/right state. It conditions simultaneously on the exact support syndromes and shared-only reachability constraints, constructs the exact jointly reachable pair of aggregate left frequencies, maps both local truth vectors into the fixed 388-vector reachable basis, and evaluates the polarization of the XOR-to-integer-lift quadratic carry.

On a fixed support-pair fiber the two truth-vector coordinate functions are affine-linear in the joint frequency-image coordinates. The cross-carry polarization is therefore quadratic, so degree-two ANF interpolation is exact. The two right-only scalar-gauge constants are relaxed over all four fixed patterns, making this an upper envelope for pairwise cross terms.

## Exact result

Clean exploratory run `34222740270`, job `102049464002` completed all group pairs and produced:

- total group pairs: `31125`;
- group pairs completed: `31125`;
- support-pair fibers processed: `610335`;
- scalar fibers processed: `2441340`;
- maximum joint frequency-image rank: `15`;
- mapped frequency-image generators: `83744693`;
- degree-two ANF coefficients inserted: `65447487`;
- coordinate cache size: `25008`;
- truth cache size: `1039920`;
- polar cache size: `8589161`;
- exact pairwise-correlated e0 cross-carry GF(2) span: **`1848`**;
- no saturation at `2048`.

The previously measured ambient pairwise truth hull of the 388-vector reachable e0 basis is also exactly `1848`.

Therefore enforcing exact shared-state reachability separately for every group pair gives no pairwise cross-carry dimension gain:

`NO_PAIRWISE_CORRELATED_CROSS_GAIN`.

## Interpretation

This closes the natural pairwise-envelope route. The failure does **not** imply that the true all-group realized carry has dimension at least 1848. Pairwise envelopes forget higher-order correlations among three or more grouped factors and relax the aggregate right-only scalar relation.

The next valid route must preserve the all-group state structure. The unrefined same-support aggregate support/frequency model has a good C separator tree of width `58`, but the exact aggregate right-only scalar cannot be made local by naive linear refinement without destroying that geometry: the aggregate-scalar refined tree has width `147`.

That leaves a nonlinear/hybrid scalar treatment as the surviving separator route, in particular exploiting the observed split between singleton high-polar-rank groups and multi-sector low-polar-rank aggregate groups rather than linearizing every quadratic scalar into shared-state coordinates.

## Scope

Not included:

- exact all-250-group aggregate e0 carry;
- support/e1 own carry;
- support-times-e0 cross carry;
- half/e0 cross carry;
- exact all-group scalar correlation;
- complete `C2`;
- complete leaf theorem;
- `W_repr`;
- arithmetic-work factor;
- alpha/ranking/search/full-round claim.

`ALPHA_PASS=0`.
