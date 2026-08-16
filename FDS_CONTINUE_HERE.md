# FDS_CONTINUE_HERE

**State:** Issue #13 `NO_GO_ALL_TWO_WORD_SINGLE_BOUNDARY_MITM`; Issues #10–#12 also structural NO-GO; Issue #9 constant-factor PASS; alpha=1.  
**Next:** freeze exact two-boundary-word XOR projection cancellation audit.

1. Do not retest another two-word placement under raw dependency support; all 28 are closed.
2. New mechanism must test algebraic cancellation not visible in dependency unions.
3. Freeze layout, fresh targets, split/projection set and exact half-independence gates before results.
4. Candidate projection should be a fixed XOR of one or two internal boundary words.
5. Forward projection must be exactly independent of one 8-bit half; backward projection exactly independent of the other on every fresh target.
6. Only such a projection may open half-table matching/TOTAL accounting.
7. No approximate cancellation or target-specific projection selection after inspection.
