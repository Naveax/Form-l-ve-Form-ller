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

Low23 rows:

`A0..5,B0..5,D0..5,C12..16`.

High/gap21 rows:

`A12..16,B12..16,D12..16,C0..5`.

Certified low rank:

- repeated-D D0..5 rank `2^19`, clean `32041446052`;
- C12..14 carry map rank16/16, hence low merged rank `n=2^22`, clean `32040887484`;
- j2 bits22..31 high bridge rank32/32, preserving all16 D12..15 prefixes, clean `32041617140`.

Useful j2 gap:

- bits1..11 row domain128, exact rank66, kernel62, clean `32042410012`;
- fixed-D16 minimal loop misses the kernel, clean `32042794811`;
- keeping D16=0/1 together after closing C1..5 gives exact local geometry `64,64,intersection63`, universal over shared `q=(v3_12,sigma2_11)`, clean `32043345651`.

With j1 D16 geometry `448,448,intersection424`, each high prefix has rank

`448*(64n)+448*(64n)-424*(63n)=30632*n`.

Sixteen prefixes are direct, so

`rank_center(S1)<=3829*2^29=2,055,678,722,048`.

Clean full rank/tree run `32043410513`.

With predecessor-leaf exponent44:

`dim_factor<=3829*2^73`,

`W_repr(1)<=73+log2(3829)=84.90275194485017...`.

Factor generation matches the same message/storage bound; clean run `32043554316`. Arithmetic work is still not reduced.

## Secondary representation closure

The retained-only j1 sites6..11 carry gap has exact endpoint Gram rank4/4 and is injective.

Clean run `32043801142`.

No reduction below `3829*2^29` from that direct route.

## d=1 arithmetic structure and closed work routes

### Materialization gate

Per high prefix the D16 union decomposes dimensionally as

`26712n common +1960n private0 +1960n private1 =30632n`.

About87.2% of the channel dimension is common between D16 sectors.

But explicit full-factor materialization emits

`3829*2^73 =36,163,882,525,815,743,046,483,968`

scalars, so materialization itself already has exponent84.90275.

Clean run `32044123499`.

### New: low/high star product barrier

For the complete five-QR star, generic predecessor-leaf Hilbert ranks give

- low23 star mode: central `2^22` times leaf `2^23`, hence `<=2^45`;
- high21 star mode: central `490112=3829*2^7` times leaf `2^21`, hence `<=3829*2^28`.

Their Cartesian product is exactly

`2^45 * (3829*2^28)=3829*2^73`.

Therefore separately completing low and high channel bases before joining them reproduces the existing materialization wall exactly. A work improvement must remove channels before that Cartesian joint is formed.

Clean run `32055881609`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_D1_LOW_HIGH_STAR_PRODUCT_BARRIER.md`;
- `scripts/verify_v26_q138_d1_low_high_star_product_barrier.py`.

### New: monotone complement-interleave generic-leaf barrier

Start from the high21 set and monotonically add the84 non-S1 physical rows one at a time, while using only

1. the high central rank extended by raw `x2` per added row, or
2. the exact reduced central topology terminal cut,

plus generic predecessor-leaf Hilbert ranks.

Every such path passes the layer with44 added complement rows.

At that layer the generic four-leaf Hilbert exponent has exact minimum23. Thus the coefficient/raw-extension certificate is at least

`log2(490112)+44+23 =85.90275194485016...`.

A clean binary cut MILP minimizing central topology plus generic leaf cuts over all choices of44 complement physical rows has exact optimum86, matching dual bound86 with zero MIP gap.

Hence this entire monotone/raw-extension/generic-leaf certificate class cannot certify below the current84.90275. This is a method-scope NO-GAIN, not a true-rank or unrestricted-work lower bound.

Clean run `32056604049`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_D1_MONOTONE_COMPLEMENT_INTERLEAVE_NO_GAIN.md`;
- `scripts/verify_v26_q138_d1_monotone_complement_interleave_no_gain.py`.

## Predecessor-leaf status

The reduced exact leaf topology has terminal cut11 on every frozen HT critical partition, so topology alone cannot improve the generic `2^11` single-leaf rank bound. Historical clean run `32010227963`.

The older coefficient full-rank witness workflow `32011941759` is **not authority**: it ended with runner shutdown/exit143 before producing a mathematical result.

A new exploratory single-copy 2048x2048 minor probe (`32054802994`) is also **not authority**: generic greedy contraction predicted a `2^64` intermediate and failed on a32-GiB allocation before any rank result. This is an implementation/path failure, not evidence for low or full leaf rank.

No canonical frozen `outer128` predecessor mask was found in the repository. Therefore source-specific leaf-rank claims remain provenance-gated; only a uniform theorem can currently be admitted.

## Closed / revoked warnings

- repeated-D D0..5 alone: no gain;
- C12..14 alone: no gain;
- block2 D11 one-bit extension: no gain;
- direct shared `v3_12` alone: product bound exact;
- 39-bit natural bridge before C1..5: old center exactly;
- fixed-D16 minimal gap loop: no gain;
- j1 retained gap6..11: rank4/4;
- explicit factor materialization: scoped arithmetic NO-GO;
- separate complete low/high basis Cartesian joint: scoped arithmetic NO-GO;
- monotone raw complement interleaving with generic leaf Hilbert bounds: method-scope NO-GAIN;
- old four-site ranks96/208 and W84/W83 claims are **revoked** after int32 overflow correction; corrected ranks256/256.

## d>=2 authority — unchanged

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Fully-open exponent63.562242424221076. Semi-open A54.661778097771986, B generic55, C54.92481250360578, D53.74357218893564.

Current law for every d>=2:

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`.

## First unfinished mathematical pass

1. **d=1 coefficient-specific/uniform leaf-central joint algebra.** Generic leaf Hilbert accounting is now the identified blocker. A successful scalar evaluator must exploit actual predecessor-leaf coefficients together with the central common/private D16 blocks before a complete low/high Cartesian basis is formed.
2. **Uniform predecessor-leaf 11|21 coefficient rank.** The topological bound11 is tight as a cut, but coefficient saturation is unresolved. Do not use the failed 32-GiB probe. Seek a small exact streaming/sparse/full-rank certificate or a direct algebraic channel proof. Source-specific work requires the missing/frozen outer128 mask.
3. **Other nonlocal center regroupings.** Additional simultaneous retained-coordinate couplings may still beat `3829*2^29`; direct j1 gap is closed.
4. **Semi-open B<55** and **fully-open S3<63.562** remain separate d>=2 exact rank problems.
5. Clean-checkout every finite claim before authority changes.

All admitted reductions are exact, `epsilon=0`. Approximation remains inactive while exact routes remain open.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round cryptanalytic relevance.
