import tkinter as tk
from tkinter import messagebox
import json
import os
import sys

# Load macros from macros.json
if getattr(sys, 'frozen', False):
    # If running as a bundled executable, use the folder of the executable
    BASE_PATH = os.path.dirname(sys.executable)
    MACROS_PATH = os.path.join(BASE_PATH, 'macros.json')
    if not os.path.exists(MACROS_PATH):
        # Try parent directory (for macOS .app bundles)
        PARENT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(BASE_PATH)))
        alt_path = os.path.join(PARENT_PATH, 'macros.json')
        if os.path.exists(alt_path):
            MACROS_PATH = alt_path
else:
    BASE_PATH = os.path.dirname(__file__)
    MACROS_PATH = os.path.join(BASE_PATH, 'macros.json')
def load_macros():
    with open(MACROS_PATH, 'r') as f:
        return json.load(f)

def expand_macros(text, macros):
    # Replace each macro key with its value, word by word
    for key, value in macros.items():
        text = text.replace(key, value)
    return text

def on_expand():
    try:
        macros = load_macros()
    except Exception as e:
        messagebox.showerror("Error", f"Could not load macros.json: {e}")
        return
    text = input_text.get("1.0", tk.END)
    if not text.strip():
        messagebox.showinfo("Info", "Input box is empty. Paste some text first.")
        return
    expanded = expand_macros(text, macros)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, expanded)

root = tk.Tk()
root.title("Macro Expander")
root.geometry("500x400")

label = tk.Label(root, text="Paste your text below, then click 'Expand Macros'", pady=10)
label.pack()

input_text = tk.Text(root, height=8, width=60)
input_text.pack(pady=5)

expand_btn = tk.Button(root, text="Expand Macros", command=on_expand, height=2, width=20)
expand_btn.pack(pady=10)

output_label = tk.Label(root, text="Expanded text (copy manually):")
output_label.pack()

output_text = tk.Text(root, height=8, width=60)
output_text.pack(pady=5)

root.mainloop()
