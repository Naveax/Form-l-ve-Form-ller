# V26 q138 Semi-Open S3 Pair-Full-Rank Falsifier

## Purpose

The d>=2 common-tree representation contains four semi-open predecessor QRs per depth stack. Their generic common-tree bound on the maximizing 11-site set

`S3={4,5,11,12,13,19,20,21,27,28,29}`

is the physical Hilbert cap

`5*|S3| = 55`,

corresponding to four open input mask words and one open output mask word.

After signed local rank reduced the fully-open QR cap, the natural next question was whether the same local mechanism also reduces this semi-open 55.

This note records a negative exact result for the most natural occurrence-closed local factorization.

## 1. Four semi-open orientations

The central active column uses state words `(0,4,8,12)`. The four preceding ChaCha diagonal QRs are

- `(0,5,10,15)`;
- `(3,4,9,14)`;
- `(2,7,8,13)`;
- `(1,6,11,12)`.

Therefore the four central input words are respectively local output words

`A, B, C, D`

of the four diagonal predecessor QRs.

All four semi-open orientations must therefore be covered; one cannot analyze only a convenient output word and silently generalize it.

## 2. Exact fused site tensor

Use the same fused exact site formula as in the fully-open signed-rank theorem, but keep only one output word open and set the other three output masks to zero.

At site i the local physical inputs are

`Ain_i, Bin_i, Cin_i, Din_i, Din_{i+16}`.

The last two entries are the two occurrences of D-input mask bits in the fused representation. The local output variable is

- `Aout_i` for orientation A;
- `Bout_{i+7}` for orientation B;
- `Cout_i` for orientation C;
- `Dout_i` for orientation D.

All local Walsh amplitudes are exact dyadic values; the implementation scales the site tensor by16 to integral entries.

## 3. Occurrence-closed site pairs

A physical `Din_j` bit occurs at site j and again at site `j-16 mod32`. Therefore a single-site rank factorization that mixes `Din_j` without its second occurrence is not admissible.

Pair sites

`(i,i+16)`, `0<=i<16`.

Within each pair every D-input physical variable has all of its occurrences included. The remaining A/B/C inputs and the one open output bit each occur at only one fused site.

For the S3 matricization, form the exact coefficient matrix of each active pair from its physical S3 row bits to all local/internal and complement-side variables. Instead of expanding the huge pair coefficient matrix explicitly, compute its exact integer Gram matrix from the two site tensors, respecting shared complement-side D bits.

## 4. Full-rank result

For every active pair and every output orientation A/B/C/D, the pair coefficient row rank equals its raw physical row dimension.

Summing the pair log-ranks gives exactly

`55`

for each of the four orientations.

The verifier establishes full rank over an odd prime. Because every pair has at most its raw number of rows, full row rank modulo the prime supplies a nonsingular integer minor and therefore proves the same full row rank over `Q`.

Thus this occurrence-closed `i<->i+16` local-pair factorization gives no exact signed reduction below the generic semi-open physical cap55.

## 5. Scope

This is **not** a global lower bound `rank_semi(S3)>=2^55`.

It only falsifies the natural product of occurrence-closed local D-pairs. A larger multi-pair sector coupling, a different fused representation, or genuinely global signed cancellation could still reduce the true semi-open Schmidt rank.

The result is useful because it prevents reusing the fully-open single-site signed argument in a form that ignores the duplicated D-input occurrences.

## 6. Verification

Authority verifier:

`scripts/verify_v26_q138_semi_open_s3_pair_fullrank.py`.
