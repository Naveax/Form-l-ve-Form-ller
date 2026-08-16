# FDS_SOURCE_REGISTRY

Bu registry araştırmada kullanılan bilgi sınıflarını ayırır. Bir iddia yalnız burada veya ilgili milestone manifestinde kaynak sınıfıyla eşleşiyorsa canonical sayılır.

## Sınıflar

- `MEASURED_LOCAL`: yerel kodla gerçekten ölçülmüş sonuç.
- `VERIFIED_REFERENCE`: küçük/toy/reference uygulamayla exact eşleşme.
- `FROZEN_PROTOCOL`: sonuç görülmeden sabitlenmiş split/metric/gate.
- `AI_HYPOTHESIS`: bağımsız model önerisi; deney yapılmadan gerçek kabul edilmez.
- `EXTERNAL_SOURCE`: paper/docs/web kaynağı; tarih/URL/versiyon kaydedilir.
- `HISTORICAL`: eski sohbet/deney; current authority ile çelişirse current kazanır.
- `EXPLORATORY_POST_HOC`: sonuç görüldükten sonra hesaplanan diagnostic; promotion için kullanılamaz.
- `KILLED_FAMILY`: falsifier/gate ile kapatılmış araştırma ailesi.

## Current authority sources

| ID | Class | Scope | Current status |
|---|---|---|---|
| SRC-CURRENT-001 | MEASURED_LOCAL | BJ common-candidate 16-pair fresh development | 1/6 significant; NO-GO |
| SRC-CURRENT-002 | MEASURED_LOCAL | Nested pair count M16/M32/M64 | M64 0/3 significant; expansion stopped |
| SRC-CURRENT-003 | MEASURED_LOCAL | C1 label-free orientation | branch signal target-dependent; pair gate 0/4 |
| SRC-CURRENT-004 | VERIFIED_REFERENCE | pair-product HVP | small explicit reference exact |
| SRC-CURRENT-005 | VERIFIED_REFERENCE | arbitrary-4-word C1 batch point evaluation | repeated evaluator exact |
| SRC-CURRENT-006 | FROZEN_PROTOCOL | synthetic reliability learnability | next unfinished canonical pass |
| SRC-HISTORY-001 | HISTORICAL | prior chat/import bundle | archived/hash-indexed; not automatically current |
| SRC-AI-001 | AI_HYPOTHESIS | multi-model FDS reviews | hypotheses only until locally falsified/verified |

## Raw history

Bootstrap sırasında mevcut çalışma alanı 94 dosya / 4,341,402 byte olarak hash'lendi. Compact authority record `archive/RAW_IMPORT_MANIFEST.json` içindedir. Binary bulk snapshotın GitHub connector üzerinden doğrudan file-parameter aktarımı desteklenmediği için raw bytes current committe source-of-truth olarak kullanılmaz; historical claims gerektiğinde original conversation files veya yeniden materialize edilen bundle ile hash karşılaştırması yapılır.

## Rule

Yeni milestone kapanırken bu registry güncellenir. AI önerisi doğrudan `MEASURED_LOCAL` statüsüne terfi edemez; arada kod/deney/falsifier gerekir.
