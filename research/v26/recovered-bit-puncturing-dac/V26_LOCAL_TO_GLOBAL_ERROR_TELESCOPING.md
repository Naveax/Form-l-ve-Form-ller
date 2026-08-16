# V26 Local-to-Global Error Telescoping Theorem

## Purpose

A useful approximation theory for the full ChaCha trail tensor should not require enumerating the omitted global trail set. If each local nonlinear layer has a certified operator or state-dependent approximation error, those local errors can be propagated through the composition algebraically.

This note derives the basic telescoping inequalities needed for that program.

## 1. Sequential composition

Let

`U = U_m U_{m-1} ... U_1`

be the exact linear operator on Walsh coefficient vectors obtained by composing exact local correlation operators, and let

`A = A_m A_{m-1} ... A_1`

be corresponding approximations.

The exact telescoping identity is

`U-A = sum_{j=1}^m U_m ... U_{j+1} (U_j-A_j) A_{j-1} ... A_1`.

This follows by replacing factors one at a time.

Taking any submultiplicative operator norm gives

`||U-A|| <= sum_j (product_{i>j} ||U_i||) ||U_j-A_j|| (product_{i<j} ||A_i||)`.

For exact Walsh correlation operators of bijections, `||U_i||_2=1` because they are orthogonal. Hence

`||U-A||_2 <= sum_j epsilon_j product_{i<j} ||A_i||_2`,

where

`epsilon_j = ||U_j-A_j||_2`.

If every approximation is also contractive, `||A_i||_2<=1`, then

`||U-A||_2 <= sum_j epsilon_j`.

No trail enumeration appears in this bound.

## 2. Bound without assuming approximate contractions

Because

`||A_i||_2 <= ||U_i||_2 + ||U_i-A_i||_2 <= 1+epsilon_i`,

we always have

`||U-A||_2 <= sum_j epsilon_j product_{i<j}(1+epsilon_i)`.

The right-hand side telescopes algebraically to

`product_{i=1}^m (1+epsilon_i) - 1`.

Therefore

`||U-A||_2 <= product_i(1+epsilon_i)-1`.

For small errors this is approximately `sum_i epsilon_i`, but the exact product form makes error accumulation explicit.

## 3. State-dependent version

Uniform operator-norm bounds may be too pessimistic, especially because the modular-addition sigma theorem proves that a fixed small hard cap can be maximally bad on some masks.

For a specific initial Walsh vector `x_0`, define the exact and approximate intermediate states

`x_j = U_j x_{j-1}`,

`y_j = A_j y_{j-1}`, with `x_0=y_0`.

Then

`x_j-y_j = U_j(x_{j-1}-y_{j-1}) + (U_j-A_j)y_{j-1}`.

Since `||U_j||_2=1`,

`||x_j-y_j||_2 <= ||x_{j-1}-y_{j-1}||_2 + ||(U_j-A_j)y_{j-1}||_2`.

Thus

`||x_m-y_m||_2 <= sum_{j=1}^m eta_j`,

where the local **on-orbit defect** is

`eta_j = ||(U_j-A_j)y_{j-1}||_2`.

This is potentially much sharper than `epsilon_j ||y_{j-1}||`, because it measures approximation error only on states actually reached by the source-conditioned orbit.

This distinction is central for FDS: a cap may be terrible uniformly while accurate on the narrow mask family reached from q138.

## 4. Certified local-column version

Suppose `y_{j-1}` has sparse expansion

`y_{j-1} = sum_w c_w e_w`

in the output-mask basis of local operator j, and for every reached basis mask w we have a certified column residual

`r_j(w) = ||(U_j-A_j)e_w||_2`.

Without assuming orthogonality between the residual columns,

`eta_j <= sum_w |c_w| r_j(w)`

by the triangle inequality.

If additional Gram information for residual columns is available, a sharper exact expression is

`eta_j^2 = c^T G_j c`,

where

`G_j(w,w') = <(U_j-A_j)e_w, (U_j-A_j)e_{w'}>`.

Thus the same Gram-contraction philosophy used for signed trail factors can certify approximation error itself.

## 5. Tensor-product parallel layer

ChaCha column and diagonal layers consist of four disjoint quarter-rounds acting in parallel. Let

`U = U_0 tensor U_1 tensor U_2 tensor U_3`,

`A = A_0 tensor A_1 tensor A_2 tensor A_3`.

A tensor-product telescoping identity gives

