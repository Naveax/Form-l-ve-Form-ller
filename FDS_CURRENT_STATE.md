# FDS_CURRENT_STATE

## Canonical status — 2026-08-16

### Admitted infrastructure / observations
- Reduced-model source/orbit research framework çalışıyor.
- Signed trail / second-layer contraction hattında exact-within-cap ve factorized yöntemler araştırıldı.
- Pair-product HVP small-reference'a karşı exact doğrulandı; 60,672-term full HVP pratik maliyette ölçüldü.
- Natural C2 grouping'de term-level diagonal sıfırken group-level off-diagonal support resurrection gözlendi.
- Candidate-independent C1 observable bazı targetlarda branch-level gerçek correlation taşıyor.
- Arbitrary 4-word C1 point evaluation için batch yaklaşımı repeated evaluation ile exact eşleşecek şekilde doğrulandı.

### Canonical NO-GO / not admitted
- First-order pair gradient selector: NO-GO.
- Positive Ritz spectral leverage selector: NO-GO.
- Projected/truncated HVP binary selector: NO-GO.
- Corrected DAPS batch-greedy: NO-GO.
- Static natural C2 group selector: NO-GO.
- Robust-min C2 selector / robust two-group seed: NO-GO.
- Observation-conditioned top-RMS pair selector: aggregate signal var, robust gate geçmedi.
- D-opt pair diversity: top-RMS ile 6/6 aynı set, distinct value yok.
- 16-pair common-candidate footprint: 1/6 significant, NO-GO.
- Pair-count scaling M16→M32→M64: M64 0/3 significant, M128/851 aynı statistic ile STOP.
- C1-only pair sign orientation: 0/4 gate, NO-GO.
- End-to-end work reduction: NOT ADMITTED.
- `alpha < 1`: NOT DEMONSTRATED.
- Full-round ChaCha break: NO.

### Latest key numbers
- BJ fresh dev p-values: `[0.802, 0.315, 0.514, 0.603, 0.027, 0.148]`
- BJ true-key ranks: `[510.5, 1014, 594, 703, 23, 498]`
- BJ median rank: `552.25 / 1024`
- M64 footprint significant: `0/3`
- M64 p-values: approximately `[0.690, 0.899, 0.326]`
- C1 branch corr targets `[715,677,888,910]`: approximately `[+0.304,-0.045,+0.221,+0.326]`
- C1 pair agreement: `[56.25%,43.75%,50.00%,56.25%]`

## Exact next milestone

`V25_SYNTHETIC_RELIABILITY_LEARNABILITY_AUDIT`

Amaç: inference-time observable descriptorlarda oracle pair reliability hakkında **ölçülebilir ve fresh-target'a taşınabilir bilgi var mı** sorusunu cevaplamak. Yeni selector tasarımı bundan sonra gelir, önce değil.
