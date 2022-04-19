import itertools
from typing import List
from typing import Any
from typing import Dict
import mysql.connector

def PlantyModel() -> Dict[str,str]:
    model = {"plant" : "plant VARCHAR(10) NOT NULL",
    "motor_duration" : "motor_duration INT NOT NULL",
    "motor_power" : "motor_power INT NOT NULL",
    "temperature" : "temperature FLOAT NOT NULL",
    "humidity" : "humidity FLOAT NOT NULL",
    "light" : "light INT NOT NULL",
    "moisture" : "moisture FLOAT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"
    }
    return model

def CameraModel() -> Dict[str,str]:
    model = {"original_pixel" : "original_pixel INT NOT NULL",
    "green_pixel" : "green_pixel INT NOT NULL",
    "green_percent" : "green_ercent FLOAT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"}
    return model

def SettingsModel() -> Dict[str,str]:
    model = {"motor_duration" : "motor_duration INT NOT NULL",
    "motor_power" : "motor_power INT NOT NULL",
    "moisture_samples" : "moisture_samples INT NOT NULL",
    "moisture_threshold" : "moisture_threshold INT NOT NULL",
    "light_setpoint" : "light_setpoint INT NOT NULL",
    "max_light" : "max_light INT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"}
    return model

def TestModel() -> Dict[str,str]:
    model = {"plant" : "plant VARCHAR(10) NOT NULL",
    "motor_duration" : "motor_duration INT NOT NULL",
    "motor_power" : "motor_power INT NOT NULL"}
    return model

class Table:
    def __init__(self, name : str, model : Dict[str,str]) -> None:
        self. name = name
        self.model = model

class DataBaseHandler:
    def __init__(self, host, user="root", password="password"):
        self.host = host
        self.user = user
        self.password = password
        self.cursor = None
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password)
            self.cursor = self.conn.cursor()

        except mysql.connector.Error as e:
            print(f"Could not connect to database: {e}")

    def connect_to_database(self, database):
        if not self._database_exist:
            raise Exception(f"Database {database} does not exist")
        try:
            self.conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = database)
            self.cursor = self.conn.cursor()

        except mysql.connector.Error as e:
            print(f"Could not connect to database: {e}")

    def create_database(self, new_database) -> bool:
        if self._database_exist(new_database):
            print(f"DEBUG: Database {new_database} already exist")
            return False
        insert_statement = f"CREATE DATABASE {new_database}"
        self.cursor.execute(insert_statement)
        print(f"DEBUG: Database {new_database} created")
        return True

    def delete_database(self, remove_database):
        insert_statement = f"DROP DATABASE {remove_database}"
        if self._database_exist(remove_database):
            self.cursor.execute(insert_statement)
            print(f"DEBUG: Database {remove_database} deleted")
            return True
        print(f"DEBUG: Database {remove_database} does not exist")
        return False

    def _database_exist(self, database_check: str) -> bool:
        for database in self._get_databases():
            if database_check in database:
                return True
        return False

    def _get_databases(self) -> List[str]:
        insert_statement = "SHOW DATABASES"
        self.cursor.execute(insert_statement)
        databases = self.cursor.fetchall()
        return list(itertools.chain(*databases))

    def close_database_connection(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def create_table(self, table_name: str, table: List[str]):
        column_string = ""
        for column in table:
            column_string += f"{column}, "
        column_string = column_string[0:len(column_string)-2]
        insert_statement = f"CREATE TABLE {table_name}({column_string})"
        try:
            self.cursor.execute(insert_statement)
            return True
        except mysql.connector.errors.ProgrammingError as e:
            print(f"DEBUG: {e}")
            return False

    def delete_table(self, table_name: str):
        insert_statement = f"DROP TABLE {table_name}"
        try:
            self.cursor.execute(insert_statement)
            return True
        except mysql.connector.errors.ProgrammingError as e:
            print(f"DEBUG: {e}")
            return False

    def insert_into_table(self, table_name: str, table: Dict[str,Any]):
        insert_statement_start = f"INSERT INTO {table_name} "
        insert_statement_colums = "("
        for column in table.keys():
            insert_statement_colums += f"{column},"
        insert_statement_colums = insert_statement_colums[0:len(insert_statement_colums)-1]
        insert_statement_colums += ") "
        insert_statement_values = f"VALUES ("
        for column in table.keys():
            insert_statement_values += f"%s,"
        insert_statement_values = insert_statement_values[0:len(insert_statement_values)-1]
        insert_statement_values += ")"
        insert_statement = insert_statement_start + insert_statement_colums + insert_statement_values
        print(insert_statement)
        print(type(table.values()))
        try:
            self.cursor.execute(insert_statement, list(table.values()))
            return True
        except mysql.connector.errors.ProgrammingError as e:
            print(f"DEBUG: {e}")
            return False

if __name__ == "__main__":
    print("Test database handler")
    host = "localhost"
    database = "test_planty3"
    table = "test1"
    PlantData = "lol"
    columns = ["plant VARCHAR(10) NOT NULL",
            "motor VARCHAR(10) NOT NULL",
            "temperature VARCHAR(10) NOT NULL"]

    databaseHandler = DataBaseHandler(host)
    databaseHandler.connect()
    databaseHandler.create_database(database)
    temp = databaseHandler._get_databases()
    for database in temp:
        print(database)
    databaseHandler.close_database_connection()
    databaseHandler.connect_to_database(database)
    test_table = Table("test", TestModel())
    databaseHandler.create_table(test_table.name, test_table.model.values())
    test = {"plant" : "Basil2", "motor_duration" : 40000, "motor_power" : 100}
    databaseHandler.insert_into_table(test_table.name, test)

    '''    planty_table = Table("planty", PlantyModel())
    camera_table = Table("camera", CameraModel())
    settings_table = Table("settings", SettingsModel())
    print("DEBUG new:")
    databaseHandler.create_table(planty_table.name, planty_table.model.values())
    databaseHandler.create_table(camera_table.name, camera_table.model.values())
    databaseHandler.create_table(settings_table.name, settings_table.model.values())
    print("DEBUG: insert table")
    planty_values = ["Basil", 30000, 100, 24.00, 46.00, 15000, 500.00, "2019-12-19T22:07:25"]
    databaseHandler.insert_into_table(planty_table.name, planty_table.model.keys(), planty_values)'''
    #databaseHandler.delete_table(planty_table.name)
    #databaseHandler.delete_table(camera_table.name)
    #databaseHandler.delete_table(settings_table.name)
