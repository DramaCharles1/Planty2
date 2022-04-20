from datetime import datetime
from SettingsHandler import PlantySetings
from SettingsHandler import CameraSettings
from DatabaseHandler import DataBaseHandler
from DatabaseHandler import Table
from DatabaseHandler import SettingsModel

PLANTY_DATABASE = "Planty2"
PLANTY_TABLE = "Planty_data"
SETTINGS_TABLE = "Planty_settings"

def main(settings_path, settings_file, camera, nightmode):
    timestamp = datetime.now().replace(microsecond=0).isoformat()
    planty_settings = PlantySetings(settings_path, settings_file)
    camera_settings = CameraSettings(settings_path, settings_file)
    database_handler = DataBaseHandler()
    database_handler.connect()

    if not database_handler.database_exist(PLANTY_DATABASE):
        database_handler.create_database(PLANTY_DATABASE)
    database_handler.close_database_connection()
    database_handler.connect_to_database(PLANTY_DATABASE)
    
    if not database_handler.table_exist(SETTINGS_TABLE):
        new_settings_table = Table(SETTINGS_TABLE, SettingsModel())
        database_handler.create_table(new_settings_table.name, new_settings_table.columns)

    last_planty_settings = {"motor_duration" : database_handler.select_from_table(SETTINGS_TABLE, ["motor_duration"], True, "datetime", limit=1)[0][0],
                        "motor_power" : database_handler.select_from_table(SETTINGS_TABLE, ["motor_power"], True, "datetime", limit=1)[0][0],
                        "moisture_samples" : database_handler.select_from_table(SETTINGS_TABLE, ["moisture_samples"], True, "datetime", limit=1)[0][0],
                        "moisture_threshold" : database_handler.select_from_table(SETTINGS_TABLE, ["moisture_threshold"], True, "datetime", limit=1)[0][0],
                        "light_setpoint" : database_handler.select_from_table(SETTINGS_TABLE, ["light_setpoint"], True, "datetime", limit=1)[0][0],
                        "max_light" : database_handler.select_from_table(SETTINGS_TABLE, ["max_light"], True, "datetime", limit=1)[0][0]}
    new__planty_settings = {}
    update_settings_database = False
    for setting in last_planty_settings.keys():
        if not last_planty_settings[setting] == planty_settings.settings[setting]:
            update_settings_database = True
            new__planty_settings[setting] = planty_settings.settings[setting]
        else:
            new__planty_settings[setting] = last_planty_settings[setting]
    if update_settings_database:
        new__planty_settings["datetime"] = timestamp
        database_handler.insert_into_table(SETTINGS_TABLE, new__planty_settings)


if __name__ == "__main__":
    #args: settings_path, settings_file, camera, nightmode
    print("main test")
    test_argv = ["misc/", "settings.xml", False, False]

    if len(test_argv) is not 4:
        raise Exception(f"Arguements not correct: {test_argv}")
    main(test_argv[0], test_argv[1], test_argv[2], test_argv[3])

    print("End main test")