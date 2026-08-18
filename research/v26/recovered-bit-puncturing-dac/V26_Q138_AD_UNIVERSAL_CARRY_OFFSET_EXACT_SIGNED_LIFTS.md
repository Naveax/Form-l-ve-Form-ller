# V26 Q1.38 universal A/D carry-offset map and exact-signed valuation lifts

## Scope

Fix the predecessor128 input and the frozen output split

`S1={0,1,2,3,4,5,12,13,14,15,16}`,

`R1={0,...,31}\S1`.

This theorem proves a universal affine formula for the selected singleton side of every A/D carry sector, then uses the carry-offset code to sharpen the exact signed dyadic lifts.

All statements are exact (`epsilon=0`). This is still a predecessor-leaf dyadic theorem, not a complete d=1 representation or arithmetic-work result.

## Universal affine selected-side map

For j1..j3, the bit1..30 three-variable equations and the bit31 equations are present for every carry pattern. Only their RHS depends on the carry-zero indicators. The forced-zero j4 equations are likewise always present.

Eliminate the128 internal variables and the unselected beta variables from this always-present system while keeping the93 j1..j3 zero indicators `z` symbolic. Exact elimination gives

`beta_keep = L x + H z + c`,

where `x` is the128-bit predecessor input, `L` and `c` are fixed, and H depends only on the output position and the frozen side.

For A, `beta_keep` is the right21 assignment. For D it is the left11 assignment.

The selected beta variables all pivot in the always-present system. Therefore every solution of every complete carry-sector system obeys this same formula; additional zero-site equality rows can only restrict existence, not change the selected-side value.

Consequently every reachable signed A/D carry sector is supported on one matrix column (A) or one matrix row (D), and all sectors with the same carry offset `Hz` share that selected label for every fixed predecessor input.

## Exact carry-offset maps

Let the93 zero-site columns of H be indexed by the j1..j3 sites. The two special sites are

`P={(1,0),(3,0)}`.

Exact symbolic elimination gives:

A:

- selected-side dimension21;
- `rank(H_A)=21`;
- both special columns are0;
- among the91 nonspecial sites there are41 distinct offset vectors, including0;
-20 nonspecial site columns are0.

D:

- selected-side dimension11;
- `rank(H_D)=11`;
- both special columns are0;
- among the91 nonspecial sites there are20 distinct offset vectors, including0;
-45 nonspecial site columns are0.

The full H ranks are generic, so no complete-leaf reduction follows merely from `rank(H)`. The useful structure is the exact-weight XOR code induced by the valuation families.

## Direct valuation-e carry families

The admitted A/D zero-set internal-rank law gives a common one-dimensional internal fiber for every all-nonspecial zero set and a unique internal solution whenever a special zero is present.

For an all-nonspecial zero set of size z, the surviving equal-sign two-point fiber contributes magnitude2 at carry weight `93-z`, hence after the natural `2^92` scaling has dyadic valuation z.

For a special-containing zero set of size z, the unique solution contributes magnitude1 at carry weight `93-z`, hence scaled valuation `z-1`.

Therefore direct valuation e consists of:

- e nonspecial zero sites in the nullity-one equal-sign family;
- e+1 zero sites containing at least one special in the full-rank family.

Because the special H columns vanish, the selected-side offset set of the complete candidate valuation-e family is

`O_e = Sigma_e(V) union Sigma_{e-1}(V)`,

where V is the list of91 nonspecial H columns and `Sigma_w(V)` is the set of XOR sums of exactly w distinct site columns. External inconsistency can only shrink `O_e`.

## Exact-weight offset spectra

Exact subset-XOR dynamic programming gives, for A:

- `|O_0|=1`;
- `|O_1|=41`;
- `|O_2|=763`;
- `|O_3|=8525`;
- `|O_4|=62718`.

For D the full exact-weight spectrum is symmetric. At the low-valuation end:

