# V26 q138 block1 D4 boundary-fiber no-gain theorem

## Statement

Let `V3` be the exact occurrence-closed block1 row space through repeated variables `D0..3`, with physical row bits

`A0..3, B0..3, D0..3, C15, C16`.

The previously certified exact rank is

`dim(V3)=8192=16*2^9`.

On the new j1 boundary carry `s3`, both coordinate projections are injective:

`rank(P_{s3=0} V3)=8192`,

`rank(P_{s3=1} V3)=8192`.

Equivalently, `V3` has no nonzero vector supported wholly in either `s3` slice.

Therefore the next occurrence-closed repeated-D extension by physical bits `A4,B4,D4`, closing `D4` simultaneously in j1 bit4 and j2 bit20, cannot intersect the generic 8-dimensional local coupled-carry kernel. Its exact row rank is

`rank(D0..4 block)=8*8192=65536=16*2^12`.

Thus the D4 one-site repeated-D extension gives no compression and does not lower the canonical d=1 bound.

## 1. Old D0..2 space and the quarter-turn operator

Write the exact D0..2 row space as `V`, with boundary carry `s2`. The clean D3 theorem already proves

`dim(V)=1024`

and exact projection ranks

`rank(P_{s2=0}V)=rank(P_{s2=1}V)=1024`.

Define the linear quarter-turn operator on the two `s2` slices by

`J(u0,u1)=(u1,-u0)`.

The new verifier constructs the exact rational basis of `V`, constructs `J(V)`, reduces both spaces modulo the odd prime

`p=2147483647`,

and obtains the full possible union rank

`rank_p(V + J(V))=2048`.

All rational denominators are nonzero modulo p. Reduction modulo p cannot increase matrix rank relative to Q. Since the modular rank already equals the maximum possible 2048, the rational union rank is exactly2048, hence

`V ∩ J(V) = {0}`

over Q.

This is an exact rank certificate, not a heuristic modular deficiency estimate.

## 2. Fixed-D3 j2 transfer sectors are a direct sum

For fixed `D3`, the j2 bit19 transfer maps the old carry `s18` into local outputs

`(s19,C19,x19,w19)`

through

`T(s19,s18,C19,x19 xor D3,w19)`.

For each `D3=0,1`, the two `s18` rows have exact rational rank2. Taking all four rows from both D3 values gives exact rank4. Therefore the fixed-D3 j2 output row spaces have zero intersection.

Consequently any rank statement proved inside a fixed D3 sector adds directly across the two D3 sectors.

## 3. The s3=0 projection

At `s3=0`, the addition tensor forces

`A3=s2`,

and then the local outputs are uniquely

`k3=A3 xor B3`,

`q3=A3 xor D3`.

For fixed D3 the four `(A3,B3)` channels are therefore disjoint. In the channel with fixed A3, the map sees exactly the old slice projection `P_{s2=A3}V`, which has rank1024.

Thus each fixed-D3 sector has projected rank

`4*1024=4096`.

The two D3 sectors are disjoint by the j2 direct-sum fact above, so

`rank(P_{s3=0}V3)=2*4096=8192`.

Hence the opposite one-slice fiber is zero.

## 4. The s3=1 projection

Fix D3 and B3. The four local j1 rows indexed by `(A3,s2)` have exact rank2 and obey precisely

`row(A3=0,s2=1)=row(A3=1,s2=0)`,

`row(A3=0,s2=0)=-row(A3=1,s2=1)`.

For the two values of B3, these two-dimensional row spaces are disjoint; their exact union rank is4.

A kernel vector in one fixed-B3 sector would therefore require two old vectors `v0,v1 in V` whose slice pairs satisfy

`v1 = -J(v0)`

(up to the harmless sign convention above). Such a nonzero kernel exists exactly when `V` intersects `J(V)` nontrivially.

Section 1 proves

`V ∩ J(V)={0}`.

Therefore the fixed-D3 `s3=1` map is injective on all four `(A3,B3)` copies of V and has rank4096. Again the two D3 sectors are a direct sum through j2, giving

`rank(P_{s3=1}V3)=8192`.

Hence this one-slice fiber is also zero.

## 5. Consequence for D4

The local D4 coupled-carry tensor is algebraically the same generic one-site map as for D3, with carries relabelled

`(s2,s18) -> (s3,s19)`

and site variables relabelled from3 to4.

Its exact local rank is24/32 and its complete 8-dimensional left kernel consists of the same pair relations

`(A4=0,s3=1) == (A4=1,s3=0)`

for fixed `(B4,D4,s19)`.

Any nonzero intersection of this kernel with `F^8 tensor V3` would require a nonzero vector of V3 supported wholly in one `s3` slice. Sections 3 and 4 prove that no such vector exists.

Therefore the D4 local map is injective on the actual incoming row space:

`rank(D0..4 block)=8*dim(V3)=8*8192=65536`.

No compression occurs.

## Scope

This theorem closes only the one-site occurrence-closed repeated-D extension through D4. It is not a lower bound on the full S1 central rank and does not exclude merged block1/block2 multi-site overlap.

The canonical d=1 representation/factor-generation bound remains

`78+log2(171)=85.4178525148859...`.

All statements are exact and `epsilon=0`.

Verifier:

`scripts/verify_v26_q138_block1_d4_boundary_fiber_no_gain.py`.
