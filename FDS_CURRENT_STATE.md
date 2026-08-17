# FDS_CURRENT_STATE

## Canonical status — 2026-08-17

All previously killed/inapplicable V25/V26 families remain closed and `ALPHA_PASS` remains 0.

The recovered bit-puncturing/D&C Stage0 remains admitted as `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`. Its bounded-family result remains distinct from the full-exact Walsh line below.

The active work while historical measured-runtime provenance is blocked is mathematics-first exact Walsh tensor-network analysis. Code is a calculator/falsifier, not the research object.

## Exact q138 one-QR structural chain

For the full physical fixed-mask family of the q138 fixed-output exact one-quarter-round Walsh object, the complete certified structural message-width chain is now

`44 -> 42 -> 41 -> 40 -> 38.75488750216347...`.

Interpretation:

- `44`: natural fused-site path;
- `42`: optimal fused-site carving tree;
- `41`: exact minimal-TT-core refinement;
- `40`: exact rank-528 separator compression plus a complete global tree;
- `38.754887502...`: full physical-family rank-27 parent compression plus exact left-I9 support-216 factorization and a complete rewritten global tree.

The older conditioned `u2_31=1` certificate at `39.044394119...` remains a valid intermediate result but is superseded as the sharp global bound by the stronger all-mask result below.

## Physical right/parent algebra retained

The certified width-40 bottleneck contains 171 leaves and splits `64|107` through six binary interface bits. Its parent external partition is `16|24`.

The exact 64-leaf left map has rational rank 48 for all 64 physical left fixed-mask choices. Its 48-dimensional row space has only two classes, selected by the shared bit `u2_8`.

The physical 107-leaf right map is an exact five-site transfer chain. Its doubled Gram state has formal dimension 1024, but the sharp physical reachable hull is

`1024 -> 162 = 114 + 48`.

Over all `2^12=4096` physical right-mask cases, exact rational transfer algebra gives

`11 <= rank(R_m) <= 38`.

The full 171-leaf parent flattening satisfies

`5 <= rank(M_m) <= 27`.

More sharply:

- `u2_31=0`: parent rank `16..27`;
- `u2_31=1`: parent rank `5..8`.

Core authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RIGHT_HULL162_THEOREM.md`
- `scripts/verify_v26_qr_q138_physical_right_hull162.py`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_PHYSICAL_RANK_ENVELOPE27_THEOREM.md`
- `scripts/verify_v26_qr_q138_physical_rank_envelope27.py`

## New exact left-I9 support theorem

The previous conditioned `39.044...` maximum was traced to a 230-leaf cluster consisting of a 229-leaf outside child plus the old left parent factor. The interface between those pieces is the nine binary indices

- `v4_8`;
- `v4_9`;
- `v4_10`;
- `sig4_18`;
- `sig3_10`;
- `v3_21`;
- `v3_22`;
- `aux_j2_i10_k2`;
- `sig1_10`.

Call this boundary `I9`.

For every one of the 64 physical left fixed-mask choices, Boolean-semiring projection of the exact minimal-TT nonzero support onto `I9` gives at most

`216`

feasible nine-bit assignments. This is an exact **support upper envelope**: signed cancellation may remove more states, but any assignment absent from this projection is rigorously zero in the coefficient tensor.

The exact support-size distribution is

- 117: 2 masks;
- 120: 2;
- 144: 12;
- 174: 4;
- 177: 2;
- 180: 6;
- 216: 36.

Therefore

`rank_{I9 | rest}(L_m) <= 216`

for every physical left mask.

If the parent Schmidt factor is chosen as `X_m=L_m B_m`, where `B_m` is any mask-conditioned interface basis realizing parent rank `rho_m<=27`, multiplication by `B_m` cannot create an absent `I9` row. Hence the left parent factor also satisfies

`rank_{I9 | (O7,rho_m)}(X_m) <= 216`

