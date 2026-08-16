# V26 Modular-Addition Sigma-Shell Theorem

## Purpose

This note derives exact sigma-weight energy shells for a single modular addition directly from the Walsh-coefficient characterization used in the bit-puncturing literature.

It is a mathematical result about the modular-addition Walsh transform. Mapping the repository parameter `max_sigma_weight` byte-for-byte to this exact definition still requires restoration of the canonical recovered core. The name and historical context strongly suggest that relationship, but this note does not silently assume implementation identity.

## 1. Source-level modular-addition coefficient formula

For `n`-bit modular addition

`z = x + y mod 2^n`, 

let `u,v,w` be the masks on `x,y,z`. The exact normalized Walsh coefficient is determined by

`gamma = u xor v xor w`

and a binary vector `sigma` satisfying

`sigma_{n-1}=0`,

`sigma_{i-1}=sigma_i xor gamma_i` for `i=n-1,...,1`.

The coefficient is zero if for some `i` with `sigma_i=0` the equality `u_i=v_i=w_i` fails. Otherwise its magnitude is

`2^{-wt(sigma)}`

(with the sign determined by the standard quadratic parity term).

This is Lemma 2 in Flórez-Gutiérrez and Todo, "Improved Cryptanalysis of ChaCha: Beating PNBs with Bit Puncturing", EUROCRYPT 2025 / ePrint 2025/437.

## 2. Sigma-pattern admissibility

Fix the output mask `w` and a candidate sigma vector `s`.

For every bit `i>=1`:

- if `s_i=0`, the nonzero condition forces `u_i=v_i=w_i`, hence `gamma_i=w_i`, so

  `s_{i-1}=w_i`;

- if `s_i=1`, either value `s_{i-1} in {0,1}` is possible.

Therefore the exact downward transition rule is

`if s_i=0: s_{i-1}=w_i; else: s_{i-1} is free`,

with boundary `s_{n-1}=0`.

Equivalently:

- for `w_i=1`, transition `(s_i,s_{i-1})=(0,0)` is forbidden;
- for `w_i=0`, transition `(0,1)` is forbidden.

This is a two-state automaton over the bits of `w`.

## 3. Multiplicity of one sigma pattern

For a fixed admissible sigma pattern `s`:

- at each `i>=1` with `s_i=0`, there is exactly one pair `(u_i,v_i)`;
- at each `i>=1` with `s_i=1`, `gamma_i` is fixed and there are exactly two pairs `(u_i,v_i)`;
- at `i=0`, if `s_0=0` there is exactly one pair, while if `s_0=1`, `gamma_0` is unconstrained by the sigma recurrence and all four pairs `(u_0,v_0)` occur.

Hence the number of nonzero Walsh coefficients having the same sigma pattern is

`mult(s) = 2^{wt(s)+s_0}`.

Every such coefficient has squared magnitude `2^{-2 wt(s)}`. Therefore the total Walsh energy carried by one admissible sigma pattern is

`E(s) = 2^{-wt(s)+s_0}`.

This is an exact orthogonal energy statement for one modular-addition Walsh column because distinct `(u,v)` are distinct Walsh coordinates. It must not be generalized to multi-step trail energy before endpoint signed merging.

## 4. Exact sigma-energy generating polynomial

Define

`E_w(z) = sum_k E_k(w) z^k`,

where

`E_k(w) = sum_{u,v : coefficient nonzero, wt(sigma)=k} coefficient(u,v,w)^2`.

Then `E_k(w)` is the exact fraction of the modular-addition Walsh-column energy in sigma shell `k`.

The polynomial can be computed without enumerating `(u,v)`.

Start with row vector

`v_{n-1} = (1,0)`

indexed by `s_{n-1}=0,1`.

For a transition from bit `i` to `i-1`, define

`q_i = z/2` if `i-1 >= 1`,

`q_1 = z` for the final transition into `s_0`.

The transfer matrices, with rows indexed by `s_i` and columns by `s_{i-1}`, are

for `w_i=0`:

`M_0(q) = [[1,0],[1,q]]`,

for `w_i=1`:

`M_1(q) = [[0,q],[1,q]]`.

Then

`E_w(z) = (1,0) M_{w_{n-1}}(q_{n-1}) ... M_{w_1}(q_1) (1,1)^T`.

Only the bits `w_1,...,w_{n-1}` matter; the LSB `w_0` changes signs/labels but not this energy distribution.

This gives the complete sigma-shell energy distribution in `O(n^2)` symbolic work, or `O(nK)` work if only shells up to cap `K` are retained.

Parseval appears as the identity

`E_w(1)=1`.

## 5. Exact hard-cap error for one modular addition

Let the sigma-cap approximation keep exactly the coefficients with

`wt(sigma) <= K`.

For one fixed output mask `w`, define retained energy

`R_K(w) = sum_{k<=K} E_k(w)`.

Because omitted `(u,v)` coordinates are orthogonal in this single Walsh column,

`||A_w - A_{w,K}||_2^2 = 1-R_K(w)`.

Thus the one-addition cap error is exactly computable from the transfer polynomial, with no trail enumeration and no heuristic energy assumption.

This exact local result is fundamentally different from a composed trail hull, where several trails may merge into the same final endpoint and squared individual trail weights cannot be summed safely.

## 6. Single-output-bit theorem

Take

`w = 2^b`, with `1 <= b <= n-1`.

The admissibility recurrence gives exactly one sigma pattern of every weight

`k=1,...,b`.

