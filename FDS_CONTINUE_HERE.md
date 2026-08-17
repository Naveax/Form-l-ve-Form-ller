# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**d=1 exact representation:** `W_repr(1)<=73+log2(3829)=84.90275194485017...`.  
**d=1 coefficient-aware materialized-factor generation:** `W_factor-gen<=84.90275194485017...`.  
**d=1 coefficient-blind static method:** `W_static,blind=95`.  
**d>=2 law:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**ALPHA_PASS=0`.

Code is only a calculator/falsifier. Mathematics is the authority; new finite claims require clean-checkout execution.

## d=1 exact center

`S1={0,1,2,3,4,5,12,13,14,15,16}`.

All44 physical S1 row bits are occurrence-closed.

Low23 rows: `A0..5,B0..5,D0..5,C12..16`.  
High/gap21 rows: `A12..16,B12..16,D12..16,C0..5`.

Certified structure:

- repeated-D D0..5 rank `2^19`, clean `32041446052`;
- C12..14 carry map rank16/16, low merged rank `n=2^22`, clean `32040887484`;
- j2 bits22..31 bridge rank32/32, preserving16 high prefixes, clean `32041617140`;
- j2 bits1..11 rank66/128, kernel62, clean `32042410012`;
- fixed-D16 minimal loop misses that kernel, clean `32042794811`;
- combined D16 sector geometry after closing C1..5: `64,64,intersection63`, uniform over `q=(v3_12,sigma2_11)`, clean `32043345651`;
- extended-block2 j1 D16 geometry `448,448,intersection424`.

Per high prefix:

`448*(64n)+448*(64n)-424*(63n)=30632*n`.

Sixteen prefixes are direct:

`rank_center(S1)<=3829*2^29=2,055,678,722,048`.

Clean rank/tree run `32043410513`.

With predecessor-leaf exponent44:

`dim_factor<=3829*2^73`,

`W_repr(1)<=84.90275194485017...`.

Factor generation matches this message/storage bound; clean `32043554316`. Arithmetic work is not reduced.

## d=1 work-route closures

- retained-only j1 gap6..11 rank4/4, clean `32043801142`;
- D16 channel decomposition per prefix:
  `26712n common +1960n private0 +1960n private1`;
- explicit full-factor materialization emits
  `3829*2^73 =36,163,882,525,815,743,046,483,968` scalars, clean gate `32044123499`;
- complete low/high star mode envelopes are `2^45` and `3829*2^28`; their Cartesian product is exactly `3829*2^73`, clean `32055881609`;
- monotone complement interleaving with only raw central extension/topology plus generic leaf Hilbert ranks has an unavoidable 44-added-row layer: coefficient certificate85.90275194485 and exact topology+leaf MILP optimum86, clean `32056604049`.

Thus generic leaf-Hilbert bookkeeping is now a certified method blocker. A work improvement must use actual predecessor-leaf coefficients before forming the full low/high Cartesian joint.

## New predecessor-leaf dyadic structure

The reduced leaf topology still has exact terminal cut11 on the critical HT partitions; topology alone cannot beat generic `2^11`. Historical clean run `32010227963`.

Old coefficient full-rank witness `32011941759` is non-authoritative: runner exit143 before a mathematical result. Exploratory dense single-copy minor `32054802994` is also non-authoritative: greedy contraction predicted a `2^64` intermediate and failed on a32-GiB allocation before rank output.

### Top-carry cancellation

Formal four-addition carry denominator exponent is124. Exact GF(2) carry/sign analysis proves:

- A/D weight124 is impossible;
- B/C weight124 internal matrix rank124/128, nullity4;
- restricted sign polar rank2;
- every affine-fiber Gauss sum is `0,+8,-8`.

Clean `32057838229`.

### Position-dependent dyadic descent

A/D: j4 output expression is identically zero, forcing every j4 carry bit to zero. Formal maximum carry weight becomes93. The unique weight93 internal matrix has rank127, two-point fibers and even signed numerator. Therefore

`L_A(beta),L_D(beta) in 2^-92 Z`.

B/C: exact carry-sector descent gives

- weight123 classes `(rank,nullity,polar)`:
  `(124,4,2):95`, `(125,3,2):14`, `(125,3,0):7`, `(126,2,0):8`;
- weight122 rank distribution:
  `124:4465,125:2058,126:1025,127:74,128:4`;
- only four weight122 rank128 sectors:
  `(j1 bit0,j2 bit0)`, `(j1 bit0,j4 bit0)`, `(j2 bit0,j3 bit0)`, `(j3 bit0,j4 bit0)`;
- those four sectors have one identical rank8 external consistency system for B, and likewise one identical system for C.

Hence

`L_B(beta),L_C(beta) in 2^-121 Z`.

Clean `32058413111`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_PREDECESSOR_LEAF_TOP_CARRY_CANCELLATION.md`;
- `research/v26/recovered-bit-puncturing-dac/V26_Q138_PREDECESSOR_LEAF_DYADIC_DESCENT92_121.md`.

