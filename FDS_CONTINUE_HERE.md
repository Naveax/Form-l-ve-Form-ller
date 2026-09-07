# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**d=1 exact representation:** `W_repr(1)<=73+log2(3829)=84.90275194485017...`.  
**d=1 coefficient-aware factor generation:** same `84.90275194485017...`.  
**d=1 coefficient-blind static:** `95`.  
**d>=2:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**ALPHA_PASS=0**.

All admitted reductions are exact (`epsilon=0`). Code is calculator/falsifier/certificate machinery; finite computational claims require clean-checkout execution.

## Center authority — unchanged

`S1={0,1,2,3,4,5,12,13,14,15,16}`; all44 S1 physical bits are occurrence-closed.

`rank_center(S1)<=3829*2^29`.

D16 per-high-prefix decomposition:

`26712n common +1960n private0 +1960n private1`, `n=2^22`.

No arithmetic-work reduction is admitted.

## Current predecessor-leaf dyadic envelopes

Natural four-leaf scale: `2^426`.

A `[1,41,564,1761,2048,...]`

B `[36,812,2048,2048,...]`

C `[84,972,2048,2048,...]`

D `[1,20,173,838,1958,2048,...]`

The older A/D chains `[3,219,565,...]` and `[3,207,364,...]` remain valid historical bounds but are superseded.

## A/D universal carry-offset exact-signed lifts

Clean run `34109587357` is current low-layer authority.

The always-present carry equations give a selected-side affine map `beta_keep=Lx+Hz+c`. Sectors sharing a carry offset share one selected matrix row/column, so the exact signed aggregate over one offset class has rational rank at most1. Using the exact signed aggregate is a valid binary lift and removes that valuation family from later residuals.

Certified prefixes:

- A `[1,41,564,2048,2048]`;
- D `[1,20,173,838,1958]`.

For A e2, the clean global raw-e2 interpolated singleton-template cover564 improves the generic carry-offset count763.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_AD_UNIVERSAL_CARRY_OFFSET_EXACT_SIGNED_LIFTS.md`;
- `scripts/verify_v26_q138_ad_universal_carry_offset_exact_signed_lifts.py`;
- clean run `34109587357`.

## A direct e3 — now subgeneric

Clean run `34109587313` proves the direct valuation-e3 A signed aggregate satisfies

`rank_Q(K_A,3^direct)<=1761<2048`.

The four enlarged regime row-set sizes are `1168,1206,1206,151`. Their joint relative predecessor-shift map has GF(2) rank4, so only16 relative shift states occur. Exact union sizes are `{1742:8,1761:8}`. Omitted external consistency can only shrink support.

Because A e0/e1/e2 are exact-signed lifts with zero inherited correction, this is a valid index3 lift. Canonical A is therefore

`[1,41,564,1761,2048,...]`.

This closes the A-side subgeneric condition for the current k9 search, but does **not** pass k9 by itself. The theorem notes that under the equal-rank idealization the remaining B/C index2 condition would still require roughly `b2=c2<=31`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_PREDECESSOR_LEAF_A_DIRECT_E3_ROW_UNION1761.md`;
- `scripts/verify_v26_q138_predecessor_leaf_a_direct_e3_row_union1761.py`;
- clean run `34109587313`.

## Certified dynamic product gate — k8 pass, currently non-sharp

Clean run `34109587357` used A index3=2048 and certified:

- k0 `3,024`
- k1 `287,664`
- k2 `12,038,592`
- k3 `292,005,472`
- k4 `4,586,351,280`
- k5 `49,716,263,696`
- k6 `387,621,863,744`
- k7 `2,230,860,887,520`
- k8 `9,647,756,379,008`

Hence

`sum(k0..k8)=12,320,846,080,000 <2^44=17,592,186,044,416`,

with certified margin

`5,271,339,964,416`.

This remains a valid exact k8 pass, but it is now non-sharp because A e3 was subsequently improved to1761. Do not promote sharpened convolution numbers until a clean-checkout assertion records them. K9 and the complete tail remain open.

