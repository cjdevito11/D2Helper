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

pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

speed_multiplier = 0.6  # 10% faster (use 1.1 for 10% slower, etc.)

# Configuration for image paths and hotkeys
shop_images = ['images/town/jamella/jamella1.jpg','images/town/jamella/jamella2.jpg','images/town/jamella/jamella3.jpg', 'images/town/jamella/jamella4.jpg', 'images/town/jamella/jamella5.jpg','images/town/jamella/jamella6.jpg']
jamellaSelect = 'images/town/jamella/jamellaSelect.jpg'
star_images = ['starPart1.jpg', 'starPart2.jpg', 'starPart3.jpg']
seal_images = ['chaosSeal.jpg', 'chaosSeal1.jpg', 'seal1.jpg', 'seal3.jpg', 'seal4.jpg', 'seal5.jpg', 'seal6.jpg', 'seal8.jpg', 'seal9.jpg', 'seal11.jpg', 'seal12.jpg', 'seal13.jpg']
waypoint_image = 'wp.jpg' 
riverwaypoint_image = 'riverWP.jpg'
river_image = 'riverOfFlameWP.jpg'
river_terror_image = 'riverTerrorWp.jpg'
starImg = 'chaosStar.jpg'
sealImg = 'chaosSeal.jpg'
sealHoverImg = 'chaosSealHover.jpg'

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

def get_screen_position(x_percent, y_percent):
    screen_width, screen_height = pyautogui.size()
    return int(screen_width * x_percent), int(screen_height * y_percent)

def confirm_act4():
    pass

def confirm_act5():
    pass


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
        selectPos = pyautogui.locateOnScreen(jamellaSelect,confidence=0.45)
        if selectPos:
            print("Selecting Trade")
            pyautogui.moveTo(selectPos)
            #time.sleep(10)
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

def wait_for_tp_and_confirm_leader(leader, game_name, password):
    print("Starting to search for TPs...")
    while True:
        try:
            checkLeaderLeft(leader, game_name, password)
            tp_positions = list(pyautogui.locateAllOnScreen('tp.png', confidence=0.7))
            if tp_positions:
                for tp_pos in tp_positions:
                    pyautogui.moveTo(tp_pos)
                    x, y, w, h = tp_pos.left, tp_pos.top, tp_pos.width, tp_pos.height  # Adjust to top-left corner
                    text_region = (x - 100, y - 100), (x + 100, y - 50)
                    #text = setup.read_screen_text(region=text_region)
                    #if leader_name in text:
                    print(f"Leader's TP found at ({x}, {y}).")
                    time.sleep(10) # wait 15 seconds for safety
                    pyautogui.click(tp_pos)
                    return
                    #else:
                    #    print(f"TP at ({x}, {y}) is not the leader's TP.")
            else:
                print("No TP found, retrying...")
            time.sleep(3)
        except:
            print("failed tp")
            time.sleep(3)

# Function to wait for leader to leave and rejoin the next game
def wait_for_leader_to_leave(leader, game_name, password):
    x = 0
    while True:
        x = x + 1
        if (x > 100):
            pass
        time.sleep(1)
        print('Waiting for leader to leave')
        chat_text = setup.read_screen_text(region=(0, 650, 650, 930))  # Adjust region to match chat area
        print(f'chat_text: {chat_text}')
        if f"{leader} left our world" in chat_text:
            print("Leader has left the world")
            save_and_quit()
            next_game_name = increment_game_name(game_name)
            loopBaalLeech(leader,next_game_name,password)
            #while True:
                #enter_game(next_game_name, password)
                #time.sleep(10)
                #chat_text = setup.read_screen_text(region=(0, 650, 600, 930))  # Adjust region to match chat area
                #if "Your connection has been interrupted" not in chat_text:
                    #break
            break

def checkLeaderLeft(leader, game_name, password):
    print('Check if Leader Left')
    chat_text = setup.read_screen_text(region=(0, 650, 650, 930))  # Adjust region to match chat area
    print(f'chat_text: {chat_text}')
    if f"{leader} left our world" in chat_text:
        print("Leader has left the world")
        save_and_quit()
        next_game_name = increment_game_name(game_name)
        loopBaalLeech(leader,next_game_name,password)

