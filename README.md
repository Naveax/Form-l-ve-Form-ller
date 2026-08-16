# FDS — Formula Data System Research Repository

Bu repo FDS araştırmasının **canonical devam noktasıdır**. Amaç yalnızca sonuç biriktirmek değil; deneylerin, falsifier'ların, NO-GO sonuçlarının, source snapshotlarının ve devam disiplininin kaybolmamasını sağlamaktır.

## Şu anki durum

**Canonical V25 statüsü (2026-08-16):**

- `P_ONLY_LABELFREE_RELIABILITY_NO_GO_CURRENT_XOR256_FAMILY`
- 16-pair common-candidate footprint: **1/6 significant**
- Berk–Jones fresh development median true-key rank: **552.25 / 1024**
- Nested pair-count scaling `M=16→32→64`: **M64 = 0/3 significant**
- Candidate-independent C1 branch observable: bazı targetlarda gerçek sinyal var
- C1 pair-sign orientation gate: **0/4**
- `M128/851` expansion under the same statistic: **NO-GO**
- End-to-end work reduction: **NOT ADMITTED**
- Alpha reduction: **NOT DEMONSTRATED**
- Full-round ChaCha break claim: **NO**

Bir sonraki ana gate: **Synthetic Target Observable → Oracle Pair Reliability Learnability Audit**. GitHub Issue **#1** bu milestone'un executable checklist'idir.

## Mandatory reading order

1. `FDS_CONTINUE_HERE.md`
2. `FDS_CURRENT_STATE.md`
3. `FDS_VISION.md`
4. `FDS_RESEARCH_DISCIPLINE.md`
5. `FDS_KNOWLEDGE_GRAPH.md`
6. `FDS_SOURCE_REGISTRY.md`
7. `FDS_VALIDATION_MATRIX.md`
8. `FDS_CHECKLIST.md`
9. `FDS_DECISION_LOG.md`
10. `archive/RAW_IMPORT_MANIFEST.json` gerektiğinde historical/raw provenance için

## Ham kaynak snapshotı

Bootstrap sırasında o anda `/mnt/data` altında görünen **94 dosya / 4,341,402 byte** byte-for-byte hash'lendi ve yerelde tek ZIP olarak doğrulandı:

- archive SHA-256: `b21a45f80d7af4fdf745d490daf8c100d620e40b89dc6b49a158a8c0f4263863`
- exact archive size: `1,566,535 byte`

`archive/RAW_IMPORT_MANIFEST.json` compact authority kaydıdır.

**Önemli:** Bu ChatGPT/GitHub connector oturumunda GitHub write API UTF-8 içerik/blob kabul ediyor fakat yerel binary dosyayı file-parameter olarak aktaran bir köprü sunmuyor; ortamda authenticated `gh` de bulunmuyor. Bu yüzden 1.57 MB raw ZIP'i repoda varmış gibi göstermiyoruz. Canonical çalışma dosyaları ve provenance/hash kaydı GitHub'dadır; bulk raw byte snapshotı bu committe Git object değildir. Araştırma authority'si raw dump değil, root continuity + source/results/cert zinciridir.

## Çalışma ilkesi

Yerelde hesap yapmak serbesttir. GitHub'a her ara cache'i gömmek zorunlu değildir. Ancak **admitted veya killed milestone** sonrası kaynak, test, frozen plan, sonuç özeti, karar, manifest/hash ve continuity dosyaları repoya dönmelidir. Scratch yeniden üretilebiliyorsa manifestte tarif edilip repo dışında kalabilir.
