# FDS_RESEARCH_DISCIPLINE

## 1. Pre-registration
Her deneyden önce:
- training/development/validation/confirm split,
- metric,
- threshold/gate,
- parameter grid,
- stop rule,
- TOTAL accounting kapsamı
yazılır ve commit edilir veya en azından immutable çalışma dosyasına kaydedilir.

## 2. Freshness
- Development'ta seçilen yöntem aynı development verisiyle “kanıtlanmış” sayılmaz.
- Validation yalnız development gate'i geçtiyse açılır.
- Failed method ikinci development setiyle diriltilmez.
- Confirm yalnız validation geçerse açılır.

## 3. Exactness hierarchy
Her sonuç şu sınıflardan biriyle etiketlenir:
- `EXACT`
- `EXACT_WITHIN_CAP`
- `CONTROLLED_APPROXIMATION`
- `HEURISTIC`
- `EXPLORATORY_POST_HOC`

Post-hoc exploratory sonuç promotion için kullanılamaz.

## 4. Total accounting
Şunlar maliyetin içindedir:
- preprocessing,
- source scan,
- training,
- model/metadata storage,
- cache build,
- selector cost,
- candidate evaluation,
- false-positive verification,
- reruns / failed branches,
- reconstruction time.

## 5. Negative results are first-class
NO-GO sonucu silinmez. Killed family, falsifier ve neden tekrar denenmemesi gerektiği decision log'a yazılır.

## 6. Tool choice
- Küçük/orta hesap: local Python/Numba/compiled code.
- Uzun ömürlü authority: GitHub.
- GitHub Actions ancak reproducibility veya matrix test gerçekten değer katıyorsa.
- Büyük yeniden üretilebilir scratch/cache: repo dışında; manifest + build recipe + hash repo içinde.

## 7. Claims
Aşağıdaki ifadeler gate olmadan kullanılmaz:
- “100× random compression achieved”
- “key recovery attack”
- “alpha reduction demonstrated”
- “full-round relevance demonstrated”

## 8. Milestone closure contract
Her milestone sonunda minimum paket:
- source,
- tests,
- frozen plan/split,
- result summary,
- decision JSON/MD,
- manifest/hashes,
- continuity update.
