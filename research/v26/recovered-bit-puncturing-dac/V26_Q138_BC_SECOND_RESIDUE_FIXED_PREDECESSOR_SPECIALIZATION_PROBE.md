# V26 Q1.38 B/C second residue fixed-predecessor specialization probe

## Motivation

The exact predecessor-reachability probe has rank 77 for B and 75 for C. A clean max-overlap run then found explicit predecessors where pure support-group filtering leaves the full predecessor-uniform sign basis and Walsh quotient unchanged: B remains 348/144/812 and C remains 432/184/972.

Therefore the next possible gain must use more than support reachability. This probe specializes the already validated complete Gauss-corrected quadratic phase at those explicit predecessor witnesses.

## What is specialized exactly

For every reachable e0 signed-correction sector:

- predecessor128 is fixed in the complete 160-variable quadratic phase;
- predecessor/left-beta cross terms become exact left linear terms;
- only the 21 right-beta cross frequencies remain variable;
- support equations are specialized to beta32;
- the exact image of the 21 right-beta variables in the support-syndrome space is enumerated, so only actually reachable left11 support masks are retained;
- sectors sharing one support are assembled before the GF(2) span is taken.

The four half sectors are treated with the same predecessor specialization and reachable support-mask restriction before applying the existing pairwise half-correction span construction.

## Remaining relaxations

This is still a diagnostic, not a uniform theorem. Two deliberate upper-bound relaxations remain:

1. support-syndrome states and phase cross-frequency states are not yet coupled by the common right-beta assignment;
2. right-only phase signs are represented by the usual support-mask generator.

The support-only second-residue space also remains the global U120 space of dimensions 668 for B and 788 for C.

Hence any rank reduction reported here is safe for the explicit predecessor witness, but it is not by itself a uniform B/C second-lift bound.

## Baseline

Current clean authority remains:

- B sign basis 348, Walsh quotient 144, second lift <=812;
- C sign basis 432, Walsh quotient 184, second lift <=972.

No representation, arithmetic-work, alpha, or full-round claim is made by this probe.
