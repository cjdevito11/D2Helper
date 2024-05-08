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
        #terrorTracker.hide_terror_interface()
    elif feature == "Rings":
        ringScore.show_ring_score_interface()
        runeHelper.hide_rune_interface()
        #terrorTracker.hide_terror_interface()
    elif feature == "Terror Tracker":
        #terrorTracker.show_terror_interface()
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

def toggle_menu(root):
    try:
        if menu_window.state() == "normal":  # If window is visible
            menu_window.withdraw()  # Hide it
        else:
            menu_window.deiconify()  # Show it
    except NameError:  # If the menu window doesn't exist, create it
        setup_menu_window(root)

def setup_menu_window(root):
    global menu_window
    menu_window = tk.Toplevel(root)
    menu_window.overrideredirect(True);
    menu_window.attributes("-topmost", True)
    menu_window.geometry("200x100+1270+45")  # Position right below the "^" button
    menu_window.attributes("-alpha", 0.9)  # Slightly less transparent

    # Setup the dropdown menu within this window
    feature_options = ["Terror Tracker", "Runes", "Rings", "Close"]
    feature_dropdown = ttk.Combobox(menu_window, values=feature_options, state="readonly")
    feature_dropdown.current(0)  # Default to Terror Tracker
    feature_dropdown.pack()
    feature_dropdown.bind("<<ComboboxSelected>>", lambda event: feature_selected(event, root))

    setup_main_components(menu_window)

def setup_main_components(menu_window):
    # Setup other components like runeHelper and ringScore interfaces here
    runeHelper.setup_rune_interface(menu_window)
    runeHelper.hide_rune_interface()
    ringScore.setup_ring_score_interface(menu_window)
    ringScore.hide_ring_score_interface()

    # Add any other initialization as needed
    
    
def main():
    print("Setting up the main window...")
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.geometry('25x25+1275+15')

    # Set the background to a specific color that will be made transparent
    root.config(bg='white')
    root.attributes('-transparentcolor', 'white')

    expand_button = tk.Button(root, text="^", command=lambda: toggle_menu(root))
    expand_button.pack(fill="both", expand=True)
    expand_button.config(bg='grey')
    
    terrorTracker.setup_terror_tracker(root)
    terrorTracker.show_terror_tracker()  # Assuming this initializes and shows the terror tracker
    
    root.mainloop()

if __name__ == "__main__":
    main()