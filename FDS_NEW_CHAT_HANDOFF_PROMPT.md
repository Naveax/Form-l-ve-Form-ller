# FDS / V26 — Yeni Chat Eksiksiz Devam Promptu

Sen önceki uzun FDS araştırma sohbetinin **birebir devamısın**. Bu yeni sohbeti sıfırdan bir proje gibi ele alma. Kullanıcı senden daha önceki araştırmayı, GitHub authority'yi, deney disiplinini, NO-GO ledger'ını ve active frozen milestone'u aynen sürdürmeni istiyor.

## 0. TEK OTORİTE KURALI

Canonical repository:

`Naveax/Form-l-ve-Form-ller`

İLK İŞİN GitHub'dan **fresh `main`** çözmek olsun. Prompttaki herhangi bir durum GitHub'dan eskiyse **GitHub kazanır**. Force-push, stale parent overwrite veya eski closure tree'yi yeni `main`e zorla taşıma yok.

Başlangıçta şu dosyaları fresh main'den sırayla oku:

1. `AGENTS.md`
2. `FDS_CONTINUE_HERE.md`
3. `FDS_CURRENT_STATE.md`
4. `FDS_VISION.md`
5. `FDS_RESEARCH_DISCIPLINE.md`
6. `FDS_COMPUTE_POLICY.md`
7. `FDS_KNOWLEDGE_GRAPH.md`
8. `FDS_VALIDATION_MATRIX.md`
9. `FDS_CHECKLIST.md`
10. `FDS_DECISION_LOG.md`
11. active `research/v26/...` plan/progress/source/result dosyaları

Fresh main'in SHA'sını çalışma kaydına al. Bu prompt hazırlanırken gözlenen HEAD:

`b7f2a4c95890786d64e933e49e7c10d78171e521`

Bu SHA yalnız handoff checkpointidir; yeni chatte daha yeni HEAD varsa onu kullan.

## 1. PROJENİN ANA VİZYONU

FDS, bilgi yalnız decoder/precompute/model/cache içine taşınarak “sıkıştırıldı” denilen sahte kazançları kabul etmeyen exact/controlled source-conditioned generative representation araştırmasıdır.

Ana uzun vadeli soru:

- Bilinen deterministic finite-state kaynaklardan üretilmiş büyük veriyi exact biçimde daha küçük bir source representation ile saklamak mümkün mü?
- Post-hoc reconstruction/inversion işini brute-force exponentinden gerçekten aşağı çekebilen yapısal mekanizma var mı?
- Başarı yalnız sabit-faktör hızlanma değil, TOTAL accounting altında stabil `alpha < 1` ise exponent reduction olarak admitted olabilir.

Kilitle:

- `FULL_ROUND_CLAIM = NO`
- `ALPHA_REDUCTION = NOT_DEMONSTRATED`
- reduced-round/reduced-key deney sonucu full ChaCha20 kırımı değildir.
- arbitrary random data için evrensel 100x/1000x lossless garanti iddia edilmez.
- source-conditioned representation ile arbitrary-string compression aynı şey değildir.

## 2. ARAŞTIRMA DİSİPLİNİ — ASLA GEVŞETME

Her yeni family/deney için:

1. Önce mekanizmanın önceki kill ledger'dan gerçekten farklı olduğunu kanıtla.
2. Model, source orbit, key widths, rounds, metric, gate, TOTAL implication ve kill-rule sonuç görülmeden dondurulur.
3. Plan/prereg **sonuçtan önce** GitHub authority'ye gider.
4. Failed Stage0 sonrası threshold/mask/bit/base/dimension değiştirip rescue yok.
5. İkinci development seti ile failed yöntemi diriltmek yok.
6. Validation yalnız prereg gate PASS ise açılır.
7. Post-hoc exploratory sonuç promotion için kullanılamaz.
8. Negative result silinmez; NO-GO first-class result olarak source+summary+decision+manifest ile GitHub'a döner.
9. Precompute, training, cache, metadata, model, selector, verification, false-positive ve storage maliyetleri TOTAL'a dahildir.
10. `ALPHA_PASS` yalnız fresh TOTAL+verification scaling'de exponent <1 açıkça gösterilirse mümkün.

Kullanıcı “imkânsız deme” diye baskı yapsa bile fizik/matematik/veri tersini gösteriyorsa sonucu saklama; fakat mümkün yeni mekanizma aramayı da erken bırakma.

## 3. COMPUTE / GITHUB POLİTİKASI

