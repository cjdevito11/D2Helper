import pyautogui
import time
import pytesseract
from pytesseract import Output
from PIL import Image
import sys
import subprocess

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

def locate_on_screen(image_path, retries=5, delay=2):
    """Attempt to locate an element on screen, retrying a specified number of times."""
    for _ in range(retries):
        try:
            position = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)
            if position:
                print(f"position:{position}")
                return position
            time.sleep(delay)
        except:
            print(f"Failed to locate {image_path} on screen... position: {position}")
    return None
    
def capture_screen(region=None):
    return pyautogui.screenshot(region=region)

def read_screen_text(region=None):
    """Capture the screen and use OCR to extract text."""
    img = capture_screen(region)
    text = pytesseract.image_to_string(img)
    return text

def read_screen_text_with_coordinates():
    """Capture the screen and use OCR to extract text along with their bounding boxes."""
    img = pyautogui.screenshot()  # Capture the entire screen or define a specific region if needed
    data = pytesseract.image_to_data(img, output_type=Output.DICT)
    return data
    
def wait_for_login_screen(login_screen_image):
    """Wait indefinitely until the login screen is detected."""
    print("Waiting for the login screen...")
    while True:
        screen_pos = locate_on_screen(login_screen_image)
        if screen_pos:
            print("Login screen detected.")
            return True
        time.sleep(1)  # Check every second

def login():
    """Perform the login process."""
    with open("password.txt", "r") as file:
        user_password = file.read().strip()
    if wait_for_login_screen('loginscreen.png'):
        password_pos = locate_on_screen('password.png')
        if password_pos:
            pyautogui.click(password_pos)
            pyautogui.write(password, interval=0.05)
            
            login_button_pos = locate_on_screen('login.png')
            if login_button_pos:
                pyautogui.click(login_button_pos)
                print("Login successful!")
                startDiablo()
                print("Starting Diablo")
            else:
                print("Login button not found.")
        else:
            print("Password box not found.")

def startDiablo():
    time.sleep(10)
    d2r_pos = locate_on_screen('d2rlogo.png')
    if d2r_pos:
        pyautogui.click(d2r_pos)
        time.sleep(5)
        playd2r_pos = locate_on_screen('playd2r.png')
        if playd2r_pos:
            pyautogui.click(playd2r_pos)
            time.sleep(5)
            pyautogui.click(playd2r_pos)
            time.sleep(5)
            pyautogui.click(playd2r_pos)
            time.sleep(6)
            pyautogui.click(playd2r_pos)
            time.sleep(7)
            pyautogui.click(playd2r_pos)
            
def selectOffline():
    time.sleep(10)
    offline_pos = locate_on_screen('offline.png')
    pyautogui.click(offline_pos)
    
def selectOffline():
    time.sleep(10)
    online = locate_on_screen('online.png')
    pyautogui.click(online)
            
def selectCharacter(characterName):
    time.sleep(4)
    try:
        print("Looking for character:", characterName)
        imgName = characterName + '.png'
        print("Looking for character:", imgName)
        char_pos = locate_on_screen(imgName)
        if char_pos:
            pyautogui.click(char_pos)
            pyautogui.click(char_pos)
    except:
        print(f"failed to select character: {characterName} @ {char_pos} .. imgName: {imgName}")

def enter_game(game_name, password):
    # Coordinates for each click can be set here
    # Example coordinates are placeholders and should be replaced with actual coordinates
    lobby_pos = (1100, 1050)  # Replace with actual coordinates
    join_game_pos = (1450, 750)  # Replace with actual coordinates
    game_name_pos = (1480, 175)  # Replace with actual coordinates
    password_pos = (1775, 175)  # Replace with actual coordinates
    
    # Check if you need to Enter the lobby
    pyautogui.click(lobby_pos)
    time.sleep(2)
    # Enter Game Name
    pyautogui.click(game_name_pos)
    print(f"Writing game_name - {game_name}.")
    for _ in range(10):
        pyautogui.press('backspace')
    pyautogui.write(game_name, interval=0.05)
    time.sleep(3)
    
    # Enter Password
    pyautogui.click(password_pos)
    print(f"Writing password - {password}.")
    for _ in range(10):
        pyautogui.press('backspace')
    pyautogui.write(password, interval=0.05)
    time.sleep(3)
    
    # Click on Join Game
    print(f"Joining Game.")
    pyautogui.click(join_game_pos)
    time.sleep(15)