import sys
from pathlib import Path

# add backend dir to path so our app modules resolve
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.main import app
