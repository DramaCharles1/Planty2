import itertools
from typing import List
import mysql.connector

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
    databaseHandler.create_table(table, columns)
    databaseHandler.delete_table(table)
