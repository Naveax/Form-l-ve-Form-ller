# V26 Error-Representation Exponent

## Purpose

FDS needs a mathematical quantity that connects approximation quality to representation/work growth. A fixed cap label is not such a quantity. The natural object is the scaling exponent between certified residual decay and factor/representation growth.

This note derives that exponent under explicit assumptions and shows how it leads to an optimal local error-budget allocation.

## 1. Local exponential model

Consider one local approximation family indexed by integer cap K. Assume that, on the relevant source-conditioned state family, we have certified bounds

`eta(K) <= A q^K`, with `0<q<1`,

and representation/work cost

`C(K) <= B r^K`, with `r>1`.

The constants A,B,q,r may depend on the type of local gate or source family, but not on K over the certified regime.

Define

`theta = log(r)/(-log(q))`.

Then eliminating K gives the error-cost law

`C = O(eta^{-theta})`

up to constants.

More explicitly, to guarantee local error at most tau, it suffices to choose

`K >= log(A/tau)/(-log q)`,

so, ignoring the at-most-one-step ceiling factor,

`C(K) <= B (A/tau)^theta`.

With an integer ceiling, a safe bound is

`C(K) <= B r (A/tau)^theta`.

The dimensionless quantity theta is the **error-representation exponent**.

## 2. Interpretation of theta

A smaller theta is better:

- theta<1: cost grows sublinearly in `1/tau`;
- theta=1: reciprocal error-cost law;
- theta>1: increasingly expensive accuracy.

This is not the attack exponent alpha and must not be called one. It is a local/representation scaling exponent describing controlled approximation quality.

Unlike raw support counts, theta compares the growth of what is kept with the decay of what is omitted.

## 3. m-step composition under additive on-orbit error

Assume m local approximation steps are composed and the local-to-global theorem supplies the contractive/on-orbit bound

`eta_total <= sum_{j=1}^m eta_j`.

For identical local bounds, use a uniform cap K. Then

`eta_total <= m A q^K`.

To achieve target global error epsilon, it suffices that

`K >= log(mA/epsilon)/(-log q)`.

If each local cost is at most `B r^K`, total cost obeys

`C_total <= m B r (mA/epsilon)^theta`.

Therefore

`C_total = O(m^{1+theta} epsilon^{-theta})`

for fixed A,B,q,r.

This is a useful scaling theorem: if local residual decays geometrically faster than cost grows in the exponent sense, a fixed controlled global error can remain polynomial in the number of composed local gates.

It says nothing yet about whether the recovered ChaCha cap family satisfies the required geometric bounds.

## 4. Exactness versus controlled approximation

If epsilon is held fixed as m grows, the theorem gives polynomial scaling in m under the assumptions.

If epsilon itself is required to be exponentially small, for example

`epsilon = 2^{-lambda m}`,

then

`epsilon^{-theta}=2^{theta lambda m}`

and the cost becomes exponential.

Thus a controlled-approximation representation can have favorable scaling for fixed physical/statistical tolerance while exact recovery may remain exponentially expensive.

This distinction is important for FDS: exact representation and certified approximate representation are different success levels.

## 5. Heterogeneous local gates

Now let gate j have

`eta_j(K_j) <= A_j q_j^{K_j}`,

`C_j(K_j) <= B_j r_j^{K_j}`,

and

`theta_j = log(r_j)/(-log(q_j))`.

Eliminating K_j gives the continuous cost envelope

`C_j <= D_j eta_j^{-theta_j}`,

where

`D_j = B_j A_j^{theta_j}`

(up to the integer-cap ceiling factor).

The cap-selection problem becomes

minimize

`sum_j D_j eta_j^{-theta_j}`

subject to

`sum_j eta_j <= epsilon`,

`eta_j>0`.

This is the mathematical form of adaptive accuracy allocation across a factor graph.

## 6. Closed-form optimal allocation for common theta

If all local steps share the same exponent theta>0, solve

`min sum_j D_j eta_j^{-theta}`

subject to `sum_j eta_j=epsilon`.

The Lagrange equations give

`eta_j^{theta+1} proportional to D_j`.

Therefore the optimal continuous allocation is

`eta_j* = epsilon * D_j^{1/(theta+1)} / sum_l D_l^{1/(theta+1)}`.

