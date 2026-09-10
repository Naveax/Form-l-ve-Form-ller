# V26 Q138 C916 width-147 orientation lemma

## Scope

Let the 250 exact phase-complete minimal GF(2) group row spaces live in the 149-dimensional physical shared domain. For a group subset `S`, let

`k(S) = dim(intersection_{g in S} K_g)`,

where `K_g` is the exact homogeneous kernel of the minimal row space for group `g`.

For every cut `S | S^c`, the exact connectivity is

`lambda(S) = 149 - k(S) - k(S^c)`.

Hence a width-147 decomposition requires

`k(S) + k(S^c) >= 2`

on every tree edge.

This note isolates a purely combinatorial consequence of two exact kernel-cover facts. It is independent of the historical V25 runtime-byte blocker and uses code only to certify the finite premises.

## Definitions

A side `S` is **plane-covered** when `k(S) >= 2`. Equivalently, there exists a 2-dimensional kernel subspace `P` contained in every `K_g` for `g in S`; therefore all groups of `S` lie in the coverage set of the same kernel plane.

A cut is a **line-line cut** when

`k(S) = k(S^c) = 1`.

Such a cut implies the existence of two nonzero kernel directions `d,e` whose coverage sets together contain all 250 groups: one direction is common to `S`, the other to `S^c`.

## Conditional theorem

Assume both:

1. no pair of nonzero kernel directions covers all 250 groups;
2. no cover of all 250 groups by at most three common 2D kernel planes exists.

Then no branch decomposition of width at most 147 exists.

### Proof

Suppose, for contradiction, that a branch-decomposition tree `T` of width at most 147 exists.

For every edge cut `S | S^c`, width 147 gives

`k(S) + k(S^c) >= 2`.

If neither side were plane-covered, both kernel dimensions would be at most 1. Their sum being at least 2 would force

`k(S)=k(S^c)=1`,

which is a line-line cut. By assumption 1 no such global two-direction cover exists. Therefore **at least one side of every tree edge is plane-covered**.

Both sides cannot be plane-covered simultaneously: choosing one common 2D kernel plane for each side would cover all 250 groups by two planes, contradicting assumption 2. Hence **exactly one side of every edge is plane-covered**.

Orient every tree edge from its plane-covered side toward its non-plane-covered side. Any finite directed tree has a sink vertex: starting from any vertex and repeatedly following an outgoing edge must terminate because the underlying graph has no cycle.

Let `v` be a sink.

- If `v` is an internal vertex of degree 3, each of the three components of `T-v` lies on the plane-covered side of its incident edge. The three leaf sets therefore admit a cover by at most three common 2D kernel planes, contradicting assumption 2.
- If `v` has degree 2, its two incident components are both plane-covered, yielding a cover by at most two planes, again contradicting assumption 2.
- If `v` is a leaf, the complement of that singleton leaf is plane-covered because the unique incident edge points into `v`. The singleton group itself has row rank at most 147 in the 149-dimensional domain, hence kernel dimension at least 2 and is plane-covered as well. Thus all groups are covered by at most two planes, again contradicting assumption 2.

Every possible sink degree contradicts assumption 2. Therefore no width-147 branch decomposition exists. QED.

## Consequence for the current C916 line

PR #170 already gives an explicit exact width-148 tree, so

`branchwidth <= 148`.

PR #171 proves assumption 2 by the 16 exact rank-147 groups: their unique 2D kernels force five distinct planes, so no cover by at most three common 2D kernel planes exists.

PR #174 is designed to decide assumption 1 exactly by checking all unordered pairs among the 3,607 nonzero kernel directions. If PR #174 certifies that no pair covers all 250 groups, the inequalities combine immediately to

`branchwidth >= 148`

and therefore

`branchwidth = 148`.

If a two-direction cover does exist, this lemma remains valid but its first premise is false; the project must then analyze the surviving line-line cut family instead of claiming a lower bound.

## Boundary

This theorem concerns only the exact phase-complete **linear-factorization** branchwidth of the C916 first-dyadic object. It does not rule out nonlinear compression and does not establish complete C2, a lower complete `W_repr`, arithmetic-work reduction, ranking/search gain, full-round relevance, or `alpha < 1`.

`ALPHA_PASS=0`.
