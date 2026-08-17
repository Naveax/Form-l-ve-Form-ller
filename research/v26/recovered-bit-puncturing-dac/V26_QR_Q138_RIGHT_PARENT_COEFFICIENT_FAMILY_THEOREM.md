# V26 q138 Right-Gram / Parent Gram-Image Family Theorem

## Semantic status

This note concerns **Gram/rank-space objects**, not the full right-external coefficient amplitudes needed to compose another QR.

For each physical 12-control case `m`, let `R_m` denote the exact right-child coefficient map from the six parent-interface bits to the 24 right-external bits. Define

`G_m = R_m R_m^T`.

The exact family ranks below are ranks of the `64 x 64` Gram matrices `G_m` and of their images under the common 48-dimensional left interface row space. They preserve right/parent ranks and interface Schmidt spaces, but they do not determine the individual coefficient amplitudes on the 24 right-external bits.

Therefore the 145/124/47 results are valid for rank-space analysis and mask-sector organization, but they must **not** be used as a replacement for the single-copy coefficient tensor when attaching another QR.

## Physical control order

Use

`u1_3,u2_3,u1_4,u2_4,u1_5,u2_5,u1_6,u2_6,u1_7,u2_7,u2_8,u2_31`.

## Exact right-Gram family span

Clean exact rational computation proves

`dim_Q Span{G_m}=145`

over all 4096 physical controls.

The five-site doubled transfer construction factorizes the Gram family into

- an 8-control site3--6 prefix family of exact span 140;
- a 4-control site7 closure family of exact span 16.

The 2240 prefix-basis/closure-basis products span only 145 independent Gram matrices.

Authority:

`scripts/verify_v26_qr_q138_right_bilinear_family_span.py`.

Clean Actions run `32008645947`, job `95323277617`.

## Exact parent Gram-image family

Let `L` be the common exact 48-dimensional left interface row space, represented by a fixed 48x64 basis matrix. For rank-space purposes define

`H_m = L G_m`.

Then

`dim_Q Span{H_m}=124`.

A fixed exact factorization exists

`H_m = sum_{lambda=1}^{124} D(m,lambda) K_lambda`,

where `K_lambda` are fixed rational 48x64 Gram-image matrices.

The row directions of the fixed 124-matrix basis span an exact 47-dimensional subspace of the canonical six-interface-bit coordinate. This is the previously observed common parent **Gram-image/interface rank space**.

It is not a claim that the full coefficient matrices `L R_m` or the complete 16|24 parent tensors lie in a 124-dimensional coefficient-amplitude family.

## Natural mask-TT profile of the Gram-image selector

For the natural 12-control order, the exact prefix-flattening / TT profile of `D(m,lambda)` is

`[2,4,8,16,32,64,128,119,196,136,143,124]`.

The natural-order maximum is 196.

The `4096 x 124` selector has 243,335 nonzero rational entries in the deterministic elimination basis. The fixed kernel from the 124 Gram-image sectors to `48 x U47` has 31,491 nonzero entries.

Authority:

`scripts/verify_v26_qr_q138_mask_coeff124_tt.py`.

Clean Actions run `32006391041`, job `95316690780`.

The script filename retains the historical word `coeff`, but its mathematical object is `H_m=L G_m` and should be read as a Gram-image/rank-space verifier.

## What these results prove

They prove exact finite structure for rank analysis:

- 4096 right Gram matrices -> family span 145;
- 4096 parent Gram-images -> family span 124;
- their interface row directions -> common span 47.

These facts explain the rank envelope and organize mask-conditioned Schmidt spaces without comparing 4096 unrelated bases.

## What they do not prove

They do **not** provide the single-copy coefficient map required by the next QR. In particular, `G_m=R_mR_m^T` forgets the orientation/amplitude information in the 24-dimensional right-external output space. Different `R_m` can have the same Gram matrix.

Hence one may not propagate `D(m,lambda)` through a subsequent QR and call that exact coefficient composition.

The actual next-layer object must retain either

1. the single-copy right map `R_m` with its 24 external mask legs;
2. an exact factorization provably equivalent to `R_m` for composition;
3. or the original tensor network with those legs explicit.

## Relation to the six-left-mask family

The separately verified complete left coefficient family has exact span 64 and natural TT profile

`[2,4,8,16,32,64]`.

Thus support-only or low-linear-rank encoding of the six left controls is unavailable. Any exact next-layer gain must emerge after coupling to the next operator or from nonlinear/sector structure.

## Scope

No approximation is used. This theorem does not prove a full second-layer coefficient representation, arithmetic-work reduction, optimal mask ordering, ranking gain, `alpha<1`, or full-round relevance.
