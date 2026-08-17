# V26 q138 Central Open-QR Refined Terminal-Cut-44 Falsifier

## Purpose

The double-round HT88 bound has three critical 11|21 partitions. On each, the generic central contribution is 44 by physical input-side dimension. This note tests whether the exact minimal-rank local TT refinement of the central open-input QR lowers that value topologically.

## Exact refined central network

Use the q138 central fixed-output/open-four-input backward mask equations with constants suppressed only as invertible bit relabelings:

- `A0 = u1`;
- `C0 = u2`;
- `T1.w = u3 xor D0`;
- `T1.v = ROR12(v3) xor B0 xor const`;
- `T2.w = u4 xor ROR12(v3) xor const`;
- `T2.v = ROR8(v4) xor ROL16(D0)`;
- `T3.w = ROR8(v4)`;
- `T4.w` is the fixed q138 output-side mask.

Every modular-addition bit tensor is replaced by its exact local TT decomposition:

- fixed-output T4 interior profile `[2,3,2]`;
- generic T1/T2/T3 interior profile `[2,3,3,2]`;
- exact lower-rank boundary cores at bits 0 and 31.

XOR/rotation relations are explicit factors. Ternary TT bonds are conservatively charged as two binary exponent bits, so the resulting cut is a safe exact upper bound.

## Result

For each of the three HT88 maximizing partitions, exact terminal min-cut between the four open physical input-word masks on the two sides is

`44`.

In all three cases the minimum cut consists solely of 44 physical input bits. No ternary TT auxiliary bond is needed in the cut.

Thus

`central refined topology bound = 44`

on every critical partition.

## Interpretation

The minimal local TT core representation does **not** improve the central contribution below the generic physical input-dimension cap on the HT88 bottlenecks.

This closes the route

`HT88 -> refine central local TT topology -> smaller terminal separator`

for those partitions.

It does not prove the actual central tensor Schmidt rank is 44. Coefficient-specific cancellation/algebraic rank deficiency could still lower it. The result says only that refined topology cannot certify such a reduction.

## Verification

Authority:

`scripts/verify_v26_q138_central_open_refined_terminal_cut.py`.

Clean GitHub Actions run `32009323380`, job `95325289419`, passes with refined safe cut exponents `44,44,44`.

## Next implication

To beat the generic-envelope optimum 88, the strongest remaining exact targets are:

1. actual leaf Schmidt ranks below `2^11` on the critical partitions;
2. actual central coefficient rank below `2^44`;
3. joint central/leaf rank structure not visible to independent envelope multiplication.
