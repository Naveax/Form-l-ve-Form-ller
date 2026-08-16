# V26 Epsilon-Rank Bridge Theorem

## Purpose

Exact algebraic rank is not a stable bridge from a bounded trail family to the full Walsh tensor: an arbitrarily small generic residual can raise exact rank to full rank. The stable quantity is approximate rank under a certified norm error.

This note connects three ingredients already derived in the mathematics-first V26 line:

1. a capped signed boundary tensor `F_K`;
2. a certified residual bound `||F-F_K|| <= epsilon` for the full exact tensor `F`;
3. low-rank / low-singular-tail structure of a chosen column bipartition of `F_K`.

The result is a rigorous route from bounded-cap factorization to full-exact controlled approximation, without pretending capped exact rank is itself a full-exact invariant.

## 1. Flattening setup

Fix a column bipartition `A|B`, for example `03|12`, and let

`M = Flat_{A|B}(F)`,

`M_K = Flat_{A|B}(F_K)`.

Assume a certified Frobenius residual

`||M-M_K||_F <= epsilon`.

Such a bound may come directly from a tensor residual bound, or from a sharper bound for this particular flattening.

Let the singular values of a matrix `X` be

`sigma_1(X) >= sigma_2(X) >= ... >= 0`.

Define the best rank-r Frobenius error

`delta_r(X) = min_{rank(Y)<=r} ||X-Y||_F`

`= (sum_{j>r} sigma_j(X)^2)^{1/2}`

by Eckart-Young-Mirsky.

## 2. Main bridge inequality

Let `Y_K` be a best rank-r approximation to `M_K`. Then

`||M-Y_K||_F <= ||M-M_K||_F + ||M_K-Y_K||_F`

`<= epsilon + delta_r(M_K)`.

Therefore

`delta_r(M) <= epsilon + delta_r(M_K)`.

This is the central bridge theorem.

Special case: if

`rank(M_K) <= r`,

then `delta_r(M_K)=0`, hence

`delta_r(M) <= epsilon`.

So a rank-r capped flattening plus an epsilon-certified cap residual implies that the full exact flattening has epsilon-approximate rank at most r.

## 3. Epsilon-rank definition

For tolerance `eta>=0`, define

`rank_eta(M) = min{r : delta_r(M) <= eta}`.

The bridge theorem implies

`rank_{epsilon + delta_r(M_K)}(M) <= r`.

In particular, if `rank(M_K)<=r`,

`rank_epsilon(M) <= r`.

This is the correct robust replacement for the invalid implication

`rank(M_K) small => rank(M) small`.

## 4. Singular-value stability

Let `E=M-M_K`.

Weyl's singular-value perturbation inequality gives

`|sigma_j(M)-sigma_j(M_K)| <= ||E||_2 <= ||E||_F <= epsilon`

for every j.

Hoffman-Wielandt/Mirsky also gives the global bound

`sum_j (sigma_j(M)-sigma_j(M_K))^2 <= ||E||_F^2 <= epsilon^2`.

Consequences:

- a capped singular value much larger than epsilon cannot disappear in the full tensor;
- a capped zero singular value may become nonzero, but by at most epsilon individually;
- exact rank can jump, while numerical rank above a certified epsilon scale is stable.

## 5. Gap-certified rank persistence

Suppose for some r,

`sigma_r(M_K) > epsilon`

and

`sigma_{r+1}(M_K)=0`.

Then

`sigma_r(M) >= sigma_r(M_K)-epsilon > 0`,

while

`sigma_{r+1}(M) <= epsilon`.

Thus the full exact matrix has exactly r singular directions that are guaranteed to remain above the residual floor; all additional directions lie at or below epsilon.

More generally, if

`sigma_r(M_K) - sigma_{r+1}(M_K) > 2 epsilon`,

then the corresponding spectral gap persists in `M`.

This makes singular gaps a more meaningful structural target than raw capped support cardinality.

## 6. Orthogonal QR invariance

For the full exact next-column QR layer, let the local Walsh correlation operators on the columns be orthogonal matrices `T_c`. Across bipartition `A|B`, the flattening transforms as

`M -> U M V^T`,

where

`U = tensor_{c in A} T_c`,

`V = tensor_{c in B} T_c`.

Both U and V are orthogonal. Therefore every singular value is exactly invariant:

`sigma_j(U M V^T) = sigma_j(M)`.

