# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**d=1 exact representation:** `W_repr(1)<=73+log2(3829)=84.90275194485017...`.  
**d=1 coefficient-aware factor generation:** same `84.90275194485017...`.  
**d=1 coefficient-blind static:** `95`.  
**d>=2:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**ALPHA_PASS=0**.

All admitted reductions are exact (`epsilon=0`). Code is only calculator/falsifier/certificate machinery.

## Center authority — unchanged

`S1={0,1,2,3,4,5,12,13,14,15,16}`; all44 S1 physical bits are occurrence-closed.

`rank_center(S1)<=3829*2^29`.

The D16 per-high-prefix decomposition remains

`26712n common +1960n private0 +1960n private1`, `n=2^22`.

No arithmetic-work reduction is admitted.

## Current predecessor-leaf dyadic envelopes

Natural four-leaf scale: `2^426`.

A `[3,219,565,2048,...]`

B `[36,812,2048,2048,...]`

C `[84,972,2048,2048,...]`

D `[3,207,364,2048,...]`

The A/D index2 values are complete uniform dyadic-lift envelopes for the current lift choice. B/C index2 and all later2048 entries remain unresolved universal caps.

## New key theorem: exact signed e1 lift

Clean run `32189863746` is authority.

Previous valid accounting used unsigned e1 support indicators in the second lift, leaving inherited index2 correction. That is superseded.

For every reachable e1 sector:

- A: all271 supports have a unique right21 assignment; at most181 sectors are simultaneously active;
- D: all274 supports have a unique left11 assignment; at most171 sectors are simultaneously active.

Therefore every exact signed e1 matrix has rank<=1. Since `-1 == +1 (mod2)`, the exact signed matrix itself is a valid second lift at the same rank cost as the unsigned support indicator.

Together with the already-admitted exact e0 `-q` lift:

`rank(K_A,1)<=181+38=219`,

`rank(K_D,1)<=171+36=207`,

and **all inherited e0/e1 index2 correction is zero**.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_PREDECESSOR_LEAF_AD_EXACT_SIGNED_E1_LIFT_RANK565_364.md`
- `scripts/verify_v26_q138_predecessor_leaf_ad_exact_signed_e1_lift_rank565_364.py`
- clean `32189863746`.

## A/D index2 = direct e2 only

Forced-core theorem remains:

- A global direct maximizers lie in A6; outside A6 direct rank<=189;
- D global direct maximizers lie in D5; outside D5 direct rank<=364.

Corrected interpolated affine-coset covers:

- A6 direct cover565, clean `32160207690`;
- D5 direct cover179, clean `32160149637`.

Therefore

`a2<=565`,

`d2<=364`.

This supersedes D1022, D851/D535, A746/D535, and the old362/171 inherited-correction accounting.

## Dynamic product gate — now passes through k7

Using the current envelopes, exact four-leaf convolution gives

- k0 `27,216`
- k1 `4,793,472`
- k2 `286,719,696`
- k3 `6,955,731,216`
- k4 `79,723,547,424`
- k5 `535,328,405,616`
- k6 `2,657,484,843,456`
- k7 `10,194,932,924,416`

Hence

`sum(k0..k7)=13,474,716,992,512 <2^44=17,592,186,044,416`.

Exact margin:

`4,117,469,051,904`.

This is a genuine dynamic k0..k7 pass. It is **not** a frozen remaining-budget theorem. The complete k>=8 tail is still open, and deeper residue improvements must be dynamically recounted because they also lower earlier convolution layers.

## B/C status

B/C second lifts remain authority:

B `[36,812,...]`, C `[84,972,...]`.

Third residues remain open. Existing scoped facts:

- B direct leading-support envelope<=1796;
- C corresponding homogeneous candidate envelope saturates2048;
- ordinary second-lift support-carry Walsh sumsets saturate2048 for both B/C.

So no complete `b2/c2` claim yet.

## Immediate higher-residue program

The exact signed e1 lift gives the structural simplification we wanted: valuation e0/e1 sectors are exhausted exactly and create no later correction.

The next question is whether valuation e2 can be treated the same way.

### Active raw-e2 global-cover probe

Do **not** reuse A6/D5 outside-core bounds for this step. Those are mod2 odd-residue statements. An exact signed e2 lift contains raw sectors that may cancel mod2 but still exist over the integers.

Current active probe therefore:

1. enumerate every reachable raw e2 sector from the exact direct-e2 generator;
2. verify cut intersection0 / singleton side sector-by-sector;
3. deduplicate condition-map classes;
4. construct a **global** affine singleton-template cover, not merely A6/D5-local;
5. if cover rank is subgeneric, use the exact signed raw-e2 aggregate as `K2`, which is congruent mod2 to the direct e2 residue and would leave zero inherited e2 correction at index3.

This may trade a somewhat larger index2 lift for a much cleaner higher tail; compare dynamically rather than with a frozen k8 budget.

### A/D arbitrary zero-set internal-rank law

A separate theorem is in validation:

For the93 j1..j3 carry sites and specials `{(1,0),(3,0)}`:

- zero sets containing no special have internal rank127/nullity1;
- zero sets containing a special have rank128.

The proof uses the unique top kernel and monotonic row addition, so it covers all `2^93` zero sets without enumeration.

Consequent next-family counts before external pruning:

`C(91,3)=121,485` three-nonspecial nullity-one candidates,

`C(93,4)-C(91,4)=247,065` four-zero-with-special full-rank candidates,

combined `368,550` per position.

Do not naively RREF all368,550 if the structural law is clean; external consistency/template geometry is the real remaining cost.

## Closed/revoked routes

- frozen-tail k7 “necessity” interpretations are revoked;
- pointwise `2^128` affine-coset enumeration is invalid as a practical exact route;
- A/D active-group whole-quotient/FWHT bounds are too coarse;
- D global affine label-hyperplane route is falsified;
- existing-map-only A6 cover1977 is superseded by interpolated565;
- old one-QR support216/rank12 state remains revoked.

## Sharp blockers

1. Global exact-signed raw-e2 template persistence.
2. Higher direct e3/e4 external consistency and singleton-map compression using the internal-rank law, not naive internal solves.
3. Complete dyadic k>=8 tail or a direct complete-leaf Schmidt/Gram theorem.
4. Only after complete leaf control, fuse with central `common+private+private` geometry and count arithmetic work.

Still not admitted: lower complete `W_repr(1)`, arithmetic-work improvement, ranking/search gain, `alpha<1`, or full-round relevance.
