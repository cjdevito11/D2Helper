import time
import win32gui
import win32api
import win32con
import keyboard
import threading

# Global variables to control script execution
running = True
paused = False

# Target window title for the background window
BACKGROUND_WINDOW_TITLE = "Diablo II - Instance 2"

def get_window_handle(title):
    """Get the window handle by title."""
    return win32gui.FindWindow(None, title)

def send_click_to_window(hwnd, x, y, button="left"):
    """Send a click to the specified window at (x, y) coordinates."""
    # Convert screen coordinates to window-relative coordinates
    window_rect = win32gui.GetWindowRect(hwnd)
    win_x = x - window_rect[0]
    win_y = y - window_rect[1]

    # Pack the coordinates into LPARAM format
    lparam = win_x | (win_y << 16)

    if button == "left":
        # Send left mouse down and up messages
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
        time.sleep(0.05)  # Short delay between down and up
        win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, lparam)
    elif button == "right":
        # Send right mouse down and up messages
        win32api.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lparam)
        time.sleep(0.05)  # Short delay between down and up
        win32api.PostMessage(hwnd, win32con.WM_RBUTTONUP, None, lparam)

def monitor_clicks():
    global running, paused

    # Get the handle of the background window
    target_hwnd = get_window_handle(BACKGROUND_WINDOW_TITLE)

    if not target_hwnd:
        print("Background window not found.")
        return

    print("Script is running. Press 'Ctrl + Z' to stop, 'Enter' to pause/resume.")

    while running:
        # Check for pause toggle
        if keyboard.is_pressed('enter'):
            paused = not paused
            state = "Paused" if paused else "Resumed"
            print(f"Script {state}.")
            time.sleep(0.5)  # Debounce delay to prevent rapid toggling

        if paused:
            time.sleep(0.1)
            continue

        # Detect left mouse click on the main window
        if win32api.GetAsyncKeyState(0x01):  # Left mouse button
            x, y = win32api.GetCursorPos()
            print(f"Left-click at ({x}, {y})")
            send_click_to_window(target_hwnd, x, y, button="left")
            time.sleep(0.1)  # Debounce delay

        # Detect right mouse click on the main window
        if win32api.GetAsyncKeyState(0x02):  # Right mouse button
            x, y = win32api.GetCursorPos()
            print(f"Right-click at ({x}, {y})")
            send_click_to_window(target_hwnd, x, y, button="right")
            time.sleep(0.1)  # Debounce delay

        # Stop condition
        if keyboard.is_pressed('ctrl+z'):
            running = False
            print("Stopping script.")

# Run the click duplication in a separate thread
thread = threading.Thread(target=monitor_clicks)
thread.start()
