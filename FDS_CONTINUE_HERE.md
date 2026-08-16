# FDS_CONTINUE_HERE

Bu dosya yeni oturumların başlangıç otoritesidir. Yeni bir çalışma oturumunda önce fresh `main` alınır, mandatory reading order uygulanır ve burada yazan ilk tamamlanmamış canonical pass'ten devam edilir.

## Current canonical checkpoint

**Date:** 2026-08-16  
**State:** `P_ONLY_LABELFREE_RELIABILITY_NO_GO_CURRENT_XOR256_FAMILY`  
**Next:** `SYNTHETIC_TARGET_OBSERVABLE_TO_ORACLE_RELIABILITY_LEARNABILITY_AUDIT`  
**Executable backlog:** GitHub Issue `#1`

## Mandatory reading order

1. `AGENTS.md`
2. `FDS_CONTINUE_HERE.md`
3. `FDS_CURRENT_STATE.md`
4. `FDS_VISION.md`
5. `FDS_RESEARCH_DISCIPLINE.md`
6. `FDS_COMPUTE_POLICY.md`
7. `FDS_KNOWLEDGE_GRAPH.md`
8. `FDS_SOURCE_REGISTRY.md`
9. `FDS_VALIDATION_MATRIX.md`
10. `FDS_CHECKLIST.md` + `FDS_DECISION_LOG.md`

## 8-adımlık devam zinciri

### 1. Fresh authority + continuity verification
- Fresh `main` HEAD'i kaydet.
- Yukarıdaki mandatory reading order'ı tamamen uygula.
- Açık GitHub issue'ları kontrol et; canonical next milestone ile çelişiyorsa önce continuity uyuşmazlığını çöz.
- Önceki milestone hash/manifestleri ile local çalışma alanını karşılaştır.

### 2. Synthetic reliability corpus v1
- Frozen seed ile **24 random reduced-key target** üret.
- Her target için frozen 16 xor-256 pair kullan.
- Inference'ta erişilebilir descriptorları kaydet: structural-zero, pair RMS, robust tail shape/kurtosis, max robust-z, entropy, leave-one-out consensus, C1 observable, public counter class.
- Oracle label yalnız synthetic training/evaluation için true-key pair percentile/rank olarak ayrı tutulur.

### 3. Predictability null gate
- Target-shuffle ve row-permutation null'larını önceden dondur.
- Tek-feature monotone baselines + fixed-regularization ridge/logistic kullan.
- Tree/boosting/large model yok; önce bilginin var olup olmadığı ölçülür.
- Descriptor→oracle transferi null'dan ayrışmıyorsa bu branch `NO_GO_IDENTIFIABILITY` olarak kapanır.

### 4. Untouched fresh-target transfer
- Stage 3 geçerse mapping dondurulur.
- Fresh targetlarda true label inference'a verilmeden pair reliability tahmin edilir.
- Rank, paired wins, calibration ve total cost birlikte raporlanır.
- Development başarısı fresh transfer olmadan admitted değildir.

### 5. Observation-conditioned ranking integration
- Yalnız Stage 4 geçerse learned reliability map ranking pipeline'a bağlanır.
- Full 60,672 trail baseline, fixed-first4, top-RMS ve learned aggregator aynı fresh targetlarda karşılaştırılır.
- Hidden preprocessing/cache/descriptor maliyeti TOTAL'a eklenir.

### 6. Structural pivot gate
- Learnability NO-GO ise yeni “unsupervised metric” üretmeye devam etme.
- Ancak yeni observable side-structure matematiksel olarak nontrivial ise yeni family aç: multi-delta orbit, public syndrome, counter-class factorization vb.
- Candidate-independent ama her candidate için cebirsel özdeş olan ilişkiler discriminator sayılmaz.

### 7. Scaling + total accounting
- Her başarılı reduced-model mekanizmada `b`, pair count ve target count scaling ölç.
- `T(b)=C·2^(alpha·b)` fit'i local slope ve bootstrap ile denetlenir.
- Precompute, metadata, cache, model size, verification, false positives ve storage maliyetleri TOTAL'a dahildir.
- `alpha<1` ancak geniş ve stabil scaling ile admitted olabilir.

### 8. Milestone admission + repository closure
Her admitted veya killed milestone sonunda:
- `FDS_CURRENT_STATE.md` güncelle.
- `FDS_CHECKLIST.md` tiklerini güncelle.
- `FDS_DECISION_LOG.md` içine tarihli karar ekle.
- `FDS_KNOWLEDGE_GRAPH.md` dependency/status ilişkilerini güncelle.
- `FDS_SOURCE_REGISTRY.md` ve `FDS_VALIDATION_MATRIX.md` current authority'yi yansıtacak şekilde güncelle.
- Source + test + frozen plan + result summary + cert/manifest commit et.
- İlgili GitHub issue'yu güncelle/kapat.
- Sonraki exact unfinished pass'i bu dosyada açıkça yaz.

## Stop rules

- Failed development gate sonrası validation açılmaz.
- İkinci development setiyle başarısız yöntemi diriltme yok.
- Aynı matematiksel mekanizmayı yeni isimle tekrar test etmek yok.
- Full-round veya alpha-reduction claim yalnız kanıt gate'i geçerse yazılır.
