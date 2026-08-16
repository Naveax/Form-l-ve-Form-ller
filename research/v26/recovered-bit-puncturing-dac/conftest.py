from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]

for dep_dir in (
    REPO_ROOT / "research" / "v25" / "bit-puncturing" / "recovered-runtime",
    REPO_ROOT / "research" / "v25" / "bit-puncturing",
    REPO_ROOT / "research" / "v25" / "boundary-syndrome",
):
    dep = str(dep_dir)
    if dep not in sys.path:
        sys.path.insert(0, dep)
