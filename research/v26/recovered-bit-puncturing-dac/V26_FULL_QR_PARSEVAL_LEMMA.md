# V26 Full-QR Parseval Marginal Lemma

## Purpose

This note separates two mathematical objects that must not be conflated:

1. the full exact Walsh correlation operator of a ChaCha quarter-round;
2. the bounded local sigma-cap trail operator used by the recovered V25/V26 experiments.

The Stage0 result is exact relative to the second object. The lemmas below describe the first object and therefore give rigorous diagnostics for what a bounded cap can or cannot mean about the full operator.

## 1. Full correlation matrix

Let `f : F_2^N -> F_2^N` be the 128-bit ChaCha quarter-round viewed as a bijection (`N=128` for four 32-bit words). For input mask `alpha` and output mask `beta`, define the normalized linear correlation coefficient

`C_f(alpha,beta) = 2^{-N} sum_x (-1)^{<alpha,x> + <beta,f(x)>}`.

For fixed `beta`, `C_f(.,beta)` is the full exact inverse linear-hull column for that output mask.

## 2. Subset-marginal identity

Let `S` be any subset of input bit coordinates and write `alpha=(alpha_S,alpha_barS)`, `x=(x_S,x_barS)`. Define the coefficient marginal

`m_{S,beta}(alpha_S) = sum_{alpha_barS} C_f((alpha_S,alpha_barS), beta)`.

Then

`m_{S,beta}(alpha_S) = 2^{-|S|} sum_{x_S} (-1)^{<alpha_S,x_S> + <beta,f(x_S,0_barS)>}`.

Proof: substitute the definition of `C_f`, exchange the two sums, and use Walsh orthogonality

`sum_{alpha_barS} (-1)^{<alpha_barS,x_barS>} = 2^{|barS|}` if `x_barS=0`, and `0` otherwise.

Therefore `m_{S,beta}` is exactly the normalized Walsh spectrum of the restricted Boolean function

`x_S -> <beta,f(x_S,0_barS)>`.

## 3. Parseval consequence

Because the restricted phase function takes values in `{+1,-1}`, normalized Walsh Parseval gives

`sum_{alpha_S} m_{S,beta}(alpha_S)^2 = 1`.

Hence, for the full exact quarter-round correlation operator:

- no nonempty subset marginal can be identically zero;
- in fact every subset marginal has squared l2 energy exactly `1`.

This statement also covers `beta=0`: the restricted phase is constant and the spectrum is a delta at the zero mask.

## 4. Orthogonality of the full QR correlation operator

Let `W` be the normalized Walsh-Hadamard matrix and `P_f` the permutation matrix of the bijection `f`. Up to the conventional transpose/orientation,

`C_f = W P_f W^T`.

Both `W` and `P_f` are orthogonal, so `C_f` is orthogonal.

Consequences for a full multi-column tensor transformed by independent quarter-round correlation operators:

- Frobenius energy is preserved;
- matrix/Schmidt rank across any bipartition of whole columns is preserved;
- the next exact column-QR layer is an invertible local basis change for intrinsic tensor-rank questions.

## 5. Consequence for the admitted Stage0 zero marginals

The admitted bounded-cap Stage0 has exact single-column cancellations in `C0` and `C3`. Mapping the cap4 word-union supports back to diagonal-local coordinates gives

- `D0 = [1,1,1,1]`,
- `D1 = [394,58,58,8]`,
- `D2 = [44,1,122,3792]`,
- `D3 = [0,0,16,16]`.

Thus, inside the bounded sigma-cap family, the local `D3` one-word coefficient marginals at positions 0 and 1 are identically zero.

By the Parseval lemma, such an identically-zero one-word marginal is impossible for the corresponding full exact QR correlation column.

Therefore these zeros are necessarily properties of the bounded sigma-cap trail representation, not algebraic zeros of the full exact quarter-round operator.

This is stronger than the already-recorded warning that a zero single-column marginal does not imply zero joint correlation: even the full exact local one-word spectrum itself must eventually become nonzero when the omitted trail family is restored.

## 6. Rigorous truncation-error interpretation

Let `m` be a full exact subset marginal and `m_cap` the bounded-cap approximation to that same marginal, when the recovered implementation is interpreted as a truncation/subsum of the full trail expansion.

Since `||m||_2 = 1`, the reverse triangle inequality gives

`||m - m_cap||_2 >= |1 - ||m_cap||_2|`.

In particular, if `m_cap` is identically zero, then

`||m - m_cap||_2 = 1`.

So a zero capped local marginal is maximally incomplete in l2 norm relative to the full exact local restricted Walsh spectrum.

Implementation caveat: applying this residual statement to the recovered code requires confirming, from the canonical core bytes, that the bounded sigma-cap object is literally a truncation/subsum of the same full correlation expansion with compatible normalization. The full-operator lemma itself does not depend on those missing bytes.

## 7. Research implication

The pairwise/joint tensor-rank analysis remains mathematically useful for the bounded-cap model, especially for locating correlations hidden by signed marginal cancellation. But it cannot by itself justify a full-exact conclusion while the cap omits all one-word restricted spectral energy on some local coordinates.

The more fundamental bridge question is now:

`How does omitted Walsh/trail energy decay as the local sigma cap increases, and can that tail be bounded without enumerating the full hull?`

A useful future result would be an analytic or certified upper bound on

`||m - m_cap||_2`

and on the analogous local `2|2` matricization residuals as a function of sigma cap.

Only after such cap-convergence control can low-rank / separator behavior observed at small cap be promoted toward a full-exact structural claim.

## 8. Immediate mathematics-first order

1. Keep the existing Stage0 and frozen QR-cap measurements scoped exactly as bounded-cap results.
2. Treat the full QR operator through the Parseval/orthogonality lemmas, not through sparse-cap support counts.
3. Once canonical runtime bytes are restored, verify the exact mathematical meaning/normalization of `max_sigma_weight` in the recovered core.
4. Derive or measure cap-by-cap local marginal energies for the `D3` positions that are zero at cap4.
5. Attempt an analytic tail bound for omitted sigma classes before investing in large joint materialization.
6. In parallel, use the tensor-rank reframing to measure exact local 2|2 ranks inside each bounded cap, but label them as capped-model ranks until convergence is controlled.

## 9. Claims not admitted

This lemma does not demonstrate cap convergence, low full-exact rank, a new attack, alpha reduction, or full-round relevance. It provides a rigorous reason not to interpret bounded-cap zero marginals as full-exact structural zeros.