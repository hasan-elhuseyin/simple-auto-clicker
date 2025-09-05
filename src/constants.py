import os

# Hotkeys
RECORD_KEY = '0'
REPLAY_KEY = '-'
STOP_KEY = 'esc'

# Overlay settings
OVERLAY_DURATION = 1.5
OVERLAY_ALPHA = 0.8

# Macro settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # parent of src
MACRO_FOLDER = os.path.join(BASE_DIR, "macros")  # folder at same level as src
DEFAULT_MACRO = "default_macro.pkl"
