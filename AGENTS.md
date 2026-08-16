# AGENTS.md — FDS Autonomous Continuation Contract

Bu repo üzerinde çalışan her agent için canonical çalışma sözleşmesi.

## Başlangıçta zorunlu

1. Fresh `main` HEAD'i çöz ve kaydet.
2. Şu sırayla tamamen oku:
   - `FDS_CONTINUE_HERE.md`
   - `FDS_CURRENT_STATE.md`
   - `FDS_VISION.md`
   - `FDS_RESEARCH_DISCIPLINE.md`
   - `FDS_KNOWLEDGE_GRAPH.md`
   - `FDS_SOURCE_REGISTRY.md`
   - `FDS_VALIDATION_MATRIX.md`
   - `FDS_CHECKLIST.md`
   - `FDS_DECISION_LOG.md`
3. İlk tamamlanmamış canonical pass'i `FDS_CONTINUE_HERE.md` ve açık GitHub issue'lardan belirle.
4. Daha önce `NO-GO` olan aileyi yalnız yeni, açıkça farklı mekanizma varsa yeniden aç.

## Çalışırken

- Sonuç görülmeden split/metric/gate/stop rule dondur.
- True-key/oracle bilgiyi inference descriptorlarına sızdırma.
- Post-hoc diagnostic'i promotion kanıtı yapma.
- TOTAL accounting yap: compute + precompute + storage + cache + metadata + verification.
- Büyük yeniden üretilebilir scratch'i Git'e gömmek zorunda değilsin; build recipe/hash/manifest kaydet.
- Hız için local Python/Numba/Rust/C++ kullanabilirsin.
- Reproducibility/matrix/CI için GitHub Actions kullanabilirsin.
- Hangisi kolay/hızlı ise compute orada yapılır; **authority her zaman GitHub'a geri döner**.

## Bir milestone kapanırken

Aşağıdakiler tamamlanmadan “bitti” deme:

1. Source/runners commit edildi veya açık build recipe var.
2. Regression/reference tests kaydedildi.
3. Frozen plan/split kaydedildi.
4. Compact result summary kaydedildi.
5. PASS/NO-GO decision açık yazıldı.
6. Manifest/hash/cost accounting kaydedildi.
7. `FDS_CURRENT_STATE.md` güncellendi.
8. `FDS_CHECKLIST.md` güncellendi.
9. `FDS_DECISION_LOG.md` güncellendi.
10. `FDS_KNOWLEDGE_GRAPH.md` ve `FDS_CONTINUE_HERE.md` bir sonraki exact pass'e taşındı.

## Claim policy

Gate geçmeden şu claimler yasaktır:

- arbitrary/random data için guaranteed 100×/1000× lossless compression,
- end-to-end key-recovery work reduction,
- `alpha < 1` demonstrated,
- full-round ChaCha break/relevance.

Reduced-model structural signal değerlidir ama yukarıdaki claimlerle aynı şey değildir.

## Current next task

GitHub Issue #1: **V25 — Synthetic Reliability Learnability Audit**.