For `k<b`, its ones form a contiguous run of length `k` ending at position `b-1`, with `s_0=0`. The shell energy is

`E_k = 2^{-k}`.

The final pattern `k=b` has `s_0=1`, so

`E_b = 2^{1-b}`.

Hence

`E_w(z) = sum_{k=1}^{b-1} 2^{-k} z^k + 2^{1-b} z^b`.

For every `K<b`,

`R_K(w) = 1-2^{-K}`,

so the exact omitted energy is

`1-R_K(w) = 2^{-K}`

and the exact l2 error is

`2^{-K/2}`.

For the q138 bit position `b=10`, if a single modular-addition expansion is directly fed the one-bit mask `2^10`, a sigma cap gives:

- `K=2`: retained energy `3/4`, l2 error `1/2`;
- `K=3`: retained energy `7/8`, l2 error `2^{-3/2}`;
- `K=4`: retained energy `15/16`, l2 error `1/4`;
- `K=5`: retained energy `31/32`, l2 error `1/sqrt(32)`.

These are local one-addition values only; a four-addition quarter-round does not inherit them by simply multiplying retained energies because intermediate masks branch and signed-merge.

## 7. Sigma-complexity of an output mask

Define

`kappa(w) = min wt(sigma)`

over all admissible sigma patterns for output mask `w`.

Then a hard cap `K` annihilates the entire modular-addition Walsh column exactly iff

`K < kappa(w)`.

The value `kappa(w)` is computable by the same two-state automaton using min-plus arithmetic instead of the energy polynomial.

There is also a simple graph lower bound. For every active output bit `w_i=1`, admissibility requires

`s_{i-1} OR s_i = 1`.

Associate edge `{i-1,i}` of the path graph to each active `w_i` (`i>=1`). The support of every admissible sigma vector is a vertex cover of these active edges. Therefore

`kappa(w) >= tau(G_w) = nu(G_w)`,

where `tau` is minimum vertex-cover size and `nu` is maximum-matching size; equality of `tau` and `nu` follows because the graph is bipartite (indeed a subgraph of a path).

The matching bound alone is enough for the annihilation construction below; no claim of general equality `kappa=tau` is needed here.

## 8. Exact annihilation construction

Fix a hard cap `K` and assume `n >= 2K+2`. Choose an output mask whose active bits are

`{1,3,5,...,2K+1}`.

The corresponding active path edges are

`{0,1}, {2,3}, ..., {2K,2K+1}`,

which are pairwise disjoint. Hence every vertex cover, and therefore every admissible sigma vector, has weight at least `K+1`.

Moreover the bound is attainable: choose

`s_{2j}=1`, `s_{2j+1}=0`

for `j=0,...,K` and zero elsewhere. It satisfies the transition rules and has weight exactly `K+1`.

Therefore

`kappa(w)=K+1`.

A sigma cap `wt(sigma)<=K` returns the zero column:

`A_{w,K}=0`,

while the full exact Walsh column has Parseval norm one:

`||A_w||_2=1`.

Thus

`||A_w-A_{w,K}||_2=1`.

This proves that a fixed sigma cap can be maximally inaccurate on specific modular-addition output masks.

For `n=32` and `K=4`, the explicit witness mask with bits `{1,3,5,7,9}` is already sufficient.

## 9. Uniform-approximation consequence

Let `A` denote the full modular-addition Walsh transform from output masks `w` to input-mask pairs `(u,v)`, and let `A_K` be the hard sigma-cap version.

For every fixed `K` and every word size `n >= 2K+2`, the annihilation witness gives a unit basis vector `e_w` such that

`A_K e_w = 0`,

`||A e_w||_2=1`.

Hence

`||A-A_K||_{2->2} >= 1`.

Therefore a fixed `K` cannot be a uniformly accurate approximation to modular addition in operator norm as word size grows.

This does **not** kill source-conditioned or mask-conditioned use of a small cap. It says the mathematical complexity parameter must depend on which masks are actually reached. A useful separator/contraction theory must track something like `kappa(w)` or the full shell polynomial along the reachable mask orbit, rather than treating `K=4` as globally representative.

## 10. Consequence for the V26 tensor program

The bounded-cap Stage0 can remain useful as an exact statement about its retained trail family. But the next mathematics should not ask only whether cap4 support is small.

The sharper questions are:

1. What is `kappa(w)` for the actual intermediate masks reached by the q138 inverse-QR orbit?
2. What fraction `R_K(w)` of each local modular-addition Walsh column is retained at `K=2,3,4,5,...`?
3. Do the reached masks remain in a low-`kappa` family under repeated inverse QR operations, or does `kappa` grow toward `Theta(n)`?
4. Can the two-state energy polynomial be composed with the QR factor graph to produce certified local tail bounds without enumerating all trails?
5. Once a residual is controlled, do the 2|2 tensor flattenings have low epsilon-rank, not merely low exact rank inside a truncated cap?

These are mathematical questions. Code should only evaluate the transfer recurrences and validate small cases.

## 11. Claims not admitted

This theorem does not show that the current recovered implementation uses exactly this hard sigma criterion; canonical source recovery is still required for that implementation statement. It does not show that q138 reaches the annihilation witness, nor does it establish full-round attack improvement or alpha reduction.

It does establish, independently of the missing implementation, that the sigma-weight mechanism from the modular-addition Walsh theory has highly mask-dependent approximation quality and that fixed small sigma caps cannot support a uniform full-exact interpretation.