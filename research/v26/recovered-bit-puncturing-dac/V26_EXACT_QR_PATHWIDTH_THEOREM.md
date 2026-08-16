# V26 Exact QR Pathwidth Theorem

## Purpose

`V26_EXACT_MODADD_WALSH_MPO_THEOREM.md` shows that one modular-addition Walsh tensor has exact carry/sigma bond dimension 2. The next question is whether composing four such additions through ChaCha XOR/rotation wiring necessarily destroys that compactness.

For a fixed input/output Walsh coefficient of one ChaCha quarter-round, the answer is no in the word-size direction: the exact tensor network has a path contraction whose frontier contains at most **44 binary bonds** for the standard internal rotation offsets that remain after boundary fixing.

This is an exact structural upper bound. It is not a claim that `2^44` memory is practical.

## 1. Standard quarter-round

Write the forward ChaCha quarter-round as

1. `a1 = a0 + b0`
2. `d1 = ROL(d0 xor a1, 16)`
3. `c1 = c0 + d1`
4. `b1 = ROL(b0 xor c1, 12)`
5. `a2 = a1 + b1`
6. `d2 = ROL(d1 xor a2, 8)`
7. `c2 = c1 + d2`
8. `b2 = ROL(b1 xor c2, 7)`.

Fix all four input Walsh masks `(A0,B0,C0,D0)` and all four output masks `(Af,Bf,Cf,Df)`. We seek one exact Walsh coefficient of this bijection.

## 2. Backward mask reduction

Transport the fixed output masks backward through the exact XOR/rotation relations and use the fixed input masks at the opposite boundary.

After eliminating mask variables that are locally determined, one convenient internal description uses four n-bit mask families

`u3, u4, v3, v4`

and four addition sigma chains.

At bit position i the four addition factors depend on the following physical mask bits, with all indices modulo n:

- addition 4: `u4_i, v4_i`;
- addition 3: `u3_i, v3_i, v4_{i+8}`;
- addition 2: `v4_{i+8}, u4_i, v3_{i+12}`;
- addition 1: `v3_{i+12}, u3_i`.

Each addition factor also contains its local sigma bond variables `sigma_i, sigma_{i-1}` as specified by the exact modular-addition MPO.

The standard rotations by 7 and 16 are absorbed into fixed boundary mask relations in this fixed-input/fixed-output reduction; the internal long-range shifts that remain are 8 and 12.

## 3. Local site contraction

At each bit i, the variables `u3_i` and `u4_i` occur only among factors at the same bit site. Contract/sum them locally.

The resulting exact network has n site tensors. Site i is connected to other sites only by:

1. four binary sigma bonds to the adjacent bit site through the four modular-addition carry/sigma chains;
2. one binary `v4` bond linking sites separated by 8;
3. one binary `v3` bond linking sites separated by 12.

Equivalently, ignoring parallel-edge multiplicity, the site interaction skeleton has offsets

`{1, 8, 12}`.

The offset-1 connection has multiplicity four because there are four independent addition sigma chains.

This site network is exact; no sigma cap, trail truncation or approximate rank compression has been introduced.

## 4. Prefix-cut lemma

Order sites as

`0,1,...,n-1`

and contract them sequentially.

For a prefix cut between processed sites and unprocessed sites:

- each non-cyclic sigma chain contributes at most one crossing bond, for a total of at most 4;
- an edge family connecting `i` to `i+d mod n` contributes at most `2d` crossing binary bonds across any contiguous prefix cut, provided `d<n/2`; if the word is smaller or a degeneracy occurs, the count is no larger than the corresponding trivial edge count.

For the standard 32-bit case:

- offset 8 contributes at most `16` crossing bonds;
- offset 12 contributes at most `24` crossing bonds;
- the four sigma chains contribute at most `4`.

Therefore every prefix frontier has at most

`4 + 16 + 24 = 44`

binary indices.

For n=32 the maximum 44 is attained by ordinary contiguous cuts; this is not merely a loose symbolic count.

## 5. Exact contraction-width consequence

Sequentially contracting the n site tensors produces an intermediate tensor whose open index set is exactly the current frontier, after already-internal bonds are summed.

Hence the maximum intermediate **rank in binary indices** is at most 44.

The largest frontier state space is therefore at most

`2^44 = 17,592,186,044,416`

