import win32gui
import easygui
import time

def get_window_at_mouse():
    x, y = win32gui.GetCursorPos()
    return win32gui.WindowFromPoint((x, y))

def confirm_window(hwnd):
    window_title = win32gui.GetWindowText(hwnd)
    return easygui.ynbox(f"Is this the correct window?\n\nTitle: {window_title}", "Confirm Window")

def rename_window(hwnd, new_title):
    win32gui.SetWindowText(hwnd, new_title)
    print(f"Window renamed to '{new_title}'")

def setup_windows(config):
    labeled_hwnds = set()

    for loader in config["loaders"]:
        easygui.msgbox(f"Click on the window you want to label as '{loader['name']}'.", "Select Window")
        while True:
            #time.sleep(3)
            hwnd = get_window_at_mouse()
            if hwnd not in labeled_hwnds and hwnd != 0:
                if confirm_window(hwnd):
                    rename_window(hwnd, loader['name'])
                    loader["window_title"] = loader['name']
                    labeled_hwnds.add(hwnd)
                    break
                else:
                    easygui.msgbox("Please try selecting the window again.", "Try Again")
            else:
                easygui.msgbox("Invalid selection or window already labeled. Try again.", "Error")

    #save_config(config)
    easygui.msgbox("All windows have been labeled successfully!", "Done")

if __name__ == "__main__":
    setup_windows()
