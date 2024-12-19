import os
import pyautogui
import time
import pytesseract
from pytesseract import Output
from PIL import Image
import sys
import tkinter as tk
from tkinter import ttk
import mouse
import pygetwindow as gw
import setup
import subprocess
import discord
from discord.ext import commands
from scripts.workers.window_setup import setup_windows
from scripts.workers.multi_load import send_click_to_window, send_keys_to_window
from scripts.workers.config_loader import load_config
import win32gui
import win32con

intents = discord.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True
#bot = commands.Bot(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)


#custom_config = r'--oem 1 --psm 6 -l eng+exocet --logfile tesseract_log.txt'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

speed_multiplier = 0.6  # 10% faster (use 1.1 for 10% slower, etc.)

# Configuration for image paths and hotkeys
shop_images = ['images/town/act4/jamella/jamella1.jpg','images/town/act4/jamella/jamella2.jpg','images/town/act4/jamella/jamella3.jpg', 'images/town/act4/jamella/jamella4.jpg', 'images/town/act4/jamella/jamella5.jpg','images/town/act4/jamella/jamella6.jpg']
jamellaSelect = 'images/town/act4/jamella/jamellaSelect.jpg'
star_images = ['images/chaos/star/starPart1.jpg', 'images/chaos/star/starPart2.jpg', 'images/chaos/star/starPart3.jpg']
seal_images = ['images/chaos/seals/chaosSeal.jpg', 'images/chaos/seals/chaosSeal1.jpg', 'images/chaos/seals/seal1.jpg', 'images/chaos/seals/seal3.jpg', 'images/chaos/seals/seal4.jpg',
                'images/chaos/seals/seal5.jpg', 'images/chaos/seals/seal6.jpg', 'images/chaos/seals/seal8.jpg', 'images/chaos/seals/seal9.jpg', 'images/chaos/seals/seal11.jpg',
                    'images/chaos/seals/seal12.jpg', 'images/chaos/seals/seal13.jpg']
waypoint_image = 'images/town/act4/waypoint/wp.jpg' 
riverwaypoint_image = 'images/town/act4/waypoint/riverWP.jpg'
river_image = 'images/town/act4/waypoint/riverOfFlameWP.jpg'
river_terror_image = 'images/town/act4/waypoint/riverTerrorWp.jpg'
starImg = 'images/chaos/star/chaosStar.jpg'
sealImg = 'images/chaos/seals/chaosSeal.jpg'
sealHoverImg = 'images/chaos/seals/chaosSealHover.jpg'
portalToThrone = 'images/general/PortalToThrone.png'
#errors
failedToJoinImg = 'images/errors/lobby/failedToJoin.png'

#Fly's Hotkeys (Going to add a config via interface)
#tp_hotkey = 'F12'
#teleHotkey = 'F4'
#boHotkey = 'F10'
#bcHotkey = 'F9'
#attackHotkey = 'F1'

#Cj's Hotkeys
tp_hotkey = 'x'
teleHotkey = 'j'
boHotkey = 'g'
bcHotkey = 'f'
attackHotkey = 'F1'

hasCTA = False

# Global variables for life and mana
current_life = None
max_life = None
current_mana = None
max_mana = None


pickit_folder = 'pickit'  

# Screen resolution used during initial development
initial_screen_width = 1900
initial_screen_height = 1200

def cleanOcr(ocr_text,characterOnly=False):
    #if characterOnly:  # These can be also Q's instead of O's
    corrections = {
        '0': 'O',
        '@': 'O',
        '®': 'O',
        'Â®': 'O',
        '*': 'O',
        '|': 'I',
        '1': 'I',
        '!': 'I'
    }
    for wrong, right in corrections.items():
        ocr_text = ocr_text.replace(wrong, right)
    return ocr_text

def get_screen_position(x_percent, y_percent):
    screen_width, screen_height = pyautogui.size()
    return int(screen_width * x_percent), int(screen_height * y_percent)

def confirmAct1Load():
    try:
        confirmPos = pyautogui.locateOnScreen('images/town/act1/confirm/confirm1.png', confidence=0.45)
        if confirmPos:
            print(f"Confirmed Act1 Pos: {confirmPos}")
            return True
    except:
        print('cant confirm act1')
    
def confirmAct2Load():
    try:
        confirmPos = pyautogui.locateOnScreen('images/town/act1/confirm/confirm1.png', confidence=0.45)
        if confirmPos:
            print(f"Confirmed Act2 Pos: {confirmPos}")
            return True
    except:
        print('cant confirm act2')
        
def confirmAct3Load():
    try:
        confirmPos = pyautogui.locateOnScreen('images/town/act1/confirm/confirm1.png', confidence=0.45)
        if confirmPos:
            print(f"Confirmed Act3 Pos: {confirmPos}")
            return True
    except:
        print('cant confirm act3')

def confirmAct4Load():
    try:
        confirmPos = pyautogui.locateOnScreen('images/town/act4/confirm/confirm1.png', confidence=0.45)
        if confirmPos:
            print(f"Confirmed Act4 Pos: {confirmPos}")
            return True
    except:
        print('cant confirm act4')

def confirmAct5Load():
    try:
        confirmPos = pyautogui.locateOnScreen('images/town/act5/confirm/confirm1.png', confidence=0.45)
        if confirmPos:
            print(f"Confirmed Act5 Pos: {confirmPos}")
            return True
    except:
        print('cant confirm act5')

def whatAct():
    if confirmAct1Load():
        return '1'
    if confirmAct2Load():
        return '2'
    if confirmAct3Load():
        return '3'
    if confirmAct4Load():
        return '4'
    if confirmAct5Load():
        return '5'
    
## MultiLoad ##
def activate_window_by_handle(hwnd):
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore if minimized
        win32gui.SetForegroundWindow(hwnd)  # Bring to foreground
        print(f'Activated window with handle: {hwnd}')
    except Exception as e:
        print(f'Error activating window: {e}')

def get_window_by_class(class_type):
    """Retrieve window title based on class type from the config."""
    config = load_config()
    for loader in config["loaders"]:
        if loader["type"] == class_type:
            return loader["window_title"]
    return None

