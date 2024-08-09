import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import pyautogui
import json
import threading
import time
import keyboard

class ClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        
        # Always stay on top
        self.root.attributes("-topmost", True)
        
        self.coords = []
        self.running = False
        self.paused = False

        # GUI elements
        self.coord_label = tk.Label(root, text="Current Selected Coordinates:")
        self.coord_label.pack()

        self.coord_listbox = tk.Listbox(root, height=10, width=50)
        self.coord_listbox.pack()

        self.iterations_label = tk.Label(root, text="Number of Iterations (0 = infinite):")
        self.iterations_label.pack()
        
        self.iterations_entry = tk.Entry(root)
        self.iterations_entry.pack()

        self.select_button = tk.Button(root, text="Select Coordinates", command=self.select_coords)
        self.select_button.pack()

        self.save_button = tk.Button(root, text="Save Coordinates", command=self.save_coords)
        self.save_button.pack()

        self.load_button = tk.Button(root, text="Load Coordinates", command=self.load_coords)
        self.load_button.pack()

        self.run_button = tk.Button(root, text="Run Script", command=self.run_script)
        self.run_button.pack()

        self.stop_button = tk.Button(root, text="Stop Script", command=self.stop_script)
        self.stop_button.pack()

        self.pause_button = tk.Button(root, text="Pause Script", command=self.pause_script)
        self.pause_button.pack()

        self.resume_button = tk.Button(root, text="Resume Script", command=self.resume_script)
        self.resume_button.pack()

        # Add labels for hotkeys
        self.hotkey_label_stop = tk.Label(root, text="Hotkey to Stop: Ctrl+Shift+Q")
        self.hotkey_label_stop.pack()

        self.hotkey_label_pause = tk.Label(root, text="Hotkey to Pause: Ctrl+Shift+P")
        self.hotkey_label_pause.pack()

        self.hotkey_label_resume = tk.Label(root, text="Hotkey to Resume: Ctrl+Shift+R")
        self.hotkey_label_resume.pack()

        self.json_label = tk.Label(root, text="Saved Coordinates from JSON:")
        self.json_label.pack()

        self.json_listbox = scrolledtext.ScrolledText(root, height=10, width=50)
        self.json_listbox.pack()

        # Bind hotkeys
        keyboard.add_hotkey('ctrl+shift+q', self.stop_script)
        keyboard.add_hotkey('ctrl+shift+p', self.pause_script)
        keyboard.add_hotkey('ctrl+shift+r', self.resume_script)

    def select_coords(self):
        self.coords = []
        self.coord_listbox.delete(0, tk.END)
        
        for i in range(1, 7):
            messagebox.showinfo("Info", f"Move your mouse to the desired position for click {i} and press Enter.")
            x, y = pyautogui.position()
            nickname = f"Click {i}"
            self.coords.append({"x": x, "y": y, "nickname": nickname})
            self.update_coords_listbox()

    def save_coords(self):
        if not self.coords:
            messagebox.showerror("Error", "No coordinates to save.")
            return

        with open('coords.json', 'w') as f:
            json.dump(self.coords, f)
        messagebox.showinfo("Info", "Coordinates saved successfully.")
        self.update_json_listbox()

    def load_coords(self):
        try:
            with open('coords.json', 'r') as f:
                self.coords = json.load(f)
            self.update_coords_listbox()
            messagebox.showinfo("Info", "Coordinates loaded successfully.")
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "No valid coordinates file found.")

    def run_script(self):
        iterations = self.iterations_entry.get()
        try:
            iterations = int(iterations)
        except ValueError:
            messagebox.showerror("Error", "Invalid number of iterations.")
            return

        if len(self.coords) < 4:
            messagebox.showerror("Error", "You need to select four coordinates.")
            return

        self.running = True
        self.paused = False
        thread = threading.Thread(target=self.click_loop, args=(iterations,))
        thread.start()

    def stop_script(self):
        self.running = False

    def pause_script(self):
        self.paused = True

    def resume_script(self):
        self.paused = False

    def click_loop(self, iterations):
        count = 0
        while self.running and (iterations == 0 or count < iterations):
            if not self.paused:
                for i, coord in enumerate(self.coords):
                    if not self.running:
                        break
                   # if i == 3:  # Right click for the fourth coordinate
                    #    pyautogui.click(coord['x'], coord['y'], button='right')
                   #     pyautogui.click(coord['x'], coord['y'], button='right')
                    else:  # Left click for the first three coordinates
                        pyautogui.click(coord['x'], coord['y'], button='left')
                    time.sleep(0.15)
                count += 1

    def update_coords_listbox(self):
        self.coord_listbox.delete(0, tk.END)
        for coord in self.coords:
            self.coord_listbox.insert(tk.END, f"{coord['nickname']} ({coord['x']}, {coord['y']})")

    def update_json_listbox(self):
        self.json_listbox.delete(1.0, tk.END)
        try:
            with open('coords.json', 'r') as f:
                coords = json.load(f)
            for coord in coords:
                self.json_listbox.insert(tk.END, f"{coord['nickname']} ({coord['x']}, {coord['y']})\n")
        except (FileNotFoundError, json.JSONDecodeError):
            self.json_listbox.insert(tk.END, "No valid coordinates file found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickerApp(root)
    root.mainloop()
