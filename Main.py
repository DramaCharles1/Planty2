import os
from datetime import datetime
import numpy as np
from CameraHandler import CameraHandler
from PlantyColor import PlantyColor
from SettingsHandler import PlantySetings
from SettingsHandler import CameraSettings
from DatabaseHandler import CameraModel, DataBaseHandler, PlantyModel
from DatabaseHandler import Table
from DatabaseHandler import PlantySettingsModel
from DatabaseHandler import CameraSettingsModel

PLANTY_DATABASE = "Planty2"
PLANTY_TABLE = "Planty_data"
CAMERA_TABLE = "Camera_data"
PLANTY_SETTINGS_TABLE = "Planty_settings"
CAMERA_SETTINGS_TABLE = "Camera_settings"

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

    if not database_handler.table_exist(PLANTY_SETTINGS_TABLE):
        new_table = Table(PLANTY_SETTINGS_TABLE, PlantySettingsModel())
        database_handler.create_table(new_table.name, new_table.columns)
        database_handler.insert_into_table(PLANTY_SETTINGS_TABLE,{"motor_duration" : 0})

    if not database_handler.table_exist(CAMERA_SETTINGS_TABLE):
        new_table = Table(CAMERA_SETTINGS_TABLE, CameraSettingsModel())
        database_handler.create_table(new_table.name, new_table.columns)
        database_handler.insert_into_table(CAMERA_SETTINGS_TABLE,{"picture_directory" : "lol"})

    if not database_handler.table_exist(PLANTY_TABLE):
        new_table = Table(PLANTY_TABLE, PlantyModel())
        database_handler.create_table(new_table.name, new_table.columns)
        database_handler.insert_into_table(PLANTY_TABLE,{"plant" : "lol"})

    if not database_handler.table_exist(CAMERA_TABLE):
        new_table = Table(CAMERA_TABLE, CameraModel())
        database_handler.create_table(new_table.name, new_table.columns)
        database_handler.insert_into_table(CAMERA_TABLE,{"original_pixel" : 0})

    last_planty_settings = {"motor_duration" : database_handler.select_from_table(PLANTY_SETTINGS_TABLE, ["motor_duration"], True, "datetime", limit=1)[0][0],
                        "motor_power" : database_handler.select_from_table(PLANTY_SETTINGS_TABLE, ["motor_power"], True, "datetime", limit=1)[0][0],
                        "moisture_samples" : database_handler.select_from_table(PLANTY_SETTINGS_TABLE, ["moisture_samples"], True, "datetime", limit=1)[0][0],
                        "moisture_threshold" : database_handler.select_from_table(PLANTY_SETTINGS_TABLE, ["moisture_threshold"], True, "datetime", limit=1)[0][0],
                        "light_setpoint" : database_handler.select_from_table(PLANTY_SETTINGS_TABLE, ["light_setpoint"], True, "datetime", limit=1)[0][0],
                        "max_light" : database_handler.select_from_table(PLANTY_SETTINGS_TABLE, ["max_light"], True, "datetime", limit=1)[0][0]}
    new_planty_settings = {}
    update_settings_database = False
    for setting in last_planty_settings.keys():
        if not last_planty_settings[setting] == planty_settings.settings[setting]:
            update_settings_database = True
            new_planty_settings[setting] = planty_settings.settings[setting]
        else:
            new_planty_settings[setting] = last_planty_settings[setting]
    if update_settings_database:
        new_planty_settings["datetime"] = timestamp
        database_handler.insert_into_table(PLANTY_SETTINGS_TABLE, new_planty_settings)

    last_camera_settings = {"picture_directory" : database_handler.select_from_table(CAMERA_SETTINGS_TABLE, ["picture_directory"], True, "datetime", limit=1)[0][0],
                        "picture_copy_directory" : database_handler.select_from_table(CAMERA_SETTINGS_TABLE, ["picture_copy_directory"], True, "datetime", limit=1)[0][0],
                        "l1" : database_handler.select_from_table(CAMERA_SETTINGS_TABLE, ["l1"], True, "datetime", limit=1)[0][0],
                        "l2" : database_handler.select_from_table(CAMERA_SETTINGS_TABLE, ["l2"], True, "datetime", limit=1)[0][0],
                        "l3" : database_handler.select_from_table(CAMERA_SETTINGS_TABLE, ["l3"], True, "datetime", limit=1)[0][0],
                        "u1" : database_handler.select_from_table(CAMERA_SETTINGS_TABLE, ["u1"], True, "datetime", limit=1)[0][0],
                        "u2" : database_handler.select_from_table(CAMERA_SETTINGS_TABLE, ["u2"], True, "datetime", limit=1)[0][0],
                        "u3" : database_handler.select_from_table(CAMERA_SETTINGS_TABLE, ["u3"], True, "datetime", limit=1)[0][0]}
    new_camera_settings = {}
    update_settings_database = False
    for setting in last_camera_settings.keys():
        if not last_camera_settings[setting] == camera_settings.settings[setting]:
            update_settings_database = True
            new_camera_settings[setting] = camera_settings.settings[setting]
        else:
            new_camera_settings[setting] = last_camera_settings[setting]
    if update_settings_database:
        new_camera_settings["datetime"] = timestamp
        database_handler.insert_into_table(CAMERA_SETTINGS_TABLE, new_camera_settings)

    if camera:
        planty_camera = CameraHandler()
        image_name = timestamp
        planty_camera.take_picture(camera_settings.picture_directory, image_name, nightmode=True)

        original_color = PlantyColor(camera_settings.picture_directory, image_name)
        green_image = original_color.color_filter_image(camera_settings.lower_green_filter, camera_settings.upper_green_filter)
        green_image_name = f"{image_name}_green"
        original_color.save_image(green_image, camera_settings.picture_directory, green_image_name)

        original_image_pixels = np.count_nonzero(original_color.original_image)
        green_image_pixels = np.count_nonzero(green_image)
        green_percent = round((green_image_pixels / original_image_pixels)*100, 1)
        print(f"original image pixels: {original_image_pixels}")
        print(f"green image pixels: {green_image_pixels}")
        print(f"green percent: {green_percent}")

        camera_result = {"original_pixel" : original_image_pixels,
                        "green_pixel" : green_image_pixels,
                        "green_percent" : green_percent,
                        "datetime" : timestamp}
        database_handler.insert_into_table(CAMERA_TABLE, camera_result)

if __name__ == "__main__":
    #args: settings_path, settings_file, camera, nightmode
    print("main test")
    test_argv = ["misc/", "settings.xml", True, False]

    if len(test_argv) != 4:
        raise Exception(f"Arguements not correct: {test_argv}")
    main(test_argv[0], test_argv[1], test_argv[2], test_argv[3])

    print("End main test")
