# V26 Modular-Addition Residual Gram Theorem

## Purpose

For a source-conditioned Walsh state, bounding each reached output-mask column separately and then summing absolute errors can be very loose. Residual columns can interfere just like trail contributions do.

For the published modular-addition sigma definition, this note derives an exact dynamic program for the **pairwise residual Gram matrix** of a hard sigma-cap operator. It permits exact l2 error calculation for an arbitrary linear combination of reached output masks without enumerating the `(u,v)` Walsh domain.

This is a theorem about the published one-addition hard sigma model, not yet a theorem about the recovered project `max_sigma_weight` semantics.

## 1. Full modular-addition Walsh columns

For n-bit addition `z=x+y mod 2^n`, let

`a_w(u,v) = C_add((u,v),w)`

be the normalized Walsh coefficient from output mask w to input-mask pair `(u,v)`.

The published coefficient theorem gives

`a_w(u,v)=0`

unless the sigma compatibility condition holds; otherwise

`a_w(u,v)=(-1)^{<u xor w, v xor w>} 2^{-wt(sigma^w(u,v))}`.

For fixed w, write

`k_w(u,v)=wt(sigma^w(u,v))`.

The full column vector is `a_w`.

## 2. Orthonormality of full columns

The phase functions

`phi_w(x,y)=(-1)^{<w,x+y>}`

are orthonormal over uniform `(x,y)`: for `w != w'`, the sum over x,y of `phi_w phi_w'` vanishes, while each column has norm one.

Since the Walsh transform on `(x,y)` is orthogonal,

`<a_w,a_w'> = delta_{w,w'}`.

Thus the full modular-addition correlation matrix is an isometry from the output-mask space into the larger input-pair mask space.

## 3. Hard sigma-cap residual columns

For the mathematical hard cap K, define

`a_{w,K}(u,v) = a_w(u,v)` if `k_w(u,v)<=K`, and `0` otherwise.

Define residual

`r_{w,K}=a_w-a_{w,K}`.

For an arbitrary source-conditioned coefficient vector

`c = sum_w c_w e_w`,

the exact local approximation error is

`||sum_w c_w r_{w,K}||_2^2 = c^T G_K^res c`,

where

`G_K^res(w,w')=<r_{w,K},r_{w',K}>`.

The task is therefore to compute `G_K^res` without enumerating all `2^(2n)` pairs `(u,v)`.

## 4. Bivariate overlap polynomial

Define

`P_{w,w'}(X,Y)`

`= sum_{u,v} a_w(u,v) a_w'(u,v) X^{k_w(u,v)} Y^{k_w'(u,v)}`,

where terms with either zero Walsh coefficient contribute zero.

Let

`[X^p Y^q]P = g_{p,q}(w,w')`.

Then:

- full inner product: `sum_{p,q} g_{p,q}=delta_{w,w'}`;
- retained-cap Gram: `sum_{p<=K,q<=K} g_{p,q}`;
- residual Gram:

  `G_K^res(w,w') = sum_{p>K,q>K} g_{p,q}`;

- mixed full/retained terms can likewise be obtained from the corresponding rectangular regions of the `(p,q)` plane.

So the exact residual problem reduces to computing a bivariate polynomial of degree at most n-1 in each variable.

## 5. Four-state bit dynamic program

Process bits from most significant to least significant. At bit i, maintain the pair of current sigma bits

`(s_i,t_i) in {0,1}^2`

for masks w and w'. Start at

`(s_{n-1},t_{n-1})=(0,0)`.

For each local pair `(u_i,v_i) in {0,1}^2`, require both nonzero conditions:

- if `s_i=0`, then `u_i=v_i=w_i`;
- if `t_i=0`, then `u_i=v_i=w'_i`.

For i>=1, the next sigma states are

`s_{i-1}=s_i xor u_i xor v_i xor w_i`,

`t_{i-1}=t_i xor u_i xor v_i xor w'_i`.

The local product of Walsh signs is

`(-1)^{(u_i xor w_i)(v_i xor w_i) + (u_i xor w'_i)(v_i xor w'_i)}`.