- `|O_0|=1`;
- `|O_1|=20`;
- `|O_2|=173`;
- `|O_3|=838`;
- `|O_4|=1958`;
- `|O_e|=2048` for `5<=e<=87`;
- then `1958,838,173,20,1` for `e=88,...,92`.

Thus D remains subgeneric through valuation4 before saturating the11-bit selected side.

## Exact signed aggregate lemma

Fix a valuation family e and a predecessor input x. Group all active signed sectors by their offset `Hz`.

Every sector in one offset group is supported on the same single selected row/column. Therefore the entire signed sum of that group has rational rank at most1, regardless of cancellation or values on the opposite side. Summing over distinct offsets gives

`rank_Q(K_e) <= |O_e|`.

The exact signed valuation-e aggregate is a valid binary dyadic lift because each nonzero sector coefficient is `+1` or `-1`, both congruent to1 modulo2. Choosing the exact signed aggregate itself as `K_e` removes that complete valuation family from every later residual.

This is the same exact-lift principle previously used for e1/e2, now expressed directly through the universal carry-offset code.

## Sharpened A/D lifts

### e0

There are three direct e0 candidate sectors: the top nullity-one sector and the two single-special full-rank sectors. Their offsets are all0. Hence

`rank(K_A,0)<=1`,

`rank(K_D,0)<=1`.

This supersedes the old rank3 first-lift bound and removes all inherited e0 correction.

### e1

The candidate offset counts give

`rank(K_A,1)<=41`,

`rank(K_D,1)<=20`.

Choose the exact signed e1 aggregate, so no inherited e1 correction remains. This supersedes219/207.

### e2

For D, the candidate offset code gives

`rank(K_D,2)<=173`.

For A the generic offset count763 is weaker than the clean global raw-e2 interpolated singleton-template cover564 from run `32190142624`; therefore use

`rank(K_A,2)<=564`.

These exact signed e2 lifts leave zero inherited e2 correction.

### e3 and e4

For D, candidate offset counts alone give

`rank(K_D,3)<=838`,

`rank(K_D,4)<=1958`.

No external-consistency pruning is needed for these safe bounds. Choosing the exact signed aggregates removes inherited e3/e4 correction.

For A, the offset sets exceed the universal2048 matrix-row cap from e3 onward, so retain the generic2048 bound there.

## Current exact-signed A/D envelopes

The sharpened low layers are

A `[1,41,564,2048,2048,...]`,

D `[1,20,173,838,1958,2048,...]`.

B/C remain

B `[36,812,2048,2048,...]`,

C `[84,972,2048,2048,...]`.

## Dynamic four-leaf convolution through k8

Using the envelopes above, exact convolution gives

- k0 `3,024`;
- k1 `287,664`;
- k2 `12,038,592`;
- k3 `292,005,472`;
- k4 `4,586,351,280`;
- k5 `49,716,263,696`;
- k6 `387,621,863,744`;
- k7 `2,230,860,887,520`;
- k8 `9,647,756,379,008`.

Hence

`sum(k0..k8)=12,320,846,080,000`.

The generic four-leaf S1 Hilbert budget is

`2^44=17,592,186,044,416`,

so the exact margin after k8 is

`5,271,339,964,416`.

Thus the dynamic dyadic prefix now passes through k8.

With all remaining unresolved entries kept generic, k9 is still too large, so complete-tail control is not yet achieved.

## Consequence for the search program

A/D sector rank is no longer the main higher-residue blocker. The universal selected-side map and exact-weight offset code reduce the A/D higher problem to carry-offset cardinality/template compression. D is already controlled through e4.

The next sharp blockers are:

1. A index3 below2048, or B/C index2/index3 improvements, enough to push the dynamic prefix beyond k8;
2. stronger nonlocal/product cancellation that bypasses separate single-leaf residue sums;
3. ultimately the complete dyadic tail or a direct complete-leaf Schmidt theorem.

No change is made here to the current complete d=1 representation/factor-generation bound `84.90275194485017...`; arithmetic-work reduction, ranking/search gain, `alpha<1`, and full-round relevance remain unproved.
