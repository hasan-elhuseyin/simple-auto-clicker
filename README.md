# Simple Auto Clicker

A lightweight cross-platform auto-clicker and macro recorder built in Python.
It allows you to record mouse and keyboard events and replay them endlessly with a single hotkey.

✨ Features:
- Record and replay mouse + keyboard events
- Hotkey controls (`0` for record, `-` for replay, `ESC` for stop)
- GUI with macro selection and management
- Use the "Create New Macro" in the GUI to save a new macro.
- Floating overlay notifications

⚠️ Notes
- Works on Windows, macOS, and Linux (requires python3-tk).
- Running with elevated permissions may be required for global key/mouse hooks.

---

## 🔧 Requirements

- Python 3.8+  
- [pynput](https://pypi.org/project/pynput/)  
- Tkinter (usually bundled with Python, but install `python3-tk` if missing)  

Install dependencies with:

```bash
pip install -r requirements.txt
```

## 🚀 Usage
```bash
python main.py
```

---

📂 Project Structure
```bash
simple-auto-clicker/
├── main.py              # Entry point
├── macros/              # Saved macro files (*.pkl)
└── src/
    ├── app.py           # Tkinter GUI
    ├── constants.py     # Hotkeys, paths, overlay settings
    ├── macro.py         # Recording/replaying logic
    ├── macro_manager.py # Macro listing utilities
    └── overlay.py       # Floating overlay system
```

---

📜 License
MIT License © 2025