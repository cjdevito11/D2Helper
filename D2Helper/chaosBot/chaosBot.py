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
import pygetwindow as gw  # Import for window management

pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configuration for image paths and hotkeys
star_images = ['starPart1.jpg', 'starPart2.jpg', 'starPart3.jpg']
seal_images = ['chaosSeal.jpg', 'chaosSeal1.jpg']
waypoint_image = 'waypoint.jpg'
riverwaypoint_image = 'riverWP.jpg'
river_image = 'riverOfFlameWP.jpg'
starImg = 'chaosStar.jpg'
sealImg = 'chaosSeal.jpg'
sealHoverImg = 'chaosSealHover.jpg'

tp_hotkey = 'x'
teleHotkey = 'j'
boHotkey = 'g'
bcHotkey = 'f'

pickit_folder = 'pickit'  

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
#pickit_images = [os.path.join(pickit_folder, img) for img in os.listdir(pickit_folder) if img.endswith('.png')]


def find_image(image_path, confidence=0.5):
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        return location
    except pyautogui.ImageNotFoundException:
        return None

def click_image(location, click_delay=.5):
    if location:
        pyautogui.moveTo(pyautogui.center(location))
        time.sleep(.5)  # Small delay to simulate hovering
        pyautogui.click(pyautogui.center(location))
        time.sleep(click_delay)
        return True
    return False

def scan_for_items():
    for pickit_image in pickit_images:
        if not os.path.exists(pickit_image):
            print(f"Image not found: {pickit_image}")
            continue

        try:
            item_location = pyautogui.locateOnScreen(pickit_image, confidence=0.7)
            if item_location:
                pyautogui.moveTo(pyautogui.center(item_location))
                pyautogui.click()
                time.sleep(1)  # Delay to ensure item is picked up
        except pyautogui.ImageNotFoundException:
            print(f"Failed to locate image on screen: {pickit_image}")
        except Exception as e:
            print(f"Unexpected error: {e}")

# Function to confirm if in Act 4 (placeholder, needs implementation)
def confirm_act4():
    pass

def wpToRiver():
    print("Starting to search for Waypoint...")
    x = 0
    while True:
        try:
            waypoint_position = pyautogui.locateOnScreen(waypoint_image, confidence=0.6)
            if waypoint_position:
                print(f"Waypoint found at {waypoint_position}.")
                pyautogui.moveTo(waypoint_position)
                pyautogui.click()
                time.sleep(4)
                riverPos = pyautogui.locateOnScreen(river_image, confidence=0.65)
                if riverPos:
                    print(f"River found at {riverPos}.")
                    pyautogui.moveTo(riverPos)
                    pyautogui.click()
                    time.sleep(3)
                    while x == 0:
                        riverwaypoint_position = pyautogui.locateOnScreen(riverwaypoint_image, confidence=0.5)
                        if riverwaypoint_position:
                            print(f"Waypoint found at {riverwaypoint_position}.")
                            pyautogui.moveTo(riverwaypoint_position)
                            pyautogui.press(teleHotkey)
                            x = 1
                        time.sleep(2)
                    break
                else:
                    print("Found WP, Can't find River")
                    
            else:
                print("No Waypoint found, retrying...")
            time.sleep(5)
        except:
            print("Failed to locate waypoint.")
            time.sleep(5)

def preBuff():
    hasCTA = True
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
        pyautogui.press("v")
        time.sleep(2)
        pyautogui.press("w")
    time.sleep(1)

def teleRiver():
    preBuff()
    pyautogui.moveTo(1910, 80)
    x = 0
    while (x < 19):
        print(f"Tele - Press: {teleHotkey}")
        pyautogui.press(teleHotkey)
        time.sleep(.5)
        x = x + 1