def multi_load_script(leader, game_name, password,battletag = 'none', firstGame=True):
    config = load_config()
    print('Setup Window')
    setup_windows(config)
    print('setup')
    windows = [loader["window_title"] for loader in config["loaders"] if loader["window_title"]]
    print(f"Starting multi-load for windows: {windows}")
    time.sleep(5)

    for windowName in windows:
        print(f"Joining game on windowName: {windowName}")
        time.sleep(.3)  # Delay between actions

        matched_windows = gw.getWindowsWithTitle(windowName)
        if matched_windows:
            window = matched_windows[0]  # Take the first matching window
            print(f"Joining game on window: {window}")
            activate_window_by_handle(window._hWnd)
        else:
            print(f"No window found with title: {windowName}")
            continue 

        time.sleep(.3)
        joinGame(game_name, password, firstGame)
    waitForLeaderMultiLoader(windows, leader, game_name, password,battletag)
    print("Multi-load complete.")


def joinMultiGame(window_title, game_name, password, firstGame=True):
    game_name_pos = (.7/1, .13/1)
    password_pos = (.84/1,.13/1 )
    join_game_pos = (.73/1, .60/1)
    attempts = 10
    attemptCounter = 0

    time.sleep(0.3)
    send_click_to_window(window_title, *game_name_pos)
    time.sleep(0.1)
    print(f"Writing game_name - {game_name}.")
    send_keys_to_window(window_title, game_name)
    time.sleep(0.3)
    
    if firstGame and password:
        send_click_to_window(window_title, *password_pos)
        time.sleep(0.1)
        print(f"Writing password - {password}.")
        send_keys_to_window(window_title, password)
        time.sleep(0.3)

    while attemptCounter < attempts:
        print(f"Joining Game.")
        send_click_to_window(window_title, *join_game_pos)
        time.sleep(2)  # Increase delay to check if the join was successful


        failedToJoin = checkFailedToJoinGame()  
        if not failedToJoin:
            return

        attemptCounter += 1

    print('Too many join game attempts. Sleeping for a long time.')
    time.sleep(1000000)
    sys.exit()

def preBuffMulti(window_title, bcHotkey="F1", boHotkey="F2"):
    global hasCTA
    time.sleep(1)
    if hasCTA:
        # Switch to CTA weapon
        send_keys_to_window(window_title, "w")
        time.sleep(0.5)

        # Battle Command sequence
        for _ in range(2):
            send_keys_to_window(window_title, bcHotkey)
            time.sleep(0.4)

        # Battle Orders sequence
        for _ in range(2):
            send_keys_to_window(window_title, boHotkey)
            time.sleep(0.4)

        # Repeat BC and BO
        for _ in range(2):
            send_keys_to_window(window_title, bcHotkey)
            time.sleep(0.4)
            send_keys_to_window(window_title, boHotkey)
            time.sleep(0.4)

        # Switch back to main weapon
        send_keys_to_window(window_title, "w")
        time.sleep(1)

def setWindow(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)

def waitForLeaderMultiLoader(windows, leader, game_name, password,battletag):
    x = 0
    boInRiver = False
    time.sleep(2)

    while True:
        x = x + 1
        if (x > 10000):
            pass
        time.sleep(.5)
        print('Waiting for leader to leave')
        chat_text = setup.read_screen_text(region=(0, 650, 650, 930))  # Adjust region to match chat area
        print(f'chat_text: {chat_text}')
        if battletag:
            print("in battletag")
            if (f"{leader} left our world" in chat_text) or (f"{battletag} left our world" in chat_text):
                print("Leader has left the world")
                for window in windows:
                    window.activate()
                    time.sleep(.5)
                    save_and_quit()
                    time.sleep(.5)
                next_game_name = increment_game_name(game_name)
                multi_load_script(leader,next_game_name,password,battletag, False)
                break

            elif(f"help" in chat_text):
                helpText = "Sit & Listen Traveler.... (help) (pause -> resume) (bo) (chant) (newGame)"
                sayInGame(helpText)
                time.sleep(10)

            elif(f"pause" in chat_text):
                print("PAUSING")
                sayInGame('Pausing')
                paused = True
                while paused:
                    print('Waiting for leader to resume')
                    chat_text = setup.read_screen_text(region=(0, 650, 650, 930))  # Adjust region to match chat area
                    if (f"resume" in chat_text or ""):
                        paused = False
                        time.sleep(10)
                        print('Resuming)')
            
            elif(f"bo" in chat_text):
                print("BO - Testing")
                sayInGame('BO at River')
                #bo_window = get_window_by_class("BO")
                bo_window = gw.getWindowsWithTitle('BO')[0]
                if bo_window:
                    print(f"Found BO Barb window: {bo_window}")
                    print(f'PrebuffMulti - bo_window: {bo_window}')
                    bo_window.activate()
                    #setWindow(bo_window)
                    #wpToRiver()
                    if boInRiver == False:
                        wpToRiverUsingCoords(bo_window)
                    preBuff()
                    boInRiver = True
                else:
                    print("BO Barb window not found in config.")
                time.sleep(1)

            
            elif(f"chant" in chat_text):
                print("Chant - Testing")
                sayInGame('Chant by a1 tent')
                bo_window = get_window_by_class("Chant")
                time.sleep(1)
                #Chant
            
            elif(f"newGame" in chat_text):
                print("Get New Game Name - NOT IMPLEMENTED YET")
                sayInGame('Not Yet')
                time.sleep(10)

            elif(f"leader?" in chat_text):
                print(f"Leader: {leader}")
                sayInGame(f'Leader: {leader}')
                time.sleep(10)

            elif(f'set leader' in chat_text):
                print(f'Set Leader: - NOT IMPLEMENTED YET')
                sayInGame('Not Yet')
                time.sleep(10)

            elif(f'whois retep' in chat_text):
                print(f'Retep')
                sayInGame('Retep is the Doomlord of thunderdome. This is what Cain told me anyway.')
                time.sleep(10)

        else:
            if (f"{leader} left our world" in chat_text):
                print("Leader has left the world")
                #for window in windows:
                #    window.activate()
                #    time.sleep(.5)
                #    save_and_quit()
                #    time.sleep(.5)
                multiQuit(windows)
                next_game_name = increment_game_name(game_name)
                multi_load_script(leader,next_game_name,password,battletag, False)
                break

            elif(f"help" in chat_text):
                helpText = "Sit & Listen Traveler.... (help) (pause -> resume) (bo) (chant) (newGame)"
                sayInGame(helpText)
                time.sleep(10)

            elif(f"pause" in chat_text):
                print("PAUSING")
                sayInGame('Pausing')
                paused = True
                while paused:
                    print('Waiting for leader to resume')
                    chat_text = setup.read_screen_text(region=(0, 650, 650, 930))  # Adjust region to match chat area
                    if (f"resume" in chat_text):
                        paused = False
                        time.sleep(10)
                        print('Resuming)')
            
            elif(f"bo" in chat_text):
                print("BO - Testing")
                sayInGame('BO at River')
                bo_window = gw.getWindowsWithTitle('BO')[0]
                if bo_window:
                    print(f"Found BO Barb window: {bo_window}")
                    bo_window.activate()
                    #wpToRiver()
                    if boInRiver == False:
                        wpToRiverUsingCoords(bo_window)
                    preBuff()
                    boInRiver = True
                else:
                    print("BO Barb window not found in config.")
                time.sleep(1)

            
            elif(f"chant" in chat_text):
                print("Chant - Testing")
                sayInGame('Chant by a1 tent')
                bo_window = get_window_by_class("Chant")
                time.sleep(1)
                #Chant
            
            elif(f"newGame" in chat_text):
                print("Get New Game Name - NOT IMPLEMENTED YET")
                sayInGame('Not Yet')
                time.sleep(10)

            elif(f"leader?" in chat_text):
                print(f"Leader: {leader}")
                sayInGame(f'Leader: {leader}')
                time.sleep(10)

            elif(f'set leader' in chat_text):
                print(f'Set Leader: - NOT IMPLEMENTED YET')
                sayInGame('Not Yet')
                time.sleep(10)

            elif(f'whois retep' in chat_text):
                print(f'Retep')
                sayInGame('Retep is the Doomlord of thunderdome. This is what Cain told me anyway.')
                time.sleep(10)
            
            elif(f'END' in chat_text):
                print(f'ENDING SCRIPT')
                sayInGame('GG')
                multiQuit(windows)
                return
            

