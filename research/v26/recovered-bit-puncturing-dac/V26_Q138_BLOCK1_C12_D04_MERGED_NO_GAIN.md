# V26 Q138 block1 C12..14 × D0..4 merged no-gain theorem

## Scope

This closes the smallest genuine merged block1 bridge obtained by combining the already-clean repeated-D chain `D0..4` with the backward j2 physical carry extension `C12,C13,C14`. It does **not** close the larger bridge from block1 to the extended-block2 high/wrap factors.

All arithmetic is exact over `Q`.

## Incoming exact space

The clean boundary-fiber theorem gives

`rank(D0..4)=65536=16*2^12`.

The relevant j2 boundary carry exposed to the backward C-chain is `s14`.

Authority prerequisite:

- `V26_Q138_BLOCK1_D4_BOUNDARY_FIBER_NO_GAIN.md`;
- `scripts/verify_v26_q138_block1_d4_boundary_fiber_no_gain.py`;
- clean run `32040273839`.

## Universal C-carry injectivity

For one physical C site the local operator has domain coordinates `(C_i,s_i)` and retained output coordinates `(s_{i-1},v_i,w_i)`:

`L_i(C_i,s_i)[s_{i-1},v_i,w_i] = T(s_i,s_{i-1},C_i,v_i,w_i)`.

The exact 4-row matrix has rank4. Therefore `L_i` is injective on its entire domain, not merely on a particular incoming subspace.

Composing the three sites 14,13,12 and contracting the internal carries `s13,s12` gives

`L_12:14 : F^{C12,C13,C14} tensor F^{s14} -> F^{s11,v14,w14,v13,w13,v12,w12}`.

Its exact domain dimension is16 and its exact rational rank is16.

Thus the full three-site operator is injective. Tensoring/composing an arbitrary incoming row space through it cannot create a new kernel or a new row-space overlap.

## Consequence for the merged bridge

The three new physical bits `C12,C13,C14` therefore multiply the clean incoming D0..4 rank by exactly `2^3`:

`rank(C12..14 joined with D0..4) = 65536*8 = 524288 = 16*2^15`.

This is exactly the naive product rank.

Hence

`C12..14 × D0..4 merged bridge = NO GAIN`.

## Interpretation

The negative result is stronger than the earlier isolated C12..14 rank test. The local C-carry map is universally injective, so **no** hidden geometry of the repeated-D incoming space can make this backward three-site C extension compressive.

Any new d=1 reduction must cross a factor where the local operator itself has a kernel or where two independently retained channels are actually contracted together. The remaining natural target is the larger j2 bridge toward the extended-block2 high/wrap side, with every repeated S1 D occurrence entering that bridge closed consistently.

## Authority

- `scripts/verify_v26_q138_block1_c12_d04_merged_no_gain.py`;
- `.github/workflows/block1-c12-d04-merged-no-gain.yml`.
