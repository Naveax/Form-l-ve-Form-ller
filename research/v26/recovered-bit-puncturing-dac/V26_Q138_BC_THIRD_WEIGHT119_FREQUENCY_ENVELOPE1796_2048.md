# V26 Q1.38 B/C third-residue weight119 homogeneous frequency envelope

## Scope

This theorem concerns the five-zero, carry-weight119, internally full-rank support-indicator family that can contribute at direct dyadic exponent e=2 for B/C across the frozen

`S1={0,1,2,3,4,5,12,13,14,15,16}`

11|21 split.

It computes the union of the **homogeneous left Walsh-frequency spaces over every internally full-rank five-zero candidate**. This is a safe support-space envelope: externally inconsistent candidates may enlarge the envelope but can never make the true contribution larger.

Therefore a proper subgeneric envelope gives a valid integer-lift left-factor bound. Conversely, saturation of the candidate envelope only closes this homogeneous-envelope method; it does not prove that the externally reachable support union itself saturates.

## Four-dimensional top-nullspace quotient

The all-one B/C carry system has internal rank124 and a four-dimensional nullspace.

Each zero-carry site contributes two homogeneous restrictions on that nullspace. Exact quotient signatures show:

-95 of the124 sites have zero quotient signature and are inert for internal-rank completion;
-29 sites have nonzero quotient signature.

A five-zero pattern is internally rank128 exactly when the restrictions from its subset of the29 active sites span all four null directions. The remaining zero sites, if any, may be chosen from the95 inert sites.

Enumerating by active core therefore covers every internally full-rank five-zero pattern exactly once without scanning all `C(124,5)` patterns.

The exact number of such full-rank five-zero candidates is

`1,152,040`.

## B envelope

For every full-rank candidate, eliminate the four old null directions and project the residual homogeneous external row space to the11 S1 beta coordinates.

Each individual B candidate left row space has dimension at most8.

The exact union of all candidate left Walsh-frequency spaces has cardinality

`|U_B,119| =1796`.

Hence every externally reachable weight119 full-rank support indicator has its left Walsh factors in the fixed1796-dimensional character space

`W_B,119 = span_Q{chi_u : u in U_B,119}`.

Therefore the complete support-only contribution of this weight119 full-rank family admits an integer lift with left-factor rank at most

`1796`.

This is a genuine subgeneric support-space envelope, with252 of the2048 S1 Walsh frequencies absent even before external-inconsistency pruning.

## C candidate envelope

For C, the same exact candidate enumeration reaches all2048 Walsh frequencies. Under the deterministic enumeration used by the verifier, saturation is first reached after934,476 full-rank candidates. Individual candidate left rank is again at most8.

Thus

`|U_C,119^candidate| =2048`.

This is an exact NO-GAIN result for the homogeneous full-rank-candidate frequency-envelope method on this C weight119 family. It is not a claim that every frequency is realized by an externally reachable C support.

## Interpretation

The B/C third residue is still open. Other direct-e=2 carry classes and inherited corrections from the explicit812/972 second lifts remain to be assembled.

The result gives a new exact structural asymmetry:

- B weight119 full-rank support-only left-factor envelope `<=1796`;
- C candidate homogeneous envelope is generic2048 and must be sharpened by external consistency, predecessor-condition regrouping, sign/correction overlap, or another nonlocal method.

No complete `b2` or `c2` bound, complete leaf Schmidt-rank reduction, complete-factor improvement, or arithmetic-work improvement is claimed.
