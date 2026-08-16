# V26 Coherent Signed-Trail Tail Bounds

## Purpose

The recovered trail machinery is a coherent signed sum: many distinct trails can terminate at the same mask tuple and must be merged before any hull coefficient or hull energy is interpreted. Therefore the omitted-trail problem is not an orthogonal-energy bookkeeping problem.

This note derives safe tail bounds without assuming that individual trails are orthogonal. It is mathematics-only authority; it does not use missing runtime bytes and does not claim that the project-specific `max_sigma_weight` parameter already satisfies any particular decay law.

## 1. Endpoint-merged trail model

Let `T` be a finite or absolutely summable family of trails. Every trail `tau` has

- endpoint `e(tau)` in a discrete endpoint set `Y`;
- signed real coefficient `w_tau`.

The exact merged hull vector is

`H(y) = sum_{tau : e(tau)=y} w_tau`.

Let `T_K` be a nested retained trail family and define the exact-within-cap merged vector

`H_K(y) = sum_{tau in T_K : e(tau)=y} w_tau`.

The omitted residual is

`R_K = H - H_K`.

All norms below are norms of the endpoint-merged coefficient vector, not sums over unmerged trails.

## 2. Universal l1-tail bound

For every endpoint,

`|R_K(y)| <= sum_{tau notin T_K, e(tau)=y} |w_tau|`.

Therefore

`||R_K||_2 <= ||R_K||_1 <= sum_{tau notin T_K} |w_tau|`.

Define

`L1_tail(K) = sum_{tau notin T_K} |w_tau|`.

Then

`||H-H_K||_2 <= L1_tail(K)`.

This bound is cancellation-safe and requires no orthogonality assumption. It can be pessimistic, but if an analytic counting argument makes `L1_tail(K)` small, full-hull convergence is certified immediately.

## 3. Multiplicity-controlled squared-weight bound

Let

`O_y = {tau notin T_K : e(tau)=y}`

and `m_y = |O_y|`. By Cauchy-Schwarz,

`|R_K(y)|^2 <= m_y sum_{tau in O_y} |w_tau|^2`.

Summing over endpoints gives

`||R_K||_2^2 <= sum_y m_y sum_{tau in O_y}|w_tau|^2`.

If `m_max = max_y m_y`, then

`||R_K||_2^2 <= m_max sum_{tau notin T_K}|w_tau|^2`.

Thus a sum of squared individual omitted trail weights becomes a valid upper bound only after paying an endpoint-coherence/multiplicity factor. Without such control, the individual trail-square sum is not a safe hull-error bound.

This explains mathematically why project authority insists on signed merge before hull energy.

## 4. Level-count / amplitude tail theorem

Suppose omitted trails are partitioned into levels `j=K+1,K+2,...`. Let

- `N_j` be the number of level-`j` trails;
- `a_j` be a certified upper bound on the absolute coefficient of every level-`j` trail.

Then the universal l1 result gives

`||R_K||_2 <= sum_{j>K} N_j a_j`.

If one can prove

`N_j <= A rho^j`

and

`a_j <= B q^j`

with `rho q < 1`, then

`||R_K||_2 <= A B (rho q)^(K+1)/(1-rho q)`.

This is a genuine analytic convergence certificate: combinatorial trail growth may be exponential as long as coefficient decay wins.

No claim is currently made that the recovered `sigma` cap equals this level `j`, or that its coefficients obey a particular `q^j`. Those facts require the canonical core or an independent derivation from the modular-addition Walsh formula.

## 5. Signed-merged shell theorem

A stronger route avoids individual-trail accounting entirely.

Assume the retained families are nested and define the merged shell

`Delta_K = H_K - H_{K-1}`.

If `H_K -> H` in l2, then

`H-H_K = sum_{j>K} Delta_j`.

Therefore

`||H-H_K||_2 <= sum_{j>K} ||Delta_j||_2`.

This is preferable to raw trail energy because every `Delta_j` is already endpoint-merged and therefore already contains all signed interference inside that shell.

If for all `j >= J` one can certify

`||Delta_j||_2 <= A r^j`, with `0 <= r < 1`,

then for every `K >= J-1`,

`||H-H_K||_2 <= A r^(K+1)/(1-r)`.

An empirical decreasing sequence is not yet a certificate. A proof, interval bound, monotonic domination argument, or separately frozen extrapolation/validation protocol is required before the geometric tail is admitted.

## 6. Why cap-energy differences are not shell energies

