import os
import time
import pickle
import threading
from pynput import mouse, keyboard

# ------------------ CONFIGURABLE HOTKEYS ------------------
RECORD_KEY = '0'   # Toggle recording on/off
REPLAY_KEY = '-'   # Toggle replay on/off
STOP_KEY = 'esc'   # Emergency stop (always works)

# ------------------ GLOBALS ------------------
events = []
start_time = None
mode = "idle"   # idle | recording | replaying

# Ensure macros directory exists
MACRO_DIR = "macros"
os.makedirs(MACRO_DIR, exist_ok=True)
macro_file = os.path.join(MACRO_DIR, "macro.pkl")

kb = keyboard.Controller()
ms = mouse.Controller()


# ------------------ UTILS ------------------
def show_hotkeys():
    print(f"⏹ Idle")
    print(f"Hotkeys: Record[{RECORD_KEY}] | Replay[{REPLAY_KEY}] | EmergencyStop[{STOP_KEY.upper()}]")


# ------------------ CORE FUNCTIONS ------------------
def start_recording():
    global events, start_time, mode
    events = []
    start_time = time.time()
    mode = "recording"
    print("🎤 Recording... (press 0 again to stop)")


def stop_recording():
    global events, mode
    with open(macro_file, "wb") as f:
        pickle.dump(events, f)
    mode = "idle"
    print(f"✅ Saved recording → {macro_file}")
    show_hotkeys()


def replay_loop():
    global mode
    try:
        with open(macro_file, "rb") as f:
            recorded = pickle.load(f)
    except FileNotFoundError:
        print("⚠️ No macro recorded!")
        mode = "idle"
        show_hotkeys()
        return

    print("▶️ Replaying... (press - again or ESC to stop)")
    mode = "replaying"

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
    # no idle print here, handled by toggle_replay()


def toggle_replay():
    global mode
    if mode == "idle":
        t = threading.Thread(target=replay_loop, daemon=True)
        t.start()
    elif mode == "replaying":
        mode = "idle"
        print("⏹ Stopped replay")
        show_hotkeys()


def stop_all():
    """Emergency stop (ESC key)."""
    global mode
    mode = "idle"
    print("⏹ Emergency stop")
    show_hotkeys()


# ------------------ LISTENERS ------------------
def on_click(x, y, button, pressed):
    if mode == "recording":
        events.append(("mouse", x, y, button, pressed, time.time() - start_time))


def on_press(key):
    global events, mode

    # Toggle recording
    if hasattr(key, 'char') and key.char == RECORD_KEY:
        if mode == "idle":
            start_recording()
        elif mode == "recording":
            stop_recording()
        return

    # Toggle replay
    if hasattr(key, 'char') and key.char == REPLAY_KEY:
        toggle_replay()
        return

    # Emergency stop (ESC)
    if hasattr(key, 'name') and key.name == STOP_KEY:
        stop_all()
        return

    if mode == "recording":
        events.append(("key", key, True, time.time() - start_time))


def on_release(key):
    if mode == "recording":
        events.append(("key", key, False, time.time() - start_time))


# ------------------ MAIN ------------------
if __name__ == "__main__":
    show_hotkeys()

    ml = mouse.Listener(on_click=on_click)
    kl = keyboard.Listener(on_press=on_press, on_release=on_release)
    ml.start()
    kl.start()

    # Keep program alive
    ml.join()
    kl.join()