def centerStar(starPos, location):
    # Move to the center of the star and drop a TP
    if location == 'Bottom':
        center_x = starPos.left + starPos.width // 2 + 200
        center_y = starPos.bottom + starPos.height // 2 + 50
        pyautogui.moveTo(center_x, center_y)
        #pyautogui.click()
        pyautogui.press(teleHotkey)
        time.sleep(1)  # Wait a second to ensure movement
        print("Centered Star (Bottom)")
    if location == 'Left':
        center_x = starPos.left + starPos.width // 2 + 200
        center_y = starPos.top + starPos.height // 2 + 50
        pyautogui.moveTo(center_x, center_y)
        #pyautogui.click()
        pyautogui.press(teleHotkey)
        time.sleep(1)  # Wait a second to ensure movement
        print("Centered Star (Left)")
    if location == 'Top':
        center_x = starPos.left - starPos.width // 2 - 200
        center_y = starPos.bottom + starPos.height // 2 + 50
        pyautogui.moveTo(center_x, center_y)
        #pyautogui.click()
        pyautogui.press(teleHotkey)
        time.sleep(1)  # Wait a second to ensure movement
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
                        time.sleep(1)  # Wait a second to ensure movement
                        break
                except:
                    print("Issue locating Star")
            if star_found:
                # Move to the center of the star and drop a TP
                #center_x = starPos.left + starPos.width // 2
                #center_y = starPos.top - starPos.height // 1.5
                #pyautogui.moveTo(center_x, center_y)
                #pyautogui.click()
                #time.sleep(1)  # Wait a second to ensure movement
                print("Found Star (Bottom) - Town portal dropped.")
                #centerStar(starPos,'Bottom')
                openTP()
                time.sleep(2)
                preBuff()
                break
            else:
                print("Can't find star, moving towards the top right.")
                pyautogui.moveTo((1250, 450))
                pyautogui.click()
                time.sleep(2)  # Wait a second before checking again
                scan_for_items()  # Scan for items each movement
                count = count + 1
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
                        time.sleep(1)  # Wait a second to ensure movement
                        break
                except:
                    print("Issue locating Star")
            if star_found:
                # Move to the center of the star and drop a TP
                center_x = starPos.left - starPos.width // 2
                center_y = starPos.bottom + starPos.height // 2
                pyautogui.moveTo(center_x, center_y)
                pyautogui.click()
                print("Found Star (Top) - Town portal dropped.")
                centerStar(starPos,'Top')
                break
            else:
                print("Can't find star, moving towards the Bottom right.")
                pyautogui.moveTo((1400, 900))
                pyautogui.click()
                time.sleep(2)  # Wait a second before checking again
                #scan_for_items()  # Scan for items each movement
                count = count + 1
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
                        time.sleep(1)  # Wait a second to ensure movement
                        break
                except:
                    print("Issue locating Star")
            if star_found:
                # Move to the center of the star and drop a TP
                center_x = starPos.left + starPos.width // 2 + 200
                center_y = starPos.bottom + starPos.height // 2 
                pyautogui.moveTo(center_x, center_y)
                pyautogui.click()
                time.sleep(1)  # Wait a second to ensure movement
                print("Found star (Left) - Town portal dropped.")
                centerStar(starPos,'Left')
                break
            else:
                if count == 0:
                    pyautogui.moveTo((1250, 600))
                    pyautogui.press(teleHotkey)
                print("Cant find star, moving to the right")
                pyautogui.moveTo((1250, 850))
                pyautogui.click()
                time.sleep(2)  # Wait a second before checking again
                #scan_for_items()  # Scan for items each movement
                count = count + 1
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
                        time.sleep(1)  # Wait a second to ensure movement
                        break
                except:
                    print("Issue locating Star")
            if star_found:
                # Move to the center of the star and drop a TP
                center_x = starPos.left - starPos.width // 2 - 200
                center_y = starPos.bottom + starPos.height // 2 
                pyautogui.moveTo(center_x, center_y)
                pyautogui.click()
                time.sleep(1)  # Wait a second to ensure movement
                print("Found star (Left) - Town portal dropped.")
                centerStar(starPos,'Right')
                break
            else:
                if count == 0:
                    pyautogui.moveTo((150, 60))
                    pyautogui.press(teleHotkey)
                print("Cant find star, moving to the Left")
                pyautogui.moveTo((150, 50))
                pyautogui.click()
                time.sleep(2)  # Wait a second before checking again
                #scan_for_items()  # Scan for items each movement
                count = count + 1
    except Exception as e:
        print(f"Couldn't findStarLeft(): {e}")
        
