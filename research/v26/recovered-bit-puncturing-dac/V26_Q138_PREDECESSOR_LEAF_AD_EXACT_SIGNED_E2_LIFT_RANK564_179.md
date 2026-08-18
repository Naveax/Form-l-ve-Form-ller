# V26 Q1.38 exact signed e2 lift and A/D index-2 ranks 564 / 179

## Scope

This theorem continues the exact-signed dyadic lift used for the A/D predecessor leaves across

`S1={0,1,2,3,4,5,12,13,14,15,16}`.

The admitted exact signed-e1 lift already gives

A `[3,219,565,2048,...]`,

D `[3,207,364,2048,...]`,

and leaves **zero inherited e0/e1 correction** in the index-2 residual. Hence index2 consists only of the direct valuation-e2 signed sectors.

Clean raw-e2 cover run `32190142624` now shows that the complete raw e2 signed families admit global singleton-template covers of size564 for A and179 for D. Using the exact signed raw-e2 aggregate itself as `K2` is therefore a valid same-parity integer lift and leaves zero inherited e2 correction at index3.

All statements are exact (`epsilon=0`). The complete index>=3 tail remains open.

## Raw e2 family

Clean run `32190142624` enumerates every externally reachable raw direct-e2 sector from the exact carry generator.

A:

- raw reachable sectors: `12098`;
- types: `4003` w91-nullity1 and `8095` w90-full;
- all12098 have cut intersection0;
- global affine right21 singleton-template cover size `564`.

D:

- raw reachable sectors: `12363`;
- types: `4091` w91-nullity1 and `8272` w90-full;
- all12363 have cut intersection0;
- global affine left11 singleton-template cover size `179`.

The raw reachable sector counts equal the previously certified odd direct-support counts12098/12363. Thus no reachable raw e2 support disappears by even multiplicity before the binary direct residue is formed.

The first PR63 implementation used a conservative under-deduplicating condition-map key. That can only retain extra equivalent classes; it cannot make the explicit verified cover artificially smaller. Every final template is checked against every class it claims to cover. Therefore the clean564/179 counts are valid upper bounds even before the fixed-head quotient-dedup rerun.

## Singleton-template aggregation lemma

Fix a predecessor input x. Suppose a family of signed sector matrices is covered by R global affine singleton templates on one matrix side.

For each template, sum all active signed sectors assigned to it. Every summand is supported in the same single row or single column selected by that template at x. Hence the entire template-group sum has rational rank at most1. Summing over R templates gives aggregate rank at most R.

Therefore the exact signed raw-e2 aggregate satisfies

`rank_Q(K_A,2)<=564`,

`rank_Q(K_D,2)<=179`.

## Why the exact signed aggregate is a valid dyadic lift

After the admitted exact e0/e1 lifts, write

`M = K0 + 2 K1 + 4 R2`.

Each raw valuation-e2 sector contributes coefficient `s in {+1,-1}` to `R2`, while higher-valuation sectors contribute even coefficients. Modulo2,

`s == 1 (mod2)`.

Thus the exact signed raw-e2 aggregate is congruent to the direct-e2 binary residue `R2 mod2`. It is a valid integer `K2`.

Choose that aggregate itself as `K2`. Then

`R3=(R2-K2)/2`

contains no contribution inherited from valuation e2. Combined with the exact lower lifts, valuation e0,e1,e2 sectors are now exhausted exactly and contribute zero correction to every later residue.

## New A/D envelopes

The current exact A/D dyadic envelopes become

A `[3,219,564,2048,...]`,

D `[3,207,179,2048,...]`.

B/C remain

B `[36,812,2048,2048,...]`,

C `[84,972,2048,2048,...]`.

This strictly supersedes the previous A565/D364 index-2 authority.

## Dynamic four-leaf recount through k7

With B/C index2 still generic2048, exact convolution gives

- k0 `27,216`;
- k1 `4,793,472`;
- k2 `285,032,304`;
- k3 `6,775,002,288`;
- k4 `74,626,868,736`;
- k5 `479,046,918,480`;
- k6 `2,345,342,671,296`;
- k7 `9,015,469,473,792`.

Hence

`sum(k0..k7)=11,921,550,787,584`.

Against

`2^44=17,592,186,044,416`,

the exact margin is

`5,670,635,256,832`.

With every unresolved index>=3 rank left at the universal2048 cap, k8 is still

`28,230,524,010,496`,

so this is not complete-tail control.

## Structural consequence

The important gain is not merely `565->564` and `364->179`. The lift chain now eliminates inherited corrections through valuation e2. The index3 residual starts from direct valuation-e3 sectors only.

Therefore the next sharp problem is direct-e3 singleton-map complexity, preferably using the arbitrary zero-set internal-rank law and universal singleton-side theorem rather than sectorwise internal RREF.

Still not admitted: lower complete `W_repr(1)`, lower `W_factor-gen`, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round relevance.
