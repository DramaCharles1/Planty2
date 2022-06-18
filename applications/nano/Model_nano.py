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

if __name__ == "__main__":
    from DatabaseHandler import DataBaseHandler
    from DatabaseHandler import Table
    print("test nano model")
    host = "localhost"
    database = "nano"
    table = "nano"
    databaseHandler = DataBaseHandler(host)
    databaseHandler.connect()
    databaseHandler.create_database(database)
    databaseHandler.close_database_connection()
    databaseHandler.connect_to_database(database)
    test_table = Table(table, NanoModel())
    databaseHandler.create_table(test_table.name, test_table.columns)
    test_data= {"entry": 1,
    "plant_1": "basilika",
    "moisture_1": "100",
    "plant_2": "sallad",
    "moisture_2": "100",
    "temperature": 25.0,
    "humidity": 40.0,
    "datetime": None}
    databaseHandler.insert_into_table(test_table.name, test_data)
    select_cols = ["plant_1","moisture_1","temperature"]
    temp = databaseHandler.select_from_table(table, select_cols)
    print(temp)
    databaseHandler.close_database_connection()
