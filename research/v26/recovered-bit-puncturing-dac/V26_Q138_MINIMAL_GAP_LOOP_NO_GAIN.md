# V26 Q138 minimal gap-loop accessibility no-gain theorem

## Scope

The j2 bits1..11 gap has a genuine local rank deficiency `66/128`, with kernel dimension62. This theorem tests whether that kernel is already reachable from the smallest real incoming loop containing:

- the exact rank16 block1 core on `A0,B0,C15,C16,D0`;
- the D16/bit0 factor with physical C0 and shared retained `v3_12`;
- the physical C12,C13,C14 backward carry bridge.

D16 is fixed as a sector. The larger D0..5 and high-prefix bridge are not yet included in this theorem.

## Incoming minimal loop before C1..5

For either fixed D16, merging block1 with bit0 through the shared retained coordinate `v3_12` gives rank32. Adding physical C12..14 through the universally injective three-site carry operator multiplies this by8:

`rank(W)=256`.

The open boundary variables relevant to the missing gap are `(s0,s11)`.

## Fixed-s11 boundary graph

For either D16 and either fixed `s11`, restrict W to that s11 slice. The exact projection space has dimension

`dim W_s11 = 248`.

Inside this projected space:

- the `s0=0` image has dimension124;
- the `s0=1` image has dimension248;
- the `s0=0` image is an exact subspace of the `s0=1` image;
- every vector `u` in the 124-dimensional smaller image has its diagonal lift `(u,u)` inside `W_s11`.

Because the `s0=1` projection has full rank248, `W_s11` is the graph of a unique operator `A` on the 248-dimensional `s0=1` image. The facts above imply

`im(A)` has dimension124,

`A|im(A)=I`,

hence

`A^2=A`.

Thus A is an exact projector with two eigenspaces over Q:

- lambda0 dimension124;
- lambda1 dimension124.

## Gap geometry at fixed s11

For each fixed s11, let `M0` and `M1` be the 32-row maps indexed by physical `C1..5` at fixed `s0=0` and `s0=1`.

The exact gap Gram theorem gives:

- `rank M0=32`;
- `rank M1=32`;
- `rank(span(M0,M1))=33`.

The complete s11=0 and s11=1 image spaces are each rank33 and are direct because the full gap rank is66.

For the incoming projector eigenspaces, the composed fixed-s11 map reduces to two matrix pencils:

- lambda0: `M1`;
- lambda1: `M0+M1`.

Exact Gram calculations give

`rank(M1)=32`,

`rank(M0+M1)=32`.

Therefore both eigensectors are injective. The gap kernel misses the entire `32*248` projected incoming domain for each fixed s11.

## Full minimal-loop consequence

The full W has dimension256 but projection to either fixed s11 has dimension248, so each fixed-s11 composed map has an 8-dimensional incoming fiber as its only kernel source. After tensoring with the32 physical C1..5 states, that kernel has dimension256 and is exactly the opposite-s11 fiber.

Because the two fixed-s11 gap image spaces are direct, cancellation between s11=0 and s11=1 is impossible. The two opposite-s11 fiber kernels have zero intersection.

Hence the complete map obtained by adding physical C1..5 to W is injective:

`rank = 32*256 = 8192`.

This is the full naive rank. Thus the genuine local gap kernel is **not reachable** in the minimal physical loop.

## Interpretation

The rank66 gap deficiency is real, but it behaves exactly like the earlier D3 local kernel lesson: existence of a local kernel is insufficient. The incoming boundary graph must have an eigenvalue matching a singular matrix pencil of the gap. Here the incoming graph has only eigenvalues0 and1, while both corresponding gap pencils are full rank.

The next question is whether the additional occurrence-closed D0..5 and high-prefix bridge operations preserve this projector boundary geometry. If they act as boundary-blind injective lifts, the full 39-bit incoming factor also misses the gap kernel and the entire natural S1 bridge closes with no gain. If they alter the boundary graph spectrum, a gain remains possible.

Canonical d=1 bound is unchanged by this theorem.

## Authority

- `scripts/verify_v26_q138_minimal_gap_loop_no_gain.py`;
- `.github/workflows/minimal-gap-loop-no-gain.yml`.
