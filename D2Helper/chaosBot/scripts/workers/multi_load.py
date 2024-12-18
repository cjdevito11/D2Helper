import time
from .config_loader import load_config
import win32gui
import win32api
import win32con

def send_keys_to_window(window_title, text):
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        print(f"Window '{window_title}' not found.")
        return

    for char in text:
        win32api.PostMessage(hwnd, win32con.WM_CHAR, ord(char), 0)
        time.sleep(0.06)  # Typing delay between characters

def send_click_to_window(window_title, x_percent, y_percent, button="left"):
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        print(f"Window '{window_title}' not found.")
        return

    # Get the window's dimensions
    window_rect = win32gui.GetWindowRect(hwnd)
    window_width = window_rect[2] - window_rect[0]
    window_height = window_rect[3] - window_rect[1]

    # Convert percentage-based coordinates to absolute positions
    win_x = int(window_width * x_percent)
    win_y = int(window_height * y_percent)

    # Calculate lparam for the click position
    lparam = win_x | (win_y << 16)

    if button == "left":
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
        time.sleep(0.05)
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lparam)
    elif button == "right":
        win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lparam)
        time.sleep(0.05)
        win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, None, lparam)

def multi_load_script(game_name, password):
    config = load_config()
    windows = [loader["window_title"] for loader in config["loaders"] if loader["window_title"]]

    print(f"Starting multi-load for windows: {windows}")
    time.sleep(5)

    for window in windows:
        print(f"Joining game on window: {window}")
        send_click_to_window(window, 500, 500)  # Example coordinates for clicking 'Join Game'
        time.sleep(1)  # Delay between actions

    print("Multi-load complete.")

if __name__ == "__main__":
    multi_load_script("GameName123", "Password123")
