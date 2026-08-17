# V26 q138 d=1 low/high star product barrier

## Statement

Let the complete d=1 five-QR star be viewed as the exact central q138 coefficient tensor multiplied by the four predecessor-leaf coefficient vectors on the physical intermediate words A,B,C,D.

Use the already certified occurrence-closed S1 partition into

- low23 physical rows
  `L={A0..5,B0..5,D0..5,C12..16}`;
- high/gap21 physical rows
  `H={A12..16,B12..16,D12..16,C0..5}`.

Then the exact full-star matricization ranks satisfy

`rank_star(L | rest) <= 2^45`,

and

`rank_star(H | rest) <= 490112*2^21 = 3829*2^28`.

The product of these two mode-channel envelopes is exactly

`2^45 * (3829*2^28) = 3829*2^73`,

the current complete materialized-factor size.

Therefore any arithmetic route which first forms complete independent low and high channel bases and then forms their Cartesian joint cannot beat the current materialization envelope. An arithmetic improvement must interleave predecessor-leaf complement contraction, or otherwise exploit additional coefficient structure, before the low/high Cartesian joint is formed.

This is a scoped structural work gate, not an arithmetic-work lower bound for unrestricted algorithms.

## Proof

### Low mode

The certified low23 central row rank is

`n=2^22`.

For a predecessor leaf, a matricization across k of its 32 physical output-mask bits has rank at most `2^min(k,32-k)` by physical Hilbert dimension alone.

Across L the selected predecessor-leaf bit counts are

- A:6,
- B:6,
- C:5,
- D:6.

Thus the product of the four exact leaf rank envelopes is

`2^(6+6+5+6)=2^23`.

For matrices/tensors on the same physical row variables, pointwise multiplication obeys

`rank(X hadamard Y) <= rank(X) rank(Y)`

by expanding both rank decompositions and taking pairwise products. Applying this to the central tensor and four leaf vectors gives

`rank_star(L|rest) <= 2^22 * 2^23 = 2^45`.

### High mode

The complete high/gap operator multiplies an arbitrary incoming low row-space W by the universal exact high-sector channel envelope

`16*30632 = 490112 = 3829*2^7`.

Equivalently, taking a one-dimensional incoming W gives a valid standalone high21 central row-rank envelope `490112`.

Across H the predecessor-leaf bit counts are

- A:5,
- B:5,
- C:6,
- D:5,

so their product rank envelope is

`2^(5+5+6+5)=2^21`.

Therefore

`rank_star(H|rest) <= 490112*2^21 = 3829*2^28`.

### Product barrier

Finally,

`2^45 * (3829*2^28) = 3829*2^73`.

Hence separately materializing both complete mode-channel systems and forming all pairs reconstructs exactly the existing complete factor envelope. The result does not prohibit an on-the-fly scalar contraction that lets complement variables remove channel degrees of freedom before this joint is formed.

## Scope

Exact, epsilon=0. No arithmetic-work reduction, practical evaluator, ranking/search gain, alpha<1, or full-round cryptanalytic relevance is claimed.

Dependencies:

- `V26_Q138_FULL_S1_GAP_RANK3829_THEOREM.md`;
- `V26_Q138_D1_ARITHMETIC_MATERIALIZATION_GATE.md`.
