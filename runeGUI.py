import tkinter as tk
from tkinter import ttk
import threading
import os
import cv2
import numpy as np
from PIL import ImageGrab, Image
import pytesseract
from zones import zone_mapping  # Import the zone_mapping dictionary from zones.py
import numpy as np
import json
import pyautogui
import time
import fontstyle
import requests
import keyboard
import re

initial_mouse_position = None

# Theme colors
dark_background_color = "#000000"  # Dark purple, similar to Diablo 2's dark aesthetic
light_background_color = "#EAE3AA"
text_color = "#B9761D"  # Gold text, similar to the iconic Diablo 2 gold lettering
highlight_color = "#ff4500"  # Orange for highlights, selections, etc.

imagePath = r'C:\Users\cjdev\OneDrive\Desktop\New folder\D2R\RuneCount\test-main\images\run'
empty_img_path = os.path.join(imagePath, 'empty.png')
runewordsPath = '../data/runewords.json'

stash_image_path = 'stash.png'
stash_image = cv2.imread(stash_image_path, 0)

terrorApi = "https://d2emu.com/api/v1/tz"

print("Current Working Directory:", os.getcwd())
print("File exists:", os.path.exists(runewordsPath))

# Import necessary functions from your script
from windows10 import count_images_on_screen, get_rune_sort_key, get_rune_positions, sort_runes

INVENTORY_COORDS = (1230, 575,1860,830)
STASH_COORDS = (55, 150, 690, 785)

with open('ring_score.json', 'r') as ring_score_json:
    attribute_points = json.load(ring_score_json)
    
# Global variable to store counted runes
counted_runes = {}

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

def toggle_gui():
    if root.winfo_height() == 30:  # Assuming the button size is 50x50
        root.geometry("200x60+1600+43")  # Adjust size for feature selection dropdown
        root.attributes("-alpha", 0.8)  # Make slightly more opaque
        expand_button.config(text="Select Feature ->")  # Change text
        feature_selection_dropdown.pack()  # Show the dropdown for feature selection
    else:
        root.geometry("30x30+1670+15")
        root.attributes("-alpha", 1)  # Make fully opaque
        expand_button.config(text="^")  # Change text back to expand icon
        feature_selection_dropdown.pack_forget()  # Hide the dropdown
        hide_feature_interfaces()  # Hide all feature interfaces

def hide_feature_interfaces():
    print("Hiding all feature interfaces")
    top_frame.pack_forget()
    bottom_frame.pack_forget()
    # Also forget any other specific widgets that may be visible
    ring_score_label.pack_forget()
    help_text_display.pack_forget()


def feature_selected(event):
    feature_name = selected_feature.get()
    print(f"Feature selected: {feature_name}")  # Debug print to check the captured feature name
    if feature_name == "Rune":
        load_rune_feature_interface()
    elif feature_name == "Ring Scores":
        print("Loading ring score interface")  # Add similar debug prints for other conditions
        load_ring_scores_interface()
    elif feature_name == "Help":
        print("Loading help interface")
        load_help_interface()

def load_rune_feature_interface():
    print("Executing load_rune_feature_interface")
    hide_feature_interfaces()
    root.geometry("1000x300+800+43")
    root.attributes("-alpha", 0.8)
    expand_button.config(text="Minimize ->")
    # Make sure all necessary widgets for Rune Tracking are packed here
    # Example:
    rune_display.pack(expand=True)
    count_button.pack()  # Make sure this is defined if it needs to be visible
    top_frame.pack(expand=True)
    bottom_frame.pack(expand=True) 
    
def load_ring_scores_interface():
    hide_feature_interfaces()
    # Setup GUI for ring scores
    print("Loading Ring Scores Interface")
    # Example: pack components related to ring scores
    ring_score_label.pack(expand=True)
    top_frame.pack(expand=True)
    bottom_frame.pack(expand=True)

