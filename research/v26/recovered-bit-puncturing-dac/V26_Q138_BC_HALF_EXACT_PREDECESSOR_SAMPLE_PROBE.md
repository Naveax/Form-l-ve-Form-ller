# V26 Q1.38 B/C exact half correction across predecessor samples

## Scope

The current exact half-sector right21 probe proves, at the explicit max-overlap predecessor witnesses, exact second-bit GF(2) half spans of 128 for B and 136 for C. That result is not yet uniform over predecessor inputs.

This diagnostic samples the affine predecessor solution space on which the common four half-sector support is reachable. For each position B/C it chooses four deterministic half-active predecessors: the current max-overlap witness, one affine particular solution, and low-index nullspace flips when distinct.

At every sample it reuses the already-validated exact right21 evaluator unchanged. Thus each run traverses all 2^21 right-beta assignments and jointly tracks the common support syndrome, the four cross frequencies, and the four right-only scalar phase bits before evaluating the exact second-bit Boolean correction.

## Interpretation

If all sampled exact half ranks equal the current 128/136 witness ranks, that is evidence for predecessor-gauge invariance and motivates a proof of uniformity. It is not itself a proof.

If ranks vary, the sample immediately falsifies simple invariance and identifies concrete predecessor classes for worst-case analysis.

No sampled result replaces the admitted uniform B/C second-lift bounds 812/972 without a separate uniform theorem.