So expensive gates receive a larger error allowance; cheap gates are driven more accurately.

The resulting minimum cost envelope is

`C_min(epsilon) = epsilon^{-theta} (sum_j D_j^{1/(theta+1)})^{theta+1}`.

This is a clean error-budget theorem for FDS-style factorized approximation.

## 7. Discrete cap version

Real caps are discrete. For each local object j, suppose we have a finite certified menu

`(K, error_j(K), cost_j(K))`.

First remove dominated choices: option a dominates b if

- `error_a <= error_b`,
- `cost_a <= cost_b`,

with at least one strict inequality.

The remaining Pareto menus form a multiple-choice resource-allocation problem.

Under an additive error budget, an exact dynamic program can minimize total cost for a discretized/certified error grid. Alternatively, the Lagrangian relaxation chooses independently

`K_j(lambda) in argmin_K [cost_j(K) + lambda error_j(K)]`.

Varying lambda traces the supported Pareto frontier.

Thus adaptive cap selection is not post-hoc threshold fiddling when the error/cost menus and global tolerance are frozen in advance; it is a well-defined constrained optimization problem.

## 8. Multiplicative telescoping budget

Without contraction assumptions, the local-to-global theorem gives

`eta_total <= product_j (1+epsilon_j) - 1`.

Define logarithmic local risk

`b_j = log(1+epsilon_j)`

and total budget

`B_total = log(1+epsilon_total)`.

Then the sufficient global constraint becomes exactly additive:

`sum_j b_j <= B_total`.

So the same resource-allocation machinery applies after replacing raw local errors by log-risk variables.

This is useful when approximate local operator norms may exceed one.

## 9. Representation exponent from shell data

Suppose a nested capped representation yields empirically or analytically

- factor/support size `S_K`;
- certified residual `epsilon_K`.

A finite-difference local estimate of theta is

`theta_K = [log S_{K+1}-log S_K] / [log epsilon_K - log epsilon_{K+1}]`

when both denominator and numerator are positive.

An admitted asymptotic theta requires a frozen scaling protocol and a certified residual sequence, not merely two convenient cap points.

Still, this ratio is a much more informative diagnostic than reporting that cap5 has millions of factors while cap4 has fewer: it directly measures the price of one unit of certified error decay.

## 10. Connection to epsilon-rank

Suppose cap K gives both

- full-to-cap residual `epsilon_K`;
- capped best rank-r error `delta_r(M_K)`.

The epsilon-rank bridge gives full-exact rank-r error

`E_r(K) <= epsilon_K + delta_r(M_K)`.

The optimization target can therefore include both cap and retained rank:

minimize

`representation_cost(K,r)`

subject to

`epsilon_K + delta_r(M_K) <= epsilon_target`.

This is the natural two-dimensional compression tradeoff:

- K controls omitted-trail/operator error;
- r controls low-rank truncation error inside the retained tensor.

One should optimize both rather than treating cap and rank as unrelated heuristics.

## 11. Source-conditioned advantage

The published modular-addition theorem shows that fixed small hard sigma caps can be poor in uniform operator norm. Therefore the meaningful A,q,r parameters, if they exist, are expected to be **source/on-orbit quantities**, not worst-case quantities over all masks.

This is consistent with the FDS vision: exploit a known deterministic source/orbit rather than claim universal arbitrary-string compression.

The critical mathematical test is whether the reached mask family has a favorable theta and remains favorable as the number of rounds/problem scale grows.

## 12. A concrete research success criterion

A future controlled-approximation branch would have genuine mathematical evidence if it can certify, over a preregistered scaling family:

1. residual decay `epsilon_K`;
2. factor/representation growth `S_K` or work growth `C_K`;
3. a stable error-representation exponent theta;
4. full-exact epsilon-rank or downstream score error at the chosen tolerance;
5. TOTAL cost including factor construction, storage and contraction.

Only after those exist should the project ask whether the resulting total scaling improves an attack exponent or a generative-storage objective.

## 13. Claims not admitted

No theta is currently measured or certified for the recovered V25 cap family. This note introduces the mathematical scaling quantity and its optimization laws; it does not establish a compression win, alpha<1, or full-round cryptanalytic result.