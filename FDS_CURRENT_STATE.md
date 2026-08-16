# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

All previously killed/inapplicable V25/V26 families remain closed and `ALPHA_PASS` remains 0.

The recovered bit-puncturing/D&C Stage0 remains admitted as `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`. Its bounded-family cap4 single-column result is unchanged and remains distinct from the full-exact Walsh line below.

The active work while historical measured-runtime provenance is blocked is mathematics-first exact Walsh tensor-network analysis. Code is only a calculator/falsifier.

## Exact q138 one-QR structural chain

For the q138 fixed-output exact one-quarter-round Walsh object, the complete certified dense-message upper-bound chain remains

`44 -> 42 -> 41 -> 40`.

- `44`: natural fused-site path;
- `42`: optimal fused-site carving tree;
- `41`: exact minimal-TT-core refinement;
- `40`: exact q138 rank-528 separator compression plus a complete 536-leaf / 535-internal-node contraction tree.

Width-40 authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_ALGEBRAIC_WIDTH40_CERTIFICATE.json`
- `scripts/verify_v26_qr_q138_algebraic_width40.py`

`W<=40` is an exact message-dimension upper bound for this q138 fixed-output one-QR representation. It is not an optimality theorem, arithmetic-work bound, arbitrary-mask result, double-round result or practical-memory claim.

## Width-40 bottleneck algebra

The unique `2^40` maximum cluster contains 171 leaves and splits `64|107` through six binary interface bits. Its 40 parent-external bits partition `16|24`.

### Uniform left map

The 64-leaf map

`L_64 : 2^16 -> 2^6`

has exact rational rank

`rank(L_64)=48`

for all 64 combinations of its six relevant fixed T1/T2 input-mask bits, up to affine internal state relabelings.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_WIDTH40_LEFT_CHILD_RANK48_THEOREM.md`
- `scripts/verify_v26_qr_q138_width40_left_rank48.py`

Thus the raw six-bit interface admits a uniform exact algebraic compression `64 -> 48` on the left child.

### Right map is mask conditioned

The opposite 107-leaf map

`R : 2^6 -> 2^24`

does not have one mask-independent exact rank. Exact fixed-mask examples include

- `rank(R)=34`, parent rank `23`;
- `rank(R)=19`, parent rank `8`;
- `rank(R)=37`, parent rank `26`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_RIGHT_MAP_RANK_CONDITIONING_FALSIFIER.md`
- `scripts/verify_v26_qr_q138_right_map_rank_conditioning.py`

Therefore zero-gauge or single-sample ranks must not be universalized. The next compression layer is intrinsically source/input-mask conditioned.

## Five-site right-map transfer theorem

The 107-leaf right map has an exact five-site factorization over sites `3,4,5,6,7` with tensor counts

`18,21,21,21,26`.

Across every interior prefix cut, exactly five binary sigma/carry indices survive:

`sig4_i, sig4_{i+8}, sig3_i, sig2_i, sig1_i`.

Hence the one-copy hidden state has dimension `2^5=32`, and the doubled Gram transfer state has formal dimension `2^10=1024`.

Interior sites 4,5,6 share one exact family of eight transfer operators indexed by

`tau=(u1,u2,p) in {0,1}^3`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_RIGHT_MAP_TRANSFER_CHAIN_THEOREM.md`
- `scripts/verify_v26_qr_q138_right_map_transfer_chain.py`

## Exact reachable-hull compression: `1024 -> 197`

The ambient eight doubled interior operators are not generically low rank. In tau order

`000,001,010,011,100,101,110,111`,

their exact rational ambient ranks are

`1016,575,384,397,454,537,431,315`.

The compression instead comes from boundary-conditioned reachability.

Taking every site-3 control type and all four interface-pair sectors gives an exact initial span of dimension `28`. Closing monotonically under all eight interior operators gives

`28 -> 150 -> 193 -> 197 -> 197`.

Therefore the formal 1024-dimensional doubled Gram state has an exact common invariant reachable hull

`U`, `dim U = 197`.

The eight transfer ranks restricted to U are

`194,126,89,94,112,122,100,80`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_RIGHT_MAP_REACHABLE_HULL197_THEOREM.md`
- `scripts/verify_v26_qr_q138_right_map_reachable_hull197.py`

## Canonical quotient blocks: `197 = 138 + 59`

Exchange of the two Gram copies commutes exactly with every doubled transfer. The reachable hull decomposes into

- symmetric sector `U_+`, dimension `138`;
- antisymmetric sector `U_-`, dimension `59`.

Reachable sector growth is

`(20,8) -> (107,43) -> (135,58) -> (138,59) -> (138,59)`.

The exact block ranks are:

- symmetric: `136,89,63,66,80,87,68,56`;
- antisymmetric: `58,37,26,28,32,35,32,24`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_RIGHT_MAP_QUOTIENT_BLOCKS197_THEOREM.md`
- `scripts/verify_v26_qr_q138_right_map_quotient_blocks197.py`

This is now the sharp exact right-map state representation. Do not return to the 1024-state ambient Gram transfer unless validating the quotient.

## Current sharp mathematical bottleneck

The next pass is **quotient boundary closure and rank-envelope classification**.

Work in this order:

1. choose exact rational bases for the `138` and `59` copy-swap sectors;
2. materialize the eight interior quotient transfer blocks in those bases;
3. express the site-3 boundary map in the same quotient coordinates;
4. contract/project the site-7 boundary/closure map into the quotient;
5. compute the exact right-map and parent-rank envelope over the five-site control sequences by quotient dynamic programming rather than full 107-leaf recontraction;
6. derive any further simultaneous invariant sectors or quotient-state collapse exposed by the transfer products;
7. restrict the final rank law to the genuinely q138 source-conditioned/reachable fixed-mask family;
8. only after that reinsert conditioned rank factors globally and require a complete machine-verifiable tree/work certificate before claiming `W<=39` or another work reduction.

A natural rank-48 reinsertion geometry previously failed to close one residual subproblem below 39. This remains only a scoped geometry result, not a lower bound or NO-GO.

Only after exact quotient/rank structure stalls should certified epsilon-rank/tail approximation become active.

## Measured-execution blocker

The frozen historical project-cap QR measurement remains blocked by the missing exact recovered V25 runtime bytes.

Canonical blocker authority:

- `research/v26/recovered-bit-puncturing-dac/V26_MISSING_CANONICAL_BYTES.md`
- GitHub Issue #22

Required identities:

- snapshot SHA-256 `fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`
- core SHA-256 `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

This remains a provenance blocker, not a mathematical NO-GO.

After byte recovery: SHA-locked rematerialization -> prove exact historical cap semantics -> historical `19/19 PASS` -> frozen cap2 all-column QR regression -> only PASS opens cap3 under the existing resource gates.

Still not admitted: practical exact QR evaluation, exact end-to-end arithmetic-work reduction, full second-layer contraction, four-inverse-round exact energy, ranking reduction, `alpha<1`, or full-round relevance.
