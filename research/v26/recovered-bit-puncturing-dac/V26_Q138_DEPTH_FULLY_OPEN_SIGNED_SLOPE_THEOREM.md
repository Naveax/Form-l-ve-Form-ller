# V26 q138 Signed Fully-Open Slope Theorem

## Result

For fixed outer input masks, combine the exact S3 central joint-sector rank with three exact signed local rank compressions of the fully-open QR on the same common-tree partition.

The current exact representation bounds are

- one inverse double round:

`W_repr(1) <= 79 + log2(87) = 85.44294349584872...`;

- for every `d>=2`:

`W_repr(d) <= log2(24,663,038,400) + 396 + (8d-12) * log2(189*2^56)`.

Numerically this is the affine law

`W_repr(d) <= 508.4979393937686... * d - 332.22527759611046...`.

Verified values include

- d=2: `684.7706011914267...`;
- d=3: `1193.2685405851953...`;
- d=4: `1701.7664799789638...`;
- d=5: `2210.2644193727324...`.

The previous slope520 is therefore reduced by

`11.5020606062314...`

log2 message bits per additional inverse double round.

## 1. Exact fused fully-open site coordinates

The fully-open QR keeps all eight input/output mask words open. Introduce exact binary fused channels

- `b_i = Bout_{i+7}`;
- `z_i = J4_v[i] xor Dout[i]`;
- `K_i = J3_v[i] xor Bout[i+7]`;

with indices modulo32.

At bit site i, after summing the two purely local internal masks `x=J4_u[i]` and `q=J3_u[i]`, the exact site contribution is

`sum_{x,q}`

`T4(s4,t4, x, z_i xor Dout_i, Cout_i xor b_i)`

`* T3(s3,t3, q, K_i xor b_i, Aout_i xor z_{i+8})`

`* T2(s2,t2, Cin_i, z_{i+8} xor Din_{i+16}, x xor K_{i+12})`

`* T1(s1,t1, Ain_i, K_{i+12} xor Bin_i, q xor Din_i)`.

This exposes exactly the fused channel families used by the common fully-open envelope:

- four longitudinal carry channels;
- offset7 b channels;
- offset8 z channels;
- offset12 K channels.

The offset16 Din interaction is intentionally left on the column/rest side of the local rank calculations below. Keeping the two Din appearances separate is a relaxation relative to any later offset16 fusion and can only increase the tested row rank. Hence the resulting rank upper bounds remain safe for the already-fused representation.

## 2. S3 fully-open cut

The common-tree maximizing bit set is

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Its old fused fully-open cut had 65 binary channels. The crossing-channel distribution includes three useful S3 sites:

### Site 11

Crossing channel tuple

`(t4,t3,t2,t1,K0,K1,z0,b0)`

has raw dimension256.

The exact fused local Walsh matrix, with all remaining site variables treated as the column side, has rational rank

`168`.

### Site 19

Crossing tuple

`(t4,t3,t2,t1,K0,K1,b0)`

has raw dimension128 and exact rational rank

`96`.

The separate offset16 crossing channel at this site is not included in this local compression and remains in the residual binary count.

### Site 27

Crossing tuple

`(t4,t3,t2,t1,K0,K1,z1,b0)`

has raw dimension256 and exact rational rank

`192`.

The three selected crossing-channel sets are disjoint because every cut channel has a unique S3 endpoint.

Thus 23 raw binary crossing channels may be replaced by exact rank channels of dimensions

`168, 96, 192`.

The other42 fused cut channels remain binary.

Therefore

`rank_fully_open(S3) <= 168*96*192*2^42`.

Since

`168*96*192 = 189*2^14`,

this becomes

`rank_fully_open(S3) <= 189*2^56`.

Hence the fully-open S3 exponent is at most

`56 + log2(189) = 63.562242424221076...`,

a gain of

`1.437757575778924...`

bits from the previous fused cap65.

## 3. Exact rank certificates

Each of the three local ranks is certified over the rationals in both directions.

For the lower bound, the certificate supplies an odd-prime nonsingular square minor of the scaled integer site matrix. A nonzero determinant modulo the odd prime implies the corresponding integer/rational determinant is nonzero.

For the upper bound, the certificate supplies exactly `n-r` independent integer left-null relations. Every relation is checked against every column of the exact site matrix. All relation coefficients lie in `{-1,0,1}`; at sites19 and27 all null relations are two-term equalities, while site11 uses two- and four-term relations.

Therefore the exact rational ranks are

- site11:168;
- site19:96;
- site27:192.

Authority certificate:

`research/v26/recovered-bit-puncturing-dac/V26_Q138_FULLY_OPEN_S3_LOCAL_RANK_CERTIFICATE.json`.

Verifier:

`scripts/verify_v26_q138_fully_open_s3_local_signed_rank.py`.

## 4. Common-tree fully-open maximum

In the frozen common tree the old fully-open value65 occurred only on S3 and its complement. The next largest generic fully-open cap is62.

Therefore replacing the S3/complement value65 by

`56+log2(189)=63.562242...`

changes the actual common-tree fully-open maximum to that new value.

The refined minimal-TT hypergraph does not provide this gain: its exact S3 terminal min-cut is86. The improvement is specifically signed coefficient rank inside the fused channel representation.

## 5. Multi-depth recount

The already certified exact central S3 rank is

`rank_center(S3) <= 24,663,038,400`,

with exponent

`34.52163149454245...`.

The four semi-open QR factors retain exponent55 each, and the four earliest fixed-input vector kernels retain exponent44 each.

For `d>=2`, there are `8d-12` fully-open QRs. Thus the S3 message exponent is at most

`log2(24,663,038,400) + 4*55 + (8d-12)*log2(189*2^56) + 4*44`.

Combining the fixed terms gives

`log2(24,663,038,400) + 396 + (8d-12)*log2(189*2^56)`.

Every node of the frozen common tree is re-evaluated; S3 and its complement remain the unique maximizers. Hence this is a complete common-tree representation upper bound for all d>=2.

## 6. Scope

This theorem reduces representation/message growth. It does **not** certify factor-generation work at the same exponent, reduce the existing constructive double-round ledger95, prove arithmetic-work savings, or establish optimality of the true fully-open QR rank.

All arithmetic is exact and `epsilon=0`.
