# V26 q138 Exact Double-Round Path-450 Theorem

## Purpose

The one-QR q138 line has a sharp source-conditioned internal message-width certificate below 39, but that internal U47 separator is not the complete 128-bit Walsh boundary required to compose another ChaCha layer.

This note therefore constructs a **separate, fully open-boundary exact topology theorem** for one q138 inverse double round. It is intentionally coarse but valid without pretending that U47 is the whole inter-round state.

## 1. Active QR count for q138

A ChaCha double round consists of four column QRs and four diagonal QRs.

For the fixed q138 output mask (state word 4, bit 10), only the column QR containing word 4 has a nonzero output mask. The other three column-Qr output masks are all zero and, because a QR is a bijection, their exact Walsh input masks remain zero.

Backward through the one active column QR, its four input word masks lie on words

`0,4,8,12`.

Those four words belong to four distinct diagonal QRs:

- word 0 -> diagonal `(0,5,10,15)`;
- word 4 -> diagonal `(3,4,9,14)`;
- word 8 -> diagonal `(2,7,8,13)`;
- word 12 -> diagonal `(1,6,11,12)`.

Hence the exact q138 inverse-double-round dependency cone contains at most

**5 active quarter rounds**:

one column QR plus four diagonal QRs.

## 2. Open-boundary QR network

Use the unreduced exact Walsh factor graph of one ChaCha QR, leaving any inter-layer word-mask legs open rather than replacing them by constants.

Each QR contains

- four modular additions;
- therefore four binary carry/sigma chains along the bit direction;
- four XOR/rotation wire families with offsets `16,12,8,7` modulo 32.

Every modular-addition bit tensor is exact and may be represented by the established local TT/MPO core. No trail enumeration or sigma cap is introduced.

## 3. Prefix-cut bound for one open QR

Group all factor variables with the same natural bit position into a bit site and consider a contiguous bit-prefix cut.

For a periodic binary wire family with offset `r`, the number of crossing bonds is at most

`2*min(r,32-r)`.

Thus one fully open QR contributes at most

- four carry/sigma bonds: `4`;
- rotation 16: `32`;
- rotation 12: `24`;
- rotation 8: `16`;
- rotation 7: `14`.

Total:

`4+32+24+16+14 = 90`

binary crossing bonds.

This 90 bound is deliberately more conservative than the fixed-IO 44 theorem. The latter absorbs boundary relations that are no longer allowed when an inter-layer mask word is left open.

## 4. Compose the five active QRs

Build the q138 double-round network from the one active column QR and the four diagonal QRs.

Identify the four 32-bit intermediate word-mask legs exactly according to the ChaCha column/diagonal intersection wiring. Those identifications are equality constraints at the physical mask boundary. They introduce no new modular-addition state and no approximation.

For a common bit-prefix cut, the union of the five QR frontiers therefore has at most

`5*90 = 450`

binary bonds.

Hence a complete sequential bit-site contraction exists with structural message dimension

`D <= 2^450`.

Define the coarse full-boundary two-layer exponent

`W_2_topo <= 450`.

This is a rigorous topology-only upper bound, not a claim that `2^450` memory is useful.

## 5. Why this does not contradict the one-QR 38.754... result

The sharp one-QR result

`W_1 <= 38.754887502...`

uses source-conditioned internal rank/support compression after fixing a particular one-QR coefficient family.

The present `450` theorem leaves the actual inter-layer Walsh mask words available for composition. It therefore solves a different and strictly larger boundary problem.

Comparing `38.754...` and `450` as if they were two measurements of the same separator would be invalid. The important fact is that an exact complete double-round generative network now exists, while the remaining research problem is to compress its huge open-boundary separators algebraically.

## 6. Coarse finite-depth law

For `d` ChaCha double rounds, the q138 backward dependency cone contains at most

`8d-3`

active QRs: one active QR in the last column layer and at most four active QRs in each of the preceding `2d-1` half-round layers.

Using the same open-QR bound independently gives

`W_topo(d) <= 90*(8d-3) = 720d-270`.

This is a rigorous coarse linear-in-depth structural upper bound for the bit-prefix frontier of a fixed q138 coefficient family. It is not a sharp rank law and not an attack exponent.

## 7. Representation size versus contraction width

The local generative representation remains linear in word size and active QR count. For one double round there are

`5 * 4 * 32 = 640`

modular-addition bit tensors, each with constant exact local bond dimension.

Thus the representation itself is small while the naive open-boundary contraction frontier is enormous. This separation is exactly the phenomenon the FDS program must exploit: compact local generation does not automatically imply cheap global contraction.

## 8. Next exact target

Do not attack `2^450` by dense materialization.

The next exact pass is:

1. expose the four 32-bit intermediate word-mask interfaces of the five-QR star;
2. derive MPS/TT transfer spaces for each single-word diagonal output kernel and for the central four-word input kernel;
3. compute exact separator/common-span ranks before multiplying them;
4. use the already proved U47, 119-state coefficient quotient and rank-12 support sector only where they are valid internal compressions;
5. require a complete global two-layer certificate before replacing the coarse 450 bound by a sharper `W2`.

## 9. Claims not admitted

This theorem does not establish a practical two-layer contraction, a sharp `W2`, arithmetic-work reduction, ranking gain, `alpha<1`, or full-round relevance. It establishes the correct complete open-boundary two-layer topology and a rigorous finite structural upper bound.