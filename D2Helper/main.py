import tkinter as tk
from tkinter import ttk
import threading
from config import *
import events
import runeHelper
import ringScore
import terrorTracker
from terrorTracker import setup_terror_tracker, show_terror_tracker, hide_terror_tracker


def feature_selected(event, root):
    feature = event.widget.get()
    if feature == "Runes":
        runeHelper.show_rune_interface()
        ringScore.hide_ring_score_interface()
        terrorTracker.hide_terror_tracker()
    elif feature == "Rings":
        ringScore.show_ring_score_interface()
        runeHelper.hide_rune_interface()
        terrorTracker.hide_terror_tracker()
    elif feature == "Terror Tracker":
        terrorTracker.show_terror_tracker()
        runeHelper.hide_rune_interface()
        ringScore.hide_ring_score_interface()
    elif feature == "Close":
        root.destroy()  # This will close the application

def setup_main_window(root):
    feature_options = ["Terror Tracker", "Runes", "Rings", "Close"]
    feature_dropdown = ttk.Combobox(root, values=feature_options, state="readonly")
    feature_dropdown.current(0)  # Default to Terror Tracker
    feature_dropdown.pack()
    feature_dropdown.bind("<<ComboboxSelected>>", lambda event: feature_selected(event, root))
    
    # Initially show the Terror Tracker
    terrorTracker.setup_terror_tracker(root)
    terrorTracker.show_terror_tracker()
    runeHelper.setup_rune_interface(root)
    runeHelper.hide_rune_interface()
    ringScore.setup_ring_score_interface(root)
    ringScore.hide_ring_score_interface()

def main():
    print("Setting up the main window...")
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.geometry("200x60+1270+15")  # Adjusted to be in the top right
    #root.geometry("200x200+500+200")
    root.attributes("-alpha", 0.8)
    root.configure(bg=dark_background_color)
    
    setup_main_window(root)
    print("Main window setup complete.")
    
    root.mainloop()

if __name__ == "__main__":
    main()
