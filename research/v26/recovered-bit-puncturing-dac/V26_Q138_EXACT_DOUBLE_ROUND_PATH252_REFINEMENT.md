# V26 q138 Exact Double-Round Path-252 Refinement

## Purpose

`V26_Q138_EXACT_DOUBLE_ROUND_PATH450_THEOREM.md` gives a deliberately conservative open-boundary bound of 90 binary frontier bonds per active QR and therefore 450 for the five-QR q138 inverse-double-round star.

The q138 boundary pattern is much more structured. This note keeps the actual fixed/open word-mask pattern and reduces the exact path bound to

**252 binary frontier bonds**.

No approximation or trail cap is used.

## 1. Backward mask relations for one QR

Use the standard QR outputs `(Af,Bf,Cf,Df)` and inputs `(A0,B0,C0,D0)`. After exact backward transport through the XOR/rotation steps, one convenient reduced description uses the free internal mask families `u3,u4,v3,v4` and four addition sigma chains.

Write

- `q7 = ROR7(Bf)`;
- `q8 = ROR8(v4 xor Df)`;
- `q12 = ROR12(v3 xor q7)`.

The addition masks can be chosen so that, bitwise up to the fixed rotation-index convention,

- addition 4 output uses `Cf xor q7`;
- addition 3 output uses `Af xor q8`;
- addition 2 output uses `u4 xor q12`;
- addition 1 second input uses `B0 xor q12`;
- the `D0` boundary relation is the rotation-16 relation between `D0` and the combination feeding addition 2/addition 1.

With all four input/output masks fixed, this is exactly the previously proved `{1,8,12}` reduced network with frontier 44.

## 2. Central q138 column QR: output fixed, all four inputs open

For the active q138 column QR, `(Af,Bf,Cf,Df)` are fixed by the q138 output mask, while `(A0,B0,C0,D0)` are the four 32-bit intermediate word masks that must be connected to the preceding diagonal layer.

Opening `A0`, `B0` and `C0` introduces only local physical legs in the reduced site description.

Opening `D0` restores one periodic rotation-16 mask-wire family: the same `D0` bit participates in the two reduced relations separated by 16 bit positions.

Therefore the exact central-QR site skeleton has

- four sigma chains: `4` crossing binary bonds;
- one offset-8 family: at most `16`;
- one offset-12 family: at most `24`;
- one offset-16 boundary family: at most `32`.

Hence

`W_center_path <= 4+16+24+32 = 76`.

## 3. Diagonal leaves: fixed inputs, one output word open

The four intermediate words `0,4,8,12` occupy the four different local QR output positions across the four diagonal QRs, so all four output-position cases must be covered.

### A-output open

`Af` appears only as the local side mask of the addition-3 output. It creates no new inter-site family. Frontier remains 44.

### C-output open

`Cf` appears only as the local side mask of the addition-4 output. Frontier remains 44.

### D-output open

Replace the internal family by

`x4 = v4 xor Df`.

Then `q8=ROR8(x4)` retains the existing offset-8 family and the open `Df` leg is local at the addition-4 site. Frontier remains 44.

### B-output open

Let

`b = q7 = ROR7(Bf)`

and replace

`x3 = v3 xor b`.

Then `q12=ROR12(x3)` retains the existing offset-12 family, while `b` appears locally in the remaining addition factors. A uniform cyclic relabeling of that diagonal QR's bit sites by 7 aligns its physical `Bf` boundary with the central word-mask bit. A global cyclic site shift does not change the internal offsets `{1,8,12}`.

Thus this case also has frontier 44.

Therefore each of the four diagonal one-output kernels satisfies

`W_leaf_path <=44`.

## 4. Glue the star

Choose one common bit-prefix order after applying the allowed uniform site relabeling to the B-output diagonal leaf.

At each bit position group

- the central QR site;
- the corresponding site of each of the four diagonal QRs;
- the equality identifications of their intermediate word-mask boundary bits

into one super-site.

The inter-layer equality edges are then local to the super-site and do not cross the bit-prefix cut.

The combined frontier is bounded by the union of the five internal QR frontiers:

`76 + 4*44 = 252`.

Hence the exact q138 inverse-double-round star admits a complete sequential path contraction with

`D <= 2^252`.

Define the refined topology-only bound

**`W_2_topo <=252`**

for this full intermediate-mask boundary object.

## 5. Coarse depth law

The first q138 inverse double round therefore costs at most 252 frontier bits in this reduced/open pattern.

For every additional preceding double round, use a safe bound of eight fully open QRs. The general open-QR theorem gives at most 90 frontier bits per such QR. Therefore

`W_topo(d) <= 252 + 720*(d-1) = 720d - 468`

for `d>=1` inverse double rounds.

This is only a coarse structural upper bound. It is not a sharp Schmidt-rank recurrence.

## 6. Relation to U47 / prefix119

The internal one-QR structures

- common parent interface `U47`;
- exact right-control observable prefix quotient `119`;
- I9 support selector rank `12`

may reduce the 252 bound, but only after they are embedded into the **actual four 32-bit intermediate word-mask interfaces** of this star.

They must not be substituted for those word masks by dimensional analogy.

## 7. What is proved and what is not

Proved:

- exact q138 double-round dependency cone has five active QRs;
- central fixed-output/open-input reduced frontier `<=76`;
- each fixed-input/single-output diagonal kernel frontier `<=44`;
- exact combined path frontier `<=252`;
- coarse finite-depth law `<=720d-468`.

Not proved:

- that 252 is optimal or close to optimal;
- a practical double-round contraction;
- an algebraic/Schmidt rank below the topological frontier;
- arithmetic-work reduction, ranking gain, `alpha<1`, or full-round relevance.

The next exact target is to compress the four intermediate 32-bit word-mask interfaces of the five-QR star as MPS/transfer objects and then require a complete two-layer contraction certificate.