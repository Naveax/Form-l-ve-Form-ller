# V26 q138 Rotation / Carry-Tail Amplification

## Purpose

This note identifies, from the exact modular-addition Walsh theorem and ChaCha wiring alone, why the q138 inverse-quarter-round trail space explodes after an initially tiny local expansion. It also quantifies how strongly low-sigma shells can compress one of the resulting huge modular-addition Walsh columns.

The calculations below concern the published one-addition sigma model and standard ChaCha quarter-round wiring. They are not yet numerical authority for the missing recovered project `max_sigma_weight` implementation.

## 1. MSB conservation for nonzero addition Walsh coefficients

Let w be a nonzero output mask of n-bit modular addition and let

`h = max{i : w_i=1}`.

For every nonzero Walsh coefficient `a_w(u,v)`:

- `u_i=v_i=0` for every `i>h`;
- `u_h=v_h=w_h=1`.

Therefore

`msb(u)=msb(v)=msb(w)=h`.

Proof: the sigma recurrence starts from `sigma_{n-1}=0`. Above h, `w_i=0`; while sigma is zero, the nonzero condition forces `u_i=v_i=w_i=0`, so sigma remains zero downward. At i=h, sigma is still zero and the nonzero condition forces `u_h=v_h=w_h=1`. Hence `gamma_h=1` and the carry-state sigma becomes one below h.

This simple lemma is the structural source of the carry-tail explosion: a high output-mask MSB permits input-mask activity anywhere below that bit.

## 2. Universal support lower bound at MSB h

For every nonzero output mask w with `msb(w)=h>=1`, there is an admissible sigma pattern

`sigma_i=1` for `0<=i<h`,

`sigma_i=0` for `i>=h`.

Its weight is h and `sigma_0=1`.

The multiplicity theorem gives

`2^(h+1)`

distinct nonzero Walsh coefficients associated with this single sigma pattern.

Therefore every such full Walsh column satisfies

`support(a_w) >= 2^(h+1)`.

This lower bound is crude but universal.

For h=27 it already gives at least

`2^28 = 268,435,456`

nonzero coefficients from one sigma pattern alone.

## 3. q138 first inverse wiring step

Take the local q138-style quarter-round output mask with only word B bit 10 active.

The final ChaCha operation is

`B_out = ROL(B_in xor C, 7)`.

Backward Walsh mask transport through the rotation gives

`ROR(2^10,7)=2^3`.

Backward transport through the XOR places this same mask on both the pre-XOR B wire and the C wire.

Thus the first reverse modular addition `C += D` is driven by output mask

`w=2^3`.

## 4. Exact first-addition mask family

For `w=2^3`, the MSB conservation lemma forces every nonzero input mask u,v to have

`msb(u)=msb(v)=3`

and no active bit above 3.

Hence v belongs to the eight-mask set

`{0x8,0x9,0xa,0xb,0xc,0xd,0xe,0xf}`.

Each of these eight v values occurs in at least one nonzero coefficient; this is also directly verified by the exact sigma recurrence on the four-bit domain.

The full `w=2^3` addition column has

`3*2^3 - 2 = 22`

nonzero `(u,v)` coefficients.

## 5. Rotation-induced amplification

The next inverse ChaCha wiring applies `ROR(...,8)` to the D mask.

Every v above is supported entirely in bits 0..3 and has bit 3 active. Therefore

`ROR(v,8) = v << 24`

in 32-bit word coordinates.

The resulting masks are exactly

- `0x08000000`,
- `0x09000000`,
- `0x0a000000`,
- `0x0b000000`,
- `0x0c000000`,
- `0x0d000000`,
- `0x0e000000`,
- `0x0f000000`.

Every one has MSB 27.

Thus a tiny four-bit carry tail produced by the first addition is rotated into the high word positions, and the **next** reverse modular addition is forced to expand an output mask whose carry-relevant domain extends through bits 0..27.

This is a purely algebraic explanation of the dramatic trail-space growth.

## 6. Full support sizes of the eight second-addition columns

Using the sigma-pattern multiplicity recurrence, without enumerating `(u,v)`, the exact full nonzero Walsh support sizes are:

| w | full nonzero coefficients |
|---|---:|
| `0x08000000` | 402,653,182 |
| `0x09000000` | 704,643,052 |
| `0x0a000000` | 603,979,768 |
| `0x0b000000` | 805,306,348 |
| `0x0c000000` | 402,653,182 |
| `0x0d000000` | 704,643,052 |
| `0x0e000000` | 603,979,768 |
| `0x0f000000` | 805,306,348 |

