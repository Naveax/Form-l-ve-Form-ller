# V26 Q138 universal D16/bit0 shared-v3_12 geometry theorem

## Scope

This isolates the wrap/bit0 factor that carries physical row `C0`, repeated physical sector bit `D16`, and the retained coordinate `v3_12` shared with the block1 side.

The result is universal: it applies to any incoming row space `W` whose retained coordinate contains `v3_12`.

## Local fixed-v geometry

For fixed retained `v=v3_12` and fixed `D16=d`, the two physical `C0` rows are

`K_{d,v}(C0)[s0,u4_0] = T0(s0,C0,d,u4_0 xor v)`.

Exact rational ranks are

- `dim K_{0,v}=2`;
- `dim K_{1,v}=2`;
- `dim(K_{0,v}+K_{1,v})=3`;
- therefore `dim(K_{0,v} intersect K_{1,v})=1`.

Moreover the common row is explicit and independent of v:

`K_{0,v}(C0=1) = K_{1,v}(C0=0)`.

The two retained v slices are disjoint. Hence with v retained explicitly the fixed-D spaces have dimensions4 and4, union6, intersection2.

## Universal lifting to an arbitrary incoming space

Let

`W <= F^{v3_12} tensor R`

be any incoming row space, `dim W=n`.

For fixed D16, adjoining physical C0 and the bit0 map is injective on `F^{C0} tensor W`: within each retained v slice the two C0 rows have rank2, and the v slices stay disjoint. Thus

`dim L_0(W)=dim L_1(W)=2n`.

For the intersection, the local common line has the same preimage for every v slice:

- in D16=0 it is selected by `C0=1`;
- in D16=1 it is selected by `C0=0`.

Therefore every `w in W` maps to one common output under the two sectors, giving an injected copy of W. Conversely the exact local intersection is only that one line in each v slice, so there are no additional directions. Hence

`dim(L_0(W) intersect L_1(W)) = n`.

So the old bit0 geometry `2,2,intersection1` scales **exactly** by `dim W` for every incoming W:

`2n,2n,intersection n`.

## Consequence

The previously observed block1 rank16 numbers

`32,32,intersection16`

were not a special feature of that block1 basis. They are the universal instance `n=16`.

Therefore enlarging block1 through the low repeated-D chain and carry bridge cannot create an extra D16/bit0 gain merely by changing the internal geometry of the shared `v3_12` coordinate.

Combined with the certified extended-block2 j1 geometry

`448,448,intersection424`,

the two D16 tensor-product sectors over any incoming W have union dimension

`448*(2n) + 448*(2n) - 424*n = 1368*n`

per independent D12..15 high prefix.

## Authority

- `scripts/verify_v26_q138_bit0_universal_shared_v312_geometry.py`;
- `.github/workflows/bit0-universal-shared-v312-geometry.yml`.
