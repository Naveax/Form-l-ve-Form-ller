# V26 Single-Key Rotational Applicability Audit

Frozen Issue #20 assumption audit completed before any statistical benchmark.

Primary ChaCha rotational analysis studies word-wise rotational pairs at the permutation input. The canonical FDS source instead fixes ChaCha's asymmetric constants, uses one unknown fixed key, fixed nonce and only sequential counter variation, and observes block output `P_R(S)+S`.

Exact r=1..31 audit:
- rotations preserving all four fixed constants: `[]`;
- rotations satisfying a generic arbitrary same-key direct relation: `[]`;
- rotations with a public/generic same-key RX difference: `[]`;
- direct applicable rotations: `[]`;
- some rotations do have source counter pairs, so counter availability alone is not the blocker;
- raw permutation oracle is unavailable.

Regression: 3/3 PASS.

Decision: `NOT_APPLICABLE_TO_FDS_SINGLE_KEY_SOURCE_MODEL`. Do not fabricate a rotational bias benchmark from incompatible inputs. No Stage1 opens.
