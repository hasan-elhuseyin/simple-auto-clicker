import tkinter as tk
import threading
import time
from src.constants import OVERLAY_DURATION, OVERLAY_ALPHA

def show_overlay(message, duration=OVERLAY_DURATION):
    overlay = tk.Toplevel()
    overlay.overrideredirect(True)
    overlay.attributes("-topmost", True)
    overlay.attributes("-alpha", OVERLAY_ALPHA)
    overlay.configure(bg="black")

    label = tk.Label(overlay, text=message, font=("Arial", 20), fg="white", bg="black")
    label.pack(padx=20, pady=10)

    overlay.update_idletasks()
    w = overlay.winfo_width()
    h = overlay.winfo_height()
    ws = overlay.winfo_screenwidth()
    hs = overlay.winfo_screenheight()
    x = (ws - w) // 2
    y = hs // 5
    overlay.geometry(f"{w}x{h}+{x}+{y}")

    def close_after():
        time.sleep(duration)
        overlay.destroy()

    threading.Thread(target=close_after, daemon=True).start()
