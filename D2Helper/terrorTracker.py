import tkinter as ttk  # This import seems incorrect. It should be:
from tkinter import ttk
import requests
from utils import schedule_periodic_update
from zones import zone_mapping  # Importing zone_mapping

# Global variables
terrorApi = "https://d2emu.com/api/v1/tz"
terror_tracker_interface = None

def setup_terror_tracker(root):
    global terror_tracker_interface
    terror_tracker_interface = ttk.Frame(root)
    terror_tracker_interface.pack(fill='both', expand=True)
    
    # Tracking label showing the next terror zone
    next_terror_label = ttk.Label(terror_tracker_interface, text="Next Terror Zone: Unknown", background="black", foreground="purple", font=("Exocet Heavy", 12))
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
        next_terror_zone_number = int(data["next"][0])  # Convert zone number to integer
        next_terror_zone_name = zone_mapping.get(next_terror_zone_number, "Unknown Zone")
        label.config(text=f"Next Terror Zone: {next_terror_zone_name}")
    else:
        label.config(text="Next Terror Zone not found in data")

def update_next_terror_zone(label):
    terror_data = fetch_terror_data()
    if terror_data:
        display_next_terror_zone(terror_data, label)

def show_terror_tracker():
    if terror_tracker_interface:
        terror_tracker_interface.pack(fill='both', expand=True)

def hide_terror_tracker():
    if terror_tracker_interface:
        terror_tracker_interface.pack_forget()
