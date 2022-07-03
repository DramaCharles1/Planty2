import os
from typing import List
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
