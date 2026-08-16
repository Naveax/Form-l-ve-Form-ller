# V25 Layout-Specialized Codegen Wall Realization

## Verdict

`ADMIT_BROAD_NONUNIVERSAL_WALL_REALIZATION`

Fresh targets `[404,274,285,190,939,749,785,460]` were frozen before measurement. Generated-vs-generic exactness passed for 49,152 full syndrome values and 49,152 direct predicates. Generated source is 12,032 bytes; generation+compile is about 14 ms.

Frozen median wall speedups: W4 control 1.0623x; W5 1.1135x; W6 1.1284x; W7 1.1215x; W4+W8 1.0077x; W4+W6 1.0751x.

Four of five non-control layouts pass the preregistered median>=1.05, positive>=7/8 and exact-unique gates. Thus broad wall realization is admitted by the frozen rule, but it is not universal: same-column W4+W8 failed. QR transfer remains 5/5 from the prior layout L1.

This remains a reduced 6-round constant-factor engineering result. Candidate enumeration is still 2^b and alpha=1.
