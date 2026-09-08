# v26 q=138 B/C grouped-e0 reachable + relaxed-half ZZ envelope: 748 / 916

## Result

The exact half-uniform linear-state / relaxed-scalar construction and the reachable-joint grouped-e0 construction can be combined positionwise without assuming that equal GF(2) spans have equal integer Walsh-complement geometry.

The resulting certified second-integer-lift upper bounds are

- **B: `rank_Q <= 748`**, using the canonical grouped-e0 basis with the exact-linear-image relaxed-half span;
- **C: `rank_Q <= 916`**, using the reachable-joint grouped-e0 basis with the same relaxed-half construction.

This improves the previous relaxed-half pair `B <= 748, C <= 936` by 20 dimensions on C while preserving the B bound.

## Exact half relaxation

For both B and C, the four half sectors have an exact combined predecessor/right linear image of rank 18. Therefore all `2^18 = 262144` image states can be enumerated. Exactly 131072 states have nonempty support, and allowing all 16 scalar phase patterns per feasible state is a safe relaxation of the true quadratic scalar image.

The resulting relaxed-half GF(2) span has rank 144 for both positions.

## Grouped-e0 comparison

The reachable-joint grouped-e0 construction and the canonical grouped-e0 construction have the same GF(2) dimensions:

| position | grouped-e0 GF(2) rank | grouped-e0 + relaxed-half GF(2) rank |
| --- | ---: | ---: |
| B | 272 | 272 |
| C | 388 | 388 |

Thus the relaxed-half span adds no new GF(2) direction to either grouped-e0 span. This does **not** make the displayed exact ZZ Walsh-complement quotient basis-independent.

## Exact Walsh-complement quotients

The admitted support-only Walsh spaces have dimensions 668 for B and 788 for C. Recomputing the integer quotient rank for both constructions gives:

| position | canonical quotient | reachable quotient | canonical total | reachable total | selected total |
| --- | ---: | ---: | ---: | ---: | ---: |
| B | 80 | 92 | 748 | 760 | **748** |
| C | 148 | 128 | 936 | 916 | **916** |

The asymmetry matters. Reachability improves C by 20 dimensions but worsens the displayed B quotient by 12 dimensions. The certificate therefore takes the valid positionwise envelope rather than imposing one construction on both positions.

## What is proved

The frozen verifier reconstructs the exact rank-18 half linear image, enumerates the feasible states, rebuilds the relaxed-half span, rebuilds the reachable grouped-e0 family, verifies the GF(2) containment/equality checks, and recomputes both ZZ Walsh-complement quotient ranks before selecting the positionwise minimum.

Exploratory authority: GitHub Actions run `34213132070`, job `102018555319`, completed successfully on 2026-09-08.

## Scope limits

This certificate concerns the admitted second dyadic integer-lift sign-span model only. It does not prove a complete B2/C2 leaf bound, `W_repr`, arithmetic work, ranking/search complexity, or a full-round result. In particular, it does not close the remaining scalar/carry/representation chain.

`ALPHA_PASS=0`.
