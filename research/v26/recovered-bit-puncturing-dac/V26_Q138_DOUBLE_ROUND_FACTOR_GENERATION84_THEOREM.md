# V26 q138 coefficient-aware materialized-factor generation84 theorem

## Statement

The exact d=1 four-site signed rank96 theorem lowers the materialized signed factor size to

`261*2^76`,

so

`W_2_factor-gen <= 76+log2(261)=84.02790599656988...`.

This matches the current d=1 representation upper bound. Arithmetic work is not improved by this theorem.

## Constructivity of the new rank96 block

The new four-site block on physical row bits

`A2,B2,C2,D2,A3,B3,C3,D3`

has256 physical rows. Its exact Gram has64 zero rows and96 nonzero signed classes, each class containing exactly two rows. Hence the96 rank directions can be chosen as actual physical-row directions and every nonzero physical row maps to one basis channel with coefficient `+1` or `-1`.

Therefore the new rank96 factor adds no abstract right-basis oracle.

Block1 remains physical-row explicit. Block2 retains the clean physical-row bridge: each normalized block2 right-basis direction is an exact combination of at most64 ordinary physical block2 rows. Consequently every complete signed right-basis slice after multiplying block1, block2, the new rank96 block and the eighteen raw identity bits is still an exact combination of at most64 ordinary physical S1 central input-mask rows.

## Factor size

The new central S1 rank is

`R=261*2^32`.

Four predecessor leaves contribute44 S1 mask bits, so a complete materialized signed factor indexed by `(alpha,r)` contains

`R*2^44 =261*2^76`

entries, exponent

`76+log2(261)=84.02790599656988...`.

## Right-factor generation

Reuse the explicit21-site complement tree from the factor-generation85 theorem. For every complement cluster T,

`C(T)=gb(T)+4*min(|T|,21-|T|)`

and the complete tree peak is80. A fixed physical S1 central row leaves only the51-bit reduced-central boundary; leaf generation remains at most44. Hence right-entry generation peak

`max(80,51,44)=80`

is below the84.028 materialized factor size.

Materialize the right factor entrywise using at most64 physical central-row slice contractions per signed basis direction. The left factor has the same dimension. Final contraction over `(alpha,r)` introduces no larger single message.

Thus

`W_2_factor-gen<=84.02790599656988...`.

## Ledger semantics

This is coefficient-aware materialized-factor generation, not the coefficient-blind static graph+leaf method, whose method-optimal peak remains95. It is also not an arithmetic-work theorem: at least `261*2^76` scalar entries must be produced for one complete materialized factor, and the actual repeated contraction work is much larger.

No unrestricted scalar-streaming memory number is canonically assigned without a work budget.

All operations are exact; `epsilon=0`.

Verifier:

`scripts/verify_v26_q138_double_round_factor_generation84.py`.
