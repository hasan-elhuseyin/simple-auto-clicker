import tkinter as tk
from tkinter import simpledialog
import macro
from macro_manager import list_macros
from constants import RECORD_KEY, REPLAY_KEY
from pynput import mouse, keyboard

# ------------------ UI ------------------
root = tk.Tk()
root.title("Simple Auto Clicker")
root.geometry("450x400")

status_var = tk.StringVar(value="⏹ Idle")
status_label = tk.Label(root, textvariable=status_var, font=("Arial", 14))
status_label.pack(pady=10)

# ------------------ Recording Button ------------------
record_btn = tk.Button(
    root, 
    text=f"Toggle Recording ({RECORD_KEY})", 
    width=35,
    command=lambda: macro.start_recording(status_var.set) if macro.mode=="idle" else macro.stop_recording(status_var.set)
)
record_btn.pack(pady=5)

# ------------------ Replay Toggle Button ------------------
replay_btn = tk.Button(
    root,
    text=f"Toggle Replay ({REPLAY_KEY})",
    width=35,
    command=lambda: macro.start_replay(status_var.set)
)
replay_btn.pack(pady=5)

# ------------------ Macro Dropdown ------------------
macro_label = tk.Label(root, text="Select Macro:")
macro_label.pack(pady=5)

macro_list = list_macros()
macro_var = tk.StringVar()
default_macro = macro_list[0] if macro_list else ""
macro_var.set(default_macro)
macro.set_macro_file(default_macro)

macro_dropdown = tk.OptionMenu(root, macro_var, *macro_list)
macro_dropdown.pack(pady=5)

# Bind proper macro selection
def on_macro_select(*args):
    macro.set_macro_file(macro_var.get())

macro_var.trace_add("write", on_macro_select)

# ------------------ Create New Macro ------------------
def create_new_macro():
    name = simpledialog.askstring("Create New Macro", "Enter new macro name (without .pkl):")
    if not name:
        return
    if not name.endswith(".pkl"):
        name += ".pkl"
    macro.set_macro_file(name)
    macro.stop_recording(status_var.set)  # save empty macro if no events

    # Refresh dropdown
    macros = list_macros()
    menu = macro_dropdown["menu"]
    menu.delete(0, "end")
    for m in macros:
        menu.add_command(label=m, command=lambda value=m: macro_var.set(value))
    macro_var.set(name)
    status_var.set(f"✅ Created macro: {name}")

create_macro_btn = tk.Button(root, text="Create New Macro", command=create_new_macro)
create_macro_btn.pack(pady=5)

# ------------------ Exit ------------------
exit_btn = tk.Button(root, text="Exit", width=35, command=root.quit)
exit_btn.pack(pady=5)

# ------------------ Listeners ------------------
ml = mouse.Listener(on_click=macro.on_click)
kl = keyboard.Listener(
    on_press=lambda key: macro.on_press(key, status_var.set, RECORD_KEY, REPLAY_KEY),
    on_release=macro.on_release
)
ml.start()
kl.start()

root.mainloop()
