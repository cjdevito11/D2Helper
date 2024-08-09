import tkinter as tk
from tkinter import ttk
import json
import os
from items import categorized_items  # Importing the categorized items from items.py

class ItemTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.geometry("25x25+0+0")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.3)
        self.minimized = True

        self.categories = categorized_items

        self.current_category = "Normal"
        self.checkbox_vars = {}
        self.load_progress()
        
        self.create_widgets()

    def create_widgets(self):
        self.menu_button = tk.Button(self.root, text="^", command=self.toggle_menu)
        self.menu_button.pack(fill="both", expand=True)

        self.close_button = tk.Button(self.root, text="X", command=self.close_app)
        self.close_button.pack_forget()  # Hide the close button initially

        self.menu_frame = tk.Frame(self.root)
        
        self.category_var = tk.StringVar(value=self.current_category)
        
        self.menu_bar = tk.Menu(self.root)
        
        self.category_menu = tk.Menu(self.menu_bar, tearoff=0)
        for category in self.categories.keys():
            self.category_menu.add_radiobutton(label=category, variable=self.category_var, command=self.change_category)
        self.menu_bar.add_cascade(label="Categories", menu=self.category_menu)
        
        self.scrollbar = tk.Scrollbar(self.menu_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas = tk.Canvas(self.menu_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill='both', expand=True)
        
        self.scrollbar.config(command=self.canvas.yview)
        
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')
        
        self.update_items()
        
        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset_progress)
        self.reset_button.pack(pady=10)
        
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def toggle_menu(self):
        if self.minimized:
            self.root.geometry("300x400+0+0")
            self.root.attributes('-alpha', 1)
            self.root.config(menu=self.menu_bar)
            self.menu_frame.pack(fill='both', expand=True)
            self.minimized = False
            self.menu_button.config(text="Minimize")
            self.close_button.pack()  # Show the close button when expanded
        else:
            self.root.geometry("25x25+0+0")
            self.root.attributes('-alpha', 0.3)
            self.root.config(menu="")
            self.menu_frame.pack_forget()
            self.minimized = True
            self.menu_button.config(text="^")
            self.close_button.pack_forget()  # Hide the close button when minimized

    def change_category(self):
        self.current_category = self.category_var.get()
        self.update_items()

    def update_items(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        if self.current_category == "Misc" and "Class Specific" in self.categories[self.current_category]:
            for sub_subcategory, items in self.categories[self.current_category]["Class Specific"].items():
                sub_subcategory_label = ttk.Label(self.frame, text=f"Class Specific > {sub_subcategory}", font=('Helvetica', 12, 'bold'))
                sub_subcategory_label.pack(anchor='w', pady=(10, 0))

                for item in items:
                    var = self.checkbox_vars.get(item, tk.BooleanVar())
                    chk = ttk.Checkbutton(self.frame, text=item, variable=var, command=self.update_json)
                    chk.pack(anchor='w')
                    self.checkbox_vars[item] = var

        if self.current_category == "Runes":
            for item in self.categories[self.current_category]:
                var = self.checkbox_vars.get(item, tk.BooleanVar())
                chk = ttk.Checkbutton(self.frame, text=item, variable=var, command=self.update_json)
                chk.pack(anchor='w')
                self.checkbox_vars[item] = var

        elif self.current_category != "Runes":
            for subcategory, items in self.categories[self.current_category].items():
                subcategory_label = ttk.Label(self.frame, text=subcategory, font=('Helvetica', 12, 'bold'))
                subcategory_label.pack(anchor='w', pady=(10, 0))

                for item in items:
                    var = self.checkbox_vars.get(item, tk.BooleanVar())
                    chk = ttk.Checkbutton(self.frame, text=item, variable=var, command=self.update_json)
                    chk.pack(anchor='w')
                    self.checkbox_vars[item] = var

    def update_json(self):
        progress = {item: var.get() for item, var in self.checkbox_vars.items()}
        with open("progress.json", "w") as f:
            json.dump(progress, f)
        
    def load_progress(self):
        if os.path.exists("progress.json"):
            with open("progress.json", "r") as f:
                saved_data = json.load(f)
                self.checkbox_vars = {item: tk.BooleanVar(value=value) for item, value in saved_data.items()}
        else:
            self.checkbox_vars = {item: tk.BooleanVar(value=False) for category in self.categories.values() for subcategory in category for item in subcategory}
    
    def reset_progress(self):
        for var in self.checkbox_vars.values():
            var.set(False)
        self.update_json()

    def close_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ItemTrackerApp(root)
    root.mainloop()
