from tkinter import Tk, Label, StringVar, Button

class InventoryOverlay:
    def __init__(self, inventory, stop_event):
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry("400x400+600+0")  # Adjust position and size as needed
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
