# V26 Modular-Addition Side-Mask Residual Gram

## Purpose

A ChaCha modular-addition gate acts on two words. In Walsh space the local output basis is indexed not only by the mask w on the updated word but also by a side mask q on the unchanged word. The correct source-conditioned residual Gram matrix must therefore be indexed by pairs `(w,q)`.

This note extends `V26_MODADD_RESIDUAL_GRAM_THEOREM.md` to that two-word gate exactly.

## 1. Addition gate with side mask

Consider the reversible gate

`F(x,y) = (x+y mod 2^n, y)`.

Let `(w,q)` be output masks on the two output words. If `a_w(u,v)` denotes the Walsh coefficient for the addition output mask w alone, then

`(-1)^{<w,x+y> + <q,y>}`

expands with input-mask coefficient

`a_w(u,v)`

at input pair

`(u, v xor q)`.

Equivalently, the full Walsh column of the reversible two-word gate is

`A_(w,q)(u,b) = a_w(u,b xor q)`.

Because F is a bijection, all full columns `(w,q)` are orthonormal.

## 2. Hard-cap residual column

For the mathematical published-sigma hard cap K, let

`r_{w,K}(u,v)`

be the omitted part of the one-addition column. The omitted column for the full two-word gate is

`R_(w,q),K(u,b) = r_{w,K}(u,b xor q)`.

For two output columns `(w,q)` and `(w',q')`, define

`delta = q xor q'`.

Changing variable `v=b xor q` gives the exact residual inner product

`G_K((w,q),(w',q'))`

`= sum_{u,v} r_{w,K}(u,v) r_{w',K}(u,v xor delta)`.

Thus the side masks enter only through their XOR difference delta.

## 3. Shifted bivariate overlap polynomial

Define

`P_{w,w',delta}(X,Y)`

`= sum_{u,v} a_w(u,v) a_w'(u,v xor delta)`

`  * X^{k_w(u,v)} Y^{k_w'(u,v xor delta)}`.

Then the coefficient region with both sigma weights greater than K gives the exact side-mask residual Gram entry:

`G_K((w,q),(w',q'))`

`= sum_{p>K, r>K} [X^p Y^r] P_{w,w',q xor q'}(X,Y)`.

This is the gate-level object needed for exact on-orbit error of a ChaCha addition approximation.

## 4. Four-state shifted bit DP

At bit i maintain the two current sigma bits

`(s_i,t_i)`

for the first and shifted second coefficient.

Start from

`(s_{n-1},t_{n-1})=(0,0)`.

Let `d_i` be bit i of delta. Choose local bits `u_i,v_i`; the second coefficient uses

`v'_i = v_i xor d_i`.

Nonzero compatibility requires

- if `s_i=0`, then `u_i=v_i=w_i`;
- if `t_i=0`, then `u_i=v'_i=w'_i`.

For i>=1 the next states are

`s_{i-1}=s_i xor u_i xor v_i xor w_i`,

`t_{i-1}=t_i xor u_i xor v'_i xor w'_i`.

The local signed generating factor is

`(-1)^E * 2^{-(s_i+t_i)} X^{s_i}Y^{t_i}`,

where

`E = (u_i xor w_i)(v_i xor w_i)`

`  xor (u_i xor w'_i)(v'_i xor w'_i)`.

At i=0 use the same local compatibility/sign/magnitude rule and terminate without imposing a next sigma state.

The DP again has only four sigma-pair states; delta merely changes the second local v bit.

## 5. Exact source-conditioned local defect

Let a current approximate Walsh state on the two output words be

`c = sum_{w,q} c_{w,q} e_(w,q)`.

Then the hard-cap local error is exactly

`eta_K(c)^2 = c^T G_K c`,

with

`G_K((w,q),(w',q'))`

computed by the shifted DP above.

No global trail expansion and no `2^(2n)` input-mask enumeration is required.

## 6. External-context factorization

Suppose the addition acts on two words inside a larger state and write the current coefficient vector as

`Y = sum_z e_z tensor c_z`,

where z labels all masks on untouched words and `c_z` is the two-word coefficient vector for the addition gate.

Different z are orthogonal basis contexts. Therefore the exact local residual norm is

`||(I tensor R_K)Y||_2^2`

`= sum_z c_z^T G_K c_z`.

This is a direct D&C error factorization: one can certify the omitted local energy context by context, then sum the exact quadratic forms, without merging the untouched-word Cartesian product.

## 7. Small-domain validation

As a calculator-only check, the shifted four-state DP was compared with direct rational Walsh enumeration for all choices

`w,q,w',q'`

at n=2 and n=3.

Every bivariate coefficient matched exactly.

This check includes nonzero side-mask shifts `delta=q xor q'`; it therefore validates the extension beyond the unshifted residual Gram special case.

## 8. Consequence for ChaCha error propagation

For a four-addition inverse QR approximation, the mathematically sharp local program is now:

1. represent the reached approximate coefficient state factorwise;
2. before each modular addition, group terms by untouched-word context z;
3. for each context evaluate `c_z^T G_K c_z` using side-mask residual Gram entries;
4. sum over contexts to obtain the exact local on-orbit defect `eta_j` for the chosen hard-cap model;
5. propagate the four local defects with the telescoping theorem.

This is strictly sharper than multiplying retained-energy fractions or summing independent per-mask residual norms.

## 9. Broader significance

The kept-part D&C method factorizes trail computation. The side-mask residual Gram theorem shows that **error certification can be factorized in the same geometry**.

That is the key mathematical pattern needed for controlled compression:

- factorize the represented signal;
- factorize the omitted-error certificate;
- combine both under one global tolerance.

If an analogous compact Gram construction can be derived for the actual recovered project cap semantics after source recovery, the missing global-tail problem may be tractable without enumerating omitted trails.

## 10. Claims not admitted

This theorem concerns the published hard-sigma mathematical model. It does not identify the historical project cap semantics, does not yet provide a canonical project QR residual, and does not admit full second-layer contraction, ranking gain, alpha<1, or full-round relevance.