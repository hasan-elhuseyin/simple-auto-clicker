# src/overlay.py
import tkinter as tk
import threading
import time
from src.constants import OVERLAY_DURATION, OVERLAY_ALPHA

def show_overlay(message, duration=OVERLAY_DURATION, color="white"):
    overlay = tk.Toplevel()
    overlay.overrideredirect(True)
    overlay.attributes("-topmost", True)
    overlay.attributes("-alpha", OVERLAY_ALPHA)
    overlay.configure(bg="black")

    label = tk.Label(overlay, text=message, font=("Segoe UI", 20, "bold"), fg=color, bg="black")
    label.pack(padx=20, pady=10)

    overlay.update_idletasks()
    w, h = overlay.winfo_width(), overlay.winfo_height()
    ws, hs = overlay.winfo_screenwidth(), overlay.winfo_screenheight()
    overlay.geometry(f"{w}x{h}+{(ws-w)//2}+{hs//5}")

    def animate():
        alpha = OVERLAY_ALPHA
        overlay.attributes("-alpha", alpha)
        time.sleep(duration)
        while alpha > 0:
            alpha -= 0.05
            overlay.attributes("-alpha", max(alpha,0))
            time.sleep(0.02)
        overlay.destroy()

    threading.Thread(target=animate, daemon=True).start()
