from datetime import datetime
from Model_nano import NanoModel
from Model_nano import NanoSettingsModel
from PlantyLib import PlantyCommands
from DatabaseHandler import DataBaseHandler
from DatabaseHandler import Table
from applications.nano.NanoSettings import NanoSettings

DATABASE = "nano"
TABLE = "nano_data"
SETTINGS_TABLE = "nano_settings"
MOIS_SAMPLES = 5
MOIS_SENSORS = 2

def main(settings_path, settings_file, test=False):
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    print(f"[START] {timestamp}")
    nano_settings = NanoSettings(settings_path, settings_file)

    database_handler = DataBaseHandler()
    database_handler.connect()

    if not database_handler.database_exist(DATABASE):
        database_handler.create_database(DATABASE)
    database_handler.close_database_connection()
    database_handler.connect_to_database(DATABASE)

    if not database_handler.table_exist(SETTINGS_TABLE):
        new_table = Table(SETTINGS_TABLE, NanoSettingsModel())
        database_handler.create_table(new_table.name, new_table.columns)
        database_handler.insert_into_table(SETTINGS_TABLE,{"moisture_samples" : 0.0})

    last_nano_settings = {"moisture_samples" : database_handler.select_from_table(SETTINGS_TABLE, ["moisture_samples"], True, "datetime", limit=1)[0][0],
                        "moisture_threshold" : database_handler.select_from_table(SETTINGS_TABLE, ["moisture_threshold"], True, "datetime", limit=1)[0][0],
                        }
    new_nano_settings = {}
    update_settings_database = False
    for setting in last_nano_settings.keys():
        if not last_nano_settings[setting] == nano_settings.settings[setting]:
            print(f"[DEBUG] update nano setting {setting} to {nano_settings.settings[setting]}")
            update_settings_database = True
            new_nano_settings[setting] = nano_settings.settings[setting]
        else:
            new_nano_settings[setting] = last_nano_settings[setting]
    if update_settings_database:
        new_nano_settings["datetime"] = timestamp
        if not test:
            database_handler.insert_into_table(SETTINGS_TABLE, new_nano_settings)

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
        test_argv = ["applications/nano/", "settings.xml", False]
        print("main test")
        main(test_argv[0], test_argv[1], test_argv[2])
        print("End main test")
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        if len(sys.argv) < 4:
            raise Exception(f"[DEBUG] Not enough arguements: {sys.argv}")
        raise Exception(f"[DEBUG] Too many arguments: {sys.argv}")