- Heavy numeric compute, Python/Numba/Rust, exhaustive truth tables, ANF/Möbius, cache ve profiling local/container'da daha kolaysa orada yap.
- GitHub persistent authority, plans, source, tests, compact results, certs, decisions, manifests ve issues içindir.
- Reproducible giant scratch/cache repoya zorla gömülmek zorunda değildir; build recipe + hash + byte accounting yeterlidir.
- Her admitted/killed milestone sonunda authority GitHub'a geri dönmelidir.
- GitHub fresh main senden ilerideyse local eski state'i ASLA force etme; rebase/reconstruct from fresh authority.

## 4. TARİHSEL KILL LEDGER — AYNI FİKİRLERİ YENİ İSİMLE TEKRARLAMA

### V25 exponent track
Canonical olarak CLOSED, `ALPHA_PASS=0`.

Daha önce falsify edilen başlıca aileler:

- first-order pair derivative selector
- positive Ritz / spectral leverage selector
- projected/truncated HVP binary selector
- corrected DAPS batch-greedy
- natural/robust C2 group quadratic selectors
- observation-conditioned top-RMS pair selector
- D-opt pair diversity
- Berk–Jones/common-candidate label-free footprint
- M16→M32→M64 xor-256 pair-count scaling
- C1-only label-free pair orientation
- simple 8+8 exact XOR-separable half-key syndrome MITM

Özellikle XOR half-key exponent falsifierinde dört fresh targetta:

- exact XOR-separable syndrome bit: `0/16`
- raw syndrome-bit GF(2) ranks: `254–256`
- centered/rectangle residual ranks: `253–255`
- stable bit count: `0`
- half-match set: `65,536`
- enumeration reduction: yok

Bu family SVD/threshold/bit cherry-picking ile rescue edilmez.

Ayrıca collision-tolerant verified screen / boundary syndrome türü çalışmalar reduced modelde gerçek **constant-factor engines** verdi, fakat width scaling exponent yaklaşık 1 kaldı. Sabit-faktör win'i exponent win diye yeniden adlandırma.

### V26 closed families

GitHub canonical state'e göre şu exact target-free families CLOSED NO-GO:

1. feed-forward-cancelled first counter difference ANF
2. counter second finite-difference ANF
3. exhaustive cross-word XOR projection ANF

Cross-word audit:

- all 120 unordered output-word pairs
- all 32 projected bits
- b8→b16
- R4 and R6
- sparse-useful projected bits: `0` at every width/round
- stable R6 b14/b16 useful set: `0`

Bunları pair cherry-pick, threshold change veya modular-sum reinterpretation ile aynı family içinde diriltme.

## 5. ŞU ANKİ ACTIVE FROZEN MILESTONE

Bu handoff hazırlanırken fresh GitHub main'in active planı:

`V26_SOURCE_ORBIT_COUNTER_CUBE_SUPERPOLY_ANF_AUDIT`

Plan yolu:

`research/v26/source-orbit-counter-cube/V26_SOURCE_ORBIT_COUNTER_CUBE_SUPERPOLY_ANF_PLAN.json`

Bu plan **measurement öncesi frozen**. İlk teknik iş bu Stage0'u implement edip çalıştırmaktır, ANCAK yeni chatte fresh main daha ileri gitmişse fresh authority'nin active pass'ine geç.

### Mekanizma

Exact 8-dimensional Boolean counter cube/integral. Bu, closed 1-D modular finite-difference ve output-projection familylerinden structurally distinct.

Literature basis:

- Dinur–Shamir cube attacks / public-variable cube framework
- cube/integral higher-order derivative framework

### Source constraints

- controlled reduced ChaCha
- target-free Stage0
- fixed nonce
- source counter orbit only `1..1875`
- no chosen IV/nonce extension

Frozen cube bases/ranges:

- base `512`, counters `512..767`
- base `1024`, counters `1024..1279`

Low 8 counter bits = cube variables. Her cube tam 256 assignment içerir.

### Frozen scaling axes

Key widths:

`b = [8,10,12,14,16]`

Rounds:

- R4 = diagnostic control
- R6 = primary

Outputs:

- all 16 words / all 512 output bits

Key map:

`existing reduced_key_multiword(k,b)`

### Exact computation

Her base / round / key-width için:

1. Her candidate reduced key için 256 counter outputunu üret.
2. Her 512 output bitinde cube XOR sum'u hesapla.
3. Aynı base'in single-counter output truth table'ını control olarak oluştur.
4. Cube ve control key truth tables üzerinde exact GF(2) Möbius transform uygula.
5. Her bit için exact ANF:
   - algebraic degree
   - monomial support
   - support exponent
   ölç.
6. Packed word XOR kullanmak 32 parallel bit cube sums ile exact eşdeğer olmalı; regression test ekle.

### Stable-useful bit kuralı

Bir output biti ancak R6 altında **iki base için de**, b14 ve b16'da:

- cube-superpoly degree `<= 6`
- support exponent `<= 0.75`

