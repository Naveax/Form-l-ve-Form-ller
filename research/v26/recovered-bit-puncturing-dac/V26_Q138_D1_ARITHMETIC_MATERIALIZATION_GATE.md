# V26 Q138 d=1 arithmetic materialization gate

## Scope

The new exact d=1 rank bound improves representation and coefficient-aware materialized-factor **memory/message** to

`3829*2^73` entries.

This note asks a narrower arithmetic question: can an evaluator obtain a useful work reduction while still explicitly materializing that factor?

Answer: no. Explicit materialization itself has an output-size lower bound equal to the full factor size. Any arithmetic-work improvement must therefore contract on the fly and avoid emitting the complete rank-by-leaf table.

## Exact D16 common/private decomposition

Let the low incoming rank per high prefix be

`n=2^22`.

The j1 D16 spaces have

`448,448,intersection424`.

The new bit0+gap D16 spaces have

`64n,64n,intersection63n`.

For the two tensor-product D16 sectors, the common intersection block has dimension

`424*63n = 26712n`.

Each full sector has dimension

`448*64n = 28672n`.

Therefore the part of each sector outside the common block has dimension

`28672n-26712n = 1960n`.

The complete per-prefix union decomposes dimensionally as

`26712n + 1960n + 1960n = 30632n`.

Thus approximately87.2% of the union channels are common to both D16 sectors. Treating the two sectors independently would touch `57344n` channels before deduplication, whereas the exact overlap-aware channel space has `30632n` directions, a formal channel-reuse factor of about1.872.

This is the algebra that a useful scalar evaluator should preserve rather than flattening immediately to one generic basis.

## Explicit-factor output lower bound

Across16 independent D12..15 high prefixes the central rank is

`R=16*30632*2^22 =3829*2^29`.

The four predecessor leaves contribute `2^44` S1 assignments in the current coefficient-aware materialized factor.

Therefore the table contains

`R*2^44 =3829*2^73`

scalar entries:

`36,163,882,525,815,743,046,483,968`.

Any algorithm that explicitly produces this complete table must perform at least one scalar emission/write per output entry. Hence, in the scalar-write model,

`work_materialize >=3829*2^73`,

with log2 exponent

`>=84.90275194485017...`.

This lower bound is independent of the entry-generation algorithm. Streaming Gaussian reduces simultaneous storage, not the number of table entries that must be emitted.

## Consequence

The materialized-factor route is unsuitable as the route to an admitted arithmetic-work reduction.

The next evaluator must instead push contraction with predecessor leaves inside the exact central decomposition, so that common D16 channels are accumulated directly into the scalar or a much smaller boundary message. The natural exact decomposition to preserve is

`common 26712n + private0 1960n + private1 1960n`

for each high prefix, together with the sixteen-prefix direct sum.

The most obvious next arithmetic probe is predecessor-leaf structure. The current generic accounting pays `2^11` Schmidt directions per predecessor leaf at the S1 cut, hence `2^44` across four leaves. Any uniform exact reduction in those four leaf Schmidt ranks would reduce the scalar-contraction channel count without changing the central theorem.

## Ledger discipline

This is a scoped NO-GO for **explicit materialization as an arithmetic-work strategy** only.

It does not prove that scalar-on-the-fly contraction has exponent84.9, nor does it prove a total-work improvement over any external baseline. Factor generation, sparse merge, contraction, recomputation, memory traffic and final reconstruction must all be counted before an arithmetic-work claim is admitted.

`ALPHA_PASS=0` remains unchanged.

## Authority

- `scripts/verify_v26_q138_d1_arithmetic_materialization_gate.py`;
- `.github/workflows/d1-arithmetic-materialization-gate.yml`.
