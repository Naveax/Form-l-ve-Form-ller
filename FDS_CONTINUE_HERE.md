# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**d=1 exact representation:** `W_repr(1)<=73+log2(3829)=84.90275194485017...`.  
**d=1 coefficient-aware factor generation:** `W_factor-gen<=84.90275194485017...`.  
**d=1 coefficient-blind static:** `95`.  
**d>=2:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**ALPHA_PASS=0**.

All admitted reductions are exact (`epsilon=0`). Code is only calculator/falsifier/certificate machinery; mathematics is the authority.

## d=1 center — unchanged

`S1={0,1,2,3,4,5,12,13,14,15,16}` and all44 physical S1 bits are occurrence-closed.

`rank_center(S1)<=3829*2^29`, hence

`W_repr(1),W_factor-gen <=73+log2(3829)=84.90275194485017...`.

The D16 channel decomposition per high prefix remains

`26712n common +1960n private0 +1960n private1`, `n=2^22`.

Explicit materialize-then-contract is a scoped work NO-GO. No arithmetic-work win is admitted.

## Current predecessor-leaf dyadic envelopes

Natural four-leaf scale is `2^426`.

Current exact single-leaf envelopes are

A `[3,219,2048,2048,...]`,

B `[36,812,2048,2048,...]`,

C `[84,972,2048,2048,...]`,

D `[3,207,1022,2048,...]`.

The D index-2 value is the first admitted subgeneric third-residue envelope in the current A/D assembled-rank program.

### A/D inherited third correction

Under the admitted same-rank second-lift sign choice, inherited e0 third correction vanishes. The remaining e1 correction satisfies

`A_correction<=362`,

`D_correction<=171`.

### A/D direct e=2 condition groups

Clean rank-one regrouping:

- A:12098 odd direct supports ->4531 predecessor affine conditions, multiplicities `617x1,261x2,3653x3`; one common right21 singleton map per condition group.
- D:12363 ->8629 conditions, multiplicities `4895x1,3734x2`; one common left11 singleton map per group.

Thus fixed-input direct rank is bounded by active groups, but active-group counting is too coarse for sharp rank bounds.

### Forced affine common cores

Exact averaging/counting theorem `V26_Q138_AD_THIRD_DIRECT_E2_FORCED_COMMON_CORE.md` proves:

A:
- every global direct active-count maximizer satisfies the six most frequent affine equations;
- A6 has4067 compatible groups;
- residual condition ranks `{2:3,3:364,4:3700}`;
- exact mean active count `555/2`, hence global max>=278;
- outside A6 direct active-group/rank upper `<=189`.

D:
- every global maximizer satisfies the first five equations;
- D5 has8084 compatible groups;
- residual ranks `{3:12,4:649,5:4129,6:3294}`;
- D6 mean `12327/32`, hence global max>=386;
- outside D5 direct upper `<=364`.

The old `2^128` point-enumeration and large weighted-MILP routes are superseded. The sharp object is singleton-map collision/cover geometry inside A6/D5.

### D direct singleton-map theorem

Clean run `32158688395` constructs a fixed family of global affine left11 maps covering every D5-compatible direct-e2 condition-group map:

-90 zero sites occur in D5;
-90 site representatives collapse to54 maps modulo D5;
-these cover4413/8084 groups;
-deterministic completion adds797 maps;
-final cover size851.

Hence

`rank_Q(E_D,2(x))<=851`

uniformly over every128-bit predecessor input (outside D5 the stronger364 count bound applies).

Combining by subadditivity with the admitted inherited correction171 gives

`d2<=851+171=1022<2048`.

Authority:

- `V26_Q138_PREDECESSOR_LEAF_D_THIRD_RANK1022.md`;
- `scripts/verify_v26_q138_predecessor_leaf_d_third_rank1022.py`.

Dedicated clean verifier PR58 is the provenance follow-up; the851 construction itself already has clean PR-checkout receipt `32158688395`.

### A existing-map cover — scoped NO-GAIN

Clean run `32156922775` on A6:

-88 zero sites;
-62 initial maps modulo A6;
-initial maps cover763/4067 groups;
-deterministic existing-group-map completion needs1915 additional templates;
-cover1977;
-`1977+362` saturates the row cap2048.

So the **existing-map-only** A cover is NO-GAIN for the complete A third residue. This does not rule out interpolated affine-coset templates.

### Active-group Walsh envelopes — scoped NO-GAIN

A6 full residual-dual span rank119; D5 rank121. Whole-quotient FWHT is infeasible.

Coverage-greedy exact20-dimensional FWHT gives only

A active-group upper2568,

D upper4636.

Therefore active-condition counting is too coarse. Do not keep extending this route; exploit singleton-map collisions instead.

## B/C status

Second lifts remain exact authority:

