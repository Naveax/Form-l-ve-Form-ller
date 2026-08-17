# V26 Q1.38 predecessor-leaf B/C second-residue support-frequency nesting

## Scope

Use the explicit first dyadic lifts

`M_B=2^121 L_B=K_B+2R_B`,

`M_C=2^121 L_C=K_C+2R_C`.

The clean weight120 theorem gives integer lifts of the weight120 support-indicator component of `R mod2` with S1 left-Walsh frequency unions

- B:668;
- C:788.

This theorem proves that every remaining **support-indicator** correction coming from carry weights121..124 uses no additional S1 Walsh frequency beyond those same unions.

It excludes the sign-negative Boolean corrections of the e0 sectors and the special four-half-sector second-bit correction.

## High-weight correction classes

For a carry sector with k zero carry sites, weight is `124-k`. Let n be the internal nullity and p the polar rank of the sign quadratic form on the internal fiber. For the scaled integer coefficient `M=2^121L`, a nonzero quadratic Gauss contribution has 2-adic exponent

`e = k-3+n-p/2`.

After subtracting the first lift and dividing by2:

- e1 sectors contribute support indicators modulo2; sign disappears;
- e0 sectors contribute a support term plus a sign-negative correction;
- e>=2 sectors vanish at this bit;
- the four e=-1 weight122 unique-solution sectors form a separate joint half-sector correction.

Exact class counting gives e1 raw sectors

- one-zero:102;
- two-zero:2397;
- three-zero:8196;

and e0 raw sectors

- top:1;
- one-zero:22;
- two-zero:74;
- three-zero:484.

After full affine consistency and canonical XOR grouping, the e1 support indicators have odd-support S1 frequency unions

- B:320;
- C:704.

The raw e0 support indicators have S1 frequency unions

- B:92;
- C:104.

## Exact nesting

Let `U120` be the S1 Walsh frequency union of all affine-consistent internal-rank128 weight120 support indicators.

The clean weight120 theorem gives

`|U120_B|=668`,

`|U120_C|=788`.

Let `Ue1` be the union from the canonical odd e1 support indicators, and `Ue0sup` the union from the raw e0 support indicators.

Exact set comparison gives

B:

`|Ue1|=320`, `|Ue0sup|=92`,

`Ue1 subset U120`, `Ue0sup subset U120`.

C:

`|Ue1|=704`, `|Ue0sup|=104`,

`Ue1 subset U120`, `Ue0sup subset U120`.

Therefore the entire support-indicator portion of the B/C second residue has an ordinary integer lift whose rational row rank stays within

`<=668` for B,

`<=788` for C.

No separate `+320`, `+704`, `+92`, or `+104` rank payment is required.

## Remaining obstruction

The complete second residue still contains

1. e0 sign-negative correction functions; and
2. the four-half-sector second-bit Boolean correction.

Only those sign-dependent pieces can enlarge the S1 left-row space beyond the668/788 support basis.

This theorem does not bound those pieces and therefore is not yet a complete B/C second-residue rank theorem.
