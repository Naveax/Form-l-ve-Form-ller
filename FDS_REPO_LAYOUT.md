# FDS_REPO_LAYOUT

Recommended long-term layout:

```text
/
  README.md
  FDS_CONTINUE_HERE.md
  FDS_CURRENT_STATE.md
  FDS_VISION.md
  FDS_RESEARCH_DISCIPLINE.md
  FDS_KNOWLEDGE_GRAPH.md
  FDS_CHECKLIST.md
  FDS_DECISION_LOG.md
  src/                  # canonical implementation
  tests/                # regression/reference tests
  experiments/          # frozen experiment plans + runners
  results/              # compact result JSON/MD, no giant reproducible cache
  cert/                 # admission/certification summaries
  archive/              # historical raw snapshots and manifests
  scripts/              # verification / packaging helpers
```

Rules:
- source-of-truth code is never hidden only inside ZIP;
- raw historical dumps may live in `archive/`;
- giant scratch/cache should be reproducible and hash-described, not casually committed;
- one milestone = one clear result/decision trail;
- continuity root files are updated at milestone closure.