uniformly over the entire physical family.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_LEFT_I9_SUPPORT216_THEOREM.md`
- `scripts/verify_v26_qr_q138_left_i9_support216.py`

## Full-family exact global sub-39 certificate

Use the exact parent factorization with a safe uniform Schmidt bond `RP27`, zero-padding smaller ranks. Split the left parent factor further as

`I9 -- RL216 -- (O7,RP27)`.

Start from the already rank-528-compressed global q138 network, remove the certified 171-leaf parent cluster, and insert three factors:

- `XA(I9,RL216)`;
- `XB(RL216,O7,RP27)`;
- `Z27(RP27,right24)`.

A complete deterministic tree rewrite of the previously certified outside topology gives a 368-leaf / 367-internal-node exact structural tree. Every non-root cluster boundary is recomputed in the target hypergraph.

The maximum message dimension is

`D_max = 216 * 2^31 = 463,856,467,968`,

so

`W <= log2(D_max) = 38.75488750216347... < 39`.

The maximizing cluster contains only the two factors `XB` and `Z27`; their `RP27` bond is internal. Its boundary consists of

- 31 binary indices;
- one dimension-216 `RL216` bond.

The next-largest certified message is

`528 * 2^29 = 283,467,841,536`,

with log-width `38.04439411935845...`.

This result applies to **all 4096 physical fixed-input-mask cases**, including both values of `u2_31`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_THEOREM.md`
- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_GENERAL_RANK27_SUPPORT216_GLOBAL_SUB39_CERTIFICATE.json`
- `scripts/verify_v26_qr_q138_general_rank27_support216_global_sub39.py`
- algebraic dependencies above.

## Mask-conditioned support structure

The 64 physical left-mask choices produce only 13 distinct `I9` feasible-support sets.

Across those classes:

- maximum per-mask active coordinates: 216;
- union: 384 of 512 possible `I9` states;
- intersection: 96;
- no strict subset of the six left fixed-mask controls determines exact support-set identity.

Define the exact binary selector matrix

`C(m,i)=1[i is feasible for mask m]`,

of shape `64 x 512`.

Exact rational elimination gives

`rank_Q(C)=12`.

An explicit 12-row / 12-pivot exact factorization is verified, and all reconstruction coefficients lie in `{-1,0,1}`.

Therefore later joint-mask composition has two exact support representations available:

1. a mask-independent coordinate envelope of size 384;
2. a rank-12 generative mask/support selector.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_QR_Q138_SUPPORT_SELECTOR_RANK12_COMPOSITION_BRIDGE.md`
- `scripts/verify_v26_qr_q138_left_i9_support216.py`

## Error / approximation status

The new reduction is exact. Support states that are removed are impossible, so the residual introduced by support pruning is

`epsilon = 0`.

Therefore epsilon-rank/tail approximation is **not activated**. Residual-Gram error budgeting is unnecessary for this branch at present.

The existing epsilon-rank, coherent-tail and local-to-global error theorems remain available if exact algebraic compression later stalls.

## Current sharp mathematical bottleneck

The one-QR fixed-mask representation target has advanced substantially. The next exact problem is composition across a later QR/layer.

The rank-12 selector solves the zero/nonzero support dependence on the six left mask controls, but the exact parent Schmidt basis used in the `rho_m<=27` theorem may still depend on the fixed mask.

The next sharp object is therefore one of the equivalent forms:

- the common span of the mask-conditioned parent Schmidt spaces;
- a finite transfer/sector representation of those spaces;
- or a directly factorized joint coefficient tensor carrying the mask variable without 64 separate Schmidt bases.

Do **not** replace the mask-conditioned rank-27 family by one universal rank-27 basis until such a theorem is proved.

A secondary optimization target remains lowering the one-QR bound below `38.754887502...`; the current maximum is the `XB-Z27` pair and is itself rank-limited through the internal `RP27` bond, so the dense maximum is not necessarily intrinsic. A naive LCA/Steiner placement was tested and was worse; this is only a scoped geometry falsifier, not a lower bound.

## FDS metric status

Relative to the prior dense `2^40` maximum, the new exact maximum is smaller by

`2^40 / (216*2^31) = 512/216 = 64/27 ~= 2.37037037`.

The certified log-width gain is

`log2(64/27) ~= 1.2451124978 bits`.

This is an **exact zero-error representation/message-width gain**.

It is not yet an admitted arithmetic-work exponent reduction. `ALPHA_PASS` remains 0.

Still not admitted: practical exact QR evaluation at the formal maximum, exact end-to-end arithmetic-work reduction, full second-layer contraction, four-inverse-round exact energy, ranking reduction, `alpha<1`, or full-round relevance.

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
