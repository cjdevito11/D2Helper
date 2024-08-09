import tkinter as tk
from tkinter import ttk
import threading
from config import *
import events
import runeHelper
import ringScore
import terrorTracker
from terrorTracker import setup_terror_tracker, show_terror_tracker, hide_terror_tracker
from utils import load_config, shut_down, print_mouse_coords_relative_to_hwnd, click_saved_position, count_images_on_screen, get_rune_positions, get_rune_sort_key, sort_runes, move_item

hotkeys_registered = False
shutdown_flag = False

def feature_selected(event, root):
    feature = event.widget.get()
    if feature == "Runes":
        runeHelper.show_rune_interface()
        ringScore.hide_ring_score_interface()
        terrorTracker.hide_terror_tracker()
        adjust_menu_window_size("Runes")
    elif feature == "Rings":
        ringScore.show_ring_score_interface()
        runeHelper.hide_rune_interface()
        terrorTracker.hide_terror_tracker()
        adjust_menu_window_size("Rings")
    elif feature == "Terror Tracker":
        terrorTracker.show_terror_tracker()
        runeHelper.hide_rune_interface()
        ringScore.hide_ring_score_interface()
        adjust_menu_window_size("Terror Tracker")
    elif feature == "Close":
        root.destroy()  # This will close the application

def adjust_menu_window_size(feature):
    if feature == "Runes":
        menu_window.geometry("1000x300+1270+45")  # Adjust size for runes interface
    elif feature == "Rings":
        menu_window.geometry("600x400+1270+45")  # Adjust size for rings interface
    elif feature == "Terror Tracker":
        menu_window.geometry("800x400+1270+45")  # Adjust size for terror tracker

def setup_menu_window(root):
    global menu_window
    menu_window = tk.Toplevel(root)
    menu_window.overrideredirect(True)
    menu_window.attributes("-topmost", True)
    menu_window.geometry("200x100+1270+45")  # Initial size
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
    terrorTracker.setup_terror_tracker(menu_window)
    terrorTracker.show_terror_tracker()  # Show Terror Tracker by default

def register_hotkeys(hwnd):
    global hotkeys_registered
    if not hotkeys_registered:
        keyboard.add_hotkey('num 1', print_mouse_coords_relative_to_hwnd, args=(hwnd,))
        print("Press 'num 1' to print mouse coordinates relative to HWND.")
        keyboard.add_hotkey('num 2', click_saved_position, args=(hwnd,))
        print("Press 'num 2' to click at the saved position.")
        keyboard.add_hotkey('num 4', lambda: count_images_on_screen(r'C:\path\to\your\image.png'))
        print("Press 'num 4' to find location.")
        keyboard.add_hotkey('num 8', restart_script)
        print("Press 'num 8' to reload the script.")
        keyboard.add_hotkey('num 9', shut_down)
        print("Press 'num 9' to reload the script or close the window to exit.")
        hotkeys_registered = True

def main_loop(window_title_to_check):
    global hotkeys_registered
    while not shutdown_flag:
        result = functions.window_exists(window_title_to_check)
        if result:
            hwnd, (left, top, right, bottom) = result
            register_hotkeys(hwnd)
            time.sleep(1)
        else:
            print(f"Window '{window_title_to_check}' does not exist.")
            hotkeys_registered = False
            keyboard.unregister_all_hotkeys()
            time.sleep(1)

def main():
    config = load_config()
    window_title_to_check = config.get("window_title_to_check", "")

    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.geometry('25x25+1500+25')

    # Set the background to a specific color that will be made transparent
    root.config(bg='white')
    root.attributes('-transparentcolor', 'white')

    expand_button = tk.Button(root, text="^", command=lambda: toggle_menu(root))
    expand_button.pack(fill="both", expand=True)
    expand_button.config(bg='grey')

    setup_menu_window(root)  # Initialize the dropdown menu window

    threading.Thread(target=main_loop, args=(window_title_to_check,), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()
