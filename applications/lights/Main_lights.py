import time
from datetime import datetime
from LightSettings import LightSetings
from PlantyLib import PlantyCommands

def main(settings_path, settings_file, nightmode,test=False):
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    print(f"[START] {timestamp}")
    light_settings = LightSetings(settings_path, settings_file)
    planty_lib = PlantyCommands()

    if not nightmode:
        planty_lib.light_regulator_values(True, light_settings.kp, light_settings.ki, light_settings.integration_time, light_settings.max_light)
        planty_lib.start_light_regulator(True, light_settings.light_setpoint)

if __name__ == "__main__":
    import sys
    print("main test")
    if len(sys.argv) == 1:
        test_argv = ["applications/planty/", "settings.xml", "True", True]
        main(test_argv)
    else:
        print(f"[ARGUEMENTS] {sys.argv}")
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print("End main test")