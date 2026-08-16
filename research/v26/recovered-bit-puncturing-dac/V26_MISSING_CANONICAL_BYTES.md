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
