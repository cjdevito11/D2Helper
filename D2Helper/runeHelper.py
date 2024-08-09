import tkinter as tk
from tkinter import ttk
import threading
import os
import json
from utils import count_images_on_screen, get_rune_sort_key, get_rune_positions, sort_runes

def setup_rune_interface(root):
    global rune_interface, rune_display
    rune_interface = ttk.Frame(root)
    rune_display = tk.Text(rune_interface, height=15, width=75, font=("Exocet Light", 10), bg="#EAE3AA", fg="#B9761D")
    rune_display.pack(side=tk.TOP, padx=5, pady=10)
    rune_display.configure(state='disabled')

def show_rune_interface():
    rune_interface.pack(fill='both', expand=True)

def hide_rune_interface():
    rune_interface.pack_forget()

def update_display_with_runes(counted_runes):
    rune_display.configure(state='normal')
    rune_display.delete('1.0', tk.END)
    if counted_runes:
        for rune, count in counted_runes.items():
            rune_display.insert(tk.END, f"{rune}: {count}\n")
    else:
        rune_display.insert(tk.END, "No runes to display.\n")
    rune_display.configure(state='disabled')

def count_runes_in_directory(directory_path, distance_threshold=10):
    total_runes_count = {}
    for filename in os.listdir(directory_path):
        if filename.lower().endswith((".png", ".jpg")):
            image_path = os.path.join(directory_path, filename)
            rune_positions = count_images_on_screen(image_path, distance_threshold)
            rune_name = os.path.splitext(filename)[0]
            total_runes_count[rune_name] = len(rune_positions)
    return total_runes_count

def count_runes():
    global counted_runes
    result = count_runes_in_directory(imagePath)
    if result is not None and isinstance(result, dict):
        counted_runes = result
        update_display_with_runes()
    else:
        print("No runes counted or an error occurred.")

def run_counting_in_thread():
    count_thread = threading.Thread(target=count_runes)
    count_thread.start()

def load_runewords_from_json(runewordsPath):
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
            'required_runes': required_runes,
            'missing_runes': missing_runes
        })
    runeword_details.sort(key=lambda x: x['completion'], reverse=True)
    return runeword_details

def update_display_with_potential_runewords(runewords, counted_runes):
    rune_display.configure(state='normal')
    rune_display.delete('1.0', tk.END)
    runeword_details = check_runeword_availability_and_detail(runewords, counted_runes)
    if runeword_details:
        for index, detail in enumerate(runeword_details):
            if detail['completion'] > 0:
                rune_display.tag_configure('gold', foreground='#d5a021')
                rune_display.tag_configure('green', foreground='green')
                rune_display.tag_configure('red', foreground='red')
                rune_display.insert(tk.END, f"{detail['name']}: ", 'gold')
                rune_display.insert(tk.END, "Runes: ", 'gold')
                normalized_counted_runes = {normalize_rune_name(key): value for key, value in counted_runes.items()}
                for rune in detail['required_runes']:
                    rune_name = normalize_rune_name(rune)
                    if rune_name in normalized_counted_runes and normalized_counted_runes[rune_name] > 0:
                        rune_display.insert(tk.END, f"{rune} ", 'green')
                        normalized_counted_runes[rune_name] -= 1
                    else:
                        rune_display.insert(tk.END, f"{rune} ", 'red')
                rune_display.insert(tk.END, "\n")
                tk.Radiobutton(options_frame, text=detail['name'], variable=runeword_track_var, value=index, 
                               command=lambda idx=index: update_runeword_tracking(idx), bg=dark_background_color, fg=text_color).pack(side=tk.LEFT, padx=5)
    else:
        rune_display.insert(tk.END, "No potential runewords with current runes.")
    rune_display.configure(state='disabled')
