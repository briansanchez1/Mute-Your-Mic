from MicrophoneController import MicrophoneController
import customtkinter as ctk


class App(ctk.CTk):
    """A class representing the Mute Your Mic graphical application."""

    def __init__(self):
        """Initialize the Microphone Manager application."""
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

        if self.volume_percent == 0:
            self.button.configure(state="disabled")

    def setup_gui(self):
        """Set up the GUI elements."""
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

    def button_click(self):
        """Handle clicking the mute/unmute button."""
        if self.volume_percent == 0:
            return
        self.is_muted = not self.is_muted
        self.microphone_controller.toggle_mic(self.volume_percent)
        self.button.configure(text=self.button_text())
        self.volume_percent_label.configure(
            text=f"{0 if self.is_muted else round(self.volume_percent)}%"
        )
        self.muted_label.configure(text=self.muted_text(), text_color=self.text_color())
        self.slider.set(0 if self.is_muted else self.volume_percent)

    def slider_event(self, value):
        """Handle the slider bar moving."""
        self.volume_percent = value
        self.microphone_controller.set_volume(self.volume_percent)
        self.volume_percent_label.configure(text=f"{round(self.volume_percent)}%")

        if self.volume_percent == 0:
            self.is_muted = True
            self.button.configure(state="disabled")
        else:
            self.is_muted = False
            self.button.configure(state="normal")

        self.button.configure(text=self.button_text())
        self.muted_label.configure(text=self.muted_text(), text_color=self.text_color())

    def muted_text(self):
        """Return text indicating if the microphone is muted."""
        return "You are muted" if self.is_muted else "You are not muted"

    def text_color(self):
        """Return text color based on microphone mute status."""
        return "red" if self.is_muted else "green"

    def button_text(self):
        """Return text for the mute/unmute button based on microphone status."""
        return "Click to mute" if not self.is_muted else "Click to unmute"


# Starts the app
app = App()
app.mainloop()
