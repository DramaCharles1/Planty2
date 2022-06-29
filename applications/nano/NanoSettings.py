from SettingsHandler import SettingsHandler

class NanoSettings(SettingsHandler):
    def __init__(self, path, file) -> None:
        super().__init__(path, file)

        nano_settings = self.mydoc.getElementsByTagName('nano_settings')
        self._moisture_threshold = nano_settings[0].getElementsByTagName("moisture_threshold")[0].firstChild.data.strip()
        self._samples = nano_settings[0].getElementsByTagName("moisture_samples")[0].firstChild.data.strip()
        self.settings = {"moisture_samples" : self.moisture_samples,
                       "moisture_threshold" : self.moisture_threshold,
                        }

    @property
    def moisture_samples(self) -> int:
        return int(self._samples)
    @property
    def moisture_threshold(self) -> float:
        return float(self._moisture_threshold)
