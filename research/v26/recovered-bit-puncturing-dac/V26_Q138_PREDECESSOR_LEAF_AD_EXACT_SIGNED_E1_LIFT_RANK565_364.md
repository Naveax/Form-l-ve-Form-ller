# V26 Q1.38 exact signed e1 lift and A/D index-2 ranks 565 / 364

## Scope

This theorem sharpens the A/D dyadic descent across the frozen

`S1={0,1,2,3,4,5,12,13,14,15,16}`

11|21 predecessor-leaf split.

It changes the **integer lift choice** at the second dyadic layer. The previous valid lift used the unsigned support indicator for each e1 signed sector. That choice left an inherited third-residue correction. Here we instead lift each e1 sector by its **exact signed matrix**. Exact singleton-side geometry shows that this has the same rank cost, so the inherited e1 third correction vanishes completely.

All statements are exact (`epsilon=0`). This is still a residue-layer theorem, not a complete rational leaf Schmidt-rank theorem and not an arithmetic-work result.

## Scalar dyadic identity

Let

`M = 2^92 L = M0 + 2 M1`

for A/D, with the admitted rank<=3 first lift `M0`.

For an e0 signed contribution, after the first lift the exact contribution to `M1` is

`(s-1)/2 = -q`,

where `s in {+1,-1}` and `q=1` iff `s=-1`.

As already admitted, choose the exact integer e0 second lift `-q`; those terms leave zero higher residual.

For an e1 sector, the exact contribution to `M1` is the signed support matrix

`s * 1_support`.

Modulo2 this equals the ordinary support indicator because `s == 1 (mod2)`. Therefore **any** integer matrix congruent to this support indicator mod2 is a valid second lift. In particular, the exact signed matrix itself is a valid lift.

If that exact signed matrix can be represented at the same rank cost as the unsigned support indicator, then subtracting it leaves zero e1 contribution to `M2=(M1-K1)/2`.

## Exact singleton-side rank of every e1 sector

The admitted e1 support family contains

- A:271 reachable sectors =181 weight91-full +90 weight92-nullity1;
- D:274 reachable sectors =183 weight91-full +91 weight92-nullity1.

For A, clean run `32189193782` verifies that all271 supports have a unique right21 beta assignment for every fixed predecessor input on which the affine support is active. Equivalently, after eliminating the11 S1 beta variables, all21 complement beta variables pivot.

Hence the signed A-sector matrix is supported in one matrix column. Its rational rank is at most1 regardless of the sign variation on its one or two allowed left rows.

For D, all274 e1 supports have left-beta rank11, and clean combined-row run `32159421297` evaluates the corresponding left11 singleton map for every sector. Thus every active signed D-sector matrix is supported in one matrix row and has rational rank at most1.

So the exact signed and unsigned e1 lifts have the same per-active-sector rank bound1.

## Second-lift rank is unchanged

The admitted predecessor-input activity theorem gives at most

-181 simultaneously active A e1 sectors;
-171 simultaneously active D e1 sectors.

Therefore the exact signed e1 part costs at most181 /171 rank respectively.

The admitted exact e0 `-q` budgets remain38 for A and36 for D. Consequently the full second lift still satisfies

`rank_Q(K_A,1) <=181+38 =219`,

`rank_Q(K_D,1) <=171+36 =207`.

Thus the canonical index1 envelopes do **not** increase.

But under this lift choice, both e0 and e1 contributions leave zero inherited correction in the next residual.

## Index-2 residue is direct e2 only

The third binary residue now contains only the direct e2 parity component. There is no inherited e0/e1 correction term.

Use the clean corrected interpolated affine-map covers:

- A6 clean run `32160207690`: inside A6 direct rank<=565; outside the forced A6 core the admitted direct upper is189. Hence uniformly
  `a2<=565`.
- D5 clean run `32160149637`: inside D5 direct rank<=179; outside the forced D5 core the admitted direct upper is364. Hence uniformly
  `d2<=364`.

These strictly supersede the previous complete index-2 envelopes746/535 and, a fortiori, the older A-generic / D1022 state.

## Current A/D dyadic envelopes

The exact envelopes through index2 become

A `[3,219,565,2048,...]`,

D `[3,207,364,2048,...]`.

B/C remain

B `[36,812,2048,2048,...]`,

C `[84,972,2048,2048,...]`.

## Dynamic four-leaf recount through k7

With B/C index2 still generic2048, exact convolution gives

- k0 `27,216`;
- k1 `4,793,472`;
- k2 `286,719,696`;
- k3 `6,955,731,216`;
- k4 `79,723,547,424`;
- k5 `535,328,405,616`;
- k6 `2,657,484,843,456`;
- k7 `10,194,932,924,416`.

Therefore

`sum(k0..k7)=13,474,716,992,512`.

Against the generic four-leaf S1 Hilbert budget

`2^44=17,592,186,044,416`,

the exact margin is

`4,117,469,051,904`.

So the dynamic k0..k7 pass is now substantially stronger than the intermediate746/535 corollary.

## Higher-residue consequence

The lift choice is structurally useful beyond the numerical k7 pass: all valuation e0 and e1 sectors are now exhausted exactly by `K0,K1`. They create no inherited correction at index2 or any later residue.

The next residue therefore starts from direct e2 sectors only. This makes persistence of singleton-side affine-template families a meaningful higher-residue target: if exact signed direct-e2 contributions can themselves be lifted within the same template spaces, their higher corrections can likewise be removed.

That stronger persistence statement is **not** claimed here because the current interpolated covers were constructed for the odd mod2 direct-e2 support groups, not yet for every raw signed e2 sector.

Still not admitted: complete k>=8 control, complete leaf Schmidt-rank reduction, lower `W_repr(1)`, arithmetic-work improvement, `alpha<1`, or full-round relevance.
