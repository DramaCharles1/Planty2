from typing import Dict

def NanoModel() -> Dict[str,str]:
    '''SQL nano Table model'''
    model = {"entry" : "entry INT NOT NULL",
    "plant_1" : "plant_1 VARCHAR(10) NOT NULL",
    "moisture_1" : "moisture_1 FLOAT NOT NULL",
    "plant_2" : "plant_2 VARCHAR(10) NOT NULL",
    "moisture_2" : "moisture_2 FLOAT NOT NULL",
    "temperature" : "temperature FLOAT NOT NULL",
    "humidity" : "humidity FLOAT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"
    }
    return model

def NanoSettingsModel() -> Dict[str,str]:
    '''SQL settings Table model'''
    model = {"moisture_samples" : "moisture_samples FLOAT NOT NULL",
    "moisture_threshold" : "moisture_threshold FLOAT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"}
    return model

if __name__ == "__main__":
    from DatabaseHandler import DataBaseHandler
    from DatabaseHandler import Table
    print("test nano model")
    host = "localhost"
    database = "nano"
    table = "nano_settings_test"
    databaseHandler = DataBaseHandler(host)
    databaseHandler.connect()
    databaseHandler.create_database(database)
    databaseHandler.close_database_connection()
    databaseHandler.connect_to_database(database)
    test_table = Table(table, NanoSettingsModel())
    databaseHandler.create_table(test_table.name, test_table.columns)
    test_data= {"moisture_samples": 5.0,
    "moisture_threshold": 500.0,
    "datetime": None}
    databaseHandler.insert_into_table(test_table.name, test_data)
    select_cols = ["moisture_samples","moisture_threshold","datetime"]
    temp = databaseHandler.select_from_table(table, select_cols)
    print(temp)
    databaseHandler.close_database_connection()
