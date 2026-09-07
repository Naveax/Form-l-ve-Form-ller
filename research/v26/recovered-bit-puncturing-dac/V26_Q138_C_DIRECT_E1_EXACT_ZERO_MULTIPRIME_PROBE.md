# V26 Q1.38 C direct-e1 exact-zero multiprime probe

## Motivation

At the deterministic reachable C predecessor witness, clean exact aggregate probes found the first4096 deterministic Gray-code columns identically zero over both `F_3` and `F_5`, despite3043 direct-e1 sectors being active. Whole-sector `+M/-M` cancellation had previously been ruled out, so any genuine zero here must come from partial overlap between different affine supports.

## Exact integer certificate

Each aggregate entry is a sum of at most3043 normalized direct-e1 sector contributions, each in `{+1,-1}` when its support contains that matrix entry and0 otherwise. Therefore every integer coefficient `c` obeys

`|c| <= 3043`.

Evaluate the same exact aggregate entries modulo the five pairwise-coprime primes

`3,5,7,11,13`.

Their product is

`15015 > 3043`.

Hence if an entry is zero modulo every one of these primes, then `15015 | c`; the absolute bound forces `c=0` over the integers.

The verifier computes all five residue systems directly in one clean run, using disjoint2048-bit residue masks and the same exact predecessor/support/Gauss-phase specialization as the admitted aggregate probes. It tests the identical first4096 right-beta Gray-code columns.

If every row in all4096 columns vanishes modulo all five primes, those entire4096 aggregate columns are certified **exactly zero over Z**. This is a direct certificate of partial cross-support signed cancellation on the sampled right-beta subcube; it is not merely a finite-field rank observation.

The result still does not determine the remaining right-beta columns or the complete aggregate rank. No complete predecessor-leaf rank, representation-width reduction, arithmetic-work reduction, alpha, or full-round claim is made.