def findSeal():
    print("Looking for Seal")
    try:
        seal_found = False
        for seal_image in seal_images:
            try:
                sealPos = pyautogui.locateOnScreen(seal_image, confidence=0.3)
                if sealPos:
                    seal_found = True
                    print(f"Seal found using {seal_image} at {sealPos}.")
                    pyautogui.moveTo(sealPos)
                    pyautogui.click()
                    time.sleep(1)  # Wait a second to ensure movement
                    break
            except:
                print("Issue locating Seal")
        if seal_found:
            pyautogui.moveTo(sealPos)
            pyautogui.click()
            time.sleep(3)  # Wait a second to ensure movement
        else:
            print("Can't find seal.")
    except Exception as e:
        print(f"Couldn't findSeal(): {e}")

def openTP():
    pyautogui.press(tp_hotkey)
    #time.sleep(5)
    #preBuff()

def vizier():
    vizierWaypoints = [(200, 250), (100, 50), (200, 750), (100, 450),(200,600),(200,50), (800,20),(800,20),(50,600)]
    doubleCheck = [(25, 650), (1500, 800), (100, 100), (900, 100), (1700, 600)]
    count = 0
    for step in vizierWaypoints:
        x, y = step
        pyautogui.moveTo(x, y)
        if count < 2 or count > 5:
            pyautogui.press(teleHotkey)
        pyautogui.click()
        time.sleep(4)
        scan_for_items()  # Scan for items each movement
        #findSeal()
        count += 1
   ## for step in doubleCheck:
   #     x, y = step
   #     pyautogui.moveTo(x, y)
   #     pyautogui.press(teleHotkey)
   #     time.sleep(1)
   #     scan_for_items()  # Scan for items each movement
   ##     findSeal()
    #findSeal()
    time.sleep(5)

def vizierToStar():
    vizierToStar = [(500,650),(1650, 650), (1650, 900), (1650, 750), (1050, 700),(1650,900),(1600,800)]
    count = 0
    for step in vizierToStar:
        x, y = step
        pyautogui.moveTo(x, y)
        if count < 3:
            pyautogui.press(teleHotkey)
        pyautogui.click()
        time.sleep(1)
        #scan_for_items()  # Scan for items each movement
        count += 1
    findStarLeft()

def deSeis():
    deSeisSteps = [(1750, 100), (1750, 100), (1750, 150), (1750, 50),(1750, 550)]
    #doubleCheck = [(25, 650), (1500, 800), (100, 100), (900, 100), (1700, 600)]
    count = 0
    for step in deSeisSteps:
        x, y = step
        pyautogui.moveTo(x, y)
        #if count < 2:
        pyautogui.press(teleHotkey)
        #pyautogui.click()
        time.sleep(4)
        #scan_for_items()  # Scan for items each movement
        #findSeal()
        count += 1
    #for step in doubleCheck:
    #    x, y = step
    #    pyautogui.moveTo(x, y)
    #    pyautogui.press(teleHotkey)
    #    time.sleep(1)
    #    scan_for_items()  # Scan for items each movement
    #    findSeal()
    time.sleep(2)

def deSeisToStar():
    deSeisToStar = [(200, 1000), (50, 500), (150, 1000), (800,700), (1250, 700), (1050, 800), (1050, 800)]
    count = 0
    for step in deSeisToStar:
        x, y = step
        pyautogui.moveTo(x, y)
        if count < 3:
            pyautogui.press(teleHotkey)
            time.sleep(2)
        pyautogui.click()
        time.sleep(1)
        #scan_for_items()  # Scan for items each movement
        count += 1
    findStarTop()

