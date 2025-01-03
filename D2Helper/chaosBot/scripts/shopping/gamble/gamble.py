import cv2
import numpy as np
import pyautogui
import json
import os
import time
from datetime import datetime
from tkinter import Tk, Label, StringVar, Button
from threading import Thread, Event
from PIL import ImageGrab
import pytesseract
import re
from utils import capture_item_tooltip, extract_text_from_image

INVENTORY_GRID_WIDTH = 7  # Reduced to 7 columns
INVENTORY_GRID_HEIGHT = 4
INVENTORY_FILE = 'inventory.json'
CLEAN_LOG_FILE = 'clean_log.txt'
LOG_FILE = 'ring_log.txt'

shop_images = ['../../../images/town/act4/jamella/jamella1.png','../../../images/town/act4/jamella/jamella2.png','../../../images/town/act4/jamella/jamella3.png', '../../../images/town/act4/jamella/jamella4.png', '../../../images/town/act4/jamella/jamella5.png','../../../images/town/act4/jamella/jamella6.png','../../../images/town/act4/jamella/jamella7.png']
jamellaGamble = '../../../images/town/act4/jamella/jamellaGamble.png'
jamellaName = '../../../images/town/act4/jamella/jamellaName.png'
failToBuyImage = '../../../images/errors/notEnoughGold.png'

# Load the ring score configuration
with open('ring_score.json', 'r') as ring_score_json:
    attribute_points = json.load(ring_score_json)

expected_stats = {
    'FASTER CAST RATE': ['FASTER CAST RATE'],
    'MINIMUM DAMAGE': ['MINIMUM DAMAGE'],
    'ATTACK RATING': ['ATTACK RATING'],
    'LIFE STOLEN PER HIT': ['LIFE STOLEN PER HIT'],
    'MANA STOLEN PER HIT': ['MANA STOLEN PER HIT'],
    'LIFE': ['LIFE'],
    'MANA': ['MANA'],
    'LIGHTNING RESIST': ['LIGHTNING RESIST'],
    'FIRE RESIST': ['FIRE RESIST'],
    'COLD RESIST': ['COLD RESIST'],
    'POISON RESIST': ['POISON RESIST'],
    'ALL RESISTANCES': ['ALL RESISTANCES'],
    'STRENGTH': ['STRENGTH'],
    'DEXTERITY': ['DEXTERITY'],
    'ENERGY': ['ENERGY'],
    'REPLENISH LIFE': ['REPLENISH LIFE'],
}

def clean_ocr_output(ocr_text):
    corrections = {
        '@': '0',  # Assuming @ is misinterpreted as 0
        'Te': 'to',  # Assuming Te is misinterpreted as to
        'T@': 'to',  # and other similar corrections...
        'T®': 'to',
        'ST0®LEN': 'STOLEN',
        '+100% FASTER CAST RATE': '+10% FASTER CAST RATE',
        '100% FASTER CAST RATE': '10% FASTER CAST RATE',
        'ST0LEN': 'STOLEN',
        'SHIFT * LEFT CLICK T® EQUIP pee': '',
        'CTRL + Left CLick to Meve': '',
        '4 H0LD SHIFT T® COMPARE ne': '',
        '4 H0LD SHIFT T® COMPARE i': '',
        '1Q% FASTER CAST RATE ia': '10% FASTER CAST RATE',
        'P0IS0N': 'POISON',
        'P0ISON': 'POISON',
        'CeLpD': 'COLD',
        'CeLp': 'COLD',
        '+1Q00 to ATTACK RATING': '+100 to ATTACK RATING'
    }
    for wrong, right in corrections.items():
        ocr_text = ocr_text.replace(wrong, right)
    return ocr_text

def parse_item_stats(text, expected_stats):
    stats = {}
    lines = text.split('\n')
    for line in lines:
        clean_line = clean_ocr_output(line).upper()
        for expected_stat in expected_stats:
            if expected_stat in clean_line:
                values = re.findall(r'\d+', clean_line)
                if values:
                    stats[expected_stat] = int(values[0])
                break
    return stats

def get_points_for_stat(stat_name, stat_value, attribute_points):
    points = 0
    if isinstance(stat_value, tuple):  # If stat_value is a tuple, use only the first value.
        stat_value = stat_value[0]
    
    stat_values = attribute_points.get(stat_name, {})
    points = stat_values.get(str(stat_value), 0)  # Convert stat_value to string if your JSON keys are strings.

    return points

def calculate_item_score(stats, attribute_points):
    score = 0
    for stat, value in stats.items():
        points_awarded = get_points_for_stat(stat, value, attribute_points)
        score += points_awarded
    return score

def log_clean(scannedText, cleanedText):
    with open(CLEAN_LOG_FILE, 'a') as f:
        f.write("\n" + "="*40 + "\n")
        f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Scanned Text: \n{scannedText}\n")
        f.write(f"Cleaned Text: \n {cleanedText}\n")
        f.write("="*40 + "\n")
        
