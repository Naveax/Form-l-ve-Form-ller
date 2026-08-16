# FDS_VALIDATION_MATRIX

## Admission matrix

| Family / claim | Training | Fresh development | Validation | Current verdict |
|---|---:|---:|---:|---|
| First-order pair selector | done | done | done | NO-GO |
| Positive Ritz spectral selector | done | done | not opened | NO-GO |
| Projected HVP binary selector | done | done | not opened | NO-GO |
| Corrected DAPS 8192 | done | 2W/4L vs full | not opened | NO-GO |
| Natural C2 group selector | done | 3W/3L vs full | not opened | NO-GO |
| Robust C2 group seed | done | killed in training geometry | not opened | NO-GO |
| Top-RMS observation pair selector | label-free rule | 3W/3L | not opened | NO-GO for promotion |
| D-opt pair diversity | label-free rule | 6/6 same set as RMS | not opened | NO distinct value |
| Common-candidate BJ footprint M16 | synthetic primitive PASS | 1/6 significant | not opened | NO-GO |
| Pair-count scaling M64 | same statistic | 0/3 significant | not opened | NO-GO; M128/851 stopped |
| C1-only pair sign orientation | 4 canonical targets | gate 0/4 | not opened | NO-GO |
| Synthetic descriptor→oracle learnability | NOT STARTED | NOT STARTED | LOCKED | ACTIVE NEXT |
| End-to-end work reduction | — | — | — | NOT ADMITTED |
| `alpha < 1` | — | — | — | NOT DEMONSTRATED |
| Full-round relevance | — | — | — | NO CLAIM |

## Gate discipline

1. Bir satır `NO-GO` olduktan sonra ikinci development setiyle aynı yöntemi diriltme.
2. Validation yalnız pre-registered development gate geçerse açılır.
3. Confirm yalnız validation geçerse açılır.
4. Post-hoc diagnostic yeni hypothesis üretebilir ama aynı milestone içinde promotion kanıtı değildir.
5. Runtime/memory/precompute/storage/metadata TOTAL accounting'e dahildir.

## Next active row

`Synthetic descriptor → oracle reliability learnability`

PASS için minimum:
- target-grouped CV,
- target-shuffle + row-permutation null,
- predeclared small model family,
- untouched target transfer,
- inference sırasında oracle/true-key label erişimi olmaması,
- effect size ve cost gate'in önceden dondurulması.
