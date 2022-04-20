import itertools
from typing import List
from typing import Any
from typing import Dict
import mysql.connector

def PlantyModel() -> Dict[str,str]:
    '''SQL planty Table model'''
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
    '''SQL camera Table model'''
    model = {"original_pixel" : "original_pixel INT NOT NULL",
    "green_pixel" : "green_pixel INT NOT NULL",
    "green_percent" : "green_ercent FLOAT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"}
    return model

def SettingsModel() -> Dict[str,str]:
    '''SQL settings Table model'''
    model = {"motor_duration" : "motor_duration INT NOT NULL",
    "motor_power" : "motor_power INT NOT NULL",
    "moisture_samples" : "moisture_samples INT NOT NULL",
    "moisture_threshold" : "moisture_threshold INT NOT NULL",
    "light_setpoint" : "light_setpoint INT NOT NULL",
    "max_light" : "max_light INT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"}
    return model

def TestModel() -> Dict[str,str]:
    '''SQL test Table model'''
    model = {"plant" : "plant VARCHAR(10) NOT NULL",
    "motor_duration" : "motor_duration INT NOT NULL",
    "motor_power" : "motor_power INT NOT NULL"}
    return model

class Table:
    '''Class represents SQL table. Translates model to
    Dict'''
    def __init__(self, name : str, model : Dict[str,str]) -> None:
        self. name = name
        self.model = model

class DataBaseHandler:
    '''Database handler class'''
    def __init__(self, host, user="root", password="password"):
        self.host = host
        self.user = user
        self.password = password
        self.cursor = None
        self.connection = None

    def connect(self):
        '''SQL connection'''
        try:
            self.connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password)
            self.cursor = self.connection.cursor()

        except mysql.connector.Error as connect_error:
            print(f"Could not connect to database: {connect_error}")

    def connect_to_database(self, database):
        '''Connect to database. The cursor will point to database'''
        if not self._database_exist:
            raise Exception(f"Database {database} does not exist")
        try:
            self.connection = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = database)
            self.cursor = self.connection.cursor()

        except mysql.connector.Error as connect_error:
            print(f"Could not connect to database: {connect_error}")

    def create_database(self, new_database) -> bool:
        '''Create new database. Returns False if already exist'''
        if self._database_exist(new_database):
            print(f"DEBUG: Database {new_database} already exist")
            return False
        insert_statement = f"CREATE DATABASE {new_database}"
        self.cursor.execute(insert_statement)
        print(f"DEBUG: Database {new_database} created")
        return True

    def delete_database(self, remove_database):
        '''Delete database. Returns False if does not exist'''
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
        '''Close database and SQL connection'''
        self.cursor.close()
        self.connection.close()

    def create_table(self, table_name: str, table: List[str]):
        '''Create table_name table in current database. Table is a List[str]
        that represents all columns, their types and allowed NULL'''
        column_string = ""
        for column in table:
            column_string += f"{column}, "
        column_string = column_string[0:len(column_string)-2]
        insert_statement = f"CREATE TABLE {table_name}({column_string})"
        try:
            self.cursor.execute(insert_statement)
            return True
        except mysql.connector.errors.ProgrammingError as program_error:
            print(f"DEBUG: {program_error}")
            return False

    def delete_table(self, table_name: str):
        '''Delete table_name table form current database'''
        insert_statement = f"DROP TABLE {table_name}"
        try:
            self.cursor.execute(insert_statement)
            return True
        except mysql.connector.errors.ProgrammingError as program_error:
            print(f"DEBUG: {program_error}")
            return False

    def insert_into_table(self, table_name: str, table: Dict[str,Any]):
        '''Insert table data into table_name table. Not all columns need to
        be filled'''
        insert_statement_start = f"INSERT INTO {table_name} "
        insert_statement_colums = "("
        insert_statement_values = "VALUES ("
        values = []
        for column in table.keys():
            if not table[column] is None:
                insert_statement_colums += f"{column},"
                insert_statement_values += "%s,"
                values.append(table[column])
        insert_statement_colums = insert_statement_colums[0:len(insert_statement_colums)-1]
        insert_statement_values = insert_statement_values[0:len(insert_statement_values)-1]
        insert_statement_colums += ") "
        insert_statement_values += ")"
        insert_statement = insert_statement_start + insert_statement_colums + insert_statement_values
        print(insert_statement)
        print(values)
        try:
            self.cursor.execute(insert_statement, values)
            self._commit()
            return True
        except mysql.connector.errors.ProgrammingError as program_error:
            print(f"DEBUG: {program_error}")
            return False

    def _commit(self) -> bool:
        try:
            self.connection.commit()
            return True
        except mysql.connector.Error as connect_error:
            print(f"DEBUG: {connect_error}")
            return False

if __name__ == "__main__":
    print("Test database handler")
    host = "localhost"
    database = "test_planty99"
    table = "test99"
    databaseHandler = DataBaseHandler(host)
    databaseHandler.connect()
    databaseHandler.create_database(database)
    temp = databaseHandler._get_databases()
    for database in temp:
        print(database)
    databaseHandler.close_database_connection()
    databaseHandler.connect_to_database(database)
    test_table = Table(table, TestModel())
    databaseHandler.create_table(test_table.name, test_table.model.values())
    test_data= {"plant" : "Basil55", "motor_duration" : 50000, "motor_power" : None}
    databaseHandler.insert_into_table(test_table.name, test_data)
    #databaseHandler.delete_table(planty_table.name)
    #databaseHandler.delete_table(camera_table.name)
    #databaseHandler.delete_table(settings_table.name)
