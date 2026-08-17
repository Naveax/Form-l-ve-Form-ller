# V26 q138 Exact Double-Round Path-236 Correction

## Statement

The earlier `V26_Q138_EXACT_DOUBLE_ROUND_PATH252_REFINEMENT.md` correctly identified the five-active-QR q138 inverse-double-round star but overcounted the central QR's periodic offset-16 family.

A clean executable frontier count gives the corrected topology-only bound

`W_2_topo <= 236`.

## Active dependency cone

For q138 output word 4, the active final column QR is

`(0,4,8,12)`.

Backward through it, the four intermediate words land in four distinct diagonal QRs and occupy the four local output positions:

- word 0 -> A;
- word 4 -> B;
- word 8 -> C;
- word 12 -> D.

Thus the first inverse double round contains one central column QR plus four diagonal leaf QRs.

## Exact prefix count

For a 32-site cyclic binary wire family of offset `r`, count unique undirected edges crossing the prefix cut. The reduced central fixed-output/open-four-input QR contains

- four sigma path bonds;
- one offset-8 family;
- one offset-12 family;
- one offset-16 family.

At the maximizing half cut:

- sigma: 4;
- offset 8: 16;
- offset 12: 24;
- offset 16: 16.

The offset-16 family is a perfect matching on 32 sites and therefore has only 16 unique undirected edges. The older formula `2*min(16,16)=32` counted both orientations of the same matching edges.

Hence

`W_center_path <= 4+16+24+16 = 60`.

Each diagonal fixed-input/single-output leaf retains the reduced `{1,8,12}` skeleton and has

`W_leaf_path <= 4+16+24 = 44`.

Grouping the central site and four corresponding leaf sites into one bit super-site makes the inter-layer equality wires local. Therefore

`W_2_topo <= 60 + 4*44 = 236`.

The maximum occurs at the 16|16 bit-prefix cut.

## Coarse depth law

Retaining the previous safe `720` frontier-bit increment per additional preceding double round gives

`W_topo(d) <= 236 + 720*(d-1) = 720d - 484`, `d>=1`.

This remains a coarse topology-only law, not a Schmidt-rank recurrence or arithmetic-work exponent.

## Verification

Authority verifier:

`scripts/verify_v26_q138_double_round_path252.py`

(the historical filename is retained, but the executable milestone printed by the corrected script is `V26_Q138_EXACT_DOUBLE_ROUND_PATH236`).

Clean GitHub Actions run `32007903249`, job `95321104877`, passes with

- active column `(0,4,8,12)`;
- diagonal positions `0:A,4:B,8:C,12:D`;
- central maximum 60;
- leaf maximum 44;
- star maximum 236;
- maximizing prefix 16;
- coarse depth law `720d-484`.

## Superseded material

The numerical `252` bound in `V26_Q138_EXACT_DOUBLE_ROUND_PATH252_REFINEMENT.md` is superseded by 236. Its five-QR dependency-cone description remains useful.

Any reference in that older note to the now-revoked rank-12 support selector is also not current authority.

## Scope

This is the correct complete open-boundary bit-prefix topology upper bound for the five-QR q138 inverse-double-round star under the reduced QR skeleton. It does not prove a practical two-layer contraction, algebraic width 236, optimality, arithmetic-work reduction, ranking gain, `alpha<1`, or full-round relevance.