def log_ring_info(score, stats, kept):
    with open(LOG_FILE, 'a') as f:
        f.write("\n" + "="*40 + "\n")
        f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Ring Score: {score}\n")
        f.write(f"Stats:\n")
        for stat, value in stats.items():
            f.write(f"  {stat}: {value}\n")
        f.write(f"Kept: {'Yes' if kept else 'No'}\n")
        f.write("="*40 + "\n")

class InventoryOverlay:
    def __init__(self, inventory, stop_event):
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.8)
        self.root.geometry("1500x150+1850+200")
        self.inventory_str = StringVar()
        self.label = Label(self.root, textvariable=self.inventory_str, font=("Helvetica", 16), bg="black", fg="white")
        self.label.pack()
        self.update_inventory(inventory)
        self.update_position()
        
        self.stop_button = Button(self.root, text="Stop", command=self.stop_gambling)
        self.stop_button.pack()

        self.stop_event = stop_event

    def update_inventory(self, inventory):
        inventory_display = '\n'.join([' '.join(map(str, row)) for row in inventory])
        self.inventory_str.set(f"Inventory:\n{inventory_display}")
        self.root.update()

    def update_position(self):
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"125x125+{(screen_width//2) + 450}+50")
        self.root.update()

    def stop_gambling(self):
        self.stop_event.set()

    def start(self):
        self.root.mainloop()

def get_inventory_corners():
    print("Please click the top-left corner of the inventory.")
    top_left = (1070, 510)  # Adjust as needed
    bottom_right = (1530, 715)  # Adjust as needed for 7 columns
    print(f"Top-left corner: {top_left}, Bottom-right corner: {bottom_right}")
    return top_left, bottom_right

def get_grid_coordinates(top_left, bottom_right):
    grid_width = (bottom_right[0] - top_left[0]) // INVENTORY_GRID_WIDTH
    grid_height = (bottom_right[1] - top_left[1]) // INVENTORY_GRID_HEIGHT
    coordinates = []
    for col in range(INVENTORY_GRID_WIDTH):
        col_coords = []
        for row in range(INVENTORY_GRID_HEIGHT):
            x = top_left[0] + col * grid_width + grid_width // 2
            y = top_left[1] + row * grid_height + grid_height // 2
            col_coords.append((x, y))
        coordinates.append(col_coords)
    print("Grid coordinates calculated.")
    for col_coords in coordinates:
        for (x, y) in col_coords:
            print(f"({x}, {y})")
    return coordinates

def find_ring_coordinates():
    print("Attempting to find ring coordinates...")
    ring1off_coords = locate_on_screen('ring1off.png')
    ring1on_coords = locate_on_screen('ring1on.png')
    if ring1off_coords:
        print(f"Found 'ring1off' at {ring1off_coords}")
        return ring1off_coords
    elif ring1on_coords:
        print(f"Found 'ring1on' at {ring1on_coords}")
        return ring1on_coords
    else:
        print("No ring found.")
        return None

def buy_ring(coords):
    print(f"buy_ring @ coords: {coords}")
    if coords:
        pyautogui.moveTo(coords)
        print(f"Would right-click at: {coords}")
        pyautogui.rightClick(coords)
        print("--Bought Ring--")
        #time.sleep(1)  # Wait for 1 second between each purchase

def is_inventory_full(inventory):
    for row in inventory:
        if 0 in row:
            return False
    return True

def inspect_ring_at(x, y):
    area = (x - 600, y - 600, x+200, y)
    image = capture_item_tooltip(area)
    time.sleep(0.2)
    # Save the image for debugging purposes
    ###image.save(f"ring_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

    text = extract_text_from_image(image)
    clean_text = clean_ocr_output(text)
    log_clean(text, clean_text)
    print(f"OCR Text: {clean_text}")  # Debugging print
    stats = parse_item_stats(clean_text, expected_stats)
    print(f"Parsed Stats: {stats}")  # Debugging print
    score = calculate_item_score(stats, attribute_points)
    return score, stats

def update_inventory_json(inventory):
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f)
    print("Inventory updated.")

def load_inventory_json():
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r') as f:
            inventory = json.load(f)
        print("Loaded existing inventory.")
        return inventory
    else:
        print("Creating new inventory.")
        return [[0 for _ in range(INVENTORY_GRID_WIDTH)] for _ in range(INVENTORY_GRID_HEIGHT)]

def locate_on_screen(image_path, retries=5, delay=2):
    for attempt in range(retries):
        try:
            position = pyautogui.locateCenterOnScreen(image_path, confidence=0.6)
            if position:
                print(f"Located {image_path} on attempt {attempt+1}")
                return position
            time.sleep(delay)
        except Exception as e:
            print(f"Failed to locate {image_path} on attempt {attempt+1} due to {e}")
    print(f"Failed to locate {image_path} after {retries} attempts")
    return None

def get_screen_position(x_percent, y_percent):
    screen_width, screen_height = pyautogui.size()
    return int(screen_width * x_percent), int(screen_height * y_percent)

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

