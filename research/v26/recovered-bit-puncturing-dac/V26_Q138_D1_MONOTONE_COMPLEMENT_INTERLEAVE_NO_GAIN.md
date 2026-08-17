# V26 q138 d=1 monotone complement-interleave certificate barrier

## Statement

Start from the certified high/gap21 physical set

`H={A12..16,B12..16,D12..16,C0..5}`

and monotonically add physical bits from the 84-bit complement of S1, one binary physical row at a time, until reaching the complement of the low23 set.

Consider the following exact certificate calculus at every intermediate physical set P:

1. central coefficient route: begin from the certified standalone high central rank
   `490112=3829*2^7` and charge at most one raw binary factor `x2` for every newly added physical row;
2. central topology route: use the exact reduced q138 terminal-cut graph with
   - four unit physical terminal legs per bit site,
   - carry-chain capacity4 between adjacent sites,
   - rotation capacities1 at offsets8,12,16;
3. predecessor leaves: for each 32-bit leaf word W, charge the generic exact Hilbert exponent
   `min(k_W,32-k_W)`, where k_W is the number of selected physical bits of that word;
4. at each set P, take the better of the two central bounds and add the generic four-leaf Hilbert exponent.

No monotone path in this certificate class can certify a peak below the current

`73+log2(3829)=84.90275194485017...`.

Indeed, every path must pass the layer containing exactly44 newly added complement physical rows. On that layer:

- the best coefficient-route certificate is at least
  `62.90275194485016... + 23 = 85.90275194485016...`;
- the globally optimal topology-plus-generic-leaf terminal-cut certificate is exactly86.

Hence the best available certificate on that unavoidable layer is at least

`85.90275194485016...`, exactly one bit above the current rank3829 materialized-factor exponent.

This closes only the stated monotone/raw-extension/generic-leaf certificate class. It is not a lower bound on the true tensor rank or unrestricted arithmetic complexity.

## 1. The unavoidable 44-added-bit layer

H contains21 physical S1 rows. Its complement inside the128 physical intermediate-mask bits contains107 rows: the low23 S1 rows plus84 non-S1 rows.

A monotone path that adds all84 non-S1 rows one at a time necessarily visits a state with exactly44 added rows.

The central coefficient envelope at that layer is

`log2(490112)+44 = 18.90275194485016...+44`

`=62.90275194485016...`.

## 2. Generic predecessor-leaf Hilbert minimum at 44 additions

At H, selected bit counts in the four predecessor leaves are

`A=5, B=5, C=6, D=5`.

Let `a_A,a_B,a_C,a_D` be the numbers of added non-S1 bits in the four words. Each lies in `[0,21]` and

`a_A+a_B+a_C+a_D=44`.

The generic exact leaf exponent assigned by this certificate calculus is

`ell(a)=phi(5+a_A)+phi(5+a_B)+phi(6+a_C)+phi(5+a_D)`,

where `phi(k)=min(k,32-k)`.

The finite four-variable minimization gives

`min ell = 23`.

For example it is attained by `(a_A,a_B,a_C,a_D)=(0,2,21,21)` and its admissible symmetric variants.

Therefore the coefficient/raw-extension branch cannot certify below

`62.90275194485016...+23 =85.90275194485016...`.

## 3. Topology-plus-leaf optimum is86

The topology branch is a finite binary cut problem.

Use nodes

- 32 central bit-site nodes;
- four predecessor-leaf hub nodes;
- one physical terminal for each A/B/C/D bit.

Edges are

- central adjacent-site capacity4;
- central offset8/12/16 capacity1;
- physical-terminal to central-site capacity1;
- physical-terminal to its leaf hub capacity1.

Fix the21 H terminals on the selected side and the23 low terminals on the unselected side. The84 non-S1 physical terminals are binary decision variables with exact cardinality44. Minimize the total cut capacity over all terminal choices, all32 central-site sides and all four leaf-hub sides.

This objective is exactly

`central_topology_terminal_cut(P) + sum_W min(k_W,32-k_W)`.

The clean MILP has optimum

`86`.

A concrete optimum has leaf selected counts

`A=6, B=26, C=27, D=6`,

leaf contribution23, and places all32 central site nodes on the selected side, giving central physical-terminal cut63 and total86.

The clean verifier also obtains matching MILP dual bound86 with zero MIP gap.

## 4. Consequence

At the unavoidable 44-added-row layer the certificate value is bounded below, within this method class, by

`min(85.90275194485016...,86)=85.90275194485016...`.

Thus merely interleaving raw complement physical bits between H and its complement cannot turn the current rank3829 representation into a lower-width/work certificate while predecessor leaves are still treated only by generic Hilbert ranks.

A successful arithmetic route must use additional coefficient-specific leaf/central joint algebra, a non-monotone regrouping outside this calculus, or a different contraction identity.

## Scope

Exact finite method-scope NO-GAIN result. `epsilon=0`.

Not claimed: true-rank lower bound, unrestricted arithmetic-work lower bound, practical evaluator, ranking/search gain, `alpha<1`, or full-round cryptanalytic relevance.