The exponent simplifies over F2 to

`(w_i xor w'_i)(u_i xor v_i xor 1)`.

The local magnitude/generating factor is

`2^{-(s_i+t_i)} X^{s_i} Y^{t_i}`.

Therefore each permitted local choice contributes

`(-1)^{(w_i xor w'_i)(u_i xor v_i xor 1)}`

`* 2^{-(s_i+t_i)} X^{s_i}Y^{t_i}`

to the transition from `(s_i,t_i)` to `(s_{i-1},t_{i-1})`.

At bit i=0, apply the same nonzero/sign/magnitude factor but do not require a next sigma state; sum over the permitted `(u_0,v_0)`.

This four-state polynomial DP evaluates `P_{w,w'}` exactly.

## 6. Complexity

If all bidegrees are retained, the DP has

- 4 sigma-pair states;
- O(n^2) possible `(p,q)` weight pairs;
- four local `(u_i,v_i)` choices per transition;
- n bit positions.

A straightforward implementation is polynomial time, roughly O(n^3) scalar coefficient operations, and can be reduced when only cap regions up to K and residual aggregates are needed.

For a reached mask support W of size m, constructing the entire residual Gram matrix costs m(m+1)/2 pair DPs, not a `2^(2n)` Walsh enumeration and not a trail expansion.

## 7. Exact on-orbit error

Once `G_K^res` is known for the reached mask set,

`eta_K(c)^2 = c^T G_K^res c`

is the exact hard-cap l2 defect on that local source-conditioned state c.

This is strictly more informative than the cancellation-blind bound

`eta_K(c) <= sum_w |c_w| ||r_{w,K}||_2`.

The Gram quadratic form preserves constructive and destructive interference between residual columns.

## 8. Positive semidefiniteness

By construction `G_K^res=R_K^T R_K`, where R_K is the residual operator restricted to the reached output-mask columns. Therefore

`G_K^res` is positive semidefinite.

This supplies useful consistency checks:

- all diagonal entries are nonnegative;
- every principal minor is nonnegative;
- `c^T G_K^res c >= 0` for every c.

The diagonal has a direct interpretation:

`G_K^res(w,w)=1-R_K(w)`,

where `R_K(w)` is the retained one-column sigma-shell energy from `V26_MODADD_SIGMA_SHELL_THEOREM.md`.

Thus the previous shell polynomial is exactly the diagonal special case of the residual Gram theorem.

## 9. Brute-force validation of the DP identity

As a calculator-only finite check, the four-state bivariate DP was compared with direct Walsh enumeration for every pair `(w,w')` at word sizes

- n=2,
- n=3,
- n=4.

For every pair, every bivariate coefficient `g_{p,q}` matched exactly using rational arithmetic.

This validates the derived recurrence on the exhaustive small domains; the theorem itself follows algebraically from the published coefficient formula and does not rely on the finite check.

## 10. QR error certification route

A ChaCha inverse quarter-round alternates exact XOR/rotation mask permutations with four inverse modular-addition Walsh operators.

If the project approximation were eventually proven equivalent to a local cap for which residual Gram matrices can be derived, then for the current reached coefficient vector at each addition one could compute

`eta_j^2 = c_j^T G_j^res c_j`

and feed those exact on-orbit defects into `V26_LOCAL_TO_GLOBAL_ERROR_TELESCOPING.md`.

This would produce a certified QR residual without enumerating omitted trails.

The same idea extends beyond the hard published sigma cap: for any local approximation whose residual columns admit a compact pairwise inner-product DP, the Gram route remains valid.

## 11. Why this matters for D&C

The D&C representation already exploits factorization of the **kept** signed hull. The residual Gram theorem shows an analogous factorization target for the **discarded** part.

A controlled representation needs both:

- cheap representation/contraction of what is kept;
- cheap certification of what is omitted.

Without the second, memory reduction is an engineering fact but not a full-exact approximation theorem.

## 12. Claims not admitted

This note does not identify the recovered project cap with the published hard sigma cap, does not give a numerical project `epsilon_K`, and does not prove a full second-layer, ranking, alpha, or full-round result.