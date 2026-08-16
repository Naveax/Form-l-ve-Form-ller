# FDS_CONTINUE_HERE

**State:** `ADMIT_REDUCED_MODEL_CONSTANT_FACTOR_COMPUTE_WIN`  
**Next:** `REDUCED_KEY_LAYOUT_TRANSFER_FALSIFIER`.

1. Resolve fresh main and read authority.
2. Use the frozen boundary-syndrome engine: split1, word0, width16.
3. Do not retune split/word/width from layout outcomes.
4. Freeze b=10 key-bit layouts and fresh targets before measuring transfer.
5. For every layout, derive candidate-dependent QR groups structurally and cache only truly candidate-independent groups.
6. Compare exact syndrome-screen TOTAL QR and fair direct-word baseline under the same layout; verify true candidate exactly.
7. Measure wall only after exact QR/equivalence passes.
8. If the win disappears when active bits span multiple key words/groups, scope the admitted result to one-word layout; if it transfers, enlarge the claim only to the tested layouts.

Stop: no alpha<1 claim; no full-round claim; no post-hoc layout/width selection.
