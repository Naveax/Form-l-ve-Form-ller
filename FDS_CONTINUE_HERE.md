# FDS_CONTINUE_HERE

**State:** `ADMIT_BROAD_NONUNIVERSAL_WALL_REALIZATION`  
**Next:** `V25_MULTI_LAYOUT_CODEGEN_SCALING_B10_B16`.

1. Fresh main + authority.
2. Use only W5_SINGLE and W4_W6_SPLIT representative layouts from the frozen scaling plan.
3. b=10/12/14/16 targets and benchmark repeats are already frozen.
4. Keep split1/word0/width16/codegen rule unchanged.
5. Full generated-vs-generic exactness across every candidate/case precedes scaling wall admission.
6. Each layout/b requires true unique 3/3, median wall >=1.05 and positive >=2/3.
7. Both layouts must pass all four b values for family scaling PASS.
8. Report slopes but alpha remains 1 by leading 2^b enumeration; no full-round claim.