def load_help_interface():
    hide_feature_interfaces()
    # Setup GUI for help
    print("Loading Help Interface")
    # Example: pack components related to help
    help_text_display.pack(expand=True)
    top_frame.pack(expand=True)
    bottom_frame.pack(expand=True)

    
def count_runes():
    global counted_runes
    result = count_runes_in_directory(imagePath)  # Ensure this path is correct
    print("Result from count_images_on_screen:", result)  # Debugging statement

    if result is not None and isinstance(result, dict):
        counted_runes = result
        update_display_with_runes()
    else:
        print("No runes counted or an error occurred.")

def count_runes_in_directory(directory_path, distance_threshold=10):
    total_runes_count = {}
    for filename in os.listdir(directory_path):
        if filename.lower().endswith((".png", ".jpg")):  # Make sure it's an image file
            image_path = os.path.join(directory_path, filename)
            rune_positions = count_images_on_screen(image_path, distance_threshold)
            rune_name = os.path.splitext(filename)[0]
            total_runes_count[rune_name] = len(rune_positions)
            
            print(f"{rune_name}s: {len(rune_positions)}")
    return total_runes_count

# Run the counting in a separate thread to prevent GUI freeze
def run_counting_in_thread():
    count_thread = threading.Thread(target=count_runes)
    count_thread.start()

def load_runewords_from_json():
    try:
        with open(runewordsPath, 'r', encoding='utf-8') as file:
            data = file.read()
            return json.loads(data)
    except FileNotFoundError:
        print(f"Error: The file {runewordsPath} was not found.")
    except json.JSONDecodeError as exc:
        print(f"Error: Failed to decode JSON from {runewordsPath}. Exception: {exc}")
    return []

def normalize_rune_name(rune_name):
    # Remove "Rune" suffix and strip extra spaces
    return rune_name.replace("Rune", "").strip()

def check_runeword_availability_and_detail(runewords, counted_runes):
    runeword_details = []
    normalized_counted_runes = {normalize_rune_name(key): value for key, value in counted_runes.items()}

    for runeword in runewords:
        required_runes = runeword['required_runes']
        rune_availability = {rune: normalized_counted_runes.get(normalize_rune_name(rune), 0) for rune in required_runes}
        completion_percentage = sum(min(rune_availability[rune], required_runes.count(rune)) for rune in required_runes) / len(required_runes)
        missing_runes = [rune for rune in required_runes if rune_availability[normalize_rune_name(rune)] < required_runes.count(rune)]
        runeword_details.append({
            'name': runeword['name'],
            'completion': completion_percentage,
            'required_runes': required_runes,  # Add this line
            'missing_runes': missing_runes
        })

    # Sort runewords by completion percentage, highest first
    runeword_details.sort(key=lambda x: x['completion'], reverse=True)
    return runeword_details

def update_display_with_runes():
    rune_display.configure(state='normal')  # Enable editing of the Text widget
    rune_display.delete('1.0', tk.END)  # Clear existing entries

    # Assuming you want a simple, non-color-coded display for counted runes.
    # If you wish to add specific colors for different runes or counts, you'll need to configure and use tags similar to update_display_with_potential_runewords.
    if counted_runes:
        for rune, count in counted_runes.items():
            rune_display.insert(tk.END, f"{rune}: {count}\n")  # Append a newline character for each entry
    else:
        rune_display.insert(tk.END, "No runes to display.\n")

    rune_display.configure(state='disabled')  # Disable editing after updating

