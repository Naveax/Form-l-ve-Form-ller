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

Bir sonraki ana gate: **Synthetic Target Observable → Oracle Pair Reliability Learnability Audit**.

## Mandatory reading order

1. `FDS_CONTINUE_HERE.md`
2. `FDS_CURRENT_STATE.md`
3. `FDS_VISION.md`
4. `FDS_RESEARCH_DISCIPLINE.md`
5. `FDS_KNOWLEDGE_GRAPH.md`
6. `FDS_CHECKLIST.md`
7. `FDS_DECISION_LOG.md`
8. `archive/RAW_IMPORT_MANIFEST.json` gerektiğinde ham tarih için

## Ham kaynak snapshotı

Bu bootstrap sırasında konuşma çalışma alanında bulunan tüm dosyalar byte-for-byte şu arşive alındı:

`archive/raw-import-2026-08-16.zip`

Dosya bazında SHA-256 ve boyutlar `archive/RAW_IMPORT_MANIFEST.json` içinde bulunur.

## Çalışma ilkesi

Yerelde hesap yapmak serbesttir. GitHub'a her ara cache'i gömmek zorunlu değildir. Ancak **admitted milestone** sonrası kaynak, test, sonuç özeti, karar, manifest/hash ve continuity dosyaları repoya dönmelidir. Scratch yeniden üretilebiliyorsa manifestte tarif edilip repo dışında kalabilir.
