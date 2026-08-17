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

All44 physical S1 row bits are occurrence-closed. No raw S1 bit remains.

Low23 rows:

`A0..5,B0..5,D0..5,C12..16`.

High/gap21 rows:

`A12..16,B12..16,D12..16,C0..5`.

### Low block

- repeated-D D0..5 rank `2^19`; clean run `32041446052`;
- C12..14 carry map exact rank16/16, hence low merged rank `n=2^22`; clean run `32040887484`;
- j2 bits22..31 bridge exact rank32/32 on `(sigma2_21,D12..15)`; all16 high prefixes remain direct; clean run `32041617140`.

### Useful gap overlap

The j2 bits1..11 gap has row domain `(C1..5,sigma2_0,sigma2_11)`, dimension128, exact rank66 and kernel dimension62. Exact four-state paired-carry Gram DP implicitly sums all `2^28` retained columns. Clean run `32042410012`.

At fixed D16 the smallest physical loop misses this kernel; clean run `32042794811`.

Keeping both D16 sectors together after closing C1..5 gives physical local geometry

`64,64,intersection63`.

The same63-dimensional sector relation holds in every fixed shared slice

`q=(v3_12,sigma2_11)`.

Therefore for any incoming W on q, `dim W=n`, the lifted local geometry is exactly

`64n,64n,intersection63n`.

Clean run `32043345651`.

### Full S1 rank

Extended-block2 j1 D16 geometry remains

`448,448,intersection424`.

Per D12..15 prefix:

`448*(64n)+448*(64n)-424*(63n)=30632*n`.

Sixteen prefixes are direct, so

`rank_center(S1)<=16*30632*2^22=3829*2^29`.

Clean full rank/tree run `32043410513`.

With predecessor-leaf exponent44:

`dim_factor<=3829*2^73`,

`W_repr(1)<=73+log2(3829)=84.90275194485017...`.

Exact improvement over the old85.4178525 bound:

`log2(5472/3829)=0.5151005700357...` bits.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_BIT0_GAP1_11_SECTOR_RANK65.md`;
- `research/v26/recovered-bit-puncturing-dac/V26_Q138_FULL_S1_GAP_RANK3829_THEOREM.md`;
- `scripts/verify_v26_q138_bit0_gap1_11_sector_rank65.py`;
- `scripts/verify_v26_q138_full_s1_gap_rank3829.py`.

## Factor-generation constructivity

Streaming exact Gaussian can select actual physical row basis elements with pivot storage at most `R^2`, `R=3829*2^29`, exponent81.8055. The physical-to-rank transform has at most `2^44*R=3829*2^73` entries. The clean21-site complement entry tree remains peak80.

Thus

`W_factor-gen<=84.90275194485017...`.

Clean run `32043554316`.

Authority:

- `V26_Q138_FACTOR_GENERATION_RANK3829_THEOREM.md`;
- `scripts/verify_v26_q138_factor_generation_rank3829.py`.

This is message/storage constructivity, not arithmetic-work reduction.

## Secondary exact representation closure

The retained-only j1 carry gap at sites6..11 has endpoint row domain `(sigma1_5,sigma1_11)`, dimension4. Exact six-site paired-carry Gram rank is

`4/4`.

Thus the direct j1 retained carry gap is injective and gives no reduction below `3829*2^29`.

Clean run `32043801142`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_J1_GAP6_11_INJECTIVE.md`;
- `scripts/verify_v26_q138_j1_gap6_11_injective.py`.

## Arithmetic-work gate

Per high prefix the new D16 union has exact dimensional decomposition

`26712n + 1960n + 1960n =30632n`.

The `26712n` block is common to both D16 sectors; about87.2% of the union channels are shared.

However any method that explicitly emits the complete coefficient-aware rank factor must write

`3829*2^73 = 36,163,882,525,815,743,046,483,968`

scalars. Thus explicit materialization has a scalar-output work lower bound with exponent84.90275 and is scoped NO-GO as the route to an arithmetic-work win.

Clean run `32044123499`: success.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_D1_ARITHMETIC_MATERIALIZATION_GATE.md`;
- `scripts/verify_v26_q138_d1_arithmetic_materialization_gate.py`.

A useful evaluator must contract on the fly and preserve the common/private D16 decomposition instead of flattening to one materialized factor.

## Revoked / closed warnings

- repeated-D D0..5 alone: no gain;
- C12..14 alone: no gain;
- D11 one-bit block2 extension: no gain;
- direct shared `v3_12` alone: product bound exact;
- 39-bit natural bridge before C1..5: old center exactly;
- fixed-D16 minimal gap loop: no gain;
- j1 retained gap6..11: rank4/4, no gain;
- old four-site ranks96/208 and W84/W83 claims are **revoked** after int32 overflow correction; corrected ranks256/256.

Do not revive revoked results without an independent derivation.

## First unfinished mathematical pass

1. **d=1 scalar arithmetic evaluator.** Do not materialize `3829*2^73`. Preserve the exact per-prefix decomposition `common 26712n + private0 1960n + private1 1960n`, and push predecessor-leaf contraction inside those blocks. Count multiply/add, factor generation, recomputation, memory traffic and final output.
2. **Predecessor-leaf Schmidt structure.** Current generic S1 accounting pays rank `2^11` per 32-bit predecessor leaf, hence `2^44` across four leaves. Compute exact 11|21 Schmidt ranks for the relevant leaf family. A uniform reduction is the most direct current route to lower scalar work. Coefficient-specific claims require a frozen outer128 mask or a uniform theorem.
3. **Other nonlocal representation regroupings.** The direct j1 carry gap is closed, but additional shared retained-coordinate couplings may still lower center `3829*2^29`.
4. **Semi-open B<55** and **fully-open S3<63.562** remain separate d>=2 rank problems.
5. Recount every complete tree and clean-checkout every finite claim before authority changes.

All admitted reductions are exact, `epsilon=0`. Approximation remains inactive while exact routes remain open.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round cryptanalytic relevance.
