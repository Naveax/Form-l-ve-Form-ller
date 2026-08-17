# V26 q138 block1 D3 extension kernel no-gain theorem

## Statement

Start from the clean occurrence-closed block1 extension through repeated D variables `D0,D1,D2`, whose exact row rank is

`1024 = 16*2^6`.

Add the next physical row bits

`A3,B3,D3`,

and close both occurrences of `D3` simultaneously:

- j1 bit3;
- j2 bit19.

The resulting exact rational row rank is

`8192 = 16*2^9`.

Thus the D3 extension gives exactly the naive factor8 and no representation-rank improvement.

The useful point is not merely the number8192. The no-gain result has a clean kernel explanation: the local D3 coupled-carry operator has an 8-dimensional kernel, but the current D0..2 row space has zero intersection with the fibers required to enter that kernel.

All arithmetic is exact over `Q`; `epsilon=0`.

## 1. Old D0..2 block

The clean two-site block1 falsifier closes D0,D1,D2 across

- j1 bits0,1,2;
- j2 bits16,17,18;

while retaining the C15,C16 part of the original rank16 block1.

Its exact row-space construction uses eight D sectors. Per sector:

- j1 row rank64;
- j2 row rank3.

The 1536 natural sector-product vectors span exact rank1024.

Let this old row space be `V`, with

`dim V = 1024`.

The old j1 boundary carry is `s2`; the old j2 boundary carry is `s18`.

## 2. Both s2 projections are injective on V

Project the old column space to fixed `s2=0`, drop the s2 coordinate, and compute the exact row rank. The result is

`1024`.

Do the same for `s2=1`. The result is again

`1024`.

Therefore the restriction maps

`P0: V -> columns(s2=0)`

and

`P1: V -> columns(s2=1)`

are both injective.

Equivalently,

- V contains no nonzero vector supported only on `s2=0`;
- V contains no nonzero vector supported only on `s2=1`.

This fiber fact is the decisive obstruction to exploiting the next local kernel.

## 3. Local D3 coupled-carry operator

Before attaching the old remainder, isolate the new two-site occurrence closure.

Rows are indexed by

`(A3,B3,D3,s2,s18)`,

32 possibilities.

Columns are indexed by the new outside variables

`(s3,k3,q3,s19,C19,x19,w19)`.

The exact coefficient is

`T(s3,s2,A3,k3 xor B3,q3 xor D3)`

times

`T(s19,s18,C19,x19 xor D3,w19)`.

This finite rational 32-row operator has exact rank

`24`,

so its left kernel has dimension8.

## 4. The kernel is explicit

For every fixed triple

`(B3,D3,s18)`,

the two local rows

`(A3=0,s2=1)`

and

`(A3=1,s2=0)`

are identical.

There are exactly eight such pair relations, one for each `(B3,D3,s18)`.

Since the local rank is24, these eight relations span the full kernel.

Thus any vector entering the local kernel must pair

- an old component supported entirely on `s2=1` with A3=0;
- an equal old component supported entirely on `s2=0` with A3=1.

## 5. Why the old space misses the kernel

The domain before the D3 local map is

`F^8_(A3,B3,D3) tensor V`,

with dimension

`8*1024 = 8192`.

A nonzero intersection with the local kernel would require a nonzero vector of V supported entirely in one fixed s2 slice.

Section2 proves that neither such fiber exists.

Therefore

`(F^8 tensor V) ∩ ker(local D3 map) = {0}`.

The local D3 map is injective on the actual old block1 row-space domain even though it is not injective on the full abstract32-dimensional local domain.

Hence the new exact rank is

`8*1024 = 8192`.

## 6. Consequence

The repeated-D block1 route is now closed one site farther:

- D1/D2 two-site extension: rank1024=`16*2^6`, no gain;
- D3 extension: rank8192=`16*2^9`, no gain.

This makes a blind D4/D5 continuation less attractive. Any further local extension should first show a new kernel/fiber geometry; otherwise the next serious target is a merged block1/block2 multi-site factor or direct joint-channel overlap.

## Verification

Authority verifier:

`scripts/verify_v26_q138_block1_d3_extension_kernel_falsifier.py`

It verifies exactly:

- old D0..2 rank1024;
- s2 slice projection ranks1024 and1024;
- local D3 operator rank24/32;
- the eight explicit kernel pair relations;
- zero kernel intersection by the injective-projection argument;
- final exact rank8192.

## Scope

Scoped exact NO-GAIN theorem for the D3 occurrence-closed extension only. It is not a lower bound on the full S1 central rank and does not rule out D4/D5 under a different joint mechanism, merged block1/block2 factors, arithmetic-work improvements, ranking gains, `alpha<1`, or full-round relevance.