def loopBaalLeech(leader,game_name,password):
    joinGame(game_name, password)
    confirm_act5()
    wait_for_tp_and_confirm_leader(leader, game_name, password)
    preBuff()
    wait_for_leader_to_leave(leader, game_name, password)



#Fix if failed to join game
#Fix if portal opened to area other than Throne
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
    x, y = get_screen_position(x_percent, y_percent)
    pyautogui.moveTo(x, y)
    if (click == 'left'):
        print('click left')
        pyautogui.click()
    if (click == 'right'):
        print('click right')
        pyautogui.click(button='right')

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
        loop_script(leader, next_game_name, password)
    else:
        next_game_name = increment_game_name(game_name)
        loop_script(leader, next_game_name, password)
    return True

def save_and_quit():
    time.sleep(.5)
    pyautogui.press('esc')
    click_at_percentage(950/1900, 525/1200)  # Coordinates based on initial resolution
    pyautogui.press('esc')
    time.sleep(.5)
    pyautogui.click(get_screen_position(950/1900, 525/1200))

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
    time.sleep(1)
    
    click_at_percentage(*password_pos)
    print(f"Writing password - {password}.")
    for _ in range(20):
        pyautogui.press('backspace')
    pyautogui.write(password, interval=0.05)
    time.sleep(1)
    
    print(f"Joining Game.")
    click_at_percentage(*create_game_pos)
    time.sleep(7)
    
def joinGame(game_name, password):
    game_name_pos = (1440/1900, 191/1200)
    password_pos = (1700/1900, 191/1200)
    join_game_pos = (1470/1900, 725/1200)
    
    #click_at_percentage(*lobby_pos)
    time.sleep(1)
    click_at_percentage(*game_name_pos)
    click_at_percentage(*game_name_pos)
    print(f"Writing game_name - {game_name}.")
    for _ in range(20):
        pyautogui.press('backspace')
    pyautogui.write(game_name, interval=0.05)
    time.sleep(1)
    
    click_at_percentage(*password_pos)
    click_at_percentage(*password_pos)
    print(f"Writing password - {password}.")
    for _ in range(20):
        pyautogui.press('backspace')
    pyautogui.write(password, interval=0.05)
    time.sleep(1)
    
    print(f"Joining Game.")
    click_at_percentage(*join_game_pos)
    time.sleep(7)

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
    diablo_window = gw.getWindowsWithTitle('Diablo II: Resurrected')[0]
    if diablo_window:
        diablo_window.activate()
        time.sleep(2)
 
def loop_script(leader, game_name, password):
    #post_to_discord(game_name, password)
    refocus_diablo_window()
    createGame(game_name, password)
    confirm_act4()
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
    root.geometry("300x350+1610+750")
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

    tk.Label(root, text="Select Script", bg=dark_bg, fg=dark_fg).pack(pady=1)
    run_area = ttk.Combobox(root, values=["Chaos Lead", "Baal Leecher"])
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
        
        hasCTA = hasCTAVar.get()
        print(f'Has CTA? : {hasCTA}')
        
        refocus_diablo_window()
        
        if run == 'Baal Leecher':
            print("GOT BAAL LEECHER")
            #refocus_diablo_window()
            loopBaalLeech(leader,game_name,password)    
            
        if run == 'Chaos Lead':
            print("GOT CHAOS LEECHER")
            #post_to_discord(game_name, password)
            #refocus_diablo_window()
            createGame(game_name, password)
            confirm_act4()
            prep()
            wpToRiver()
            teleRiver()
            findStarBottom()
            openTP()
            walkChaos()
            check_end_of_chaos(leader, game_name, password)

    def stop_script():
        sys.exit()

    button_frame = tk.Frame(root, bg=dark_bg)
    button_frame.pack(pady=5)

    start_button = tk.Button(button_frame, text="Start", command=start_script, bg=btn_bg, fg=btn_fg)
    start_button.pack(side="left", padx=5)

    stop_button = tk.Button(button_frame, text="Stop", command=stop_script, bg=btn_bg, fg=btn_fg)
    stop_button.pack(side="left", padx=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
