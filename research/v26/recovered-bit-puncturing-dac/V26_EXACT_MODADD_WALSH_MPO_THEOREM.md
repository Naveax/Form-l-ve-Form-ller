# V26 Exact Modular-Addition Walsh MPO Theorem

## Purpose

The trail-enumeration view makes one modular-addition Walsh column look enormous. The exact coefficient formula reveals a more fundamental representation: the complete three-mask Walsh correlation tensor of modular addition is a one-dimensional tensor network with a binary hidden state.

This is an **exact representation theorem**, not an approximation and not a sigma cap.

It suggests a different research direction: represent the full Walsh operator by constant-bond local tensors and study the treewidth/bond growth caused by composing those tensors through ChaCha rotations/XOR/addition wiring.

## 1. Full addition Walsh tensor

For n-bit modular addition

`z = x + y mod 2^n`,

let

`A_n(u,v,w)`

be the normalized Walsh coefficient from output mask w to input masks u,v.

The exact coefficient theorem introduces binary hidden variables

`sigma_{n-1},...,sigma_0`

with boundary

`sigma_{n-1}=0`

and recurrence, for i>=1,

`sigma_{i-1}=sigma_i xor u_i xor v_i xor w_i`.

A coefficient is nonzero only if

`sigma_i=1`

or

`u_i=v_i=w_i`

at every bit i. When nonzero,

`A_n(u,v,w)= product_i [(-1)^{(u_i xor w_i)(v_i xor w_i)} 2^{-sigma_i}]`.

The sign factor is written as a product because the global exponent is the mod-2 sum of the bitwise exponents.

## 2. Local tensor

For every bit i>=1 define a local tensor

`T_i(s,t;u,v,w)`

with binary bond indices

`s=sigma_i`, `t=sigma_{i-1}`

and physical mask bits u,v,w by

`T_i(s,t;u,v,w)`

`= 1[t = s xor u xor v xor w]`

`  * 1[s=1 or (u=v=w)]`

`  * (-1)^{(u xor w)(v xor w)}`

`  * 2^{-s}`.

For i=0, define the terminal tensor

`T_0(s;u,v,w)`

`= 1[s=1 or (u=v=w)]`

`  * (-1)^{(u xor w)(v xor w)}`

`  * 2^{-s}`.

Equivalently one may introduce a dummy `sigma_-1` determined by the recurrence and contract it with an all-ones boundary vector. Both conventions give the same scalar.

## 3. Exact tensor-train contraction

Then

`A_n(u,v,w)`

`= sum_{sigma_0,...,sigma_{n-2}}`

`  T_{n-1}(0,sigma_{n-2};u_{n-1},v_{n-1},w_{n-1})`

`  * product_{i=1}^{n-2} T_i(sigma_i,sigma_{i-1};u_i,v_i,w_i)`

`  * T_0(sigma_0;u_0,v_0,w_0)`.

Because the recurrence determines at most one sigma path for each `(u,v,w)`, the contraction reproduces exactly:

- the zero/nonzero condition;
- the exact sign;
- the exact magnitude `2^{-wt(sigma)}`.

Thus the complete `2^n x 2^n x 2^n` Walsh tensor has a tensor-train / matrix-product representation of bond dimension at most **2** along the bit direction.

## 4. Representation size

The explicit tensor has `2^(3n)` entries before exploiting zeros.

The TT/MPO representation uses O(n) local tensors. Each interior local tensor has dimensions

`2 x 2 x 2 x 2 x 2`

and therefore only 32 raw entries, most of which are zero or simple dyadic signs.

Hence the exact structural representation size is O(n), with constant hidden-state dimension 2.

For n=32, the entire modular-addition Walsh operator can therefore be specified by a few dozen constant-size tensors even though individual columns may contain hundreds of millions or more nonzero coefficients.

This is exact generative representation, not sparse enumeration.

## 5. Bond dimension is the carry/sigma state

The bond variable sigma is precisely the bit-to-bit state that communicates the nonlinear carry-correlation constraint across a cut between adjacent bit positions.

The enormous global support arises from summing over physical mask choices while this hidden state remains only binary.

This distinction is central:

- **support complexity** can be exponential;
- **generative tensor-network state complexity** can remain constant locally.

The recovered D&C trail method exploited part of this phenomenon indirectly by factorizing local hulls. The MPO theorem exposes it at the exact full-addition level.

