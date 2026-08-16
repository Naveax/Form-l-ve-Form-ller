# V25 Exhaustive Two-Key-Word Dependency MITM Audit

Frozen Issue #13 target-free protocol completed.

Every unordered pair of active key/state words 4..11 was tested: **28 layouts × 80 internal cones = 2,240 layout-cones**.

The exact gate required forward/backward active-half supports to be nonempty, disjoint, and jointly cover the two active words.

**Candidate count: 0 / 2,240. Layouts with candidates: 0 / 28.**

The W4_W6 subcase reproduces closed Issue #12 exactly, including its seven-pattern histogram. Regression **2/2 PASS**.

Decision: `NO_GO_ALL_TWO_WORD_SINGLE_BOUNDARY_MITM`. No target/numerical stage was opened. This closes simple two-word, single-boundary, dependency-separated MITM across all tested key-word pairs in the controlled six-round structure.

The next admissible mechanism must rely on exact algebraic cancellation not visible in dependency-union analysis, not another placement of the same two halves.