def getWindowByCharName(name):
    pyautogui.press('a')
    nameText = setup.read_screen_text(region=(175, 175, 340, 197))  # Adjust region to match chat area
    cleanName = cleanOcr(nameText)
    if cleanName == name:
        return True

## INTERACT WITH D2R ##
def multiQuit(windows):
    for window in windows:
        window.activate()
        time.sleep(.5)
        save_and_quit()
        time.sleep(.5)

def sayInGame(text):
    time.sleep(.3)
    pyautogui.press('enter')
    time.sleep(.3)
    pyautogui.write(text, interval=0.04)
    time.sleep(.3)
    pyautogui.press('enter')
    time.sleep(.3)

## ACT 4 SHOP ##

def walkToShop():
    shopSteps = [(1825/1900, 1080/1200), (975/1900, 700/1200)]
    for step in shopSteps:
        time.sleep(.5)
        click_at_percentage(*step)
        time.sleep(2)
    
def findShop():
    print("Looking for Jamella")
    try:
        shop_found = False
        for _ in range(10):
            for shop_image in shop_images:
                try:
                    shopPos = pyautogui.locateOnScreen(shop_image, confidence=0.5)
                    if shopPos:
                        time.sleep(.5)
                        shop_found = True
                        print(f"Jamella found using {shop_image} at {shopPos}.")
                        pyautogui.moveTo(shopPos)
                        pyautogui.click()
                        time.sleep(3)  # Wait a second to ensure movement
                        break
                    else:
                        print("Can't find Shop.")
                except:
                    print(f"Issue locating Jamella - Try again")
                    time.sleep(1)
            if shop_found:
                break
    except Exception as e:
        print(f"Couldn't findShop(): {e}")
        
def openShopTrade():
    try:
        time.sleep(1)
        selectPos = pyautogui.locateOnScreen(jamellaSelect,confidence=0.5)
        if selectPos:
            print("Selecting Trade")
            pyautogui.moveTo(selectPos)
            time.sleep(5)
            pyautogui.click()
            time.sleep(1)
    except Exception as e:
        print("couldn't open shop")
        
def shop():
    tpPos = (625/1900,375/1200)
    hpPos = (625/1900,725/1200)
    closePos = (685/1900,65/1200)
    pyautogui.keyDown('shift')
    time.sleep(.5)
    click_at_percentage(*tpPos, 'right')
    print("BOUGHT TP'S")
    time.sleep(.5)
    
    click_at_percentage(*hpPos, 'right')
    print("BOUGHT Health Pots")
    time.sleep(.5)
    pyautogui.keyUp('shift')
    time.sleep(.5)
    click_at_percentage(*closePos)
    click_at_percentage(*closePos)

def shopToWP():
    steps = [(1440/1900,270/1200), (120/1900, 120/1200), (850/1900,400/1200)]
    for step in steps:
        click_at_percentage(*step)
        time.sleep(2)
       
def prep():
    walkToShop()
    findShop()
    openShopTrade()
    shop()
    shopToWP()

#
# Baal Leech
#

def wait_for_tp_and_confirm_leader(leader, game_name, password,battletag):
    print("Starting to search for TPs...")
    while True:
        print('-----waiting for throne-----')
        try:
            checkLeaderLeft(leader, game_name, password,battletag)
            tp_positions = list(pyautogui.locateAllOnScreen('images/general/tp.png', confidence=0.7))
            if tp_positions:
                for tp_pos in tp_positions:
                    pyautogui.moveTo(tp_pos)
                    #x, y, w, h = tp_pos.left, tp_pos.top, tp_pos.width, tp_pos.height  # Adjust to top-left corner
                    #text_region = (x - 100, y - 100), (x + 100, y - 50)
                    #text = setup.read_screen_text(region=text_region)
                    #if leader_name in text:
                    print(f"TP found at ({x}, {y}).")
                    time.sleep(1)
                    if check_if_throne_portal():
                        time.sleep(5) # wait 15 seconds for safety
                        pyautogui.click(tp_pos)
                        return
                    else:
                        print('not throne')
            else:
                print("throne not found, retrying...")
            time.sleep(3)
        except:
            print("failed tp")
            time.sleep(3)

# Function to wait for leader to leave and rejoin the next game
def wait_for_leader_to_leave(leader, game_name, password, battletag ='none'):
    x = 0
    while True:
        x = x + 1
        if (x > 100):
            pass
        time.sleep(1)
        print('Waiting for leader to leave')
        chat_text = setup.read_screen_text(region=(0, 650, 650, 930))  # Adjust region to match chat area
        print(f'chat_text: {chat_text}')
        if (f"{leader} left our world" in chat_text) or (f"{battletag} left our world" in chat_text):
            print("Leader has left the world")
            save_and_quit()
            next_game_name = increment_game_name(game_name)
            loopBaalLeech(leader,next_game_name,password,battletag)
            #while True:
                #enter_game(next_game_name, password)
                #time.sleep(10)
                #chat_text = setup.read_screen_text(region=(0, 650, 600, 930))  # Adjust region to match chat area
                #if "Your connection has been interrupted" not in 
            break

