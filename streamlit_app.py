"""Streamlit Cloud entry point."""
import sys
from pathlib import Path

# Ensure src is in path for imports
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import and run the main app
from web_app import main

if __name__ == "__main__":
    main()
