import tkinter as tk
from pynput import mouse, keyboard
from constants import RECORD_KEY, REPLAY_KEY, STOP_KEY
import macro

# ------------------ UI ------------------
root = tk.Tk()
root.title("Simple Auto Clicker")
root.geometry("300x250")

status_var = tk.StringVar(value="⏹ Idle")
status_label = tk.Label(root, textvariable=status_var, font=("Arial", 14))
status_label.pack(pady=10)

record_btn = tk.Button(root, text=f"Toggle Recording ({RECORD_KEY})", width=25,
                       command=lambda: macro.start_recording(status_var.set) if macro.mode=="idle" else macro.stop_recording(status_var.set))
record_btn.pack(pady=5)

play_btn = tk.Button(root, text=f"Start Replay ({REPLAY_KEY})", width=25,
                     command=lambda: macro.start_replay(status_var.set))
play_btn.pack(pady=5)

stop_play_btn = tk.Button(root, text=f"Stop Replay ({STOP_KEY.upper()})", width=25,
                          command=lambda: macro.stop_replay(status_var.set))
stop_play_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Exit", width=25, command=root.quit)
exit_btn.pack(pady=5)

# ------------------ Listeners ------------------
ml = mouse.Listener(on_click=macro.on_click)
kl = keyboard.Listener(
    on_press=lambda key: macro.on_press(key, status_var.set, RECORD_KEY, REPLAY_KEY, STOP_KEY),
    on_release=macro.on_release
)
ml.start()
kl.start()

root.mainloop()