def update_display_with_potential_runewords():
    rune_display.configure(state='normal')  # Enable editing of the Text widget
    rune_display.delete('1.0', tk.END)  # Clear existing entries

    runeword_details = check_runeword_availability_and_detail(runewords, counted_runes)
    if runeword_details:
        for index, detail in enumerate(runeword_details):
            if detail['completion'] > 0:  # Show only if there's at least one rune available
                rune_display.tag_configure('gold', foreground='#d5a021')  # Gold
                rune_display.tag_configure('green', foreground='green')  # Green
                rune_display.tag_configure('red', foreground='red')  # Red
                
                # Display runeword name
                rune_display.insert(tk.END, f"{detail['name']}: ", 'gold')
                
                # Display "Runes:" label
                rune_display.insert(tk.END, "Runes: ", 'gold')
                
                # Iterate through required runes to display them in green if available, red if missing
                normalized_counted_runes = {normalize_rune_name(key): value for key, value in counted_runes.items()}
                for rune in detail['required_runes']:
                    rune_name = normalize_rune_name(rune)
                    # Check if the rune is available
                    if rune_name in normalized_counted_runes and normalized_counted_runes[rune_name] > 0:
                        rune_display.insert(tk.END, f"{rune} ", 'green')
                        normalized_counted_runes[rune_name] -= 1  # Decrement count to handle duplicates accurately
                    else:
                        rune_display.insert(tk.END, f"{rune} ", 'red')

                rune_display.insert(tk.END, "\n")  # New line after each runeword's runes

                # Ensure this matches how you've defined and are using the options_frame and runeword_track_var
                tk.Radiobutton(options_frame, text=detail['name'], variable=runeword_track_var, value=index, 
                               command=lambda idx=index: update_runeword_tracking(idx), bg=dark_background_color, fg=text_color).pack(side=tk.LEFT, padx=5)
    else:
        rune_display.insert(tk.END, "No potential runewords with current runes.")
    
    rune_display.configure(state='disabled')  # Disable editing after updating

def update_runeword_tracking():
    selected_index = runeword_track_var.get()
    if selected_index >= 0:  # Valid selection
        selected_detail = runeword_details[selected_index]
        tracking_info = f"{selected_detail['name']}: Completion {selected_detail['completion']*100:.0f}%"
    else:
        tracking_info = "No runeword selected"
    
    tracking_runeword_name.set(tracking_info)
    # Update the label in your transparent tracking window here
    tracking_label.config(text=tracking_info)

def sort_runes(runes_dict, sort_type):
    # Convert the runes dictionary to a list of tuples
    runes_list = list(runes_dict.items())

    # Sorting based on sort_type
    if sort_type == "High->Low":
        sorted_runes = sorted(runes_list, key=lambda x: x[1], reverse=True)
    elif sort_type == "Low->High":
        sorted_runes = sorted(runes_list, key=lambda x: x[1])
    elif sort_type == "A-Z":
        sorted_runes = sorted(runes_list, key=lambda x: x[0])
    elif sort_type == "Z-A":
        sorted_runes = sorted(runes_list, key=lambda x: x[0], reverse=True)
    elif sort_type == "Runeword-based":
        sorted_runes = sorted(runes_list, key=lambda x: get_rune_sort_key(x[0]))

    return sorted_runes
    
def automate_sorting(sort_type):
    print("Starting the sorting process")

    # Getting rune positions
    runes = get_rune_positions(imagePath)
    print(f"Rune positions obtained: {runes}")

    # Sorting runes
    print("*****************")
    print("*****************")
    print("*****************")
    print("*****************")
    print("Try to Sort Runes")
    sorted_runes = sort_runes(runes, sort_type)
    print(f"Sorted runes: {sorted_runes}")

    # Finding empty slots
    empty_slots = find_empty_slots(INVENTORY_COORDS, imagePath)
    print(f"Empty slots found: {empty_slots}")

    # Iterating through sorted runes
    for rune_name, rune_info in sorted_runes:
        print(f"Processing rune: {rune_name}, Rune info: {rune_info}")
        for position in rune_info['positions']:
            print(f"Current rune position: {position}")
            if not empty_slots:
                print("No more empty slots available")
                break

            # Selecting target position and moving rune
            target_pos = empty_slots.pop(0)
            print(f"Moving rune {rune_name} from {position} to {target_pos}")
            move_rune(position, target_pos)
            time.sleep(0.5)

    print("Sorting process completed")

