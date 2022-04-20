import os
from xml.dom import minidom

class SettingsHandler:
    '''
    Class to handle settings read from settings.xml
    '''
    def __init__(self, path, file) -> None:
        self.path = path
        self.file = file

        settings_file = os.path.join(self.path, self.file)
        if not os.path.exists(settings_file):
            raise FileNotFoundError(f"{settings_file} was not found")

        self.mydoc = minidom.parse(settings_file)

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
        self._light_setpoint = planty_settings[0].getElementsByTagName("light_setpoint")[0].firstChild.data.strip()
        self._light_max_control = planty_settings[0].getElementsByTagName("max_light")[0].firstChild.data.strip()
        self.settings = {"motor_duration" : self.motor_duration,
                        "motor_power" : self.motor_power,
                        "moisture_samples" : self.moisture_samples,
                        "moisture_threshold" : self.moisture_threshold,
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
    def moisture_threshold(self) -> int:
        return int(self._moisture_threshold)
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
    def lower_green_filter(self):
        return self._lower_green_filter
    @property
    def upper_green_filter(self):
        return self._upper_green_filter


if __name__ == "__main__":
    path = "misc"
    file = "settings.xml"
    planty_settings = PlantySetings(path, file)
    cam_settings = CameraSettings(path, file)

    print(f"duraion: {planty_settings.duration}")
    print(f"power: {planty_settings.power}")
    print(f"samples: {planty_settings.samples}")
    print(f"moisture threshold: {planty_settings.moisture_threshold}")
    print(f"light setpoint: {planty_settings.light_setpoint}")
    print(f"light max control: {planty_settings.light_max_control}")

    print(f"picture dir: {cam_settings.picture_directory}")
    print(f"picture copy dir: {cam_settings.picture_copy_directory}")
    print(f"lower green filter: {cam_settings.lower_green_filter}")
    print(f"upper green filter: {cam_settings.upper_green_filter}")
