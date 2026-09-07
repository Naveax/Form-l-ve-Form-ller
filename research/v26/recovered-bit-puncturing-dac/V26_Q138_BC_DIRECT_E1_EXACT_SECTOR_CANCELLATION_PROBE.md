# V26 Q1.38 B/C direct-e1 exact whole-sector cancellation probe

## Scope

This probe tests the smallest exact cross-sector cancellation mechanism left open by the signed affine-quadratic sector Schmidt theorem.

For each reachable direct-e1 B/C sector, after Gauss completion its normalized signed matrix is

`M_nu = 1_{A_nu} (-1)^{q_nu}`.

Only sectors with the same affine support `A_nu` can cancel as whole matrices without further decomposition. For each duplicate affine support, the verifier constructs the complete quadratic Boolean phase on all160 external variables, restricts it exactly to that affine support, and canonicalizes the restricted quadratic ANF in deterministic support coordinates.

Two sectors with equal nonconstant restricted phase and opposite restricted constant term are exact negatives and cancel in the integer aggregate. Equal phases with the same sign combine into an integer coefficient.

This is stronger than syntactic ANF duplicate detection because phases are compared after restriction to the common affine support.

## Non-claims

Different affine supports are not combined. Partial cross-support cancellation, the complete signed aggregate Schmidt rank, the complete B/C K1 rank, complete dyadic tail, representation/factor-generation improvements, arithmetic work, alpha and full-round relevance remain open.

Authority is conditional on a clean pull-request run of

`scripts/probe_v26_q138_bc_direct_e1_exact_sector_cancellation.py`.
