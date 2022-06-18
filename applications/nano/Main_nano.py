import sys
from datetime import datetime
from PlantyLib import PlantyCommands

MOIS_SAMPLES = 5
MOIS_SENSORS = 2

def main():
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    print(f"[START] {timestamp}")
    planty_lib = PlantyCommands("/dev/ttyUSB0")

    planty_result = {}
    planty_result["plant"] = planty_lib.read_plant()
    print(planty_result["plant"])
    for sensor in range(1, MOIS_SENSORS + 1):
        moisture_result = planty_lib.read_moisture(sensor_number=sensor, samples=MOIS_SAMPLES)
        print(moisture_result["sensor_number_return"])
        print(moisture_result["sensor_read"])

if __name__ == "__main__":
    if len(sys.argv) == 1:
        test_argv = ["misc/", "settings.xml", "True", "False", True]
        print("main test")
        main()
        print("End main test")
