# V26 Q138 C916 phase-complete linear branchwidth = 148

## Canonical decision

For the exact C916 first-dyadic phase-complete group-output family on the 149-bit physical shared domain,

`branchwidth_linear = 148`.

This is an exact theorem for the **linear-factorization** representation family. It closes the current phase-complete linear separator question. It does not close nonlinear compression.

## Certified chain

### Exact local linear spaces — PR #168

All 250 exact group residual outputs have exact minimal GF(2) linear-factorization ranks in

`142..147`,

with histogram

`{142:74,143:16,144:60,145:72,146:12,147:16}`.

The ambient physical shared dimension is 149.

### Dual-kernel geometry — PR #169

There are exactly 3,607 nonzero common-kernel directions across the 250 group spaces. The largest one-direction coverage is exactly 217 groups.

### Width-148 upper certificate — PR #170

Clean run `34473608906` certifies an explicit branch-decomposition tree with

- 499 nodes;
- 498 independently verified non-root edges;
- maximum exact cut connectivity `lambda=148`;
- zero edges above 148.

Therefore

`branchwidth_linear <= 148`.

### No cover by at most three common kernel planes — PR #171

The 16 exact rank-147 groups have kernel dimension exactly 2 and force five distinct 2D kernel planes. Hence all 250 groups cannot be covered by at most three common 2D kernel planes.

### Forced-five construction diagnostic — PR #172

The five forced planes cover 223/250 groups and leave 27 uncovered. This rejects that particular five-plane construction as a complete cover but is not an impossibility theorem by itself.

### Exact seven-plane cover — PR #173

Clean run `34477851082` proves the 27 uncovered groups need exactly two additional 2D kernel planes within the tested exact extension family. Thus the five forced planes plus two additional planes form a seven-plane cover of all 250 groups.

This is useful structural geometry but does not construct a width-147 tree.

### No global two-direction cover — PR #174

Clean run `34479021450`, job `102876839631`, exhaustively checks all

`C(3607,2)=6,503,421`

unordered pairs of nonzero kernel directions.

Exact result:

- global two-direction cover count: `0`;
- maximum one-direction coverage: `217/250`;
- maximum two-direction union coverage: `238/250`;
- exactly one pair attains 238;
- maximizing pair digests:
  - `4a6fb6925a8f5418ab88`;
  - `0913d6a8787377491d4d`.

Therefore no width-147 edge can have kernel split `(1,1)`.

## Lower-bound theorem

For a cut `S | S^c`, let

`k(S)=dim(intersection_{g in S} K_g)`.

Exact connectivity is

`lambda(S)=149-k(S)-k(S^c)`.

A width-147 tree requires

`k(S)+k(S^c)>=2`

on every edge.

PR #174 excludes the only case where neither side has kernel dimension at least 2, namely `(1,1)`. Hence every edge has a plane-covered side. PR #171 excludes both sides being plane-covered simultaneously, because that would give a two-plane global cover. Therefore every edge has exactly one plane-covered side.

Orient every edge from its plane-covered side toward the other side. A finite tree has a sink. At an internal degree-3 sink, the three incident components are each plane-covered and therefore give a cover by at most three common 2D kernel planes, contradicting PR #171. The degree-2 and leaf sink cases similarly give covers by at most two planes.

Hence a width-147 tree cannot exist:

`branchwidth_linear >= 148`.

Combined with the PR #170 upper certificate,

`branchwidth_linear = 148`.

The full proof is frozen in `V26_Q138_C916_WIDTH147_ORIENTATION_LEMMA.md`.

## Mathematical interpretation

The exact phase-complete linear separator is almost maximally wide: 148 versus the 149-dimensional physical shared domain. The C916 first-dyadic object therefore does not expose a useful large compression through exact linear signatures alone.

This is a scoped NO-GO for pursuing progressively refined **linear-factorization separator** families as the main compression mechanism for this object. Repackaging the same linear state under different bases does not change the theorem.

It does **not** imply that the exact nonlinear joint output state has 148 bits of irreducible information. The 250 output functions are nonlinear functions of the same 149 physical bits, and earlier exact value-image work shows that their individual alphabets are far smaller than arbitrary integer functions.

## Next canonical mathematics gate

Stop searching for lower linear branchwidth.

The next target is the exact **nonlinear joint-state / separator** structure. Begin with small exact joint images using the already-frozen nonlinear value-image machinery:

1. reconstruct exact individual output alphabets for the 103 singleton and 147 even-multiplicity groups;
2. compute exact pair joint images `Im(F_i,F_j)` for a deterministic complete or structurally representative pair family;
3. compare exact joint-state bits
   `log2 |Im(F_i,F_j)|`
   with the independent Cartesian budget
   `log2 |Im(F_i)| + log2 |Im(F_j)|`;
4. measure conditional image sizes in both directions;
5. if strong exact collapse exists, lift it to small blocks and separator-aware state construction;
6. if pair images nearly saturate Cartesian products, record that local nonlinear dependency is weak and move to higher-order/shared-latent constructions rather than pretending pairwise compression exists.

Pairwise collapse is only a falsifier/discovery gate. It cannot by itself certify an all-250 nonlinear separator.

## Boundary

Still not admitted:

- exact all-250 nonlinear joint image;
- nonlinear branchwidth optimum;
- complete C2;
- lower complete `W_repr`;
- arithmetic-work reduction;
- ranking/search gain;
- full-round relevance;
- `alpha < 1`.

`ALPHA_PASS=0`.
