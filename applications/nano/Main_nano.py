import sys
from datetime import datetime
from PlantyLib import PlantyCommands
from PlantyLib import Temp_option
from DatabaseHandler import DataBaseHandler
from Model_nano import NanoModel

DATABASE = "nano"
TABLE = "nano_data"
MOIS_SAMPLES = 5
MOIS_SENSORS = 2

def main():
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    print(f"[START] {timestamp}")
    database_handler = DataBaseHandler()
    database_handler.connect()
    if not database_handler.database_exist(DATABASE):
        database_handler.create_database(DATABASE)
    database_handler.close_database_connection()
    database_handler.connect_to_database(DATABASE)

    planty_lib = PlantyCommands("/dev/ttyUSB0")
    planty_result = {}
    plant = planty_lib.read_plant()
    print(f"[DEBUG] Plant: {plant}")
    planty_result["plant_1"] = plant
    planty_result["plant_2"] = plant
    
    for sensor in range(1, MOIS_SENSORS + 1):
        moisture_result = planty_lib.read_moisture(sensor_number=sensor, samples=MOIS_SAMPLES)
        print(moisture_result["sensor_number_return"])
        print(moisture_result["sensor_read"])
    temperature = planty_lib.read_temperature(Temp_option.TEMPERATURE)
    print(f"[DEBUG] Temperature: {temperature}")
    planty_result["temperature"] = temperature
    humidity = planty_lib.read_temperature(Temp_option.HUMIDITY)
    print(f"[DEBUG] Humidity: {humidity}")
    planty_result["humidity"] = humidity

if __name__ == "__main__":
    if len(sys.argv) == 1:
        test_argv = ["misc/", "settings.xml", "True", "False", True]
        print("main test")
        main()
        print("End main test")
