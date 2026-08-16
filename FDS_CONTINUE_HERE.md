# FDS_CONTINUE_HERE

**Admitted state:** recovered bit-puncturing/D&C Stage0 `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.  
**Frozen measured milestone:** `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes are missing.  
**Active work while blocked:** mathematics-first exact Walsh tensor-network / source-conditioned quotient analysis.

Code is only a calculator/falsifier. The mathematical object is the signed Walsh tensor and its exact low-state / low-rank contraction structure.

## Current exact q138 chain

For the q138 fixed-output one-quarter-round exact Walsh object, the complete global dense-message upper-bound chain is

`44 -> 42 -> 41 -> 40`.

The width-40 maximum cluster splits `64|107` through six binary bits.

Left child:

`rank(L_64)=48`

uniformly over all 64 relevant fixed-u combinations.

Right child:

- rank is input-mask conditioned;
- do not universalize any one fixed-mask example.

The 107-leaf right child has now been reduced to an exact five-site transfer problem.

## Current right-map quotient

Read in this order:

1. `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_RIGHT_MAP_TRANSFER_CHAIN_THEOREM.md`
2. `scripts/verify_v26_qr_q138_right_map_transfer_chain.py`
3. `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_RIGHT_MAP_REACHABLE_HULL197_THEOREM.md`
4. `scripts/verify_v26_qr_q138_right_map_reachable_hull197.py`
5. `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_RIGHT_MAP_QUOTIENT_BLOCKS197_THEOREM.md`
6. `scripts/verify_v26_qr_q138_right_map_quotient_blocks197.py`

Exact facts:

- sites `3,4,5,6,7` contain `18,21,21,21,26` tensor leaves;
- every interior site cut carries exactly five binary sigma/carry bits;
- one-copy hidden state dimension = `32`;
- formal doubled Gram state dimension = `1024`;
- eight interior transfer operators are indexed by `tau=(u1,u2,p)`;
- their ambient exact ranks are `1016,575,384,397,454,537,431,315`;
- site-3 boundary span over all controls/interface sectors = `28`;
- cumulative closure under all eight transfers is `28 -> 150 -> 193 -> 197 -> 197`;
- therefore the exact common invariant reachable hull has dimension `197`;
- copy-exchange symmetry splits it as `138 + 59`;
- restricted transfer ranks are `194,126,89,94,112,122,100,80`;
- symmetric block ranks are `136,89,63,66,80,87,68,56`;
- antisymmetric block ranks are `58,37,26,28,32,35,32,24`.

Do not mistake equal exact-length span dimensions for invariance. The exact-length spans at depths two and three both have dimension 166 but are different; their union has dimension 193. The invariant object is the cumulative 197-dimensional hull.

## First unfinished mathematical pass

The next pass is **quotient boundary closure and exact rank envelope**.

Work in this order:

1. choose exact rational bases for the symmetric 138-dimensional and antisymmetric 59-dimensional sectors;
2. materialize the eight exact interior transfer matrices in those quotient coordinates;
3. express the site-3 boundary vectors in the same coordinates;
4. contract the site-7 closing tensor against the quotient basis, including the real boundary controls such as the T2 bit-31 control rather than treating them as bulk tau bits;
5. compute `rho_R(m)` and preferably `rho_parent(m)` over the five-site control sequences by quotient dynamic programming;
6. search for a still smaller common invariant/sector quotient of the block-transfer algebra;
7. identify the fixed-mask family actually reachable/relevant to the q138 source-conditioned path and prove a uniform rank envelope or finite exact class decomposition on that family;
8. only then reinsert conditioned rank factors globally and require a complete machine-verifiable tree/work certificate before claiming `W<=39` or another work reduction.

Prefer theorem -> quotient algebra -> finite falsifier. Do not fall back to repeated full 107-leaf contractions or arbitrary 17-bit brute-force enumeration unless used only as an independent check.

## Measured execution remains frozen behind provenance

Canonical blocker authority:

- `research/v26/recovered-bit-puncturing-dac/V26_MISSING_CANONICAL_BYTES.md`
- GitHub Issue #22

Preferred snapshot SHA-256:

`fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`

Core SHA-256:

`ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

When bytes become available:

1. SHA-locked rematerialization;
2. prove exact historical project-cap semantics/normalization/nestedness;
3. reproduce historical `19/19 PASS`;
4. run the frozen cap2 all-four-column QR regression;
5. only PASS opens packed cap3 under the existing resource gates.

Still no admitted practical exact QR evaluation, exact end-to-end arithmetic-work reduction, full second-layer solution, ranking gain, `alpha<1`, or full-round relevance.
