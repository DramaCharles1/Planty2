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
    "green_percent" : "green_percent FLOAT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"}
    return model

def PlantySettingsModel() -> Dict[str,str]:
    '''SQL settings Table model'''
    model = {"motor_duration" : "motor_duration INT NOT NULL",
    "motor_power" : "motor_power INT NOT NULL",
    "moisture_samples" : "moisture_samples INT NOT NULL",
    "moisture_threshold" : "moisture_threshold INT NOT NULL",
    "light_setpoint" : "light_setpoint INT NOT NULL",
    "max_light" : "max_light INT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"}
    return model

def CameraSettingsModel() -> Dict[str,str]:
    model = {"picture_directory" : "picture_directory VARCHAR(20) NOT NULL",
    "picture_copy_directory" : "picture_copy_directory VARCHAR(20) NOT NULL",
    "l1" : "l1 INT NOT NULL",
    "l2" : "l2 INT NOT NULL",
    "l3" : "l3 INT NOT NULL",
    "u1" : "u1 INT NOT NULL",
    "u2" : "u2 INT NOT NULL",
    "u3" : "u3 INT NOT NULL",
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
        self.columns = model.values()

class DataBaseHandler:
    '''Database handler class'''
    def __init__(self, host="localhost", user="root", password="password"):
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
        if not self.database_exist:
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
        if self.database_exist(new_database):
            print(f"[DEBUG] Database {new_database} already exist")
            return False
        insert_statement = f"CREATE DATABASE {new_database}"
        self.cursor.execute(insert_statement)
        print(f"[DEBUG] Database {new_database} created")
        return True

    def delete_database(self, remove_database):
        '''Delete database. Returns False if does not exist'''
        insert_statement = f"DROP DATABASE {remove_database}"
        if self.database_exist(remove_database):
            self.cursor.execute(insert_statement)
            print(f"[DEBUG] Database {remove_database} deleted")
            return True
        print(f"[DEBUG] Database {remove_database} does not exist")
        return False

    def database_exist(self, database_check: str) -> bool:
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
            print(f"[DEBUG] {program_error}")
            return False

    def table_exist(self, table_check: str) -> bool:
        for table in self._get_tables():
            if table_check in table:
                return True
        return False

    def _get_tables(self) -> List[str]:
        insert_statement = "SHOW TABLES"
        self.cursor.execute(insert_statement)
        tables = self.cursor.fetchall()
        return list(itertools.chain(*tables))

    def delete_table(self, table_name: str):
        '''Delete table_name table form current database'''
        insert_statement = f"DROP TABLE {table_name}"
        try:
            self.cursor.execute(insert_statement)
            return True
        except mysql.connector.errors.ProgrammingError as program_error:
            print(f"[DEBUG] {program_error}")
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
        try:
            self.cursor.execute(insert_statement, values)
            self._commit()
            return True
        except mysql.connector.errors.ProgrammingError as program_error:
            print(f"[DEBUG] {program_error}")
            return False

    def select_from_table(self, table_name: str, columns: List[str], order=False, order_by=None, limit=0):
        '''Select columns from table_name from current database'''
        insert_columns = ""
        for column in columns:
            insert_columns += f"{column}, "
        insert_columns = insert_columns[0:len(insert_columns)-2]
        insert_statement = f"SELECT {insert_columns} FROM {table_name}"
        if order:
            insert_order = f" order by {order_by} desc"
            insert_statement += insert_order
        if limit > 0:
            insert_limit = f" limit {limit}"
            insert_statement += insert_limit
        try:
            self.cursor.execute(insert_statement)
            return self.cursor.fetchall()
        except mysql.connector.errors.ProgrammingError as program_error:
            print(f"[DEBUG] {program_error}")
            raise program_error

    def _commit(self) -> bool:
        try:
            self.connection.commit()
            return True
        except mysql.connector.Error as connect_error:
            print(f"[DEBUG] {connect_error}")
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
    databaseHandler.create_table(test_table.name, test_table.columns)
    test_data= {"plant" : "Basil55", "motor_duration" : 50000, "motor_power" : None}
    databaseHandler.insert_into_table(test_table.name, test_data)
    temp = databaseHandler.select_from_table(table, list(test_data.keys()))
    print(temp)
    select_cols = ["plant","motor_duration"]
    temp = databaseHandler.select_from_table(table, select_cols)
    print(temp)
    temp = databaseHandler.select_from_table(table, select_cols, order=True, order_by="motor_duration")
    print(temp)
    temp = databaseHandler.select_from_table(table, select_cols, order=True, order_by="motor_duration", limit=10)
    print(temp)
    #databaseHandler.delete_table(planty_table.name)
    #databaseHandler.delete_table(camera_table.name)
    #databaseHandler.delete_table(settings_table.name)
