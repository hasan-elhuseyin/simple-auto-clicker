import os
from constants import MACRO_FOLDER

def list_macros():
    os.makedirs(MACRO_FOLDER, exist_ok=True)
    return [f for f in os.listdir(MACRO_FOLDER) if f.endswith(".pkl")]
