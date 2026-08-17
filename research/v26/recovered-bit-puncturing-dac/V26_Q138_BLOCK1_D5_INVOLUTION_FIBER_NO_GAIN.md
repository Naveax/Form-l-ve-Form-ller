# V26 Q138 block1 D5 involution/fiber no-gain theorem

## Scope

This closes the complete low-S1 occurrence-closed repeated-D chain through `D5`. It does not close the larger block1/block2 carry bridge toward the extended-block2 high/wrap factors.

All claims are exact over `Q`.

## 1. Old D0..2 graph involution

Let `V` be the exact rank1024 D0..2 row space, with leading j1 boundary carry `s2`.

For every fixed sector `(D0,D1,D2)`, the exact j1 basis has dimension64 and is invariant under pure carry-slice swap

`S(u0,u1)=(u1,u0)`.

This is checked directly on all eight fixed-D sectors:

`rank(J_D + S(J_D)) = 64`.

The complete old space also has injective projections onto either fixed-s2 slice:

`rank(P0 V)=rank(P1 V)=1024`.

Hence `V` is the graph of an invertible operator `G`:

`V={(u,Gu): u in U}`.

Because `S(V)=V`, swapping `(u,Gu)` gives `(Gu,u)` in the same graph. Therefore

`G^2=I`.

This is an exact structural identity, not a numerical eigenvalue observation.

## 2. One repeated-D extension on the +/- eigenspaces

Over `Q`, `G^2=I` implies the decomposition

`U=U_+ direct_sum U_-`,

with eigenvalues `lambda=+1,-1`.

For a single repeated-D j1 site, fix D and keep both physical A/B rows. Restrict the incoming graph to a one-dimensional `G` eigendirection `(u,lambda*u)`.

For each `lambda=+1,-1` the exact local calculation gives

- extended A/B row-space rank4;
- after applying the new-carry quarter-turn `J`, `rank(E + J(E))=8`.

Thus

`E_lambda intersect J(E_lambda)={0}`

for both eigenvalues, independently of their multiplicities.

The two fixed-D j2 transfer spaces each have rank2 and their union has rank4, so D sectors are direct and cannot create cross-cancellation. Therefore the complete D0..3 space `V3` satisfies

`V3 intersect J(V3)={0}`.

Equivalently, the previously derived obstruction polynomial

`G^4+6G^2+I`

reduces under `G^2=I` to

`8I`,

which is invertible over `Q`.

## 3. D0..4 boundary fibers

The generic next-site projection algebra is the same as in the clean D4 boundary theorem:

- at new carry0 the only surviving local rows satisfy `A=s_old` and form injective direct channels;
- at new carry1 the only possible kernel is exactly the incoming `V3 intersect J(V3)` obstruction.

Since that intersection is zero, the exact D0..4 space `V4` has

`rank(P_{s4=0} V4)=65536`,

`rank(P_{s4=1} V4)=65536`.

Both one-slice fiber dimensions are therefore zero.

## 4. D5 closure

The D5 local coupled-carry map is algebraically identical to the D3/D4 one-site map:

- domain rank32;
- exact local rank24;
- explicit8D pair kernel.

That kernel requires nonzero incoming one-slice fibers. Since the D0..4 fibers are both zero, the kernel misses the actual domain.

Therefore the D5 extension is injective on the exact incoming row space and

`rank(D0..5)=8*65536=524288=16*2^15`.

This is exactly the naive rank. Hence

`D0..5 occurrence-closed repeated-D chain = NO GAIN`.

Since sites0..5 are the complete low contiguous run of S1, this exhausts that repeated-D route inside the low S1 segment.

## Authority

- `scripts/verify_v26_q138_block1_d5_involution_fiber_no_gain.py`;
- `.github/workflows/block1-d5-involution-fiber-no-gain.yml`.
