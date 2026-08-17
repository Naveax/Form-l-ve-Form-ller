# V26 q138 depth law with exact semi-open A/C/D ranks

For the frozen common contraction tree and every inverse-double-round depth `d>=2`, retain the exact central S3 joint-sector rank and the exact fully-open S3 signed rank already certified on main. Replace the four generic semi-open exponents by the current exact orientation-specific bounds:

- A: `405*2^46`;
- B: `2^55` (generic cap retained);
- C: `243*2^47`;
- D: `3429*2^42`, from the exact two-site D interval rank1016 and three rank96 entry blocks.

Thus the four-semi product is

`405*243*3429 * 2^(46+55+47+42) = 337,465,035 * 2^190`,

with total exponent

`218.3301627903134...`.

Using

`rank_center(S3)<=24,663,038,400`,

`rank_fully_open(S3)<=189*2^56`,

and the same four earliest-vector exponent contribution176, every complete-tree node is recounted by `scripts/verify_v26_q138_depth_semi_open_signed_acd.py`.

The resulting exact representation-width law is

`W_repr(d) <= log2(24,663,038,400) + log2(337,465,035*2^190) + (8d-12)log2(189*2^56) + 176`,

or numerically

`W_repr(d) <= 508.4979393937686... d - 333.8951148057971...`,  for all `d>=2`.

In particular

- `d=2`: `683.1007639817401...`;
- `d=3`: `1191.5987033755087...`.

The slope is unchanged from the fully-open signed theorem; the new D interval theorem improves only the intercept by `1.25642781106436...` bits relative to the previous A/C-only semi-open theorem.

All reductions are exact, `epsilon=0`. This is representation/message width only; it does not imply a constructive evaluator, arithmetic-work reduction, ranking reduction, alpha<1, or optimality.
