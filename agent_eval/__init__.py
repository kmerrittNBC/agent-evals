"""Source-tree import shim for `python -m agent_eval`."""
from pathlib import Path
__path__.append(str(Path(__file__).resolve().parents[1] / "src" / "agent_eval"))
