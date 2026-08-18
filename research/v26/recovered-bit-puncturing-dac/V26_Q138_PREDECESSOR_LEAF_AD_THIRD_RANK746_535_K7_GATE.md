# V26 Q1.38 predecessor-leaf A/D third ranks 746 / 535 and dynamic k0..k7 gate

## Scope

This theorem is an exact corollary of the clean A6/D5 interpolated affine-map cover receipts, the admitted forced-common-core theorem, and the inherited e1 correction geometry under the admitted e0-zero second-lift sign choice.

It sharpens the complete index-2 dyadic envelopes for the A and D predecessor leaves across the frozen

`S1={0,1,2,3,4,5,12,13,14,15,16}`

11|21 split.

It also performs the exact four-leaf dynamic convolution recount through layer k7. It does **not** control the complete k>=8 tail, prove a complete leaf Schmidt-rank reduction, lower the current d=1 representation exponent, or prove an arithmetic-work improvement.

All statements are exact; `epsilon=0`.

## Clean ingredients

### Forced common cores

The admitted forced-core theorem gives:

- A: every global direct-e2 active-count maximizer lies in A6; outside A6 the direct rank is at most189.
- D: every global direct-e2 active-count maximizer lies in D5; outside D5 the direct rank is at most364.

### Interpolated direct-e2 covers

Clean corrected PR-checkout run `32160207690` constructs an A6 affine-coset interpolated right21 template cover of size565. Therefore

`rank_Q(E_A,2(x)) <=565`

for x in A6, and the outside-A6 bound189 is smaller. Hence the uniform direct-A bound is565.

Clean corrected PR-checkout run `32160149637` constructs a D5 affine-coset interpolated left11 template cover of size179. Therefore

`rank_Q(E_D,2(x)) <=179`

for x in D5; outside D5 the admitted direct upper is364.

### A inherited e1 correction: singleton sharpening

The earlier correction theorem bounded A by `2*181=362` because 266 sectors have two possible left rows. This is conservative on the wrong side of the cut.

Clean PR-checkout run `32189193782` verifies for **all271** reachable A e1 correction supports that, after eliminating the11 S1 beta variables, all21 complement beta variables pivot. Thus for every fixed predecessor input for which such a support is active, the support has exactly one right21 assignment.

The inherited correction value `-q` is zero outside that support. Therefore each active A e1 correction sector is supported in a single matrix column and has rational rank at most1, regardless of whether one or two left rows are present and regardless of the quadratic sign values on those rows.

The admitted predecessor-input activity theorem gives at most181 simultaneously active A e1 sectors. Hence

`rank_Q(C_A,2(x)) <=181`.

This strictly supersedes the old362 correction bound.

### D inherited e1 correction inside/outside D5

Clean combined-row run `32159421297` verifies:

-265 of the274 D e1 correction sectors are compatible with D5;
-9 are outside D5;
-every D correction sector has rank at most1;
-the previously admitted global correction bound is171.

For the present corollary no direct/correction overlap is needed. Inside D5, correction rank is at most265 by sector count; outside D5, use the sharper global171 bound.

## Complete A third residue

Inside A6:

`rank(T_A,2) <=565 +181 =746`.

Outside A6:

`rank(T_A,2) <=189 +181 =370`.

Therefore uniformly over all128-bit predecessor inputs,

`a2 <=746 <2048`.

## Complete D third residue

Inside D5:

`rank(T_D,2) <=179 +265 =444`.

Outside D5:

`rank(T_D,2) <=364 +171 =535`.

Therefore uniformly,

`d2 <=535 <2048`.

This supersedes the previous canonical `d2<=1022` bound.

## Current single-leaf dyadic envelopes

The exact envelopes through index2 are now

A `[3,219,746,2048,...]`,

B `[36,812,2048,2048,...]`,

C `[84,972,2048,2048,...]`,

D `[3,207,535,2048,...]`.

B/C index2 remain generic in this theorem.

## Dynamic four-leaf convolution through k7

Let layer k be the subadditive four-sequence convolution coefficient. Exact recount gives

- k0 `27,216`;
- k1 `4,793,472`;
- k2 `289,913,040`;
- k3 `7,291,256,400`;
- k4 `89,132,856,768`;
- k5 `639,130,051,056`;
- k6 `3,234,960,487,008`;
- k7 `12,391,314,882,560`.

Hence

`sum(k0..k7)=16,362,124,267,520`.

The generic four-leaf S1 Hilbert budget is

`2^44=17,592,186,044,416`.

Therefore

`sum(k0..k7) <2^44`

with exact margin

`1,230,061,776,896`.

This is the first admitted dynamic k0..k7 pass in the current dyadic predecessor-leaf program.

## What this does not prove

The complete dyadic tail remains open. In particular, this theorem does not reserve the above margin as a frozen k>=8 budget: improving deeper residues also changes earlier layers, exactly as the old frozen-k7 interpretation taught us at unnecessary computational expense.

The next mathematically relevant target is therefore one of:

1. prove persistence of the A6/D5 affine singleton-template families through several higher dyadic residues and perform a new dynamic recount; or
2. bypass residue-by-residue subadditivity with a direct complete predecessor-leaf Schmidt-rank / Gram / tensor-network theorem.

No change is made here to `W_repr(1)=84.90275194485017...`, `W_factor-gen`, arithmetic-work status, `ALPHA_PASS=0`, or full-round relevance.
