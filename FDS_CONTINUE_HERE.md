# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**d=1 exact representation:** `W_repr(1)<=73+log2(3829)=84.90275194485017...`.  
**d=1 coefficient-aware factor generation:** same `84.90275194485017...`.  
**d=1 coefficient-blind static:** `95`.  
**d>=2:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**ALPHA_PASS=0**.

All admitted reductions are exact (`epsilon=0`). Code is calculator/falsifier/certificate machinery; finite computational claims require clean-checkout execution.

## Center authority — unchanged

`S1={0,1,2,3,4,5,12,13,14,15,16}`; all44 S1 physical bits are occurrence-closed.

`rank_center(S1)<=3829*2^29`.

D16 per-high-prefix decomposition:

`26712n common +1960n private0 +1960n private1`, `n=2^22`.

No arithmetic-work reduction is admitted.

## Current predecessor-leaf dyadic envelopes

Natural four-leaf scale: `2^426`.

A `[1,41,564,1761,2048,...]`

B `[36,748,2048,2048,...]`

C `[84,936,2048,2048,...]`

D `[1,20,173,838,1958,2048,...]`

The older A/D chains `[3,219,565,...]` and `[3,207,364,...]` remain valid historical bounds but are superseded. The older B/C second-lift bounds812/972 are also superseded by the clean uniform half-state result below.

## A/D exact-signed low layers

Clean run `34109587357` remains the A/D low-layer authority.

The always-present carry equations give a selected-side affine map `beta_keep=Lx+Hz+c`. Sectors sharing a carry offset share one selected matrix row/column, so the exact signed aggregate over one offset class has rational rank at most1. The signed aggregate is a valid binary lift and removes that valuation family from later residuals.

Certified prefixes:

- A `[1,41,564,2048,2048]`;
- D `[1,20,173,838,1958]`.

A direct-e3 clean run `34109587313` additionally proves

`rank_Q(K_A,3^direct)<=1761<2048`,

so canonical A is

`[1,41,564,1761,2048,...]`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_AD_UNIVERSAL_CARRY_OFFSET_EXACT_SIGNED_LIFTS.md`;
- `scripts/verify_v26_q138_ad_universal_carry_offset_exact_signed_lifts.py`;
- `research/v26/recovered-bit-puncturing-dac/V26_Q138_PREDECESSOR_LEAF_A_DIRECT_E3_ROW_UNION1761.md`;
- `scripts/verify_v26_q138_predecessor_leaf_a_direct_e3_row_union1761.py`.

## B/C uniform second-lift authority — 748 / 936

PR104 clean authority run `34134200886` replaces812/972 by the uniform bounds

`rank(K_B,1)<=748`,

`rank(K_C,1)<=936`.

The construction avoids enumerating the123-dimensional half-active predecessor affine space. For the four common-support half sectors it combines predecessor-null directions with the21 right-beta variables and takes the exact linear image seen by support syndrome plus four left phase frequencies.

For both B and C:

- combined linear-state rank =18;
- linear states =`2^18`;
- support-feasible states =131072;
- all16 scalar phase patterns are allowed at every feasible state, a safe superset of the true quadratic scalar image;
- generated relaxed state/scalar pairs =2,097,152;
- resulting uniform relaxed half span dimension <=144.

The relaxed half span is explicitly verified inside the previously admitted uniform half span. Combining with grouped-e0 and support-only Walsh spaces gives:

- B: grouped/half union dimension<=272, support-only dimension668, exact ZZ quotient<=80, total `668+80=748`;
- C: grouped/half union dimension<=388, support-only dimension788, exact ZZ quotient<=148, total `788+148=936`.

These are uniform second-lift upper bounds, not optimality theorems. They do not by themselves lower complete leaf rank or `W_repr(1)`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_BC_HALF_UNIFORM_LINEAR_STATE_RELAXED_SCALAR_PROBE.md`;
- `scripts/probe_v26_q138_bc_half_uniform_linear_state_relaxed_scalar.py`;
- clean run `34134200886`.

## B/C direct-e1 and direct-e2 obstruction record

Simple sectorwise and same-support routes are closed.

Direct-e1:

- clean `34109587338`: an individually reachable signed sector has exact rational rank2048 for both B and C;
- clean `34109587395`: identical-support whole-sector exact cancellation is absent for both B and C;
- clean `34107536167`: complete direct-e1 B aggregate reaches `rank_F3=2048`, hence `rank_Q=2048`;
- clean `34107785435`: a deterministic 12D C right-beta subcube is exactly zero over Z;
- clean `34109587430`: the ninth tested escape coset drives the complete C aggregate to `rank_F3=2048`, hence `rank_Q=2048`.

Direct-e2:

- clean `32228843165`: an individually reachable direct-e2 signed sector has exact rational rank2048 for both B and C.

Therefore B/C higher-residue progress must use aggregate cancellation across more structure, a different mod4/integer lift gauge, support/phase coupling, inherited-correction structure, complete-leaf compression, or a genuinely nonlocal/product theorem. Sectorwise rank-subadditivity is not enough.

The historical B direct-e2 support-only left-frequency envelope<=1796 remains structural information, but it is nowhere near the present k9 requirement and is not a complete B2 theorem.

## Current four-leaf convolution authority

PR105 clean authority run `34138576678` uses

A `[1,41,564,1761,2048,...]`,
B `[36,748,2048,2048,...]`,
C `[84,936,2048,2048,...]`,
D `[1,20,173,838,1958,2048,...]`.