Hence

- exact rank is invariant;
- every epsilon-rank is invariant;
- every best rank-r Frobenius error `delta_r` is invariant.

So once the full exact boundary tensor is controlled, the next exact QR layer does not worsen the intrinsic low-rank approximation problem across a whole-column bipartition. It only changes the coordinate representation/sparsity.

## 7. Capped QR caveat

The frozen V26 QR-transform experiment applies another bounded local trail operator, not the complete orthogonal Walsh correlation matrix. The invariance statement above does not automatically apply to that capped operator.

For the capped operator `T_K`, error propagation must instead be written explicitly. If

`M' = T M`,

`M'_K = T_K M_K`,

then

`M'-M'_K = T(M-M_K) + (T-T_K)M_K`.

Thus

`||M'-M'_K|| <= ||T|| ||M-M_K|| + ||T-T_K|| ||M_K||`.

For the full exact orthogonal T, `||T||_2=1`. The second term is the operator-approximation error of the capped QR itself. This decomposition separates boundary-tensor truncation error from next-layer transform truncation error instead of mixing them into support counts.

## 8. Tensor-network interpretation

For a capped boundary tensor with the exact mixture-of-products form

`F_K = sum_r a_r tensor_d D_{r,d}`, 

one can estimate or compute low-rank structure locally before materializing a global matrix. For a 2|2 cut,

`M_K = sum_r a_r tensor_d Q_{r,d}`.

Each term obeys

`rank(tensor_d Q_{r,d}) = product_d rank(Q_{r,d})`,

so

`rank(M_K) <= sum_r product_d rank(Q_{r,d})`.

This gives a rigorous capped rank upper bound. Combined with a certified residual epsilon, it becomes a full-exact epsilon-rank upper bound via the bridge theorem.

The logical chain is therefore

`local capped ranks -> global capped rank bound -> certified cap residual -> full-exact epsilon-rank bound`.

That chain is mathematically meaningful. The shorter chain

`small capped support -> full exact separator`

is not.

## 9. Energy retained by a rank-r approximation

Because

`||M||_F^2 = sum_j sigma_j(M)^2`,

the fraction of Frobenius energy captured by the best rank-r approximation is

`Q_r(M) = 1 - delta_r(M)^2 / ||M||_F^2`.

If the full exact tensor/flattening is normalized and `||M||_F` is known, the bridge bound gives a certified lower bound

`Q_r(M) >= 1 - (epsilon + delta_r(M_K))^2 / ||M||_F^2`.

Thus the eventual separator criterion should be expressed not only in bytes/support, but in a triplet:

- rank r or factor width;
- certified residual epsilon;
- retained full-exact energy lower bound.

## 10. Contraction error downstream

Suppose a later stage evaluates a linear functional `ell(M)` with dual norm `||ell||_*`. Replacing `M` by a rank-r approximation `Y` gives

`|ell(M)-ell(Y)| <= ||ell||_* ||M-Y||`.

With the bridge theorem,

`|ell(M)-ell(Y_K)| <= ||ell||_* (epsilon + delta_r(M_K))`.

This is the form needed to connect tensor compression to a final correlation/score calculation. A small representation is useful only when its induced downstream error is also controlled.

For nonlinear ranking decisions, a separate margin argument is required: if the certified score error is smaller than half the observed gap between competing candidates, the ordering is stable; otherwise a ranking claim is not certified.

## 11. Recommended mathematical gate

The next robust separator gate should eventually freeze quantities of the form:

1. choose a bipartition, initially compare `01|23`, `02|13`, `03|12`;
2. compute capped singular spectra or rigorous local rank bounds;
3. certify a cap residual `epsilon_K` independently of the rank calculation;
4. report `delta_r(M_K)` for a preregistered r / memory budget;
5. certify the full-exact bound

   `delta_r(M) <= epsilon_K + delta_r(M_K)`;

6. only call the separator useful if the right-hand side is small enough for the downstream correlation/ranking tolerance and TOTAL memory/work is favorable.

## 12. Claims not admitted

No numerical epsilon_K is currently certified for the recovered V25 sigma-cap family. Therefore this theorem does not yet admit a full-exact low-rank separator, full second-layer contraction, ranking gain, alpha<1, or full-round relevance.

Its role is to identify the stable mathematical invariant that the project should measure once cap semantics and tail error are controlled.