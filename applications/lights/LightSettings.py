from typing import List
from SettingsHandler import SettingsHandler

class LightSetings(SettingsHandler):
    def __init__(self, path, file) -> None:
        super().__init__(path, file)

        light_settings = self.mydoc.getElementsByTagName('light_settings')
        self._kp = light_settings[0].getElementsByTagName("kp")[0].firstChild.data.strip()
        self._ki = light_settings[0].getElementsByTagName("ki")[0].firstChild.data.strip()
        self._integration_time = light_settings[0].getElementsByTagName("integration_time")[0].firstChild.data.strip()
        self._light_setpoint = light_settings[0].getElementsByTagName("light_setpoint")[0].firstChild.data.strip()
        self._light_max_control = light_settings[0].getElementsByTagName("max_light")[0].firstChild.data.strip()
        self.settings = {
                        "kp" : self.kp,
                        "ki" : self.ki,
                        "integration_time" : self.integration_time,
                        "light_setpoint" : self.light_setpoint,
                        "max_light" : self.max_light}

    @property
    def kp(self) -> float:
        return float(self._kp)
    @property
    def ki(self) -> float:
        return float(self._ki)
    @property
    def integration_time(self) -> int:
        return int(self._integration_time)
    @property
    def light_setpoint(self) -> int:
        return int(self._light_setpoint)
    @property
    def max_light(self) -> int:
        return int(self._light_max_control)
