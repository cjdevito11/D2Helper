import tkinter as tk
from tkinter import ttk
import requests
from utils import schedule_periodic_update
from zones import zone_mapping  # Make sure this is correctly imported

# Global variables
terrorApi = "https://d2emu.com/api/v1/tz"
terror_tracker_window = None

def setup_terror_tracker(root):
    global terror_tracker_window
    terror_tracker_window = tk.Toplevel(root)
    terror_tracker_window.attributes("-topmost", True)
    terror_tracker_window.attributes("-alpha", 0.8)  # Semi-transparent
    terror_tracker_window.overrideredirect(True)  # No title bar
    terror_tracker_window.geometry("+1385+5")  # Position in the top-right corner

    # Tracking label showing the next terror zone
    next_terror_label = ttk.Label(terror_tracker_window, text="Unknown", background="black", foreground="purple", font=("Exocet Heavy", 12))
    next_terror_label.pack()

    # Schedule the periodic update of the terror zone
    schedule_periodic_update(root, lambda: update_next_terror_zone(next_terror_label), 3600000)

def fetch_terror_data():
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

def display_next_terror_zone(data, label):
    if "next" in data and len(data["next"]) > 0:
        next_terror_zone_number = int(data["next"][0])
        next_terror_zone_name = zone_mapping.get(next_terror_zone_number, "Unknown Zone")
        label.config(text=f"{next_terror_zone_name}")
    else:
        label.config(text="Unknown")

def update_next_terror_zone(label):
    terror_data = fetch_terror_data()
    if terror_data:
        display_next_terror_zone(terror_data, label)

def show_terror_tracker():
    if terror_tracker_window:
        terror_tracker_window.deiconify()

def hide_terror_tracker():
    if terror_tracker_window:
        terror_tracker_window.withdraw()
