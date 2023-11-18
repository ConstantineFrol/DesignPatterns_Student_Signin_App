import time
import tkinter as tk


# Concrete state: Main Frame
class MainFrame:
    def show_frame(self):
        print("Displaying Main Frame")


# Concrete state: Registration Frame
class RegistrationFrame:
    def show_frame(self):
        print("Displaying Registration Frame")


# Context class
class AppContext(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Frame Switching App")
        self.geometry("800x600")

        self.main_frame = MainFrame()
        self.registration_frame = RegistrationFrame()

        self.current_frame = self.main_frame
        self.current_frame.show_frame()

        switch_button = tk.Button(self, text="Switch Frame", command=self.switch_frame)
        switch_button.pack()

    def switch_frame(self, frame_name=None):
        if frame_name == "main" or not frame_name:
            self.current_frame = self.main_frame
        elif frame_name == "registration":
            self.current_frame = self.registration_frame
        else:
            print(f"Unknown frame name: {frame_name}")
            return

        # Hide current frame and show the new one
        self.current_frame.show_frame()


if __name__ == "__main__":
    app = AppContext()

    # Switch to the Registration Frame
    print("Switching to Registration Frame...")
    app.switch_frame("registration")
    print("Waiting 10 seconds...")
    time.sleep(10)
    print("Switching to Main Frame...")
    app.switch_frame("main")

    app.mainloop()
