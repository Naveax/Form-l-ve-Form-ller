# V26 q138 Semi-Open S3 Signed A/C Rank Theorem

## Scope

This note sharpens the one-output/open-four-input semi-open QR contribution on the frozen common-tree S3 bipartition

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

It is an exact representation/Schmidt-rank upper bound over the rational Walsh tensor. It is not an arithmetic-work or constructive evaluator bound.

The four predecessor diagonal QRs feeding the central column expose local output orientations A, B, C, D respectively. The generic physical Hilbert cap is `2^55` for each orientation.

## Exact fused local tensor

Use the exact fused one-output/open-four-input site tensor, scaled by16 to integral values. Internal channel variables are

`s4,t4,s3,t3,s2,t2,s1,t1,K0,K1,z0,z1`,

with external local variables

`Ain,Bin,Cin,O,d0,d1`.

The modular-addition coefficient is evaluated exactly through the four local addition signs. Scaling by16 changes no rank.

On the EC common-tree cut, the graph boundary has57 binary channels. Four disjoint S3 site blocks contain27 of those channels:

- site4: `t4,t3,t2,t1,K0,K1` (6 raw bits);
- site11: `t4,t3,t2,t1,K0,K1,z0` (7 raw bits);
- site19: `t4,t3,t2,t1,K0,K1,d1` (7 raw bits);
- site27: `t4,t3,t2,t1,K0,K1,z1` (7 raw bits).

The other30 cut channels remain unsqueezed binary channels.

## Exact rational ranks

For output orientation A the four local flattening ranks over Q are

`48,60,96,96`.

For orientation C they are

`48,72,96,96`.

Each rank is certified twice:

1. exact signed-row classes give the rational upper bound. Every nonzero row is exactly equal to plus or minus a representative row, and the number of signed classes equals the claimed rank;
2. reduction modulo the odd prime `1000003` has the same rank, so an integer minor of that size is nonzero modulo the prime and therefore nonzero over Q.

Thus the rational ranks are exact, not numerical estimates.

## Semi-open A bound

The selected27 channels contribute

`48*60*96*96 = 405*2^16`.

Passing the other30 binary channels gives

`rank_A(S3) <= 405*2^46`.

Therefore

`log2 rank_A(S3) <= 46+log2(405) = 54.661778097771986... <55`.

## Semi-open C bound

Similarly,

`48*72*96*96 = 243*2^17`,

so

`rank_C(S3) <= 243*2^47`,

and

`log2 rank_C(S3) <= 47+log2(243) = 54.92481250360578... <55`.

## B and D

No exact signed improvement is claimed here for orientations B or D. Retain the generic caps

`rank_B(S3), rank_D(S3) <= 2^55`.

Hence the product of all four semi-open contributions satisfies

`rank_A rank_B rank_C rank_D <= 98415*2^203`,

with total exponent

`203+log2(98415) = 219.58659060137776...`.

This improves the previous generic semi-open contribution220 by

`0.413409398622235...` bits.

The complementary 21|11 orientation has the same matricization rank, so the same bounds apply to the S3 complement node.

## Authority

- `scripts/verify_v26_q138_semi_open_s3_signed_ac.py`.

The verifier reconstructs the exact scaled site tensors, checks signed-row class counts, checks matching odd-prime ranks, and verifies the resulting integer product identities.

## Limitations

This theorem does not prove the semi-open Schmidt rank is globally optimal, and it does not prove a lower bound55 for B or D. The clean occurrence-closed `i<->i+16` pair test being full rank only falsifies that specific local pair compression route. Larger multi-site/sector coupling remains open.
