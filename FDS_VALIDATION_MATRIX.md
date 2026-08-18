# FDS_VALIDATION_MATRIX

| Family | Result | Verdict |
|---|---|---|
| One-QR exact | `W_1<=38.768184324776925...<39`, peak `218*2^31` | ADMITTED EXACT |
| d=1 center | `rank_center(S1)<=3829*2^29` | ADMITTED EXACT (`32043410513`) |
| d=1 representation | `W_repr(1)<=84.90275194485017...` | ADMITTED EXACT / UNCHANGED |
| d=1 factor generation | `W_factor-gen<=84.90275194485017...` | ADMITTED MESSAGE/STORAGE / UNCHANGED |
| d=1 coefficient-blind static | `95` | ADMITTED METHOD-SCOPED |
| Materialize-then-contract | output `3829*2^73` scalars | SCOPED ARITHMETIC NO-GO |
| A/D natural lattices | `2^-92 Z` | ADMITTED EXACT |
| B/C natural lattices | `2^-121 Z` | ADMITTED EXACT |
| A/D index0 | `<=3/3` | ADMITTED EXACT |
| A/D index1 | `<=219/207` | ADMITTED EXACT UNIFORM (`32065522597`) |
| B/C index0/index1 | B `36/812`, C `84/972` | ADMITTED EXACT INTEGER-LIFT BOUNDS |
| A/D direct-e2 condition groups | A4531 right21-singleton groups; D8629 left11-singleton groups | ADMITTED EXACT |
| A/D forced cores | A6 outside direct<=189; D5 outside direct<=364 | ADMITTED EXACT |
| A6 interpolated direct cover |565 templates | ADMITTED EXACT (`32160207690`) |
| D5 interpolated direct cover |179 templates | ADMITTED EXACT (`32160149637`) |
| A e1 singleton geometry | all271 supports unique right21 | ADMITTED EXACT (`32189193782`) |
| D e1 singleton geometry | all274 supports unique left11 | ADMITTED EXACT dependency (`32159421297`) |
| Exact signed e1 second lift | same index1 ranks219/207; inherited e0/e1 index2 correction exactly0 | ADMITTED EXACT (`32189863746`) |
| A complete index2 | `a2<=565` | ADMITTED EXACT (`32189863746`) |
| D complete index2 | `d2<=364` | ADMITTED EXACT (`32189863746`) |
| Old D1022 / D851 / D535 | superseded by364 | SUPERSEDED |
| Intermediate A746/D535 | superseded by565/364 | SUPERSEDED |
| Dynamic layers k0..k7 | `27216,4793472,286719696,6955731216,79723547424,535328405616,2657484843456,10194932924416` | ADMITTED EXACT (`32189863746`) |
| Dynamic prefix k0..k7 | `13,474,716,992,512 <2^44` | ADMITTED EXACT; margin `4,117,469,051,904` |
| Complete k>=8 tail | unresolved | ACTIVE EXACT SEARCH |
| B direct third leading support | `<=1796` | ADMITTED SCOPED / NOT COMPLETE b2 |
| C third homogeneous candidate envelope |2048 | SCOPED NO-GAIN |
| B/C coarse support-carry sumset |2048 for both | SCOPED NO-GAIN |
| Raw e2 exact-signed global cover | all reachable raw sectors, including mod2-canceling sectors | ACTIVE VALIDATION |
| A/D arbitrary zero-set internal rank law | no-special rank127; any-special rank128 | ACTIVE VALIDATION |
| Next A/D family counts from rank law | `121,485 +247,065 =368,550` before external pruning | PENDING CLEAN THEOREM RECEIPT |
| Complete predecessor-leaf Schmidt rank | unresolved | ACTIVE ALTERNATIVE |
| d>=2 exact representation | `W_repr(d)<=508.4979393937686...d-333.8951148057971...` | ADMITTED EXACT |
| Arithmetic-work reduction | — | NOT DEMONSTRATED |
| `alpha<1` | — | NOT DEMONSTRATED |
| full-round relevance | — | NO CLAIM |

## Revoked / closed interpretation notes

- Old one-QR support216/rank12 selector remains revoked.
- Frozen-tail k7 necessity statements remain revoked; all tail comparisons are dynamic.
- Pointwise `2^128` affine-coset enumeration is not an accepted practical exact route.
- A/D active-group FWHT envelopes are too coarse for sharp assembled rank.
- D global affine-label hyperplane route is falsified.
- Existing-map-only A6 cover1977 is superseded by interpolated565.
