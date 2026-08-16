# FDS V25 — Synthetic Reliability Learnability Audit

## Verdict

`NO_GO_CURRENT_DESCRIPTOR_FAMILY`

The 24-target supervised audit closes the current label-free descriptor family as a practical pair-reliability predictor. The descriptors strongly predict whether a trail pair is structurally active, but they do not predict whether the true key is highly ranked within an active pair.

## Frozen corpus

- 24 previously unused b=10 synthetic target keys.
- 16 fixed xor-256 orbit pairs per target.
- 384 pair rows total.
- Six frozen target-group CV folds, four unseen targets per fold.
- No complex tree model.
- Ridge alpha=1.0 and logistic C=1.0 were fixed before labels were inspected.
- 256 target-block label-shuffle null replicates.

Inference-available descriptors were: structural zero, pair RMS, robust q99/q75 tail ratio, max MAD-normalized robust z, normalized row entropy, leave-one-out consensus, C1 observable magnitude, public counter class.

Main result: pooled grouped-CV Spearman **0.73216**, but median top-4 true-key-rank enrichment **-0.02804** and only **10/24** positive enrichment targets. Direct true-key-rank ridge pooled Spearman **-0.24693**; active-row logistic top-10 AUC **0.3158**.

Interpretation: activity is learnable; true-key alignment is not. Do not build another selector from this descriptor family.
