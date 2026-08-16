# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

### Closed families
- Static pair-gradient / spectral / projected-HVP / DAPS / C2 selectors: NO-GO.
- P-only xor-256 reliability: NO-GO.
- Synthetic score-shape/C1/public-counter descriptors: `NO_GO_CURRENT_DESCRIPTOR_FAMILY`.
- Public xor delta j6/j7/j8/j9: `NO_GO_PUBLIC_DELTA_CLASS`.
- Public additive distance d1/d64/d256/d512: `NO_GO_PUBLIC_ADDITIVE_DISTANCE`.
- Public binary-addition carry-transition signature: `NO_GO_PUBLIC_CARRY_SIGNATURE`.

### Carry-transition result
32 public pairs, 12 fresh b=10 targets, three grouped folds. All 6/6 frozen gates failed:
- pooled Spearman **-0.07541**;
- median target Spearman **-0.03423**;
- median top-8 enrichment **-0.03994**;
- positive top-8 targets **5/12**;
- gain vs distance-only **-0.06990**;
- target-block shuffle p **0.78988**.
Distance-only pooled Spearman: **-0.00551**.
Accounting: 349.87 s total target build wall, 29.12 s median, 527.2 MiB max RSS.

### Structural conclusion
Three successive public-static pair geometry families fail robust transfer: xor-delta class, additive-distance class, and carry-transition signature. Do not create another static public counter classifier under a new label.

### Still not admitted
True-key pair reliability learnability; end-to-end work reduction; `alpha<1`; full-round relevance.

## Exact next milestone
`V25_OUTPUT_CONDITIONED_FEEDFORWARD_BORROW_SIGNATURE_AUDIT`

This family is target/output-dependent. It uses observed Z and the complete candidate ensemble to summarize feed-forward subtraction borrow geometry in key word4, while never identifying the true candidate at inference.
