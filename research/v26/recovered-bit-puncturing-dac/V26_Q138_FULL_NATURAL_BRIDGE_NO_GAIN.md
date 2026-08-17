# V26 Q138 full natural d=1 bridge no-gain theorem

## Scope

This combines the exact local closures into the largest natural occurrence-closed j2 carry/repeated-D bridge considered so far. It joins:

- the complete low repeated-D chain through D0..5;
- the backward physical C12..14 carry extension around C15,C16;
- the retained-column j2 bridge bits22..27;
- the physical D12..15 high sector at bits28..31;
- the D16 wrap/bit0 factor with physical C0 and shared retained coordinate v3_12;
- the extended-block2 j1 D16 geometry.

The merged factor consumes39 of the44 S1 physical row bits. Only C1..5 remain raw.

This theorem closes this **natural bridge topology**. It is not a lower bound against every possible nonlocal regrouping of the full double-round tensor network.

## 1. Low side

Clean repeated-D theorem:

`rank(D0..5)=524288=16*2^15`.

The three-site C12..14 carry map has exact domain/rank16/16, so it is universally injective on any incoming space. Therefore it multiplies D0..5 by exactly `2^3`:

`n = rank(low merged block) = 524288*8 = 4194304 = 2^22`.

Physical low-side rows are

`A0..5,B0..5,D0..5,C12..16`,

23 bits total.

## 2. High carry bridge

The exact bit22..31 theorem proves

`rank_Q((s21,D12..15) -> retained bridge outputs)=32/32`.

Thus attaching the low `s21` carry cannot collapse the sixteen physical D12..15 high-prefix sectors. They remain a direct sum exactly as in the rank21888 block2 theorem.

## 3. Universal D16/bit0 scaling

For any incoming row space W with retained `v3_12`, `dim W=n`, the exact bit0 theorem gives

`dim L_0(W)=2n`,

`dim L_1(W)=2n`,

`dim(L_0(W) intersect L_1(W))=n`.

The extended-block2 j1 D16 spaces have certified dimensions

`448,448,intersection424`.

The j1 and bit0/low retained column groups are otherwise disjoint, so the intersection of the two D16 tensor-product sectors is the tensor product of the intersections. Therefore, for every fixed D12..15 prefix,

`rank = 448*(2n) + 448*(2n) - 424*n = 1368*n`.

Across the16 independent D12..15 prefixes,

`rank(merged 39-bit factor) = 16*1368*n = 21888*n`.

With `n=2^22`:

`rank = 91,804,925,952`.

## 4. Central rank accounting

The merged low factor uses23 physical S1 bits.

Extended block2 uses16 disjoint physical S1 bits:

`A12..16,B12..16,D12..16,C0`.

Total consumed:

`23+16=39`.

The only remaining S1 physical bits are

`C1,C2,C3,C4,C5`,

so five raw binary channels remain.

Hence the complete central rank bound from this merged topology is

`91,804,925,952 * 2^5 = 2,937,757,630,464`.

But

`2,937,757,630,464 = 171*2^34 = 16*21888*2^23`.

Therefore the fully merged natural bridge reproduces the existing central bound **exactly**. There is no hidden rank gain from combining the previously separate low repeated-D, C-carry, high-carry, D12..15, D16, bit0, and shared-v3_12 mechanisms.

With predecessor-leaf exponent44,

`W_repr(1) <= 78 + log2(171) = 85.4178525148859...`

remains unchanged.

## Interpretation

This is stronger than the earlier one-site and direct-shared-coordinate NO-GAIN results. The obvious physical j2 bridge from the low S1 run to extended block2 is now closed as a whole.

Any further d=1 reduction below `171*2^34` must use a qualitatively different nonlocal regrouping, another retained-coordinate overlap not present in this bridge model, a coefficient-specific outer-mask theorem, or a different central subset/tree decomposition.

No arithmetic-work, ranking, alpha, or full-round attack claim follows.

## Authority

Prerequisites:

- `V26_Q138_BLOCK1_D5_INVOLUTION_FIBER_NO_GAIN.md`;
- `V26_Q138_BLOCK1_C12_D04_MERGED_NO_GAIN.md` (universal C12..14 injectivity lemma);
- `V26_Q138_J2_BRIDGE22_31_INJECTIVE.md`;
- `V26_Q138_BIT0_UNIVERSAL_SHARED_V312_GEOMETRY.md`;
- `V26_Q138_SIGNED_BLOCK2_EXTEND12_RANK21888_THEOREM.md`.

Global ledger verifier:

- `scripts/verify_v26_q138_full_natural_bridge_no_gain.py`;
- `.github/workflows/full-natural-bridge-no-gain.yml`.