So after one 22-term local expansion plus a rotation, the next exact modular-addition columns already contain roughly 0.40 to 0.81 billion nonzero Walsh coefficients each.

## 7. Low-sigma concentration despite huge exact support

The same exact sigma-shell recurrence gives the number of coefficients retained by a mathematical hard cap `wt(sigma)<=K` and the exact retained one-addition Walsh energy.

### K=2

| w family | retained coefficients | retained energy |
|---|---:|---:|
| `08`/`0c` prefix | 6 | `3/4` |
| `09`/`0b`/`0d`/`0f` | 4 | `1/4` |
| `0a`/`0e` | 8 | `1/2` |

### K=3

- retained count range: 14..28;
- retained energy range: `5/8`..`7/8`.

### K=4

- retained count range: 30..76;
- retained energy range: `13/16`..`15/16` = 81.25%..93.75%.

### K=5

- retained count range: 62..172;
- retained energy range: `29/32`..`31/32` = 90.625%..96.875%.

Thus, in a **single** modular-addition Walsh column, tens of retained coefficients can capture most l2 energy of a column whose exact support has hundreds of millions of coefficients.

This is an explicit mathematical instance of the concentration phenomenon that makes trail/puncturing compression plausible.

## 8. Exact table for K=4

| w | full support | K4 support | K4 retained energy | K4 l2 residual |
|---|---:|---:|---:|---:|
| `0x08000000` | 402,653,182 | 30 | `15/16` | `1/4` |
| `0x09000000` | 704,643,052 | 76 | `13/16` | `sqrt(3)/4` |
| `0x0a000000` | 603,979,768 | 56 | `7/8` | `1/(2 sqrt(2))` |
| `0x0b000000` | 805,306,348 | 76 | `13/16` | `sqrt(3)/4` |
| `0x0c000000` | 402,653,182 | 30 | `15/16` | `1/4` |
| `0x0d000000` | 704,643,052 | 76 | `13/16` | `sqrt(3)/4` |
| `0x0e000000` | 603,979,768 | 56 | `7/8` | `1/(2 sqrt(2))` |
| `0x0f000000` | 805,306,348 | 76 | `13/16` | `sqrt(3)/4` |

The local compression ratio measured only as exact-support / retained-support is enormous, but it must not be mistaken for a composed-QR error guarantee.

## 9. Single-bit asymptotic error-representation exponent

For a single-bit output mask `w=2^b` and K<b, the sigma-shell theorem gives

`l2 residual = 2^(-K/2)`.

The number of retained coefficients is

`N_K = sum_{k=1}^K 2^k = 2^(K+1)-2`.

Hence asymptotically

`N_K = Theta(2^K)`

while

`epsilon_K = 2^(-K/2)`.

Eliminating K gives

`N_K = Theta(epsilon_K^(-2))`.

Therefore the exact local error-representation exponent for this single-bit modular-addition family is

`theta = 2`

when error is measured in l2 norm.

If squared l2 error/energy loss were used instead, the numerical exponent would be 1; the metric must therefore always be stated explicitly.

## 10. What breaks at the composed QR level

The strong one-addition concentration does **not** imply that applying the same small hard cap independently at four successive additions gives a good QR approximation.

Intermediate mask mixtures change, residual columns interfere, and later rotations repeatedly move low carry tails into high positions. A direct hard-per-addition calculator diagnostic already shows collapse for some small K values along the q138 path.

Therefore the correct composed analysis is not

`multiply retained energy fractions`.

It is

1. compute/upper-bound the local residual Gram on the actually reached mixture;
2. propagate local on-orbit defects by the telescoping theorem;
3. optimize caps under a global error budget.

## 11. Structural interpretation

The q138 path exhibits two competing mechanisms:

**Amplification:** rotations move a short low-bit dependency cone to high bit positions, causing the next modular addition to expose an exponentially large exact Walsh support.

**Concentration:** despite that support size, a small number of low-sigma coefficients can carry most of the local l2 energy.

The research question is exactly whether concentration wins over repeated amplification under source-conditioned controlled-error composition.

That is a mathematical compression question, not a programming-performance question.

## 12. Claims not admitted

These exact local calculations use the published modular-addition sigma definition and standard ChaCha wiring. They do not identify the recovered project `max_sigma_weight` semantics, do not certify a full QR residual for the historical cap family, and do not establish full-round compression, ranking gain, alpha<1, or attack relevance.