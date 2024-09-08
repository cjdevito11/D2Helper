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
SHOP_GRID_WIDTH = 8
SHOP_GRID_HEIGHT = 10
STASH_GRID_WIDTH = 8
STASH_GRID_HEIGHT = 10

INVENTORY_FILE = 'inventory.json'
CLEAN_LOG_FILE = 'clean_log.txt'
LOG_FILE = 'ring_log.txt'

# Load the ring score configuration
with open('clawScore.json', 'r') as clawScorejson:
    attribute_points = json.load(clawScorejson)

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

def go_through_anya_portal():
    # Find the red portal and go through it
    print("Looking for Anya's red portal...")
    portal_coords = locate_on_screen('images/portal1.png')  # Assuming you have a screenshot
    if portal_coords:
        print(f"Found portal at {portal_coords}, entering...")
        pyautogui.moveTo(portal_coords)
        pyautogui.click()
        time.sleep(5)  # Wait for the portal transition

        # After entering, come back through the portal
        town_portal_coords = locate_on_screen('town_portal.png')  # Assuming you have a screenshot
        if town_portal_coords:
            print(f"Found town portal at {town_portal_coords}, returning to town...")
            pyautogui.moveTo(town_portal_coords)
            pyautogui.click()
            time.sleep(5)  # Wait for transition back to town

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

def scan_for_claws():
    print("Scanning shop for claws...")
    claw_positions = [
        (100, 200), (300, 200), (500, 200),  # Add specific coordinates where claws are likely found
        (100, 400), (300, 400), (500, 400)
    ]
    print("Attempting to find ring coordinates...")
    clawTypeOneCoords = locate_on_screen('images/claw1.png')
    clawTypeTwoCoords = locate_on_screen('images/claw2.png')
    claws_found = []
    for pos in claw_positions:
        pyautogui.moveTo(pos)
        pyautogui.click()  # Click the claw item in shop
        time.sleep(1)  # Wait for tooltip to load
        tooltip_area = (pos[0], pos[1], pos[0] + 200, pos[1] + 400)
        tooltip_text = capture_item_tooltip(tooltip_area)
        stats = parse_item_stats(tooltip_text, expected_stats)
        score = calculate_item_score(stats, attribute_points)
        
        if score >= 3:
            print(f"Claw at {pos} has score: {score}. Considering purchase.")
            claws_found.append(pos)
        else:
            print(f"Claw at {pos} did not meet score criteria.")
    
    return claws_found

def update_inventory_for_claw(inventory, row, col):
    # Claws take 3 vertical slots, update the inventory accordingly
    inventory[row][col] = 1  # Mark as filled
    inventory[row + 1][col] = 1
    inventory[row + 2][col] = 1
    return inventory

def buy_claw(coords):
    print(f"Buying claw at {coords}...")
    pyautogui.moveTo(coords)
    pyautogui.rightClick(coords)
    print("--Bought Claw--")
    time.sleep(1)  # Wait between purchases

def clawLoop(stop_event, overlay):
    while not is_inventory_full(inventory):
        if stop_event.is_set():
            print("Claw shopping stopped by user.")
            break
        
        claws = scan_for_claws()
        for claw_pos in claws:
            buy_claw(claw_pos)
            
            # Simulate adding a claw to the inventory
            claw_added = False
            for col_index in range(INVENTORY_GRID_WIDTH - 1, -1, -1):
                for row_index in range(INVENTORY_GRID_HEIGHT - 3, -1, -1):  # Check 3 vertical slots
                    x, y = grid_coords[col_index][row_index]
                    row = INVENTORY_GRID_HEIGHT - 1 - row_index
                    col = INVENTORY_GRID_WIDTH - 1 - col_index
                    if inventory[row][col] == 0 and inventory[row + 1][col] == 0 and inventory[row + 2][col] == 0:
                        print(f"** --- Inspect claw at: ({x}, {y}) --- **")
                        pyautogui.moveTo(x, y)
                        time.sleep(4.4)
                        score, stats = inspect_ring_at(x, y)
                        print(f"Claw score: {score}")
                        kept = score >= 3
                        if kept:
                            inventory = update_inventory_for_claw(inventory, row, col)
                        else:
                            pyautogui.keyDown('ctrl')
                            pyautogui.leftClick(x, y)
                            pyautogui.keyUp('ctrl')
                        update_inventory_json(inventory)
                        overlay.update_inventory(inventory)
                        log_ring_info(score, stats, kept)
                        claw_added = True
                        break
                if claw_added:
                    break
        
        # Refresh the shop by going through the portal
        go_through_anya_portal()


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
        self.root.geometry(f"+{screen_width//2 - 100}+50")
        self.root.update()

    def stop_gambling(self):
        self.stop_event.set()

    def start(self):
        self.root.mainloop()

