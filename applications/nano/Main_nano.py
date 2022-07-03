from datetime import datetime
from Model_nano import NanoModel
from Model_nano import NanoSettingsModel
from PlantyLib import PlantyCommands
from DatabaseHandler import DataBaseHandler
from DatabaseHandler import Table
from applications.nano.NanoSettings import NanoSettings
from PlotHandler import Plot

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

    day_length = 23
    day_plot_data = database_handler.select_from_table(TABLE, ["Datetime","moisture_1","moisture_2"], True, "Datetime", day_length)
    if len(day_plot_data) < day_length:
        day_plot_data = database_handler.select_from_table(TABLE, ["Datetime","moisture_1","moisture_2"], True, "Datetime", len(day_plot_data) - 1)

    timex = [str(x[0].time().isoformat(timespec='minutes')) for x in day_plot_data]
    moisture_plant1 = [y[1] for y in day_plot_data]
    moisture_plant2 = [y[2] for y in day_plot_data]

    moisture_plant1_data_dict = {"x_label" : "Time",
                "y_label" : planty_result["plant_1"],
                "x_data" : [timex, timex],
                "y_data" : [moisture_plant1, [nano_settings.moisture_threshold] * len(day_plot_data)],
                "label" : ["Moisture","Limit"]}

    moisture_plot1 = Plot(moisture_plant1_data_dict)
    moisture_plot1.create_lineplot(limit_x_label=True)
    if not test:
        moisture_plot1.save_plot(nano_settings.settings["picture_copy_directory"], "moisture_plant1_plot_day")
    else:
        moisture_plot1.save_plot(f"{nano_settings.picture_directory}/test", "moisture_plant1_plot_day")

    moisture_plant2_data_dict = {"x_label" : "Time",
                "y_label" : planty_result["plant_2"],
                "x_data" : [timex, timex],
                "y_data" : [moisture_plant2, [nano_settings.moisture_threshold] * len(day_plot_data)],
                "label" : ["Moisture","Limit"]}
    moisture_plot2 = Plot(moisture_plant2_data_dict)
    moisture_plot2.create_lineplot(limit_x_label=True)

    if not test:
        moisture_plot2.save_plot(nano_settings.settings["picture_copy_directory"], "moisture_plant2_plot_day")
    else:
        moisture_plot2.save_plot(f"{nano_settings.picture_directory}/test", "moisture_plant2_plot_day")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        test_argv = ["applications/nano/", "settings.xml", True]
        print("main test")
        print(f"[ARGUEMENTS] {test_argv}")
        main(test_argv[0], test_argv[1], test_argv[2])
        print("End main test")
    elif len(sys.argv) == 3:
        print(f"[ARGUEMENTS] {sys.argv}")
        main(sys.argv[1], sys.argv[2], False)
    else:
        if len(sys.argv) < 4:
            raise Exception(f"[DEBUG] Not enough arguements: {sys.argv}, length: {len(sys.argv)}")
        raise Exception(f"[DEBUG] Too many arguments: {sys.argv}")
