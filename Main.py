import sys
import os
from SettingsHandler import PlantySetings
from SettingsHandler import CameraSettings

def main(settings_path, settings_file, camera, nightmode):
    planty_settings = PlantySetings(settings_path, settings_file)
    camera_settings = CameraSettings(settings_path, settings_file)

if __name__ == "__main__":
    #args: settings_path, settings_file, camera, nightmode
    print("main test")
    test_argv = ["misc/", "settings.xml", False, False]

    if len(test_argv) is not 4:
        raise Exception(f"Arguements not correct: {test_argv}")
    main(test_argv[0], test_argv[1], test_argv[2], test_argv[3])

    print("End main test")