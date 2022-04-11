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

        self._duration = planty_settings[0].getElementsByTagName("duration")[0].firstChild.data.strip()
        self._power = planty_settings[0].getElementsByTagName("power")[0].firstChild.data.strip()
        self._samples = planty_settings[0].getElementsByTagName("samples")[0].firstChild.data.strip()
        self._moisture_threshold = planty_settings[0].getElementsByTagName("mois_thres")[0].firstChild.data.strip()
        self._light_setpoint = planty_settings[0].getElementsByTagName("setpoint")[0].firstChild.data.strip()
        self._light_max_control = planty_settings[0].getElementsByTagName("max_control")[0].firstChild.data.strip()

    @property
    def duration(self) -> int:
        return self._duration
    @property
    def power(self) -> int:
        return self._power
    @property
    def samples(self) -> int:
        return self._samples
    @property
    def moisture_threshold(self) -> int:
        return self._moisture_threshold
    @property
    def light_setpoint(self) -> int:
        return self._light_setpoint
    @property
    def light_max_control(self) -> int:
        return self._light_max_control

class CamSettings(SettingsHandler):
    '''
    Camera specifc settings
    '''
    def __init__(self, path, file) -> None:
        super().__init__(path, file)

        cam_settings = self.mydoc.getElementsByTagName('cam_settings')

        self._picture_directory = cam_settings[0].getElementsByTagName("pic_dir")[0].firstChild.data.strip()
        self._picture_copy_directory = cam_settings[0].getElementsByTagName("pic_copy_dir")[0].firstChild.data.strip()
        self._lower_green_filter = [int(cam_settings[0].getElementsByTagName("lower_green")[0].getAttribute("l1")),
                                    int(cam_settings[0].getElementsByTagName("lower_green")[0].getAttribute("l2")),
                                    int(cam_settings[0].getElementsByTagName("lower_green")[0].getAttribute("l3"))]
        self._upper_green_filter = [int(cam_settings[0].getElementsByTagName("upper_green")[0].getAttribute("u1")),
                                    int(cam_settings[0].getElementsByTagName("upper_green")[0].getAttribute("u2")),
                                    int(cam_settings[0].getElementsByTagName("upper_green")[0].getAttribute("u3"))]

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
    cam_settings = CamSettings(path, file)

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
