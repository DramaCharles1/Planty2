from datetime import datetime
from PlantyLib import PlantyCommands
from DatabaseHandler import DataBaseHandler
from DatabaseHandler import Table
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
    main()
