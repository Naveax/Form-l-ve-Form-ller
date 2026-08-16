# RAW_IMPORT_STATUS

## Captured source set

2026-08-16 bootstrap anında current conversation `/mnt/data` mountunda:

- **94 file**
- **4,341,402 total bytes**
- local verified ZIP: **1,566,535 bytes**
- ZIP SHA-256: `b21a45f80d7af4fdf745d490daf8c100d620e40b89dc6b49a158a8c0f4263863`

Tam per-file filename/size/SHA-256 listesi:

`RAW_IMPORT_FULL_MANIFEST.json`

## GitHub'a taşınanlar

- Canonical continuity/vision/discipline/checklist/current-state dokümanları
- Source registry
- Validation matrix
- Agent continuation contract
- Compute policy
- Full 94-file cryptographic manifest
- Compact raw archive authority record
- Verifier scripts

## Git object olarak bulunmayan bulk bytes

Current ChatGPT GitHub connector write API'si UTF-8 content/blob yazabiliyor ancak bu oturumdaki local `/mnt/data` binary dosyasını doğrudan file-parameter olarak GitHub blob'a aktarabilen bir köprü sunmuyor. Local ortamda authenticated `gh` credentialı da bulunmadı.

Bu nedenle local verified `raw-import-2026-08-16.zip` **bu committe Git object değildir**. Bu kasıtlı olarak açık yazılmıştır; varmış gibi sahte authority oluşturulmamıştır.

## Re-materialization contract

Historical raw kaynak yeniden erişilebilir olduğunda:

```bash
python scripts/verify_raw_import.py --source-dir /path/to/rematerialized/files
# veya
python scripts/verify_raw_import.py --archive /path/to/raw-import-2026-08-16.zip
```

çıktısı `ok: true` olmadan raw history identical kabul edilmez.

## Research authority implication

Current araştırmanın canonical authority'si root continuity + measured result/source/test/cert zinciridir. Ham sohbet dökümleri **historical evidence** sınıfındadır; current measured authority ile çelişirse otomatik olarak kazanmaz.
