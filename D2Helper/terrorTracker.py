import tkinter as tk
from tkinter import ttk

def setup_terror_tracker(root):
    global terror_tracker_interface
    terror_tracker_interface = ttk.Frame(root)
    # Initialize and place terror tracker-related widgets here
    # Example: Add a label or any other components to this frame
    label = ttk.Label(terror_tracker_interface, text="Next Terror Zone: None")
    label.pack()

def show_terror_tracker():
    terror_tracker_interface.pack(fill='both', expand=True)

def hide_terror_tracker():
    terror_tracker_interface.pack_forget()
