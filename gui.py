from MicrophoneController import MicrophoneController
import customtkinter as ctk


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        #   Window setup
        self.geometry("300x200")
        self.title("Microphone Manager")
        self.resizable(False, False)

        # Microphone Setup
        self.microphone_controller = MicrophoneController()
        self.is_muted = self.microphone_controller.is_muted()
        self.volume_percent = round(self.microphone_controller.get_volume())

        self.setup_gui()

    # handles setting up the gui
    def setup_gui(self):

        # Grid setup
        self.grid_columnconfigure(0, weight=1)

        # Muted/unmuted label setup
        self.muted_label = ctk.CTkLabel(
            self, text=self.muted_text(), text_color=self.text_color(), font=(None, 30)
        )
        self.muted_label.grid(row=0, padx=20, pady=10)

        # Button setup
        self.button = ctk.CTkButton(
            self, text=self.button_text(), command=self.button_click
        )
        self.button.grid(row=1, padx=20, pady=10)

        # Volume percent label setup
        self.volume_percent_label = ctk.CTkLabel(self, text=f"{self.volume_percent}%")
        self.volume_percent_label.grid(row=2, padx=20, pady=10)

        # Slider setup
        self.slider = ctk.CTkSlider(self, from_=0, to=100, command=self.slider_event)
        self.slider.set(0 if self.is_muted else self.volume_percent)
        self.slider.configure(number_of_steps=100)
        self.slider.grid(row=3, padx=20)

    # handles clicking the mute/unmute button
    def button_click(self):
        if self.volume_percent == 0:
            return
        self.is_muted = not self.is_muted
        self.button.configure(text=self.button_text())
        self.microphone_controller.toggle_mic(self.volume_percent)
        self.slider.set(0 if self.is_muted else self.volume_percent)
        self.volume_percent_label.configure(
            text=f"{0 if self.is_muted else self.volume_percent}%"
        )
        self.muted_label.configure(text=self.muted_text(), text_color=self.text_color())

    # handles the slider bar moving
    def slider_event(self, value):
        self.volume_percent = value
        self.microphone_controller.set_volume(self.volume_percent)
        self.volume_percent_label.configure(text=f"{round(self.volume_percent)}%")

        if self.volume_percent == 0:
            self.is_muted = True
        else:
            self.is_muted = False

        self.button.configure(text=self.button_text())
        self.muted_label.configure(text=self.muted_text(), text_color=self.text_color())

    # Text that shows up on the mute/unmute text depending on whether the mic is muted or not
    def muted_text(self):
        return "You are muted" if self.is_muted else "You are not muted"

    # Color that changes depending on whether the mic is muted or not
    def text_color(self):
        return "red" if self.is_muted else "green"

    # Text that shows up on the mute/unmute button depending on whether the mic is muted or not
    def button_text(self):
        return "Click to mute" if not self.is_muted else "Click to unmute"


# Starts the app
app = App()
app.mainloop()
