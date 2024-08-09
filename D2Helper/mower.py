import pyautogui
import time
from tkinter import Tk, Button, Label, Entry, messagebox
from threading import Thread, Event
import keyboard

class Walker:
    def __init__(self, stop_event, num_iterations):
        self.stop_event = stop_event
        self.coordinates = []
        self.num_iterations = num_iterations


    def walk_loop(self):
        iterations = 0
        while not self.stop_event.is_set() and (self.num_iterations == 0 or iterations < self.num_iterations):
            for coord in self.coordinates:
                if self.stop_event.is_set():
                    break
                pyautogui.moveTo(coord)
                pyautogui.click()
                time.sleep(2.5)  # Adjust the delay as needed
            self.handle_inventory()
            iterations += 1

    def handle_inventory(self):
        inventory_key = 'i'
        gold_icon_coords = (1450, 875)  # Replace with actual coordinates
        textbox_coords = (850, 550)  # Replace with actual coordinates
        ok_button_coords = (800, 640)  # Replace with actual coordinates

        pyautogui.press(inventory_key)  # Open inventory
        time.sleep(1)
        pyautogui.moveTo(gold_icon_coords)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(textbox_coords)
        pyautogui.click()
        pyautogui.typewrite('9999999999999')
        pyautogui.moveTo(ok_button_coords)
        pyautogui.click()
        pyautogui.press(inventory_key)  # Close inventory
        time.sleep(1)

class WalkerInterface:
    def __init__(self, walker):
        self.walker = walker
        self.root = Tk()
        self.root.title("Walker Control")
        self.root.attributes('-topmost', True)
        
        self.status_label = Label(self.root, text="Status: Stopped")
        self.status_label.pack()

        self.iterations_label = Label(self.root, text="Number of Iterations (0 = Infinite):")
        self.iterations_label.pack()

        self.iterations_entry = Entry(self.root)
        self.iterations_entry.pack()

        self.start_button = Button(self.root, text="Start Walking", command=self.start_walking)
        self.start_button.pack()

        self.stop_button = Button(self.root, text="Stop Walking", command=self.stop_walking)
        self.stop_button.pack()

        self.record_button = Button(self.root, text="Record Coordinates", command=self.record_coordinates)
        self.record_button.pack()

        self.stop_event = walker.stop_event
        keyboard.add_hotkey('shift+*', self.stop_walking)
        self.recording = False

    def start_walking(self):
        num_iterations = int(self.iterations_entry.get() or 0)
        self.walker.num_iterations = num_iterations
        self.status_label.config(text="Status: Walking")
        self.stop_event.clear()
        self.walker_thread = Thread(target=self.walker.walk_loop)
        self.walker_thread.start()

    def stop_walking(self):
        self.status_label.config(text="Status: Stopped")
        self.stop_event.set()
        if self.walker_thread.is_alive():
            self.walker_thread.join()

    def record_coordinates(self):
        self.recording = True
        self.status_label.config(text="Recording: Hover over points and press 'r' to record, 'd' when done")
        self.walker.coordinates = []
        keyboard.add_hotkey('r', self.record_coord)
        keyboard.add_hotkey('d', self.done_recording)

    def record_coord(self):
        if self.recording:
            x, y = pyautogui.position()
            self.walker.coordinates.append((x, y))
            messagebox.showinfo("Recorded", f"Recorded coordinates: ({x}, {y})")

    def done_recording(self):
        if self.recording:
            self.recording = False
            keyboard.remove_hotkey('r')
            keyboard.remove_hotkey('d')
            self.status_label.config(text="Recording Done")

    def run(self):
        self.root.mainloop()

def main():
    stop_event = Event()
    walker = Walker(stop_event, 0)  # Default 0 iterations for infinite loop
    walker_interface = WalkerInterface(walker)
    walker_interface.run()

if __name__ == "__main__":
    main()
