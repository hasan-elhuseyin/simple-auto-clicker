import time
import pickle
import threading
from pynput import mouse, keyboard
from constants import MACRO_FILE
from overlay import show_overlay

events = []
start_time = None
mode = "idle"  # idle | recording | replaying

kb = keyboard.Controller()
ms = mouse.Controller()

# ------------------ Core Functions ------------------
def start_recording(status_callback=None):
    global events, start_time, mode
    events = []
    start_time = time.time()
    mode = "recording"
    if status_callback:
        status_callback("🎤 Recording...")
    show_overlay("Recording Started")

def stop_recording(status_callback=None):
    global events, mode
    with open(MACRO_FILE, "wb") as f:
        pickle.dump(events, f)
    mode = "idle"
    if status_callback:
        status_callback("✅ Saved recording")
    show_overlay("Recording Stopped")

def replay_loop(status_callback=None):
    global mode
    try:
        with open(MACRO_FILE, "rb") as f:
            recorded = pickle.load(f)
    except FileNotFoundError:
        if status_callback:
            status_callback("⚠️ No macro recorded!")
        show_overlay("No macro recorded!")
        return

    mode = "replaying"
    if status_callback:
        status_callback("▶️ Replaying...")
    show_overlay("Replay Started")

    while mode == "replaying":
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

    if status_callback:
        status_callback("⏹ Idle")
    show_overlay("Replay Stopped")

def start_replay(status_callback=None):
    t = threading.Thread(target=replay_loop, args=(status_callback,), daemon=True)
    t.start()

def stop_replay(status_callback=None):
    global mode
    mode = "idle"
    if status_callback:
        status_callback("⏹ Idle")

# ------------------ Listeners ------------------
def on_click(x, y, button, pressed):
    if mode == "recording":
        events.append(("mouse", x, y, button, pressed, time.time() - start_time))

def on_press(key, status_callback=None, record_key='0', replay_key='=', stop_key='esc'):
    global mode, events
    if hasattr(key, 'char') and key.char == record_key:
        if mode == "idle":
            start_recording(status_callback)
        elif mode == "recording":
            stop_recording(status_callback)
        return
    if hasattr(key, 'char') and key.char == replay_key and mode == "idle":
        start_replay(status_callback)
        return
    if hasattr(key, 'name') and key.name == stop_key and mode == "replaying":
        stop_replay(status_callback)
        return

    if mode == "recording":
        events.append(("key", key, True, time.time() - start_time))

def on_release(key):
    global events
    if mode == "recording":
        events.append(("key", key, False, time.time() - start_time))
