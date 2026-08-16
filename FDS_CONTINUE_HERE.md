# FDS_CONTINUE_HERE

**State:** V25 exponent track CLOSED; four V26 exact target-free families closed NO-GO.  
**Active:** `V26_SINGLE_KEY_ROTATIONAL_APPLICABILITY_AUDIT`.

1. Use frozen plan under `research/v26/rotational-applicability/`.
2. This is an applicability/assumption audit first, not a rotational benchmark.
3. Check every nonzero word rotation r=1..31 against fixed constants, arbitrary same-key compatibility, source counter-pair availability, fixed nonce, block-output observability and RX key-difference knowledge.
4. Published permutation rotational relation must be usable without related/rotated keys or chosen rotational states.
5. If essential assumptions are unavailable, close as `NOT_APPLICABLE_TO_FDS_SINGLE_KEY_SOURCE_MODEL` without statistical testing.
6. Only an actual same-key source-observable relation may open a separately frozen Stage1.
7. Any later ALPHA_PASS still requires fresh TOTAL+verification exponent <1.
8. No full-round claim.
