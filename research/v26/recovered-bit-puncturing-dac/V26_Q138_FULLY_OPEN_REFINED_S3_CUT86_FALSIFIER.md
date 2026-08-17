# V26 q138 Fully-Open Refined S3 Cut-86 Falsifier

## Statement

The current d>=2 representation law has asymptotic slope520 because the frozen common tree uses a coefficient-independent fully-open QR cap65, eight times per added inverse double round.

A natural hypothesis was that this 65 came from over-fusing each bit site and would fall after replacing every modular-addition bit tensor by exact minimal-TT cores.

For the current common-tree maximizing bit set

`S3={4,5,11,12,13,19,20,21,27,28,29}`,

that hypothesis is falsified for the direct refined construction.

The exact fully-open minimal-TT hypergraph has terminal min-cut

`86`

between the eight physical input/output mask bits on S3 and those on its complement. The optimal cut contains 86 binary indices and no ternary index.

Thus this explicit refinement is much worse than the existing fused fully-open cap65 and cannot reduce the slope520.

This is a scoped topology result, not a lower bound on the true fully-open Walsh Schmidt rank.

## Exact fully-open algebra

Use the four reverse modular-addition correlation tensors with full local Walsh bit tensor

`T(s,t,u,v,w)`

and exact interior TT profile

`[2,3,3,2]`

in order `(u,t,s,v,w)`.

At bit0, the previous-sigma leg is summed and the exact profile is `[2,3,2]`; at bit31 current sigma is fixed to zero and the exact profile is `[2,2,2]`.

Keep all eight physical QR input/output mask words open:

`Ain,Bin,Cin,Din,Aout,Bout,Cout,Dout`.

The exact reverse-mask parity relations used by the refined network are, modulo32,

1. `J4_w[i] xor Cout[i] xor Bout[i+7] = 0`;
2. `J3_w[i] xor Aout[i] xor J4_v[i+8] xor Dout[i+8] = 0`;
3. `J2_v[i] xor J4_v[i+8] xor Dout[i+8] xor Din[i+16] = 0`;
4. `J2_w[i] xor J4_u[i] xor J3_v[i+12] xor Bout[i+19] = 0`;
5. `J1_u[i] xor Ain[i] = 0`;
6. `J1_v[i] xor J3_v[i+12] xor Bin[i] xor Bout[i+19] = 0`;
7. `J1_w[i] xor J3_u[i] xor Din[i] = 0`;
8. `J2_u[i] xor Cin[i] = 0`.

When all external masks are fixed, these reduce, up to fixed XOR relabelings, to the already certified fixed-IO minimal-core scopes: j4 output fixed; j3 output linked to shifted j4-v; j2-u fixed and j2-v linked to shifted j4-v; j1-u fixed with j1-v linked to shifted j3-v; and the remaining j2-w/j4-u/j3-v relation is the explicit parity factor.

## Refined hypergraph

The exact open network contains

- 888 small tensor/parity factors;
- 1268 nontrivial index hyperedges;
- 1024 binary indices;
- 244 ternary TT bonds;
- 256 physical external binary terminals.

Repeated physical/internal mask variables are represented as one COPY hyperedge, so a variable is charged only once when a cut separates any of its incidences. Ternary TT bonds have their true dimension3.

## Terminal min-cut

Fix all eight physical external mask terminals at bit positions in S3 to side1 and all corresponding terminals at complement positions to side0. Internal factor vertices are free.

Solve the exact hyperedge-cut MILP with one binary cut indicator per index and objective

`sum_e log2(dim_e) z_e`.

HiGHS closes the MILP optimally at

`86.0`.

The returned optimal cut contains exactly

`86` binary indices

and no ternary index, so the result does not depend on floating comparison between powers of2 and3.

## Interpretation

The existing fused fully-open common-tree cap65 is therefore not an obvious over-fusion penalty. For S3, eliminating/fusing the exact local algebra is substantially better than simply exposing every minimal-TT core and parity/COPY relation.

Consequently the next slope-reduction target is not another blind refinement of the same network. It must exploit coefficient-specific signed/sector rank inside the fused fully-open representation, or derive a different exact algebraic factorization.

## Verification

Authority verifier:

`scripts/verify_v26_q138_fully_open_refined_s3_cut86.py`.

## Scope

This falsifies only the direct refined-minimal-TT terminal-cut route on S3. It is not a lower bound of65 or86 on the true fully-open QR Schmidt rank, and it makes no arithmetic-work or optimality claim.
