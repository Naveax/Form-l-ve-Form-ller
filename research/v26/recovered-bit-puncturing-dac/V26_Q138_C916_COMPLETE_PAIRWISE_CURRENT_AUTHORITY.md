# V26 Q138 C916 complete-pairwise current authority

Status date: 2026-09-14.

`ALPHA_PASS=0`.

This note records the current exact Position-C m4 value authority and the sharp boundary of what has, and has not, been proved. It supersedes older continuation notes only for the C916 m4 pairwise/all-order-affine line; historical A/B/C/D dyadic leaf authorities remain separately valid.

## Complete m4 pairwise value theorem

The m4 family has 90 outputs, hence `binom(90,2)=4005` pairwise factors. All 4005 are now exact value relations:

- 825 subset-support exact value pairs;
- 55 equal-support exact value pairs;
- 2000 overlap exact value pairs, including the two signed-magnitude contractions `(141,247)` and `(160,241)`;
- 1125 formerly activity-only remaining zero-cross pairs, now proved to be exact zero-axis unions and independently sign-reflection invariant.

The exact complete-pairwise weighted count is

`667251639197063986752771721653766635157388976602589789841148591163677039001600000`,

with

`log2 = 268.49247853554294`

and state width 269 bits.

This integer is exact for the complete set of 4005 m4 pairwise value factors. The pairwise-relaxation gap inside that model is exactly zero.

Primary clean authorities:

- zero-cross value authority run `34823110470`;
- complete 4005-pair verification run `34823245596`;
- zero-cross exact relation digest `5b93c1bae1acb4571690af475439ec9e8539d234d4626935812280eeda401d58`.

## Remaining higher-order gap

The complete-pairwise theorem is not an all-order physical-image theorem. In particular it does not yet include:

- the five frozen minimal-empty projection triples;
- the seven frozen minimal-empty projection quadruples;
- the global all-order affine-anchor intersection condition;
- any additional higher-order physical-image constraint not implied by the preceding items.

Therefore the 268.492-bit pairwise count is not permission to claim a 149-dimensional physical image, an end-to-end evaluator reduction, or `alpha<1`.

## Finite projection obstruction authority

The five exact minimal-empty triples are

- `(5,8,184)`;
- `(6,9,154)`;
- `(24,111,112)`;
- `(62,113,165)`;
- `(67,104,165)`.

The seven exact minimal-empty quadruples are

- `(3,8,12,183)`;
- `(3,113,183,185)`;
- `(7,144,154,186)`;
- `(10,24,154,186)`;
- `(11,24,112,181)`;
- `(11,24,112,182)`;
- `(237,239,240,249)`.

Clean event-mass run `34826179077` proves that all 12 forbidden events are pairwise-impossible on separator profiles through domain-state sum 154 and all 12 are active on the three dominant hard profiles 251, 288 and 302. It also counts every single event and all 66 pair intersections exactly on those hard profiles.

The first two Bonferroni inequalities therefore give the rigorous global valid-count interval

`2722414587159602541040697551354574968461239522793839001600000`

`<= N_pairwise+12hyperedges <=`

`441205873912093509972717475553434060732158565102084857212293988604025199001600000`.

Hence the 12 known finite projection obstructions alone guarantee at least

`0.5967789464455109`

bits of reduction relative to the complete-pairwise count. The lower Bonferroni endpoint is intentionally loose and is not an exact finite-hyperedge count.

The same authority gives 13 hard-profile event pairs with exact zero intersection:

`(0,7),(0,8),(1,3),(2,5),(2,6),(2,9),(2,10),(3,7),(3,8),(5,9),(5,10),(6,9),(6,10)`.

Consequently only 384 of the 4096 inclusion-exclusion event subsets avoid a certified zero pair.

## All-order affine exact-solver status

The complete affine-anchor normal span has exact GF(2) rank 92 inside the 149-dimensional physical space. The 90 anchor codimensions have histogram

`{6:12, 7:46, 8:32}`.

Direct global affine recursion and the component affine-polynomial method agree exactly with the pairwise counts on the medium separator profiles:

- domain-state sum 134: `21578474445840`;
- domain-state sum 154: `42542498200320`.

Thus those two profiles have zero all-order affine gain.

The merged component-polynomial scout, clean run `34825970336`, reduces recursion drastically but hits a 750000-state polynomial cap on the first dominant profile 251. Hash-consing canonical affine RREF states, clean run `34826688178`, confirms that the hard obstruction is not merely Python object duplication: profile 251 reaches the 1800000 interned-state cap after generating 1734398 new canonical affine states and 3917198 exact intersection-cache entries.

Conditioning first on the 12 finite projection clauses, clean run `34828969429`, still hits the 750000-state cap on the first hard terminal branch. No incomplete hard-profile affine count is admitted.

## Dominant profiles

Almost all weighted complete-pairwise mass lies in the final three separator profiles:

- domain-state sum 251: pairwise count `643305124889230385720745189422199360`;
- domain-state sum 288: pairwise count `1225045697842497384662724781551504000`;
- domain-state sum 302: pairwise count `1308847670855160788759692358502898560`.

Future all-order work must therefore target 251/288/302. Spending large compute only on the medium profiles cannot materially change the global exponent.

## Current exact-program boundary

Admitted now:

1. complete exact value relations for all 4005 m4 pairs;
2. exact complete-pairwise weighted count above;
3. exact five-triple and seven-quad projection obstruction list;
4. exact single-event and pair-intersection masses on the hard profiles;
5. rigorous finite-hyperedge Bonferroni interval;
6. exact zero all-order affine gain on profiles 134 and 154;
7. rank-92 global affine-normal span.

Not admitted:

1. exact complete count after all 12 finite hyperedges;
2. exact all-order affine counts for 251/288/302;
3. complete physical-image count in dimension 149;
4. arithmetic-work improvement or practical evaluator;
5. ranking/search improvement;
6. `alpha<1`.
