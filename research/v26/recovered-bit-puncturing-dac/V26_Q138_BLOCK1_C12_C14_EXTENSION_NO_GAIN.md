# V26 q138 block1 C12..C14 contiguous carry-extension no-gain result

## Statement

Start from the clean exact rank16 S1 block1 on physical row bits

`A0,B0,C15,C16,D0`.

Extend the j2 carry chain downward through the three remaining S1 C-row bits

`C14,C13,C12`,

so the full physical row set is

`A0,B0,C12,C13,C14,C15,C16,D0`.

The exact rational row rank is

`128 = 16*2^3`.

Therefore the contiguous local C12..C14 carry extension gives exactly the naive cost of passing the three added physical bits raw. It gives no representation-rank improvement.

All arithmetic is exact over `Q`; `epsilon=0`.

## Construction

The j2 segment contains bits16,15,14,13,12.

- `C16,C15,C14,C13,C12` are physical S1 row bits;
- `D0` is shared between j1 bit0 and j2 bit16 and is already occurrence-closed inside block1;
- carries between the five j2 sites are contracted exactly;
- the carry leaving bit12 and the local v/w legs at bits14,13,12 remain on the column side;
- j1 bit0 remains the exact bit0 Walsh factor on `A0,B0,D0`.

The resulting finite exact matrix has 256 physical rows. Sparse rational Gaussian elimination gives rank128.

The previous two-bit result

`block1 + C13,C14: rank64 = 16*4`

is therefore extended one site farther without finding any rank collapse.

## Consequence

The remaining C12 bit cannot improve the d=1 bound merely by extending the already-tested block1 j2 carry chain one additional site.

This does not rule out C12 participating in a larger multi-site construction that couples block1 to the rank21888 block2/high-sector structure. Such a construction would have to exploit shared column/carry/repeated-D geometry that is absent from this isolated contiguous block1 extension.

## Verification

Authority verifier:

`scripts/verify_v26_q138_s1_local_extension_falsifiers.py`

Clean GitHub Actions run:

`32038564342` — success.

The verifier checks

- `block1 + C13,C14` exact rank64;
- `block1 + C12,C13,C14` exact rank128.

## Scope

Scoped exact NO-GAIN result only. It is not a lower bound on the full S1 central matricization, does not rule out merged block1/block2 multi-site factors, and makes no arithmetic-work, ranking, alpha, or full-round claim.