def checkLeaderLeft(leader, game_name, password,battletag):
    print('Check if Leader Left')
    chat_text = setup.read_screen_text(region=(0, 650, 650, 930))  # Adjust region to match chat area
    print(f'chat_text: {chat_text}')
    if f"{leader} left our world" in chat_text:
        print("Leader has left the world")
        save_and_quit()
        next_game_name = increment_game_name(game_name)
        loopBaalLeech(leader,next_game_name,password,battletag)

def loopBaalLeech(leader,game_name,password, battletag):
    joinGame(game_name, password)
    #confirmAct5Load()
    act = whatAct()
    print(f'In act: {act}')
    wait_for_tp_and_confirm_leader(leader, game_name, password,battletag)
    preBuff()
    wait_for_leader_to_leave(leader, game_name, password, battletag)




        
def checkFailedToJoinGame():
    try:
        time.sleep(1)
        failedPos = pyautogui.locateOnScreen(failedToJoinImg, confidence=0.50)
        if failedPos:
            print('Failed to join game')
            time.sleep(2)
            click_at_percentage(.5/1,.52/1)
            return True
        else:
            return False
        
    except:
        print('cant find failed game')
        return False

#Version 3 of check portal
def check_if_throne_portal():
    try:
        throneCheck=pyautogui.locateOnScreen('images/general/portalToThrone.png', confidence=0.6)
        if throneCheck:
            print('found throne portal')
            return True
        else:
            print('portal not to throne')
            return False           
        

    except:
        print('check if throne portal failed')
        
#Fix if two portals opened
#Fix if Leader leaves before I enter throne room



#
# CHAOS LEAD
#

def attack(count):
    for _ in range(count):
        pyautogui.press(attackHotkey)
        time.sleep(.2)
    #scan_for_items()
    extract_life_mana_from_screen()
    
