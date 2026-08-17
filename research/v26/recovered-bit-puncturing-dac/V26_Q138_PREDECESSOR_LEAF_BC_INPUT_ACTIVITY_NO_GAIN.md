# V26 Q1.38 predecessor-leaf B/C input-activity NO-GAIN

## Scope

The clean B/C first dyadic residue theorem gives uniform bounds

`rank_F2((2^121 L_B) mod2)<=1052`,

`rank_F2((2^121 L_C) mod2)<=1160`.

Those bounds are sums of103 odd affine-support rank budgets plus one four-sector signed-support budget16. This note asks whether predecessor-input mutual exclusion can lower either sum, as it did for the A/D second residue.

The answer is no.

## Support-activity conditions

For each of the104 B/C residue objects, eliminate the32 beta variables from its exact affine support consistency system. This leaves an affine condition on the128 fixed predecessor input bits. The object is inactive if that condition fails.

The103 odd affine supports have weights `2^d`, where d is the exact S1/complement support-intersection dimension:

B: `d2:9, d3:63, d4:31`, giving `1036`.

C: `d2:2, d3:60, d4:41`, giving `1144`.

The common support of the four weight122 unique-solution sectors carries the combined signed Boolean term and has uniform rank budget16.

## Exact conjunction

Take the union of every predecessor-input affine equation from all104 activity conditions and solve the resulting GF(2) affine system exactly.

For both B and C this complete conjunction is consistent.

Therefore there exists a fixed128-bit predecessor input mask for which **all**103 odd affine supports and the signed common support are active simultaneously.

Consequently any upper bound obtained only by replacing each active object with its existing independent rank budget has exact worst-case weighted activity

B: `1036+16=1052`,

C: `1144+16=1160`.

Thus input-mask mutual exclusion cannot sharpen the current B/C first-residue bounds.

This is a method-scope NO-GAIN. It does not prove the true B/C first-residue ranks equal1052/1160; linear dependence between simultaneously active matrix contributions may still lower them by a different argument.
