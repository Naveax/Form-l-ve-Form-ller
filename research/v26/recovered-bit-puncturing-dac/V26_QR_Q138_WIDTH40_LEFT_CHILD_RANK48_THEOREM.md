# V26 q138 Width-40 Left-Child Rank-48 Theorem

## Purpose

`V26_QR_Q138_WIDTH40_BOTTLENECK_RANK64_BOUND.md` showed that the unique 171-leaf `2^40` bottleneck in the exact q138 fixed-output one-QR certificate splits as `64|107`, with a six-binary-bit child interface. Topology therefore gives only

`rank(L_64) <= 64`

for the 64-leaf left-child map

`L_64 : 2^16 -> 2^6`.

This note evaluates the actual exact rational map and proves the stronger result

`rank(L_64) = 48`

uniformly over the six fixed ordinary input-mask bits that occur in the relevant T1/T2 local factors.

## 1. Certified child geometry

The 64-leaf child is the left child of the unique 171-leaf maximum cluster in

`V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json`.

Relative to the 171-leaf parent it has

- 16 parent-external binary indices;
- six binary indices connecting it to the 107-leaf sibling.

The interface indices are

- `aux_j2_i8_k0`;
- `aux_j4_i11_k0`;
- `aux_j4_i16_k0`;
- `sig1_7`;
- `sig3_7`;
- `sig4_7`.

Hence its formal matrix shape is

`65536 x 64`.

## 2. Exact local algebra

The map is reconstructed from the same exact dyadic modular-addition Walsh tensor used throughout the V26 exact line:

`T(s,t,u,v,w)`

`= 1[t=s xor u xor v xor w]`

`  * 1[s=1 or u=v=w]`

`  * (-1)^((u xor w)(v xor w))`

`  * 2^{-s}`.

No floating rank tolerance, sigma cap, trail truncation or historical recovered runtime is used.

The fixed-IO local TT orders are the same as the width-40 certificate:

- T4: `(t,s,v,u)`, exact profile `[2,3,2]` after fixing `w`;
- T3: `(u,t,s,v,w)`, exact profile `[2,3,3,2]`;
- T2: `(t,w,v,s)`, exact profile `[2,3,2]` after fixing `u`;
- T1: `(w,v,s,t)`, exact profile `[2,3,2]` after fixing `u`.

For q138, the T4 output mask is `2^3`. Every T4 bit used by this 64-leaf child is outside bit 3, so the relevant fixed T4 `w` bits are zero.

## 3. Uniform fixed-u calculation

The 64-leaf child contains three relevant fixed-u bits from T1 and three from T2. Thus there are

`2^6 = 64`

possible fixed-u patterns.

For every one of those 64 patterns, the complete child network was contracted exactly with rational arithmetic while leaving the 16 external and six sibling-interface bits open. Exact sparse Gaussian elimination on the resulting `2^16 x 64` map gives

`rank = 48`

in all 64 cases.

Therefore the rank-48 statement is not a zero-mask accident and does not depend on those six fixed input bits.

## 4. XOR/parity constants

The local XOR parity factors may carry affine constants under different fixed-mask conventions.

Those constants act by state relabelings on internal binary indices. Such a relabeling is multiplication by a permutation matrix on an internal bond and cannot change the matrix rank of the external-to-interface map.

Representative explicit exact checks with all eight local parity-constant combinations agree with this gauge argument.

Hence the admitted rank is invariant under the affine XOR relabelings relevant to this child.

## 5. Exact result

The topology-only six-bit interface has dimension

`64`.

The actual exact child map has

`rank(L_64)=48`.

Thus the algebraic compression factor beyond topology is

`64/48 = 4/3`.

In effective Schmidt-width units,

`log2(48) = 4 + log2(3) ~= 5.5849625007`,

saving

`6 - log2(48) = log2(4/3) ~= 0.4150374993`

bits relative to the raw six-bit interface.

## 6. Machine verifier

The independent exact verifier is

`scripts/verify_v26_qr_q138_width40_left_rank48.py`.

It reconstructs the width-40 network, finds the unique 171-leaf maximum cluster and its 64-leaf child, rebuilds the exact local TT cores, enumerates all 64 relevant fixed-u cases, and performs exact rational rank elimination.

Expected output includes

`PASS V26_QR_Q138_WIDTH40_LEFT_CHILD_RANK48`

and

`topology_interface=64 exact_rank=48 fixed_u_cases=64 all_exact_fraction=PASS`.

## 7. Global consequence and limit

The 64-leaf child can therefore be replaced exactly, coefficient by coefficient, by a rank factorization through a dimension-48 bond rather than the raw six-bit dimension-64 interface.

However this theorem alone does **not** prove a complete `W<=39` contraction tree. A first natural rank-48 reinsertion geometry admits several sub-39 cuts but reaches a residual 240-factor subproblem that has no split with both child boundaries <=39 in that particular geometry.

That is a scoped contraction-tree failure, not a global lower bound.

The more important next question is the rank of the opposite 107-leaf map and the resulting parent rank. Unlike this left-child rank, the right-map rank is not invariant under all fixed input-mask choices; it must therefore be treated as source/input-mask conditioned rather than silently universalized.

## 8. Claims not admitted

This theorem does not prove `W<=39`, does not prove the 40-bit bottleneck parent has universal rank 48, and does not establish practical exact QR evaluation, arithmetic-work reduction, a double-round/full-round result, ranking gain, or `alpha<1`.
