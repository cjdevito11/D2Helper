from PIL import ImageGrab
import numpy as np
import win32gui
import cv2
import win32api
import json
import pyautogui
import time
import os
import re
import pytesseract

# Global variables
global_x = 0
global_y = 0
hotkeys_registered = False
shutdown_flag = False

def load_config():
    with open("config.json") as f:
        return json.load(f)

def shut_down():
    global shutdown_flag
    print("Shutting down the script...")
    shutdown_flag = True

def print_mouse_coords_relative_to_hwnd(hwnd):
    global global_x, global_y
    rect = win32gui.GetWindowRect(hwnd)
    x_left, y_top = rect[0], rect[1]
    x, y = win32api.GetCursorPos()
    global_x, global_y = x - x_left, y - y_top
    print(f"Mouse Coords: ({x}, {y})")
    print(f"Mouse coords relative to HWND: ({global_x}, {global_y})")

def click_saved_position(hwnd):
    global global_x, global_y
    pyautogui.moveTo(global_x, global_y)
    pyautogui.click()

def count_images_on_screen(template_path, distance_threshold=10):
    item_name = os.path.basename(template_path)
    item_name, extension = os.path.splitext(item_name)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Failed to load template image from {template_path}")
        return []
    screen_pil = ImageGrab.grab()
    screen_np = np.array(screen_pil)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)
    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    matches = list(zip(*loc[::-1]))
    grouped_matches = []
    for pt in matches:
        center_pt = (pt[0] + template.shape[1] // 2, pt[1] + template.shape[0] // 2)
        found_group = False
        for group in grouped_matches:
            dist = np.sqrt((group[0] - center_pt[0]) ** 2 + (group[1] - center_pt[1]) ** 2)
            if dist < distance_threshold:
                found_group = True
                break
        if not found_group:
            grouped_matches.append(center_pt)
    total_matches = len(grouped_matches)
    print(f"{item_name} Runes: {total_matches}")
    return grouped_matches

def get_rune_positions(template_folder):
    runes_positions = {}
    for filename in os.listdir(template_folder):
        if filename.lower().endswith(".png"):
            template_path = os.path.join(template_folder, filename)
            rune_name = os.path.splitext(os.path.basename(template_path))[0]
            grouped_matches, count = count_images_on_screen(template_path)
            runes_positions[rune_name] = {'positions': grouped_matches, 'count': count}
    return runes_positions

rune_map = [
    "El Rune", "Eld Rune", "Tir Rune", "Nef Rune",
    "Eth Rune", "Ith Rune", "Tal Rune", "Ral Rune",
    "Ort Rune", "Thul Rune", "Amn Rune", "Sol Rune",
    "Shael Rune", "Dol Rune", "Hel Rune", "Io Rune",
    "Lum Rune", "Ko Rune", "Fal Rune", "Lem Rune",
    "Pul Rune", "Um Rune", "Mal Rune", "Ist Rune",
    "Gul Rune", "Vex Rune", "Ohm Rune", "Lo Rune",
    "Sur Rune", "Ber Rune", "Jah Rune", "Cham Rune",
    "Zod Rune", "Blank Space"
]

def get_rune_sort_key(item_name):
    try:
        return rune_map.index(item_name)
    except ValueError:
        print(f"Warning: '{item_name}' not found in rune_map.")
        return len(rune_map)

def sort_runes(runes_dict, sort_type):
    runes_list = [(rune_name, rune_info) for rune_name, rune_info in runes_dict.items()]
    if sort_type == "High->Low":
        sorted_runes = sorted(runes_list, key=lambda x: x[1]['count'], reverse=True)
    elif sort_type == "Low->High":
        sorted_runes = sorted(runes_list, key=lambda x: x[1]['count'])
    elif sort_type == "A-Z":
        sorted_runes = sorted(runes_list, key=lambda x: x[0])
    elif sort_type == "Z-A":
        sorted_runes = sorted(runes_list, key=lambda x: x[0], reverse=True)
    elif sort_type == "Runeword-based":
        sorted_runes = sorted(runes_list, key=lambda x: get_rune_sort_key(x[0]))
    return sorted_runes

def move_item(current_position, target_position):
    pyautogui.moveTo(current_position[0], current_position[1])
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(target_position[0], target_position[1])
    pyautogui.click()
    time.sleep(1)

def schedule_periodic_update(root, callback, interval):
    callback()  # Call the callback function immediately
    root.after(interval, lambda: schedule_periodic_update(root, callback, interval))

def clean_ocr_output(ocr_text):
    corrections = {
        '@': '0',
        '#': '+',
        'Te': 'to',
        'T@': 'to',
        'T®': 'to',
        '+100% FASTER CAST RATE': '+10% FASTER CAST RATE',
        '100% FASTER CAST RATE': '10% FASTER CAST RATE',
        'ST0®LEN': 'STOLEN',
        'ST0LEN': 'STOLEN',
        'SHIFT * LEFT CLICK T® EQUIP pee': '',
        'CTRL + Left CLick to Meve': '',
        '4 H0LD SHIFT T® COMPARE ne': '',
        '4 H0LD SHIFT T® COMPARE i': '',
        '1Q% FASTER CAST RATE ia': '10% FASTER CAST RATE',
        'P0IS0N': 'POISON',
        'P0ISON': 'POISON',
        'P0Is0N': 'POISON',
        'P0IsON': 'POISON',
        'P0IseN': 'POISON',
        'PeIsen': 'POISON',
        'PeIs0n': 'POISON',
        'P0Isen': 'POISON',
        'Ce0LD': 'COLD',
        'CeLpD': 'COLD',
        'CeLp': 'COLD',
        'Ce0LpD': 'COLD',
        'DextoRITY': 'DEXTERITY',
        'DAmaAce': 'DAMAGE',
        '+1Q00': '+100',
        '+I]': '+11',
        '+]': '+1',
        '+I': '+1'
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

def calculate_item_score(stats, attribute_points):
    score = 0
    for stat, value in stats.items():
        points_awarded = get_points_for_stat(stat, value, attribute_points)
        score += points_awarded
    return score

def capture_item_tooltip(area):
    return ImageGrab.grab(bbox=area)

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def get_points_for_stat(stat_name, stat_value, attribute_points):
    points = 0
    if isinstance(stat_value, tuple):
        stat_value = stat_value[0]
    stat_values = attribute_points.get(stat_name, {})
    points = stat_values.get(str(stat_value), 0)
    return points