def is_within_area(x, y, area):
    """Check if a point is within the specified rectangular area."""
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = area
    return top_left_x <= x <= bottom_right_x and top_left_y <= y <= bottom_right_y

def find_empty_slots(area_coords):
    print(f"Debug: Starting find_empty_slots for area {area_coords} using template {empty_img_path}")

    empty_slots = []

    template = cv2.imread(empty_img_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Error: Unable to load template image from {empty_img_path}")
        return []

    h, w = template.shape
    print(f"Debug: Template dimensions (height, width): {h}, {w}")

    # Capture the screen area
    left, top, right, bottom = area_coords
    print(f"Debug: Capturing screen area: {(left, top, right, bottom)}")
    screen_pil = ImageGrab.grab(bbox=(left, top, right, bottom))
    screen_np = np.array(screen_pil)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)

    # Template matching
    print("Debug: Performing template matching")
    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.85
    loc = np.where(res >= threshold)

    print(f"Debug: Number of matches found: {len(loc[0])}")
    for pt in zip(*loc[::-1]):  # Switch x and y coordinates
        slot_pos = (pt[0] + left, pt[1] + top)
        print(f"Debug: Empty slot found at: {slot_pos}")
        empty_slots.append(slot_pos)  # Convert to absolute screen coordinates

    print(f"Debug: Total empty slots found: {len(empty_slots)}")
    return empty_slots

def move_rune(start_pos, end_pos):
    pyautogui.moveTo(start_pos[0], start_pos[1])
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.moveTo(end_pos[0], end_pos[1])
    pyautogui.mouseUp()
    time.sleep(0.2)

def fetch_terror_data(terrorApi):
    try:
        response = requests.get(terrorApi)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error: Failed to fetch data from the API")
            return None
    except Exception as e:
        print("Error:", e)
        return None

def display_next_terror_zone(data):
    if "next" in data and len(data["next"]) > 0:
        next_terror_zone_number = int(data["next"][0])  # Convert zone number to integer
        next_terror_zone_name = zone_mapping.get(next_terror_zone_number, "Unknown Zone")  # Get zone name from mapping, default to "Unknown Zone" if not found
        next_terror_label.config(text=f"{next_terror_zone_name}")
    else:
        next_terror_label.config(text="Next Terror Zone not found in data")

def update_next_terror_zone():
    terror_data = fetch_terror_data(terrorApi)
    if terror_data:
        display_next_terror_zone(terror_data)

def toggle_visibility(event):
    if root.attributes("-alpha") == 0:  # If everything is hidden
        root.attributes("-alpha", 1)  # Make everything visible
        top_frame.attributes("-alpha", 1) 
        bottom_frame.attributes("-alpha", 1) 
        terror_window.attributes("-alpha", 1)  
    else:
        root.attributes("-alpha", 0)  # Hide everything
        top_frame.attributes("-alpha", 0)  
        bottom_frame.attributes("-alpha", 0)  
        terror_window.attributes("-alpha", 0)  

def reload_data_every_hour():
    update_next_terror_zone()
    root.after(3600000, reload_data_every_hour)  # Reload data every hour (3600000 milliseconds)

def hide_ring_score(event):
    ring_score_window.withdraw()  # This will hide the window

def capture_item_tooltip(area):
    return ImageGrab.grab(bbox=area)
    
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def get_points_for_stat(stat_name, stat_value, attribute_points):
   # print (f"In get_points_for_stat - stat_name: {stat_name} .. stat_value: {stat_value}")
    points = 0
    if isinstance(stat_value, tuple):  # If stat_value is a tuple, use only the first value.
        stat_value = stat_value[0]
    
    stat_values = attribute_points.get(stat_name, {})
    points = stat_values.get(str(stat_value), 0)  # Convert stat_value to string if your JSON keys are strings.

    print(f"Stat: {stat_name}, Value: {stat_value}, Points Awarded: {points}")
    return points

