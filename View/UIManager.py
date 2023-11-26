import tkinter as tk
from tkinter import messagebox


class UIManager:
    def __init__(self):
        """Initialize the UIManager."""
        self.window = None

    def create_window(self, window_name, dimensions):
        """Create and return a new window."""
        self.window = tk.Tk()
        self.window.title(window_name)
        self.window.geometry(dimensions)
        return self.window

    def create_btn(self, frame, text, color, command, fg='white'):
        """Create and return a button."""
        button = tk.Button(
            frame,
            text=text,
            activebackground="black",
            activeforeground="white",
            fg=fg,
            bg=color,
            command=command,
            height=2,
            width=20,
            font=('Helvetica bold', 10)
        )
        return button

    def create_label(self, window):
        """Create and return a label."""
        label = tk.Label(window)
        label.grid(row=0, column=0)
        return label

    def get_text_label(self, window, text, size=21):
        """Create and return a text label."""
        label = tk.Label(window, text=text)
        label.config(font=("sans-serif", size), justify="left")
        return label

    def get_entry_text(self, window):
        """Create and return a text entry field."""
        inputtxt = tk.Text(window, height=2, width=15, font=("Arial", 10))
        return inputtxt

    def msg_box(self, title, description):
        """Display a message box."""
        messagebox.showinfo(title, description)


# Testing
def test():
    ui_manager = UIManager()
    window = ui_manager.create_window("My Window", "200x200")
    ui_manager.msg_box("Title", "Description")

# test()
