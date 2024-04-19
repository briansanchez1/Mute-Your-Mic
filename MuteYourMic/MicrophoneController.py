from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class MicrophoneController:
    """A class used to represent the microphone controller."""

    def __init__(self):
        """Initializes the MicrophoneController class.

        Finds and connects the default microphone to the program.
        """
        self.devices = AudioUtilities.GetMicrophone()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)

    def is_muted(self) -> bool:
        """Checks if the microphone is muted.

        Returns:
            bool: True if the microphone is muted, False otherwise.
        """
        return self.volume.GetMasterVolumeLevelScalar() == 0.0

    def toggle_mic(self, original_volume):
        """Toggles the microphone on and off.

        Args:
            original_volume (int): The original volume before toggling.

        """
        if self.is_muted():
            self.set_volume(original_volume)
        else:
            self.set_volume(0)

    def get_volume(self) -> int:
        """Gets the current volume of the microphone.

        Returns:
            int: Volume of the microphone as an integer between 0 and 100.
        """
        return round(self.volume.GetMasterVolumeLevelScalar() * 100)

    def set_volume(self, new_volume):
        """Sets the volume of the microphone.

        Args:
            new_volume (int): The new volume level to set (0-100).

        """
        self.volume.SetMasterVolumeLevelScalar(round(new_volume / 100, 2), None)
