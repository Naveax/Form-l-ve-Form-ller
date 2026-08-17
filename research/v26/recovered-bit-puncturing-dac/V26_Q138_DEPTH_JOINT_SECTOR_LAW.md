# V26 q138 Joint-Sector Multi-Double-Round Representation Law

## Result

For fixed outer input masks, the current exact structural representation bounds are

- one inverse double round:

`W_repr(1) <= 79 + log2(87) = 85.44294349584872...`;

- for every `d>=2`:

`W_repr(d) <= 520*d - 384 + log2(24,663,038,400)`.

Numerically,

`log2(24,663,038,400)=34.52163149454245...`,

so the d>=2 law is

`W_repr(d) <= 520*d - 349.47836850545755...`.

In particular,

- d=2: `690.5216314945425...`;
- d=3: `1210.5216314945425...`;
- d=4: `1730.5216314945425...`.

This supersedes both the earlier `520d-340` common-tree law and the intermediate signed434 law.

## 1. Maximizing common-tree cluster

The frozen common tree has unique maximizing bipartition up to complement with smaller side

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

The old generic central physical-rank cap on this 11-site side was `2^44`.

All 44 physical central row bits on S3 can be partitioned into exact occurrence-closed signed blocks.

## 2. First 24 row bits: two crossed 12-bit blocks

Block A uses

`A27..29, B27..29, D27..29, C11..13`

and has exact rational row rank434.

Block B uses the disjoint physical row variables

`A11..13, B11..13, D11..13, C27..29`

and has exact rational row rank1792.

The two blocks share six internal `v3` bits in crossed form:

- `v3_7..9`;
- `v3_23..25`.

Fix those six common sector bits. Exact projection ranks are paired as

- `(16,120)` in36 sectors;
- `(16,75)` in12 sectors;
- `(11,120)` in12 sectors;
- `(11,75)` in4 sectors.

For a fixed sector, the joint row space is contained in the tensor product of the two projected row spaces. Different sectors form a direct-sum coordinate decomposition. Therefore

`rank_AB <= sum_z rank_A(z)*rank_B(z)`

and the exact sector sum is

`36*(16*120)+12*(16*75)+12*(11*120)+4*(11*75) = 102660`.

This replaces the blind product `434*1792=777728`.

## 3. Remaining 20 row bits: two pair blocks plus site19 cross block

The next two disjoint occurrence-closed blocks are the symmetric site-pair couplings

- `(4,5)` with `(20,21)`;
- `(20,21)` with `(4,5)`.

Each block uses eight physical row bits, closes the two D-mask occurrences between j1 and j2, and has exact rational rank192 instead of256.

They share four internal `v3` sector bits:

- `v3_0..1`;
- `v3_16..17`.

The final four S3 row bits are `A19,B19,C19,D19`. Their exact site19/site3 cross-cut subnetwork includes both occurrences of D19 and of the complement-side D3, together with the shared `v3_15` bit. Its exact row rank is12 instead of16.

This site19 block also shares two carry-sector bits with the rank192 pair blocks:

- `sigma1_19`;
- `sigma2_19`.

Condition on the four shared `v3` bits and these two carry bits. The exact projected pair-block ranks are

- first pair block: values28,21,14 with multiplicities16,8,8 over its `(v-sector,sigma2_19)` sectors;
- second pair block: values23,32 with multiplicities16,16 over its `(v-sector,sigma1_19)` sectors;
- site19 cross block: projected ranks `{(0,0):4,(0,1):8,(1,0):4,(1,1):8}` on `(sigma1_19,sigma2_19)`.

The exact six-bit sector sum gives

`rank_CDE <= 240240`.

This is smaller than the blind `192*192*12=442368` and also smaller than the intermediate four-v-sector product bound.

## 4. Central S3 rank

The AB and CDE row-variable groups are disjoint and together cover all 44 physical S3 input-mask bits. Their remaining interface coordinates are disjoint apart from internal variables already handled by the stated sector decompositions, so the product gives a safe exact central matricization bound

`rank_center(S3) <= 102660 * 240240`.

Thus

`rank_center(S3) <= 24,663,038,400`.

Its exponent is

`34.52163149454245...`,

an exact reduction of

`44 - log2(24,663,038,400) = 9.47836850545755...`

bits from the generic physical cap.

The complementary matricization has the same matrix rank bound.

## 5. Multi-depth recount

For the frozen common tree, all non-S3 clusters retain their previous generic caps. S3 and its complement remain the maximizing clusters after the exact signed replacement.

At depth d>=2, the other common-tree terms on S3 are unchanged:

- four semi-open QRs: `4*55`;
- `(8d-12)` fully-open QRs: `(8d-12)*65`;
- four earliest fixed-input vector kernels: `4*44`.

Therefore

`W_repr(d) <= log2(24,663,038,400) + 4*55 + (8d-12)*65 + 4*44`.

Simplifying,

`W_repr(d) <= 520*d - 384 + log2(24,663,038,400)`.

The clean verifier evaluates every cluster for d=2 through9 and confirms this affine law.

## 6. Scope

This is an exact representation/message-width upper bound. No approximation is used.

It does not certify factor-generation/contraction work at the same peak, does not improve the coefficient-independent fully-open QR cap65, and therefore does not change the asymptotic slope520. No arithmetic-work, storage, attack-exponent, optimality or full-round relevance claim is made.

## 7. Verification

Authority verifier:

`scripts/verify_v26_q138_depth_joint_sector_law.py`.

The verifier reconstructs all local dyadic Walsh row spaces using exact rational arithmetic, checks all stated sector projection ranks and joint sums, and recomputes every node of the frozen common tree for d=2 through9.
