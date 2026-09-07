# V26 Q1.38 C direct-e1 aggregate mod-5 rank probe

## Motivation

The clean corrected mod-3 aggregate probe at the deterministic reachable C predecessor witness found all first4096 sampled right-beta columns equal to zero over `F_3`, despite3043 direct-e1 sectors being active. This does **not** imply rational rank zero. It only shows that every sampled aggregate coefficient is divisible by3.

The next exact discriminator is a second odd prime.

## Probe

Use the identical C predecessor witness, active-sector set, affine-support specialization, complete Gauss-corrected phase specialization, right-bit ordering, and Gray-code column family from the admitted mod-3 diagnostic. Recompute the integer signed sector sum modulo5.

Residues are accumulated exactly as five disjoint2048-bit row masks. The resulting sampled matrix is stored as a compact `uint8` array and ranked with FLINT over `F_5` after2048 columns, and if needed after4096 columns.

If the sampled matrix reaches rank2048 over `F_5`, then

`rank_F5(K_C sampled) <= rank_Q(K_C) <= 2048`

forces

`rank_Q(K_C)=2048`

at that reachable predecessor. This would prove that the mod-3 zero image is prime-specific divisibility rather than complete rational cancellation, and would rule out a uniform subgeneric rational-rank upper bound for the complete direct-e1 C aggregate.

If rank2048 is not reached, the result remains only a modular lower bound; no rational upper bound follows.

No complete predecessor-leaf rank, representation-width reduction, arithmetic-work reduction, alpha, or full-round claim is made.
