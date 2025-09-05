import time
import pickle
import threading
import tkinter as tk
from pynput import mouse, keyboard

# ------------------ CONFIGURABLE HOTKEYS ------------------
RECORD_KEY = '0'   # Toggle recording on/off
REPLAY_KEY = '-'   # Start replay loop
STOP_KEY = 'esc'   # Stop replay (use 'esc' as string)

# ------------------ GLOBALS ------------------
events = []
start_time = None
mode = "idle"   # idle | recording | replaying
macro_file = "macro.pkl"

kb = keyboard.Controller()
ms = mouse.Controller()

# ------------------ CORE FUNCTIONS ------------------
def start_recording():
    global events, start_time, mode
    events = []
    start_time = time.time()
    mode = "recording"
    status_var.set("🎤 Recording...")

def stop_recording():
    global events, mode
    with open(macro_file, "wb") as f:
        pickle.dump(events, f)
    mode = "idle"
    status_var.set("✅ Saved recording")

def replay_loop():
    global mode
    try:
        with open(macro_file, "rb") as f:
            recorded = pickle.load(f)
    except FileNotFoundError:
        status_var.set("⚠️ No macro recorded!")
        return

    status_var.set("▶️ Replaying... (press Stop/ESC)")
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
    status_var.set("⏹ Idle")

def start_replay():
    t = threading.Thread(target=replay_loop, daemon=True)
    t.start()

def stop_replay():
    global mode
    mode = "idle"
    status_var.set("⏹ Idle")

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
    # Start replay
    if hasattr(key, 'char') and key.char == REPLAY_KEY and mode == "idle":
        start_replay()
        return
    # Stop replay
    if hasattr(key, 'name') and key.name == STOP_KEY and mode == "replaying":
        stop_replay()
        return

    if mode == "recording":
        events.append(("key", key, True, time.time() - start_time))

def on_release(key):
    if mode == "recording":
        events.append(("key", key, False, time.time() - start_time))

# ------------------ UI ------------------
root = tk.Tk()
root.title("Auto Clicker Macro")
root.geometry("300x250")

status_var = tk.StringVar(value="⏹ Idle")
status_label = tk.Label(root, textvariable=status_var, font=("Arial", 14))
status_label.pack(pady=10)

record_btn = tk.Button(root, text=f"Toggle Recording ({RECORD_KEY})", width=25,
                       command=lambda: start_recording() if mode=="idle" else stop_recording())
record_btn.pack(pady=5)

play_btn = tk.Button(root, text=f"Start Replay ({REPLAY_KEY})", width=25, command=start_replay)
play_btn.pack(pady=5)

stop_play_btn = tk.Button(root, text=f"Stop Replay ({STOP_KEY.upper()})", width=25, command=stop_replay)
stop_play_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Exit", width=25, command=root.quit)
exit_btn.pack(pady=5)

# Start listeners
ml = mouse.Listener(on_click=on_click)
kl = keyboard.Listener(on_press=on_press, on_release=on_release)
ml.start()
kl.start()

root.mainloop()
