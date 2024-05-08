import tkinter as tk
from tkinter import ttk

def schedule_periodic_update(root, callback, interval):
    """ Schedule periodic updates for a given callback function.

    Args:
        root (tk.Tk): The main application root.
        callback (function): The callback function to run periodically.
        interval (int): The time interval in milliseconds.
    """
    callback()  # Call the callback function immediately
    root.after(interval, lambda: schedule_periodic_update(root, callback, interval))
