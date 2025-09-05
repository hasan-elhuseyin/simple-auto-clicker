import os
import time
import pickle
import threading
from pynput import mouse, keyboard
from src.overlay import show_overlay
from src.constants import MACRO_FOLDER, DEFAULT_MACRO

# ------------------ Globals ------------------
events = []
start_time = None
mode = "idle"  # idle | recording | replaying
current_macro_file = os.path.join(MACRO_FOLDER, DEFAULT_MACRO)
cycle_count = 0

replay_thread = None

kb = keyboard.Controller()
ms = mouse.Controller()

# ------------------ Recording ------------------
def start_recording(status_callback=None):
    global events, start_time, mode
    if mode != "idle":
        return
    events = []
    start_time = time.time()
    mode = "recording"
    if status_callback:
        status_callback("🎤 Recording...")
    show_overlay("Recording Started")

def stop_recording(status_callback=None):
    global events, mode, current_macro_file
    if not current_macro_file or os.path.isdir(current_macro_file):
        current_macro_file = os.path.join(MACRO_FOLDER, DEFAULT_MACRO)
    os.makedirs(MACRO_FOLDER, exist_ok=True)
    with open(current_macro_file, "wb") as f:
        pickle.dump(events, f)
    mode = "idle"
    if status_callback:
        status_callback(f"✅ Saved: {os.path.basename(current_macro_file)}")
    show_overlay("Recording Stopped")

# ------------------ Replay ------------------
def replay_loop(status_callback=None):
    global mode, cycle_count
    try:
        with open(current_macro_file, "rb") as f:
            recorded = pickle.load(f)
    except FileNotFoundError:
        if status_callback:
            status_callback("⚠️ No macro recorded!")
        show_overlay("No macro recorded!")
        return

    mode = "replaying"
    cycle_count = 0

    while mode == "replaying":
        cycle_count += 1
        if status_callback:
            status_callback(f"▶️ Replaying (Cycle {cycle_count})")
        # overlay removed inside loop

        start = time.time()
        for e in recorded:
            if mode != "replaying":
                break

            delay = e[-1]
            time.sleep(max(0, start + delay - time.time()))

            if e[0] == "mouse":
                _, x, y, button, pressed, _ = e
                ms.position = (x, y)
                if pressed:
                    ms.press(button)
                else:
                    ms.release(button)
            elif e[0] == "key":
                _, key, pressed, _ = e
                try:
                    if pressed:
                        kb.press(key)
                    else:
                        kb.release(key)
                except Exception:
                    pass

    # Show overlay only once after replay stops
    if status_callback:
        status_callback("⏹ Idle")
    show_overlay(f"Replayed {cycle_count} cycle{'s' if cycle_count > 1 else ''}")
    mode = "idle"

def start_replay(status_callback=None):
    """Replay toggle: start if idle, stop if replaying."""
    global replay_thread, mode
    if mode == "replaying":
        stop_replay(status_callback)
        return
    if mode != "idle":
        return  # do not start if recording

    replay_thread = threading.Thread(target=replay_loop, args=(status_callback,), daemon=True)
    replay_thread.start()

def stop_replay(status_callback=None):
    global mode
    if mode == "replaying":
        mode = "idle"
        if status_callback:
            status_callback("⏹ Idle")

# ------------------ Input Listeners ------------------
def on_click(x, y, button, pressed):
    if mode == "recording":
        events.append(("mouse", x, y, button, pressed, time.time() - start_time))

def on_press(key, status_callback=None, record_key='0', replay_key='-'):
    global mode, events
    try:
        # Recording toggle
        if hasattr(key, 'char') and key.char == record_key:
            if mode == "idle":
                start_recording(status_callback)
            elif mode == "recording":
                stop_recording(status_callback)
            return

        # Replay toggle
        if hasattr(key, 'char') and key.char == replay_key:
            start_replay(status_callback)
            return

        # Stop key (ESC)
        if hasattr(key, 'name') and key.name == 'esc' and mode == "replaying":
            stop_replay(status_callback)
            return

        # Record key events
        if mode == "recording":
            events.append(("key", key, True, time.time() - start_time))
    except Exception as e:
        print(f"Listener error: {e}")

def on_release(key):
    if mode == "recording":
        events.append(("key", key, False, time.time() - start_time))

# ------------------ Macro Selection ------------------
def set_macro_file(file_name):
    global current_macro_file
    os.makedirs(MACRO_FOLDER, exist_ok=True)

    if not file_name or file_name.endswith(os.sep):
        file_name = DEFAULT_MACRO
    elif not file_name.endswith(".pkl"):
        file_name += ".pkl"

    current_macro_file = os.path.join(MACRO_FOLDER, file_name)

# ------------------ Initialization ------------------
def initialize_macros():
    os.makedirs(MACRO_FOLDER, exist_ok=True)
    default_file_path = os.path.join(MACRO_FOLDER, DEFAULT_MACRO)
    if not os.path.isfile(default_file_path):
        with open(default_file_path, "wb") as f:
            pickle.dump([], f)

initialize_macros()
