# FDS V25 — Additive Counter-Distance Pair Geometry

## Verdict
`NO_GO_PUBLIC_ADDITIVE_DISTANCE`

Frozen family: 12 b=10 targets, three grouped folds, 16 pair budget, four pairs each at additive distances d=1,64,256,512.

All primary gates failed: selected mean rank percentile **0.49379** (>=0.55 required); median enrichment vs all **-0.02447** (>=+0.05); positive targets **5/12** (>=8); median enrichment vs d256 **+0.00868** (>=+0.02). Secondary fixed ridge pooled Spearman **0.03128**.

Class means are diagnostic only: d1 0.55666, d64 0.49204, d256 0.48951, d512 0.50813. d1 is post-hoc and cannot resurrect the family.

Accounting: total target build wall **273.75 s**, median **22.67 s**, max peak RSS **526 MiB**. Recovered C1 scratch used 69 reproducible process-isolated shards.