## B/C status — three simple low-rank routes closed

B/C lower authority remains

B `[36,812,...]`, C `[84,972,...]`.

No improved complete `b2/c2` envelope is admitted.

### Individual sector rank

Clean run `34109587338` proves an individually reachable direct-e1 signed sector has exact rational rank2048 for both B and C. Sectorwise low-rank subadditivity is therefore blocked.

### Identical-support whole-sector cancellation

Clean run `34109587395` groups reachable e1 sectors by identical affine support and compares their restricted complete Gauss phases.

- B:10695 reachable sectors,8952 support groups,1743 duplicate groups; no exact opposite-zero class.
- C:10598 reachable sectors,8876 support groups,1722 duplicate groups; no exact opposite-zero class.

Every duplicate-sector phase class combines to a nonzero odd coefficient. Thus exact whole-sector cancellation among identical affine supports is absent. Partial cancellation across different supports is not covered.

### Complete direct-e1 aggregate rank

- **B:** clean `34107536167` reaches `rank_F3=2048`, hence `rank_Q=2048`.
- **C exact-zero core:** clean `34107785435` proves a12-dimensional 4096-column subcube `U` is exactly zero over Z via primes `3,5,7,11,13` and `|c|<=3043`.
- **C escape:** clean `34109587430` finds the first eight adjacent tested cosets still mod3-zero, then `U+e31` drives accumulated rank to `rank_F3=2048`; hence complete C `rank_Q=2048`.

A preceding sampled-column run `34109587325` saw C rank0 and B rank1536 on the first4096 sampled columns; those were lower bounds only and are superseded by the later complete-rank witnesses.

Therefore useful B/C progress must exploit a more structured higher-residue lift or genuinely nonlocal/product cancellation. Uniform subgeneric direct-e1 sector rank, identical-support cancellation, and complete-direct-e1 aggregate rank are all dead ends.

## Complete-leaf exact contraction program

The full S1 `2048 x 2048` leaf-minor route remains a numerical falsifier target.

Clean path-only run `34109391867` shows output/column slicing plus opt_einsum memory ceilings can fit explicit intermediate-size caps, but selected paths use high multi-operand arity and astronomical total work. Representative C `2^28/2^30` plans use `b_open=2`,512 blocks, max step arity11, estimated total work about `7.85e45`.

The older `leaf-s1-memory-bounded-paths` workflow also only applies memory limits to the full-output network. It performs no internal index slicing and does not require binary contraction, so it does not solve this execution problem.

Immediate execution-design target:

1. preserve the admitted exact factor network and output block slicing;
2. slice selected **internal** binary indices exactly and account for every `2^k` assignment;
3. require `max_step_arity=2` throughout;
4. report peak intermediate and total work including output blocks and internal slices;
5. only if the plan is practical, execute modulo251 with reduction after every pairwise contraction and explicit int64 accumulation safety/chunking.

A dedicated branch `probe-leaf-s1-internal-sliced-binary-path` has been prepared for this path-only diagnostic; it is distinct from the older memory-limit workflows. No numerical leaf-rank claim follows until an actual exact contraction is executed.

## Sharp blockers

1. **B/C index2/index3:** find a representation surviving the exact direct-e1 rank/cancellation obstructions above.
2. **Dynamic k9 and complete tail:** first certify the sharpened convolution with A e3=1761, then attack the remaining B/C-heavy k9 term.
3. **Product-level cancellation:** any useful complete-leaf theorem must exploit structure beyond separate B/C direct-e1 aggregate ranks.
4. **Practical exact contraction:** obtain a binary internal-slicing plan with controlled peak memory and total work.
5. **Arithmetic work:** only after complete leaf control, fuse with central `common+private+private` geometry and count scalar work.

Still not admitted: lower complete `W_repr(1)`, arithmetic-work improvement, ranking/search gain, `alpha<1`, or full-round relevance.
