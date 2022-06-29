from datetime import datetime
from Model_nano import NanoModel
from PlantyLib import PlantyCommands
from DatabaseHandler import DataBaseHandler
from DatabaseHandler import Table

DATABASE = "nano"
TABLE = "nano_data"
MOIS_SAMPLES = 5
MOIS_SENSORS = 2

def main(settings_path, settings_file, test=False):
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    print(f"[START] {timestamp}")

    database_handler = DataBaseHandler()
    database_handler.connect()

    if not database_handler.database_exist(DATABASE):
        database_handler.create_database(DATABASE)
    database_handler.close_database_connection()
    database_handler.connect_to_database(DATABASE)

    if not database_handler.table_exist(TABLE):
        new_table = Table(TABLE, NanoModel())
        database_handler.create_table(new_table.name, new_table.columns)
        database_handler.insert_into_table(TABLE,{"entry" : 1})

    planty_lib = PlantyCommands("/dev/ttyUSB0")
    planty_result = {}
    planty_result["datetime"] = timestamp
    plant = planty_lib.read_plant()
    planty_result["plant_1"] = plant
    planty_result["plant_2"] = plant

    for sensor in range(1, MOIS_SENSORS + 1):
        moisture_result = planty_lib.read_moisture(sensor_number=sensor, samples=MOIS_SAMPLES)
        planty_result[f"moisture_{moisture_result['sensor_number_return']}"] = moisture_result["sensor_read"]
    new_entry = database_handler.select_from_table(TABLE, ["entry"], True, "Datetime", 1)[0][0] + 1
    planty_result["entry"] = new_entry

    database_handler.insert_into_table(TABLE, planty_result)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        test_argv = ["applications/nano/", "settings.xml", True]
        print("main test")
        main(test_argv[0], test_argv[1], test_argv[2])
        print("End main test")
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        if len(sys.argv) < 4:
            raise Exception(f"[DEBUG] Not enough arguements: {sys.argv}")
        raise Exception(f"[DEBUG] Too many arguments: {sys.argv}")
