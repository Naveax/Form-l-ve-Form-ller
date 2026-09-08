# V26 q138 C916 e0 same-support integer coefficients

## Scope

This certificate tests the first arithmetic aggregation available inside each reachable C grouped-e0 affine support. For every constituent e0 sector, the full Gauss-completed quadratic scalar phase is restricted to the common affine support. Sectors are grouped only when their restricted **nonconstant** quadratic phase is identical; the restricted constant phase contributes an exact signed coefficient `+1` or `-1`.

This is intentionally narrower than a complete grouped-e0 carry contraction. Different restricted phase classes are not combined.

## Exact result

For C:

- reachable e0 sectors: `577`
- affine support groups: `250`
- support multiplicities: `{1: 103, 2: 57, 4: 90}`
- restricted nonconstant phase classes before sign combine: `577`
- classes per support group: `{1: 103, 2: 57, 4: 90}`
- integer coefficients: `{-1: 295, +1: 282}`
- absolute coefficients: `{1: 577}`
- exact opposite zero classes: `0`
- even nonzero coefficient classes: `0`
- support groups with restricted-phase collision: `0`
- support groups with `|coefficient| > 1`: `0`
- zeroed entire support groups: `0`

The full-160-bit affine-support free-dimension histogram is `{150: 248, 151: 2}`; the corresponding deterministic restricted-phase signature sizes are `{11326: 248, 11477: 2}` bits.

## Interpretation

Same affine support does **not** create any cross-sector integer aggregation at this phase resolution. Every one of the 577 reachable sectors occupies its own restricted nonconstant quadratic phase class. Consequently there is no same-class cancellation, no coefficient doubling, and no even nonzero coefficient produced by combining sectors inside a support group.

This sharpens the earlier XOR-aggregate scalar diagnostics: replacing XOR bookkeeping by exact signed-integer combination does not reveal hidden same-support cancellation or multiplicity gain for C916 e0.

The correct decision at this layer is therefore:

`NO_SAME_SUPPORT_CROSS_SECTOR_INTEGER_AGGREGATION`

This does **not** mean that all grouped-e0 carry is absent. In particular, the 295 negative unit coefficients remain signed integer data; any later 2-adic representation/lift of those signs, and any state-dependent interaction between different restricted phase classes, is outside this certificate.

## Next target

The carry search must move beyond same-support/same-phase aggregation. The next useful object is a cross-phase/state-dependent dyadic residual representation that keeps the exact signed unit coefficients and asks whether its evaluation can be compressed on the separator tree without reverting to a monolithic state label.

## Not included

No cross-phase integer combination, aggregate grouped-e0 carry contraction, support/e1 carry, e0-half cross-carry, complete C2, `W_repr`, arithmetic-work bound, alpha, ranking/search, or full-round theorem is claimed.

`ALPHA_PASS=0`