def infector():
    infectorSteps = [(1600, 900), (1700, 950), (1700, 850), (1800, 950), (1800, 950), (1600, 550), (1300, 650), (400,700)]
    doubleCheck = [(25, 650), (1500, 800), (100, 100), (900, 100), (1700, 600)]
    count = 0
    for step in infectorSteps:
        x, y = step
        pyautogui.moveTo(x, y)
        if count < 4:
            pyautogui.press(teleHotkey)
            time.sleep(1)
        pyautogui.click()
        time.sleep(5)
        #scan_for_items()  # Scan for items each movement
        #findSeal()
        count += 1
    #for step in doubleCheck:
    #    x, y = step
    #    pyautogui.moveTo(x, y)
    #    pyautogui.press(teleHotkey)
    #    time.sleep(1)
        #scan_for_items()  # Scan for items each movement
        #findSeal()
    time.sleep(5)

def infectorToStar():
    deSeisToStar = [(150, 150), (150, 100), (150, 500), (150, 500), (150, 400), (150, 500)]
    count = 0
    for step in deSeisToStar:
        x, y = step
        pyautogui.moveTo(x, y)
        if count < 2:
            pyautogui.press(teleHotkey)
        pyautogui.click()
        time.sleep(2)
        scan_for_items()  # Scan for items each movement
        count += 1
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

def wait_for_leader_to_leave(leader, game_name, password):
    while True:
        chat_text = setup.read_screen_text(region=(0, 650, 600, 930))
        if f"{leader} left our world" in chat_text:
            print("Leader has left the world")
            save_and_quit()
            next_game_name = increment_game_name(game_name)
            loop_script(leader, next_game_name, password)
            break

def save_and_quit():
    save_and_quit_pos = (950, 525)  # Replace with actual coordinates
    pyautogui.press('esc')
    time.sleep(.5)
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

def enterGame(game_name, password):
    lobby_pos = (1100, 1050)
    game_name_pos = (1500, 220)
    password_pos = (1500, 290)
    join_game_pos = (1450, 710)
    
    #pyautogui.click(lobby_pos)
    time.sleep(1)
    pyautogui.click(game_name_pos)
    print(f"Writing game_name - {game_name}.")
    for _ in range(20):
        pyautogui.press('backspace')
    pyautogui.write(game_name, interval=0.05)
    time.sleep(1)
    
    pyautogui.click(password_pos)
    print(f"Writing password - {password}.")
    for _ in range(20):
        pyautogui.press('backspace')
    pyautogui.write(password, interval=0.05)
    time.sleep(1)
    
    print(f"Joining Game.")
    pyautogui.click(join_game_pos)
    time.sleep(7)

def post_to_discord(game_name, password):
    time.sleep(1)
    discord_window = gw.getWindowsWithTitle('#game-names')[0]
    if discord_window:
        discord_window.activate()  # Focus the Discord window
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
        diablo_window.activate()  # Refocus on the Diablo window
        time.sleep(2)
        
def loop_script(leader, game_name, password):
    post_to_discord(game_name, password)
    refocus_diablo_window()
    enterGame(game_name, password)
    confirm_act4()
    wpToRiver()
    teleRiver()
    findStarBottom()
    preBuff()
    walkChaos()
    check_end_of_chaos(leader, game_name, password)

def create_gui():
    root = tk.Tk()
    root.title("AuraBot")
    root.geometry("300x350+1610+750")
    root.attributes('-alpha', 0.6)

    tk.Label(root, text="Game Name").pack()
    game_name_entry = tk.Entry(root)
    game_name_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    tk.Label(root, text="Leader").pack()
    leader_entry = tk.Entry(root)
    leader_entry.pack()

    tk.Label(root, text="Run Area").pack()
    run_area = ttk.Combobox(root, values=["Chaos"])
    run_area.current(0)
    run_area.pack()

    def start_script():
        game_name = game_name_entry.get()
        password = password_entry.get()
        leader = leader_entry.get()
        post_to_discord(game_name, password)
        refocus_diablo_window()
        enterGame(game_name, password)
        confirm_act4()
        wpToRiver()
        teleRiver()
        findStarBottom()
        openTP()
        walkChaos()
        check_end_of_chaos(leader, game_name, password)

    def stop_script():
        sys.exit()

    start_button = tk.Button(root, text="Start", command=start_script)
    start_button.pack()

    stop_button = tk.Button(root, text="Stop", command=stop_script)
    stop_button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
