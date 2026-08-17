# V26 Q138 j2 bridge22..31 injectivity theorem

## Scope

This theorem covers the j2 carry/high bridge from incoming carry `s21` through bits22..31 to the fixed terminal carry `s32=0`.

- bits22..27 contain only retained-column variables on the current d=1 S1 row split;
- bits28..31 contain the physical repeated variables `D12..15` used by the extended block2 high sector.

It does not by itself close the remaining D16/bit0/shared-`v3_12` coupling.

## Domain

After the low repeated-D chain reaches bit21, the only physical/domain coordinates entering this bridge are

`(s21,D12,D13,D14,D15)`.

Thus the full domain dimension is exactly

`2^5 = 32`.

All C/x/w variables on bits22..27 and C/w variables on bits28..31 are retained columns.

## Exact full-rank minor

The verifier fixes 32 explicit retained-column assignments. For each of the32 domain states it contracts the deterministic carry path through bits22..31 using the exact Walsh bit tensor `T`, with terminal condition `s32=0`.

This gives a 32x32 dyadic-rational minor.

Reducing this minor modulo the odd prime

`p=65521`

gives rank32.

Because every coefficient denominator is a power of2, reduction modulo p is valid. A rank32 modular minor implies that the corresponding rational determinant is nonzero. Since the full domain has dimension32, the exact rational bridge rank is therefore

`rank_Q(bridge22..31)=32`.

So the bridge is injective on its entire domain.

## Consequence

The j2 bridge does not lose either:

- the incoming lower carry `s21`, or
- the physical high-prefix tuple `D12..15`.

Therefore attaching the low block1 carry to bits22..31 cannot collapse the sixteen `D12..15` high-prefix sectors. Their direct-sum role in the rank21888 block2 theorem survives this attachment.

Equivalently, any incoming row space exposing `s21` is embedded injectively when the four physical high-prefix bits are added through this bridge. New d=1 compression cannot come from the bit22..31 carry/high chain alone.

The remaining natural place for a nontrivial merged overlap is the D16/bit0/wrap coupling, especially after replacing the original rank16 block1 by the enlarged low repeated-D space while keeping the shared retained coordinate `v3_12` exact.

## Authority

- `scripts/verify_v26_q138_j2_bridge22_31_injective.py`;
- `.github/workflows/j2-bridge22-31-injective.yml`.
