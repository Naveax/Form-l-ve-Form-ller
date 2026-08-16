# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

### Admitted infrastructure / observations
- Reduced-model signed-trail / second-layer evaluation pipeline remains the current computational substrate.
- Pair-product HVP and arbitrary-4-word C1 batch evaluation have exact small/reference checks in recovered snapshots.
- Observable score geometry can predict **structural activity**, but that is not the same latent variable as true-key reliability.

### Closed families
- Static pair-gradient / spectral / projected-HVP / DAPS / natural-C2 selector families: `NO-GO`.
- Current P-only xor-256 label-free reliability family: `NO-GO`.
- Synthetic score-shape/C1/public-counter descriptor family: `NO_GO_CURRENT_DESCRIPTOR_FAMILY`.
- Public xor-delta class j=6/7/8/9: `NO_GO_PUBLIC_DELTA_CLASS`.
- Public additive counter-distance class d=1/64/256/512: `NO_GO_PUBLIC_ADDITIVE_DISTANCE`.

### Synthetic reliability audit — recovered canonical result
24 frozen b=10 targets × 16 pairs (384 rows), six target-group folds.
- Ridge tail-strength pooled Spearman: **0.73216**; shuffle p **0.003891**.
- But median top-4 true-key-rank enrichment: **-0.02804**, positive targets **10/24**.
- Direct true-key-rank ridge pooled Spearman: **-0.24693**.
- Active-row logistic top-10 AUC: **0.3158**.
Interpretation: descriptors learn activity, not unknown-key alignment.

### Public xor-delta audit
- Selected-delta mean true-key rank percentile: **0.53546**.
- Median enrichment vs all 16: **+0.01101**.
- Positive targets: **7/12**.
- Median enrichment vs j=8: **+0.00672**.
All preregistered gates failed.

### Public additive-distance audit
Recovered plan was completed without changing its frozen gates. 12/12 targets completed.
- CV-selected mean rank percentile: **0.49379** (gate >=0.55).
- Median enrichment vs all: **-0.02447** (gate >=+0.05).
- Positive enrichment targets: **5/12** (gate >=8).
- Median enrichment vs d=256: **+0.00868** (gate >=+0.02).
- Secondary ridge pooled Spearman: **0.03128**.
Verdict: `NO_GO_PUBLIC_ADDITIVE_DISTANCE`.

### Still not admitted
- True-key pair reliability learnability.
- End-to-end work reduction.
- `alpha < 1`.
- Full-round relevance/break.

## Exact next milestone
`V25_PUBLIC_COUNTER_CARRY_TRANSITION_SIGNATURE_AUDIT`

This next family uses public binary-addition carry-transition signatures of counter pairs, not another scalar distance/delta label or score-shape descriptor. The plan is frozen before oracle results are inspected.