def get_inventory_corners():
    print("Please click the top-left corner of the inventory.")
    top_left = (1406, 580)  # Adjust as needed
    bottom_right = (1835, 825)  # Adjust as needed for 7 columns
    print(f"Top-left corner: {top_left}, Bottom-right corner: {bottom_right}")
    return top_left, bottom_right

def get_grid_coordinates(top_left, bottom_right, window):
    if window == "inventory":
        width = INVENTORY_GRID_WIDTH
        height = INVENTORY_GRID_HEIGHT
    if window =='shop':
        width = SHOP_GRID_WIDTH
        height = SHOP_GRID_HEIGHT
    if window =='shop':
        width = STASH_GRID_WIDTH
        height = STASH_GRID_HEIGHT

    grid_width = (bottom_right[0] - top_left[0]) // INVENTORY_GRID_WIDTH
    grid_height = (bottom_right[1] - top_left[1]) // INVENTORY_GRID_HEIGHT
    coordinates = []
    for col in range(width):
        col_coords = []
        for row in range(height):
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

# Modified main loop for claws instead of rings
def main():
    print("Starting the claw gambling script.")
    inventory = load_inventory_json()
    top_left, bottom_right = get_inventory_corners()
    grid_coords = get_grid_coordinates(top_left, bottom_right, 'inventory')

    stop_event = Event()
    overlay = InventoryOverlay(inventory, stop_event)
    overlay_thread = Thread(target=overlay.start)
    overlay_thread.start()

    while not is_inventory_full(inventory):
        if stop_event.is_set():
            print("Claw shopping stopped by user.")
            break
        
        claws = scan_for_claws()
        for claw_pos in claws:
            buy_claw(claw_pos)
            
            # Simulate adding a claw to the inventory
            claw_added = False
            for col_index in range(INVENTORY_GRID_WIDTH - 1, -1, -1):
                for row_index in range(INVENTORY_GRID_HEIGHT - 3, -1, -1):  # Check 3 vertical slots
                    x, y = grid_coords[col_index][row_index]
                    row = INVENTORY_GRID_HEIGHT - 1 - row_index
                    col = INVENTORY_GRID_WIDTH - 1 - col_index
                    if inventory[row][col] == 0 and inventory[row + 1][col] == 0 and inventory[row + 2][col] == 0:
                        print(f"** --- Inspect claw at: ({x}, {y}) --- **")
                        pyautogui.moveTo(x, y)
                        time.sleep(4.4)
                        score, stats = inspect_ring_at(x, y)
                        print(f"Claw score: {score}")
                        kept = score >= 3
                        if kept:
                            inventory = update_inventory_for_claw(inventory, row, col)
                        else:
                            pyautogui.keyDown('ctrl')
                            pyautogui.leftClick(x, y)
                            pyautogui.keyUp('ctrl')
                        update_inventory_json(inventory)
                        overlay.update_inventory(inventory)
                        log_ring_info(score, stats, kept)
                        claw_added = True
                        break
                if claw_added:
                    break
        
        # Refresh the shop by going through the portal
        go_through_anya_portal()
        clawLoop(stop_event, overlay)

    print("Finished processing.")

if __name__ == "__main__":
    main()