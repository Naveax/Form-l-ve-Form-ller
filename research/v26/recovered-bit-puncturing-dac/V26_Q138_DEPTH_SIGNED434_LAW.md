# V26 q138 Signed Multi-Double-Round Representation Law

## Result

For fixed outer input masks, the current exact structural representation bounds are

- one inverse double round:

`W_repr(1) <= 79 + log2(87) = 85.44294349584872...`;

- for `d>=2` inverse double rounds:

`W_repr(d) <= 520*d - 352 + log2(434)`.

The latter supersedes the previous common-tree law `520*d-340`.

Numerically:

- d=2: `696.7615512324445...`;
- d=3: `1216.7615512324445...`;
- d=4: `1736.7615512324445...`;
- d=5: `2256.7615512324445...`.

The slope remains520, while the intercept improves by

`12-log2(434) = 3.238448767555...` bits.

## 1. Common-tree maximizing cluster

The frozen improved common bit tree is

`[[[[27,13],[29,[21,4]]],[[28,[12,5]],[11,[20,19]]]],[[[[25,0],[2,[26,1]]],[[9,18],[17,[10,3]]]],[[[22,8],[24,[23,16]]],[[30,[31,6]],[14,[15,7]]]]]]`.

Under the previous generic physical-rank accounting, the unique maximizing bipartition up to complement has smaller side

`S3={4,5,11,12,13,19,20,21,27,28,29}`

of size11.

Its frozen generic caps are

- central fixed-output/open-four-input QR:44;
- each of four semi-open QRs:55;
- each fully-open QR:65;
- each earliest fixed-input vector kernel:44.

Hence the old d>=2 cost at S3 was

`44 + 4*55 + (8d-12)*65 + 4*44 = 520d-340`.

## 2. Occurrence-closed signed S3 block

The S3 central q138 tensor contains a useful exact local block on twelve physical input-mask bits

`A27..29, B27..29, D27..29, C11..13`.

The three D bits occur twice in the central QR and **both occurrences are included**:

- D27..29 occur in j1 bits27..29;
- the same D27..29 occur in j2 bits11..13.

Thus this is an occurrence-closed physical-row block and may be rank-factorized without silently leaving a second copy of a mixed row variable elsewhere.

The q138 fixed j4 output mask is `2^3`, so exact addition MSB conservation gives

`msb(u3)=27`.

Therefore on j1 bits27..29,

- `u3_27=1`;
- `u3_28=u3_29=0`.

For a fixed three-bit D sector, the exact dyadic j1 subnetwork on the six A/B row bits maps to the interface

`(sigma1_29, v3_7, v3_8, v3_9, sigma1_26)`.

Its exact rational rank is

- 30 in six D sectors;
- 22 in two D sectors.

For the same fixed D sector, exact j2 bits11..13 map the three C row bits to

`(sigma2_13, v3_23, v3_24, v3_25, sigma2_10)`

and have exact rank8 in every D sector.

Taking exact Kronecker products within D sectors gives1792 candidate sector basis vectors. Exact rational union elimination over all sectors yields

`rank = 434`.

Thus twelve raw physical row bits, dimension4096, communicate with the remainder through only434 exact signed channels.

## 3. Central S3 rank

The other

`44-12=32`

physical central row bits on S3 are passed trivially.

Therefore

`rank_center(S3) <= 434 * 2^32`.

The complement has the same matricization rank.

This replaces the generic central exponent44 on the maximizing common-tree edge by

`32 + log2(434) = 40.761551232444...`.

## 4. Multi-depth recount

Every node of the frozen common tree is re-evaluated. S3 and its complement remain the maximizing clusters after the signed replacement. The next d=2 competitor is only676.

Hence for every `d>=2`,

`W_repr(d)` is at most

`(32+log2(434)) + 4*55 + (8d-12)*65 + 4*44`.

Simplifying,

`W_repr(d) <= 520d - 352 + log2(434)`.

The exact verifier checks d=2 through9 and all values follow the same affine law.

## 5. Relation to the special d=1 theorem

The d=1 double-round tree uses different critical partitions S1/S2 and a stronger specialized signed theorem:

`W_repr(1) <=79+log2(87)`.

Do not substitute the S3 law into d=1 or the S1/S2 theorem into the d>=2 common tree without explicit cluster analysis.

## 6. What is and is not improved

This theorem improves the exact **representation/message-width** upper bound for all d>=2 in the frozen common-tree construction.

It does not improve the coefficient-independent fully-open QR bound65, so the asymptotic slope remains520. The improvement is an intercept reduction of

`12-log2(434)` bits.

No arithmetic-work, storage, factor-generation, attack-exponent or optimality claim follows automatically.

## 7. Verification

Authority verifier:

`scripts/verify_v26_q138_depth_signed434_law.py`.

It uses exact rational Walsh arithmetic to verify the S3 local rank434 and then recomputes every cluster of the frozen common tree for d=2 through9.
