import pyautogui
import time
import pytesseract
from pytesseract import Output
from PIL import Image
import sys
import tkinter as tk
from tkinter import ttk
import setup
import mouse

pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

game_name = ''
# Function to confirm if in Act 5 (placeholder, needs implementation)
def confirm_act5():
    pass

def prebuff():
    pyautogui.press('F6')
    mouse.click('right')
    pyautogui.press('F3')

def wait_for_tp_and_confirm_leader(leader_name):
    print("Starting to search for TPs...")
    while True:
        try:
            tp_positions = list(pyautogui.locateAllOnScreen('tp.png', confidence=0.7))
            if tp_positions:
                for tp_pos in tp_positions:
                    pyautogui.moveTo(tp_pos)
                    x, y, w, h = tp_pos.left, tp_pos.top, tp_pos.width, tp_pos.height  # Adjust to top-left corner
                    text_region = (x - 100, y - 100), (x + 100, y - 50)
                    #text = setup.read_screen_text(region=text_region)
                    #if leader_name in text:
                    print(f"Leader's TP found at ({x}, {y}).")
                    prebuff()
                    time.sleep(15) # wait 15 seconds for safety
                    pyautogui.click(tp_pos)
                    pyautogui.click(tp_pos)
                    return
                    #else:
                    #    print(f"TP at ({x}, {y}) is not the leader's TP.")
            else:
                print("No TP found, retrying...")
            time.sleep(7)
        except:
            print("failed tp")
            time.sleep(5)


# Function to wait for leader to leave and rejoin the next game
def wait_for_leader_to_leave(leader, game_name, password):
    while True:
        chat_text = setup.read_screen_text(region=(0, 650, 600, 930))  # Adjust region to match chat area
        if f"{leader} left our world" in chat_text:
            print("Leader has left the world")
            save_and_quit()
            next_game_name = increment_game_name(game_name)
            loop_script(leader, next_game_name,password)
            #while True:
                #enter_game(next_game_name, password)
                #time.sleep(10)
                #chat_text = setup.read_screen_text(region=(0, 650, 600, 930))  # Adjust region to match chat area
                #if "Your connection has been interrupted" not in chat_text:
                    #break
            break

def save_and_quit():
    esc_pos = (800, 1150)
    save_and_quit_pos = (950, 525)  # Replace with actual coordinates
    pyautogui.click(esc_pos)
    time.sleep(1)
    pyautogui.click(save_and_quit_pos)

def increment_game_name(game_name):
    try:
        base_name, num = game_name.rsplit('-', 1)
        print(f"Base name: {base_name}, Current number: {num}")
        next_num = (int(num) % 99) + 1
        next_game_name = f"{base_name}-{next_num:02d}"
        print(f"Next game name: {next_game_name}")
        return next_game_name
    except Exception as e:
        print(f"Error incrementing game name: {e}")
        return game_name  # Return the original game name if there's an error


# Function to enter game
def enter_game(game_name, password):
    setup.enter_game(game_name, password)

def loop_script(leader,game_name,password):
    enter_game(game_name, password)
    confirm_act5()
    wait_for_tp_and_confirm_leader(leader)
    wait_for_leader_to_leave(leader, game_name, password)

# GUI setup using Tkinter
def create_gui():
    root = tk.Tk()
    root.title("Diablo 2 Automator")
    root.geometry("300x350+1610+750")
    root.attributes('-alpha', 0.9)
    root.attributes('-topmost', True)

    tk.Label(root, text="Game Name").pack()
    game_name_entry = tk.Entry(root)
    game_name_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    tk.Label(root, text="Leader").pack()
    leader_entry = tk.Entry(root)
    leader_entry.pack()

    tk.Label(root, text="Leach Area").pack()
    leach_area = ttk.Combobox(root, values=["Baal"])
    leach_area.current(0)
    leach_area.pack()
    
    
    def start_script():
        game_name = game_name_entry.get()
        password = password_entry.get()
        leader = leader_entry.get()
        enter_game(game_name, password)
        confirm_act5()
        wait_for_tp_and_confirm_leader(leader)
        wait_for_leader_to_leave(leader, game_name, password)
        #restart_script()

    def stop_script():
        sys.exit()

    def restart_script():
        start_script()
        
    login_button = tk.Button(root, text="Login", command=setup.login)
    login_button.pack()

    start_button = tk.Button(root, text="Start", command=start_script)
    start_button.pack()

    stop_button = tk.Button(root, text="Stop", command=stop_script)
    stop_button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
