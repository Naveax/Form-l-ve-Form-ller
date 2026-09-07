# V26 Q1.38 C direct-e1 zero-subcube escape coset probe

## Admitted starting point

At the deterministic reachable C predecessor, the first4096 deterministic right-beta Gray-code columns form a12-dimensional coordinate subcube `U` on which the complete direct-e1 aggregate is exactly zero over `Z`. The exact-zero certificate is multiprime: every entry vanishes modulo `3,5,7,11,13`, whose product `15015` exceeds the absolute coefficient bound `3043`.

The corresponding ordered right-beta coordinates are the first12 entries of the admitted aggregate heuristic order. Nine right-beta coordinates remain outside `U`.

## Escape question

Exact vanishing on `U` does not imply low rank of the full aggregate. A neighboring coset `U + e_j` can already contain enough independent columns to restore full row rank.

For each of the nine remaining right-beta coordinates, this probe scans the complete4096-column coset `U + e_j` over `F_3`. It records:

- number of nonzero columns modulo3;
- rank of that coset alone;
- rank accumulated across all tested adjacent cosets;
- first nonzero witness if one exists.

The admitted zero subcube `U` is rescanned first over `F_3` as a state-transition guard and must have rank0.

If any adjacent-coset scan raises the accumulated rank to2048, then the complete direct-e1 C aggregate has rank `2048` over `F_3`, hence exact rational rank `2048`. This rules out any uniform subgeneric rational-rank upper bound for the C aggregate despite the exact zero subcube.

If full rank is not reached, the reported rank is only a lower bound. A coset that is zero modulo3 is not claimed exact-zero without an additional multiprime certificate.

No predecessor-leaf rank, representation-width reduction, arithmetic-work reduction, alpha, or full-round claim is made by a non-full result.
