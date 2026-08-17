# FDS_CONTINUE_HERE

**Admitted one-QR exact bound:** `W_1<=38.768184324776925...<39` for all 4096 physical fixed-mask cases.  
**Admitted double-round structural ledgers:** `W_2_topo<=236`, `W_2_construct<=95`, `W_2_repr<=79+log2(87)=85.44294349584872...`.  
**Measured-execution blocker:** exact recovered V25 trail-DAC runtime bytes remain missing.  
**Active work:** exact signed central-rank compression and constructive realization of the new W2 representation bound.

Code is only a calculator/falsifier. New finite claims require clean-checkout execution.

## One-QR facts to preserve

- corrected exact I9 support range `117..218`;
- support indicator rank across 64 left masks64;
- old support216/rank12 selector line is revoked;
- full-family exact global peak `218*2^31`;
- left fixed-mask interface rank48;
- six-left-mask complete coefficient family rank64, TT profile `2,4,8,16,32,64`;
- physical right rank `11..38`;
- parent rank `5..27`;
- right doubled hull162;
- RL218 width-tree dense-work proxy is `4.0160678967x` worse than the rank27 source topology;
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

q138 inverse double round has one active final column QR and four diagonal predecessor QRs.

### Topology

`W_2_topo<=236`.

### Constructive structural bound

Central QR remains in exact reduced graph form; four fixed-input/single-output leaves are exact 32-bit vectors factored hierarchically:

`W_2_construct<=95`.

Leaf generation peak is at most44; dense leaf vector size exponent32.

### Exact representation existence: signed rank bound

Use the frozen HT tree with the critical central partitions

`S1={0,1,2,3,4,5,12,13,14,15,16}`

and

`S2={6,7,8,9,10,11,27,28,29,30,31}`.

For q138, fixed central j4 output `2^3` gives `msb(u4)=msb(v4)=3` and then `msb(u3)=msb(v3)=27`.

S1 exact signed blocks:

1. physical row bits `A0,B0,C15,C16,D0`, with all central occurrences closed inside j1 bit0 and j2 bits15,16: exact rank16;
2. physical row bits `A13..16,B13..16,D13..16,C0`, with D13..16 second occurrences closed by j2 bits29..31 and bit0: exact rank2784.

These blocks use disjoint physical row-variable sets. Passing the other26 physical S1 row bits gives

`rank_center(S1) <=16*2784*2^26 =87*2^35`.

For S2, exact j1 bits31..27 ranks by D-top sector are two rank32 sectors and thirty rank64 sectors. The safe sector-channel sum is

`1984=31*2^6`,

so

`rank_center(S2) <=31*2^35`.

With four generic diagonal leaf Hilbert exponents44, the frozen HT tree gives

- S1 message `<=87*2^79`;
- S2 message `<=31*2^79`;
- every noncritical node remains at generic exponent at most80.

Therefore

`W_2_repr <=79+log2(87)=85.44294349584872...`.

Clean Actions run `32019335785` is `success`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_DOUBLE_ROUND_SIGNED85_THEOREM.md`;
- `scripts/verify_v26_q138_double_round_signed85.py`;
- `.github/workflows/double-round-signed85.yml`.

This is representation existence only. Constructive generation remains95.

## Scoped falsifiers / cautions

- old generic central cardinality MILP boundaries k11..16: `51,52,55,54,55,56`;
- refined central minimal-TT terminal cuts: `44,44,44`, each exactly44 binary cut indices and no ternary cut bond;
- pure GF(2) critical-boundary codimension `0,0`;
- generic leaf terminal-cut exponent11.

Do **not** cite the historical coefficient-specific leaf full-rank witness as clean authority. Workflow run `32011941759` was terminated with exit143 during the heavy witness step. The HT88 dependency passed, but the witness calculation did not finish.

## Multi-double-round representation law

For fixed outer input masks:

- special d=1: `W_repr(1)<=79+log2(87)`;
- for `d>=2`: `W_repr(d)<=520d-340`.

Current exact common-tree values: d2=700, d3=1220, d4=1740, d5=2260, d6=2780, d7=3300, d8=3820, d9=4340.

The d>=2 tree uses different maximizing clusters. Do not transfer the S1/S2 signed rules by analogy. A support-aware search restricted to the old HT shape did not beat d2=700; that is scoped negative evidence only.

## First unfinished mathematical pass

Continue in this order.

1. Strengthen the S1 exact signed central rank below `87*2^35`. Any new rank factor must either include every occurrence of each physical row variable it mixes or keep multiply-used variables explicitly as sector labels.
2. Try enlarging the current occurrence-closed S1 blocks only while the exact rank ratio keeps improving. Previously rejected local factors that forgot second D occurrences must remain rejected.
3. Build an explicit factor-generation/contraction realization of the signed S1/S2 factors and seek `W_2_construct<95`. Do not replace the constructive ledger by the representation ledger without this certificate.
4. Search for a joint central×leaf factorization on S1/S2; independent central-rank × four-leaf Hilbert-rank multiplication may overcount shared sectors.
5. Revalidate coefficient-specific leaf ranks only with a completed clean computation. Repo authority does not freeze a concrete outer128 leaf-input mask, so do not assume zero masks.
6. Derive analogous exact signed/nonlinear support restrictions for the different maximizing 11-site cluster of the `520d-340` common tree.
7. Every improvement must be reinserted into every node of the complete tree before changing an admitted width.
8. Keep representation width, constructive peak, storage, arithmetic work and error as separate ledgers.

## Approximation rule

All current admitted reductions are exact, `epsilon=0`. Do not activate epsilon-rank while exact signed/support/joint-factorization routes remain open.

Still not admitted: practical evaluator at formal peaks, arithmetic-work reduction, ranking gain, `alpha<1`, or full-round relevance.
