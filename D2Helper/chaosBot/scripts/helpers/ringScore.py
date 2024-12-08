import tkinter as tk
from tkinter import ttk
from utils import parse_item_stats, calculate_item_score, capture_item_tooltip, extract_text_from_image

def setup_ring_score_interface(root):
    global ring_score_interface, ring_score_label, jsp_label
    ring_score_interface = ttk.Frame(root)
    ring_score_label = ttk.Label(ring_score_interface, text="", background="black", foreground="white", font=("Exocet Heavy", 20))
    ring_score_label.pack()
    ring_score_label.bind("<Button-1>", hide_ring_score)

    jsp_label = ttk.Label(ring_score_interface, text="", background="black", foreground="red", font=("Exocet Heavy", 20))
    jsp_label.pack()
    jsp_label.bind("<Button-1>", hide_ring_score)
    ring_score_interface.pack_forget()

def show_ring_score_interface():
    ring_score_interface.pack(fill='both', expand=True)

def hide_ring_score_interface():
    ring_score_interface.pack_forget()

def hide_ring_score(event):
    ring_score_interface.pack_forget()

def on_hotkey_pressed(attribute_points):
    area = (0, 0, 701, 1141)
    image = capture_item_tooltip(area)
    text = extract_text_from_image(image)
    cleanText = parse_item_stats.clean_ocr_output(text)
    stats = parse_item_stats(cleanText)
    score = calculate_item_score(stats, attribute_points)
    setRingScoreLabels(score)

def setRingScoreLabels(score):
    ring_score_label.config(text=f"{score}", font=("Exocet Heavy", 16, "bold"))
    jsp_label.config(font=("Exocet Light", 12))
    if score < 3:
        jsp_label.config(text=f"Charsi", background="black", foreground="red")
    elif 3 <= score < 4:
        jsp_label.config(text=f"Temp", background="black", foreground="white")
    elif 4 <= score < 4.5:
        jsp_label.config(text=f"Usable / JSP", background="black", foreground="purple")
    elif 4.5 <= score < 5:
        jsp_label.config(text=f"Great", background="black", foreground="blue")
    elif 5 <= score < 5.5:
        jsp_label.config(text=f"Amazing!", background="black", foreground="yellow")
    elif 5.5 <= score < 6:
        jsp_label.config(text=f"Godly!", background="black", foreground="orange")
    elif score >= 6:
        jsp_label.config(text=f"UNREAL!!!!!", background="black", foreground="gold", font=("Exocet Heavy", 28, "bold"))
