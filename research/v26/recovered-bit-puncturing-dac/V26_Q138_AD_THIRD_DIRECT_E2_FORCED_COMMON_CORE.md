# V26 Q1.38 A/D direct-e2 forced common-core theorem

## Scope

This theorem concerns only the **direct e=2 support-indicator component** of the third dyadic predecessor-leaf residue across the frozen

`S1={0,1,2,3,4,5,12,13,14,15,16}`

11|21 split.

The already admitted condition-group rank-one theorem gives, uniformly over every fixed 128-bit predecessor input:

- A: 12098 odd direct-e2 supports collapse to 4531 distinct predecessor affine conditions, and all supports in one condition group share one right21 singleton factor;
- D: 12363 odd direct-e2 supports collapse to 8629 conditions, and all supports in one group share one left11 singleton factor.

Hence the direct-e2 matrix rank at a fixed predecessor input is at most the number of active condition groups. This theorem does **not** yet determine that maximum. It proves that every global maximizer of the active-group count lies in a small mandatory affine common core.

## 1. Low-codimension condition geometry

Clean exact condition geometry gives:

A condition free dimensions

`{118:4052, 119:472, 120:7}`,

so condition codimensions are

`{10:4052, 9:472, 8:7}`.

D condition free dimensions

`{117:3541, 118:4406, 119:670, 120:12}`,

so condition codimensions are

`{11:3541, 10:4406, 9:670, 8:12}`.

Pointwise enumeration of these affine cosets is therefore impossible and is not used.

## 2. Exact averaging lemma

Let `V` be any nonempty affine predecessor-input subspace and let `C_g` be one condition group.

If `V cap C_g` is empty, the group contributes zero on `V`.

Otherwise let

`r_g(V) = codim_V(V cap C_g)`.

For uniform `x in V`, the exact activation probability of group `g` is

`2^(-r_g(V))`.

Therefore the exact mean number of active groups on `V` is

`mu(V) = sum_g 2^(-r_g(V))`,

where the sum is over compatible groups.

Consequently there exists at least one `x in V` with active-group count at least

`ceil(mu(V))`.

This is a deterministic counting statement, not a sampling argument.

## 3. Equation incidence

For A there are only 465 distinct canonical affine condition equations. The six most frequent occur in

`4437, 4437, 4435, 4343, 4342, 4250`

of the 4531 groups.

For D there are 751 distinct canonical equations. The six most frequent occur in

`8446, 8444, 8267, 8265, 8265, 7392`

of the 8629 groups.

The first five equations in each position are mutually consistent.

## 4. A: six equations are mandatory

Let `V_A,6` be the affine node satisfying the six most frequent A equations.

Exact intersection accounting gives

- compatible groups: 4067;
- residual condition-rank distribution inside `V_A,6`:
  `{2:3, 3:364, 4:3700}`;
- exact mean active count:
  `mu(V_A,6)=555/2=277.5`.

Therefore the global A active-group maximum is at least 278.

For each of the first five frequent equations, violating that equation can activate at most the groups which do not explicitly require it. The corresponding crude but rigorous complement uppers are at most

`94, 94, 96, 188, 189`,

all strictly below 278. Hence every global A maximizer must satisfy the first five equations.

Now work inside that forced five-equation node `V_A,5`. Exact branching on the sixth equation gives:

- sixth=true: 4067 compatible groups and mean `555/2`;
- sixth=false: only 182 compatible groups.

Since the global maximum is at least278, the sixth=false branch cannot contain a maximizer. Thus every global A maximizer satisfies all six equations.

Moreover, adding the seventh most frequent A equation with its canonical right-hand side to `V_A,6` is inconsistent. Hence every point in the forced A core necessarily lies on the opposite side of that seventh literal.

So the global A direct-e2 active-group maximizer is confined to the rank-6 affine common core `V_A,6`.

## 5. D: five equations are mandatory

Let `V_D,6` satisfy the six most frequent D equations.

Exact intersection accounting gives

- compatible groups: 7070;
- residual condition-rank distribution:
  `{2:6, 3:531, 4:3622, 5:2911}`;
- exact mean active count:
  `mu(V_D,6)=12327/32=385.21875`.

Therefore the global D active-group maximum is at least386.

For each of the first five frequent D equations, the literal-complement group-count uppers are at most

`183, 185, 362, 364, 364`,

all strictly below386. Hence every global D maximizer must satisfy the first five equations.

Inside the forced five-equation node `V_D,5`, exact branching on the sixth equation gives:

- sixth=true:7070 compatible groups, mean `12327/32`;
- sixth=false:1014 compatible groups, mean `1917/32`.

The sixth=false upper1014 is not below the certified global lower386, so the sixth D equation is **not** proved mandatory.

Thus the certified D common core has rank5.

Within `V_D,5`:

- compatible groups:8084;
- residual condition-rank distribution:
  `{3:12, 4:649, 5:4129, 6:3294}`.

## 6. Consequence for the direct-e2 rank search

Any exact upper bound for the number of active A groups only needs to be proved on `V_A,6`.

Any exact upper bound for the number of active D groups only needs to be proved on `V_D,5`.

Since each condition group contributes a rank-one direct-e2 term after fixing the predecessor input,

`rank_Q(E_A,2(x)) <= N_A(x)`,

`rank_Q(E_D,2(x)) <= N_D(x)`,

where `N_A,N_D` are the active condition-group counts.

The next exact route is therefore a residual-signature / affine-dual envelope inside these forced cores, not a 2^128 point enumeration and not the previously abandoned large MILP.

No complete third-residue rank, complete leaf Schmidt-rank, arithmetic-work, ranking/search, alpha, or full-round claim is made here.
