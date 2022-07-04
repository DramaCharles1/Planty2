from typing import List
from SettingsHandler import SettingsHandler

class PlantySetings(SettingsHandler):
    '''
    Planty specific settings from xml
    '''
    def __init__(self, path, file) -> None:
        super().__init__(path, file)

        planty_settings = self.mydoc.getElementsByTagName('planty_settings')

        self._duration = planty_settings[0].getElementsByTagName("motor_duration")[0].firstChild.data.strip()
        self._power = planty_settings[0].getElementsByTagName("motor_power")[0].firstChild.data.strip()
        self._samples = planty_settings[0].getElementsByTagName("moisture_samples")[0].firstChild.data.strip()
        self._moisture_threshold = planty_settings[0].getElementsByTagName("moisture_threshold")[0].firstChild.data.strip()
        self._kp = planty_settings[0].getElementsByTagName("kp")[0].firstChild.data.strip()
        self._ki = planty_settings[0].getElementsByTagName("ki")[0].firstChild.data.strip()
        self._integration_time = planty_settings[0].getElementsByTagName("integration_time")[0].firstChild.data.strip()
        self._light_setpoint = planty_settings[0].getElementsByTagName("light_setpoint")[0].firstChild.data.strip()
        self._light_max_control = planty_settings[0].getElementsByTagName("max_light")[0].firstChild.data.strip()
        self.settings = {"motor_duration" : self.motor_duration,
                        "motor_power" : self.motor_power,
                        "moisture_samples" : self.moisture_samples,
                        "moisture_threshold" : self.moisture_threshold,
                        "kp" : self.kp,
                        "ki" : self.ki,
                        "integration_time" : self.integration_time,
                        "light_setpoint" : self.light_setpoint,
                        "max_light" : self.max_light}

    @property
    def motor_duration(self) -> int:
        return int(self._duration)
    @property
    def motor_power(self) -> int:
        return int(self._power)
    @property
    def moisture_samples(self) -> int:
        return int(self._samples)
    @property
    def moisture_threshold(self) -> float:
        return float(self._moisture_threshold)
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

class CameraSettings(SettingsHandler):
    '''
    Camera specifc settings
    '''
    def __init__(self, path, file) -> None:
        super().__init__(path, file)

        camera_settings = self.mydoc.getElementsByTagName('camera_settings')

        self._picture_directory = camera_settings[0].getElementsByTagName("picture_directory")[0].firstChild.data.strip()
        self._picture_copy_directory = camera_settings[0].getElementsByTagName("picture_copy_directory")[0].firstChild.data.strip()
        self._lower_green_filter = [int(camera_settings[0].getElementsByTagName("lower_green_filter")[0].getAttribute("l1")),
                                    int(camera_settings[0].getElementsByTagName("lower_green_filter")[0].getAttribute("l2")),
                                    int(camera_settings[0].getElementsByTagName("lower_green_filter")[0].getAttribute("l3"))]
        self._upper_green_filter = [int(camera_settings[0].getElementsByTagName("upper_green_filter")[0].getAttribute("u1")),
                                    int(camera_settings[0].getElementsByTagName("upper_green_filter")[0].getAttribute("u2")),
                                    int(camera_settings[0].getElementsByTagName("upper_green_filter")[0].getAttribute("u3"))]
        self.settings = {"picture_directory" : self.picture_directory,
        "picture_copy_directory" : self.picture_copy_directory,
        "l1" : self.lower_green_filter[0],
        "l2" : self.lower_green_filter[1],
        "l3" : self.lower_green_filter[2],
        "u1" : self.lower_green_filter[0],
        "u2" : self.lower_green_filter[1],
        "u3" : self.lower_green_filter[2]}

    @property
    def picture_directory(self) -> str:
        return self._picture_directory
    @property
    def picture_copy_directory(self) -> str:
        return self._picture_copy_directory
    @property
    def lower_green_filter(self) -> List[int]:
        return self._lower_green_filter
    @property
    def upper_green_filter(self) -> List[int]:
        return self._upper_green_filter
