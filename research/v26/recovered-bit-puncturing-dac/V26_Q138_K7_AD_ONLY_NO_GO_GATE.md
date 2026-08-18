# V26 Q1.38 frozen-tail k7 search gate

## Status correction

The arithmetic values in this file are exact, but the old **necessity interpretation is revoked**.

This gate freezes the previously computed generic k0..k6 prefix and therefore freezes the old residual budget

`T=5,520,647,809,024`.

It then asks whether a changed k7 alone fits inside that frozen budget. This is a conservative **sufficient search gate**. It is not a necessary condition once `a2,b2,c2,d2` change, because those same index-2 improvements also reduce layers k2..k6 and enlarge the true remaining budget.

The corrected dynamic authority is

`V26_Q138_DYNAMIC_PREFIX_K7_RECOUNT.md`

with verifier

`scripts/verify_v26_q138_dynamic_prefix_k7_recount.py`.

In particular, the former statements

- “B/C reduction is mathematically necessary for k7”,
- “a2<=1439 is necessary”,
- “d2<=1414 is necessary”

are **not admitted as dynamic necessities**. They are only thresholds for this frozen-old-tail sufficient test.

## Frozen-tail setup

Use

A `[3,219,a2,2048,...]`,
B `[36,812,b2,2048,...]`,
C `[84,972,c2,2048,...]`,
D `[3,207,d2,2048,...]`,

but keep the old generic k0..k6 prefix fixed, so the reserved k>=7 budget is

`T=5,520,647,809,024`.

The exact k7 polynomial is

`k7 = 207 a2 b2 c2 +972 a2 b2 d2 +178176 a2 b2`

`    +812 a2 c2 d2 +79872 a2 c2 +245760 a2 d2 +2652831744 a2`

`    +219 b2 c2 d2 +12288 b2 c2 +178176 b2 d2 +1029758976 b2`

`    +79872 c2 d2 +845733888 c2 +2699624448 d2`

`    +1703063715840`.

Under this frozen-budget test only:

- `a2=d2=0`, `b2=c2=2048` gives `k7=5,595,612,708,864 >T`;
- the frozen-budget A threshold with the other index-2 ranks zero is1439/1440;
- the frozen-budget D threshold with the other index-2 ranks zero is1414/1415;
- with ideal A/D zero, the equal B/C threshold is2009/2010;
- with the hypothetical A/D correction-only values362/171, the equal B/C threshold is1055/1056.

These remain useful conservative pruning numbers, but no longer determine mathematical priority by themselves.

## Correct dynamic comparison

When index-2 ranks are changed, recompute k0..k6 as well. For example

`a2=d2=0`, `b2=c2=2048`

gives dynamically

`sum(k0..k6)=1,809,267,529,728`,

`k7=5,595,612,708,864`,

so

`sum(k0..k7)=7,404,880,238,592 <2^44`.

Thus the frozen-tail failure above does not imply dynamic k7 failure.

No complete k>=8 tail, complete-factor, arithmetic-work, ranking/search, alpha or full-round claim is made here.
