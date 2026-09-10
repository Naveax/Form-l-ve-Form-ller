# V26 Q138 C916 e0 first-dyadic width-61 local-signature sufficiency

## Scope

This pass tests a specific promotion of the frozen PR #148 separator state. PR #148 proved a width-61 recursive certificate for the grouped-e0 support/frequency/radical-control linear target. It did not prove that the same per-group refined linear signatures determine the exact integer-valued first-dyadic residual outputs.

For each of the 250 C916 e0 support groups, let `V` be the exact refined GF(2) row space used by the PR #148 certificate. The exact group output factors through that linear signature if and only if it is invariant under every translation in `V^perp`. The probe computes an exact basis of `V^perp` and evaluates translation invariance through exact L2 inner products of the physical affine-supported quadratic representation. A single positive translation-difference norm is an exact counterexample.

## Frozen result

- physical shared dimension: 149
- support groups: 250
- multiplicities: `{1: 103, 2: 57, 4: 90}`
- physical terms: 680
- frozen PR #148 order: `multiplicity_then_refined`
- frozen PR #148 recursive width: 61
- frozen PR #148 depth: 11
- refined-rank histogram: `{12:3, 13:6, 14:8, 15:24, 16:25, 17:38, 18:40, 19:7, 20:14, 21:85}`
- refined-kernel-dimension histogram: `{128:85, 129:14, 130:7, 131:40, 132:38, 133:25, 134:24, 135:8, 136:6, 137:3}`
- factorization status: `{refuted: 250}`
- by multiplicity: m1 `103/103` refuted, m2 `57/57` refuted, m4 `90/90` refuted
- first failure kernel-basis index: `{0:250}`
- kernel directions checked per group before the first counterexample: `{1:250}`
- first-counterexample mechanism: `{all_supports_preserved_phase_only:250}`
- synthetic factorization/translation regression cases: 68

Decision: `ALL_250_GROUP_OUTPUTS_REFUTE_WIDTH61_REFINED_LOCAL_SIGNATURE_SUFFICIENCY`.

Every group already fails on the first deterministic basis direction of `V^perp`. The failure is not caused by moving across the projection support or any post-Gauss affine support. For all 250 groups, every affine support is preserved and only the phase changes. Thus the missing information is genuinely phase information outside the PR #148 refined support/frequency/radical-control row space.

Representative exact witness for group 0:

- multiplicity: 2
- refined rank: 16
- kernel dimension: 133
- translation: `0x00000000000000000000000000000000000004`
- translation Hamming weight: 1
- original norm squared: `713623846352979940529142984724747568191373312`
- translated inner product: `0`
- translation-difference norm squared: `1427247692705959881058285969449495136382746624 > 0`
- mechanism: `all_supports_preserved_phase_only`

A representative singleton, group 1, also fails phase-only with refined rank 21 and kernel dimension 128; its first translation-difference norm squared is `713623846352979940529142984724747568191373312 > 0`.

## Interpretation

This result does **not** invalidate PR #148. Its width-61 certificate remains exact for the target it actually measured. What is refuted is the stronger claim that the same unchanged local linear signatures are sufficient to encode the exact nonlinear first-dyadic integer outputs.

The next rigorous gate is to characterize the minimal linear factorization row space of each exact group output, equivalently the orthogonal complement of its full translation stabilizer. That can quantify how many linear state bits the phase-complete local functions really require before any new separator width is attempted.

No claim is made here about minimal augmented local signatures, exact nonlinear separator width, exact all-250 joint image, support/e1 carry, half cross, complete C2, `W_repr`, arithmetic-work, ranking/search, full-round relevance, or `alpha < 1`.

`ALPHA_PASS=0`
