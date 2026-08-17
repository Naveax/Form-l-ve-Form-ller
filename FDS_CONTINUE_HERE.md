# FDS_CONTINUE_HERE

**One-QR exact:** `W_1<=38.768184324776925...<39`.  
**d=1 exact representation:** `W_repr(1)<=73+log2(3829)=84.90275194485017...`.  
**d=1 coefficient-aware materialized-factor generation:** `W_factor-gen<=84.90275194485017...`.  
**d=1 coefficient-blind static method:** `W_static,blind=95`.  
**d>=2 law:** `W_repr(d)<=508.4979393937686...d-333.8951148057971...`.  
**ALPHA_PASS=0`.

All admitted reductions are exact, `epsilon=0`. Code is only calculator/falsifier; finite claims require clean-checkout execution.

## d=1 center authority

`S1={0,1,2,3,4,5,12,13,14,15,16}`. All44 physical S1 row bits are occurrence-closed.

Low23: `A0..5,B0..5,D0..5,C12..16`.  
High/gap21: `A12..16,B12..16,D12..16,C0..5`.

Exact center:

`rank_center(S1)<=3829*2^29=2,055,678,722,048`.

Clean run `32043410513`.

Generic predecessor-leaf exponent44 gives

`dim_factor<=3829*2^73`,

`W_repr(1)<=84.90275194485017...`.

Factor-generation message/storage constructivity matches this bound; clean `32043554316`. Arithmetic work is still not reduced.

Central work structure per high prefix remains

`26712n common +1960n private0 +1960n private1`, `n=2^22`.

Materialization, separate full low/high bases and generic monotone complement interleaving are scoped work NO-GAIN routes; clean runs `32044123499`, `32055881609`, `32056604049`.

## Predecessor-leaf dyadic authority

Leaf topology cut11 is exact on all frozen HT critical partitions; topology alone cannot beat `2^11=2048`.

The coefficient algebra does beat that generic count on low dyadic residues.

### Natural dyadic scales

Exact carry/sign descent gives

`L_A,L_D in 2^-92 Z`,

`L_B,L_C in 2^-121 Z`.

Clean `32058413111`.

### A/D residues

Define `M_A=2^92L_A`, `M_D=2^92L_D`.

First residue:

`rank_F2(M_A mod2)<=3`,

`rank_F2(M_D mod2)<=3`.

Clean `32058931522`.

Choose an integer rank<=3 first-layer lift and write

`M=M0+2M1`.

Second residue:

`rank_F2(M1_A mod2)<=309`,

`rank_F2(M1_D mod2)<=310`.

Clean `32062712987`.

Authority:

- `V26_Q138_PREDECESSOR_LEAF_AD_PARITY_RANK3.md`;
- `V26_Q138_PREDECESSOR_LEAF_AD_SECOND_DYADIC_RANK310.md`.

### B/C first residue

Define `M_B=2^121L_B`, `M_C=2^121L_C`.

Exact carry-sector quotient-matroid, canonical affine cancellation and sign analysis gives

`rank_F2(M_B mod2)<=1052`,

`rank_F2(M_C mod2)<=1160`.

Both are strictly below2048.

Clean `32063042288`.

Authority:

- `V26_Q138_PREDECESSOR_LEAF_BC_FIRST_DYADIC_RANK1160.md`.

These are residue ranks, not full rational leaf Schmidt ranks.

## Exact four-leaf dyadic layers

A GF(2) residue factorization lifts to an integer rational-low-rank layer with an even residual. Thus the residue bounds above give exact dyadic layers.

Natural four-leaf scaling is `2^426`.

### Layer0

Per-leaf ranks A3, B1052, C1160, D3:

`r0<=10,982,880`, exponent `23.38875308074955...`.

Attach center:

complete-S1 layer0 exponent `64.2915050255997...`.

Clean `32063409809`.

### Layer1

Using A/D second residue309/310 and universal2048 for unresolved B/C second residues:

`r1<=2,306,905,824`.

First two leaf layers cumulative:

`2,317,888,704`, exponent `31.110164149389277...`.

Clean `32063572894`.

### Generic fallback prefix k0..k4

For every still-unresolved leaf residue use only the universal row cap2048. Four-leaf product layer bounds become

- k0 `10,982,880`;
- k1 `2,306,905,824`;
- k2 `140,380,802,112`;
- k3 `2,067,939,590,144`;
- k4 `13,446,096,486,400`;
- k5 `49,193,897,820,160`.

Prefix k0..k4:

`15,656,734,767,360`.

Old generic four-leaf budget:

`2^44=17,592,186,044,416`.

Remaining leaf tail budget:

`1,935,451,277,056`.

Attach center: k0..k4 complete-S1 prefix exponent

`84.73460054643513...`,

which is only `0.16815139841503...` bits below the current full-factor bound84.90275194485017.

Clean prefix-gate run `32063775688`.

Authority:

- `V26_Q138_FOUR_LEAF_FIRST_DYADIC_STAR_LAYER.md`;
- `V26_Q138_FOUR_LEAF_TWO_DYADIC_LAYERS.md`;
- `V26_Q138_DYADIC_FIVE_LAYER_PREFIX_GATE.md`.

No complete-factor improvement is admitted because the exact tail k>=5 is unresolved.

## Sharp dyadic tail criterion

A full dyadic representation improvement now requires

`sum_{k>=5} rank(layer_k) <1,935,451,277,056`.

Generic k5 alone is

`49,193,897,820,160`,

about25.4173x the entire remaining budget.

Do not merely solve one next residue family. Even the impossible assumptions

`r_A2=r_D2=r_B1=r_C1=0`

leave

`r5=2,067,939,590,144`,

still `132,488,313,088` above the total tail budget.

Even also setting

`r_A3=r_D3=r_B2=r_C2=0`

leaves

`r5=2,004,408,467,456`,

still `68,957,190,400` above budget.

Therefore success requires at least one deeper residue improvement or a sharper early residue bound. The current highest-leverage cheap target is to search exact canonical cancellations inside the A/D second-residue bounds309/310 before digging several layers deeper.

## Non-authoritative / provenance warnings

- old leaf coefficient full-rank run `32011941759`: exit143 before result;
- exploratory dense 2048x2048 minor `32054802994`: bad contraction path /32-GiB allocation failure before rank result;
- no canonical frozen `outer128` predecessor mask is available, so source-specific leaf claims remain provenance-gated;
- old four-site ranks96/208 and W84/W83 claims remain revoked after int32 overflow correction.

## d>=2 — unchanged

`S3={4,5,11,12,13,19,20,21,27,28,29}`.

Fully-open exponent63.562242424221076. Semi-open A54.661778097771986, B generic55, C54.92481250360578, D53.74357218893564.

`W_repr(d)<=508.4979393937686...d-333.8951148057971...`, d>=2.

## First unfinished mathematical pass

1. **A/D second-residue cancellation:** canonicalize and XOR the rank-one symbolic supports behind309/310; any exact reduction has very high k5 leverage.
2. **Dyadic tail depth:** if early cancellation is insufficient, compute deeper A/D and B/C residues with the explicit target `tail<1,935,451,277,056`; B/C second residue alone cannot finish the job.
3. **Total dyadic summation:** only after a convergent/finite total layer-rank bound exists may `W_repr(1)` be lowered.
4. **Leaf-central evaluator:** only after total layer control, fuse the dyadic layers into the central D16 common/private decomposition and count multiply/add, generation, recomputation, memory traffic and output.
5. Other nonlocal center regroupings, semi-open B<55 and fully-open S3<63.562 remain separate exact routes.

Still not admitted: practical evaluator, arithmetic-work reduction, ranking/search gain, `alpha<1`, or full-round relevance.
