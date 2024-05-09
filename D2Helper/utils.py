import tkinter as tk
from tkinter import ttk

def schedule_periodic_update(root, callback, interval):
    """ Schedule periodic updates for a given callback function.

    Args:
        root (tk.Tk): The main application root.
        callback (function): The callback function to run periodically.
        interval (int): The time interval in milliseconds.
    """
    callback()  # Call the callback function immediately
    root.after(interval, lambda: schedule_periodic_update(root, callback, interval))

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