Exact layer bounds through k9 are:

- k0 `3,024`
- k1 `280,992`
- k2 `11,542,464`
- k3 `275,107,184`
- k4 `4,247,967,584`
- k5 `45,333,814,960`
- k6 `348,805,355,152`
- k7 `1,987,672,008,800`
- k8 `8,552,484,855,456`
- k9 `28,420,855,930,176`

Hence

`sum(k0..k8)=10,938,830,935,616 < 2^44=17,592,186,044,416`,

with exact k8 margin

`6,653,355,108,800`.

But

`sum(k0..k9)=39,359,686,865,792`,

so k9 fails by

`21,767,500,821,376`.

Compared with the preceding812/972 arithmetic, cumulative k0..k9 improves by `2,244,581,425,280`.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_BC748_936_K9_CONVOLUTION.md`;
- `scripts/verify_v26_q138_bc748_936_k9_convolution.py`;
- clean run `34138576678`.

## Exact k9 B/C sensitivity authority

PR106 clean final-head run `34158461342` certifies the exact separated-leaf k0..k9 sensitivity when B3+/C3+ remain generic2048.

Let `b=B2`, `c=C2`. Then

`F(b,c)=15,892,005,024,640`

`      +5,260,847,048 b`

`      +3,952,624,408 c`

`      +1,096,366 b c`,

where `F=sum(k0..k9)` and the gate is `2^44`.

Exact thresholds:

- if `C2=0`, largest passing `B2` is323;
- if `B2=0`, largest passing `C2` is430;
- if `B2=C2=t`, largest passing `t` is180;
- if either side remains generic2048, the formal threshold for the other side is negative, so no nonnegative rank can pass;
- the historical B support-only1796 envelope still fails even with `C2=0`, by `7,748,300,278,432`.

If one structured construction gives the same cap `t` simultaneously on `B_i,C_i` for every `i=2..m`, while later entries remain2048, the exact largest passing common caps are:

- m=2 ->180
- m=3 ->568
- m=4 ->623
- m=5 ->630
- m=6 ->631
- m=7 ->631
- m=8 ->631
- m=9 ->631

Thus the practical arithmetic target is not necessarily “force B2/C2 near zero”. A repeated higher-residue mechanism around631 or below through the k9-relevant B/C residues would also pass the current separated-leaf gate.

These are upper-bound architecture thresholds only. They are not lower bounds on true ranks and not a complete-tail theorem.

Authority:

- `research/v26/recovered-bit-puncturing-dac/V26_Q138_K9_BC_INDEX2_SENSITIVITY.md`;
- `scripts/verify_v26_q138_k9_bc_index2_sensitivity.py`;
- clean final-head run `34158461342`.

## Higher-residue construction program

The strongest immediate algebraic follow-up is to ask whether the new uniform half correction carries low-complexity structure into the next dyadic bit.

A prepared probe branch reconstructs the PR104 relaxed half family as its own 144-dimensional GF(2) basis, verifies containment in grouped-e0, and uses that 144-vector basis as an explicit parity-lift gauge. For a lifted vector `y=XOR_i a_i v_i`, the induced next carry is

`XOR_{i<j, a_i=a_j=1} (v_i AND v_j)`.

Before any 2,097,152-state scan, the probe measures the pairwise-intersection hull

`span{v_i AND v_j : i<j}`.

A subgeneric hull would immediately give a uniform half-only inherited-carry upper span for this explicit gauge. Hull saturation would only reject that gauge/relaxation route, not prove intrinsic third-residue rank2048.

This probe is **not yet authority** and covers only half-correction inherited carry. It does not include grouped-e0 own lift carry, support-only lift carry, cross-carries among components, or complete B2/C2.

## Complete-leaf exact contraction program

The full S1 `2048 x 2048` leaf-minor route remains a numerical falsifier target.

Clean path-only run `34109391867` shows memory-capped row/column block plans can fit explicit intermediate ceilings, but selected paths use high multi-operand arity and astronomical total work. This is diagnostic only.

Immediate execution-design requirements remain:

1. preserve the admitted exact factor network and output block slicing;
2. slice selected internal binary indices exactly;
3. require binary/pairwise contraction;
4. account for every output block and internal slice in total work;
5. reduce modulo251 after every pairwise contraction with explicit integer-safety accounting;
6. execute only if the resulting total work is practical.

No numerical complete-leaf rank is admitted yet.

## Sharp blockers

1. **B/C higher residues:** produce a repeated or otherwise structured index2+ construction strong enough to approach the ~631 repeated-cap arithmetic scale, without relying on sectorwise low rank.
2. **Inherited carry / lift gauge:** determine whether the PR104 144-dimensional half family admits subgeneric next-carry structure, then assemble grouped-e0/support/cross-carry contributions.
3. **Complete dyadic tail:** k8 passes cleanly; k9 still fails by `21,767,500,821,376`; no complete-tail theorem exists.
4. **Product-level cancellation:** a nonlocal theorem could bypass separate residue-rank summation entirely.
5. **Practical exact contraction:** obtain a binary internal-slicing plan with controlled peak memory and total work before attempting the full S1 minor.
6. **Arithmetic work:** only after complete leaf control, fuse with central `common+private+private` geometry and count scalar work.

Still not admitted: lower complete `W_repr(1)`, practical evaluator, arithmetic-work improvement, ranking/search gain, `alpha<1`, or full-round relevance.
