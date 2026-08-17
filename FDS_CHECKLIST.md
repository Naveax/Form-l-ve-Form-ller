# FDS_CHECKLIST

## Preserved
- [x] Prior V25/V26 NO-GO/inapplicable families remain closed.
- [x] Recovered trail core historical `19/19 PASS` authority preserved.
- [x] Separator Stage0 cap2/cap3 exact validation PASS.
- [x] Separator Stage0 cap4 packed memory gates PASS.
- [x] `PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`.
- [x] `ALPHA_PASS=0` preserved; no practical evaluator/work/ranking/full-round claim silently promoted.

## Historical measured-runtime provenance blocker
- [x] Exact missing-artifact authority written: `research/v26/recovered-bit-puncturing-dac/V26_MISSING_CANONICAL_BYTES.md`.
- [x] GitHub Issue #22 opened for canonical runtime restoration.
- [x] Current conversation `/mnt/data`, including nested ZIP contents, SHA-scanned for canonical snapshot/core: `0 matches`.
- [x] Extended `/mnt` + `/home/oai` + `/tmp` SHA scan: 812 files / 130,949,394 bytes; canonical snapshot/core/test/cert: `0 hits`.
- [x] Historical recovery commit `2a94d1e...` tree audited: canonical core is not a Git blob there; direct historical core paths return 404.
- [x] Bootstrap raw archive provenance corrected: locally verified ZIP was not committed as a Git object.
- [x] Recovery helper supports nested exact snapshot recovery and exact SHA-locked `core_only` fallback without claiming complete snapshot/runtime provenance.
- [x] Recovery helper regression: nested snapshot + nested core-only synthetic cases `2 passed`.
- [ ] Recover `FDS_V25_TRAIL_ENUMERATION_DAC_SNAPSHOT.zip` with SHA `fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`, OR exact core bytes from the same lineage.
- [ ] Recover `fds_v25_bit_puncturing.py` with SHA `ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`.
- [ ] Store recovered exact bytes in a durable GitHub-accessible location and update source registry.
- [ ] Re-run historical `19/19` baseline only after exact recovery.
- [ ] Resume frozen measured single-column QR cap2/cap3 gate only after exact recovery.

## Mathematics-first exact Walsh/tensor track
- [x] One-QR exact authority lowered to `W_1<=38.768184324776925...<39` for all4096 fixed-mask cases.
- [x] d=1 coefficient-blind static method certified `W_static,blind=95` and method-optimal inside that representation.
- [x] d=1 signed block1 exact rank16.
- [x] d=1 historical signed block2 exact rank2784.
- [x] Extend block2 with occurrence-closed `A12,B12,D12`; exact rank21888.
- [x] Certify exact cross-sector geometry: j1 `448/448`, union472, intersection424; bit0 `2/2`, union3, intersection1; 16 independent high prefixes.
- [x] Lower d=1 representation and materialized-factor generation to `78+log2(171)=85.4178525148859...`.
- [x] Clean-check block2 D11 one-bit repeated-variable extension: rank remains21888, no gain (`32038491628`).
- [x] Clean-check block1 `C12,C13,C14` contiguous carry extension: rank128=`16*8`, no gain (`32038564342`).
- [x] Clean-check block1 occurrence-closed D1/D2 two-site extension: rank1024=`16*2^6`, no gain (`32033943549`).
- [x] Keep revoked int32-overflow ranks96/208 and derived84/83 bounds permanently non-authoritative.
- [ ] Probe the repeated-D block1 chain one site farther: close D3 in j1 bit3 and j2 bit19 and compare exact rank against naive `16*2^9`.
- [ ] If D3 is full-rank/no-gain, do not blindly continue; switch to the smallest merged block1/block2 multi-site carry/repeated-D factor.
- [ ] Test whether joint block1 x block2 row-space rank is strictly below the current product `16*21888`.
- [ ] Convert any new representation gain into a constructive factor-generation ledger before claiming storage/message improvement.
- [ ] Keep arithmetic-work accounting separate; current materialized factor size already exceeds `5.16e25` scalars.

## d>=2 exact track
- [x] Freeze S3 `{4,5,11,12,13,19,20,21,27,28,29}`.
- [x] Central joint-sector exponent34.52163149454245.
- [x] Fully-open exact rank bound `189*2^56`, exponent63.562242424221076.
- [x] Semi-open A/C/D exact improvements retained; B remains generic55.
- [x] Current depth law `W_repr(d)<=508.4979393937686...d-333.8951148057971...` for d>=2.
- [ ] Find a genuine multi-site overlap for semi-open B below55, respecting rotation7 and offset16 D reuse.
- [ ] Find a genuine multi-site overlap for fully-open below63.562.

## Admission discipline
- [x] Exact reductions use `epsilon=0` authority.
- [x] Code is treated as calculator/falsifier, not the mathematical object.
- [x] Finite admitted claims require clean-checkout/CI verification.
- [ ] No `alpha<1` claim until TOTAL work accounting, ranking, verification, preprocessing and storage all support it.