## 6. Reversible two-word addition gate

For the reversible ChaCha gate

`F(x,y)=(x+y,y)`,

with output masks `(w,q)` and input masks `(u,b)`, the full Walsh coefficient is

`A_F((u,b),(w,q)) = A_n(u, b xor q, w)`.

The additional relation

`v = b xor q`

is bitwise and can be imposed by a local XOR-copy tensor at each bit. It does not increase the carry/sigma bond dimension.

Therefore the complete reversible two-word addition Walsh operator also has an exact O(n), constant-bond tensor-network representation.

## 7. Exact XOR and rotation tensors

The other ChaCha operations are even simpler in Walsh space:

- XOR assignments transport masks through local parity constraints;
- rotations are permutations of bit-mask wires.

Both have exact constant-size local tensor descriptions and introduce no approximation error.

Therefore a complete ChaCha quarter-round Walsh operator can be written as a tensor network composed of:

- four bond-2 addition carry/sigma chains;
- local XOR constraint tensors;
- rotation wire permutations.

The full operator is exact. Trail enumeration is one contraction strategy for this network, not the definition of the network itself.

## 8. New central complexity question

Once the exact operator is represented this way, the key issue is no longer

`How many trails exist?`

but

`What is the contraction width / treewidth / induced bond dimension of the composed bit-level tensor network under the ChaCha wiring?`

Rotations are the likely source of width growth: they connect low-bit carry chains from one addition to shifted bit positions before the next addition, producing long-range edges when all four addition chains are overlaid.

This reframes the exact problem as a graph-width problem.

## 9. Relation to q138 rotation/carry amplification

`V26_Q138_ROTATION_CARRY_AMPLIFICATION.md` shows that after the first reverse addition, an 8-bit rotation moves a tiny mask family from bits 0..3 into bits 24..27, after which the next addition has hundreds of millions of nonzero explicit Walsh coefficients.

The MPO theorem shows the complementary fact:

those same huge columns still arise from a bond-2 carry chain.

So explicit support explosion does **not** by itself prove that exact computation or exact representation must explode. The relevant obstruction would be growth of bond dimension/treewidth when multiple addition chains and rotations are composed.

This is a more fundamental falsifier than raw trail count.

## 10. Single-coefficient evaluation

For fixed masks `(u,v,w)`, contracting the bond-2 chain is O(n), although the published recurrence already gives an even simpler direct evaluation.

More importantly, fixing only a subset of physical mask indices and leaving the others open produces an exact compressed tensor over the remaining masks. Its complexity is governed by the open physical dimensions and contraction ordering, not by the number of explicit nonzero coefficients.

This is precisely the setting needed for FDS-style source-conditioned marginals and punctured spectra.

## 11. Composition and bond growth

Composing two MPOs generally multiplies bond dimensions before recompression. For ChaCha, however, additions act on different word pairs at different times and rotations permute physical wires, so a naive one-dimensional MPO ordering may be poor.

The appropriate object is therefore a general tensor network, not necessarily one global TT chain.

Possible exact strategies to analyze next include:

1. choose a bit/word elimination order and compute exact graph treewidth or upper bounds;
2. exploit the four independent addition chains before rotations couple them;
3. seek separators aligned with rotation offsets 16,12,8,7;
4. compare word-major, bit-major and mixed cyclic bit orderings;
5. examine whether source-fixed output masks reduce effective network width before contraction;
6. study exact or epsilon-rank compression of intermediate bonds if exact width grows.

## 12. FDS interpretation

The theorem gives an exact source-independent generative representation for a nonlinear ARX primitive component:

`exponentially many explicit Walsh coefficients`

represented by

`O(n) constant-bond local factors`.

That is a legitimate representation-level compression result.

It is **not** yet a compute-level win, because extracting a large composed object may still require high-width contraction. FDS success levels must keep those claims separate.

The immediate research task is therefore to determine whether the ChaCha composition preserves enough low-width structure for useful exact or certified approximate contraction.

## 13. Claims not admitted

This theorem does not prove low treewidth for a quarter-round/double-round, does not solve the full Walsh spectrum, does not imply attack improvement, and does not establish alpha<1 or full-round relevance.

It does establish that raw modular-addition trail/support explosion is not a fundamental representation lower bound: the full exact local Walsh tensor has bond dimension at most 2.