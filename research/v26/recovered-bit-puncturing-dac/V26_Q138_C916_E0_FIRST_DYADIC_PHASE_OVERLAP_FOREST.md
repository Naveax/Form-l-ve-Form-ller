# V26 Q138 C916 C e0 First-Dyadic Phase Overlap Forest

## Status

Frozen exact research result for the 340 first-dyadic term anchors after local Gauss elimination and physical shared-support pullback.

Decision:

`FIRST_DYADIC_ANCHOR_PHASE_GRAPH_MULTIPLE_SUPPORT_COMPONENTS`

`ALPHA_PASS=0`.

## Authority

This pass starts from the merged post-Gauss physical phase authority. The 340 anchors are frozen as:

- 103 singleton anchors;
- 237 selected pair anchors.

Each anchor is represented only on its exact physical affine support in the 149-bit shared coordinate space. An overlap edge exists only when the two physical supports intersect. Its weight is the intrinsic polar rank of the normalized-sign difference restricted to that true intersection. No arbitrary ambient quadratic lift is introduced.

## Exact algorithm

For each polar-rank threshold, deterministic component growth is used. A component is finalized only after a no-addition pass has exhausted every physical-overlap cross edge from that component to every remaining anchor. Therefore the reported component counts are exact even though phase evaluations are cached and performed lazily.

The candidate order prefers larger physical intersections and then stable anchor order. A synthetic weighted-graph regression covers thresholds 0, 2, and 4.

All possible support pairs were checked:

- anchors: 340;
- unordered support pairs: 57,630;
- unique physical-overlap phase edges actually evaluated: 6,502.

The evaluated overlap-edge polar-rank histogram is:

- rank 0: 337;
- rank 2: 2,942;
- rank 4: 1,993;
- rank 6: 1,135;
- rank 8: 95.

Thus physical overlap alone does not imply a rank-0/2/4 phase correction.

## Rank-0 graph

Exact connected components: **9**.

Component sizes:

`[325, 2, 2, 2, 2, 2, 2, 2, 1]`

The deterministic rank-0 forest contains 331 edges, all affine-nonconstant rank-0 phase differences.

## Rank <= 2 graph

Exact connected components: **5**.

Component sizes:

`[332, 2, 2, 2, 2]`

Stable component roots:

`[(0,0), (158,0), (180,0), (236,0), (238,0)]`

The deterministic forest contains 335 edges with rank histogram:

- rank 0: 58;
- rank 2: 277.

So rank-2 corrections merge four of the rank-0 components into the large chart, but four 2-anchor charts remain physically disconnected from it under rank<=2 edges.

## Rank <= 4 graph

Exact connected components remain **5** with the same component sizes and roots:

`[332, 2, 2, 2, 2]`

The deterministic rank<=4 forest contains 335 edges with rank histogram:

- rank 0: 40;
- rank 2: 162;
- rank 4: 133.

Allowing rank-4 corrections does **not** connect any of the four remaining 2-anchor components to the 332-anchor component.

## Interpretation

The single-root model is not merely missing a few rank-4 bridges. The physical-support overlap geometry itself decomposes the 340 frozen anchors into five phase-chart components even when rank-4 overlap corrections are permitted.

The dominant chart is very large: 332 of 340 anchors. The remaining eight anchors form four isolated 2-anchor charts.

This does not yet give a separator-width theorem. Connectivity is only a chart-coverage property. Within each component, path/cycle consistency and the cost of representing affine/rank-2/rank-4 corrections still need to be measured. In addition, every true physical overlap edge can matter pointwise, so a spanning forest alone is not sufficient to bound the full correction family.

## Next exact target

Perform a complete census over all true physical overlap pairs among the 340 anchors, not only the 6,502 lazily required forest edges, and measure:

- total physical-overlap pair count;
- complete intrinsic polar-rank histogram;
- maximum rank by the five frozen phase-chart components;
- cross-component physical-overlap count, which should be zero if the component decomposition is caused by support disjointness rather than rank threshold alone;
- phase-difference type and intersection-codimension histograms.

That census will determine whether each chart admits a uniformly low-rank pointwise correction representation before any quotient-aware first-dyadic message-state or separator-width claim.

## Scope exclusions

Not included:

- complete grouped-e0 carry separator;
- support/e1 carry;
- half cross;
- complete C2;
- `W_repr`;
- arithmetic-work reduction;
- `alpha < 1`;
- ranking/search improvement;
- full-round claim.
