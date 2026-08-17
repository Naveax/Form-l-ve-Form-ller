# FDS_CONTINUE_HERE

**Admitted one-QR exact bound:** `W_1<=38.768184324776925...<39` for all 4096 physical fixed-mask cases.  
**Admitted double-round structural ledgers:** `W_2_topo<=236`, `W_2_construct<=95`, `W_2_repr<=86+log2(3)=87.58496250072116...`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes remain missing.  
**Active work:** mathematics-first coefficient-specific Schmidt structure beyond the new nonlinear-support W2 bound.

Code is only a calculator/falsifier. New finite claims require clean-checkout execution.

## One-QR facts to preserve

- corrected exact I9 support range: `117..218`;
- support indicator rank across 64 left masks: `64`;
- old support216/rank12 selector line is revoked;
- full-family exact global peak: `218*2^31`;
- left fixed-mask interface rank:48;
- six-left-mask complete coefficient family rank:64, TT profile `2,4,8,16,32,64`;
- physical right rank: `11..38`;
- parent rank: `5..27`;
- right doubled hull:162;
- current dense-work proxy for the RL218 width tree is `4.0160678967x` worse than the rank27 source topology;
- `ALPHA_PASS=0`.

## Gram-image semantics

For right map `R_m`, `G_m=R_mR_m^T`.

Exact rank-space structure:

- right Gram family span145;
- prefix family140;
- closure family16;
- parent Gram-image family `L G_m` span124;
- its row directions span47;
- natural 12-control Gram-image selector TT profile `2,4,8,16,32,64,128,119,196,136,143,124`.

These are **not** full right-external coefficient amplitudes. Do not feed the 124/U47 Gram-image family into a subsequent QR as if it were the single-copy coefficient tensor. True composition must retain `R_m` with its 24 external mask legs or an exactly equivalent factorization.

## Double-round exact structure

q138 inverse double round has one active final column QR `(0,4,8,12)` and four diagonal QRs.

### Topology

Corrected open-boundary common-prefix bound:

`W_2_topo<=236`.

The historical 252 double-counted offset16 perfect-matching edges.

### Constructive structural bound

Generate each fixed-input/single-output diagonal leaf as an exact 32-bit vector, factor the four vectors hierarchically on the frozen bit tree, and leave the central QR in its reduced graph form:

`W_2_construct<=95`.

Leaf generation peak is at most44; dense leaf vector size exponent32.

### Exact representation existence: nonlinear support improvement

The old generic Hilbert-envelope result `W_2_repr<=88` is superseded.

On the two unique critical 11|21 central partitions, modular-addition MSB conservation plus the exact nonlinear support rule `sigma=0 => u=v=w` removes physical boundary rows.

For

`S1={0,1,2,3,4,5,12,13,14,15,16}`

the q138 carry geometry forces

`C15=0 => C16=D0`.

Only 6 of the 8 triples `(C15,C16,D0)` are support-compatible, so

`rank_center(S1) <= 3*2^42`.

For

`S2={6,7,8,9,10,11,27,28,29,30,31}`

j1 MSB conservation permits only 342 of the 1024 top-pattern pairs `(A27..31,D27..31)`, hence

`rank_center(S2) <= 342*2^34`.

Reinserting these exact support-rank bounds into the frozen HT tree gives

`D_max <= 3*2^86`,

therefore

`W_2_repr <= 86+log2(3) = 87.58496250072116... <88`.

The other tree clusters were already at exponent at most80. Clean GitHub Actions run `32017394330` passes both the historical HT88 dependency and the new verifier.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DOUBLE_ROUND_SUPPORT87_THEOREM.md`;
- `scripts/verify_v26_q138_double_round_support87.py`;
- `.github/workflows/double-round-support87.yml`.

This is still representation existence. A central support/Schmidt-factor generation procedure staying below `87.5849...` is not yet certified, so the constructive ledger remains95.

## Generic-envelope optimality / falsifiers

The old 88 generic-envelope method is exhausted, but the true tensor is now known to beat it through nonlinear support.

Retain these scoped facts:

1. exact central cardinality MILPs for k=11..16 give graph boundaries `51,52,55,54,55,56`;
2. refined central minimal-TT terminal cuts on the old critical partitions are `44,44,44`, each using exactly 44 binary cut indices and no ternary cut bond;
3. pure GF(2) projection codimension on the two unique 44-bit boundaries is `0,0`;
4. reduced generic leaf terminal cuts are `11,11,11`;
5. fixed-input leaf full-rank witnesses exist for every output position and critical partition for some outer masks, so no uniform leaf exponent below11 theorem is possible.

Thus the new gain is specifically nonlinear Walsh support, not topology or linear parity.

## Multi-double-round representation law

For fixed outer input masks, the current common-tree law is

- special one-double-round bound: `W_repr(1)<=86+log2(3)`;
- for `d>=2`: `W_repr(d)<=520d-340`.

The d>=2 law uses a separate common bit tree whose fully-open QR bound is65. The new S1/S2 support theorem does not automatically change those different maximizing clusters. Keep `520d-340` until a direct support analysis of that common tree is proved.

Verified values of the current law: d2=700, d3=1220, d4=1740, d5=2260, d6=2780, d7=3300, d8=3820, d9=4340.

This is structural representation/message width only, not arithmetic work.

## First unfinished mathematical pass

Continue in this order.

1. Try to strengthen the central nonlinear-support bound on `S1`. The currently proved local restriction is exactly `C15=0 => C16=D0`; small j1 boundary-block checks have not produced a second uniform rule.
2. Search for signed coefficient Schmidt deficiency below the support-row bound `3*2^42` on S1. Support count is only an upper bound on rank.
3. In parallel, look for a joint central×leaf factorization on the two critical bipartitions. Independent central and four-leaf rank multiplication may still overcount shared sectors.
4. Do not assume a concrete outer 128-bit leaf-input mask. Repo authority does not freeze one. Source-specific leaf compression is inadmissible until such a mask is specified; only uniform/parametric leaf theorems are valid.
5. If a smaller central or joint rank is proved, re-evaluate every node of the complete HT tree before changing `W_2_repr`.
6. Separately test whether analogous nonlinear-support restrictions reduce the maximizing 11-site cluster of the `520d-340` common tree. Do not transfer the S1/S2 rule by analogy.
7. Keep representation width, constructive factor-generation peak, storage, arithmetic work and error as separate ledgers.

## Storage/work warning

Generic exact HT leaf factorization does not compress arbitrary leaf storage: one leaf uses 4,308,611,904 scalar slots in the frozen generic tree, slightly above dense `2^32`. The separator gain is geometric, not generic storage compression.

A practical or arithmetic-work gain therefore requires coefficient-specific leaf/central structure, not merely generic Hilbert-rank factorization.

## Approximation rule

All current admitted reductions are exact, `epsilon=0`. Do not activate epsilon-rank while exact central-support/rank and joint-factorization routes remain open.

Still not admitted: practical evaluator at the formal peaks, arithmetic-work reduction, ranking gain, `alpha<1`, or full-round relevance.
