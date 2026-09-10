# V26 Q138 C916 e0 first-dyadic group-output mod-p rank witness

Date: 2026-09-10

## Scope

This note freezes a deterministic physical evaluation witness for the 250 exact integer-valued C916 e0 first-dyadic group residual functions.

The upstream authority is the complete 250-group residual family assembled from:

- 103 singleton groups, including the exact projection-baseline term from `R=(G-2^k)/2`;
- 57 multiplicity-2 groups;
- 90 multiplicity-4 groups.

The physical representation has 680 terms in total: 577 post-Gauss sector terms plus 103 singleton projection-baseline terms.

## Why a modular evaluation witness proves linear independence

Let `f_0,...,f_249` be the 250 integer-valued group residual functions on the 149-bit physical shared domain.

Choose 250 physical points `x_0,...,x_249` and form the integer evaluation matrix

\[
M_{ij}=f_j(x_i).
\]

If `M` has rank 250 modulo an odd prime `p`, then its determinant is nonzero modulo `p`. Therefore the determinant of the integer matrix is itself nonzero. Hence the 250 columns are linearly independent over `Q`, so the 250 functions are linearly independent over `Q`.

This is a deterministic certificate, not a probabilistic inference.

## Candidate construction

The probe evaluates candidates in a fixed order:

1. all 250 group projection origins;
2. all 577 Gauss-support origins;
3. up to eight single projection-basis toggles per group;
4. up to four single Gauss-support-basis toggles per Gauss term;
5. deterministic SHAKE256-derived projection affine points if still necessary;
6. deterministic SHAKE256-derived Gauss-support affine points if still necessary.

The last two stages were not reached because full rank was obtained during the fourth stage.

Duplicate physical points are removed before evaluation. Failure to reach rank 250 would have been reported only as inconclusive.

Two fixed odd primes are tracked in parallel:

```text
65521
1000003
```

## Exact rank growth

```text
stage                       unique cumulative   rank mod 65521   rank mod 1000003
projection origins                       127               78                 78
Gauss-support origins                    503              244                244
projection basis singles                1354              248                248
Gauss basis singles                     1468              250                250
```

The final fourth stage inspected only 201 candidate sources before the first full-rank witness was complete; 114 of those were new physical points.

Global candidate accounting:

```text
unique physical candidates evaluated   1468
duplicate candidates skipped           1560
zero evaluation rows                     32
```

## Frozen witness

The canonical frozen witness uses prime `65521`.

```text
rank                                      250
selected evaluation rows                  250
determinant mod 65521                   27993
witness SHA-256
154b789ef5b116ebae864169d9be793d4e03e1d35a1804b06f871d6b067e21fd
```

The selected-row source composition is:

```text
projection origins             78
Gauss-support origins         166
projection basis singles        4
Gauss basis singles             2
total                         250
```

The witness digest is computed from the prime, deterministic candidate indices, source labels, physical 149-bit points, and every selected evaluation-row entry modulo the witness prime. The frozen verifier recomputes the entire candidate stream, rank process, determinant residue, and digest from the repository code.

The second tracked prime `1000003` independently reaches rank 250 on the same candidate stream. It is not needed for the theorem, but it confirms that the certificate is not an accident of the chosen witness prime.

## Exact conclusion

The 250 exact C916 e0 first-dyadic group residual functions are linearly independent over `Q`.

This strictly strengthens the previous pairwise result. PR #165 proved that no two group outputs are scalar multiples. The present witness also excludes every higher-order rational linear relation among three or more group outputs.

## Interpretation boundary

Linear independence does **not** imply that the joint nonlinear output state requires 250 bits. All 250 functions are still functions of only 149 physical shared input bits, and nonlinear correlations can remain substantial.

Therefore this result does not establish:

- the exact all-250 joint image size;
- a complete grouped-e0 separator width;
- support/e1 carry handling;
- half cross;
- complete C2;
- `W_repr`;
- arithmetic-work or ranking/search bounds;
- full-round relevance;
- `alpha < 1`.

The next useful gate is dependency-aware nonlinear joint-state/separator analysis rather than further searches for linear reuse.

## Frozen decision

```text
MODP_FULL_RANK250_PHYSICAL_EVALUATION_WITNESS
ALPHA_PASS=0
```
