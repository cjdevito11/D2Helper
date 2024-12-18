import win32gui
import win32con
import pyautogui
import easygui
import time

# Function to get the window handle at the current mouse position
def get_window_at_mouse():
    x, y = pyautogui.position()
    hwnd = win32gui.WindowFromPoint((x, y))
    return hwnd

# Function to confirm the window selection with a popup
def confirm_window(hwnd):
    window_title = win32gui.GetWindowText(hwnd)
    return easygui.ynbox(f"Is this the correct window?\n\nTitle: {window_title}", "Confirm Window")

# Function to rename the window
def rename_window(hwnd, new_title):
    win32gui.SetWindowText(hwnd, new_title)
    print(f"Window renamed to '{new_title}'")

# Main function to label multiple windows
def label_windows():
    instance_count = 4  # Number of instances you want to label
    labeled_hwnds = set()

    for i in range(1, instance_count + 1):
        easygui.msgbox(f"Click on the window you want to label as 'Diablo II - Instance {i}'.", "Select Window")

        while True:
            hwnd = get_window_at_mouse()
            if hwnd not in labeled_hwnds and hwnd != 0:
                if confirm_window(hwnd):
                    new_title = f"Diablo II - Instance {i}"
                    rename_window(hwnd, new_title)
                    labeled_hwnds.add(hwnd)
                    break
                else:
                    easygui.msgbox("Please try selecting the window again.", "Try Again")
            else:
                easygui.msgbox("Invalid selection or window already labeled. Try again.", "Error")

    easygui.msgbox("All windows have been labeled successfully!", "Done")

# Run the main function
if __name__ == "__main__":
    label_windows()
