import tkinter as tk
from tkinter import ttk

def setup_rune_interface(root):
    global rune_interface
    rune_interface = ttk.Frame(root)
    # Add rune-related widgets to rune_interface
    # ...

def show_rune_interface():
    rune_interface.pack(fill='both', expand=True)

def hide_rune_interface():
    rune_interface.pack_forget()
