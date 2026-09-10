# V26 Q138 C916 width-147 orientation lemma

## Status

**Certified exact on 2026-09-10.**

For the 250 phase-complete exact minimal GF(2) group row spaces in the 149-dimensional physical shared domain, width 147 is impossible. Combined with the already-certified width-148 construction, the exact linear-factorization branchwidth is

`branchwidth_linear = 148`.

This is a mathematics-first finite theorem. The scripts are only exact certificate/falsifier machinery.

## Definitions

For a group subset `S`, define

`k(S) = dim(intersection_{g in S} K_g)`,

where `K_g` is the exact homogeneous kernel of the minimal row space for group `g`.

For every cut `S | S^c`, exact connectivity is

`lambda(S) = 149 - k(S) - k(S^c)`.

Therefore a width-147 decomposition would require

`k(S) + k(S^c) >= 2`

on every tree edge.

A side `S` is **plane-covered** when `k(S) >= 2`, equivalently when one common 2-dimensional kernel subspace is contained in every `K_g` for `g in S`.

A cut is a **line-line cut** when

`k(S) = k(S^c) = 1`.

Such a cut necessarily implies two nonzero kernel directions whose coverage sets together contain all 250 groups.

## Exact finite premises

### Premise A: no global two-direction cover

PR #174, clean GitHub Actions run `34479021450`, job `102876839631`, exhaustively checked all unordered pairs among the exact 3,607 nonzero common-kernel directions.

Exact counts:

- nonzero kernel directions: `3,607`;
- unordered direction pairs: `6,503,421`;
- global two-direction covers: `0`;
- maximum one-direction coverage: `217/250`;
- maximum two-direction union coverage: `238/250`;
- exactly one direction pair attains 238;
- its digests are `4a6fb6925a8f5418ab88` and `0913d6a8787377491d4d`.

Hence no width-147 edge can be a `(1,1)` line-line cut.

### Premise B: no cover by at most three common 2D kernel planes

PR #171 proves this exactly from the 16 rank-147 groups

`[5,8,24,62,113,154,155,156,158,179,182,186,234,239,241,244]`.

Each has kernel dimension exactly 2 and therefore forces one unique 2D kernel plane. Those 16 groups force five distinct planes. Thus any common-2D-plane cover of all 250 groups needs at least five planes, in particular more than three.

PR #173 later shows that a seven-plane cover does exist: the five forced planes cover 223 groups and exactly two additional planes cover the remaining 27. That positive seven-plane construction is compatible with, and does not weaken, the no-three-plane theorem used below.

## Theorem: width 147 is impossible

Suppose, for contradiction, that a branch-decomposition tree `T` has width at most 147.

For every edge cut `S | S^c`,

`k(S)+k(S^c)>=2`.

If neither side were plane-covered, both kernel dimensions would be at most 1. Their sum being at least 2 would force

`k(S)=k(S^c)=1`,

a line-line cut. Premise A excludes that. Therefore at least one side of every edge is plane-covered.

Both sides cannot be plane-covered simultaneously, because one common 2D plane for each side would give a two-plane cover of all groups, contradicting Premise B. Thus **exactly one side of every tree edge is plane-covered**.

Orient every edge from its plane-covered side toward its non-plane-covered side. Every finite directed tree has a sink vertex.

Let `v` be a sink.

- If `v` is an internal degree-3 vertex, all three components of `T-v` are plane-covered, giving a cover of all leaves by at most three common 2D planes. This contradicts Premise B.
- If a degree-2 vertex is allowed by the chosen tree convention, both components are plane-covered, giving a cover by at most two planes, again contradicting Premise B.
- If `v` is a leaf, the complement of that singleton is plane-covered. The singleton group itself has row rank at most 147 in the 149-dimensional domain, hence kernel dimension at least 2, so it is plane-covered as well. This gives a cover by at most two planes, again contradicting Premise B.

Every possible sink contradicts Premise B. Hence no width-147 branch decomposition exists.

Therefore

`branchwidth_linear >= 148`.

## Exact equality

PR #170, clean run `34473608906`, already supplies an explicit exact width-148 branch-decomposition certificate:

- 499 nodes;
- 498 independently checked non-root edges;
- maximum exact `lambda = 148`;
- edges above 148: `0`.

Thus

`branchwidth_linear <= 148`.

Combining both inequalities gives

`branchwidth_linear = 148`.

## Interpretation

The phase-complete C916 first-dyadic linear-factorization state is almost maximally wide relative to its 149-dimensional physical shared domain. The exact linear separator family therefore does not provide the dramatic compression sought by FDS at this object.

This closes **linear-factorization branchwidth only**. It does not rule out nonlinear compression or a smaller exact nonlinear joint state / nonlinear separator.

## Boundary

This result does not establish:

- the exact all-250 nonlinear joint image;
- a nonlinear separator optimum;
- support/e1 carry or half-cross closure;
- complete C2;
- a lower complete `W_repr`;
- arithmetic-work reduction;
- ranking/search gain;
- full-round relevance;
- `alpha < 1`.

`ALPHA_PASS=0`.