`U-A = sum_{j=0}^3 (tensor_{i>j} U_i) tensor (U_j-A_j) tensor (tensor_{i<j} A_i)`

up to the fixed chosen ordering.

Therefore

`||U-A||_2 <= sum_j epsilon_j product_{i<j} ||A_i||_2`

and hence, without contraction assumptions,

`||U-A||_2 <= product_j(1+epsilon_j)-1`.

If all four local approximations are contractions,

`||U-A||_2 <= epsilon_0+epsilon_1+epsilon_2+epsilon_3`.

So local QR error certificates can be lifted to a whole ChaCha layer without constructing the 512-bit operator.

## 6. Alternating round layers

For a sequence of column and diagonal layers, apply the sequential theorem to the layer-level approximations. If each layer l has certified defect `E_l`, then

`||U_total-A_total||_2 <= product_l(1+E_l)-1`,

or `<=sum_l E_l` when the approximate layers are contractive.

This gives a mathematically clean target for multi-round controlled approximation:

- certify local nonlinear Walsh approximation defects;
- tensor them into layer defects;
- telescope layer defects through rounds.

The global trail count never enters the error proof directly.

## 7. Interaction with exact linear operations

XOR wire permutations and bit rotations are exact orthogonal permutation operators in Walsh space. Their approximation error is zero and their operator norm is one.

Therefore only modular-addition approximation steps contribute to the error budget in a decomposition that implements XOR/rotation exactly.

This is useful because the published modular-addition Walsh formula is precisely where sigma-weight structure lives.

## 8. From operator error to tensor epsilon-rank

Let the exact round/double-round output boundary tensor be `F=Ux` and the approximate one be `F_K=Ax`. If `||x||_2=1`, then

`||F-F_K||_2 <= ||U-A||_2`.

After reshaping into any matrix flattening, the same coefficient-vector l2 norm equals the Frobenius norm of the matrix. Hence a global operator/state error certificate supplies the epsilon required by `V26_EPSILON_RANK_BRIDGE_THEOREM.md`.

The chain becomes

`local addition errors`

`-> QR errors`

`-> layer errors`

`-> round/double-round residual epsilon`

`-> full-exact epsilon-rank / controlled contraction`.

This is the desired local-to-global mathematical bridge.

## 9. Why uniform hard-cap bounds are insufficient

The modular-addition sigma-shell theorem supplies masks whose hard sigma-cap column residual has norm one. Thus a small fixed cap can have

`||U_add-A_add,K||_2 >= 1`.

A uniform telescoping bound built from such worst-case defects is immediately useless.

Therefore the project should pursue **source-conditioned on-orbit error certificates**, not global fixed-cap operator approximation. In concrete terms, the mathematical question is not

`Is cap K uniformly accurate for addition?`

but

`How much residual does cap K incur on the mask distribution actually reached from the chosen q138/source orbit?`

The latter can be small even when the former is provably large.

## 10. Adaptive mathematical complexity parameter

The source-dependent route suggests that cap should not necessarily be a fixed scalar used everywhere. Abstractly, let each local reached mask w receive a budget `K(w)` sufficient to make its certified residual `r(w,K(w))` below an allocated tolerance.

If a global target error is `epsilon_total`, choose local error budgets `tau_j` satisfying, for example,

`sum_j tau_j <= epsilon_total`

in a contractive/on-orbit setting, and select the minimal local cap needed to satisfy each `eta_j<=tau_j`.

This turns sigma/trail enumeration into an **error-budget allocation problem** rather than a globally fixed threshold.

Such an adaptive scheme would require a separately frozen controlled-approximation protocol before numerical admission. The mathematical point here is only that telescoping identifies the correct optimization variables.

## 11. Compression / TOTAL implication

For FDS, a representation wins only if the cost of achieving the certified errors remains favorable. Therefore the eventual optimization problem is multi-objective:

minimize

`factor generation + representation bytes + contraction work`

subject to

`certified total error <= epsilon_total`.

The telescoping theorem turns the error constraint into local constraints that can potentially be optimized independently or by dynamic programming over the factor graph.

This is a more principled target than fixing cap4 globally because it happened to fit memory.

## 12. Claims not admitted

No local project-cap defect `eta_j` or `epsilon_j` is currently certified because the exact recovered cap semantics are unresolved. This theorem does not yet prove a useful full-round approximation, compression win, ranking gain, alpha<1, or full-round attack relevance.