import tkinter as tk
from tkinter import messagebox


class UIManager:
    def __init__(self):
        self.window = None

    def create_window(self, window_name, dimensions):
        self.window = tk.Tk()
        self.window.title(window_name)
        self.window.geometry(dimensions)
        return self.window

    def create_btn(window, text, color, command, fg='white'):
        button = tk.Button(
            window,
            text=text,
            activebackground="black",
            activeforeground="white",
            fg=fg,
            bg=color,
            command=command,  # You should provide a function or method here
            height=2,
            width=20,
            font=('Helvetica bold', 10)
        )
        return button

    def create_label(self, window):
        label = tk.Label(window)
        label.grid(row=0, column=0)
        return label

    def get_text_label(self, window, text):
        label = tk.Label(window, text=text)
        label.config(font=("sans-serif", 21), justify="left")
        return label

    def get_entry_text(self, window):
        inputtxt = tk.Text(window, height=2, width=15, font=("Arial", 10))
        return inputtxt

    def msg_box(self, title, description):
        messagebox.showinfo(title, description)


# Testing
def test():
    ui_manager = UIManager()
    window = ui_manager.create_window("My Window", "200x200")
    ui_manager.msg_box(window, 'Hi')


test()
