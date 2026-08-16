from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
required=['README.md','FDS_CONTINUE_HERE.md','FDS_CURRENT_STATE.md','FDS_VISION.md','FDS_RESEARCH_DISCIPLINE.md','FDS_KNOWLEDGE_GRAPH.md','FDS_CHECKLIST.md','FDS_DECISION_LOG.md','archive/RAW_IMPORT_MANIFEST.json']
missing=[x for x in required if not (ROOT/x).exists()]
print({'required':len(required),'missing':missing,'ok':not missing})
raise SystemExit(1 if missing else 0)