def calculate_item_score(stats, attribute_points):
    print(f"Parsed stats: {stats}")
    score = 0
    for stat, value in stats.items():
        points_awarded = get_points_for_stat(stat, value, attribute_points)
        score += points_awarded
        print(f"Stat: {stat}, Value: {value}, Points Awarded: {points_awarded}")
    print(f"Total score for the item: {score}")
    return score

def parse_item_stats(text):
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

def on_hotkey_pressed():
    print("Hotkey pressed. Capturing item tooltip...")
    area = (0, 0, 701, 1141)  # Example area; adjust as needed
    image = capture_item_tooltip(area)
    text = extract_text_from_image(image)
   # print(f"Extracted text from image: {text}")
    cleanText = clean_ocr_output(text)
    print(f"Cleaned text: {cleanText}")
    stats = parse_item_stats(cleanText)
    print(f"Parsed stats: {stats}")
    score = calculate_item_score(stats, attribute_points)
    print(f"Final score for the item: {score}")
    print(f"Tazer loves it when his rings are yellow")
    setRingScoreLabels(score)
    #ring_score_label.config(text=f"Ring Score: {score}")
    #ring_score_window.deiconify()
    display_ring_score_near_tooltip()
    
    mouse_monitor_thread = threading.Thread(target=monitor_mouse_movement, args=(50,))  # Use the threshold value you want
    mouse_monitor_thread.daemon = True  # This thread will close automatically when the main program exits
    mouse_monitor_thread.start()
    
def setRingScoreLabels(score):
    ring_score_label.config(text=f"{score}", font=("Exocet Heavy", 16, "bold"))
    jsp_label.config(font=("Exocet Light", 12))
    if(score < 3 ):
        jsp_label.config(text=f"Charsi", background="black", foreground="red")
    
    if(score >= 3) & (score < 4):
        jsp_label.config(text=f"Temp" , background="black", foreground="white")
   
    if(score >= 4) & (score < 4.5):
        jsp_label.config(text=f"Usable / JSP" , background="black", foreground="purple")

    if(score >= 4.5) & (score < 5):
        jsp_label.config(text=f"Great" , background="black", foreground="blue")
    
    if(score >= 5) & (score < 5.5):
        jsp_label.config(text=f"Amazing!" , background="black", foreground="yellow")
    
    if(score >= 5.5) & (score < 6):
        jsp_label.config(text=f"Godly!" , background="black", foreground="orange")
    
    if(score >= 6):
        jsp_label.config(text=f"UNREAL!!!!!" , background="black", foreground="gold", font=("Exocet Heavy", 28, "bold"))
    
    

