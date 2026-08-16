# FDS_COMPUTE_POLICY

## Amaç

Hesabın nerede çalıştığı araştırma claim'inin parçası değildir. Doğru araç; en hızlı, en ucuz ve en yeniden üretilebilir olan araçtır. İnsanlar sırf “CI'da koştu” diye matematiğin daha doğru olduğunu sanabiliyor; bilgisayarlar bu kadar törensel değil.

## Local compute seç

Şunlarda local/container tercih edilir:
- hızlı exploratory hesaplar,
- Numba/Python/Rust prototipleri,
- küçük/orta Monte Carlo,
- iterative debugging,
- büyük geçici feature cache,
- tek makinede dakikalar-saatler içinde biten deney.

Local sonuç admitted olacaksa repo'ya şu bilgiler döner:
- exact source/runner,
- environment/version notu,
- seed/split,
- result JSON/CSV summary,
- runtime/RSS/storage,
- hash/manifest,
- tests.

## GitHub compute seç

Şunlarda GitHub Actions veya repo-native compute tercih edilir:
- OS/version matrix,
- temiz checkout reproducibility,
- uzun süre korunması gereken authority testleri,
- başka agentların bağımsız tekrar etmesi gereken certification,
- local environment'ın sonucu etkileyebileceği toolchain işleri.

## Large scratch policy

Yeniden üretilebilir büyük cache/model/intermediate için:
1. mümkünse repo dışında tut;
2. generator script commit et;
3. byte count + SHA-256 kaydet;
4. gerekli input/version/seed kaydet;
5. gerçekten authority artifact ise GitHub artifact/release/LFS benzeri uygun taşıma yolu kullan.

## Decision rule

`expected wall time + reproducibility need + data size + environment sensitivity` birlikte değerlendirilir. Daha kolay yol seçilebilir. Ancak milestone closure her durumda GitHub canonical state'ini günceller.