B `[36,812,...]`, C `[84,972,...]`.

Clean B/C third leading-support result:

- B direct-e2 left-Walsh envelope `<=1796`;
- C saturates2048 by weight119, so this homogeneous support-envelope route is NO-GAIN for C.

B1796 is **not** a complete `b2` bound.

Natural second-lift support carry also closes coarsely:

`U120_B xor U120_B = F2^11`,

`U120_C xor U120_C = F2^11`.

Thus the ordinary XOR-vs-integer-sum third-bit support carry has full2048 Walsh frequency envelope for both B and C. Finer sign/sector-aware lifts remain open.

## Correct dynamic product gate

The old frozen-tail k7 comparison is only a conservative sufficient test. It is **not** a necessity statement, because improving `a2,b2,c2,d2` lowers k2..k6 at the same time.

The immediate exact test is

`S_0..7(a2,b2,c2,d2)<=2^44`.

The exact polynomial is

`210 a2 b2 c2 +1056 a2 b2 d2 +399936 a2 b2`

`+848 a2 c2 d2 +257952 a2 c2 +1141248 a2 d2 +3127931904 a2`

`+222 b2 c2 d2 +58908 b2 c2 +412608 b2 d2 +1168937856 b2`

`+268128 c2 d2 +930192576 c2 +3188419584 d2`

`+2858783053824`.

Clean dynamic-recount run `32137271413`.

With B/C generic2048 this reduces to

`S07(a,d)=7,404,880,238,592 +5,356,090,368 a +5,513,702,400 d +5,040,640 ad`.

At current D1022 with A/B/C generic,

`S0..7=34,559,498,960,896 >2^44`.

The current D gain does lower `S0..6` to

`8,270,906,966,016`,

but k7 remains too large.

Useful B/C-generic tradeoffs for **complete** A/D index-2 ranks:

- if `d2=1022`, need `a2<=433`;
- `d2=851` -> `a2<=569`;
- `d2=700` -> `a2<=712`;
- `d2=535` -> `a2<=898`.

Since A inherited correction costs362 by the current subadditive accounting, the corresponding direct-A targets are71,207,350,536.

Even passing `S0..7` is not full-tail control. Generic k8 remains enormous; after any index-2 success, k>=8 or a stronger whole-leaf/product cancellation theorem remains mandatory.

## Closed / revoked search interpretations

- Old frozen-tail statement “B/C reduction is mathematically necessary for k7” is revoked. It was true only for the old frozen sufficient budget.
- Direct j1 gap and simple carry bridges remain closed NO-GAIN.
- B/C support-carry sumset coarse route is full2048 NO-GAIN.
- D global affine label-hyperplane route is falsified by a clean fixed-input witness with47 distinct rows and full affine hull rank11/11.
- A/D active-group FWHT envelope is too coarse; K20 bounds2568/4636.
- Pointwise affine-coset enumeration is invalid as a practical exact method because condition free dimensions are117..120.
- Old support216/rank12 one-QR state remains revoked; current one-QR support peak is218.

## Active exact passes

1. **D complete-third row overlap (PR57):** test all274 inherited e1 correction singleton rows against the direct851 D5 row-template family. Inside-D5 combined row support may be much smaller than `851+171`; outside-D5 coarse combined upper is535.
2. **D interpolated affine-coset cover (PR56, fixed head):** a shared template need not equal an existing group map. Intersect the exact cosets `m_g + span(D5+condition_g)` coordinatewise to construct smaller global left11 templates. The first implementation had a quotient-reduction bug; only the fixed-head clean run is valid.
3. **A interpolated affine-coset cover (PR59, fixed head):** same construction on A6/right21. If D complete rank reaches roughly535, A direct<=536 is enough for the dynamic k0..k7 gate.
4. **D rank1022 clean theorem receipt (PR58):** provenance closure of the dedicated theorem/verifier.
5. If interpolation remains weak, do not return to active-group counting. Next stronger object is joint template-coset clustering / higher-residue persistence, or a direct complete-leaf Schmidt-rank witness/theorem.

## Longer-term exact direction

Residue-by-residue control may not be enough: even a successful index-2 gate leaves generic k8 far above budget. Two serious continuations are:

- prove the same affine singleton-map families persist across higher dyadic residues, compressing several residue layers with one structural theorem; or
- attack the **complete predecessor-leaf Schmidt rank** directly. A single fixed predecessor input with exact rank2048 would falsify any uniform subgeneric full-leaf theorem for that position; conversely a uniform low-rank tensor-network/Gram theorem would bypass the residue tail.

## d>=2 — unchanged

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Fully-open exponent63.562242424221076. Semi-open A54.661778097771986, B generic55, C54.92481250360578, D53.74357218893564.

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`, d>=2.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round relevance.
