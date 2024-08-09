from tkinter import Tk, Text

class Terminal:
    def __init__(self):
        self.overlay = Tk()
        self.overlay.title("Overlay Terminal")
        self.overlay.geometry("800x400+50+740")  # Adjust position and size as needed
        self.overlay.attributes('-topmost', True)
        self.overlay.attributes('-alpha', 0.8)  # Set opacity (0.0 to 1.0)
        self.overlay.overrideredirect(True)  # Remove window borders and title bar

        self.terminal_output = Text(self.overlay, bg='black', fg='white', font=('Consolas', 12), wrap='word')
        self.terminal_output.pack(expand=True, fill='both')

    def write_to_terminal(self, message):
        self.terminal_output.insert('end', message + '\n')
        self.terminal_output.see('end')
