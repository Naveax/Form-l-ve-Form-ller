# V26 Q1.38 saturated-complement exact closure theorem

## Scope

This theorem is a general exact integer-lift theorem for predecessor-leaf matrices across the frozen 11|21 split, with row dimension

`N = 2^11 = 2048`.

It proves two things:

1. any admitted rank-`d` binary parity lift can be completed **exactly in one additional term** of rank at most `N-d`;
2. consequently, dimension-only dyadic residue bookkeeping can always close a leaf at total rank budget exactly `N`, but cannot by itself certify a strict `<N` complete-leaf improvement.

All statements are exact over integers/rationals; `epsilon=0`.

## Saturated primitive lattice lemma

Let

`L <= Q^N`

be a rational subspace of dimension `d`, and define

`Lambda = L intersect Z^N`.

Then `Lambda` is a rank-`d` **primitive** (saturated) sublattice of `Z^N`.

Primitivity is immediate: if `m v in Lambda` for a nonzero integer `m` and `v in Z^N`, then `m v in L`; since `L` is a rational vector space, `v in L`, hence `v in Lambda`.

Therefore `Z^N/Lambda` is torsion-free. A finite-rank torsion-free abelian group is free, so the exact sequence splits. Hence there exists a complementary lattice `Lambda'` of rank `N-d` such that

`Z^N = Lambda direct_sum Lambda'`.

Reduction modulo2 also gives

`dim_F2(Lambda mod2)=d`,

because the reduction kernel is exactly `2 Lambda`: if an element of `Lambda` is coordinatewise even, division by2 stays integral and inside `L`.

This distinction matters for Walsh spaces: a chosen rational Walsh basis can collapse modulo2, while its **saturated integer lattice** still has the full dimension.

## Exact two-term closure theorem

Let `R` be an integer `N x M` matrix. Suppose there exists an integer parity lift `K` satisfying

`K = R (mod 2)`

and

`rank_Q K <= d`.

Choose a rational `d`-dimensional space `L` containing all columns of `K`; if the actual rank is smaller, extend its rational column space arbitrarily to dimension `d`.

Let

`Lambda=L intersect Z^N`

and choose a primitive lattice complement

`Z^N = Lambda direct_sum Lambda'`,

with `rank Lambda'=N-d`.

Since `R-K` is even, define

`S=(R-K)/2 in Z^(N x M)`.

Split every column of `S` uniquely as

`s=s0+s1`, `s0 in Lambda`, `s1 in Lambda'`.

Collect these columns into integer matrices `S0,S1` and define

`K0 = K + 2 S0`,

`K1 = S1`.

Then exactly

`R = K0 + 2 K1`.

Moreover:

- every column of `K0` lies in `L`, so `rank_Q K0<=d`;
- every column of `K1` lies in `span_Q Lambda'`, so `rank_Q K1<=N-d`;
- `K0=R (mod2)` as required.

Therefore:

> **Exact closure theorem.** Any integer residue matrix with an integer parity lift of rational rank at most `d` has an exact two-term decomposition
>
> `R = K0 + 2 K1`
>
> with ranks at most `d` and `N-d`.

There is no unresolved higher dyadic tail in this construction.

## Immediate complete-rank consequence

The rank-sum budget of the generic exact closure is

`d+(N-d)=N`.

For the predecessor-leaf cut this is exactly

`2048`.

Thus the theorem gives a complete exact decomposition at the **generic Hilbert budget**, not below it.

This yields a scoped NO-GO:

> Purely dimension-based completion of an already-known low-rank parity lift cannot by itself certify a strict complete-leaf rank-sum `<2048`; the generic complementary term consumes exactly the remaining dimension.

To obtain a strict complete-leaf improvement one needs additional structure that makes the complementary exact term smaller than `N-d`, overlap/cancellation between terms beyond rank subadditivity, or a direct complete-leaf Schmidt-rank theorem.

## Multi-layer dimension-only NO-GO

