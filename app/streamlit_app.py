
from pathlib import Path
import sys
import runpy

# Locate the actual Streamlit application
BASE_DIR = Path(__file__).resolve().parent
APP_DIR = BASE_DIR / "app"
APP_FILE = APP_DIR / "streamlit_app.py"

# Check that the application file exists
if not APP_FILE.exists():
    raise FileNotFoundError(
        f"Streamlit application not found: {APP_FILE}"
    )

# Make the app folder available for imports
# This ensures the correct caption_generator_api.py is loaded.
app_dir = str(APP_DIR)

if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Launch the actual application
runpy.run_path(
    str(APP_FILE),
    run_name="__main__"
)
