# V25 Full Linear Boundary-Word XOR Nullspace Audit

Frozen Issue #15 exhausts all **65,535 nonzero GF(2) masks** over the 16 internal boundary words for every split/orientation.

Exact equation-span results:
- split1 forward half-independence spaces have rank4 / nullity12 for both orientations;
- splits2–5 forward spaces are already rank16 / nullity0;
- after adding the opposite-half backward equations from the first frozen fresh target `25053`, split1 also reaches rank16 for both orientations.

Thus every one of the ten split/orientation combined spaces has **nullity0**. Stable nonzero mask count = **0**. The other three frozen outputs cannot rescue an intersection already reduced to `{0}`.

Synthetic GF(2) nullspace regression **2/2 PASS**.

Decision: `NO_GO_FULL_LINEAR_XOR_CANCELLATION`. This closes the entire exact linear XOR boundary-projection MITM family under W4_W6, rather than only low-arity masks.

No matching/TOTAL stage, no alpha<1 claim.