The same point persists if several early lift spaces are known.

Suppose exact components lie in rational spaces `L_i` of dimensions `d_i`, and let

`S = span_Q(L_0+...+L_t)`

have dimension `s`. A generic exact lattice complement of their joint saturated span has dimension `N-s`.

Charging ranks separately gives total dimension budget at least

`sum_i d_i + (N-s)`

`= N + (sum_i d_i - s)`

`>= N`.

The excess is precisely the redundancy/overlap in the separately charged early spaces. Therefore dimension-only tail closure after any finite list of dyadic lifts can never force a strict total rank-sum below `N`.

This is not a lower bound on the true matrix rank. It is a NO-GO for this **proof method** when it uses only component dimensions plus a generic complementary tail.

## Finite-prefix gauge corollary

The earlier one-step saturated-code argument remains useful as a diagnostic. If a rank-`d` lift space is followed by a chosen `(N-d)`-dimensional binary complement, the two saturated mod2 codes span `F2^N`.

At any later finite dyadic depth `j>=2`, the parity of the current residual can be absorbed into higher-even modifications of those two old lifts without changing their rational rank envelopes. Repeating this pushes the unresolved residual beyond any prescribed finite depth `T` while setting all intermediate binary lifts to zero.

Hence finite statements such as

`sum(k0..k9)<2^44`

are **gauge-dependent diagnostics**, not invariant compression milestones. One can improve a finite prefix merely by moving the obstruction to a deeper residual. The exact two-term closure theorem makes the invariant lesson clearer: only the complete decomposition/tail matters.

## Application to current A/B/C/D authority

Current exact-signed/direct main authority includes

A `[1,41,564,1761,...]`,

B `[36,812,...]`,

C `[84,972,...]`,

D `[1,20,173,838,1958,...]`.

Applying the one-step complementary construction at the latest displayed subgeneric layer gives safe **prefix diagnostics**

A `[1,41,564,1761,287,1761,287,...]`,

B `[36,812,1236,812,1236,...]`,

C `[84,972,1076,972,1076,...]`,

D `[1,20,173,838,1958,90,1958,...]`.

In particular, alternative representatives can realize

`b2<=1236`,

`c2<=1076`,

without any new direct B/C third-residue theorem.

The corresponding arithmetic diagnostic gives

`sum(k0..k8)=7,312,357,496,576<2^44`,

while the simple alternating k9 diagnostic is

`sum(k0..k9)=20,832,211,913,648>2^44`.

These values are exact but are **not** complete-tail search thresholds.

If hypothetical direct B/C index2 bounds `b2,c2` are inserted and simple alternation is restarted there, the k0..k9 diagnostic is

`12,425,800,334,816`

`+3,537,036,576 b2`

`+2,841,485,712 c2`

`+734,769 b2 c2`.

The equal diagnostic crosses `2^44` between745 and746. This replaces the old31 figure only as a bookkeeping diagnostic; neither31 nor745 is a complete-compression necessity.

## New invariant research target

The correct next work is therefore:

1. **complete-leaf Schmidt geometry:** prove or falsify `rank_Q L_X<2048` uniformly for one or more predecessor leaves;
2. **structured complementary tail:** beat the generic `N-d` exact complement using actual coefficient/carry structure, so the total finite rank-sum becomes `<2048` rather than merely moving residue depth;
3. **product-level cancellation:** exploit cancellation/overlap before separate-leaf rank subadditivity turns the complete budget into a product of per-leaf sums;
4. **aggregate signed rank:** determine whether the complete B/C signed aggregates are already full row rank, which would close broad classes of separate-leaf compression routes.

## Status discipline

Still not claimed:

- complete predecessor-leaf Schmidt rank below2048;
- complete four-leaf factor rank below2^44;
- lower `W_repr(1)` or `W_factor-gen`;
- arithmetic-work reduction;
- ranking/search gain, `alpha<1`, or full-round relevance.
