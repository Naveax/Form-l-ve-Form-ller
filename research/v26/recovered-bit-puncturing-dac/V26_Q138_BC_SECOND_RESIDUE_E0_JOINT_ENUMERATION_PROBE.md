# V26 Q1.38 B/C second-residue e0 joint enumeration probe

## Scope

This is the exact-enumeration follow-up to the clean joint-image rank probe.

At the explicit max-overlap predecessor witnesses, the previous fixed-predecessor construction still treated the reachable left-support syndrome image and the left phase cross-frequency image as independent spans, even though both are driven by the same 21 right-beta bits.

For each reachable e0 affine-support group this probe now:

1. assembles the same-support e0 phase exactly as in the admitted sign-span machinery;
2. fixes the predecessor witness;
3. builds the common linear image `right21 -> (support syndrome, cross frequency)`;
4. enumerates that joint image exactly (the clean rank probe proved max ranks 15 for B and 14 for C);
5. reconstructs the corresponding nonzero left-support mask and left phase vector;
6. inserts only correction vectors associated with a reachable joint pair.

The right-only phase at a fixed right-beta assignment is a scalar bit. This probe deliberately keeps a safe relaxation for it: for each reachable joint pair it spans both the left phase vector and the corresponding support mask. Thus either scalar sign is contained without inventing unreachable support/cross-frequency pairs.

The four half sectors are **not** rederived here. Their already-validated fixed-predecessor specialized span from PR #94 is retained unchanged. The support-only `U120` space also remains global.

## Claim discipline

Any rank printed by this probe is an upper bound only for the two explicit predecessor witnesses. It is not a uniform B/C second-lift theorem and does not replace the canonical uniform bounds `812` and `972`.

A useful result is evidence that exact support/phase coupling removes real span inflation and therefore motivates a later uniform predecessor argument. A non-improvement closes this e0-only coupling relaxation as a useful witness route.

No complete-leaf Schmidt rank, representation, arithmetic-work, alpha, search/ranking, or full-round claim follows.
