# V26 q138 signed S1 block2 explicit rank-2784 factor theorem

Scope: the exact d=1 S1 block2 used in the signed85 theorem. This upgrades the previous rank count to an explicit exact local channel factorization. It does not by itself prove a full constructive double-round bound below95.

The natural occurrence-closed decomposition has 16 sectors for `D13..16`. In each sector:

- the j1 bits13..16 row family has exact basis dimension112;
- the j2 bits29..31 contribution is one exact vector determined by the D sector;
- the j2 bit0/C0 row family has exact basis dimension2.

Therefore there are

`16*112*2 = 3584`

natural product channels in a `2^18`-dimensional retained-column space. Exact rational Gaussian elimination gives their span dimension

`2784`.

The verifier `scripts/verify_v26_q138_signed_block2_explicit_factor.py` constructs all3584 sparse exact product vectors, builds a normalized exact rational echelon basis of2784 vectors, computes the coordinate map of every natural product channel, and reconstructs all3584 channels exactly.

Coordinate structure:

- maximum nonzeros in one natural-channel coordinate vector:41;
- mean nonzeros: `2.5398995535714284...`;
- denominator set exactly `{1,2,3,4,6,8,9,12,16,24,32,48,64,96,128,256,512}`;
- maximum absolute numerator37;
- maximum denominator512.

The coefficients are therefore small exact rationals, but they are **not all dyadic**. An earlier draft incorrectly called them dyadic; clean-checkout verification caught and removed that overstatement.

Even a dense storage of the 3584x2784 coordinate transform is below `2^24` scalars. Dense storage of the 2784 basis vectors over `2^18` retained columns is below `2^30` scalars.

Hence the block2 rank2784 reduction is not merely an existential Schmidt-rank statement: it has an explicit finite exact rational coordinate transform and explicit retained-column basis, both far below the current double-round structural peaks.

This removes local block2 factor generation as the constructive<95 blocker. The remaining constructive problem is global: contract/generate the complement/right factor while preserving these signed rank channels without materializing the old coefficient-blind 51-bit central boundary.
