# V26 — Missing Canonical Bytes / Recovery Authority

## Status

This is the active reproducibility blocker for `V26_SINGLE_COLUMN_QR_TRANSFORM_FALSIFIER`.

The mathematical Stage0 result remains admitted:

`PASS_EXACT_SINGLE_COLUMN_SEPARATOR_STAGE0`

The blocker is **not** a mathematical NO-GO. It is missing exact historical runtime provenance.

## Missing canonical artifacts

### Preferred complete artifact

`FDS_V25_TRAIL_ENUMERATION_DAC_SNAPSHOT.zip`

Required SHA-256:

`fd4d1fbf2378b7950430f18f9efb49f2dab875ee1f72bea5a0336c9d1c5180b6`

### Critical core source

`fds_v25_bit_puncturing.py`

Required SHA-256:

`ec81640f87aaaa97ec5805a973a282241e9e2c2b86011530b4db519dec2be130`

### Useful companions if recovered from the same snapshot

- `fds_v25_chacha.py`
- `fds_v25_pnb_orbit.py`
- recovered bit-puncturing / trail-DAC regression tests
- `V25_TRAIL_ENUMERATION_DAC_PROGRESS.md`
- `V25_TRAIL_ENUMERATION_DAC_DECISION.json`
- `certify_v25_trail_enumeration_dac.py`
- `v25_trail_enumeration_dac_cert/summary.json`

## Search completed on 2026-08-16

The current conversation `/mnt/data` mount was recursively scanned, including nested ZIP contents, for both canonical SHA-256 values.

Result:

`0 matches`

The available historical transcript records the canonical hashes, result lineage and continuation instructions, but does not provide a verified byte-identical core file.

## Extended recovery audit — 2026-08-16

A second recovery pass broadened the search and checked historical Git state rather than relying only on the current tree.

- Fresh `main` before this audit was `ebc3756aab31aaa7241d3ed816b6fd801c96222f`.
- Accessible container roots `/mnt`, `/home/oai`, and `/tmp` were scanned directly by SHA-256: 812 files, 130,949,394 bytes hashed.
- Exact snapshot, core, recovered-test and cert-summary hashes all returned `0 hits`.
- Historical commit `2a94d1ea06c6f167b6f2e64ba71ae8bd0a5e9a1e` records that the snapshot had been located and the historical `19/19 PASS` reproduced in that earlier runtime, but direct Git content lookups for `research/v25/bit-puncturing/fds_v25_bit_puncturing.py` and `research/v25/bit-puncturing/recovered-runtime/fds_v25_bit_puncturing.py` at that ref return 404; the recursive commit tree contains authority/result files but not the canonical core blob.
- `archive/raw-import-2026-08-16.zip` is not present as a Git object on current `main`, and a direct lookup at bootstrap-era commit `d8714b83f5ea55318433b7469fc717a77e902ecc` also returns 404.
- `archive/RAW_IMPORT_STATUS.md` is therefore authoritative over the stale wording previously present in `RAW_IMPORT_MANIFEST.json`: the raw ZIP was locally verified but was not committed as a Git object. `RAW_IMPORT_MANIFEST.json` has been corrected to state `archive_git_object: false`.

Conclusion: the exact historical bytes are not recoverable from the currently accessible filesystem or repository objects inspected in this pass. Recovery still requires an old project ZIP/source backup or another durable copy containing the byte-identical canonical artifact.

## Non-negotiable provenance rule

Do **not** silently rewrite or approximately reconstruct `fds_v25_bit_puncturing.py` and label it canonical.

A new implementation may be created only as a separately labelled reimplementation. It cannot satisfy the provenance gate unless its bytes match the canonical SHA-256.

## Recovery procedure

1. Obtain old project ZIPs/backups from prior chats or the user's machine.
2. Run:

   `python scripts/rematerialize_v25_trail_dac.py <candidate-path> --restore`

3. Require exact snapshot SHA and exact core SHA.
4. Restore runtime dependencies.
5. Re-run historical `19/19 PASS` baseline.
6. Only then execute the frozen cap2 all-four-column QR-transform exact regression.
7. cap2 requires exact support, signed coefficients and energy within `1e-12`.
8. cap2 PASS opens packed cap3 measurement under the existing `2 GiB RSS / 1 GiB compact` gates.

## GitHub tracking

Primary blocker issue: `#22 — Restore exact recovered V25 trail-DAC runtime bytes`.

Until this file's recovery checklist is satisfied, no new cap2/cap3 transform measurement is canonical.
