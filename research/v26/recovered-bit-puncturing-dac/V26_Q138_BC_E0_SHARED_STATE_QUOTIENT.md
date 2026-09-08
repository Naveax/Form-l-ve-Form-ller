# V26 Q1.38 B/C grouped-e0 shared-state quotient diagnostic

## Authority

This note continues the PR110 shared-state rank diagnostic without enumerating the full `2^149` predecessor/right state.

Clean pull-request run:

- workflow: `B-C e0 shared-state quotient diagnostic`;
- run: `34192321862`;
- job: `101952727895`;
- result: `PASS V26_Q138_BC_E0_SHARED_STATE_QUOTIENT`.

The probe reconstructs the same grouped-e0 sectors and support groups as PR110 and splits the packed linear signature into two disjoint semantic channels:

1. support-syndrome deltas;
2. sector left-frequency deltas.

All ranks are exact over `GF(2)`.

## Exact result

The shared domain has

`128 predecessor + 21 right-beta = 149`

binary coordinates.

### B

- raw grouped-e0 sectors: `581`;
- support groups: `251`;
- support signature width: `2508` bits;
- frequency signature width: `6391` bits;
- support-channel rank: `149`;
- frequency-channel rank: `149`;
- combined rank: `149`;
- `dim ker(support)=0`;
- `dim ker(frequency)=0`;
- frequency residual after fixing support: `0` dimensions;
- support residual after fixing frequency: `0` dimensions.

Thus both semantic channels are individually injective on the full shared state.

### C

- raw grouped-e0 sectors: `577`;
- support groups: `250`;
- support signature width: `2498` bits;
- frequency signature width: `6347` bits;
- support-channel rank: `149`;
- frequency-channel rank: `147`;
- combined rank: `149`;
- `dim ker(support)=0`;
- `dim ker(frequency)=2`;
- frequency residual after fixing support: `0` dimensions;
- support residual after fixing frequency: `2` dimensions.

Thus the support channel is already injective. Frequency alone forgets exactly two shared-state dimensions, but conditioning on support cannot leave a smaller frequency state because support has zero kernel.

## Linear-algebra interpretation

Let

`V = GF(2)^149`,

`A : V -> support signatures`,

`B : V -> left-frequency signatures`.

PR110 proves

`rank(A,B)=149`.

The new diagnostic gives

- B position: `rank(A)=rank(B)=149`;
- C position: `rank(A)=149`, `rank(B)=147`.

For any two linear maps,

`rank(A,B)-rank(A) = rank(B restricted to ker A)`.

Because `rank(A)=149` for both positions,

`ker A = {0}`

and therefore

`rank(B restricted to ker A)=0`.

So the proposed support-conditioned residual enumeration does **not** reduce the exact state dimension. The zero residual is not a compression win: the support signature itself already uniquely labels all `2^149` states.

For C only, `dim ker B=2`, hence support contributes exactly two dimensions not visible in the frequency channel.

## Decision

The coarse lossless linear-quotient route is closed as a practical state-reduction mechanism:

`NO_LINEAR_QUOTIENT_GAIN_SUPPORT_CHANNEL_ALREADY_INJECTIVE`.

Do not replace the `2^149` direct enumeration by an equally large support-signature enumeration under a different name. Renaming the state is not compression, however emotionally satisfying it may be.

## Next surviving mathematical route

The remaining structure is not a global linear quotient. It must exploit one of the following without materializing the full state:

1. **local-group factorization**: each support group observes only its own small linear projection; study exact local ranks and overlap/separator dimensions between groups;
2. **algebraic-degree factorization**: prove the grouped-e0 carry observable depends on the shared state through a low-degree ANF or another exact low-complexity polynomial representation;
3. a combination of the two, contracting local low-degree factors over a separator tree.

The immediate next probe should therefore measure per-group joint ranks and inter-group row-space overlap / incremental separator ranks. A useful result must be a factorization or contraction bound, not another global 149-bit relabeling.

## Claim discipline

Not included:

- quadratic scalar phase feasibility;
- grouped-e0 own carry rank;
- e0-half cross-carry;
- support-only lift carry;
- complete `B2/C2`;
- complete leaf Schmidt rank;
- `W_repr`;
- arithmetic-work reduction;
- `alpha < 1`;
- ranking/search gain;
- full-round security claim.

`ALPHA_PASS=0` remains unchanged.
