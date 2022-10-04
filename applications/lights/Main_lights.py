from datetime import datetime
from PlantyLib import Light_color_option
from PlantyLib import PlantyCommands
from LightSettings import LightSetings

def main(settings_path, settings_file, nightmode):
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    print(f"[START] {timestamp}")
    light_settings = LightSetings(settings_path, settings_file)
    planty_lib = PlantyCommands()

    if not nightmode:
        planty_lib.light_regulator_values(True, light_settings.kp, light_settings.ki, light_settings.integration_time, light_settings.max_light)
        planty_lib.start_light_regulator(True, light_settings.light_setpoint)
    else:
        planty_lib.lights(True, Light_color_option.PURPLE, power=0)

if __name__ == "__main__":
    import sys
    print("main test")
    if len(sys.argv) == 1:
        test_argv = ["applications/lights/", "settings.xml", True]
        main(test_argv[0],test_argv[1],test_argv[2])
    else:
        print(f"[ARGUEMENTS] {sys.argv}")
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    print("End main test")