Write

`H_K = H_{K-1} + Delta_K`.

Then

`||H_K||_2^2 - ||H_{K-1}||_2^2`

`= 2 <H_{K-1},Delta_K> + ||Delta_K||_2^2`.

Therefore the difference between two reported cap energies is not generally the energy of the newly added shell.

In particular, values such as the recovered cap3/cap5 merged energies cannot be subtracted and interpreted as omitted or newly recovered trail energy without the actual merged shell inner products.

## 7. Parseval lower bounds: necessary convergence tests

For a full exact Walsh correlation column of a bijection, and for every coefficient marginal onto a subset of input coordinates, the companion Parseval lemma gives

`||H||_2 = 1`

for the appropriately normalized full vector.

Hence every approximation `H_K` in the same coefficient space satisfies the reverse triangle lower bound

`||H-H_K||_2 >= |1-||H_K||_2|`.

Consequences:

1. If `H_K=0`, the l2 error is exactly `1`.
2. If a target error is `epsilon`, a necessary condition is

   `1-epsilon <= ||H_K||_2 <= 1+epsilon`.

3. Norm convergence is necessary but not sufficient for directional/coefficient convergence. A vector can have norm near one while pointing in the wrong spectral direction.

Thus cap-energy should be used first as a necessary completion diagnostic, never as a complete accuracy certificate.

## 8. Conditional numerical implication of the recovered cap5 first-layer energy

Recovered authority records a cap5 first-layer merged energy

`E_5 = 0.695971894718241`

relative to the local sigma<=5 enumeration.

Its norm is

`sqrt(E_5) = 0.8342493001005401`.

If, after canonical-source recovery, this vector is confirmed to live in the same normalized full correlation-column coefficient space and to be the cap approximation `H_5`, then Parseval alone implies

`||H-H_5||_2 >= 1 - sqrt(E_5)`

`= 0.1657506998994599`.

So under that interpretation cap5 could not yet certify l2 error below about `16.6%`, regardless of its large D&C memory advantage.

This numerical statement is explicitly conditional on normalization/semantic verification from the canonical core. The algebraic inequality is unconditional.

## 9. Local zero marginals are even stronger warnings

The admitted cap4 Stage0 has bounded-cap local D3 one-word marginals that are identically zero at two positions. For the corresponding full exact restricted Walsh spectra, Parseval requires norm exactly one.

Therefore, if the capped local marginal is a compatible truncation approximation,

`||m_full - m_cap4||_2 = 1`

at those two local coordinates.

This means the spectacular sparsity/cancellation seen there is useful information about the bounded trail family but cannot be promoted to a full-exact separator claim without a cap-convergence argument.

## 10. Pairwise / tensor-rank residual transfer

Let `F` be the full boundary tensor and `F_K` its capped approximation. Marginalization and flattening are linear maps. For any chosen column subset or 2|2 flattening, write the linear map as `L`.

Then

`L(F)-L(F_K) = L(F-F_K)`

and

`||L(F)-L(F_K)||_2 <= ||L||_{2->2} ||F-F_K||_2`.

Therefore a certified global l2 tail bound automatically transfers to pairwise marginals and flattenings with the corresponding operator norm. Conversely, low rank observed in `F_K` is not stable under an uncontrolled residual: an arbitrarily small generic perturbation can raise exact algebraic rank dramatically.

This is why approximate numerical rank and exact algebraic rank must be distinguished:

- exact rank is structurally brittle under nonzero tails;
- singular-value decay / epsilon-rank is the stable quantity once a controlled l2/Frobenius residual is available.

A future full-exact compression/contraction argument may therefore need certified epsilon-rank rather than literal exact rank unless the tail is proven identically zero.

## 11. Mathematics-first next gate

Before large pairwise materialization, the preferred sequence is:

1. recover/derive the exact meaning of the project `sigma` level;
2. prove or compute nested merged shells `Delta_K`;
3. determine whether shell norms admit a certified summable tail;
4. use Parseval norm-one identities as necessary checks on every local/full correlation column;
5. only after a residual bound exists, study 2|2 singular-value spectra / epsilon-ranks together with exact capped ranks;
6. use Gram contractions to evaluate pairwise energies without materializing full joint supports whenever possible.

## 12. Claims not admitted

This note does not prove sigma-cap convergence, a geometric tail, low full-exact rank, attack improvement, alpha<1, or full-round relevance. It supplies the error calculus needed to make any such future claim mathematically meaningful.