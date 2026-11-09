
from pathlib import Path
import sys
import runpy

BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "app"
APP_FILE = APP_DIR / "streamlit_app.py"

if not APP_FILE.exists():
    raise FileNotFoundError(f"App file not found: {APP_FILE}")

sys.path.insert(0, str(APP_DIR))

runpy.run_path(str(APP_FILE), run_name="__main__")