def get_value_from_image(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(img)
    
    # Extract the number part from the string
    value = ''.join(filter(str.isdigit, text))
    
    # Return the value as an integer
    return int(value) if value.isdigit() else None

def correct_ocr_typos(text):
    # Replace common OCR mistakes
    text = text.replace('@', '0')
    text = text.replace('o', '0')
    text = text.replace('O', '0')
    text = text.replace('l', '1')
    text = text.replace('I', '1')
    text = text.replace('i', '1')
    text = text.replace('!', '1')
    text = text.replace('T', '7')
    
    # Further validation could be added here
    # Example: If the text doesn't contain a '/' or doesn't split into two numbers, ignore it
    if '/' not in text:
        return None
    
    try:
        current, max_value = map(int, text.split('/'))
        return current, max_value
    except ValueError:
        # If conversion fails, return None to ignore the data
        return None

def capture_screen_area(x_percent_start, y_percent_start, x_percent_end, y_percent_end):
    # Calculate the screen dimensions based on percentages
    screen_width, screen_height = pyautogui.size()
    left = int(screen_width * x_percent_start)
    top = int(screen_height * y_percent_start)
    right = int(screen_width * x_percent_end)
    bottom = int(screen_height * y_percent_end)
    
    # Capture the screen area
    img = pyautogui.screenshot(region=(left, top, right-left, bottom-top))
    
    # Convert to grayscale for better OCR results
    img = img.convert('L')
    
    return img

def extract_life_mana_from_screen():
    global current_life, max_life, current_mana, max_mana
    
   # Define the percentage coordinates for life and mana
    life_coords = (0.25, 0.77, 0.315, 0.795)  # Example: top-left and bottom-right percentages
    mana_coords = (0.72, 0.77, 0.775, 0.795)
    
    # Capture the life and mana areas
    life_img = capture_screen_area(*life_coords)
    mana_img = capture_screen_area(*mana_coords)
    
    # Use pytesseract to extract text
    life_text = pytesseract.image_to_string(life_img, config='--psm 7')
    mana_text = pytesseract.image_to_string(mana_img, config='--psm 7')
    
    # Correct and validate the text
    life_values = correct_ocr_typos(life_text)
    mana_values = correct_ocr_typos(mana_text)
    
    print(f'Life Read : {life_text}')
    print(f'Mana Read : {mana_text}')
    print(f'Life Fix: {life_values}')
    print(f'Mana Fix: {mana_values}')

    if life_values:
        current_life, max_life = life_values
        print(f"Current Life: {current_life}, Max Life: {max_life}")
        if current_life < 800:
            pyautogui.press('1')
            print('healing - press 1')
      
    else:
        print("Failed to extract valid life values.")
    
    if mana_values:
        current_mana, max_mana = mana_values
        print(f"Current Mana: {current_mana}, Max Mana: {max_mana}")
        if current_mana < 120:
            pyautogui.press('2')
            print('mana - press 2')
    else:
        print("Failed to extract valid mana values.")

def check_life_and_press_keys(image_path):
    life_value = get_value_from_image(image_path)
    
    if life_value is None:
        print("Failed to read life value.")
        return
    
    print(f"Life: {life_value}")
    
    if life_value < 100:
        pyautogui.press('1')
        time.sleep(1)
        new_life_value = get_value_from_image(image_path)
        
        if new_life_value == life_value:
            pyautogui.press('2')
            time.sleep(1)
            new_life_value = get_value_from_image(image_path)
            
            if new_life_value == life_value:
                pyautogui.press('3')
                time.sleep(1)
                new_life_value = get_value_from_image(image_path)
                
                if new_life_value == life_value:
                    pyautogui.press('4')


    check_life_and_press_keys('/mnt/data/life.jpg')
    time.sleep(1)  # Adjust the delay as needed

def get_mana_value(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(img)
    
    # Extract the number part from the string
    mana_value = ''.join(filter(str.isdigit, text))
    
    # Return the mana value as an integer
    return int(mana_value) if mana_value.isdigit() else None

def check_mana_and_press_keys(image_path):
    mana_value = get_mana_value(image_path)
    
    if mana_value is None:
        print("Failed to read mana value.")
        return
    
    print(f"Mana: {mana_value}")
    
    if mana_value < 100:
        pyautogui.press('1')
        time.sleep(1)
        new_mana_value = get_mana_value(image_path)
        
        if new_mana_value == mana_value:
            pyautogui.press('2')
            time.sleep(1)
            new_mana_value = get_mana_value(image_path)
            
            if new_mana_value == mana_value:
                pyautogui.press('3')
                time.sleep(1)
                new_mana_value = get_mana_value(image_path)
                
                if new_mana_value == mana_value:
                    pyautogui.press('4')


    check_mana_and_press_keys('/mnt/data/mana.jpg')
    time.sleep(1)  # Adjust the delay as needed

def scan_for_items():
    for pickit_image in pickit_images:
        if not os.path.exists(pickit_image):
            print(f"Image not found: {pickit_image}")
            continue

        try:
            item_location = pyautogui.locateOnScreen(pickit_image, confidence=0.7)
            if item_location:
                pyautogui.moveTo(pyautogui.center(item_location))
                time.sleep(1)
                item_location = pyautogui.locateOnScreen(pickit_image, confidence=0.3)
                pyautogui.moveTo(pyautogui.center(item_location))
                time.sleep(1)
                pyautogui.click()
                time.sleep(1)  # Delay to ensure item is picked up
        except pyautogui.ImageNotFoundException:
            print(f"Failed to locate image on screen: {pickit_image}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def preBuff():
    global hasCTA
    #extract_life_mana_from_screen()
    time.sleep(1)
    if hasCTA:
        pyautogui.press("w")
        time.sleep(.5)
        pyautogui.press(bcHotkey)
        time.sleep(.4)
        pyautogui.press(bcHotkey)
        time.sleep(.4)
        pyautogui.press(boHotkey)
        time.sleep(.4)
        pyautogui.press(boHotkey)
        time.sleep(.4)
        pyautogui.press(bcHotkey)
        time.sleep(.4)
        pyautogui.press(bcHotkey)
        time.sleep(.4)
        pyautogui.press(boHotkey)
        time.sleep(.4)
        pyautogui.press(boHotkey)
        time.sleep(1)
        pyautogui.press("F5")
        time.sleep(2)
        pyautogui.press("w")
    time.sleep(1)

def load_pickit_images(pickit_folder):
    try:
        images = []
        for img in os.listdir(pickit_folder):
            if img.endswith('.png'):
                img_path = os.path.join(pickit_folder, img)
                if os.path.isfile(img_path):
                    images.append(img_path)
                else:
                    print(f"File not found: {img_path}")
        return images
    except Exception as e:
        print(f"Error loading pickit images: {e}")
        return []
          
pickit_images = load_pickit_images(pickit_folder)

def click_at_percentage(x_percent, y_percent, click='left'):
    if not (0 <= x_percent <= 1) or not (0 <= y_percent <= 1):
        print(f"Invalid percentage coordinates: x={x_percent}, y={y_percent}")
        return
    x, y = get_screen_position(x_percent, y_percent)
    pyautogui.moveTo(x, y)
    if click == 'left':
        print('Clicking left')
        pyautogui.click()
    elif click == 'right':
        print('Clicking right')
        pyautogui.click(button='right')
    else:
        print(f"Unknown click type: {click}")

# Function to convert percentage-based coordinates to absolute pixel coordinates
def percent_to_pixel(window, percent_coords):
    x_pixel = window.left + int(window.width * percent_coords[0])
    y_pixel = window.top + int(window.height * percent_coords[1])
    return x_pixel, y_pixel

def wpToRiverUsingCoords(window):
    print("Starting to search for Waypoint...")

    # Ensure the window is active and focused
    window.activate()
    time.sleep(1)  # Give time for the window to focus

    x = 0
    while True:
        try:
            # Waypoint position in percentage (83.5%, 10.75%)
            waypoint_position = percent_to_pixel(window, (0.835, 0.1075))
            pyautogui.moveTo(waypoint_position)
            pyautogui.click()
            print(f"Clicked waypoint at {waypoint_position}.")
            time.sleep(4)

            try:
                # River position in percentage (20%, 31%)
                riverPos = percent_to_pixel(window, (0.2, 0.31))
                if riverPos:
                    print(f"River found at {riverPos}.")
                    pyautogui.moveTo(riverPos)
                    pyautogui.click()
                    time.sleep(3)

                    while x == 0:
                        # River waypoint position in percentage (40%, 40%)
                        riverwaypoint_position = percent_to_pixel(window, (0.4, 0.4))
                        
                        print(f"Waypoint found at {riverwaypoint_position}.")
                        pyautogui.moveTo(riverwaypoint_position)
                        pyautogui.press(teleHotkey)
                        x = 1
                        time.sleep(2)
                    break
                else:
                    print("Found WP, Can't find River.")
            except Exception as e:
                print(f"Error while searching for river: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"Failed to locate waypoint: {e}")
            time.sleep(5)


def wpToRiver():
    print("Starting to search for Waypoint...")
    x = 0
    while True:
        try:
            waypoint_position = pyautogui.locateOnScreen(waypoint_image, confidence=0.35)
            if waypoint_position:
                print(f"Waypoint found at {waypoint_position}.")
                pyautogui.moveTo(waypoint_position)
                pyautogui.click()
                time.sleep(4)
                try:
                    riverPos = pyautogui.locateOnScreen(river_image, confidence=0.45)
                    if riverPos:
                        print(f"River found at {riverPos}.")
                        pyautogui.moveTo(riverPos)
                        pyautogui.click()
                        time.sleep(3)
                        while x == 0:
                            riverwaypoint_position = pyautogui.locateOnScreen(riverwaypoint_image, confidence=0.4)
                            if riverwaypoint_position:
                                print(f"Waypoint found at {riverwaypoint_position}.")
                                pyautogui.moveTo(riverwaypoint_position)
                                pyautogui.press(teleHotkey)
                                x = 1
                            time.sleep(2)
                        break
                    else:
                        print("Found WP, Can't find River")
                except:
                    print("Found WP, Can't find River")
                try:
                    riverPos = pyautogui.locateOnScreen(river_terror_image, confidence=0.45)
                    if riverPos:
                        print(f"River found at {riverPos}.")
                        pyautogui.moveTo(riverPos)
                        pyautogui.click()
                        time.sleep(3)
                        while x == 0:
                            riverwaypoint_position = pyautogui.locateOnScreen(riverwaypoint_image, confidence=0.4)
                            if riverwaypoint_position:
                                print(f"Waypoint found at {riverwaypoint_position}.")
                                pyautogui.moveTo(riverwaypoint_position)
                                pyautogui.press(teleHotkey)
                                x = 1
                            time.sleep(2)
                        break
                    else:
                        print("Found WP, Can't find River")
                except:
                    print("Found WP, Can't find River")
                    
            else:
                print("No Waypoint found, retrying...")
            time.sleep(5)
        except:
            print("Failed to locate waypoint.")
            time.sleep(5)

def teleRiver():
    preBuff()
    extract_life_mana_from_screen()
    click_at_percentage(1890/1900, 60/1200)  # Top right corner based on initial resolution
    for _ in range(18):
        print(f"Tele - Press: {teleHotkey}")
        pyautogui.press(teleHotkey)
        time.sleep(.50)

def centerStar(starPos, location):
    # Move to the center of the star and drop a TP
    if location == 'Bottom':
        center_x = starPos.left + starPos.width // 2 + 200
        center_y = starPos.bottom + starPos.height // 2 + 50
        pyautogui.moveTo(center_x, center_y)
        pyautogui.press(teleHotkey)
        time.sleep(1)
        print("Centered Star (Bottom)")
    if location == 'Left':
        center_x = starPos.left + starPos.width // 2 + 200
        center_y = starPos.top + starPos.height // 2 + 50
        pyautogui.moveTo(center_x, center_y)
        pyautogui.press(teleHotkey)
        time.sleep(1)
        print("Centered Star (Left)")
    if location == 'Top':
        center_x = starPos.left - starPos.width // 2 - 200
        center_y = starPos.bottom + starPos.height // 2 + 50
        pyautogui.moveTo(center_x, center_y)
        pyautogui.press(teleHotkey)
        time.sleep(1)
        print("Centered Star (Top)")

def findStarBottom():
    print("Looking for Star Bottom")
    count = 0
    starPos = 0,0
    try:
        while count < 10:
            star_found = False
            for star_image in star_images:
                try:
                    starPos = pyautogui.locateOnScreen(star_image, confidence=0.6)
                    if starPos:
                        star_found = True
                        print(f"Star found using {star_image} at {starPos}.")
                        pyautogui.moveTo(starPos)
                        pyautogui.click()
                        time.sleep(1)
                        break
                except:
                    print("Issue locating Star")
            if star_found:
                print("Found Star (Bottom) - Town portal dropped.")
                openTP()
                time.sleep(2)
                preBuff()
                break
            else:
                print("Can't find star, moving towards the top right.")
                click_at_percentage(1250/1900, 450/1200)
                time.sleep(2)
                #scan_for_items()
                count += 1
    except Exception as e:
        print(f"Couldn't findStarBottom(): {e}")

def findStarTop():
    print("Looking for Star Top")
    count = 0
    starPos = 0,0
    try:
        while count < 10:
            star_found = False
            for star_image in star_images:
                try:
                    starPos = pyautogui.locateOnScreen(star_image, confidence=0.6)
                    if starPos:
                        star_found = True
                        print(f"Star found using {star_image} at {starPos}.")
                        pyautogui.moveTo(starPos)
                        pyautogui.click()
                        time.sleep(1)
                        break
                except:
                    print("Issue locating Star")
            if star_found:
                center_x = starPos.left - starPos.width // 2
                center_y = starPos.bottom + starPos.height // 2
                pyautogui.moveTo(center_x, center_y)
                pyautogui.click()
                print("Found Star (Top) - Town portal dropped.")
                centerStar(starPos,'Top')
                break
            else:
                print("Can't find star, moving towards the Bottom right.")
                click_at_percentage(1400/1900, 900/1200)
                time.sleep(2)
                count += 1
    except Exception as e:
        print(f"Couldn't findStarTop(): {e}")
        
def findStarLeft():
    print("Looking for Star Left")
    count = 0
    try:
        while count < 10:
            star_found = False
            for star_image in star_images:
                try:
                    starPos = pyautogui.locateOnScreen(star_image, confidence=0.6)
                    if starPos:
                        star_found = True
                        print(f"Star found using {star_image} at {starPos}.")
                        pyautogui.moveTo(starPos)
                        pyautogui.click()
                        time.sleep(1)
                        break
                except:
                    print("Issue locating Star")
            if star_found:
                center_x = starPos.left + starPos.width // 2 + 200
                center_y = starPos.bottom + starPos.height // 2 
                pyautogui.moveTo(center_x, center_y)
                pyautogui.click()
                time.sleep(1)
                print("Found star (Left) - Town portal dropped.")
                centerStar(starPos,'Left')
                break
            else:
                if count == 0:
                    click_at_percentage(1250/1900, 600/1200)
                    pyautogui.press(teleHotkey)
                print("Can't find star, moving to the right")
                click_at_percentage(1250/1900, 850/1200)
                time.sleep(2)
                count += 1
    except Exception as e:
        print(f"Couldn't findStarLeft(): {e}")

def findStarRight():
    print("Looking for Star Right")
    count = 0
    try:
        while count < 10:
            star_found = False
            for star_image in star_images:
                try:
                    starPos = pyautogui.locateOnScreen(star_image, confidence=0.6)
                    if starPos:
                        star_found = True
                        print(f"Star found using {star_image} at {starPos}.")
                        pyautogui.moveTo(starPos)
                        pyautogui.click()
                        time.sleep(1)
                        break
                except:
                    print("Issue locating Star")
            if star_found:
                center_x = starPos.left - starPos.width // 2 - 200
                center_y = starPos.bottom + starPos.height // 2 
                pyautogui.moveTo(center_x, center_y)
                pyautogui.click()
                time.sleep(1)
                print("Found star (Right) - Town portal dropped.")
                centerStar(starPos,'Right')
                break
            else:
                if count == 0:
                    click_at_percentage(150/1900, 60/1200)
                    pyautogui.press(teleHotkey)
                print("Can't find star, moving to the Left")
                click_at_percentage(150/1900, 50/1200)
                time.sleep(2)
                count += 1
    except Exception as e:
        print(f"Couldn't findStarRight(): {e}")
        
def findSeal():
    print("Looking for Seal")
    try:
        seal_found = False
        for seal_image in seal_images:
            try:
                print(f'seal_image: {seal_image}')
                sealPos = pyautogui.locateOnScreen(seal_image, confidence=0.5)
                if sealPos:
                    seal_found = True
                    print(f"Seal found using {seal_image} at {sealPos}.")
                    pyautogui.moveTo(pyautogui.center(sealPos))
                    time.sleep(1)
                    pyautogui.click()
                    time.sleep(1)
                    break
            except:
                print("Issue locating Seal")
        if seal_found:
            pyautogui.moveTo(pyautogui.center(sealPos))
            time.sleep(1)
            pyautogui.click()
            time.sleep(3)
        else:
            print("Can't find seal.")
    except Exception as e:
        print(f"Couldn't findSeal(): {e}")

def openTP():
    pyautogui.press(tp_hotkey)

def vizier():
    vizierWaypoints = [
        ( .07/1, .3/1),
        ( .07/1, .3/1),
        (200/1900, 250/1200),
        (150/1900, 450/1200), 
        (100/1900, 450/1200),
        (200/1900, 50/1200),
        (100/1900, 1150/1200),
        ( .96/1, .06/1),
        (800/1900, 20/1200),
    ]
    
    for step in vizierWaypoints:
        x, y = step
        click_at_percentage(x, y)
        pyautogui.press(teleHotkey)
        attack(10)
        #scan_for_items()
        findSeal()
    time.sleep(5)

def vizierToStar():
    vizierToStar = [
        (.98/1, .82/1),
        (1650/1900, 650/1200), 
        (1650/1900, 900/1200), 
        (1650/1900, 750/1200), 
        (1050/1900, 700/1200),
        (1650/1900, 900/1200),
        (1600/1900, 800/1200)
    ]
    for step in vizierToStar:
        x, y = step
        click_at_percentage(x, y)
        pyautogui.press(teleHotkey)
        time.sleep(1)

    findStarLeft()

def deSeis():
    deSeisSteps = [
        (.96/1, .05/1),
        (.96/1, .05/1),
        (.96/1, .05/1),
        (.96/1, .05/1),
        (.96/1, .05/1),
        (.93/1, .95/1),
        (.1/1, .077/1),
        (.1/1, .077/1),
        (.15/1, .84/1),
    ]
    for step in deSeisSteps:
        x, y = step
        click_at_percentage(x, y)
        pyautogui.press(teleHotkey)
        attack(10)
        findSeal()
    time.sleep(2)

def deSeisToStar():
    deSeisToStar = [
        (.20/1, .78/1), 
        (.20/1, .78/1), 
        (.20/1, .78/1), 
        (.20/1, .78/1), 
        (.66/1, .70/1), 
    ]
    for step in deSeisToStar:
        x, y = step
        click_at_percentage(x, y)
        pyautogui.press(teleHotkey)
        time.sleep(2)
        #scan_for_items()

    findStarTop()

def infector():
    infectorSteps = [
        (1600/1900, 900/1200), 
        (1600/1900, 950/1200), 
        (1450/1900, 1750/1200), 
        (1800/1900, 950/1200), 
        (800/1900, 550/1200), 
        (400/1900, 750/1200), 
    ]
    
    for step in infectorSteps:
        x, y = step
        click_at_percentage(x, y)
        pyautogui.press(teleHotkey)
        attack(10)
        findSeal()
    time.sleep(5)

def infectorToStar():
    infectorToStar = [
        (450/1900, 750/1200), 
        (150/1900, 100/1200), 
        (150/1900, 500/1200), 
        (150/1900, 500/1200), 
        (150/1900, 400/1200), 
        (150/1900, 500/1200)
    ]
    for step in infectorToStar:
        x, y = step
        click_at_percentage(x, y)
        pyautogui.press(teleHotkey)
        attack(10)
        time.sleep(2)
        #scan_for_items()

    findStarRight()

def walkChaos():
    vizier()
    vizierToStar()
    deSeis()
    deSeisToStar()
    infector()
    infectorToStar()

def check_end_of_chaos(leader, game_name, password):
    if True:
        save_and_quit()
        next_game_name = increment_game_name(game_name)
        loopDiabloLead(leader, next_game_name, password)
    else:
        next_game_name = increment_game_name(game_name)
        loopDiabloLead(leader, next_game_name, password)
    return True

def save_and_quit():
    time.sleep(.3)
    pyautogui.press('esc')
    time.sleep(.4)
    click_at_percentage(950/1900, 525/1200)  # Coordinates based on initial resolution
    #time.sleep(1)
    #pyautogui.press('esc')
    #time.sleep(2)
    pyautogui.click(get_screen_position(950/1900, 525/1200))

def increment_game_name(game_name):
    try:
        base_name, num = game_name.rsplit('-', 1)
        print(f"Base name: {base_name}, Current number: {num}")
        
        # Determine the length of the number after the dash
        num_length = len(num)
        
        # Increment the number by 1
        next_num = int(num) + 1
        
        # Format the new number with leading zeros to maintain the original length
        next_game_name = f"{base_name}-{next_num:0{num_length}d}"
        
        print(f"Next game name: {next_game_name}")
        return next_game_name
    except Exception as e:
        print(f"Error incrementing game name: {e}")
        return game_name  # Return the original game name if there's an error

def createGame(game_name, password):
    lobby_pos = (1100/1900, 1050/1200)
    game_name_pos = (1500/1900, 220/1200)
    password_pos = (1500/1900, 290/1200)
    create_game_pos = (1450/1900, 700/1200)
    
    click_at_percentage(*lobby_pos)
    time.sleep(1)
    click_at_percentage(*game_name_pos)
    print(f"Writing game_name - {game_name}.")
    for _ in range(20):
        pyautogui.press('backspace')
    pyautogui.write(game_name, interval=0.05)
    time.sleep(.5)
    
    click_at_percentage(*password_pos)
    print(f"Writing password - {password}.")
    for _ in range(20):
        pyautogui.press('backspace')
    pyautogui.write(password, interval=0.05)
    time.sleep(.5)
    
    print(f"Joining Game.")
    click_at_percentage(*create_game_pos)
    time.sleep(5)
    
def joinGame(game_name, password, firstGame = True):
    game_name_pos = (.7/1, .13/1)
    password_pos = (.84/1,.13/1 )
    join_game_pos = (.73/1, .60/1)
    attempts = 10
    attemptCounter = 0

    time.sleep(.3)
    click_at_percentage(*game_name_pos)
    click_at_percentage(*game_name_pos)
    print(f"Writing game_name - {game_name}.")
    for _ in range(20):
        pyautogui.press('backspace')
    pyautogui.write(game_name, interval=0.04)
    time.sleep(.3)
    
    if firstGame and password:
        click_at_percentage(*password_pos)
        click_at_percentage(*password_pos)
        print(f"Writing password - {password}.")
        for _ in range(20):
            pyautogui.press('backspace')
        pyautogui.write(password, interval=0.03)
        time.sleep(.3)

    while attemptCounter < attempts:
        print(f"Joining Game.")
        click_at_percentage(*join_game_pos)
        time.sleep(.5)

        failedToJoin = checkFailedToJoinGame()
        if failedToJoin == False:
            return
        #time.sleep(2)
        attemptCounter = attemptCounter + 1

    print('Too many join game attempts. Sleeping for long time')
    quit()
    print('Too many join game attempts. Sleeping for long time')
    time.sleep(10000000)
    sys.exit()

    #if (attemptCounter == attempts):
    #    time.sleep(30)
    #    next_game_name = increment_game_name(game_name)
    #    joinGame(next_game_name,password)


        
def checkFailedToJoinGame():
    try:
        time.sleep(.4)
        failedPos = pyautogui.locateOnScreen(failedToJoinImg, confidence=0.50)
        if failedPos:
            print('Failed to join game')
            time.sleep(2)
            click_at_percentage(.5/1,.52/1)
            return True
        else:
            return False
        
    except:
        print('cant find failed game')
        return False
            

def post_to_discord(game_name, password):
    time.sleep(1)
    discord_window = gw.getWindowsWithTitle('#game-names')[0]
    if discord_window:
        discord_window.activate()
        time.sleep(2)
        if password:
            pyautogui.typewrite(f"{game_name}/{password}")
        else:
            pyautogui.typewrite(f"{game_name}")
        pyautogui.press('enter')
        time.sleep(1)

def refocus_diablo_window():
    try:
        diablo_window = gw.getWindowsWithTitle('Diablo II: Resurrected')[0]
        if diablo_window:
            diablo_window.activate()
            time.sleep(2)
    except:
        print('Failed to refocus on d2 window')
 
def loopDiabloLead(leader, game_name, password):
    #post_to_discord(game_name, password)
    refocus_diablo_window()
    createGame(game_name, password)
    act = whatAct()
    if act != '4':
        print(f'In Act {act} - Not in act 4 - NAVIGATE')
        # Handle being in other acts.
    prep()
    wpToRiver()
    teleRiver()
    findStarBottom()
    preBuff()
    walkChaos()
    check_end_of_chaos(leader, game_name, password)

def create_gui():
    global hasCTA
    root = tk.Tk()
    root.title("AuraBot")
    root.geometry("300x400+1210+75")
    root.attributes('-alpha', 0.9)

    # Set the overall theme to dark
    dark_bg = "#2e2e2e"
    dark_fg = "#ffffff"
    entry_bg = "#3e3e3e"
    entry_fg = "#ffffff"
    btn_bg = "#4e4e4e"
    btn_fg = "#ffffff"

    # Configure the root background
    root.configure(background=dark_bg)

    # Labels and Entries
    tk.Label(root, text="Game Name", bg=dark_bg, fg=dark_fg).pack(pady=1)
    game_name_entry = tk.Entry(root, bg=entry_bg, fg=entry_fg)
    game_name_entry.pack(pady=1)

    tk.Label(root, text="Password", bg=dark_bg, fg=dark_fg).pack(pady=1)
    password_entry = tk.Entry(root, show="*", bg=entry_bg, fg=entry_fg)
    password_entry.pack(pady=1)

    tk.Label(root, text="Leader", bg=dark_bg, fg=dark_fg).pack(pady=1)
    leader_entry = tk.Entry(root, bg=entry_bg, fg=entry_fg)
    leader_entry.pack(pady=1)
    
    tk.Label(root, text="BattleTag", bg=dark_bg, fg=dark_fg).pack(pady=1)
    battletag_entry = tk.Entry(root, bg=entry_bg, fg=entry_fg)
    battletag_entry.pack(pady=1)

    tk.Label(root, text="Select Script", bg=dark_bg, fg=dark_fg).pack(pady=1)
    run_area = ttk.Combobox(root, values=["MultiLoad", "Chaos Lead", "Baal Leecher"])
    run_area.current(0)
    run_area.pack(pady=1)

    tk.Label(root, text="Class", bg=dark_bg, fg=dark_fg).pack(pady=1)
    playerClass = ttk.Combobox(root, values=["Paladin", "Sorceress"])
    playerClass.current(0)
    playerClass.pack(pady=1)

    hasCTAVar = tk.BooleanVar()
    hasCTAcheckbox = tk.Checkbutton(root, text="Has CTA", variable=hasCTAVar, bg=dark_bg, fg=dark_fg, selectcolor=entry_bg)
    hasCTAcheckbox.pack(pady=1)

    def start_script():
        global hasCTA
        run = run_area.get()
        game_name = game_name_entry.get()
        password = password_entry.get()
        leader = leader_entry.get()
        battletag = battletag_entry.get()
        

        hasCTA = hasCTAVar.get()
        print(f'Has CTA? : {hasCTA}')

        refocus_diablo_window()

        if run == 'Baal Leecher':
            loopBaalLeech(leader, game_name, password,battletag)

        elif run == 'Chaos Lead':
            loopDiabloLead(leader, game_name, password)

        elif run == 'MultiLoad':
            multi_load_script(leader, game_name, password,battletag)

    def stop_script():
        sys.exit()

    button_frame = tk.Frame(root, bg=dark_bg)
    button_frame.pack(pady=5)

    start_button = tk.Button(button_frame, text="Start", command=start_script, bg=btn_bg, fg=btn_fg)
    start_button.pack(side="left", padx=5)

    stop_button = tk.Button(button_frame, text="Stop", command=stop_script, bg=btn_bg, fg=btn_fg)
    stop_button.pack(side="left", padx=5)

    root.mainloop()

@bot.event
async def on_ready():
    #load_data()  # Ensure that data is loaded from JSON when the bot starts\
    print(f'Bot is online as {bot.user}')

@bot.slash_command(name="hustleload", description="Load fillers into game - (gameName, password, leaderName)")
async def hustleload(ctx: discord.ApplicationContext, gamename: str, password: str, leader: str):      # Pass in count
    print('In hustleload():')
    print(f'gameName: {gamename}   -  password: {password}  -  leaderName: {leader}')
    multi_load_script(leader, gamename, password, firstGame=True)
    await ctx.respond(f"Loaded game {gamename} with leader {leader}.")

if __name__ == "__main__":
    #bot.run('xxxxx')
    create_gui()
    