def clean_ocr_output(ocr_text):
    corrections = {
        '@': '0',  # Assuming @ is misinterpreted as 0
        'Te': 'to',  # Assuming Te is misinterpreted as to
        'T@': 'to',  # and other similar corrections...
        'T®': 'to',
        'ST0®LEN': 'STOLEN',
        '+100% FASTER CAST RATE' : '+10% FASTER CAST RATE',
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

# The rest of your setup code, including keyboard hotkey binding...

def find_tooltip():
    # Define the region of the screen where tooltips appear (you need to set this)
    x1, y1, x2, y2 = 0, 0, 701, 1141
    # Capture the current screen area
    screen_capture = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    screen_capture_np = np.array(screen_capture)
    current_screen = cv2.cvtColor(screen_capture_np, cv2.COLOR_RGB2GRAY)
    
    print(stash_image.shape)
    print(current_screen.shape)

    # Compute the absolute difference between the current screen and the reference image
    difference = cv2.absdiff(current_screen, stash_image)
    
    # Threshold the difference
    _, thresh = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
    
    # Find the contours of the differences
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Assume the largest contour corresponds to the tooltip
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 100:  # Set a minimum area to ignore small differences
            x, y, w, h = cv2.boundingRect(largest_contour)
            return (x+x1, y+y1, w, h)  # Return the position adjusted for the original screen coordinates
    return None

# New function to display the ring score near the tooltip
def display_ring_score_near_tooltip():
    tooltip_coords = find_tooltip()
    if tooltip_coords:
        x, y, w, h = tooltip_coords
        # Adjust the offset values (10 and 10 in this example) as needed for your desired position
        offset_x = -85  # Negative value to move the score window left into the tooltip
        offset_y = 5  # Positive value to move the score window down a bit from the very top
        # Position the ring score window slightly inside the top-right corner of the tooltip
        ring_score_window.geometry(f"+{x+w+offset_x}+{y+offset_y}")
        ring_score_window.deiconify()  # Show the window
    else:
        ring_score_window.withdraw()  # Hide the window if no tooltip is detected

# Global variable to keep track of the initial mouse position
initial_mouse_position = None

def monitor_mouse_movement(threshold=100):
    global initial_mouse_position
    if initial_mouse_position is None:
        initial_mouse_position = pyautogui.position()

    while True:
        current_position = pyautogui.position()
        distance_moved = ((current_position[0] - initial_mouse_position[0]) ** 2 + 
                          (current_position[1] - initial_mouse_position[1]) ** 2) ** 0.55

        if distance_moved > threshold:
            ring_score_window.withdraw()
            initial_mouse_position = None
            break
        time.sleep(0.1)  # Check every 100ms

runewords = load_runewords_from_json()

keyboard.add_hotkey('+', on_hotkey_pressed) 

# Initialize the main window
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.geometry("30x30+1670+15")
root.attributes("-alpha", .8)
root.configure(bg=dark_background_color)

# Bind the toggle_visibility function to the Tab key event
#root.bind("<Tab>", toggle_visibility)


# Styling
style = ttk.Style()
style.theme_use("clam")  # Starting with 'clam' theme as a base for customizing
style.configure("TLabel", font=("Exocet Heavy", 10), padding=3)
style.configure("TCombobox", font=("Exocet Heavy", 10), padding=3)
style.configure("TListbox", font=("Exocet Heavy", 10), padding=3)
style.configure("TButton", background=dark_background_color, foreground=text_color,
                font=("Exocet Heavy", 10), padding=3, borderwidth=1, relief="solid")
style.map("TButton", background=[("active", highlight_color)])

top_frame = ttk.Frame(root, padding="3 3 3 3")
bottom_frame = ttk.Frame(root, padding="3 3 3 3")

runeword_track_var = tk.IntVar(value=-1)  # Initialize with -1, indicating no selection
tracking_runeword_name = tk.StringVar(value="")  # Initialize as empty

expand_button = tk.Button(root, text="^", command=toggle_gui, bg=dark_background_color, fg=text_color)
expand_button.pack(fill="both", expand=True)

terror_window = tk.Toplevel()
terror_window.attributes("-topmost", True)
terror_window.attributes("-alpha", 0.8)  # Semi-transparent
terror_window.overrideredirect(True)  # No title bar
terror_window.geometry("+1700+15")  # Position in the top-right corner

# Tracking label showing the next terror zone
next_terror_label = ttk.Label(terror_window, text="", background="black", foreground="purple", font=("Exocet Heavy", 12))
next_terror_label.pack()

ring_score_window = tk.Toplevel()
ring_score_window.attributes("-topmost", True)
ring_score_window.attributes("-alpha", 0.8)  # Semi-transparent
ring_score_window.overrideredirect(True)  # No title bar
ring_score_window.geometry("+855+65")  # Position in the top-right corner
ring_score_window.configure(background=dark_background_color)  # Shade of gray

ring_score_label = ttk.Label(ring_score_window, text="", background="black", foreground="white", font=("Exocet Heavy", 20))
ring_score_label.pack()
ring_score_label.bind("<Button-1>", hide_ring_score)  # 


jsp_label = ttk.Label(ring_score_window, text="", background="black", foreground="red", font=("Exocet Heavy", 20))
jsp_label.pack()
jsp_label.bind("<Button-1>", hide_ring_score)  # <Button-1> corresponds to the left mouse button
ring_score_window.withdraw()  # This will hide the window

# Create the quit button
quit_button = tk.Button(top_frame, text="X", command=root.destroy, bg="red", fg="white", font=("Exocet Heavy", 12, "bold"))
quit_button.pack(side='right')  # Pack the button to the right side of its frame

# Adjusting the quit_frame packing to ensure it's always at the top-right, even when the window expands
top_frame.pack(side="top", fill="x", expand=True)
bottom_frame.pack(side="top", fill="both", expand=True)

# Display area for runes
#rune_display = tk.Listbox(bottom_frame, height=50, width=100, font=("Exocet Light", 10))
#rune_display.pack(side=tk.TOP, padx=20, pady=20)

rune_display = tk.Text(bottom_frame, height=15, width=75, font=("Exocet Light", 10), bg=light_background_color, fg=text_color)
rune_display.pack(side=tk.TOP, padx=5, pady=10)
rune_display.configure(state='disabled')  # Make the Text widget read-only

# After rune_display setup
options_frame = tk.Frame(bottom_frame, bg=dark_background_color)
options_frame.pack(side=tk.TOP, fill="x", expand=False)

# Widgets like dropdowns, buttons, and listboxes go here
# Similar to your existing setup, but initially not packed

feature_options = ["Rune Tracker", "Ring Scores", "Help"]  # Placeholder for feature names
selected_feature = tk.StringVar()

# Create the dropdown menu for feature selection
feature_selection_dropdown = ttk.Combobox(root, textvariable=selected_feature, values=feature_options, state="readonly")
feature_selection_dropdown.bind("<<ComboboxSelected>>", feature_selected)

# Dropdown menu for sorting options
sort_options = ["A-Z", "Z-A", "High->Low", "Low->High", "Runeword-based"]
sort_var = tk.StringVar()
sort_dropdown = ttk.Combobox(top_frame, textvariable=sort_var, values=sort_options, style="TCombobox")
sort_dropdown.pack(side=tk.LEFT, padx=5, pady=1)

# Button to count runes
count_button = ttk.Button(top_frame, text="Count Runes", command=run_counting_in_thread, style="TButton")
count_button.pack(side=tk.LEFT, padx=5, pady=1)

# Button to sort runes
sort_button = ttk.Button(top_frame, text="Sort Runes", command=lambda: automate_sorting(sort_var.get()), style="TButton")
sort_button.pack(side=tk.LEFT, padx=5, pady=1)

# Button to display potential runewords
display_runewords_button = ttk.Button(top_frame, text="Runewords",
                                      command=update_display_with_potential_runewords, style="TButton")
display_runewords_button.pack(side=tk.LEFT, padx=5, pady=1)

#sort_move_button = ttk.Button(root, text="Sort and Move Runes", command=automate_sorting)
#sort_move_button.pack(side=tk.LEFT, padx=20, pady=10)


# Initialize the tracking window, which is hidden initially
track_window = tk.Toplevel(root)
track_window.attributes("-topmost", True)
track_window.attributes("-alpha", 0.5)  # Semi-transparent
track_window.geometry("400x50+1600+100")  # Adjust size and position as needed
track_window.overrideredirect(True)  # No title bar
track_window.withdraw()  # Start with the tracking window hidden

# Tracking label showing selected runeword progress
tracking_label = tk.Label(track_window, textvariable=tracking_runeword_name, bg="black", fg="white")
tracking_label.pack()

# Initial update of next terror zone
update_next_terror_zone()
hide_feature_interfaces()
reload_data_every_hour()

root.mainloop()