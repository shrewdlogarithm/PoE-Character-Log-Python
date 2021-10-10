import sys,os

# Pyinstaller --onefile data directory handler
base_path = ""
try:
    base_path = sys._MEIPASS + "\\"
except Exception:
    base_path = os.path.abspath(".") + "\\"
