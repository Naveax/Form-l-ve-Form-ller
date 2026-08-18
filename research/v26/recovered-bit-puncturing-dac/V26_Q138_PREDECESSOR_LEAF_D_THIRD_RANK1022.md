# V26 Q1.38 predecessor-leaf D third dyadic residue: rank <=1022

## Scope

This theorem gives a uniform exact integer-lift rank envelope for the **third dyadic residue** of predecessor leaf D across the frozen

`S1={0,1,2,3,4,5,12,13,14,15,16}`

11|21 split.

It combines:

1. the admitted inherited e=1 correction bound `<=171`; and
2. a new constructive global singleton-map cover for the direct e=2 support-indicator component.

It is not a bound on the complete rational Schmidt rank of the full D leaf and not an arithmetic-work claim.

## 1. Direct e=2 condition groups

The admitted direct-e2 condition-group theorem gives:

-12363 odd direct supports;
-8629 distinct predecessor affine conditions;
-condition multiplicities `4895 x1, 3734 x2`;
-every condition group has one common left11 singleton factor after fixing the predecessor input.

Hence a family of global affine left11 singleton maps which covers every active condition-group map gives a direct matrix-rank upper equal to the size of that family.

## 2. Forced D5 common core

The admitted forced-common-core theorem proves that every global maximizer of the direct-e2 active-group count satisfies the five most frequent D predecessor affine equations.

Let this rank-5 affine node be `V_D,5`.

Inside `V_D,5`:

-8084 condition groups are compatible;
-residual condition ranks are `{3:12, 4:649, 5:4129, 6:3294}`.

Outside `V_D,5`, at least one mandatory common equation is violated. The five literal-complement group-count uppers are

`183,185,362,364,364`.

Therefore for every predecessor input outside `V_D,5`,

`rank_Q(E_D,2(x)) <=364`.

## 3. Constructive singleton-map cover inside D5

For each D5-compatible condition group `g`, let

`lambda_g(x) in F2^11`

be its admitted common left-singleton affine map on the group condition.

As deterministic initial representatives, use one group map for every direct-e2 zero-carry site that occurs among D5-compatible odd supports.

Exact recount gives:

-90 zero sites occur inside D5;
-their90 initial maps collapse to54 distinct global affine maps modulo the D5 equations;
-those54 maps already cover4413 of the8084 D5-compatible condition groups.

For every remaining uncovered group, add its own affine singleton map only if the maps already selected do not agree with it on that group's full predecessor condition intersected with D5.

Exact deterministic completion adds797 maps.

Thus there is an explicit global affine-map family of size

`54+797 =851`

such that every D5-compatible direct-e2 condition-group singleton map agrees, on its own predecessor condition, with at least one map from the family.

For any fixed `x in V_D,5`, every active condition-group left row must therefore be one of the851 values obtained by evaluating this fixed template family at x.

Consequently

`rank_Q(E_D,2(x)) <=851`

inside D5.

Together with the outside-core bound364,

`rank_Q(E_D,2(x)) <=851`

uniformly over all128-bit predecessor inputs.

The cover is constructive, not claimed minimal.

## 4. Complete D third residue

Use the admitted explicit same-rank second lift under which all inherited e=0 third correction vanishes. Then

`T_D,2 mod2 = E_D,2 + C_D,2`,

where

`rank_Q(lift(E_D,2)) <=851`,

`rank_Q(lift(C_D,2)) <=171`.

By subadditivity, an integer third-residue lift exists with

`d2 <=851+171 =1022`.

Thus the D dyadic envelope improves from

`D [3,207,2048,...]`

to

`D [3,207,1022,2048,...]`.

This is the first admitted subgeneric A/D third-residue envelope from the current assembled-rank program.

## 5. Product-level consequence and limitation

The new D value must be used in the **dynamic** four-leaf recount, not compared to the old frozen-tail k7 budget in isolation.

However D1022 alone is not sufficient to make the dynamic prefix `k0..k7` fit when A/B/C index-2 ranks remain generic2048. Further A/B/C third-residue reduction or stronger cross-component overlap is still required.

No claim is made about k>=8, complete leaf rank, full d=1 factor reduction, arithmetic work, ranking/search, alpha, or full-round relevance.
