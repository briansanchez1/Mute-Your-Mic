from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class MicrophoneController:
    def __init__(self):
        # Finds and connects the microphone interface
        self.devices = AudioUtilities.GetMicrophone()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)

    # Checks whether the microphone is muted or not
    def is_muted(self):
        return self.volume.GetMasterVolumeLevelScalar() == 0.0

    # Toggles the microphone on and off
    def toggle_mic(self, original_volume):
        if self.is_muted():
            self.set_volume(original_volume)
        else:
            self.set_volume(0)

    # Gets the microphone volume
    def get_volume(self):
        return round(self.volume.GetMasterVolumeLevelScalar() * 100, 2)

    # Sets the microphone volume
    def set_volume(self, new_volume):
        self.volume.SetMasterVolumeLevelScalar(round(new_volume / 100, 2), None)
