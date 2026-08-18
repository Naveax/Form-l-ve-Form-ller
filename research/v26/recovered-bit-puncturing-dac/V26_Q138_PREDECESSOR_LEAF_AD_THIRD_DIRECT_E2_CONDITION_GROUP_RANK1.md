# V26 Q1.38 predecessor-leaf A/D third direct-e2 condition groups are rank one

## Scope

This theorem concerns only the direct `e=2` support-indicator component of the A/D third dyadic residue across

`S1={0,1,2,3,4,5,12,13,14,15,16}`.

It does not bound the number of predecessor conditions that may be active at once, and it does not include the inherited e=1 sign correction. Therefore it is not by itself a complete third-residue rank theorem.

## Direct supports

After canonical external elimination, the reachable odd direct-e2 supports are:

- A: `12098` supports;
- D: `12363` supports.

Every one has exact S1 cut intersection zero. Hence, after fixing a predecessor input for which the support is active, each support indicator factors as one rank-one beta matrix

`1_L(beta_S1) 1_R(beta_complement)`.

The exact predecessor-input affine conditions collapse the supports into:

- A: `4531` distinct conditions, with support multiplicities `3653 x3`, `261 x2`, `617 x1`;
- D: `8629` distinct conditions, with support multiplicities `3734 x2`, `4895 x1`.

Supports in one condition group are active or inactive together.

## A: common right singleton in every condition group

For every A direct support, the complementary21 beta coordinates have projection rank21. Thus the right factor is a singleton.

Write its location as an affine map

`rho_t(x) in F2^21`

of the128 predecessor bits, valid on the support's predecessor condition `C_t`.

For every pair of A supports with the same canonical predecessor condition `C`, exact affine reduction proves

`rho_t(x)=rho_u(x)` for every `x in C`.

Equivalently, every coordinate of `rho_t-rho_u` reduces to zero modulo the affine row space of `C`.

Therefore, for fixed `x in C`, all support matrices in the group have the form

`u_i tensor e_rho`.

Their binary XOR is

`(XOR_i u_i) tensor e_rho`,

whose rational rank is at most1.

## D: common left singleton in every condition group

For every D direct support, the S1-left11 beta coordinates have projection rank11. Thus the left factor is a singleton.

Write its location as

`lambda_t(x) in F2^11`.

For every pair of D supports with the same canonical predecessor condition `C`, exact affine reduction proves

`lambda_t(x)=lambda_u(x)` for every `x in C`.

Thus the group XOR has the form

`e_lambda tensor (XOR_i v_i)`

and again has rational rank at most1.

## Consequence

For every fixed predecessor input `x`, let

`N_A(x)` = number of the4531 distinct A predecessor conditions satisfied by x,

`N_D(x)` = number of the8629 distinct D predecessor conditions satisfied by x.

Then the direct-e2 binary matrices satisfy

`rank_Q(E_A,2(x)) <= N_A(x)`,

`rank_Q(E_D,2(x)) <= N_D(x)`.

This strictly supersedes counting raw direct supports with multiplicity. The remaining optimization problem is the assembled rank across simultaneously active rank-one condition groups, not a12098/12363 weighted-support activity problem.

No complete A/D third-residue rank, complete leaf Schmidt-rank, representation improvement, or arithmetic-work improvement is claimed here.