def confirmBuy():
    try:
        failToBuy = pyautogui.locateCenterOnScreen(failToBuyImage, confidence=0.6)
        if failToBuy:
            print(f"Located {failToBuyImage}")
            return False
    except Exception as e:
        print(f"Failed to locate {failToBuyImage}")
        return True

def walkForGold():
    goldSteps = [(100,700), (1550, 100),(1550,300),(1550,700),(350,800),(1000,250),(900,600),(350,625),(400,950),(800,750),(1000,650), (900,800)]
    print(f'Walking for gold:\n Steps: {goldSteps}')
    pyautogui.moveTo(goldSteps[0])
    print('Hold Mouse')
    pyautogui.mouseDown()
    for step in goldSteps:
        time.sleep(1)
        #click_at_percentage(*step)
        print(f'Move To: {step}')
        pyautogui.moveTo(step, duration=1)
    print('Let go of mouse')
    pyautogui.mouseUp()
    pyautogui.moveTo(800,275) #walk off corner a little
    time.sleep(.1)
    pyautogui.click()
    
def scanScreenFor(scanImage, conf=0.6):
    try:
        for y in range(10):
            for x in range(50):
                newX = (x*32) + 32
                newY = (y*100)+ 10
                pyautogui.moveTo(newX,newY)
                try:
                    print(f'scanScreenFor({scanImage}) @ ({newX},{newY})')
                    image = pyautogui.locateOnScreen(scanImage, conf)
                    if image:
                        print(f'found {scanImage}')
                        #return True
                except:
                    print('fail')
        #return False
    except:
        print(f'scanScreenFor({scanImage}) failed.')
        #return False

def findShop():
    print("Looking for Jamella")
    try:
        shop_found = False
        for _ in range(5):
            for shop_image in shop_images:
                try:
                    shopPos = pyautogui.locateOnScreen(shop_image, confidence=0.6)
                    if shopPos:
                        time.sleep(.5)
                        shop_found = True
                        print(f"Jamella found using {shop_image} at {shopPos}.")
                        pyautogui.moveTo(shopPos)
                        pyautogui.click()
                        time.sleep(3)  # Wait a second to ensure movement
                        return
                    else:
                        print("Can't find Shop.")
                except:
                    print(f"Issue locating Jamella - Try again")
                    time.sleep(2)
            if shop_found:
                return
            
        print('Couldnt find shop with images, lets move mouse across screen')
        scanScreenFor(jamellaName, conf=0.6)

    except Exception as e:
        print(f"Couldn't findShop(): {e}")
        
def openShopGamble():
    try:
        time.sleep(1)
        gamblePos = pyautogui.locateOnScreen(jamellaGamble,confidence=0.5)
        if gamblePos:
            print("Selecting Gamble")
            pyautogui.moveTo(gamblePos)
            time.sleep(2)
            pyautogui.click()
            time.sleep(1)
    except Exception as e:
        print("couldn't open shop")

def restockGold():
    pyautogui.press('esc')
    pyautogui.press('esc')
    walkForGold()
    findShop()
    openShopGamble()
    time.sleep(2)


def main():
    time.sleep(2)
    print("Starting the script.")
    inventory = load_inventory_json()
    top_left, bottom_right = get_inventory_corners()
    grid_coords = get_grid_coordinates(top_left, bottom_right)

    stop_event = Event()
    overlay = InventoryOverlay(inventory, stop_event)
    overlay_thread = Thread(target=overlay.start)
    overlay_thread.start()

    print(f"Check is_inventory_full inventory: {inventory}")
    while not is_inventory_full(inventory):
        if stop_event.is_set():
            print("Gambling stopped by user.")
            break

        coords = find_ring_coordinates()
        if coords:
            buy_ring(coords)
            if confirmBuy() == False:
                restockGold()
            
            ring_added = False
            for col_index in range(INVENTORY_GRID_WIDTH - 1, -1, -1):
                for row_index in range(INVENTORY_GRID_HEIGHT - 1, -1, -1):
                    x, y = grid_coords[col_index][row_index]
                    row = INVENTORY_GRID_HEIGHT - 1 - row_index
                    col = INVENTORY_GRID_WIDTH - 1 - col_index
                    if inventory[row][col] == 0:
                        print(f"** --- Inspect ring at: ({x}, {y}) --- **")
                        pyautogui.moveTo(x, y)
                        time.sleep(4.4)
                        score, stats = inspect_ring_at(x, y)
                        print(f"Ring score: {score}")
                        kept = score >= 3
                        if kept:
                            inventory[row][col] = score
                        else:
                            inventory[row][col] = 0  # Optionally sell the ring back here
                            pyautogui.keyDown('ctrl')
                            pyautogui.leftClick(x, y)
                            pyautogui.keyUp('ctrl')
                        update_inventory_json(inventory)
                        overlay.update_inventory(inventory)
                        log_ring_info(score, stats, kept)
                        ring_added = True
                        break
                if ring_added:
                    break

    print("Finished processing.")

if __name__ == "__main__":
    main()
