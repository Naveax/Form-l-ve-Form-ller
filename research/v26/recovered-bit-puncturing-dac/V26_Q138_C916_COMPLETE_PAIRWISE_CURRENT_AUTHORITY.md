# V26 Q138 C916 current physical authority

Status date: 2026-09-14.

`ALPHA_PASS=0`.

This note records the current exact Position-C m4 value/affine/physical-factor authority. Historical A/B/C/D dyadic leaf authorities remain separately valid. Every integer admitted below comes from an exact clean CI authority; capped scouts and incomplete searches are not promoted to theorems.

## Complete 4005-pair value theorem

The m4 family has 90 outputs, hence `binom(90,2)=4005` pairwise factors. All 4005 are exact value relations:

- 825 subset-support exact value pairs;
- 55 equal-support exact value pairs;
- 2000 overlap exact value pairs, including signed-magnitude contractions `(141,247)` and `(160,241)`;
- 1125 remaining zero-cross pairs, all exact zero-axis unions and independently sign-reflection invariant.

The exact complete-pairwise weighted count is

`667251639197063986752771721653766635157388976602589789841148591163677039001600000`,

with `log2 = 268.49247853554294` and bit length 269.

Primary authorities include zero-cross run `34823110470`, complete-pairwise verification, and zero-cross relation digest

`5b93c1bae1acb4571690af475439ec9e8539d234d4626935812280eeda401d58`.

## Exact finite projection-hyperedge model

The frozen five minimal-empty triples and seven minimal-empty quadruples are exact. Two independent exact implementations, including merged PR #239 run `34831706439`, give the complete pairwise-plus-12-hyperedge count

`119224931058957005800358130035798112729920532677074863008477782553762159001600000`,

with `log2 = 266.00793353949246` and bit length 267.

Hard-profile exact counts are:

- 251: `114884695573259724175905211418508096`;
- 288: `218548782904222169092344242900939904`;
- 302: `234148899850520139999772901208978048`.

The former Bonferroni bounds are historical diagnostics only; the finite 12-hyperedge conjunction is now counted exactly.

## Complete all-order affine-support theorem

Exact iterative closure proves that, in the presence of all 1318 pairwise zero-activity conflicts, the complete higher affine obstruction family contains 19 inclusion-minimal conflicts. Its digest is

`e510dae8f89a09a914839c542e8a70806167531dffa2470f52b376ce48db30a7`.

The closure theorem checks every inclusion-maximal support admitted by those conflicts and proves nonempty exact 149-bit affine-anchor intersection whenever no conflict is present. Therefore the exact complete pairwise plus all-order affine-support weighted count is

`100215909735124105069922281032909019043326715916545026952580687530924399001600000`,

with `log2 = 265.75735915215614` and bit length 266.

Hard-profile affine-support counts are:

- 251: `96491872903925175488260425426864960`;
- 288: `183697181089509355446657454121817216`;
- 302: `196896631570740171574763723334509184`.

The affine normal span has exact GF(2) rank 92 inside the 149-dimensional physical space. All-order affine support is a complete theorem for that support condition, but it is strictly weaker than the full physical output-value image.

## Certified physical quotient factors

The current exact quotient model contains six ternary physical factors:

- `(5,181,182)`, 4 forbidden quotient tuples;
- `(11,12,24)`, 3 forbidden quotient tuples;
- `(62,67,104)`, 2 forbidden quotient tuples;
- `(111,112,113)`, 3 forbidden quotient tuples;
- `(69,82,87)`, 3 forbidden quotient tuples, with a five-state magnitude endpoint at gid 82;
- `(130,131,132)`, 2 forbidden quotient tuples.

It also contains five exact quaternary physical factors:

- `(4,5,8,9)`, 3 forbidden tuples;
- `(4,5,8,114)`, 28 forbidden tuples;
- `(4,5,9,114)`, 28 forbidden tuples;
- `(4,8,9,114)`, 6 forbidden tuples;
- `(5,8,9,114)`, 12 forbidden tuples.

The conjunction of the complete 4005-pair model, the complete 19-conflict affine-support theorem, all six certified ternary quotient factors, and all five certified quaternary quotient factors was counted exactly by merged PR #258, clean run `34840416927`:

`90987190266267462495323685079227633113020903735137825407846207198697839001600000`.

Its `log2` value is `265.6179829442682`; bit length is 266.

The two newest ternary factors affect only the medium profiles relative to the previous four-ternary/five-quad checkpoint:

- profile 134: `21578474445840 -> 21387962445840`;
- profile 154: `42542498200320 -> 39497049400320`.

Profiles 251/288/302 remain at the previous four-ternary/five-quad checkpoint values:

- 251: `87639022052873245102889951271577152`;
- 288: `167100640692156092551072548681523584`;
- 302: `178525130634609700681252266313472640`.

This integer is exact for the stated finite physical-factor model. It is not the full physical image count.

## Raw physical ternary frontier

Merged batch-5 PR #257, clean run `34840541439`, exactly resolved extended-shortlist target indices 16 through 19.

Targets 16, 17 and 18 have exact physical joint image equal to the join of their three exact pair projections.

Target 19, triple `(178,179,184)`, has exact raw physical image size 251 versus exact pairwise closure size 275, hence 24 exact physical holes. The frozen raw-hole digest is

`26550add0ec46d20b259f3db3f18beb1bbd4db6a0839e7d7edf7db26c8ccc6db`,

and the exact joint-distribution digest is

`0a8ef378e6a6b0eacf1a1b76eb8c103c6fa9fb88ea594b34095a6ebd50103f9f`.

This proves a genuine ternary physical-value obstruction beyond complete pairwise value factors and complete all-order affine support. It is not yet admitted as a quotient factor until exact sign-reflection quotient descent is separately certified.

## Exact-program boundary

Admitted now:

1. all 4005 exact m4 pairwise value factors and their exact weighted count;
2. the exact 12 finite projection-hyperedge conjunction;
3. the complete 19-conflict all-order affine-support theorem and exact weighted count;
4. six exact ternary and five exact quaternary physical magnitude-quotient factors;
5. the exact combined affine-plus-physical-factor count above;
6. the raw target-19 physical ternary obstruction `(178,179,184)` at full 149-bit value level.

Not admitted:

1. quotient propagation of target 19 before exact descent certification;
2. completeness of the currently known ternary/quaternary physical factor family;
3. the complete 149-dimensional physical output-value image count;
4. an end-to-end arithmetic-work improvement or evaluator;
5. `alpha<1`.

The active frontier is exact physical-image discovery and exact quotient descent/propagation for newly found factors. `ALPHA_PASS=0`.
