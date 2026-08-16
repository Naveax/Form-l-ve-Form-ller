# V26 Sigma-Semantics Separation

## Purpose

The mathematics-first analysis produced an important warning: the modular-addition `sigma` of the published Walsh-coefficient theorem and the repository parameter named `max_sigma_weight` must not be identified solely from naming similarity.

This note freezes that separation so future work does not quietly build a theorem about one object and attribute it to the other.

## 1. What is mathematically known from the published modular-addition theorem

For one n-bit modular addition, the published Walsh coefficient characterization defines a binary vector `sigma` from the masks and gives nonzero coefficient magnitude

`2^{-wt(sigma)}`.

A hypothetical hard local rule

`wt(sigma) <= K`

at every modular-addition expansion is therefore a perfectly well-defined mathematical approximation. Its one-addition energy shells and worst-case annihilation behavior are derived separately in `V26_MODADD_SIGMA_SHELL_THEOREM.md`.

## 2. What is known about the recovered project implementation

Historical V25/V26 authority exposes calls such as

`inverse_qr_linear_hull(..., max_sigma_weight=K, ...)`

and records exact-within-cap results for K=2,3,4,5.

However the canonical implementation bytes of `fds_v25_bit_puncturing.py` are currently unavailable. Therefore the repository does not presently expose enough source to prove how `max_sigma_weight` is accumulated or applied internally.

Possible semantics include, for example:

- a hard bound applied separately to every addition;
- a total/aggregate sigma budget across a trail;
- a bound on a particular extension variable rather than every local addition independently;
- an implementation-specific enumeration rule equivalent to the paper parameter only after additional bookkeeping.

These possibilities are examples, not claims about the missing source.

## 3. Independent diagnostic

As a mathematical calculator check, the published one-addition Walsh rule was independently composed backward through the four additions of a standard ChaCha quarter-round while imposing the simple hard rule

`wt(sigma) <= K`

at each addition independently.

Starting from the local q138-style output mask with only word B bit 10 active, this simple paper-level hard-per-addition model collapses completely at small K:

- K=2: nonzero intermediate states survive the first two reverse additions, then the third reverse addition has no retained continuation;
- K=3: states survive through the third reverse addition, then the fourth has no retained continuation.

This calculation was used only as a semantic diagnostic, not as a canonical project measurement.

The admitted recovered project history, by contrast, contains nontrivial exact-within-cap quarter-round/double-round hulls and Stage0 results at comparable cap labels. Therefore the current evidence does not support silently equating the project parameter with the naive hard-per-addition rule used in the diagnostic.

This is not a contradiction in mathematics; it is an unresolved parameter-semantics question caused by the missing canonical core.

## 4. Consequence for current theorems

The following results are source-independent mathematical statements and remain valid:

- the full-QR Parseval marginal lemma;
- orthogonality/rank invariance of the full Walsh correlation operator;
- coherent signed-trail tail inequalities;
- the tensor/Kronecker factorization identities derived from the exposed V26 factor structure;
- the epsilon-rank bridge theorem;
- the modular-addition sigma-shell theorem as a theorem about the published one-addition sigma definition.

The following identification is **not** currently admitted:

`project max_sigma_weight K == hard per-addition published wt(sigma)<=K`.

Therefore no numerical tail/error bound derived for the latter may be attached to the recovered cap2/cap3/cap4/cap5 results until source semantics are restored or independently proven equivalent.

## 5. Safe abstract model until source recovery

Until the canonical core is restored, treat the recovered capped hulls abstractly as a nested or indexed family

`H_K`

only to the extent nestedness is actually supported by authority.

Mathematical error work should use generic quantities:

- merged shell `Delta_K = H_K-H_{K-1}` when both objects are well-defined in the same coefficient space;
- certified residual `epsilon_K = ||H-H_K||`;
- capped flattening singular tail `delta_r(M_K)`;
- full-exact bridge `delta_r(M) <= epsilon_K + delta_r(M_K)`.

Do not substitute a guessed formula for `epsilon_K`.

## 6. Source-recovery questions to answer first

When the canonical core bytes are recovered, inspect and prove precisely:

1. where `max_sigma_weight` is enforced;
2. whether the budget is per addition, per QR, per trail, or another construction;
3. whether K-families are nested coefficient-wise;
4. whether coefficients use the exact published normalization/sign convention;
5. whether omitted K-shells can be obtained by difference of independently exact merged hulls;
6. whether any local pruning other than the sigma rule occurs when beam=None and min_abs=0;
7. whether cap growth converges to the full Walsh correlation operator as K reaches its mathematical maximum.

Only after these are settled can the modular-addition shell theorem be used quantitatively for the recovered project caps.

## 7. Research implication

The central mathematical program is not blocked by this semantic gap. It can proceed at two levels:

- full exact level: Parseval, orthogonal QR invariance, tensor identities;
- abstract capped level: signed factorization, Gram contraction, rank bounds, coherent-tail and epsilon-rank calculus.

What must wait is only the numerical bridge that says how close a specific project cap K is to the full exact object.

## 8. Claims not admitted

The exploratory hard-per-addition collapse is not a NO-GO result for the recovered V25/V26 method, and it must not be entered as one. It only falsifies an overly simple interpretation of the missing parameter semantics.