scalar entries.

Thus one fixed-input/fixed-output exact quarter-round Walsh coefficient has a contraction algorithm whose asymptotic dependence on word size is

`O(n * 2^C)`

for a constant C independent of n; the explicit path above gives `C<=44` for the frontier/memory exponent in the reduced standard-QR network.

The arithmetic-operation exponent of a naive local update may be somewhat larger than the frontier exponent because a contraction step also touches the local site tensor. The key theorem is the **word-size-independent width**, not a claim of a practical 32-bit implementation.

## 6. Independent calculator checks

The exact fixed-IO factor graph for n=32 has, before site reduction:

- 252 binary variables;
- 128 local addition-bit factors.

Generic graph heuristics give substantially worse upper bounds:

- min-fill primal width: 61;
- min-degree primal width: 73.

Treating the object as a tensor hypergraph and searching contraction paths gives a largest intermediate of `2^44`, matching the explicit prefix-frontier theorem.

This agreement is a finite sanity check. The 44 upper bound itself follows from the exact site-network construction and cut count.

## 7. Why support explosion is not a width lower bound

`V26_Q138_ROTATION_CARRY_AMPLIFICATION.md` exhibits second-addition Walsh columns with roughly 0.40 to 0.81 billion nonzero explicit coefficients.

The present theorem shows that such support explosion does not imply word-size-exponential contraction width for a fixed full QR coefficient. Those coefficients arise from a network whose local carry state is binary and whose inter-bit wiring has fixed geometric range.

The true difficulty is the size of the frontier induced by composing these low-state local constraints, not the number of trails or nonzero coefficients.

## 8. Fixed-depth ARX generalization

Consider a family of ARX circuits parameterized by word size n with:

- a fixed number Q of modular additions;
- XOR operations represented by local parity constraints;
- rotations by a fixed finite set of integer offsets independent of n;
- fixed input and output Walsh masks.

Each modular addition contributes one binary sigma/carry chain along the bit direction. Every rotation creates a wire family of some fixed offset r.

Group all gate variables belonging to the same bit index into one site tensor. The resulting site network is a finite-range one-dimensional periodic tensor network.

Across a contiguous bit-prefix cut:

- Q carry chains contribute at most Q binary bonds;
- each rotation/wire family of offset r contributes at most `2r` crossing binary bonds.

Therefore the frontier size is bounded by a constant

`C <= Q + 2 sum_e r_e`

where the sum is over the relevant inter-site wire families in the chosen exact network representation.

Consequently a single fixed-IO Walsh coefficient can be contracted with complexity

`poly(n) * 2^{O(C)}`,

and for fixed circuit depth/topology and fixed rotation offsets, C is independent of n.

So the fundamental exponential parameter is circuit/topological width, not word size itself.

## 9. Caveats for scaling claims

The fixed-depth generalization assumes rotation offsets remain bounded constants as n grows. If a scaling family makes rotations proportional to n, the frontier bound can grow with n.

Likewise, if round depth grows with n, the number of carry chains/wire families can grow and C need not remain constant.

The theorem concerns a **single fixed input/output Walsh coefficient**. Leaving a large set of mask legs open, materializing an entire spectrum, or composing many rounds can require much larger effective width or output size.

## 10. Implication for FDS

There are now three distinct complexities:

1. **representation size:** the exact local/full circuit tensor network is O(n) for fixed depth;
2. **single-coefficient contraction width:** bounded by a topology-dependent constant for fixed-depth/fixed-offset circuits;
3. **large-object extraction / ranking / multi-round contraction:** may still be expensive and remains the real unresolved problem.

This separation is exactly what the FDS program needs. A billion-term trail expansion can coexist with a tiny generative network and a still-large but structurally bounded contraction frontier.

The next mathematical task is to reduce the topology-dependent constant, or to prove controlled low epsilon-rank across its large frontiers, rather than enumerating more trails.

## 11. Claims not admitted

`2^44` is far too large to call the exact 32-bit fixed-IO contraction practical. This theorem does not establish a practical full QR computation, a double-round contraction, ranking gain, alpha<1, or full-round relevance.

It establishes a structural fact: **for the fixed-depth standard QR, exact Walsh contraction is not inherently exponential in word size n; the bottleneck is a constant topology-induced frontier.**