### A/D first 2-adic parity rank

Define integer matrices/vectors

`M_A=2^92 L_A`, `M_D=2^92 L_D`.

Modulo2, only three affine-indicator sectors survive:

- weight92 `(j1 bit0)`;
- weight92 `(j3 bit0)`;
- weight93 two-point fiber with the affine sign-derivative-equals-zero condition.

For each indicator, after exact internal elimination the S1 beta-column image and complement beta-column image have zero intersection. Therefore each indicator has GF(2) communication rank1 and

`rank_F2((2^92 L_A) mod2 across S1)<=3`,

`rank_F2((2^92 L_D) mod2 across S1)<=3`.

Clean `32058931522`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_PREDECESSOR_LEAF_AD_PARITY_RANK3.md`;
- `scripts/verify_v26_q138_predecessor_leaf_ad_parity_rank3.py`.

This does **not** prove rational leaf Schmidt rank<=3. It opens an exact 2-adic lifting route:

`2^92 L = M0 + 2 M1`, with `rank_F2(M0)<=3` for A/D.

## Closed / revoked warnings

- repeated-D D0..5 alone: no gain;
- C12..14 alone: no gain;
- block2 D11 one-bit extension: no gain;
- direct shared `v3_12` alone: product bound exact;
- 39-bit natural bridge before C1..5: old center exactly;
- fixed-D16 minimal gap loop: no gain;
- j1 retained gap6..11: rank4/4;
- materialization, separate full low/high bases, and generic monotone complement interleaving are scoped work NO-GAIN routes;
- old four-site ranks96/208 and W84/W83 claims are revoked after int32 overflow correction.

No canonical frozen `outer128` predecessor mask is currently available; source-specific leaf claims remain provenance-gated.

## d>=2 authority — unchanged

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Fully-open exponent63.562242424221076. Semi-open A54.661778097771986, B generic55, C54.92481250360578, D53.74357218893564.

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`, d>=2.

## First unfinished mathematical pass

1. **A/D 2-adic lift:** determine the next residue rank of `M1=(2^92 L-M0)/2`; if successive residue ranks stay small, build an exact dyadic low-rank leaf representation instead of a dense rational Schmidt matrix.
2. **B/C first parity layer:** use the `2^121` scaling and the finite carry-sector/Gauss decomposition to construct its exact S1 parity-Schmidt object.
3. **Leaf-central joint:** combine any certified dyadic leaf layers with the central D16 common/private decomposition before a full low/high Cartesian basis is formed.
4. Other nonlocal center regroupings, semi-open B<55 and fully-open S3<63.562 remain separate exact routes.
5. Clean-checkout every finite claim before authority changes.

All admitted reductions are exact, `epsilon=0`. Approximation remains inactive while exact routes remain open.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round relevance.