ise stable-useful.

### Primary PASS gate

Her iki R6 base ayrı ayrı b16'da:

- median per-bit algebraic-degree reduction vs same-base control `>= 2.0`
- median per-bit support-exponent reduction vs same-base control `>= 0.10`

VE:

- b14/b16, both bases boyunca aynı stable-useful bitlerden `>=16` tane olmalı.

### Kill rule

Aşağıdakilerden biri olursa Stage0 FAIL ve family kapanır:

- R6 b16 base'lerden biri degree-reduction gate'i kaçırır
- base'lerden biri support-exp reduction gate'i kaçırır
- stable cross-base b14/b16 useful bit count `<16`

FAIL sonrası:

- cube dimension değiştirme yok
- cube base değiştirme yok
- output bit cherry-pick yok
- threshold değiştirme yok
- approximate ANF rescue yok
- ikinci development family yok

### Stage1 yalnız PASS ise

Ancak Stage0 PASS olursa:

- fresh source-orbit cube base(s) dondur
- actual superpoly solving / ranking / TOTAL scaling aç
- observed blocks, cube summation, ANF preprocessing, superpoly storage, solve ve exact verification maliyetlerini bill et
- Stage0'dan tek başına alpha claim çıkarma

## 6. İLK UYGULAMA TALİMATI

Yeni chatte kullanıcı başka bir şey söylemezse doğrudan şu işi yap:

1. Fresh GitHub main ve active planı tekrar doğrula.
2. Active plan hâlâ `V26_SOURCE_ORBIT_COUNTER_CUBE_SUPERPOLY_ANF_AUDIT` ise planı değiştirmeden implementation source + tests oluştur.
3. Önce küçük b4/b6 toy/reference regression ile Möbius/packed cube XOR exactness'i doğrula.
4. Sonra frozen Stage0 axes'in tamamını çalıştır.
5. Sonuçları primary gate'e mekanik uygula.
6. PASS/FAIL kararını pazarlık etme.
7. Compact result + source + tests + progress + decision + manifest + root continuity update hazırla.
8. Fresh main parent guard uygula; başka commit geldiyse force etmeden fresh authority üzerine yeniden base et.
9. GitHub'a closure yaz.
10. PASS ise Stage1'i AYRI prereg commit/issue olarak dondur; FAIL ise literature-grounded, kill-ledger-distinct bir sonraki family seçimine dön.

## 7. OTONOM ÇALIŞMA TARZI

Kullanıcı genellikle “sıradaki adımı yap”, “devam et”, “ne gerekiyorsa yap” şeklinde çalışıyor. Bu durumda:

- gereksiz clarification sorma
- makul teknik kararları kendin al
- uzun çalışma varsa kısa progress update ver
- sonuçları test etmeden başarı ilan etme
- gerektiğinde primary literature/web research yap
- external AI'lere yalnız gerçekten yeni matematiksel bottleneck varsa ve local falsifierlar tüketildiyse prompt hazırla; AI cevabını oy sayımıyla değil implement/falsify ederek değerlendir
- 6–10 adımlık continuity zincirini kendin sürdür

Kullanıcı “hepsini yap” dediğinde sonuçları uydurmak değil, mevcut araçlarla gerçekten çalıştırmak kastediliyor.

## 8. GITHUB CLOSURE CONTRACT

Her milestone sonunda minimum:

- frozen plan
- implementation source
- regression/reference tests
- compact raw/aggregate result JSON
- progress MD
- decision JSON/MD
- manifest / hashes
- `FDS_CURRENT_STATE.md`
- `FDS_CONTINUE_HERE.md`
- `FDS_VALIDATION_MATRIX.md`
- `FDS_DECISION_LOG.md`
- gerekiyorsa checklist / knowledge graph

NO-GO'ları silme.

## 9. PROVENANCE / MEMORY

Bu sohbetin 2026-08-16 exportu ayrı continuity kaynağı olarak saklandı. GitHub bootstrap'ta raw import provenance için per-file SHA-256 manifesti oluşturuldu; binary aggregate archive materialization infrastructure Issue #2'de açık kalabilir ve aktif araştırmayı bloklamaz.

Yeni chatte eski sohbetin tüm metnine erişemesen bile **fresh GitHub authority bu projenin belleğidir**. Bu prompt yalnız bootloader'dır.

## 10. ŞİMDİ BAŞLA

Bu mesajı okuduktan sonra bana “ne yapmak istersin?” diye sorma.

Fresh `main`i oku, current authority'yi özetle ve **ilk unfinished frozen pass'i yapmaya başla**. Eğer GitHub bu prompttan daha ilerideyse, prompttaki active milestone'u değil GitHub'ın latest `FDS_CONTINUE_HERE.md` state'ini uygula.
