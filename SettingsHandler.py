import os
from xml.dom import minidom

class SettingsHandler:
    def __init__(self, path, file) -> None:
        self.path = path
        self.file = file

        settings_file = os.path.join(self.path, self.file)
        if not os.path.exists(settings_file):
            raise FileNotFoundError(f"{settings_file} was not found")

        mydoc = minidom.parse(settings_file)
        plantyDatas = mydoc.getElementsByTagName('planty_settings') 

        self._duration = plantyDatas[0].getElementsByTagName("duration")[0].firstChild.data.strip()
        self._power = plantyDatas[0].getElementsByTagName("power")[0].firstChild.data.strip()
        self._samples = plantyDatas[0].getElementsByTagName("samples")[0].firstChild.data.strip()
        self._moisture_threshold = plantyDatas[0].getElementsByTagName("mois_thres")[0].firstChild.data.strip()
        self._light_setpoint = plantyDatas[0].getElementsByTagName("setpoint")[0].firstChild.data.strip()
        self._light_max_control = plantyDatas[0].getElementsByTagName("max_control")[0].firstChild.data.strip()

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

if __name__ == "__main__":
    print(os.path.exists("misc/settings.xml"))
    path = "misc"
    file = "settings.xml"
    settings_handler = SettingsHandler(path, file)

    print(f"duraion: {settings_handler.duration}")
    print(f"power: {settings_handler.power}")
    print(f"samples: {settings_handler.samples}")
    print(f"moisture threshold: {settings_handler.moisture_threshold}")
    print(f"light setpoint: {settings_handler.light_setpoint}")
    print(f"light max control: {settings_handler.light_max_control}")